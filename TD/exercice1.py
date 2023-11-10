
def divEntier(x: int, y: int) -> int:
    if x < y:
        return 0
    else:
        x = x-y
        return divEntier(x, y)+1

def main():
    try:
        x = int(input("donné la valeur de x:"))
        y = int(input("donné la valeur de y:"))
        if y == 0 or x < 0 or y < 0 or y == x:
            print("division par 0 impossible ou par un nombre negatif")
            return main()

    except ValueError:
        return print("x y doivent être des entiers"), main()
    else:
        print(divEntier(x, y))


main()

#Ce code recursif vise à savoir combien de fois la valeur y est dans x.

#Ce code ne fonction pas avec des valeurs negative a cause du INT, pour
#laisser la possibilité d'utiliser les nombre negatif ou a virgule la valeur
#FLOAT aurais été necessaire

#Le value error me permet de faire des teste a l'interieur de mon code et de specifié
#via un code erreur la raison précise car désigné du problème

