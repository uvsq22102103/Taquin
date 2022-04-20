import tkinter as tk
import random as rd

########CONSTANTES#########
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
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


def clic(event):
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
            
            canvas.moveto(ens[0], (move % 4)*BRICK+5, (move//4)*BRICK+5)
            canvas.moveto(ens[1], (move % 4)*BRICK+50, (move//4)*BRICK+50)


###########################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="brown")
canvas.grid()


nbr = []
for i in range(16):
    nbr.append(i+1)
grillage = []
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
        else:
            grillage.append(None)
print(grillage)

canvas.tag_bind("brick", "<Button-1>", clic)

root.mainloop()
