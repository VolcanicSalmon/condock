import os
import sys

# for i in NP_1*/*.pdb; do python3 hadconf.py $i ligand_h.acpype/ligand_new2.pdb $(dirname $i)/*tbl $(dirname $i)_run $(dirname $i).cfg; done
config_template = """run_dir = "{run_dir}"
mode = "local"
ncores = 24
debug = true
concat = 5
queue_limit = 100

molecules = [
    "{protein_pdb}",
    "{ligand_pdb}"
]

[topoaa]
tolerance = 10
ligand_param_fname="ligand_h.acpype/ligand_h_CNS.par"
ligand_top_fname="ligand_h.acpype/ligand_h_CNS.top"
autohis = true
delenph = false

[rigidbody]
tolerance = 10
ambig_fname = "{ambig_fname}"
ligand_param_fname="ligand_h.acpype/ligand_h_CNS.par"
ligand_top_fname="ligand_h.acpype/ligand_h_CNS.top"
sampling = 80
w_vdw = 1.0

[seletop]
select = 50

[flexref]
tolerance = 20
ligand_param_fname="ligand_h.acpype/ligand_h_CNS.par"
ligand_top_fname="ligand_h.acpype/ligand_h_CNS.top"
mdsteps_rigid = 200
mdsteps_cool1 = 200

[ilrmsdmatrix]
receptor_chain = "A"
ligand_chains  = ["Z"]
contact_distance_cutoff = 10

[clustrmsd]
criterion = 'distance'
n_clusters = 4

[seletopclusts]
top_models = 4

[caprieval]
allatoms = true
"""

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 handconf.py <protein_pdb> <ligand_pdb> <ambig_fname> <run_dir> <config_filename>")
        sys.exit(1)

    protein_pdb = sys.argv[1]
    ligand_pdb = sys.argv[2]
    ambig_fname = sys.argv[3]
    run_dir = sys.argv[4]
    config_filename = sys.argv[5]

    os.makedirs(run_dir, exist_ok=True)  # Create the run directory

    config_file =  config_filename
    with open(config_file, "w") as f:
        f.write(config_template.format(
            run_dir=run_dir,
            protein_pdb=protein_pdb,
            ligand_pdb=ligand_pdb,
            ambig_fname=ambig_fname
        ))

    print(f"Generated configuration file: {config_file}")

if __name__ == "__main__":
    main()

