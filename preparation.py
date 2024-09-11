from vina import Vina
from pymol import cmd
import argparse
import subprocess

# argument parsing
parser = argparse.ArgumentParser()
parser.add_argument('input_name', help='input file path or name of receptor') # receptor name, PDB file
parser.add_argument('ligand_name', help='input file path or name of ligand') # ligand name, SDF file
args = parser.parse_args()

# path setting
ADT_path = '/home/jspark/ADFRsuite-1.0/bin/prepare_receptor'
meeko_path = '/home/jspark/anaconda3/envs/vina/bin/mk_prepare_ligand.py'

# split chains of input protein
cmd.load(args.input_name)
chain_list = cmd.get_chains()
print(f'\nThis protein has {len(chain_list)} chains\n')
for chain in chain_list:
    # remove ligand from protein-ligand complex of each chain
    print(f'chain {chain} processing...')
    cmd.load(args.input_name)
    chain_file_name = args.input_name.replace('.', f'_{chain}.') # chain name : receptor name + A or B or C or ...
    cmd.remove(f'not chain {chain}') # remove ligand from chain
    cmd.save(chain_file_name) # save each chain
    chain_receptor_name = chain_file_name.replace('.', '_receptor.')
    
    # extract center of mass coordinate of binding site of chain
    cmd.select('lig', 'organic')
    c_o_m = cmd.centerofmass('lig') # center of mass
    cmd.remove('lig')
    cmd.save(chain_receptor_name)
    cmd.delete('all')

    # move ligand to center of mass
    print(f"Let's move {args.ligand_name} to chain {chain}!")
    moved_ligand_name = args.ligand_name.replace('.', f'_{chain}.')
    with open(args.ligand_name, 'r') as file:
        lines = file.readlines()
        
    # move ligand to center of mass
    translation_vector = c_o_m 
    
    # extract 3d coordinate from ligand SDF file and move ligand
    output_lines = lines[0:4]
    lines = lines[4:]
    i=0
    while True: 
        parts = lines[i].split()
        if len(parts) <=4:
            break
        if not parts[3].isalpha():
            break
        # moves 
        x = float(parts[0]) + c_o_m[0]
        y = float(parts[1]) + c_o_m[1]
        z = float(parts[2]) + c_o_m[2]
        new_line = f"{x:>10.4f}{y:>10.4f}{z:>10.4f} {'  '.join(parts[3:])}\n"
        output_lines.append(new_line)
        i += 1
    output_lines += lines[i:]
    with open(moved_ligand_name, 'w') as f:
        f.writelines(output_lines)

    # pdb to pdbqt
    # prepare_receptor : using AutoDockTools
    # mk_prepare_ligand : using meeko (from AutoDockVina Manual, https://autodock-vina.readthedocs.io/_/downloads/en/latest/pdf/)
    print('transform pdb file to pdbqt file...')
    subprocess.run(f'{ADT_path} -r {chain_receptor_name} -A hydrogens', shell=True, executable='/bin/bash')
    subprocess.run(f'{meeko_path} -i {moved_ligand_name}', shell=True, executable='/bin/bash')

    # Generate run vina script
    vina_receptor_name = chain_receptor_name.replace('.pdb', '.pdbqt')
    vina_ligand_name = moved_ligand_name.replace('.sdf', '.pdbqt')
    vina_ligand_minimized = vina_ligand_name.replace('.', '_minimized.')
    vina_output = vina_ligand_name.replace('.', '_out.')
    script_content = f"""
from vina import Vina

v = Vina(sf_name='vina')

v.set_receptor('{vina_receptor_name}')

v.set_ligand_from_file('{vina_ligand_name}')
    
v.compute_vina_maps(center={c_o_m}, box_size=[20, 20, 20])

energy = v.score()
print('Score before minimization: %.3f (kcal/mol)' % energy[0])

energy_minimized = v.optimize()
print('Score after minimization: %.3f (kcal/mol)' % energy_minimized[0])
v.write_pose('{vina_ligand_minimized}', overwrite=True)

v.dock(exhaustiveness=8, n_poses=20)
v.write_poses('{vina_output}', n_poses=20, overwrite=True) """

    with open(f"run_vina_{chain}.py", "w") as f:
        f.write(script_content)
    print(f"Python script run_vina_{chain}.py has been generated.")
    print('Done!!!\n')
