from typing import TypedDict, List
import re 
import os 
import sys
import csv
class ProdData(TypedDict):
    pdbid: str
    N_contact: int 
    N_CC_contact: int 
    N_CP_contact: int 
    N_CA_contact: int 
    N_PP_contact: int 
    N_AP_contact: int 
    N_AA_contact: int 
    P_ANIS: float
    P_CNIS: float
    BA: float
    M: float

def collect_prod(indir: str) -> ProdData:
    data = {
        'pdbid': '',
        'N_contact': 0,
        'N_CC_contact': 0,
        'N_CP_contact': 0,
        'N_CA_contact': 0,
        'N_PP_contact': 0,
        'N_AP_contact': 0,
        'N_AA_contact': 0,
        'P_ANIS': 0.0,
        'P_CNIS': 0.0,
        'BA': 0.0,
        'M': 0.0
    }

    pdbid = os.path.basename(indir.rstrip('/'))
    prodfile = os.path.join(indir, 'ranked_0.prodigy')

    with open(prodfile, 'r') as prodin:
        plines = prodin.readlines()
        for pline in plines:
            pline = pline.strip().replace('No. of ', '')
            if pline.startswith('[+]') or pline.startswith('[++]'):
                pline = pline.lstrip('[+]').strip()

            if 'intermolecular contacts:' in pline:
                data['N_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'charged-charged contacts:' in pline:
                data['N_CC_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'charged-polar contacts:' in pline:
                data['N_CP_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'charged-apolar contacts:' in pline:
                data['N_CA_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'polar-polar contacts:' in pline:
                data['N_PP_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'apolar-polar contacts:' in pline:
                data['N_AP_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'apolar-apolar contacts:' in pline:
                data['N_AA_contact'] = int(float(pline.split(':')[-1].strip()))
            elif 'apolar nis residues:' in pline.lower():
                val = pline.split(':')[-1].strip().rstrip('%')
                data['P_ANIS'] = float(val)
            elif 'charged nis residues:' in pline.lower():
                val = pline.split(':')[-1].strip().rstrip('%')
                data['P_CNIS'] = float(val)
            elif 'binding affinity' in pline.lower():
                val = pline.split(':')[-1].strip()
                val = re.split(r'\s+', val)[0]
                try:
                    data['BA'] = float(val)
                except ValueError:
                    pass
            elif 'dissociation constant' in pline.lower():
                val = pline.split(':')[-1].strip()
                val = re.split(r'\s+', val)[0]
                try:
                    data['M'] = float(val)
                except ValueError:
                    pass

    data['pdbid'] = pdbid
    return data
def write_to_csv(row:ProdData,path:str)-> None:
    header=list(row.keys())
    with open(path,'a',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=header)
        writer.writerow(row)
if __name__ == '__main__':
    indir = sys.argv[1]
    outpath=sys.argv[2]
    row=collect_prod(indir)
    write_to_csv(row,outpath)
