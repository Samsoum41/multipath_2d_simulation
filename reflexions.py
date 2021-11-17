import turtle as tu
from math import sqrt
from random import random
from sympy import Point, Line, Segment, Polygon

TURTLE_SPEED = 12

"""
Returns the reflexion of a point about a LinearEntity
"""
def reflection_line(pt:Point, lineEntity):
    projectionOnLine = lineEntity.projection(pt)
    return pt + 2*(Point(projectionOnLine) - pt)


def reflection_polygon(pt:Point, poly:Polygon):
    return [reflection_line(pt, seg) for seg in poly.sides]

def segmentInTheGrid(seg:Segment, grille:Polygon):
    I = grille.intersection(seg)
    if dedans(seg.points[0], grille) and dedans(seg.points[1], grille):
        return seg
    elif I:
        if len(I)==1 :
            return Segment(I[0], seg.points[1]) if dedans(seg.points[1], grille) else Segment(seg.points[0], I[0])
        else : 
            return Segment(I[0], I[1]) if I[0].distance(seg.points[0]) < I[1].distance(seg.points[0]) else Segment(I[1], I[0])
    else :
        return None

def multipath(S:Point,A:Point,grille:Polygon,n,turtle, lastPoint = None):
    res=[]
    SA = Segment(S,A)
    if n==0:
        segmentInterieur=segmentInTheGrid(SA,grille)
        if segmentInterieur:
            tracer(segmentInterieur.points[0], segmentInterieur.points[1], turtle, 'red')
            return [segmentInterieur.points[0]]
        raise ValueError("You must have chosen S and A points inside the grid !")
    else:                                  
        # virtualImages contient une liste de couple ( objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        virtualImages={side : reflection_line(S, side) for side in grille.sides if reflection_line(S,side)!=lastPoint}
        res = []
        for key in virtualImages:      
            points_arrive=multipath(virtualImages[key],A,grille,n-1, turtle, lastPoint=S)
            for I in points_arrive:
                segmentInterieur=segmentInTheGrid(Segment(S,I),grille)  
                if (key.contains(I)):
                    departure, arrival = segmentInterieur.points
                    tracer(departure,arrival, turtle)
                    res+=[departure]
        return res                                             
                
"""
    Check if a point A is in a grid. Grid is described as [-x,x,y,-y]
"""
def dedans(A:Point,grille:Polygon):
    xa,ya=A
    grille = grille.bounds
    # Ici on suppose que la grille est de la forme (-abscisse,abscisse,ordonnée,-ordonnée) elle est rectangulaire
    if abs(round(xa))<=abs(grille[0]) and abs(round(ya))<=abs(grille[1]):                     
        return True
    return False

""" 
    Procedure initializing the window and drawing the initial grid.
"""
def tracer_grille(grille:Polygon,turtle):
    x1,y1,x2,y2=grille.bounds
    ADDITIONAL_SIZE = 300
    sizeOfScreen=abs(x1-x2) + ADDITIONAL_SIZE
    tu.setup(sizeOfScreen,sizeOfScreen)
    turtle.up()
    turtle.speed(5)
    turtle.goto(x1,y1)
    turtle.down()
    turtle.goto(x1,y2)
    turtle.goto(x2,y2)
    turtle.goto(x2,y1)
    turtle.goto(x1,y1)
    turtle.speed(TURTLE_SPEED)

"""
    Draws a link between two points
"""
def tracer(P:Point,I:Point,turtle,color_fleche='black'):
    milieu=((P.x+I.x)/2,(P.y+I.y)/2)
    turtle.up()
    turtle.goto(P)
    turtle.down()
    turtle.setheading(turtle.towards(*I))
    turtle.goto(milieu)
    turtle.color(color_fleche)
    turtle.stamp()
    turtle.color('black')
    turtle.goto(I)

"""
    Draw a point of a specific color on a position.
"""
def drawPoint(S:Point,color:str,turtle):
    turtle.up()
    turtle.goto(S)
    turtle.dot(None,color)
    
def main(nombre_de_reflexions=3):
    # Caractéristiques de la simulation :
    COTE = 300
    randNumber = random()*COTE
    S,A = Point(randNumber,COTE/3), Point(-randNumber,COTE/3)
    grille = Polygon(Point(-COTE, -COTE), Point(-COTE, COTE), Point(COTE, COTE), Point(COTE, -COTE))
    turtle = tu.Turtle()
    turtle.hideturtle()
    tracer_grille(grille, turtle)
    drawPoint(S,'blue',turtle)
    drawPoint(A,'red',turtle)
    res = multipath(S,A,grille,nombre_de_reflexions, turtle)
    tu.exitonclick()
    return res
    # On renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m
    lightSpeed=3*(10**8) # Célérité de la lumière en m/s
    n=len(L)
    tu.exitonclick()
    return [L[k][1]*2.6*(10**-4)/lightSpeed for k in range(n)],n

def creneaux(t,periode=0.5,amplitude=1,dephasage=0):
    if ((t+dephasage)//periode)%2==1: return amplitude
    else : return 0

    

#S,A=Point((2*random()-1)*cote,(2*random()-1)*cote)  ,  PoinS,A=Point((2*random()-1)*cote,(2*random()-1)*cote)

"""
S,A = Point(-2*COTE,0), Point(0,0)
#print(main(S,A,1))
segmentInTheGrid(Segment(S,A), grille)
"""
print(main(2))


#Pour n=10, 

#([6307.138812488593, 5522.68050859363, 5544.366510251645, 5178.802950489622, 5316.013544000805, 4623.851208678757, 4743.416490252568, 5707.889277132134, 5323.532661682466, 5346.026561849464, 4589.117562233507, 4743.41649025257, 4438.46820423443, 4518.849411078003, 3911.5214431215895, 4244.997055358225, 3911.521443121589, 4263.8011210655695, 4101.219330881975, 4429.44691807002, 4438.468204234429, 4701.063709417263, 4429.446918070021, 4384.062043356595, 4263.801121065569, 4623.851208678757, 4589.117562233507, 4701.0637094172625, 5522.680508593631, 4743.416490252569, 5544.366510251644, 5707.889277132134, 4244.997055358224, 4743.41649025257, 5178.802950489621, 4518.849411078001, 5323.532661682466, 5316.013544000806, 5346.026561849464, 6307.138812488593], 40)
        
        
        
        
        
        
        
        
        
        
        
        
        