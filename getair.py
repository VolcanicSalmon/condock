from typing import Dict, List
from pathlib import Path
import os
import argparse
from argparse import ArgumentParser
def getargs():
    parser=ArgumentParser()
    parser.add_argument('-p','--pdbin')
    parser.add_argument('-i','--pprotid')
    parser.add_argument('-a','--air2dir')
    parser.add_argument('-j','--js2dir')
    args=parser.parse_args()
    return args
def getchainid(pdbin)->List[str]:
    chs=set()
    with open(pdbin,'r') as input:
        for line in input:
            if line.startswith("ATOM"):
                chs.add(line[21])
    return sorted(chs)
def mapair(pdbin,pprotid,air2dir,js2dir):
    chains=getchainid(pdbin)
    air2files=sorted(Path(air2dir).glob(f"*{pprotid}*.air2.txt"))
    mapdict:Dict[str,str]={chain:str(air2file) for chain, air2file in zip(chains,air2files)}
    for chain, air2file in mapdict.items():
        js2files=Path(js2dir).glob("*.js2")
        for js2file in js2files:
            outfile=js2file.with_name(js2file.name.replace("js2",f"_{pprotid}_{chain}.tbl"))
            os.system(f'~/.local/bin/haddock3-restraints active_passive_to_ambig "{air2file}" "{js2file}" --segid-one "{chain}" --segid-two Z > "{outfile}"')
if __name__=='__main__':
    args=getargs()
    mapair(args.pdbin,args.pprotid,args.air2dir,args.js2dir)
