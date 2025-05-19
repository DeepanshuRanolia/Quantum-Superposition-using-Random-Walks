import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from scipy.ndimage import gaussian_filter

def run_quantum_walk(steps, symmetric=True):
    pos_qubits = math.ceil(math.log2(2 * steps + 1))
    total_qubits = 1 + pos_qubits

    creg = ClassicalRegister(pos_qubits)
    qc = QuantumCircuit(total_qubits, pos_qubits)

    coin = 0
    pos_start = 2 ** (pos_qubits - 1)

    # Initial coin state
    if symmetric:
        qc.h(coin)
        qc.s(coin)

    # Initialize position
    for i in range(pos_qubits):
        if (pos_start >> i) & 1:
            qc.x(1 + i)

    def increment(qc, control, targets):
        for i in range(len(targets)):
            qc.mcx([control] + targets[:i], targets[i])

    def decrement(qc, control, targets):
        for i in reversed(range(len(targets))):
            qc.mcx([control] + targets[:i], targets[i])

    # Quantum walk
    for _ in range(steps):
        qc.h(coin)
        qc.x(coin)
        decrement(qc, coin, [1 + i for i in range(pos_qubits)])
        qc.x(coin)
        increment(qc, coin, [1 + i for i in range(pos_qubits)])

    for i in range(pos_qubits):
        qc.measure(1 + i, i)

    backend = AerSimulator()
    shots = 1024
    result = backend.run(qc, shots=shots).result()
    counts = result.get_counts()

    sorted_keys = sorted(counts, key=lambda x: int(x, 2))
    positions = [int(k, 2) - pos_start for k in sorted_keys]
    values = np.array([counts[k] for k in sorted_keys]) / shots

    # Smooth probabilities
    prob_grid = np.zeros(2 * steps + 1)
    for p, v in zip(positions, values):
        prob_grid[p + steps] = v
    smooth_values = gaussian_filter(prob_grid, sigma=0.8)

    x = np.arange(-steps, steps + 1)
    return x, smooth_values

# --- Streamlit App Starts Here ---
st.set_page_config(page_title="Quantum Walk Simulator", layout="wide")

st.title("🌀 Quantum Random Walk Simulator")

# Sidebar controls
steps = st.sidebar.slider("Number of Steps", 1, 20, 5)
symmetric = st.sidebar.radio("Initial Coin State", ["Symmetric", "Asymmetric"]) == "Symmetric"

# Run simulation
x, probs = run_quantum_walk(steps, symmetric)

# Plot
fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(x, probs, color="purple", alpha=0.5, step="mid")
ax.plot(x, probs, color="indigo", linewidth=2)
ax.set_title(f"Quantum Walk Distribution after {steps} Steps", fontsize=16)
ax.set_xlabel("Position", fontsize=12)
ax.set_ylabel("Probability", fontsize=12)
ax.grid(True)

# Display plot
st.pyplot(fig)
