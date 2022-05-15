from copy import deepcopy
import random as rd
import tkinter as tk


HEIGHT, WIDTH = 400, 400
ECART = HEIGHT/4


def rd_color():
    r, g, b = hex(rd.randint(30, 255))[2::], hex(rd.randint(30, 255))[2::], hex(rd.randint(30, 255))[2::]
    if len(r) == 1:
        r = "0" + r
    if len(g) == 1:
        g = "0" + g
    if len(b) == 1:
        b = "0" + b
    return ("#"+r+g+b)


def melange(solution: list):
    solution = solution[0] + solution[1] + solution[2] + solution[3]
    del solution[-1]
    mixe = deepcopy(solution)
    rd.shuffle(mixe)
    mixe = [mixe[:4], mixe[4:8], mixe[8:12], mixe[12:]+["X"]]
    return mixe


def resolvable(mixe: list, solution: list):
    solution = solution[0] + solution[1] + solution[2] + solution[3]
    mixe = mixe[0] + mixe[1] + mixe[2] + mixe[3]
    cpt = 0
    for i in range(15):
        if solution[i] != mixe[i]:
            mixe[mixe.index(solution[i])] = mixe[i]
            mixe[i] = solution[i]
            cpt += 1
    if cpt % 2 == 0:
        return True
    else:
        return False


def clic(event):
    print(event)


def voisinage(grille, indice, number):
    pass


######### Corps d'éxécution #########

solution = list()
for i in range(4):
    solution.append([])
    for j in range(4):
        solution[i].append(hex(i*4+j+1)[2:])
solution[-1][-1] = "X"

grille = melange(solution)
while not resolvable(grille,solution):
    grille = melange(solution)

root = tk.Tk()
root.title("Le Taquin taquine ?")

canvas = tk.Canvas(root, height=HEIGHT, width= WIDTH, bg="black")
canvas.grid()

grille_objs = []
for line in grille:
    grille_objs.append([])
    for nbr in line:
        grille_objs[grille.index(line)].append((
            canvas.create_rectangle(ECART*line.index(nbr),ECART*grille.index(line),
            (ECART*line.index(nbr))+ECART,(ECART*grille.index(line))+ECART,fill=rd_color()),
            canvas.create_text((ECART*line.index(nbr))+ECART/2,
            (ECART*grille.index(line))+ECART/2,text=nbr,font=('Helvetica', '60'),fill="white")
        ))

canvas.itemconfigure(grille_objs[3][3][0],state='hidden')
canvas.itemconfigure(grille_objs[3][3][1],state='hidden')



root.mainloop()
