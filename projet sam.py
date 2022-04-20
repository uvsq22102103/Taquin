 # https://github.com/uvsq22102103/taquin



import tkinter as tk
import random as rd

from matplotlib.font_manager import _Weight

######################
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH / 4
######################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="darkblue")
canvas.grid()

grillage = []
matrice = []




tirage_aleatoire = [i for i in range(1,17)]
print(tirage_aleatoire)
nrb = rd.randint(tirage_aleatoire)


    





liste_taquin = []

for x in range(4)  :
    liste_taquin.append([])
    for y in range(4) :

        
        canvas.create_rectangle( x * BRICK + 5, y * BRICK + 5, x * BRICK + BRICK - 5, y * BRICK + BRICK - 5, fill= "gray", tags="brick")
        
        canvas.create_text(x *BRICK +BRICK //2 +5 , y * BRICK +BRICK//2 -5 , text = tirage_aleatoire, fill = "black", font = ("helvetica","50"))
    

        







        













root.mainloop()