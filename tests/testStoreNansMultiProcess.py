from __future__ import print_function
import unittest
from rdkit.Chem import AllChem
import numpy, math
from descriptastorus import make_store, DescriptaStore
from descriptastorus.descriptors.DescriptorGenerator import DescriptorGenerator
import contextlib, tempfile, os, shutil, sys
import datahook

one_smiles = "c1ccccc1 0"
many_smiles = "\n".join( [ "C"*i + "c1ccccc1 " + str(i) for i in range(10) ] )

class NanDescriptors(DescriptorGenerator):
    NAME="NANDescriptors"
    def GetColumns(self):
        return [('a', numpy.float32),
                ('b', numpy.float32),
                ('c', numpy.float32),
                ('d', numpy.float32)]
    
    def processMol(self, m, smiles, internalParsing=False):
        return [float('nan')]*4
NanDescriptors()

class TestCase(unittest.TestCase):
    def testNans(self):
        try:
            fname = tempfile.mktemp()+".smi"
            storefname = tempfile.mktemp()+".store"
            print("\n\nfilename:", fname, file=sys.stderr)
            print("storefilename:", storefname, file=sys.stderr)
            with open(fname, 'w') as f:
                f.write(one_smiles)
                
            opts = make_store.MakeStorageOptions( storage=storefname, smilesfile=fname,
                                                  hasHeader=False,
                                                  smilesColumn=0, nameColumn=1,
                                                  seperator=" ", descriptors="NANDescriptors",
                                                  index_inchikey=True )
            make_store.make_store(opts)

            with contextlib.closing(DescriptaStore(storefname)) as store:
                r = store.descriptors().get(0)
                for x in r:
                    self.assertTrue( math.isnan(x) )

        finally:
            if os.path.exists(fname):
                os.unlink(fname)
            if os.path.exists(storefname):
                shutil.rmtree(storefname)

