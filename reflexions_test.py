import unittest
from reflexions import segmentInTheGrid, isBetween, intersection

class TestSegmentInTheGrid(unittest.TestCase):
    def setUp(self):
        self.cote=300
        self.grille=(-self.cote,self.cote,self.cote,-self.cote)
    # This test contains the arrival point out the grid and the starting point in. 
    def test_oneInOneOut(self):
        # Here S is at the position (0,0)
        # A is on the left
        self.assertEqual(segmentInTheGrid([-2*self.cote,0],[0,0], self.grille), [[-self.cote,0],[0,0]])
        # A is on the right
        self.assertEqual(segmentInTheGrid([2*self.cote,0],[0,0], self.grille), [[self.cote,0],[0,0]])
        # A is on the right but at half the height too
        self.assertEqual(segmentInTheGrid([2*self.cote,self.cote/2],[0,0], self.grille), [[self.cote,self.cote/4],[0,0]])
        # A is on the top
        self.assertEqual(segmentInTheGrid([0,2*self.cote],[0,0], self.grille), [[0,self.cote],[0,0]])
        # A is at the bottom
        self.assertEqual(segmentInTheGrid([0,-2*self.cote],[0,0], self.grille), [[0,-self.cote],[0,0]])

    # This test contains the arrival point in the grid and the starting point out. It's the same tests as above but S and A are always swapped
    def test_oneOutOneIn(self):
        # Here A is at the position (0,0)
        # S is on the left
        self.assertEqual(segmentInTheGrid([0,0], [-2*self.cote,0], self.grille), [[-self.cote,0], [0,0]])
        # S is on the right
        self.assertEqual(segmentInTheGrid([0,0], [2*self.cote,0], self.grille), [[0,0], [self.cote,0]])
        # S is on the right but at half the height too
        self.assertEqual(segmentInTheGrid([0,0], [2*self.cote,self.cote/2], self.grille), [[0,0],[self.cote,self.cote/4]])
        # S is on the top
        self.assertEqual(segmentInTheGrid([0,0], [0,2*self.cote], self.grille), [[0,0],[0,self.cote]])
        # S is at the bottom
        self.assertEqual(segmentInTheGrid([0,0], [0,-2*self.cote], self.grille), [[0,-self.cote],[0,0]])
    # This test contains the arrival point and the starting point in the grid
    def test_bothIn(self):
        self.assertEqual(segmentInTheGrid([-self.cote/2,0], [self.cote/2,0], self.grille), [[-self.cote/2,0], [self.cote/2,0]])
        self.assertEqual(segmentInTheGrid([self.cote/2,self.cote/2], [-self.cote/2, -self.cote/2], self.grille), [[self.cote/2,self.cote/2], [-self.cote/2, -self.cote/2]])
    # This test contains the arrival point and the starting point out the grid
    def test_bothOut(self):
        self.assertEqual(segmentInTheGrid([3*self.cote,0], [2*self.cote,0], self.grille), [])
        self.assertEqual(segmentInTheGrid([-self.cote, 2*self.cote], [self.cote, 2*self.cote], self.grille), [])
        self.assertEqual(segmentInTheGrid([3*self.cote,0], [0,3*self.cote], self.grille), [])
        self.assertEqual(segmentInTheGrid([-self.cote,2*self.cote], [2*self.cote, -self.cote], self.grille), [[0,self.cote],[self.cote,0]])




if __name__ == '__main__':
    unittest.main()