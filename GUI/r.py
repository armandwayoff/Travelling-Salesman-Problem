from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Combobox, Notebook
from algorithms import *
from classes import *

# Style constants
BG = "black"
BUT_BG = "grey"
FG = "white"

# Main window
root = Tk()
root.title("TSP Solver")
root.iconbitmap('icon.ico')
root.geometry("800x600")
root.minsize(800, 600)

# Tabs
tabs = Notebook(root)
tabs.pack(side=LEFT, fill=BOTH, expand=TRUE)

f1 = Frame(tabs)
f1.pack(side=LEFT, fill=BOTH, expand=TRUE)
first_plot = Plot(f1)
tabs.add(f1, text="Initialization path")

vertices = []


def new_random_data():
    def is_int(n):
        try:
            int(n)
            return True
        except ValueError:
            return False

    if is_int(spin.get()):
        number_vertices = int(spin.get())
        x = [uniform(0, 10) for _ in range(number_vertices)]
        y = [uniform(0, 10) for _ in range(number_vertices)]
        for i in range(number_vertices):
            vertices.append(Vertex(x[i], y[i]))
        display_scatter(first_plot, vertices)
    else:
        messagebox.showerror("Error", "Number of vertices is invalid")


def display_scatter(plt, population):
    plt.plot.clear()
    for vertex in population:
        plt.plot.plot(vertex.x, vertex.y, 'bo')
    plt.canvas.draw()


def display_graph(plt, population):
    plt.plot.clear()
    for i in range(len(population) - 1):
        plt.plot.plot([population[i].x, population[i + 1].x], [population[i].y, population[i + 1].y], 'b')
    for vertex in population:
        plt.plot.plot(vertex.x, vertex.y, 'bo')
    plt.canvas.draw()


def open_files():
    root.filename = filedialog.askopenfilename()
    max_length = 20
    if len(root.filename) > 0:
        button.config(text="Select new file")
        file_name = root.filename.split("/")[-1]
        if len(file_name) > max_length:
            file_name = "[...]" + file_name[-max_length:]
        label.config(text="Selected file : " + file_name)


def data_button():
    global spin
    spin = Spinbox(data_frame, from_=3, to=100, width=4)
    if data_mode.get() == "import-data":
        button.config(text="Select file")
        button.config(command=open_files)
        label.config(text="No selected file")
        spin.grid_remove()
    else:
        button.config(text="Generate random data")
        button.config(command=new_random_data)
        label.config(text="Number of vertices :")
        spin.grid(row=3, column=1, sticky=E)


def solve():
    global init_path
    if init_alg.get() == "Random":
        messagebox.askquestion("Validation", "Do you confirm the parameters ?")
        init_path = vertices
        display_graph(first_plot, init_path)
    elif init_alg.get() == "Nearest neighbour algorithm":
        messagebox.askquestion("Validation", "Do you confirm the parameters ?")
        init_path = nearest_neighbour(vertices, 0)
        display_graph(first_plot, init_path)
    else:
        messagebox.showerror("Error", "Parameters are not valid")
    f2 = Frame(tabs)
    f2.pack(side=LEFT, fill=BOTH, expand=TRUE)
    second_plot = Plot(f2)
    tabs.add(f2, text="Solution")
    tabs.select(f2)
    sol = two_opt(init_path, 10 ** 4)
    display_graph(second_plot, sol)


# User frame
user_frame = LabelFrame(root, width=300, height=800, bg=BG)
user_frame.pack(side=RIGHT, expand=0, fill=Y)

# Data frame
data_frame = LabelFrame(user_frame, text="Data", width=215, height=100, bg=BG, fg=FG)
data_frame.grid(row=0, column=0)
data_frame.grid_propagate(1)

# Radio buttons
data_mode = StringVar()
import_data_button = Radiobutton(data_frame, text="Import data", width=10, bg=BUT_BG, fg=FG, relief=GROOVE, variable=data_mode, value="import-data", command=data_button)
import_data_button.grid(row=1, column=0, sticky=NSEW)
new_random_plot_button = Radiobutton(data_frame, text="Random data", width=10, bg=BUT_BG, fg=FG, relief=GROOVE, variable=data_mode, value="random-data", command=data_button)
new_random_plot_button.grid(row=1, column=1, sticky=NSEW)
import_data_button.select()

button = Button(data_frame, text="Select file", bg=BUT_BG, fg=FG, relief=GROOVE, command=open_files)
button.grid(row=2, column=0, columnspan=2, sticky=W+E)
label = Label(data_frame, text="No selected file", bg=BG, fg=FG)
label.grid(row=3, column=0, columnspan=2)

# Initialization algorithms
parameters_frame = LabelFrame(user_frame, text="Parameters", bg=BG, fg=FG)
parameters_frame.grid(row=1, column=0)

init_alg_label = Label(parameters_frame, text="Initialization algorithm :", bg=BG, fg=FG)
init_alg_label.grid(row=3, column=0)
init_alg_lst = ["Random", "Nearest neighbour algorithm"]
init_alg = StringVar()
init_alg_combobox = Combobox(parameters_frame, values=init_alg_lst, textvariable=init_alg)
init_alg_combobox.current(0)
init_alg_combobox.grid(row=3, column=1)

# Solving algorithms
solving_alg_label = Label(parameters_frame, text="Solving algorithm :", bg=BG, fg=FG)
solving_alg_label.grid(row=4, column=0)
solving_alg_lst = ["2-opt", "Simulated annealing", "Brute-force search"]
solving_alg = StringVar()
solving_alg_combobox = Combobox(parameters_frame, values=solving_alg_lst, textvariable=solving_alg)
solving_alg_combobox.current(0)
solving_alg_combobox.grid(row=4, column=1)

# Solve button
solve_button = Button(user_frame, text="Solve", width=15, bg=BUT_BG, fg=FG, relief=GROOVE, command=solve)
solve_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
