import unittest
from reflexions import segmentInTheGrid, isBetween

class TestIsBetween(unittest.TestCase):
    def setUp(self):
        self.cote=300
        self.grille=(-self.cote,self.cote,self.cote,-self.cote)
    def test(self):
        self.assertTrue(isBetween([-2*self.cote,0],[0,0], [-self.cote,0]))
        self.assertTrue(isBetween( [2*self.cote,self.cote/2],[0,0], [self.cote,self.cote/4]))
        self.assertTrue(isBetween([-self.cote,2*self.cote], [2*self.cote, -self.cote], [0,self.cote]))
        self.assertFalse(isBetween([-self.cote,2*self.cote], [2*self.cote, -self.cote], [1,self.cote]))
        self.assertFalse(isBetween([-2*self.cote,0],[0,1], [-self.cote,0]))
        self.assertFalse(isBetween( [2*self.cote,self.cote/2],[1,0], [self.cote,self.cote/4]))

class TestSegmentInTheGrid(unittest.TestCase):
    def setUp(self):
        self.cote=300
        self.grille=(-self.cote,self.cote,self.cote,-self.cote)
    # This test contains the arrival point out the grid and the starting point in. 
    def oneInOneOut(self):
        # Here S is at the position (0,0)
        # A is on the left
        self.assertEqual(segmentInTheGrid([-2*self.cote,0],[0,0]), [[-self.cote,0],[0,0]])
        # A is on the right
        self.assertEqual(segmentInTheGrid([2*self.cote,0],[0,0]), [[self.cote,0],[0,0]])
        # A is on the right but at half the height too
        self.assertEqual(segmentInTheGrid([2*self.cote,self.cote/2],[0,0]), [[self.cote,self.cote/4],[0,0]])
        # A is on the top
        self.assertEqual(segmentInTheGrid([0,2*self.cote],[0,0]), [[0,self.cote],[0,0]])
        # A is at the bottom
        self.assertEqual(segmentInTheGrid([0,-2*self.cote],[0,0]), [[0,-self.cote],[0,0]])

    # This test contains the arrival point in the grid and the starting point out. It's the same tests as above but S and A are always swapped
    def oneOutOneIn(self):
        # Here A is at the position (0,0)
        # S is on the left
        self.assertEqual(segmentInTheGrid([0,0], [-2*self.cote,0]), [[-self.cote,0], [0,0]])
        # S is on the right
        self.assertEqual(segmentInTheGrid([0,0], [2*self.cote,0]), [[0,0], [self.cote,0]])
        # S is on the right but at half the height too
        self.assertEqual(segmentInTheGrid([0,0], [2*self.cote,self.cote/2]), [[0,0],[self.cote,self.cote/4]])
        # S is on the top
        self.assertEqual(segmentInTheGrid([0,0], [0,2*self.cote]), [[0,0],[0,self.cote]])
        # S is at the bottom
        self.assertEqual(segmentInTheGrid([0,0], [0,-2*self.cote]), [[0,-self.cote],[0,0]])
    # This test contains the arrival point and the starting point in the grid
    def bothIn(self):
        self.assertEqual(segmentInTheGrid([-self.cote/2,0], [self.cote/2,0]), [[-self.cote/2,0], [self.cote/2,0]])
        self.assertEqual(segmentInTheGrid([self.cote/2,self.cote/2], [-self.cote/2, -self.cote/2]), [[self.cote/2,self.cote/2], [-self.cote/2, -self.cote/2]])
    # This test contains the arrival point and the starting point out the grid
    def bothOut(self):
        self.assertEqual(segmentInTheGrid([3*self.cote,0], [2*self.cote,0]), [])
        self.assertEqual(segmentInTheGrid([-self.cote, 2*self.cote], [self.cote, 2*self.cote]), [])
        self.assertEqual(segmentInTheGrid([3*self.cote,0], [0,3*self.cote]), [])
        self.assertEqual(segmentInTheGrid([-self.cote,2*self.cote], [2*self.cote, -self.cote]), [[0,self.cote],[self.cote,0]])




if __name__ == '__main__':
    unittest.main()