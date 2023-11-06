x=73
y=3
def divEntier(x: int, y: int) -> int:
    if x<y:
        return 0
    else:
        x=x-y
        return divEntier(x,y)+1

print(divEntier(x,y))

#Ce code vise à savoir quand x est inferieur a y et le +1
#fais office de compteur pour cette opération, il affiche
#le nombre d’itération nécessaire pour de résolution de la soustraction

#Ce code ne fonction pas avec des valeurs negative a cause du INT, pour
#laisser la possibilité d'utiliser les nombre negatif ou a virgule la valeur
#FLOAT aurais été necessaire

