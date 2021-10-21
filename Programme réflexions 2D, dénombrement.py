import turtle as tu
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from random import random




    
# Caractéristiques de la simulation :
cote=300
grille=(-cote,cote,cote,-cote)
# Générations de 2 positions aléatoires
S,A=(((2*random()-1)*cote,(2*random()-1)*cote),((2*random()-1)*cote,(2*random()-1)*cote))
print(S,A)


periode_codage_ajustee=1*(10**-6 )                                  # frequence du signal: 10^ Hz, pour c= 3.10^-5 !! il y a 10^3 d'écart !




def reflexions_possibles(S,grille): # Cette fonction renvoie les réflexions possibles(!) de S sur la grille sous la forme de couples (point,(orientation,position_du_plan_de_réflexion))

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
                            # et on rajoute la distance entre S et I2 en plus de celle entre I et I2
                            res.append([I2,distance(I[0],I2)+I[1]+distance(S,I2)])
                            
                        else :                                                  # Le point S n'est pas le véritable point source mais une source fictive, on ajoute seulement la distance I,I2
                            res.append([I2,distance(I[0],I2)+I[1]])
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
        return (xintersection,yintersection)
    
    return(xs,pos_ref) # Dans ce cas pos_ref est l'ordonnée du plan de réflexion, lieu où se situe l'intersection
        


def afficher_resultat(S,A,grille,nombre_de_reflexions=3):
    L=multipath(S,A,grille,nombre_de_reflexions)
    # On renvoie la liste des retards en secondes, en considérant que la distance est en pixel, donc 1 unité = 0.26 mm=2.6*10^-4 m
    c=3*(10**5) # Célérité de la lumière en m/s, réduite pour éviter les erreurs d'approximations, en accord avec la période de codage.
    n=len(L)
    R=[L[k][1]*2.6*(10**-4)/c for k in range(n)]
    
    return R

def graphe(S,A,grille,nombre_de_reflexions_max=3,periode=0.5,amplitude=1,coef_de_ref=0.5):
    t=np.linspace(0,10*periode_codage_ajustee,1000)                                                 # Sur 1 milliseconde
    p=len(t)
    L=[ afficher_resultat(S,A,grille,i) for i in range(nombre_de_reflexions_max+1)]     # L est la liste de ième terme les temps de parcours en i réflexions dans cette configuration
    y2=[ calcul(L,t[k],coef_de_ref,amplitude) for k in range(p)]                        # y2 est une liste, de même taille que t, qui contient à chaque instant t[k] la superposition de tous ces créneaux
    y= [ creneaux(t[i]) for i in range(p)]
    plt.plot(t,y,label='sans réflexion')
    plt.plot(t,y2,label='avec')

    plt.show()

def calcul(liste_de_retards,t,coef_de_ref,ampli,test=None):
    n=len(liste_de_retards)                                                     # n est le nb de réflexions maximal -1
    # On réalise une sommation par pâquets, d'abord on somme sur chaque indice du nombre de réflexions :
    L=[ somme ( [creneaux(t, amplitude=ampli*(coef_de_ref**k), dephasage= retard_rayon_en_k_ref) for retard_rayon_en_k_ref in liste_de_retards[k] ] ) for k in range(n) ]
    # Puis on somme les pâquets :
    S = somme(L)
    return S

def graphe2(S,A,grille,nombre_de_reflexions_max=2,periode=0.5,amplitude=1,coef_de_ref=0.5):
    t=np.linspace(0,10*periode_codage_ajustee,3000)                                                 # Sur 1 milliseconde
    p=len(t)
    res=[]
    L=[ afficher_resultat(S,A,grille,i) for i in range(nombre_de_reflexions_max+1)]     # L est la liste de ième terme les temps de parcours en i réflexions dans cette configuration
    # On calcule et trace les créneaux pour chaque nombre de réflexion ( aussi on stocke le résultat pour tracer la superposition ):
    for i in range(nombre_de_reflexions_max+1):
        res.append(calcul2(L[i],i,t,coef_de_ref))
    # On trace les créneaux en LOS
    y= [ creneaux(t[i]) for i in range(p)]
    plt.plot(t,y,label=('sans réflexion, T=',(periode_codage_ajustee*10**-3)))
    # On calcule la résultante
    n=len(res)
    S= [ somme( [res[i][k] for i in range(n)] ) for k in range(p)  ]
    l=len(S)
    R= [ S[i]**2 for i in range(l) ]
    # plt.plot(t,S,label='Superposition')
    # plt.plot(t,S,label='Eclairement')
    plt.legend()
    plt.xlabel('Temps, en 10^-3 s')
    plt.ylabel('Amplitude/éclairement du signal reçu')
    plt.title(' Réflexions ')
    plt.show()

def calcul2(L,i,t,coef_de_ref=1):
    n=len(L)
    res=[ somme( [ creneaux(temps,dephasage=L[u])*(coef_de_ref**i) for u in range(n) ]) for temps in t ]
    plt.plot(t,res,label=('créneaux en ',i,'  réflexions'))
    return res
    
    
    
def somme(args):
    S=0
    for i in args: S+=i
    return S


def creneaux(t,periode=periode_codage_ajustee,amplitude=1,dephasage=0):
    if ((t-dephasage)//periode)%2==1: return amplitude
    else : return 0

    
def test(nombre_de_tests):
    res=[] # res contient le nombre de tests effectués pour k réflexions dans sa k ième coordonnée
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


# graphe(S,A,grille)

#Pour n=10, 

#([6307.138812488593, 5522.68050859363, 5544.366510251645, 5178.802950489622, 5316.013544000805, 4623.851208678757, 4743.416490252568, 5707.889277132134, 5323.532661682466, 5346.026561849464, 4589.117562233507, 4743.41649025257, 4438.46820423443, 4518.849411078003, 3911.5214431215895, 4244.997055358225, 3911.521443121589, 4263.8011210655695, 4101.219330881975, 4429.44691807002, 4438.468204234429, 4701.063709417263, 4429.446918070021, 4384.062043356595, 4263.801121065569, 4623.851208678757, 4589.117562233507, 4701.0637094172625, 5522.680508593631, 4743.416490252569, 5544.366510251644, 5707.889277132134, 4244.997055358224, 4743.41649025257, 5178.802950489621, 4518.849411078001, 5323.532661682466, 5316.013544000806, 5346.026561849464, 6307.138812488593], 40)
        
        
        
        
        
        
        
        
        
        
        
        
        