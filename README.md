# Useful script for AutoDockVina
This script serves the purpose of generating all the necessary input files required for running AutoDock Vina. It automates the preparation of various essential components, including ligand and receptor files, ensuring that the input data is properly formatted and compatible with the docking process. By using this script, users can streamline the setup phase of molecular docking, saving time and reducing the potential for errors in file preparation. This makes it a useful tool for anyone looking to perform docking simulations with AutoDock Vina efficiently.

## Pre-Requisites
- `AutoDock Vina` (Python Bindings) : https://autodock-vina.readthedocs.io/en/latest/installation.html or https://pypi.org/project/vina/
- `AutoDockTools` (MGL Tools) : https://ccsb.scripps.edu/mgltools/downloads/
- `Meeko` : https://pypi.org/project/meeko/0.3.3/

## Information
This script is based on the **`AutoDock Vina Manual`** (https://autodock-vina.readthedocs.io/_/downloads/en/latest/pdf/) and follows the process outlined below:

1. Separation of receptor proteins by chain (in case of multiple chains)
2. Removal of ligands from protein-ligand complexes for each chain
3. Saving each chain separately
4. Extraction of receptor binding site center coordinates
5. Translating the ligand by the extracted coordinates
6. Protein preparation and generation of pdbqt files using AutoDockTools
7. Ligand preparation and generation of pdbqt files using Meeko
8. Generation of the necessary AutoDock Vina running script for docking

## How to Use?
Replace `1nax.pdb` and `T4.sdf` with your own receptor and ligand files.
```bash
python preparation.py [1nax.pdb] [T4.sdf]
```
Running the above command will generate a `run_vina_A.py` file (and additional files for chains B, C, etc., if applicable).<br/>
To execute the generated file, run the following command using the Python environment where AutoDock Vina is installed:
```bash
python run_vina_A.py
```
You can also run run_vina_B.py, run_vina_C.py, etc., if multiple chains are present.

## Please Note...
![process](https://github.com/user-attachments/assets/2e66ee62-f949-40cc-a785-191906427fa0)


