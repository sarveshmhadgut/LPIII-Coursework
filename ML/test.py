import numpy as np
import matplotlib.pyplot as plt


def gradient_descent(
    gradient_func, x_start, learning_rate=0.1, n_iterations=50, tolerance=1e-06
):
    x = x_start
    history = [x]

    for i in range(n_iterations):
        gradient = gradient_func(x)

        x_new = x - learning_rate * gradient

        history.append(x_new)

        if abs(x_new - x) < tolerance:
            print(f"Converged after {i + 1} iterations")
            break

        x = x_new

    return x, history


def function(x):
    return (x + 3) ** 2


def gradient(x):
    return 2 * (x + 3)


x_start = 2
x_min, history = gradient_descent(gradient, x_start, learning_rate=0.1)

print(f"Starting point: x = {x_start}")
print(f"Local minima found at: x = {x_min:.6f}")
print(f"Function value at minima: y = {function(x_min):.6f}")

print("\n" + "=" * 80)
print("DETAILED ITERATION HISTORY")
print("=" * 80)
print(f"{'Iter':<6} {'x':<15} {'y=(x+3)²':<15} {'Gradient':<15} {'Step Size':<15}")
print("-" * 80)

for i in range(len(history)):
    x_val = history[i]
    y_val = function(x_val)
    grad_val = gradient(x_val)

    if i < len(history) - 1:
        step_size = abs(history[i] - history[i + 1])
        print(
            f"{i:<6} {x_val:<15.8f} {y_val:<15.8f} {grad_val:<15.8f} {step_size:<15.8f}"
        )
    else:
        print(f"{i:<6} {x_val:<15.8f} {y_val:<15.8f} {grad_val:<15.8f} {'FINAL':<15}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

x_range = np.linspace(-5, 3, 400)
y_range = function(x_range)
path_x = np.array(history)
path_y = function(path_x)

axes[0].plot(x_range, y_range, "b-", linewidth=2, label="y=(x+3)²")
axes[0].plot(
    path_x,
    path_y,
    "ro-",
    markersize=4,
    linewidth=1,
    alpha=0.6,
    label="Gradient Descent Path",
)
axes[0].plot(
    path_x[0], path_y[0], "go", markersize=10, label=f"Start (x={path_x[0]:.1f})"
)
axes[0].plot(
    path_x[-1], path_y[-1], "r*", markersize=15, label=f"End (x={path_x[-1]:.3f})"
)
axes[0].set_xlabel("x", fontsize=12)
axes[0].set_ylabel("y", fontsize=12)
axes[0].set_title("Gradient Descent Path on y=(x+3)²", fontsize=14)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].plot(range(len(history)), history, "b-", linewidth=2)
axes[1].axhline(
    y=-3, color="r", linestyle="--", linewidth=2, label="Analytical solution (x=-3)"
)
axes[1].set_xlabel("Iteration", fontsize=12)
axes[1].set_ylabel("x value", fontsize=12)
axes[1].set_title("Convergence of x to Minimum", fontsize=14)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

axes[2].plot(range(len(history)), path_y, "g-", linewidth=2)
axes[2].set_xlabel("Iteration", fontsize=12)
axes[2].set_ylabel("Function Value y=(x+3)²", fontsize=12)
axes[2].set_title("Function Value Convergence", fontsize=14)
axes[2].set_yscale("log")
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("gradient_descent_complete.png", dpi=150, bbox_inches="tight")
print("\n" + "=" * 80)
print("Visualization saved as 'gradient_descent_complete.png'")
print("=" * 80)
plt.show()
