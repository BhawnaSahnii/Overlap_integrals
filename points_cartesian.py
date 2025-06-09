import numpy as np

# Parameters
a =  6.0                        # lattice constant
reciprocal_unit = 2 * np.pi / a
l_point = np.array([0.5, 0.5, 0.5])  # L-point in Cartesian coordinates
radius = 0.025 * reciprocal_unit      # radius expressed in units of 2pi/a
num_points = 100                  # Number of k-points to generate
tolerance = 1e-5                  # Tolerance for excluding Gamma-L direction

kpoints = []
attempts = 0
max_attempts = num_points * 20  # Avoid infinite loop

while len(kpoints) < num_points and attempts < max_attempts:
    attempts += 1
    # Generate a random direction
    vec = np.random.normal(size=3)
    vec /= np.linalg.norm(vec)
    # Random radius within sphere
    r = np.random.uniform(0, radius)
    delta = vec * r

    # Exclude Gamma-L line (all components equal within tolerance)
    if np.allclose(delta[0], delta[1], atol=tolerance) and np.allclose(delta[0], delta[2], atol=tolerance):
        continue

    # Compute k-point in Cartesian coordinates (do not wrap)
    k = l_point + delta
    kpoints.append(k)

if len(kpoints) < num_points:
    print(f"Warning: Only generated {len(kpoints)} points after {max_attempts} attempts.")

# Save the k-points to a file in Quantum ESPRESSO cartesian k-point format
output_file = "kpoints.dat"
with open(output_file, "w") as f:
    f.write("K_POINTS cartesian\n")
    f.write(f"{len(kpoints)}\n")
    for k in kpoints:
        f.write(f"{k[0]:.8f} {k[1]:.8f} {k[2]:.8f} 1.0\n")

print(f"K-points saved to {output_file}")