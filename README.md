# Overlap_integrals
A code to compute interband and intraband overlap values was made for an example case of NbFeSb.
Steps involved: 
1) Use kpoints.py to generate the k-points (in crystal or cartesian coordinates) in the neighbourhood of the band edge (L-point in this case) to use in DFT nscf calculation.
2) Run the interband/intraband_overlap.py code in the tmp directory to get the interband or intraband overlap values. Specify the band numbers there (band 21 and 22 from QE output here in NbFeSb). 
