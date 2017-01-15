import click
import os
import numpy as np
from rdkit.Chem import RDConfig
from rdkit import Chem
from rdkit.Chem import FragmentCatalog
from rdkit.Chem import DataStructs

fName = os.path.join( RDConfig.RDDataDir, 'FunctionalGroups.txt' )
fparams = FragmentCatalog.FragCatParams( 1, 6, fName )
fcat = FragmentCatalog.FragCatalog( fparams )
fcgen = FragmentCatalog.FragCatGenerator()
fpgen = FragmentCatalog.FragFPGenerator()

@click.command()
@click.option( '--infile','-i' )
def getfragmentfp( infile ):
    fragfps = []
    sdf = Chem.SDMolSupplier( infile )
    for mol in sdf:
        if mol == None:
            continue
        nAdded = fcgen.AddFragsFromMol( mol, fcat )
    for mol in sdf:
        if mol == None:
            continue
        arr = np.zeros((1,))
        fp = fpgen.GetFPForMol( mol, fcat )
        DataStructs.ConvertToNumpyArray( fp, arr )
        fragfps.append( arr )
    print( np.asarray(fragfps).shape )
    return fragfps

if __name__ == '__main__':
    getfragmentfp()





