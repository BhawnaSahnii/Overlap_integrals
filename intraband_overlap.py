from irrep.bandstructure import BandStructure
import numpy as np
import matplotlib.pyplot as plt
import os

# Set the working directory to the location of nbfesb.save and your script
os.chdir(r"c:\Users\u2273377\OneDrive - University of Warwick\NbFeSb\tmp\tmp")

# Load wavefunctions from DFT output
bs = BandStructure(prefix='nbfesb', code='espresso')
band1 = 20  # band 21 (zero-based)
band2 = 21  # band 22 (zero-based)

# Compute intraband overlaps between all pairs for band1 and band2
intra_overlap_band1 = []
intra_overlap_band2 = []
distances = []  # distances for the pairs

for i in range(bs.num_k):
    for j in range(bs.num_k):
        if i < j:
            # Compute distance between k-points
            delta = (bs.kpoints[i].k - bs.kpoints[j].k + 0.5) % 1 - 0.5
            distances.append(np.linalg.norm(delta))
            # Compute the overlap matrix for the two bands
            S = bs.kpoints[i].overlap(bs.kpoints[j])[band1:band2+1, band1:band2+1]
            # For intraband overlaps, use diagonal elements S[0,0] and S[1,1]
            intra_overlap_band1.append(np.abs(S[0, 0]))
            intra_overlap_band2.append(np.abs(S[1, 1]))

# Compute the average intraband overlaps
avg_intra_band1 = np.mean(intra_overlap_band1)
avg_intra_band2 = np.mean(intra_overlap_band2)

print("Average intraband overlap for band 21:", avg_intra_band1)
print("Average intraband overlap for band 22:", avg_intra_band2)

# Plot the intraband overlaps against distances
plt.figure(figsize=(8, 6))
plt.scatter(distances, intra_overlap_band1, s=10, alpha=0.5, label='Band B1 Overlap')
plt.scatter(distances, intra_overlap_band2, s=10, alpha=0.5, label='Band B2 Overlap')
plt.axhline(y=avg_intra_band1, color='b', linestyle='--', label='Avg Band B1 Overlap')
plt.axhline(y=avg_intra_band2, color='g', linestyle='--', label='Avg Band B2 Overlap')

# Set font family globally
plt.rcParams['font.family'] = 'Helvetica'

# Define a consistent font size
label_fontsize = 24

# Apply font size
plt.xticks(fontsize=label_fontsize)
plt.yticks(fontsize=label_fontsize)
plt.xlabel('k-space distance between pairs', fontsize=label_fontsize)
plt.ylabel('Intraband Overlap |S[ii]|', fontsize=label_fontsize)
plt.legend(fontsize=18)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

plt.savefig('Intra_overlap_21_22.png', dpi=300)
plt.show()