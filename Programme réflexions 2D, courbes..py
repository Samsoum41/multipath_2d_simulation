import turtle as tu
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import random


##Caractéristiques de la simulation :
cote=900
grille=(-cote,cote,cote,-cote)

##Générations de 2 positions aléatoires
S,A=((int((2*random()-1)*cote),int((2*random()-1)*cote)),(int((2*random()-1)*cote),int((2*random()-1)*cote)))
print(S,A)
periode_codage_ajustee=0.1*(10**-6 )  # frequence du signal: 10^ Hz, pour c= 3.10^-5 !! il y a 10^3 d'écart !

"""
Cette fonction renvoie les réflexions possibles(!) de S sur la grille sous la forme de couples (point,(orientation,position_du_plan_de_réflexion))
"""
def reflexions_possibles(S,grille):  
    x,y=grille[1],grille[2]  # On suppose que la grille est de la forme (-x,x,y-y), donc rectangulaire.
    xs,ys=S
    res=[((2*x-xs,ys),('vertical',x)),((-2*x-xs,ys),('vertical',-x)),((xs,2*y-ys),('horizontal',y)),((xs,-2*y-ys),('horizontal',-y))]
    # On fait les tests
    if xs>=x: res.remove(((2*x-xs,ys),('vertical',x)))
    if xs<=-x: res.remove(((-2*x-xs,ys),('vertical',-x)))
    if ys<=-y:res.remove(((xs,-2*y-ys),('horizontal',-y)))
    if ys>=y:res.remove(((xs,2*y-ys),('horizontal',y)))
    return(res)  # On peut remarquer que res ne sera jamais vide, elle contient toujours au moins 2 éléments


def distance(A,B): 
    ((xa,ya),(xb,yb))=A,B
    return(sqrt(  (xa-xb)**2 + (ya-yb)**2 ))


def multipath(S,A,grille,n,derniere_reflexion=None):
    res=[]
    if n==0:
        S=intersection(S,A,derniere_reflexion,grille)
        if S!=False:
            return([[S,distance(S,A)]])
        else: return [[False,False]]
    else:
        L=reflexions_possibles(S,grille)  # L contient une liste de couple (objet virtuel, direction du miroir par rapport auquel les objets sont symétriques)
        for P in L:                                                    
            points = multipath(P[0], A, grille, n-1, derniere_reflexion=P[1]) 
            for I in points:
                if I[0]!=False:  # I[0] vaut False si c'est un point fictif, qui ne se trouve pas sur la grille ou qui ne peut pas être tracé
                    I2=intersection(P[0],I[0],P[1],grille)  # On détermine l'intersection du nouveau point avec le point intermédiaire P
                    if I2!=False:
                        if dedans(S,grille):  # Si S est bien le premier point source, il se distingue en étant à l'intérieur, alors on trace le segment [SI2] et on rajoute la distance entre S et I2 en plus de celle entre I et I2
                            res.append([I2,distance(I[0],I2)+I[1]+distance(S,I2)])                            
                        else :  # Le point S n'est pas le véritable point source mais une source fictive, on ajoute seulement la distance I,I2
                            res.append([I2,distance(I[0],I2)+I[1]])
        return res
            

def dedans(A,grille):
    xa,ya=A
    if abs(xa)<=abs(grille[0]) and abs(ya)<=abs(grille[2]):  # Ici on suppose que la grille est de la forme (-abscisse,abscisse,ordonnée,-ordonnée) elle est rectangulaire
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
        if orientation == 'horizontal':  # Si le miroir est horizontal, sa position est une ordonnée
            yintersection=pos_ref
            xintersection=(yintersection-b)/m
        else:  # Si le miroir est vertical, sa position est une abscisse
            xintersection=pos_ref
            yintersection=xintersection*m+b
        if not(dedans((xintersection,yintersection),grille)): return False  # Si le point d'intersection déterminé n'est pas sur la grille, il n'existe pas, on renvoie False
        return (xintersection,yintersection)
    return(xs,pos_ref)  # Dans ce cas pos_ref est l'ordonnée du plan de réflexion, lieu où se situe l'intersection
        
"""
renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m=2.6*10^-2 cm
"""
def afficher_resultat(S,A,grille,nombre_de_reflexions=3):
    L=multipath(S,A,grille,nombre_de_reflexions)
    c=3*(10**5) # Célérité de la lumière en m/s, réduite pour éviter les erreurs d'approximations, en accord avec la période de codage.
    n=len(L)
    R=[L[k][1]*2.6*(10**(-4))/c for k in range(n)]  # R contient la liste des distances de retard en m.
    return R


def graphe(S,A,grille,nombre_de_reflexions_max=3,periode=0.5,amplitude=1,coef_de_ref=0.5):
    t=np.linspace(0,20*periode_codage_ajustee,1000)  # Sur 1 milliseconde
    c=3*(10**5)  # Célérité de la lumière en m/s, réduite pour éviter les erreurs d'approximations, en accord avec la période de codage.
    p=len(t)
    L=[ afficher_resultat(S,A,grille,i) for i in range(nombre_de_reflexions_max+1)]  # L est la liste de ième terme les temps de parcours en i réflexions dans cette configuration
    y2=[ calcul(L,t[k],coef_de_ref,amplitude) for k in range(p)]  # y2 est une liste, de même taille que t, qui contient à chaque instant t[k] la superposition de tous ces créneaux
    plt.plot(t,y2,label='avec')
    plt.show()


def calcul(liste_de_retards,t,coef_de_ref,ampli,test=None):
    # La puissance de l'émetteur est proportionnel à l'amplitude au carré, donc à 1, de plus, cette puissance décroit en 4piR^2
    n=len(liste_de_retards)  # n est le nb de réflexions maximal -1
    c=3*(10**5)  # Célérité de la lumière en m/s, réduite pour éviter les erreurs d'approximations, en accord avec la période de codage.
    # On réalise une sommation par pâquets, d'abord on somme sur chaque indice du nombre de réflexions :
    L=[ somme ( [creneaux(t, amplitude=ampli*(coef_de_ref**k), dephasage= retard_rayon_en_k_ref)/(4*np.pi*(retard_rayon_en_k_ref*c)) for retard_rayon_en_k_ref in liste_de_retards[k] ] ) for k in range(n) ]
    # Puis on somme les pâquets :
    S = somme(L)
    return S


def graphe2(S,A,grille,nombre_de_reflexions_max=15,periode=0.5,amplitude=1,coef_de_ref=0.3):
    L=[ afficher_resultat(S,A,grille,i) for i in range(nombre_de_reflexions_max+1)]  # L est la liste de ième terme les temps de parcours en i réflexions dans cette configuration
    t=np.linspace(0,20*periode_codage_ajustee,6000)  # Sur 1 milliseconde
    p=len(t)
    res=[]
    tracer_grille(grille)
    placer(S,'blue')
    placer(A,'red')
    # On calcule et trace les créneaux pour chaque nombre de réflexion ( aussi on stocke le résultat pour tracer la superposition ):
    for i in range(nombre_de_reflexions_max+1):
        res.append(calcul2(L[i],i,t,coef_de_ref))
    # On trace les créneaux au départ
    y= [ creneaux(t[i]) for i in range(p)]
    # On calcule la résultante
    n=len(res)
    S= [ somme( [res[i][k] for i in range(n)] ) for k in range(p)  ]
    plt.plot(t,S,label='Superposition')
    plt.legend()
    plt.xlabel('Temps, en 10^-3 s')
    plt.ylabel('Amplitude/éclairement du signal reçu')
    plt.title(('Réflexions pour une période T', periode_codage_ajustee*(10**-3)))
    plt.show()


def expo(t, dephasage=0,temps_carac=periode_codage_ajustee):
    if (t-dephasage)<=0: return 0
    else: return np.exp(-(t-dephasage)/temps_carac)
    
"""
Param :  t et L sont des listes, L contient les retards et T contient la liste des temps
"""
def calcul2(L,i,T,coef_de_ref=1):   

    n=len(L)
    c=3*(10**5)  # Célérité de la lumière en m/s, réduite pour éviter les erreurs d'approximations, en accord avec la période de codage.
    res=[ somme( [ creneaux(temps,dephasage=L[u])*(coef_de_ref**i)/(4*np.pi*c*L[u]) for u in range(n) ]) for temps in T ]
    
    if i==0:
        print(1)
        plt.plot(T,res,label=('créneaux en ',i,'  réflexions'))

    #     print(L)
    #     exp=[expo(t, dephasage=L[0],temps_carac=periode_codage_ajustee)/(4*np.pi*c*L[0]) for t in T]
    #     plt.plot(T,exp,label=('exponentielle de temps caractéristique la période du signal'))
    # plt.plot(T,res,label=('créneaux en ',i,'  réflexions'))
    return res


def placer(S,color):
    tu.up()
    tu.goto(S)
    tu.dot(None,color)
    
    
def tracer_grille(grille):
    x1,x2,y1,y2=grille
    taille=abs(x1-x2) + 300
    tu.setup(taille,taille)
    tu.up()
    tu.speed(5)
    tu.goto(x1,y1)
    tu.down()
    tu.goto(x1,y2)
    tu.goto(x2,y2)
    tu.goto(x2,y1)
    tu.goto(x1,y1)
    tu.speed(7)
    
    
def somme(args):
    S=0
    for i in args: S+=i
    return S


def creneaux(t,periode=periode_codage_ajustee,amplitude=1,dephasage=0):
    if ((t-dephasage)//periode)%2==1: return amplitude
    else : return 0


# def creneaux(t,periode=periode_codage_ajustee,amplitude=1,dephasage=0):
#     if (t-dephasage)<=periode and (t-dephasage)>=0 : return amplitude
#     else : return 0

## Simulation
graphe2(S,A,grille)
tu.exitonclick()

## Dénombrement
"""
Permet de réaliser 'nombre_de_test' fois le dénombrement du nombre de rayon allant de la source à l'emetteur en N reflexion, N étant variable de 1 à 4
"""
def test(nombre_de_tests):
    res=[]  # res contient le nombre de tests effectués pour k réflexions dans sa k ième coordonnée
    bool=True
    k=0
    for i in range(1,4+1):
        res.append(0)
        while res[i-1]<nombre_de_tests and bool:
            k+=1
            S,A=(((2*random()-1)*cote,(2*random()-1)*cote),((2*random()-1)*cote,(2*random()-1)*cote))
            L=multipath(S,A,grille,i)
            if len(L)==4*i: res[i-1]+=1
            else: 
                bool=False
    return res,k
    
print(test(100000))

