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
@click.argument( 'infile' )
@click.option( '--output','-o', default = 'calc_frag_fp.npz' )
def getfragmentfp( infile, output ):
    fragfps = []
    sdf = Chem.SDMolSupplier( infile )
    counter = 0
    for mol in sdf:
        if mol == None:
            continue
        counter += 1
        nAdded = fcgen.AddFragsFromMol( mol, fcat )
    print( "{} mols read".format( counter ) )
    for mol in sdf:
        if mol == None:
            continue
        arr = np.zeros((1,))
        fp = fpgen.GetFPForMol( mol, fcat )
        DataStructs.ConvertToNumpyArray( fp, arr )
        fragfps.append( arr )
    fragfps = np.asarray( fragfps )
    np.savez( output, x = fragfps )
    print( fragfps.shape )
    print( 'done!' )

if __name__ == '__main__':
    getfragmentfp()
