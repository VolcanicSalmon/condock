import prody
import glob
import os
from prody import parseMMCIF 
from prody import writePDB
import mdtraj
import MDAnalysis as mda 
from MDAnalysis.analysis import rms 
from MDAnalysis.analysis import contacts
from MDAnalysis.analysis.distances import distance_array
import numpy as np 
from prody import parseMMCIF
from prody import writePDB
def convert_cif_to_pdb(cifin):
    cif=parseMMCIF(cifin)
    pdbout=cifin.replace('cif','pdb')
    writePDB(pdbout,cif)
    return pdbout
def mdacontact(pdbin):
    u=mda.Universe(pdbin)
    prot=u.select_atoms('protein')
    lig=u.select_atoms('resname LIG')
    distance_mat=distance_array(prot.positions, lig.positions)
    ncons=np.sum(distance_mat<5)
    meandist=np.mean(distance_mat)
    return ncons,meandist
def mdtraj_sasa(pdb):
    t=mdtraj.load(pdb)
    sasall=mdtraj.shrake_rupley(t).sum(axis=1)
    sasaprot=mdtraj.shrake_rupley(t.atom_slice(t.topology.select('protein'))).sum(axis=1)
    sasalig=mdtraj.shrake_rupley(t.atom_slice(t.topology.select(f"resname LIG"))).sum(axis=1)
    burysasa=[(p+l)-c for p,l,c in zip(sasaprot,sasalig,sasall)]
    return burysasa[0]
def loop(indir,outfile):
    cifiles=glob.glob('*.af/*lig/*model.cif')
    with open(outfile,'w') as output:
        output.writelines("protid,ncons,meandist,burysasa\n")
        for cifile in cifiles:
            protid=cifile.split('/')[0]
            pdbfile=convert_cif_to_pdb(cifile)
            ncons,meandist=mdacontact(pdbfile)
            burysasa=mdtraj_sasa(pdbfile)
            row=f"{protid},{ncons},{meandist},{burysasa}\n"
            output.writelines(row)
if __name__=="__main__":
    loop(".","res.csv")
