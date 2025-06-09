from irrep.bandstructure import BandStructure
import numpy as np
import matplotlib.pyplot as plt
import os

# Set the working directory to the location of nbfesb.save and your script
os.chdir(r"c:\Users\u2273377\OneDrive - University of Warwick\NbFeSb\tmp\tmp_cart")

# Load wavefunctions from DFT output
bs = BandStructure(prefix='nbfesb', code='espresso')
band1 = 20  # band 21 (zero-based)
band2 = 21  # band 22 (zero-based)

# Lists to store interband overlaps for both directions and the distances
interband_overlap_21_22 = []  # overlap from band 21 -> band 22 (S[0,1])
interband_overlap_22_21 = []  # overlap from band 22 -> band 21 (S[1,0])
distances = []

for i in range(bs.num_k):
    for j in range(bs.num_k):
        if i < j:
            # Compute k-space distance between the two k-points
            delta = (bs.kpoints[i].k - bs.kpoints[j].k + 0.5) % 1 - 0.5
            distances.append(np.linalg.norm(delta))
            # Extract the 2x2 overlap matrix for the two bands of interest
            S = bs.kpoints[i].overlap(bs.kpoints[j])[band1:band2+1, band1:band2+1]
            # For interband overlaps, save both off-diagonal elements
            interband_overlap_21_22.append(np.abs(S[0, 1]))
            interband_overlap_22_21.append(np.abs(S[1, 0]))

# Compute average interband overlaps for both directions
avg_21_22 = np.mean(interband_overlap_21_22)
avg_22_21 = np.mean(interband_overlap_22_21)
print("Average interband overlap from band 21 -> 22:", avg_21_22)
print("Average interband overlap from band 22 -> 21:", avg_22_21)

# Plot the interband overlaps against k-space distances
plt.figure(figsize=(8, 6))
plt.scatter(distances, interband_overlap_21_22, s=10, alpha=0.5, label='Band B1 -> B2')
plt.scatter(distances, interband_overlap_22_21, s=10, alpha=0.5, label='Band B2 -> B1')
plt.axhline(y=avg_21_22, color='r', linestyle='--', label='Avg B1 -> B2')
plt.axhline(y=avg_22_21, color='b', linestyle='--', label='Avg B2 -> B1')
# Set font family globally
plt.rcParams['font.family'] = 'Helvetica'

# Define a consistent font size
label_fontsize = 24

# Apply font size
plt.xticks(fontsize=label_fontsize)
plt.yticks(fontsize=label_fontsize)
plt.xlabel('k-space distance between pairs', fontsize=label_fontsize)
plt.ylabel('Interband Overlap |S[ij]|', fontsize=label_fontsize)
plt.grid(alpha=0.3)
plt.legend(loc='lower right', fontsize=18)
plt.tight_layout()
plt.savefig('Inter_overlap_21_22_both.png', dpi=300)
plt.show()