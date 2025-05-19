# 🌀 Quantum Walks: Classical vs Quantum Random Walk Simulation

[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/your-username/quantum-walks)](https://github.com/your-username/quantum-walks)
[![Stars](https://img.shields.io/github/stars/your-username/quantum-walks.svg?style=social)](https://github.com/your-username/quantum-walks/stargazers)

A simulation-based project that compares classical and quantum random walks in 1D and 2D. Visualizations like histograms are used to illustrate probability distributions and highlight the fundamental difference in spreading behavior between the two types of walks.


---

## ✨ Key Features

- ✅ Classical random walk simulation (1D and 2D)
- ✅ Quantum random walk simulation using Qiskit (1D and 2D)
- ✅ Smoothed heatmaps and 3D surface plots
- ✅ Raw bitstring histograms of quantum walk measurements
- ✅ Clear comparison between classical and quantum spreading behaviors
- ✅ Data saved for reproducibility (`/results` directory)

---

## 🔬 Background

### 🧍 Classical Random Walk (CRW)

- At each step, the walker moves **left or right** (or up/down in 2D) with **equal probability**.
- Probability distribution forms a **binomial distribution** (approaches Gaussian for large `n`).
- **Spread** is proportional to √n (diffusive).

### 🧑‍🚀 Quantum Random Walk (QRW)

- Uses quantum **superposition** and **interference**.
- Incorporates **Hadamard gates** and **coin states**.
- Results in **non-Gaussian, peaked distributions**.
- **Spread** is proportional to `n` (ballistic).

---

## 📊 Output Samples

### 📌 Classical Walk
- Smooth Gaussian-like distribution
- Linear dispersion

### 📌 Quantum Walk (1D & 2D)
- Interference patterns
- Bell-shaped probability with sharper peaks
- Faster spread and localization

<p align="center">
  <img src="results/quantum_2d/quantum_walk_2d_histogram.png" width="400" alt="Quantum Walk 2D Surface">
  <img src="results/quantum_2d/quantum_walk_2d_heatmap.png" width="400" alt="Quantum Walk 2D Heatmap">
</p>

---

## 🧪 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/quantum-random-walks.git
   cd quantum-random-walks

🧪 Experiments to Try
Vary n (number of steps): Observe how the spread scales.

Compare final histograms between classical and quantum walks.

Extend to biased walks or multi-particle walks.

📚 References
Quantum Walks – Wikipedia

Nielsen & Chuang, Quantum Computation and Quantum Information

IBM Qiskit Documentation (for quantum simulation)


📌 Notes
Quantum walks require a quantum simulator (e.g., Qiskit's AerSimulator).

This project uses only simulation — no real quantum hardware needed.

Adjust steps variable to control the walk length.

🙌 Acknowledgements
Developed by Deepanshu, BS Physics, IIT Jodhpur
Guided by interest in quantum superposition, algorithms, and quantum computing.

