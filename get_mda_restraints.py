import sys
import MDAnalysis as mda
from pathlib import Path
import json
from MDAnalysis.analysis import contacts
def get_mda_map(ppath):
    docked=mda.Universe(ppath)
    prot=docked.select_atoms('protein')
    lig=docked.select_atoms('resname LIG')
    dist=contacts.distance_array(prot,lig)
    contacting=dist<5.0
    conresids=set()
    for i, incontact in enumerate(contacting.any(axis=1)):
        if incontact:
            conresids.add(int(prot[i].resid))
    return sorted(conresids)
def write_list(ipath):
    activeprots=get_mda_map(ipath)
    ligsites=[int(resid) for resid in set(mda.Universe(ipath).select_atoms('resname LIG').resids)]
    protslist=ipath.replace('.pdb','_prots.txt')
    ligslist=ipath.replace('.pdb','_ligs.txt')
    with open(protslist,'w') as out1:
        out1.write(' '.join(map(str,activeprots))+'\n')
        out1.write('\n')#note that haddock3 needs 2 lines 
    with open(ligslist,'w') as out2:
        out2.write(' '.join(map(str,ligsites))+'\n')
        out2.write('\n')
    return protslist,ligslist
    ''' json file no longer used for haddock3
def write_config(ipath,opath):
    activeprots=get_mda_map(ipath)
    ligsites=[int(resid) for resid in set(mda.Universe(ipath).select_atoms('resname LIG').resids)]
    conf=[
            {
                    "id": 1,
                    "chain": "G",
                    "active": activeprots,
                    "passive": [],
                    "target": [2]
            },
            {
                    "id": 2,
                    "chain": "B",
                    "active": ligsites,
                    "passive": [],
                    "target": [1]
            }
            ]
    with open(opath,'w') as output:
        json.dump(conf,output,indent=1)
'''
if __name__=='__main__':
    ipath=sys.argv[1]
    write_list(ipath)
