import unittest
from reflexions import segmentInTheGrid, isBetween, intersection

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

class TestIntersection(unittest.TestCase):
    def test(self):
        COTE = 300
        self.assertEqual(intersection([[-COTE,COTE], [0,0]],[[COTE, COTE], [COTE, 0]]), [COTE, -COTE])
        self.assertEqual(intersection([[-COTE,COTE], [0,0]],[[COTE, COTE], [0, COTE]]), [-COTE, COTE])
        self.assertEqual(intersection([[-COTE,COTE], [0, COTE]],[[-COTE, -COTE], [0, -COTE]]), None)
        self.assertEqual(intersection([[-COTE,COTE], [0,-COTE]],[[0, COTE], [0, 0]]), [0, -COTE])
        self.assertEqual(intersection([[-COTE,COTE], [0,-COTE]],[[0, COTE], [0, 0]]), [0, -COTE])
        self.assertEqual(intersection([[0, COTE], [0, 0]],[[-COTE,COTE], [0,-COTE]]), [0, -COTE])
        self.assertEqual(intersection([[COTE, 0], [COTE, COTE]], [[-2*COTE,0], [0,0]]), [COTE,0])


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