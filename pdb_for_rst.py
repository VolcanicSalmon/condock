import sys
import numpy as np
import string
alphabets=string.ascii_uppercase
class PDB:
    def __init__(self,outlines,chains):
        self.outlines=outlines
        self.chains=chains
def clean_chain_pdb(pin):
    outlines=[]
    chains=set()
    with open(pin,'r') as input:
        for line in input:
            if line.startswith("ATOM"):
                outlines.append(line)
                chains.add(line.split()[4])
    return PDB(outlines,chains)
def combine_pdbs(pin1,pin2,pout):
    pin1data=clean_chain_pdb(pin1)
    pin2data=clean_chain_pdb(pin2)
    pin1chains=pin1data.chains
    pin2chains=pin2data.chains
    overlaps=set.intersection(pin1chains,pin2chains)
    if len(overlaps)>=1:
        newletter=set(alphabets)-pin1chains 
        mappings={}
        for oldpin2chains in overlaps:
            newchain=newletter.pop()
            mappings[oldpin2chains]=newchain 
            newoutlines=[]
            newchains=set()
            for line in pin2data.outlines:
                oldchain=line[21]
                if oldchain in mappings:
                    newline=f"{line[:21]}{mappings[oldchain]}{line[22:]}"
                    newoutlines.append(newline)
                    newchains.add(mappings[oldchain])
                else:
                    newoutlines.append(line)
                    newchains.add(oldchain)
        pin2data.outlines=newoutlines
        pin2data.chains=newchains 
    comblines= pin1data.outlines+["TER\n"]+pin2data.outlines+["TER\n","END\n"]
    with open(pout,'w') as outfile:
        outfile.writelines(comblines)
if __name__=='__main__':
    pin1=sys.argv[1]
    pin2=sys.argv[2]
    pout=sys.argv[3]
    combine_pdbs(pin1,pin2,pout)

