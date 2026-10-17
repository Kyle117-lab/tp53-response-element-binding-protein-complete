import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from check_repository import check
from inspect_structure import get_structure,chain_counts
class TestID143Data(unittest.TestCase):
    def test_core_assets(self):
        self.assertTrue(check())
    def test_chain_lengths(self):
        sizes={c:(aa,dna) for c,aa,dna,_ in chain_counts(get_structure(ROOT/'results/structures/id143_design_complex.pdb'))}
        self.assertEqual(sizes['A'],(123,0));self.assertEqual(sizes['D'],(123,0))
        self.assertEqual(sizes['B'],(0,20));self.assertEqual(sizes['C'],(0,20))
if __name__=='__main__':unittest.main()
