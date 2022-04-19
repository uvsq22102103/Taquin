import tkinter as tk

######################
WIDTH, HEIGHT = 800, 800
BRICK = WIDTH/4
######################

root = tk.Tk()
root.title("Taquin")
canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="brown")
canvas.grid()

grillage = []
for x in range(4):
    for y in range(4):
        canvas.create_rectangle(x*BRICK+5,y*BRICK+5,x*BRICK+BRICK-5,y*BRICK+BRICK-5,fill="gray",tags="brick")

root.mainloop()