# Author: Sanika Kamde / Lab 1

from tkinter import *
from backEnd import *

backend_obj = Backend()
backend_obj.build_SQLite_table()
backend_obj.insert('Temperature.html')


def sel():
    if var.get() == 1:
        selection = "You selected XY Plot"
        label.config(text=selection)
        backend_obj.build_xy_plot()
    elif var.get() == 2:
        selection = "You selected Bar Chart"
        label.config(text=selection)
        backend_obj.build_bar_chart()
    else:
        selection = "You selected Linear Regression"
        label.config(text=selection)
        backend_obj.build_linear_regression()


root = Tk()
root.geometry("300x200")
w = Label(root, text="Choose a graph to view:")
w.pack()
var = IntVar()

xy_plot = Radiobutton(root, text="XY Plot", variable=var, value=1, command=sel)
xy_plot.pack(anchor=W)

bar_chart = Radiobutton(root, text="Bar Chart", variable=var, value=2, command=sel)
bar_chart.pack(anchor=W)

linear_reg = Radiobutton(root, text="Linear Regression", variable=var, value=3, command=sel)
linear_reg.pack(anchor=W)

label = Label(root)
label.pack()

button = Button(root, text='Quit', command=root.destroy)
button.pack()

root.mainloop()
backend_obj.close_SQLite_table()
