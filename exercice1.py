
def divEntier(x: int, y: int) -> int:
    if x<y:
        return 0
    else:
        x=x-y
        return divEntier(x,y)+1

def main():
    x=int(input("donné la valeur de x:"))

    y=int(input("donné la valeur de x:"))
    print(divEntier(x, y))

main()

#Ce code recursif vise à savoir combien de fois la valeur y est dans x.

#Ce code ne fonction pas avec des valeurs negative a cause du INT, pour
#laisser la possibilité d'utiliser les nombre negatif ou a virgule la valeur
#FLOAT aurais été necessaire

