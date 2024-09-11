
from vina import Vina

v = Vina(sf_name='vina')

v.set_receptor('1nax_A_receptor.pdbqt')

v.set_ligand_from_file('T4_A.pdbqt')
    
v.compute_vina_maps(center=[4.1897893228818495, 20.728541313112814, 32.05347040440376], box_size=[20, 20, 20])

energy = v.score()
print('Score before minimization: %.3f (kcal/mol)' % energy[0])

energy_minimized = v.optimize()
print('Score after minimization: %.3f (kcal/mol)' % energy_minimized[0])
v.write_pose('T4_A_minimized.pdbqt', overwrite=True)

v.dock(exhaustiveness=8, n_poses=20)
v.write_poses('T4_A_out.pdbqt', n_poses=20, overwrite=True) 