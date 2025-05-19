# 🌀 Classical vs Quantum Random Walks

This project explores the concept of quantum superposition through the lens of random walks.
It compares **classical** and **quantum** random walks in **1D** and **2D**, using simulations
and visualizations to highlight their key differences in behavior, especially the difference in 
how they spread over time (i.e., their speed or dispersion rate).

---

## ✨ Key Features

- ✅ Classical random walk simulation (1D and 2D)
- ✅ Quantum random walk simulation using Qiskit (1D and 2D)
- ✅ Smoothed heatmaps and 3D surface plots
- ✅ Raw bitstring histograms of quantum walk measurements
- ✅ Clear comparison between classical and quantum spreading behaviors
- ✅ Data saved for reproducibility (`/results` directory)

---

## 🧠 Concepts Illustrated

### Classical Random Walk
- Each step depends on a fair coin toss.
- Position distribution follows a **binomial (or Gaussian)** profile.
- Spreads at a rate proportional to √n (n = number of steps).

### Quantum Random Walk
- Exploits **quantum superposition** and **interference**.
- Uses **coin qubits** and **position qubits**.
- Probability distribution shows sharp peaks due to interference.
- Spreads at a rate proportional to n — **quadratically faster** than classical walks.

---

## 📊 Output Samples

### 📌 Classical Walk (1D & 2D)
- Smooth Gaussian-like distribution
- Linear dispersion

### 📌 Quantum Walk (1D & 2D)
- Interference patterns
- Bell-shaped probability with sharper peaks
- Faster spread and localization

<p align="center">
  <img src="results/quantum_2d/quantum_walk_2d_bell_surface.png" width="400" alt="Quantum Walk 2D Surface">
  <img src="results/quantum_2d/quantum_walk_2d_heatmap.png" width="400" alt="Quantum Walk 2D Heatmap">
</p>

---

## 🧪 Installation

1. Clone the repository:

```bash
git clone https://github.com/DeepanshuRanolia/https://github.com/DeepanshuRanolia/Quantum-Superposition-using-Random-Walks.git
cd quantum-random-walks

▶️ How to Run
Run any of the walk simulations directly, for example:
python quantum_walks/quantum_walk_2d.py
Plots and simulation results will be saved in the results/ folder and opened automatically

📚 References
Quantum Walks — Wikipedia

Qiskit Documentation

Nayak & Vishwanath, "Quantum Walks on the Line"


📌 Notes
Quantum walks require a quantum simulator (e.g., Qiskit's AerSimulator).

This project uses only simulation — no real quantum hardware needed.

Adjust steps variable to control the walk length.

🙌 Acknowledgements
Developed by Deepanshu, BS Physics, IIT Jodhpur
Guided by interest in quantum superposition, algorithms, and quantum computing.

