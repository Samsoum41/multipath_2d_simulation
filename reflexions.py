import turtle as tu
from math import sqrt
from random import random
from sympy import Point, Line, Segment, Polygon
from sympy.core.numbers import Integer
from sympy.logic.boolalg import Boolean

TURTLE_SPEED = 12
"""
Returns the reflexion of a point about a LinearEntity
"""
def reflection_line(pt:Point, lineEntity:Segment) -> Point:
    projectionOnLine = lineEntity.projection(pt)
    return pt + 2*(Point(projectionOnLine) - pt)

"""
Adds items to a list if they don't already exist in the list and returns it
"""
def addNewItems(items:list, array:list, keyCondition= None) -> list:
    for item in items:
        if item not in array and keyCondition(item):
            array.append(item)
    return array

"""
Draw the intersection segment of the initial segment with the grid
"""
def segmentInTheGrid(seg:Segment, grille:Polygon) -> Segment:
    S, A = seg.points
    insidePoints = addNewItems([S,A], grille.intersection(seg), keyCondition=lambda pt : dedans(pt,grille))
    insidePoints.sort(key = lambda point : S.distance(point))
    return Segment(insidePoints[0], insidePoints[1]) if insidePoints and len(insidePoints)>1 else Point(*insidePoints) if insidePoints else None


def simulate_reflexions(S:Point,A:Point,grille:Polygon,n,turtle, lastPoint:Point = None) -> list:
    res=[]
    SA = Segment(S,A)
    if n==0:
        segmentInterieur=segmentInTheGrid(SA,grille)
        if segmentInterieur:
            departure, arrival = segmentInterieur.points
            tracer(departure, arrival, turtle, 'red')
            return [departure]
        raise ValueError("You must have chosen S and A points inside the grid !")
    else:                                  
        # virtualImages contient une liste de couple ( objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        virtualImages={side : reflection_line(S, side) for side in grille.sides if reflection_line(S,side)!=lastPoint}
        res = []
        for side in virtualImages:      
            points_arrive=simulate_reflexions(virtualImages[side],A,grille,n-1, turtle, lastPoint=S)
            for I in points_arrive:
                segmentInterieur=segmentInTheGrid(Segment(S,I),grille)  
                if side.contains(I):
                    departure, arrival = segmentInterieur.points
                    tracer(departure,arrival, turtle)
                    res+=[departure]
        return res                                                    
                
"""
    Check if a point A is in a grid. Grid is described as [-x,x,y,-y]
"""
def dedans(A:Point,grille:Polygon) -> bool:
    xa,ya=A
    grille = grille.bounds
    # Ici on suppose que la grille est de la forme (-abscisse,abscisse,ordonnée,-ordonnée) elle est rectangulaire
    if abs(round(xa))<=abs(grille[0]) and abs(round(ya))<=abs(grille[1]):                     
        return True
    return False

""" 
    Procedure initializing the window and drawing the initial grid.
"""
def tracer_grille(grille:Polygon,turtle: tu.Turtle) -> None:
    x1,y1,x2,y2=grille.bounds
    ADDITIONAL_SIZE = 300
    sizeOfScreen=abs(x1-x2) + ADDITIONAL_SIZE
    tu.setup(sizeOfScreen,sizeOfScreen)
    turtle.up()
    turtle.speed(TURTLE_SPEED)
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
def tracer(P:Point,I:Point,turtle,color_fleche : str ='black') -> None:
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
def drawPoint(S:Point,color:str,turtle) -> None:
    turtle.up()
    turtle.goto(S)
    turtle.dot(None,color)
    
"""
Main function where the program should start.
"""
def main(nombre_de_reflexions:int=3) -> None:
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
    res = simulate_reflexions(S,A,grille,nombre_de_reflexions, turtle)
    # On renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m
    tu.exitonclick()


"""
In order to launch the program directly by running the script, we can use the command below. However, as it lauches turtle displaying, it can't run on a virtual machine without display unit, like CI's ones. 
So it will break the tests when pushing.
"""
#main(2)