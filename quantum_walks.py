from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math
import numpy as np
import os

def quantum_walk_fixed(steps):
    pos_qubits = math.ceil(math.log2(2 * steps + 1))  # enough to represent positions
    total_qubits = 1 + pos_qubits  # 1 coin + position qubits

    creg = ClassicalRegister(pos_qubits)
    qc = QuantumCircuit(total_qubits, pos_qubits)

    coin = 0
    pos_start = 2 ** (pos_qubits - 1)

    # Initialize coin in superposition: |+i⟩ = H·S|0⟩ for symmetry
    qc.h(coin)
    qc.s(coin)

    # Initialize walker at center
    for i in range(pos_qubits):
        if (pos_start >> i) & 1:
            qc.x(1 + i)

    # Define coin-controlled shift operations
    def increment(qc, control, targets):
        for i in range(len(targets)):
            qc.mcx([control] + targets[:i], targets[i])

    def decrement(qc, control, targets):
        for i in reversed(range(len(targets))):
            qc.mcx([control] + targets[:i], targets[i])

    # Quantum walk steps
    for _ in range(steps):
        qc.h(coin)  # coin toss

        # Controlled decrement if coin == 0
        qc.x(coin)
        decrement(qc, coin, [1 + i for i in range(pos_qubits)])
        qc.x(coin)

        # Controlled increment if coin == 1
        increment(qc, coin, [1 + i for i in range(pos_qubits)])

    # Measure position qubits
    for i in range(pos_qubits):
        qc.measure(1 + i, i)

    # Run simulation
    backend = AerSimulator()
    shots = 1024
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    # Process results for bar plot
    sorted_keys = sorted(counts, key=lambda x: int(x, 2))
    positions = [int(k, 2) - pos_start for k in sorted_keys]
    values = [counts[k] for k in sorted_keys]

    # Make sure output directory exists
    os.makedirs("results/quantum_1d", exist_ok=True)

    # Bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(positions, values, color='darkred', width=0.8)
    for bar, count in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 str(count), ha='center', fontsize=8)

    plt.title(f"Quantum Random Walk After {steps} Steps (Bar Plot)")
    plt.xlabel("Position")
    plt.ylabel("Counts")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.xticks(positions)
    plt.tight_layout()
    plt.savefig("results/quantum_1d/bar_plot.png")
    plt.close()

    from qiskit.visualization import plot_histogram

    fig = plot_histogram(counts, title="Quantum Walk Histogram")
    fig.savefig("results/quantum_1d/histogram.png")
    print("Histogram saved as 'results/quantum_1d/histogram.png'")

    # Save stats
    total_shots = sum(values)
    prob_dist = np.array(values) / total_shots
    mean = np.dot(positions, prob_dist)
    stddev = np.sqrt(np.dot((np.array(positions) - mean) ** 2, prob_dist))
    max_count = max(values)
    most_probable = [p for p, v in zip(positions, values) if v == max_count]

    stats_path = "results/quantum_1d/stats.txt"
    with open(stats_path, "w") as f:
        f.write(f"Quantum Walk Stats (Steps: {steps})\n")
        f.write(f"----------------------------------\n")
        f.write(f"Shots: {total_shots}\n")
        f.write(f"Mean position: {mean:.2f}\n")
        f.write(f"Standard deviation: {stddev:.2f}\n")
        f.write(f"Most probable position(s): {most_probable}\n")
        f.write(f"Min position: {min(positions)}\n")
        f.write(f"Max position: {max(positions)}\n")

    print("Stats saved as 'results/quantum_1d/stats.txt'")

    return counts

# Example run
quantum_walk_fixed(10)
