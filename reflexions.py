import turtle as tu
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import random

            
"""
    Returns the virtual images of S on the grid as (point,(orientation,position_of_reflection_plane)) pairs
"""
def reflexions_possibles(S,grille):
    # On suppose que la grille est de la forme (-x,x,y-y), donc rectangulaire.
    x,y=grille[1],grille[2]                                                     
    xs,ys=S
    res=[((2*x-xs,ys),('vertical',x)),((-2*x-xs,ys),('vertical',-x)),((xs,2*y-ys),('horizontal',y)),((xs,-2*y-ys),('horizontal',-y))]
    # We filter edges that are inside the grid, why ? 
    #TODO : Why ?
    if xs>=x: res.remove(((2*x-xs,ys),('vertical',x)))
    if xs<=-x: res.remove(((-2*x-xs,ys),('vertical',-x)))
    if ys<=-y:res.remove(((xs,-2*y-ys),('horizontal',-y)))
    if ys>=y:res.remove(((xs,2*y-ys),('horizontal',y)))
    return res
    # On peut remarquer que res ne sera jamais vide, elle contient toujours au moins 2 éléments



def distance(A,B): 
    ((xa,ya),(xb,yb))=A,B
    return(sqrt((xa-xb)**2 + (ya-yb)**2))

def multipath(S,A,grille,n,derniere_reflexion=None):
    res=[]
    if n==0:
        segmentInterieur=segmentInTheGrid(S,A,grille)
        if segmentInterieur:
            # A must be the second element of segmentInterieur
            tracer(segmentInterieur[0], A,'red')
            return [segmentInterieur[0]]
        return []
    else:                                       
        # virtualImages contient une liste de couple ( objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        virtualImages=reflexions_possibles(S,grille) 
        res = []
        for image in virtualImages:      
            points_arrive=multipath(image[0],A,grille,n-1,derniere_reflexion=image[1])
            for I in points_arrive:
                segmentInterieur=segmentInTheGrid(S,I,grille)  
                # On détermine l'intersection du nouveau point avec le point intermédiaire image
                if segmentInterieur:
                    # Si S est bien le premier point source, il se distingue en étant à l'intérieur, alors on trace le segment [SI2]
                    departure, arrival = segmentInterieur
                    tracer(departure,arrival)
                    res+=[departure]
        return res
"""
def multipath(S,A,grille,n,derniere_reflexion=None):
    res=[]
    if n==0:
        S=intersection(S,A,derniere_reflexion,grille)
        if S:
            tracer(S,A,'red')
        return S
    else:                                       
        # virtualImages contient une liste de couple ( objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        virtualImages=reflexions_possibles(S,grille) 
        for image in virtualImages:                                        
            points=multipath(image[0],A,grille,n-1,derniere_reflexion=image[1]) 
            res = []
            for I in points:
                if I[0]:                                                 
                    # I[0] vaut False si c'est un point fictif, qui ne se trouve pas sur la grille ou qui ne peut pas être tracé
                    I2=intersection(image[0],I[0],image[1],grille)                      
                    # On détermine l'intersection du nouveau point avec le point intermédiaire image
                    if I2:
                        # Si S est bien le premier point source, il se distingue en étant à l'intérieur, alors on trace le segment [SI2]
                        if dedans(S,grille):                                    
                            tracer(S,I2)
                        # Le point S n'est pas le véritable point source mais une source fictive, on ajoute seulement la distance I,I2
                        if I2!=I[0]:
                            # On trace le rayon entre le nouveau point et le point intermédiaire 
                            tracer(I2,I[0])   
"""                                                       
                
"""
    Check if a point A is in a grid. Grid is described as [-x,x,y,-y]
"""
def dedans(A,grille):
    xa,ya=A
    # Ici on suppose que la grille est de la forme (-abscisse,abscisse,ordonnée,-ordonnée) elle est rectangulaire
    if abs(round(xa))<=abs(grille[0]) and abs(round(ya))<=abs(grille[2]):                     
        return True
    return False

def intersection(line1, line2):
    xa,ya = line1[0]
    xb,yb = line1[1]
    xc,yc = line2[0]
    xd,yd = line2[1]
    # Check if each line is well defined 
    if xa == xb and ya == yb:
        raise ValueError('Line 1 is not defined by two different point, points are the same !')
    elif xc == xd and yc == yd:
        raise ValueError('Line 2 is not defined by two different point, points are the same !')
    # Check if the two lines are parallel using cross product
    elif (xb-xa)*(yd-yc) - (xd-xc)*(yb-ya) == 0:
        return None 
    else :
        # This is the result of solving the system of equations of the intersection of two lines. This value exist because the cross product is not null here.
        k = ((xb-xd)*(ya-yd) - (yb-yd)*(xa-xb))/((xc-xd)*(ya-yb) - (xa-xb)*(yc-yd))
        return [k*xc + (1-k)*xd, k*yc + (1-k)*yd]



def isBetween(departure,arrival,point):
    if departure == arrival : 
        raise ValueError("Departure and arrival are the same point !")
    else :
        xa,ya = departure
        xb,yb = arrival
        xc,yc = point
        if xa != xb:
            lbda = (xc-xb)/(xa-xb)
            return 0 <= lbda <= 1 and yc == lbda*ya + (1-lbda)*yb
        else : 
            lbda = (yc-yb)/(ya-yb)
            return 0 <= lbda <= 1 and xc == lbda*xa + (1-lbda)*xb

def segmentInTheGrid(S,A,grille):
    # D'abord on vérifie si le point est dans la grille auquel cas on renvoie S lui-meme
    # on cherche l'intersection du segment [SA] avec le miroir "derniere_reflexion"
    if S == A : 
        raise ValueError("Departure and arrival are the same point !")
    hauteur, cote = grille[2], grille[1]
    xa,ya=A
    xs,ys=S
    # We define a line by two different points of this line
    currentLine = []
    linesOfGrid = [[0,cote], [cote,cote]], [[0, -cote], [-cote, -cote]], [[cote, 0], [cote,cote]], [[-cote, 0], [-cote, cote]]
    droiteCoteHaut,droiteCoteBas,droiteCoteDroit,droiteCoteGauche = linesOfGrid 
    # The list above may contain None Value
    intersectionsWithGrid = list(map(lambda line : intersection(line, [S,A]), linesOfGrid))
    # We filter NoneValues and intersections out of the grid
    intersectionsInTheGrid = list(filter(lambda point : point!=None and dedans(point, grille) and isBetween(S, A, point), intersectionsWithGrid))
    if dedans(S,grille) and dedans(A, grille):
        return [S,A]
    elif dedans(S,grille): # Then len(intersectionsInTheGrid)>0 :
        return [S, intersectionsInTheGrid[0]]
    elif dedans(A, grille) and len(intersectionsInTheGrid)>0 : 
        return [intersectionsInTheGrid[0], A]
    elif intersectionsInTheGrid: # Then len(intersectionsInTheGrid) == 2
        return intersectionsInTheGrid
    else:
        return None



"""
    Returns the intersection of a segment between 2 edges with a miror. It's useful when one of the edges is behind the mirror. 

def intersection(S,A,plan_reflexion,grille):
    # D'abord on vérifie si le point est dans la grille auquel cas on renvoie S lui-meme
    # on cherche l'intersection du segment [SA] avec le miroir "derniere_reflexion"
    orientation,pos_ref=plan_reflexion
    xa,ya=A
    xs,ys=S
    # On détermine l'équation de la droite (SA) : y=mx+b
    m=(ys-ya)/(xs-xa)
    b=ya-m*xa
    # Si le miroir est horizontal, sa position est une ordonnée
    if orientation == 'horizontal':                                         
        yintersection=pos_ref
        xintersection=(yintersection-b)/m
    # Si le miroir est vertical, sa position est une abscisse
    else:                                                                   
        xintersection=pos_ref
        yintersection=xintersection*m+b 
    # Si le point d'intersection déterminé n'est pas sur la grille, il n'existe pas, on renvoie False
    if dedans((xintersection,yintersection),grille):
        drawPoint((xintersection,yintersection),'black')
        return (xintersection,yintersection) 
    return False     

"""

"""
def intersection(S,A,grille):
    xa,ya=A
    xs,ys=S
    cote = grille[1]
    hauteur = grille[2]
    # On détermine l'équation de la droite (SA) : y=mx+b
    m=(ys-ya)/(xs-xa)
    b=ya-m*xa
    resultPoint =[]
    # Si le miroir est horizontal, sa position est une ordonnée
    if -hauteur<=ys<=hauteur:
        if xs<xa:
            resultPoint = [-cote,-m*cote+b]
        else:
            resultPoint = [cote,m*cote+b]
    elif ys>hauteur:
        resultPoint = [(hauteur-b)/m, hauteur]
    else :
        resultPoint = [(-hauteur-b)/m, -hauteur]
    drawPoint(resultPoint,'black')
    print(dedans(resultPoint,grille))
    return resultPoint

    if orientation == 'horizontal':                                         
        yintersection=pos_ref
        xintersection=(yintersection-b)/m
    # Si le miroir est vertical, sa position est une abscisse
    else:                                                                   
        xintersection=pos_ref
        yintersection=xintersection*m+b 
    # Si le point d'intersection déterminé n'est pas sur la grille, il n'existe pas, on renvoie False
    if dedans((xintersection,yintersection),grille):
        drawPoint((xintersection,yintersection),'black')
        return (xintersection,yintersection) 
    return False     
"""

""" 
    Procedure initializing the window and drawing the initial grid.
"""
def tracer_grille(grille):
    x1,x2,y1,y2=grille
    ADDITIONAL_SIZE = 300
    sizeOfScreen=abs(x1-x2) + ADDITIONAL_SIZE
    tu.setup(sizeOfScreen,sizeOfScreen)
    tu.up()
    tu.speed(5)
    tu.goto(x1,y1)
    tu.down()
    tu.goto(x1,y2)
    tu.goto(x2,y2)
    tu.goto(x2,y1)
    tu.goto(x1,y1)
    tu.speed(7)

"""
    Draws a link between two points
"""
def tracer(P,I,color_fleche='black'):
    x1,y1=P
    x2,y2=I
    milieu=((x1+x2)/2,(y1+y2)/2)
    tu.up()
    tu.goto(P)
    tu.down()
    tu.setheading(tu.towards(*I))
    tu.goto(milieu)
    tu.color(color_fleche)
    tu.stamp()
    tu.color('black')
    tu.goto(I)

"""
    Draw a point of a specific color on a position.
"""
def drawPoint(S,color):
    tu.up()
    tu.goto(S)
    tu.dot(None,color)
    

def main(S,A,grille,nombre_de_reflexions=3):
    # Dans l'ordre, on trace la grille, place les points de départ et d'arrivés S et A, puis on trace les différents rayons de S à A sur la grille en n (ici n=2) réflexions.
    tracer_grille(grille)
    drawPoint(S,'blue')
    drawPoint(A,'red')
    L=multipath(S,A,grille,nombre_de_reflexions)
    # On renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m
    lightSpeed=3*(10**8) # Célérité de la lumière en m/s
    n=len(L)
    return [L[k][1]*2.6*(10**-4)/lightSpeed for k in range(n)],n





def creneaux(t,periode=0.5,amplitude=1,dephasage=0):
    if ((t+dephasage)//periode)%2==1: return amplitude
    else : return 0

    
# Caractéristiques de la simulation :
cote=300
grille=(-cote,cote,cote,-cote)
S,A=[(2*random()-1)*cote,(2*random()-1)*cote]  ,  [(2*random()-1)*cote,(2*random()-1)*cote]



#print(main(S,A,grille,1))
segmentInTheGrid([-2*cote,0],[0,0], grille), [[-cote,0],[0,0]]


tu.hideturtle()
tu.exitonclick()

#Pour n=10, 

#([6307.138812488593, 5522.68050859363, 5544.366510251645, 5178.802950489622, 5316.013544000805, 4623.851208678757, 4743.416490252568, 5707.889277132134, 5323.532661682466, 5346.026561849464, 4589.117562233507, 4743.41649025257, 4438.46820423443, 4518.849411078003, 3911.5214431215895, 4244.997055358225, 3911.521443121589, 4263.8011210655695, 4101.219330881975, 4429.44691807002, 4438.468204234429, 4701.063709417263, 4429.446918070021, 4384.062043356595, 4263.801121065569, 4623.851208678757, 4589.117562233507, 4701.0637094172625, 5522.680508593631, 4743.416490252569, 5544.366510251644, 5707.889277132134, 4244.997055358224, 4743.41649025257, 5178.802950489621, 4518.849411078001, 5323.532661682466, 5316.013544000806, 5346.026561849464, 6307.138812488593], 40)
        
        
        
        
        
        
        
        
        
        
        
        
        