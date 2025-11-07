import os
import argparse
from argparse import ArgumentParser
import sys
def getargs():
    parser=ArgumentParser()
    parser.add_argument('-p','--plant_pdb')
    parser.add_argument('-z','--patho_pdb')
    parser.add_argument('-r','--run_dir')
    parser.add_argument('-a','--ambig_fname')
    parser.add_argument('-c','--config_filename')
    return parser.parse_args()

config_template="""run_dir = "{run_dir}"
mode = "local"
# concatenate models inside each job, concat = 5 each .job will produce 5 models
concat = 5
#  Limit the number of concurrent submissions to the queue
queue_limit = 100

{molblock}

[topoaa]
autohis = false
{topaablocks}

{rigidblocks}

[seletop]
select = 40

[flexref]
tolerance = 10
ambig_fname = "{ambig_fname}"

[clustfcc]

[seletopclusts]
top_models = 4

[emscoring]
"""
def getid(pdbin):
    chs=set()
    with open(pdbin,'r') as input:
        for line in input:
            if line.startswith("ATOM"):
                chain=line[21]
                chs.add(chain)
    return sorted(chs)
def sepseg(pdbin):
    chs=getid(pdbin)
    seppdbs=[]
    pdbbasename=pdbin.rstrip('.pdb')
    for chain in chs:
        seppdb=f"{pdbbasename}_{chain}.pdb"
        os.system(f'pdb_selchain -"{chain}" "{pdbin}" > "{pdbbasename}_{chain}.pdb"')
        seppdbs.append(seppdb)
    return seppdbs
def writeconf():
    args=getargs()
    plant_pdb=args.plant_pdb
    patho_pdb=args.patho_pdb
    ambig_fname=args.ambig_fname
    run_dir=args.run_dir
    config_filename=args.config_filename
    seppdbs=sepseg(plant_pdb)
    plantchains=len(seppdbs)
    molfiles = seppdbs + [patho_pdb]
    molblock = (
        "molecules = [\n"
        + "\n".join(f'    "{m}",' for m in molfiles[:-1])
        + f'\n    "{molfiles[-1]}"\n'
        + "]\n"
    )
    topaablocks=""
    for i in range(1,plantchains+1):
        topaablocks+=f"""[topaa.mol{i}]
nhisd = 0
nhise = 1
hise_1 = 75
"""
    topaablocks+=f"""[topaa.mol{plantchains+1}]
nhise = 1
hisd_1 = 76
nhise = 1
hise_1 = 15
"""
    rigidblocks="[rigidbody]\n"
    for i in range(1,plantchains+1):
        rigidblocks+=f"mol_fix_origin_{i} = true\n"
        rigidblocks+=f"mol_shape_{i} = false\n"
    rigidblocks+=f"mol_fix_origin_{plantchains+1} = false\n"
    rigidblocks+=f"mol_shape_{plantchains+1} = false\n"
    rigidblocks+=f"tolerance= = 10\nambig_fname = {ambig_fname}\nsampling = 80\n"
    os.makedirs(run_dir,exist_ok=True)
    config_file=config_filename
    with open(config_file,'w') as f:
        f.write(config_template.format(run_dir=run_dir,molblock=molblock,topaablocks=topaablocks,rigidblocks=rigidblocks,ambig_fname=ambig_fname))
if __name__=="__main__":
    writeconf()
    
