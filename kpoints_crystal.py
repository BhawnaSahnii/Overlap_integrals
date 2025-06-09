import numpy as np

# Parameters
l_point = np.array([0.5, 0.5, 0.5])  # L-point in fractional coordinates
radius = 0.05                        # 10% of BZ radius (0.5)
num_points = 100                     # Number of k-points to generate
tolerance = 1e-5                     # Tolerance for excluding gamma-L line

kpoints = []
attempts = 0
max_attempts = num_points * 20  # To avoid infinite loop

while len(kpoints) < num_points and attempts < max_attempts:
    attempts += 1
    # Generate a random direction
    vec = np.random.normal(size=3)
    vec /= np.linalg.norm(vec)
    # Random radius within sphere
    r = np.random.uniform(0, radius)
    delta = vec * r

    # Exclude gamma-L line (all components equal within tolerance)
    if np.allclose(delta[0], delta[1], atol=tolerance) and np.allclose(delta[0], delta[2], atol=tolerance):
        continue

    # Compute k-point and wrap into [0,1)
    k = (l_point + delta + 1) % 1
    kpoints.append(k)

if len(kpoints) < num_points:
    print(f"Warning: Only generated {len(kpoints)} points after {max_attempts} attempts.")

# Output in Quantum ESPRESSO format
print("K_POINTS crystal")
print(len(kpoints))
for k in kpoints:
    print(f"{k[0]:.8f} {k[1]:.8f} {k[2]:.8f} 1.0")
