import turtle as tu
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import random

            
# Cette fonction renvoie les réflexions possibles(!) de S sur la grille sous la forme de couples (point,(orientation,position_du_plan_de_réflexion))
def reflexions_possibles(S,grille):
    x,y=grille[1],grille[2]                                                     # On suppose que la grille est de la forme (-x,x,y-y), donc rectangulaire.
    xs,ys=S
    res=[((2*x-xs,ys),('vertical',x)),((-2*x-xs,ys),('vertical',-x)),((xs,2*y-ys),('horizontal',y)),((xs,-2*y-ys),('horizontal',-y))]
    # On fait les tests
    if xs>=x: res.remove(((2*x-xs,ys),('vertical',x)))
    if xs<=-x: res.remove(((-2*x-xs,ys),('vertical',-x)))
    if ys<=-y:res.remove(((xs,-2*y-ys),('horizontal',-y)))
    if ys>=y:res.remove(((xs,2*y-ys),('horizontal',y)))

    return(res)                                                                 # On peut remarquer que res ne sera jamais vide, elle contient toujours au moins 2 éléments



def distance(A,B): 
    ((xa,ya),(xb,yb))=A,B
    return(sqrt(  (xa-xb)**2 + (ya-yb)**2 ))


def multipath(S,A,grille,n,derniere_reflexion=None):
    res=[]
    if n==0:
        S=intersection(S,A,derniere_reflexion,grille)
        if S!=False:
            tracer(S,A,True,'red')
            return([[S,distance(S,A)]])
        else: return [[False,False]]        
    else:
        L=reflexions_possibles(S,grille)                                        # L contient une liste de couple ( objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        for P in L:                                        
            points=multipath(P[0],A,grille,n-1,derniere_reflexion=P[1]) 
            for I in points:
                if I[0]!=False:                                                 # I[0] vaut False si c'est un point fictif, qui ne se trouve pas sur la grille ou qui ne peut pas être tracé

                    I2=intersection(P[0],I[0],P[1],grille)                      # On détermine l'intersection du nouveau point avec le point intermédiaire P
                    if I2!=False:
                        if dedans(S,grille):                                    # Si S est bien le premier point source, il se distingue en étant à l'intérieur, alors on trace le segment [SI2]
                            tracer(S,I2,True)
                            # et on rajoute la distance entre S et I2 en plus de celle entre I et I2
                            res.append([I2,distance(I[0],I2)+I[1]+distance(S,I2)])
                        else :                                                  # Le point S n'est pas le véritable point source mais une source fictive, on ajoute seulement la distance I,I2
                            res.append([I2,distance(I[0],I2)+I[1]]) 
                        if I2!=I[0]:
                            tracer(I2,I[0],True)                                # On trace le rayon entre le nouveau point et le point intermédiaire 
        return res
            
                

def dedans(A,grille):
    xa,ya=A
    if abs(xa)<=abs(grille[0]) and abs(ya)<=abs(grille[2]):                     # Ici on suppose que la grille est de la forme (-abscisse,abscisse,ordonnée,-ordonnée) elle est rectangulaire
        return True
    return False

def intersection(S,A,plan_reflexion,grille):
    # D'abord on vérifie si le point est dans la grille auquel cas on renvoie S lui-meme
    if dedans(S,grille): return S
    # on cherche l'intersection du segment [SA] avec le miroir "derniere_reflexion"
    orientation,pos_ref=plan_reflexion
    xa,ya=A
    xs,ys=S
    if xs!=xa:
        # On détermine l'équation de la droite (SA) : y=mx+b
        m=(ys-ya)/(xs-xa)
        b=ya-m*xa
        if orientation == 'horizontal':                                         # Si le miroir est horizontal, sa position est une ordonnée
            yintersection=pos_ref
            xintersection=(yintersection-b)/m
        else:                                                                   # Si le miroir est vertical, sa position est une abscisse
            xintersection=pos_ref
            yintersection=xintersection*m+b 
        if not(dedans((xintersection,yintersection),grille)): return False      # Si le point d'intersection déterminé n'est pas sur la grille, il n'existe pas, on renvoie False
        placer((xintersection,yintersection),'black')
        return (xintersection,yintersection)
    
    return(xs,pos_ref) # Dans ce cas pos_ref est l'ordonnée du plan de réflexion, lieu où se situe l'intersection
        

def tracer_grille(grille):
    x1,x2,y1,y2=grille
    taille=abs(x1-x2) + 300
    tu.setup(taille,taille)
    tu.up()
    tu.speed(2)
    tu.goto(x1,y1)
    tu.down()
    tu.goto(x1,y2)
    tu.goto(x2,y2)
    tu.goto(x2,y1)
    tu.goto(x1,y1)
    tu.speed(3)

def tracer(P,I,fleche=False,color_fleche='black'):
    x1,y1=P
    x2,y2=I
    tu.up()
    tu.goto(P)
    tu.down()
    if fleche==False:
        tu.goto(I)
    else:
        milieu=((x1+x2)/2,(y1+y2)/2)
        tu.setheading(tu.towards(I))
        tu.goto(milieu)
        tu.color(color_fleche)
        tu.stamp()
        tu.color('black')
        tu.goto(I)

def placer(S,color):
    tu.up()
    tu.goto(S)
    tu.dot(None,color)
    

def afficher_resultat(S,A,grille,nombre_de_reflexions=3):
    # Dans l'ordre, on trace la grille, place les points de départ et d'arrivés S et A, puis on trace les différents rayons de S à A sur la grille en n (ici n=2) réflexions.
    tracer_grille(grille)
    placer(S,'blue')
    placer(A,'red')
    L=multipath(S,A,grille,nombre_de_reflexions)
    # On renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m
    c=3*(10**8) # Célérité de la lumière en m/s
    n=len(L)
    return [L[k][1]*2.6*(10**-4)/c for k in range(n)],n





def creneaux(t,periode=0.5,amplitude=1,dephasage=0):
    if ((t+dephasage)//periode)%2==1: return amplitude
    else : return 0

    
# Caractéristiques de la simulation :
cote=300
grille=(-cote,cote,cote,-cote)
S,A=(((2*random()-1)*cote,(2*random()-1)*cote),((2*random()-1)*cote,(2*random()-1)*cote))



print(afficher_resultat(S,A,grille,2))
print(S,A)

tu.hideturtle()
tu.exitonclick()

#Pour n=10, 

#([6307.138812488593, 5522.68050859363, 5544.366510251645, 5178.802950489622, 5316.013544000805, 4623.851208678757, 4743.416490252568, 5707.889277132134, 5323.532661682466, 5346.026561849464, 4589.117562233507, 4743.41649025257, 4438.46820423443, 4518.849411078003, 3911.5214431215895, 4244.997055358225, 3911.521443121589, 4263.8011210655695, 4101.219330881975, 4429.44691807002, 4438.468204234429, 4701.063709417263, 4429.446918070021, 4384.062043356595, 4263.801121065569, 4623.851208678757, 4589.117562233507, 4701.0637094172625, 5522.680508593631, 4743.416490252569, 5544.366510251644, 5707.889277132134, 4244.997055358224, 4743.41649025257, 5178.802950489621, 4518.849411078001, 5323.532661682466, 5316.013544000806, 5346.026561849464, 6307.138812488593], 40)
        
        
        
        
        
        
        
        
        
        
        
        
        