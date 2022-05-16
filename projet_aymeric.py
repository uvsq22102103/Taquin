import tkinter as tk
import random as rd
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import copy


########CONSTANTES ET VARIABLES#########
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
########################################
########FONCTIONS##########


def start_game(save=False):
    global grillage, win_condition, win, undo_liste
    win = False
    canvas.delete("all")
    grillage = []
    win_condition = {}
    if not save:
        undo_liste = []
        nbr = []
        for i in range(15):
            nbr.append(i+1)
        for y in range(4):
            for x in range(4):
                if y == 3 and x == 3:
                    grillage.append(None)
                    win_condition[16] = None
                else:
                    tirage = rd.choice(nbr)
                    del nbr[nbr.index(tirage)]
                    grillage.append([canvas.create_rectangle(x*BRICK+5,
                                                             y*BRICK+5,
                                                             x*BRICK+BRICK-5,
                                                             y*BRICK+BRICK-5,
                                                             fill="gray",
                                                             tags="brick"),
                                    canvas.create_text(x*BRICK+BRICK/2,
                                                       y*BRICK+BRICK/2,
                                                       text=tirage,
                                                       font=('Helvetica', '60'),
                                                       tags="brick")])
                    win_condition[tirage] = grillage[-1]
    else:
        dic_cache = {}
        for c in save:
            num, loc = c
            dic_cache[loc] = num
        for y in range(4):
            for x in range(4):
                if dic_cache[y*4+x+1] != 16:
                    grillage.append([canvas.create_rectangle(x*BRICK+5,
                                                             y*BRICK+5,
                                                             x*BRICK+BRICK-5,
                                                             y*BRICK+BRICK-5,
                                                             fill="gray",
                                                             tags="brick"),
                                    canvas.create_text(x*BRICK+BRICK/2,
                                                       y*BRICK+BRICK/2,
                                                       text=dic_cache[y*4+x+1],
                                                       font=('Helvetica', '60'),
                                                       tags="brick")])
                else:
                    grillage.append(None)
                win_condition[dic_cache[y*4+x+1]] = grillage[-1]
    check_win()
    button_start.config(text="Reroll")


def voisinage(index: int):
    if index in [0, 1, 2, 5, 6, 9, 10, 13, 14, 15]:
        p_move = [index-4, index+4, index-1, index+1]
    elif index in [4, 8, 12]:
        p_move = [index-4, index+4, index+1]
    elif index in [3, 7, 11]:
        p_move = [index-4, index+4, index-1]
    cpt = 0
    for i in range(len(p_move)):
        i -= cpt
        if not 0 <= p_move[i] <= 15:
            del p_move[i]
            cpt += 1
    return(p_move)


def moving(ens, move):
    canvas.moveto(ens[0], (move % 4)*BRICK+5, (move//4)*BRICK+5)
    canvas.moveto(ens[1], (move % 4)*BRICK+50, (move//4)*BRICK+50)


def clic(event):
    if not win:
        global grillage
        x, y = event.x, event.y
        obj = canvas.find_closest(x, y)[0]
        if obj % 2:  # Carré cliqué
            ens = [obj, obj+1]  # Carré + Text ID
            p_move = voisinage(grillage.index(ens))
        else:  # Text cliqué
            ens = [obj-1, obj]  # Carré + Text ID
            p_move = voisinage(grillage.index(ens))
        for move in p_move:
            if grillage[move] is None:
                if move-grillage.index(ens) == 1:
                    undo_liste.append("Left")
                elif move-grillage.index(ens) == -1:
                    undo_liste.append("Right")
                elif move-grillage.index(ens) == 4:
                    undo_liste.append("Up")
                elif move-grillage.index(ens) == -4:
                    undo_liste.append("Down")
                grillage[grillage.index(ens)] = None
                grillage[move] = ens
                moving(ens, move)
        check_win()


def keypress(event, key, undo=False):
    if not win:
        global grillage
        index = grillage.index(None)
        p_move = voisinage(index)
        if key == "Right":
            p = index-1
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
                if not undo:
                    undo_liste.append("Left")
                else:
                    del undo_liste[-1]
        elif key == "Left":
            p = index+1
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
                if not undo:
                    undo_liste.append("Right")
                else:
                    del undo_liste[-1]
        elif key == "Up":
            p = index+4
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
                if not undo:
                    undo_liste.append("Down")
                else:
                    del undo_liste[-1]
        elif key == "Down":
            p = index-4
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
                if not undo:
                    undo_liste.append("Up")
                else:
                    del undo_liste[-1]
        check_win()


def key_r(event):
    keypress(event, "Right")


def key_l(event):
    keypress(event, "Left")


def key_u(event):
    keypress(event, "Up")


def key_d(event):
    keypress(event, "Down")


def key_dd(event):
    keypress(event, "Down")
    keypress(event, "Down")


def key_ud(event):
    keypress(event, "Up")
    keypress(event, "Up")


def key_ld(event):
    keypress(event, "Left")
    keypress(event, "Left")


def key_rd(event):
    keypress(event, "Right")
    keypress(event, "Right")


def check_win():
    global win
    cpt = 0
    for i in range(len(grillage)):
        if grillage[i] == win_condition[i+1]:
            if grillage[i] is not None:
                canvas.itemconfig(grillage[i][0], fill='green')
            cpt += 1
        else:
            if grillage[i] is not None:
                canvas.itemconfig(grillage[i][0], fill='gray')
    if cpt == 16:
        print("Bravo tu as gagné !")
        win = True
    elif cpt == 15:
        print("Ce Taquin n'a pas de solution !")
        win = True


def save_party():
    save_dir = asksaveasfilename(initialdir=os.getcwd(),
                                 initialfile="save.taquin")
    print(save_dir[-7::])
    if save_dir[-7::] == ".taquin":
        print("Directory : ", save_dir)
        fichier = open(file=save_dir, mode="w")
        output = ""
        for i in range(16):
            output += str(i+1)+":"+str(grillage.index(win_condition[i+1])+1)+" "
        output += "\n" + " ".join(undo_liste)
        fichier.write(output)
        fichier.close()
    elif save_dir == "":
        print("You skip the save")
    else:
        print("Wrong one")
        save_party()
        


def load_party():
    global undo_liste
    load_dir = askopenfilename(initialdir=os.getcwd())
    fichier = open(file=load_dir, mode="r")
    texte = fichier.readline().split()
    undo_liste = fichier.readlines(1)[0].split()
    fichier.close()
    output = []
    for coords in texte:
        sep = coords.index(":")
        output.append([int(coords[:sep]), int(coords[sep+1:])])
    start_game(output)


def undo():
    if len(undo_liste) != 0:
        keypress(None, undo_liste[-1], True)


def dist_manhattan(nbr: int = 0, liste=False):
    """Fonction qui calcule la distance du nbr en entrée sur la grille entre son
    placement au temps t et sa place définitive"""
    if nbr != 0:
        if liste:
            p = liste.index(win_condition[nbr])
        else:
            p = grillage.index(win_condition[nbr])
        px, py = p % 4, p // 4
        x, y = (nbr-1) % 4, (nbr-1) // 4
        return abs(x-px)+abs(y-py)
    else:
        dico = {}
        for i in range(15):
            dico[i+1] = dist_manhattan(i+1,liste)
        return dico


def taquin_possible():
    pass


def ia_taquin():
    """IA basée sur de l'information heuristique"""
    grille = copy.deepcopy(grillage)
    print(grille)
    pass
###########################


root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="brown")
button_start = tk.Button(root, text="Start", command=start_game)
button_save = tk.Button(root, text="Save", command=save_party)
button_load = tk.Button(root, text="Load", command=load_party)
button_undo = tk.Button(root, text="Undo", command=undo)
button_ia = tk.Button(root, text="IA", command=ia_taquin)
label = tk.Label(root, text="Bonne chance")
canvas.grid(row=0, rowspan=5, column=0)
button_start.grid(row=0, column=1)
button_save.grid(row=1, column=1)
button_load.grid(row=2, column=1)
button_undo.grid(row=3, column=1)
button_ia.grid(row=4, column=1)
label.grid(row=5, column=0, columnspan=1)

canvas.tag_bind("brick", "<Button-1>", clic)
root.bind_all("<KeyPress-Left>", key_l)
root.bind_all("<Double-KeyPress-Left>", key_ld)
root.bind_all("<KeyPress-Right>", key_r)
root.bind_all("<Double-KeyPress-Right>", key_rd)
root.bind_all("<KeyPress-Up>", key_u)
root.bind_all("<Double-KeyPress-Up>", key_ud)
root.bind_all("<KeyPress-Down>", key_d)
root.bind_all("<Double-KeyPress-Down>", key_dd)

root.mainloop()
