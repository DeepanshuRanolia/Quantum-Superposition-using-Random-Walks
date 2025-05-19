from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from sys import platform
from scipy.ndimage import gaussian_filter

def quantum_walk_2d(steps):
    # --- Qubit configuration ---
    pos_qubits_per_dim = math.ceil(math.log2(2 * steps + 1))
    total_pos_qubits = 2 * pos_qubits_per_dim  # x and y directions
    total_qubits = 2 + total_pos_qubits        # 2 coin qubits + position qubits

    creg = ClassicalRegister(total_pos_qubits)
    qc = QuantumCircuit(total_qubits, total_pos_qubits)

    coin_x = 0
    coin_y = 1
    pos_x = [2 + i for i in range(pos_qubits_per_dim)]
    pos_y = [2 + pos_qubits_per_dim + i for i in range(pos_qubits_per_dim)]

    pos_start = 2 ** (pos_qubits_per_dim - 1)

    # --- Initialization ---
    for coin in [coin_x, coin_y]:
        qc.h(coin)
        qc.s(coin)

    for i in range(pos_qubits_per_dim):
        if (pos_start >> i) & 1:
            qc.x(pos_x[i])
            qc.x(pos_y[i])

    # --- Shift operations ---
    def increment(qc, control, targets):
        for i in range(len(targets)):
            qc.mcx([control] + targets[:i], targets[i])

    def decrement(qc, control, targets):
        for i in reversed(range(len(targets))):
            qc.mcx([control] + targets[:i], targets[i])

    # --- Quantum walk steps ---
    for _ in range(steps):
        qc.h(coin_x)
        qc.h(coin_y)

        # X direction shift
        qc.x(coin_x)
        decrement(qc, coin_x, pos_x)
        qc.x(coin_x)
        increment(qc, coin_x, pos_x)

        # Y direction shift
        qc.x(coin_y)
        decrement(qc, coin_y, pos_y)
        qc.x(coin_y)
        increment(qc, coin_y, pos_y)

    # --- Measurement ---
    for i in range(pos_qubits_per_dim):
        qc.measure(pos_x[i], i)
        qc.measure(pos_y[i], pos_qubits_per_dim + i)

    # --- Simulation ---
    backend = AerSimulator()
    shots = 2048
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    # --- Process counts into 2D probability grid ---
    grid_size = 2 * steps + 1
    center = 2 ** (pos_qubits_per_dim - 1)
    prob_grid = np.zeros((grid_size, grid_size))

    for key, count in counts.items():
        y_bin = key[:pos_qubits_per_dim]
        x_bin = key[pos_qubits_per_dim:]
        x = int(x_bin, 2) - center
        y = int(y_bin, 2) - center
        x_idx = x + steps
        y_idx = y + steps
        if 0 <= x_idx < grid_size and 0 <= y_idx < grid_size:
            prob_grid[y_idx, x_idx] += count

    # Normalize and smooth
    prob_grid /= shots
    smooth_prob_grid = gaussian_filter(prob_grid, sigma=1.0)

    # --- Ensure output directory exists ---
    output_dir = "results/quantum_2d"
    os.makedirs(output_dir, exist_ok=True)

    # --- 2D Heatmap ---
    extent = [-steps - 0.5, steps + 0.5, -steps - 0.5, steps + 0.5]
    plt.figure(figsize=(8, 6))
    plt.imshow(
        smooth_prob_grid,
        extent=extent,
        origin='lower',
        cmap='plasma',
        interpolation='bilinear',
        aspect='equal'
    )
    plt.colorbar(label="Probability")
    plt.title("2D Quantum Walk — Smoothed Probability Heatmap")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.grid(False)
    plt.tight_layout()

    heatmap_filename = os.path.join(output_dir, "quantum_walk_2d_heatmap.png")
    plt.savefig(heatmap_filename, dpi=300)
    print(f"2D heatmap saved as '{heatmap_filename}'")

    # --- 3D Surface Plot ---
    X = np.linspace(-steps, steps, grid_size)
    Y = np.linspace(-steps, steps, grid_size)
    X, Y = np.meshgrid(X, Y)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surface = ax.plot_surface(
        X, Y, smooth_prob_grid,
        cmap='plasma',
        edgecolor='none',
        rstride=1,
        cstride=1,
        antialiased=True,
        alpha=0.95
    )

    ax.set_title("2D Quantum Walk — Smoothed Bell Distribution", fontsize=14, pad=15)
    ax.set_xlabel("X Position", labelpad=10)
    ax.set_ylabel("Y Position", labelpad=10)
    ax.set_zlabel("Probability", labelpad=10)
    ax.view_init(elev=45, azim=135)
    fig.colorbar(surface, shrink=0.6, aspect=10, label="Probability")
    plt.tight_layout()

    surface_filename = os.path.join(output_dir, "quantum_walk_2d_bell_surface.png")
    plt.savefig(surface_filename, dpi=300)
    print(f"Bell surface plot saved as '{surface_filename}'")

    # --- Raw Histogram ---
    hist_fig = plot_histogram(counts, title="2D Quantum Walk (Raw Bitstring Histogram)")
    hist_filename = os.path.join(output_dir, "quantum_walk_2d_histogram.png")
    hist_fig.savefig(hist_filename)
    print(f"Histogram saved as '{hist_filename}'")

    # --- Optional: Open files ---
    for fname in [heatmap_filename, surface_filename, hist_filename]:
        if platform.startswith("linux"):
            os.system(f"xdg-open {fname}")
        elif platform == "darwin":
            os.system(f"open {fname}")
        elif platform == "win32":
            os.startfile(fname)

    return counts

# Run the walk
quantum_walk_2d(steps=5)
