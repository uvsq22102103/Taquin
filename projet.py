import tkinter as tk
import random as rd

######################
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
######################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="brown")
canvas.grid()


nbr = []
for i in range(16):
    nbr.append(i+1)
print(nbr)
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
                                                font=('Helvetica', '60'))])

root.mainloop()
