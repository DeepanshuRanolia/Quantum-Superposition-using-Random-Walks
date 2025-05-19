import numpy as np
import matplotlib.pyplot as plt
import os

def classical_random_walk(num_steps=100, num_trials=1000):
    """
    Perform multiple 1D classical random walks.
    
    Args:
        num_steps (int): Number of steps per walk.
        num_trials (int): Number of random walk trials.
    
    Returns:
        np.ndarray: Final positions after each walk.
    """
    steps = np.random.choice([-1, 1], size=(num_trials, num_steps))
    positions = np.cumsum(steps, axis=1)
    final_positions = positions[:, -1]
    return final_positions

def plot_single_walk(num_steps=100, save_path="results/classical/single_walk.png"):
    """
    Plot and save a single 1D random walk.
    """
    steps = np.random.choice([-1, 1], size=num_steps)
    positions = np.cumsum(steps)
    positions = np.insert(positions, 0, 0)  # Include starting position (0)

    plt.figure(figsize=(10, 5))
    plt.plot(range(num_steps + 1), positions, marker='o', linestyle='-', color='blue')
    plt.title("Single 1D Classical Random Walk")
    plt.xlabel("Step Number")
    plt.ylabel("Position")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_histogram(final_positions, save_path="results/classical/histogram.png"):
    """
    Plot and save histogram of final positions from many walks.
    """
    plt.figure(figsize=(10, 5))
    plt.hist(final_positions, bins=30, color='orange', edgecolor='black')
    plt.title("Histogram of Final Positions after Random Walks")
    plt.xlabel("Final Position")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def save_statistics(mean_pos, std_pos, num_steps, num_trials, save_path="results/classical/stats.txt"):
    """
    Save statistics to a text file.
    """
    with open(save_path, "w") as f:
        f.write("Classical Random Walk Results\n")
        f.write(f"Steps per walk: {num_steps}\n")
        f.write(f"Number of trials: {num_trials}\n")
        f.write(f"Mean final position: {mean_pos:.2f}\n")
        f.write(f"Standard deviation: {std_pos:.2f}\n")

def main():
    # Create the results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)

    # Parameters
    num_steps = 100
    num_trials = 1000

    print(f"Simulating {num_trials} random walks with {num_steps} steps each...")

    # Plot and save a single walk
    plot_single_walk(num_steps, save_path="results/classical/single_walk.png")

    # Run multiple trials
    final_positions = classical_random_walk(num_steps, num_trials)

    # Calculate statistics
    mean_pos = np.mean(final_positions)
    std_pos = np.std(final_positions)

    # Display in console
    print(f"Mean final position: {mean_pos:.2f}")
    print(f"Standard deviation: {std_pos:.2f}")

    # Plot histogram and save
    plot_histogram(final_positions, save_path="results/classical/histogram.png")

    # Save results
    save_statistics(mean_pos, std_pos, num_steps, num_trials, save_path="results/classical/stats.txt")

if __name__ == "__main__":
    main()
