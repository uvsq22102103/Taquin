import random as rd

solution = []
for i in range(0,16):
    if i // 4 == 0:
        solution.append([])
    if i == 15:
        solution[i // 4].append("X")
    else:
        solution[i // 4].append(hex(i+1)[2:])


def start():
    choix = list(range(1, 16))
    for i in range(len(choix)):
        choix[i] = hex(choix[i])[2::]
    grille = []
    for i in range(4):
        grille.append([])
        for j in range(4):
            if i == 3 and j == 3:
                grille[i].append("X")
            else:
                c = rd.choice(choix)
                grille[i].append(c)
                del choix[choix.index(c)]
    return grille


def d_manhattan(grille,solution):
    output = []
    for i in solution:
        dg, ds = grille.index(i), solution.index(i)
        dgx, dgy = dg % 4, dg // 4
        dsx, dsy = ds % 4, ds // 4
        output.append([i,abs(dsx-dgx)+abs(dsy-dgy)])
    return output



def ia_astar(grille: list,solution: list):
    # Def variables utiles
    grille = grille[0] + grille[1] + grille[2] + grille[3]
    solution = solution[0] + solution[1] + solution[2] + solution[3]
    ######################
    d_vol = d_manhattan(grille,solution)
    print(d_vol)
    ######################

    ######################


grille = start()
for line in grille:
    print(line)
ia_astar(grille, solution)