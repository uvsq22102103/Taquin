import tkinter as tk
import random as rd

########CONSTANTES#########
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
win = False
###########################
########FONCTIONS##########


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
                for i in range(len(grillage)):
                    if grillage[i] == ens:
                        grillage[i] = None
                        break
                grillage[move] = ens
                moving(ens, move)
        check_win()


def keypress(event, key):
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
        elif key == "Left":
            p = index+1
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
        elif key == "Up":
            p = index+4
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
        elif key == "Down":
            p = index-4
            if p in p_move:
                grillage[index] = grillage[p]
                grillage[p] = None
                moving(grillage[index], index)
        check_win()


def key_r(event):
    keypress(event, "Right")


def key_l(event):
    keypress(event, "Left")


def key_u(event):
    keypress(event, "Up")


def key_d(event):
    keypress(event, "Down")


def show_win_condition(event):
    print(win_condition)


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


###########################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="brown")
canvas.grid()


nbr = []
for i in range(16):
    nbr.append(i+1)
grillage = []
win_condition = {}
for y in range(4):
    for x in range(4):
        tirage = rd.choice(nbr)
        del nbr[nbr.index(tirage)]
        if tirage != 16:
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
            grillage.append(None)
            win_condition[tirage] = None
check_win()

canvas.tag_bind("brick", "<Button-1>", clic)
root.bind_all("<KeyPress-Left>", key_l)
root.bind_all("<KeyPress-Right>", key_r)
root.bind_all("<KeyPress-Up>", key_u)
root.bind_all("<KeyPress-Down>", key_d)
root.bind_all("<KeyPress-space>", show_win_condition)

root.mainloop()
