"""P3 PDE bake-off: physics-informed neural network (PINN).

Benchmark (shared by all methods):
  u_t + u u_x = nu u_xx,  x in [0, 2pi] periodic,  t in [0, 0.5],  nu = 0.07
  phi(x,t) = exp(-(x-4t)^2/(4nu(t+1))) + exp(-(x-4t-2pi)^2/(4nu(t+1)))
  u(x,t)   = -2 nu phi_x/phi + 4      (Cole-Hopf)

Method: fully connected tanh network, torch (CUDA if available).
  - Periodicity by construction: the net sees (cos x, sin x, t/T) not (x, t).
  - Initial condition by construction: u(x,t) = u0(x) + t * NN(x,t).
  - The only loss term is the mean squared PDE residual at random collocation
    points (fixed seed). Adam, then L-BFGS (strong Wolfe), with a wall-clock cap.
Sizes: three (width, collocation count) pairs, scaled together.
Error: discrete L2 norm sqrt(dx * sum(err^2)) at t = 0.5 on a 2048-point grid,
       the same norm as the grid methods.
Order: a PINN has no a-priori convergence rate. theoretical_order = null.
       The observed slope is fit of log(err) vs log(h), h = sqrt(2pi*T/N_c),
       the mean collocation spacing in space-time. It is data, not a check.
"""
import json
import time
from pathlib import Path

import numpy as np
import torch

NU = 0.07
T_END = 0.5
L = 2.0 * np.pi
DEPTH = 4                                # hidden layers
SIZES = [(32, 2000), (64, 8000), (128, 32000)]   # (width, N_collocation)
ADAM_STEPS = 3000
LBFGS_ITERS = 4000
TIME_CAP_S = 80.0                        # wall-clock cap per size
N_EVAL = 2048
SEED = 1234

DEV = torch.device("cuda" if torch.cuda.is_available() else "cpu")
DT = torch.float32


def exact(x, t, nu=NU):
    """Numpy float64 Cole-Hopf solution (same formula as finite-difference.py)."""
    d = 4.0 * nu * (t + 1.0)
    a = x - 4.0 * t
    b = x - 4.0 * t - 2.0 * np.pi
    ea = np.exp(-a * a / d)
    eb = np.exp(-b * b / d)
    phi = ea + eb
    phi_x = -2.0 * a / d * ea - 2.0 * b / d * eb
    return -2.0 * nu * phi_x / phi + 4.0


def u0_torch(x, nu=NU):
    """Initial condition u(x,0) in torch ops (differentiable in x).
    Written as 4 + weighted mean of the two Gaussian slopes, to avoid 0/0."""
    d = 4.0 * nu
    a = x
    b = x - 2.0 * np.pi
    la, lb = -a * a / d, -b * b / d
    w = torch.softmax(torch.stack([la, lb]), dim=0)      # ea/phi, eb/phi
    phi_x_over_phi = w[0] * (-2.0 * a / d) + w[1] * (-2.0 * b / d)
    return -2.0 * nu * phi_x_over_phi + 4.0


class Net(torch.nn.Module):
    def __init__(self, width, depth=DEPTH):
        super().__init__()
        layers, n_in = [], 3
        for _ in range(depth):
            layers += [torch.nn.Linear(n_in, width), torch.nn.Tanh()]
            n_in = width
        layers.append(torch.nn.Linear(n_in, 1))
        self.mlp = torch.nn.Sequential(*layers)
        for m in self.mlp:
            if isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_normal_(m.weight)
                torch.nn.init.zeros_(m.bias)

    def forward(self, x, t):
        feats = torch.stack([torch.cos(x), torch.sin(x), t / T_END], dim=-1)
        return u0_torch(x) + t * self.mlp(feats).squeeze(-1)


def residual(net, x, t):
    u = net(x, t)
    u_x, u_t = torch.autograd.grad(u.sum(), (x, t), create_graph=True)
    u_xx = torch.autograd.grad(u_x.sum(), x, create_graph=True)[0]
    return u_t + u * u_x - NU * u_xx


def l2_error(net):
    dx = L / N_EVAL
    xe = np.arange(N_EVAL) * dx
    with torch.no_grad():
        xt = torch.tensor(xe, dtype=DT, device=DEV)
        tt = torch.full_like(xt, T_END)
        up = net(xt, tt).double().cpu().numpy()
    err = up - exact(xe, T_END)
    return float(np.sqrt(dx * np.sum(err * err)))


def train(width, n_col):
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    net = Net(width).to(DEV)
    g = torch.Generator(device="cpu").manual_seed(SEED)
    x = (torch.rand(n_col, generator=g) * L).to(DEV, DT).requires_grad_(True)
    t = (torch.rand(n_col, generator=g) * T_END).to(DEV, DT).requires_grad_(True)

    t0 = time.perf_counter()
    best = {"loss": float("inf"), "state": None}

    def snap(loss):
        if np.isfinite(loss) and loss < best["loss"]:
            best["loss"] = loss
            best["state"] = {k: v.detach().clone() for k, v in net.state_dict().items()}

    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.StepLR(opt, step_size=1000, gamma=0.5)
    adam_done = 0
    for it in range(ADAM_STEPS):
        opt.zero_grad()
        loss = residual(net, x, t).pow(2).mean()
        loss.backward()
        opt.step()
        sched.step()
        adam_done = it + 1
        if it % 100 == 0:
            snap(loss.item())
        if time.perf_counter() - t0 > 0.4 * TIME_CAP_S:
            break
    snap(loss.item())

    lbfgs = torch.optim.LBFGS(net.parameters(), lr=1.0, max_iter=LBFGS_ITERS,
                              history_size=50, tolerance_grad=1e-9,
                              tolerance_change=1e-12, line_search_fn="strong_wolfe")
    evals = {"n": 0, "timeout": False}

    class Timeout(Exception):
        pass

    def closure():
        if time.perf_counter() - t0 > TIME_CAP_S:
            evals["timeout"] = True
            raise Timeout
        lbfgs.zero_grad()
        loss = residual(net, x, t).pow(2).mean()
        loss.backward()
        evals["n"] += 1
        if evals["n"] % 50 == 0:
            snap(loss.item())
        return loss

    try:
        lbfgs.step(closure)
    except Timeout:
        pass
    with torch.enable_grad():
        final = residual(net, x, t).pow(2).mean().item()
    snap(final)
    net.load_state_dict(best["state"])
    return net, {
        "residual_loss": best["loss"],
        "adam_steps": adam_done,
        "lbfgs_evals": evals["n"],
        "lbfgs_hit_time_cap": evals["timeout"],
        "train_s": time.perf_counter() - t0,
        "params": sum(p.numel() for p in net.parameters()),
    }


def main():
    t0 = time.perf_counter()
    errors, info = [], []
    for width, n_col in SIZES:
        net, meta = train(width, n_col)
        e = l2_error(net)
        errors.append(e)
        info.append(meta)
        print(f"width={width:4d}  N_c={n_col:6d}  params={meta['params']:6d}  "
              f"adam={meta['adam_steps']}  lbfgs_evals={meta['lbfgs_evals']}  "
              f"loss={meta['residual_loss']:.3e}  L2 error={e:.6e}  "
              f"train={meta['train_s']:.1f}s")

    n_c = np.array([s[1] for s in SIZES], dtype=float)
    h = np.sqrt(L * T_END / n_c)
    err = np.array(errors)
    pairwise = [float(np.log(err[i] / err[i + 1]) / np.log(h[i] / h[i + 1]))
                for i in range(len(SIZES) - 1)]
    p_fit = float(np.polyfit(np.log(h), np.log(err), 1)[0])
    runtime = time.perf_counter() - t0
    print("pairwise slopes:", ", ".join(f"{p:.3f}" for p in pairwise))
    print(f"observed slope (all 3 sizes, vs h): {p_fit:.4f}")
    print(f"runtime: {runtime:.2f} s  device: {DEV}")

    # Self-check. No order assert: a PINN has no theoretical rate.
    # Checks are recorded, not fatal: a stochastic optimizer under a hard
    # wall-clock cap can miss a threshold, and that is a real result to
    # report (pass=False), not a reason to crash before writing the file.
    checks = [
        (bool(all(np.isfinite(err))), "non-finite error"),
        (bool(err[-1] < err[0]), "largest size is not better than smallest"),
        (bool(err[-1] < 2e-2), f"largest-size error {err[-1]} too large"),
        (bool(runtime < 300.0), "runtime over 5 minutes"),
    ]
    failed = [msg for ok, msg in checks if not ok]
    passed = len(failed) == 0
    if failed:
        print("SELF-CHECK FAILED:", "; ".join(failed))

    out = {
        "method": "pinn",
        "scheme": (f"PINN, tanh MLP depth {DEPTH}, inputs (cos x, sin x, t/T) for exact "
                   "periodicity, hard IC u=u0+t*NN, residual-only loss, Adam then L-BFGS, "
                   f"torch {torch.__version__} on {DEV}, float32"),
        "benchmark": "1D viscous Burgers, Cole-Hopf, nu=0.07, x in [0,2pi] periodic, t_end=0.5",
        "grids": [int(s[1]) for s in SIZES],
        "grids_meaning": "number of random collocation points N_c in [0,2pi]x[0,0.5]",
        "widths": [int(s[0]) for s in SIZES],
        "params": [m["params"] for m in info],
        "residual_loss": [m["residual_loss"] for m in info],
        "adam_steps": [m["adam_steps"] for m in info],
        "lbfgs_evals": [m["lbfgs_evals"] for m in info],
        "lbfgs_hit_time_cap": [m["lbfgs_hit_time_cap"] for m in info],
        "errors": errors,
        "error_norm": f"discrete L2: sqrt(dx*sum(err^2)) at t=0.5 on {N_EVAL} uniform points",
        "size_abscissa": "h = sqrt(2pi*0.5/N_c), mean collocation spacing; slope of log(err) vs log(h)",
        "pairwise_orders": pairwise,
        "observed_order": p_fit,
        "observed_order_fit": "least squares on all 3 sizes",
        "theoretical_order": None,
        "theoretical_order_note": ("none: PINN error is limited by optimization and network "
                                   "capacity; there is no a-priori rate in h"),
        "seed": SEED,
        "runtime_s": runtime,
        "pass": passed,
        "self_check_failures": failed,
    }
    path = Path(__file__).with_name("pinn-order.json")
    path.write_text(json.dumps(out, indent=2))
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
