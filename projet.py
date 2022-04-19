import tkinter as tk
import random as rd

########CONSTANTES#########
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
###########################
########FONCTIONS##########


def clic(event):
    global grillage
    x, y = event.x, event.y
    obj = canvas.find_closest(x, y)[0]
    if obj % 2:  # Carré cliqué
        ens = [obj, obj+1]  # Carré + Text ID
        print(grillage.index())
    else:  # Text cliqué
        ens = [obj, obj+1]  # Carré + Text ID
        print(grillage.index([obj-1, obj]))


###########################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="brown")
canvas.grid()


nbr = []
for i in range(16):
    nbr.append(i+1)
grillage = []
for x in range(4):
    for y in range(4):
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
            grillage.append([None])
print(grillage)
canvas.tag_bind("brick", "<Button-1>", clic)

root.mainloop()
