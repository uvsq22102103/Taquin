import os
import time
import tkinter as tk
import random as rd
from copy import deepcopy
from tkinter.filedialog import asksaveasfilename


HEIGHT, WIDTH = 400, 400
ECART = HEIGHT/4
x, y = 0, 0
cpt = 0
cpt_2 = 0


def get_coord(nbr):
    for line in grille:
        try:
            return(grille.index(line),line.index(nbr))
        except:
            pass


def deplacer(event):
    #Partie 1er clique utilisateur
    global cpt, cpt_2
    clic = event.x, event.y
    try:
        obj = canvas.find_overlapping(clic[0],clic[1],clic[0],clic[1])[0]
        voisins = voisinage(grille, obj)
        if "X" in voisins:
            self_nbr = objs_grille[(obj,int(obj)+1)]
            coords = []
            for line in grille:
                try:
                    coords.append(("X",line.index("X"),grille.index(line)))
                except:
                    pass
                try:
                    coords.append((self_nbr,line.index(self_nbr),grille.index(line)))
                except:
                    pass
            cpt += 1
            xy = root.winfo_pointerxy()
            if abs(coords[0][1]-coords[1][1]) == 1: #horizontal
                while cpt % 2:
                    canvas.move(obj,root.winfo_pointerx()-xy[0],0)
                    canvas.move(int(obj)+1,root.winfo_pointerx()-xy[0],0)
                    xy = root.winfo_pointerxy()
                    canvas.update()
                    time.sleep(0.04)
            elif abs(coords[0][2]-coords[1][2]) == 1: #vertical
                while cpt % 2:
                    canvas.move(obj,0,root.winfo_pointery()-xy[1])
                    canvas.move(int(obj)+1,0,root.winfo_pointery()-xy[1])
                    xy = root.winfo_pointerxy()
                    canvas.update()
                    time.sleep(0.04) 
    except:
        print("Positionnement invalide")
        cpt -= 1
    #Partie 2nd clique utilisateur
    if not cpt % 2 and cpt != 0:
        coord_obj = canvas.coords(obj)
        coord_obj = ((coord_obj[2]+coord_obj[0])/2,(coord_obj[3]+coord_obj[1])/2)
        coord_obj_X = canvas.coords(grille_objs["X"][0])
        if coord_obj_X[0] <= coord_obj[0] <= coord_obj_X[2] and coord_obj_X[1] <= coord_obj[1] <= coord_obj_X[3]:
            cpt_2 += 1
        else:
            for line in grille:
                try:
                    i_nbr = [line.index(self_nbr),grille.index(line)]
                    canvas.moveto(obj,(i_nbr[0]*ECART)-1,(i_nbr[1]*ECART)-1)
                    canvas.moveto(int(obj)+1,(i_nbr[0]*ECART)+30,(i_nbr[1]*ECART)+10)
                except:
                    pass
    if cpt_2 == 2:
        cpt_2 = 0
        canvas.moveto(obj,coord_obj_X[0]-1,coord_obj_X[1]-1)
        canvas.moveto(int(obj)+1,coord_obj_X[0]+30,coord_obj_X[1]+10)
        for line in grille:
            try:
                canvas.moveto(grille_objs["X"][0],(line.index(self_nbr)*ECART)-1,(grille.index(line)*ECART)-1)
                canvas.moveto(grille_objs["X"][1],line.index(self_nbr)*ECART+30,grille.index(line)*ECART+10)
                i_nbr = [grille.index(line),line.index(self_nbr)]
            except:
                pass
            try:
                i_X = [grille.index(line),line.index("X")]
            except:
                pass
        grille[i_X[0]][i_X[1]], grille[i_nbr[0]][i_nbr[1]] = grille[i_nbr[0]][i_nbr[1]], grille[i_X[0]][i_X[1]]
        for i in grille:
            print(i)
        print("")
    check_win(grille,solution)


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


def voisinage(grille, obj):
    for j in range(4):
        try:
            i = (j,grille[j].index(objs_grille[(obj,int(obj)+1)]))
            break
        except:
            pass
    l_objs = []
    i_v = ((i[0]+1,i[1]),(i[0]-1,i[1]),(i[0],i[1]+1),(i[0],i[1]-1))
    for indice in i_v:
        if -1 not in indice:
            try:
                l_objs.append(grille[indice[0]][indice[1]])
            except:
                pass
    return l_objs


def clavier(event):
    v, a = [], []
    place_X = get_coord("X")
    for voisin in voisinage(grille,grille_objs["X"][0]):
        for line in grille:
            try:
                if line.index(voisin)-place_X[1] == 1:
                    action = "Left"
                elif line.index(voisin)-place_X[1] == -1:
                    action = "Right"
                elif grille.index(line)-place_X[0] == 1:
                    action = "Up"
                elif grille.index(line)-place_X[0] == -1:
                    action = "Down"
                a.append(action)
                v.append(voisin)
            except:
                pass
    try:
        objs_nbr = grille_objs[v[a.index(event.keysym)]]
        objs_X = grille_objs["X"]
        coords_nbr = canvas.coords(objs_nbr[0])[:2]
        coords_X = canvas.coords(objs_X[0])[:2]
        canvas.moveto(objs_nbr[0],coords_X[0]-1,coords_X[1]-1)
        canvas.moveto(objs_nbr[1],coords_X[0]+30,coords_X[1]+10)
        canvas.moveto(objs_X[0],coords_nbr[0]-1,coords_nbr[1]-1)
        canvas.moveto(objs_X[1],coords_nbr[0]+30,coords_nbr[1]+10)
        c_X = get_coord("X")
        c_nbr = get_coord(v[a.index(event.keysym)])
        grille[c_X[0]][c_X[1]], grille[c_nbr[0]][c_nbr[1]] = grille[c_nbr[0]][c_nbr[1]], grille[c_X[0]][c_X[1]]
    except:
        print("Commande mauvaise")
    check_win(grille,solution)


def check_win(grille,solution):
    if grille == solution:
        print("win")



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

grille_objs = {} #dictionnaire qui retourne les objs associés à un seul nbr
objs_grille = {} #dictionnaire qui fais exactement l'inverse
for line in grille:
    for nbr in line:
        if nbr != "X":
            grille_objs[nbr] = (
                canvas.create_rectangle(ECART*line.index(nbr),ECART*grille.index(line),
                (ECART*line.index(nbr))+ECART,(ECART*grille.index(line))+ECART,fill=rd_color()),
                canvas.create_text((ECART*line.index(nbr))+ECART/2,
                (ECART*grille.index(line))+ECART/2,text=nbr,font=('Helvetica', '60'))
            )
        else:
            grille_objs[nbr] = (
                canvas.create_rectangle(ECART*line.index(nbr),ECART*grille.index(line),
                (ECART*line.index(nbr))+ECART,(ECART*grille.index(line))+ECART,fill="black"),
                canvas.create_text((ECART*line.index(nbr))+ECART/2,
                (ECART*grille.index(line))+ECART/2,text=nbr,font=('Helvetica', '60'))
            )
for i in grille_objs.items():
    objs_grille[i[1]] = i[0]

canvas.bind("<1>",deplacer)
root.event_add("<<fleches>>","<Up>","<Down>","<Left>","<Right>")
root.bind("<<fleches>>",clavier)

root.mainloop()