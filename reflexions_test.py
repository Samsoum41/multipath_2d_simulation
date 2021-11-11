import unittest
from reflexions import segmentInTheGrid, dedans
from sympy import Point, Segment, Polygon

class TestDedans(unittest.TestCase):
    def setUp(self):
        self.cote=300
        self.grille=Polygon(Point(-self.cote, -self.cote), Point(-self.cote, self.cote), Point(self.cote, self.cote), Point(self.cote, -self.cote))
    def test_In(self):
        self.assertTrue(dedans(Point(0,0), self.grille))
        self.assertTrue(dedans(Point(self.cote/2,0), self.grille))
        self.assertTrue(dedans(Point(0,self.cote/2), self.grille))
        self.assertTrue(dedans(Point(self.cote/2,self.cote/2), self.grille))
        self.assertTrue(dedans(Point(self.cote,0), self.grille))
        self.assertTrue(dedans(Point(0,self.cote), self.grille))
        self.assertTrue(dedans(Point(self.cote,self.cote), self.grille))      
    def test_Out(self):
        self.assertFalse(dedans(Point(2*self.cote,self.cote), self.grille))      
        self.assertFalse(dedans(Point(self.cote,2*self.cote), self.grille))
        self.assertFalse(dedans(Point(0,2*self.cote), self.grille))
        self.assertFalse(dedans(Point(2*self.cote,0), self.grille))
        self.assertFalse(dedans(Point(self.cote,self.cote+1), self.grille))

        
        

class TestSegmentInTheGrid(unittest.TestCase):
    def setUp(self):
        self.cote=300
        self.grille=Polygon(Point(-self.cote, -self.cote), Point(-self.cote, self.cote), Point(self.cote, self.cote), Point(self.cote, -self.cote))
    # This test contains the arrival point out the grid and the starting point in. 
    def test_oneInOneOut(self):
        # Here S is at the position (0,0)
        # A is on the left
        self.assertEqual(segmentInTheGrid(Segment(Point(-2*self.cote,0),Point(0,0)), self.grille), Segment(Point(-self.cote,0),Point(0,0)))
        # A is on the right
        self.assertEqual(segmentInTheGrid(Segment(Point(2*self.cote,0),Point(0,0)), self.grille), Segment(Point(self.cote,0),Point(0,0)))
        # A is on the right but at half the height too
        self.assertEqual(segmentInTheGrid(Segment(Point(2*self.cote,self.cote/2),Point(0,0)), self.grille), Segment(Point(self.cote,self.cote/4),Point(0,0)))
        # A is on the top
        self.assertEqual(segmentInTheGrid(Segment(Point(0,2*self.cote),Point(0,0)), self.grille), Segment(Point(0,self.cote),Point(0,0)))
        # A is at the bottom
        self.assertEqual(segmentInTheGrid(Segment(Point(0,-2*self.cote),Point(0,0)), self.grille), Segment(Point(0,-self.cote),Point(0,0)))

    # This test contains the arrival point in the grid and the starting point out. It's the same tests as above but S and A are always swapped
    def test_oneOutOneIn(self):
        # Here A is at the position (0,0)
        # S is on the left
        self.assertEqual(segmentInTheGrid(Segment(Point(0,0),Point(-2*self.cote,0)), self.grille), Segment(Point(0,0), Point(-self.cote,0)))
        # S is on the right
        self.assertEqual(segmentInTheGrid(Segment(Point(0,0),Point(2*self.cote,0)), self.grille), Segment(Point(0,0),Point(self.cote,0)))
        # S is on the right but at half the height too
        self.assertEqual(segmentInTheGrid(Segment(Point(0,0),Point(2*self.cote,self.cote/2)), self.grille), Segment(Point(0,0),Point(self.cote,self.cote/4)))
        # S is on the top
        self.assertEqual(segmentInTheGrid(Segment(Point(0,0),Point(0,2*self.cote)), self.grille), Segment(Point(0,0),Point(0,self.cote)))
        # S is at the bottom
        self.assertEqual(segmentInTheGrid(Segment(Point(0,0),Point(0,-2*self.cote)), self.grille), Segment(Point(0,0),Point(0,-self.cote)))
    # This test contains the arrival point and the starting point in the grid
    def test_bothIn(self):
        self.assertEqual(segmentInTheGrid(Segment(Point(-self.cote/2,0),Point(self.cote/2,0)), self.grille), Segment(Point(-self.cote/2,0),Point(self.cote/2,0)))
        self.assertEqual(segmentInTheGrid(Segment(Point(self.cote/2,self.cote/2),Point(-self.cote/2, -self.cote/2)), self.grille), Segment(Point(self.cote/2,self.cote/2),Point(-self.cote/2, -self.cote/2)))
    # This test contains the arrival point and the starting point out the grid
    def test_bothOut(self):
        self.assertEqual(segmentInTheGrid(Segment(Point(3*self.cote,0),Point(2*self.cote,0)), self.grille), None)
        self.assertEqual(segmentInTheGrid(Segment(Point(-self.cote, 2*self.cote),Point(self.cote, 2*self.cote)), self.grille), None)
        self.assertEqual(segmentInTheGrid(Segment(Point(3*self.cote,0),Point(0,3*self.cote)), self.grille), None)
        self.assertEqual(segmentInTheGrid(Segment(Point(-self.cote,2*self.cote),Point(2*self.cote, -self.cote)), self.grille), Segment(Point(0,self.cote),(self.cote, 0)))


if __name__ == '__main__':
    unittest.main()