import tkinter as tk
from tkinter import messagebox
from scrollableFrame import ScrollableFrame
from prepareGenerator import prepareGenerator

class PageMain:
    def __init__(self):
        self.root = tk.Tk()
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))
        self.root.title("Main Page")

        self.prepareGen = prepareGenerator()

        self.title = tk.Label(self.root, text="TSP Visualizer", font='SegoeUI 32 bold')
        self.title.pack(padx=400, pady=5)

        self.algorithmTitle = tk.Label(self.root, text="Algorithm:", font='SegoeUI 20 bold')
        self.algorithmTitle.place(x=20, y=100)

        options = ["Brute Force", "Dynamic Programming", "Branch and Bound"]
        self.clicked = tk.StringVar()
        self.clicked.set("Brute Force")
        self.dropdown = tk.OptionMenu(self.root, self.clicked, *options)
        self.dropdown.configure(font="SegoeUI 14", background='white')
        self.dropdown.place(x=20, y=150)
        menu = self.root.nametowidget(self.dropdown.menuname)
        menu.configure(font="SegoeUI 14")

        self.nodenum = tk.Label(self.root, text="Node amount:", font='SegoeUI 20 bold')
        self.nodenum.place(x=20, y=220)

        self.nodenumField = tk.Entry(self.root, background='white', foreground='black', font=('SegoeUI', 16), width=15)
        self.nodenumField.place(x=22, y=260)
        self.nodenumField.insert(0, '3')

        self.graphtitle = tk.Label(self.root, text="Graph:", font='SegoeUI 20 bold')
        self.graphtitle.place(x=20, y=320)

        self.var1 = tk.IntVar()
        self.R1 = tk.Radiobutton(self.root, text="Randomize", variable=self.var1, value=1)
        self.R1.select()
        self.R1.place(x=20, y=360)
        self.R1.configure(font='SegoeUI 16')
        self.R2 = tk.Radiobutton(self.root, text="Manual Input", variable=self.var1, value=2)
        self.R2.place(x=20, y=400)
        self.R2.configure(font='SegoeUI 16')

        self.nodecostTitle = tk.Label(self.root, text="Node Cost:", font='SegoeUI 20 bold')
        self.nodecostTitle.place(x=20, y=460)

        self.var2 = tk.IntVar()
        self.R3 = tk.Radiobutton(self.root, text="Randomize", variable=self.var2, value=1)
        self.R3.select()
        self.R3.place(x=20, y=500)
        self.R3.configure(font='SegoeUI 16')
        self.R4 = tk.Radiobutton(self.root, text="Manual Input", variable=self.var2, value=2)
        self.R4.place(x=20, y=540)
        self.R4.configure(font='SegoeUI 16')

        self.speedTitle = tk.Label(self.root, text="Speed:", font='SegoeUI 20 bold')
        self.speedTitle.place(x=20, y=600)

        options2 = ["Fast", "Moderate", "Slow"]
        self.clicked2 = tk.StringVar()
        self.clicked2.set("Moderate")
        self.dropdown2 = tk.OptionMenu(self.root, self.clicked2, *options2)
        self.dropdown2.configure(font="SegoeUI 14", background='white')
        self.dropdown2.place(x=20, y=640)
        menu2 = self.root.nametowidget(self.dropdown2.menuname)
        menu2.configure(font="SegoeUI 14")

        self.submitButton = tk.Button(self.root, text="Submit", command=self.submit)
        self.submitButton.place(x=20, y=720)
        self.submitButton.configure(font="SegoeUI 16 bold", background='gray', foreground='white')

        self.dictionary_window ={}
        self.graph_valid=False
        self.nodecost_valid=False

        self.root.mainloop()

    def submit(self):
        self.algo_chosen = self.clicked.get()
        self.speed_chosen = self.clicked2.get()
        self.node_amount = self.nodenumField.get()
        if not self.node_amount.isnumeric() or int(self.node_amount) == 0:
            messagebox.showwarning("Warning", "Node amount must be an integer larger than 0")
            return  # Stop further execution
        self.node_amount = int(self.node_amount)

        self.ans1 = [[None for _ in range(self.node_amount)] for _ in range(self.node_amount)]
        self.ans2 = [None] * self.node_amount

        self.graph = []
        graph_input_chosen = self.var1.get()
        self.graph_manual = False
        if graph_input_chosen == 2:
            self.graph_manual =True
            self.open_new_window(True)

        self.nodecost = []
        node_cost_chosen = self.var2.get()
        self.nodecost_manual=False
        if node_cost_chosen == 2:
            self.nodecost_manual=True
            self.open_new_window(False)
        
        if not self.graph_manual and not self.nodecost_manual: self.submit2()




    def open_new_window(self, graph_input_true):
        self.newWindow = tk.Toplevel(self.root)
        title = "Graph Manual Input" if graph_input_true else "Node Cost Manual Input"
        self.newWindow.title(title)
        self.newWindow.geometry("500x500")

        # Store the reference properly in dictionary_window
        window_key = "1" if graph_input_true else "2"
        self.dictionary_window[window_key] = self.newWindow

        if graph_input_true:
            self.add_rows_new_window((self.node_amount * 2 - self.node_amount), graph_input_true)
        else:
            self.add_rows_new_window(self.node_amount, graph_input_true)

        



    def add_rows_new_window(self, grid_amount, graph_input):
        if graph_input:
            self.scrollable_frame1 = ScrollableFrame(self.dictionary_window["1"])
            self.scrollable_frame1.pack(fill="both", expand=True)
            self.okbutton = tk.Button(self.newWindow, text="OK", command=self.ok1_button_click)
            self.okbutton.pack(padx=200, pady=30)
            self.okbutton.configure(font="SegoeUI 14 bold", background='gray', foreground='white')

            num_row = 0
            for i in range(self.node_amount):
                for j in range(i + 1, self.node_amount):
                    label = tk.Label(self.scrollable_frame1.scrollable_frame, text=f"Node {i} to {j}")
                    entry = tk.Entry(self.scrollable_frame1.scrollable_frame)
                    label.configure(font='SegoeUI 12')
                    entry.configure(font='SegoeUI 12')
                    label.grid(row=num_row, column=0, padx=10, pady=5)
                    entry.grid(row=num_row, column=1, padx=10, pady=5)
                    self.ans1[i][j] = entry
                    self.ans1[j][i] = entry
                    num_row += 1


        else:
            self.scrollable_frame2 = ScrollableFrame(self.dictionary_window["2"])
            self.scrollable_frame2.pack(fill="both", expand=True)
            self.okbutton = tk.Button(self.newWindow, text="OK", command=self.ok2_button_click)
            self.okbutton.pack(padx=200, pady=30)
            self.okbutton.configure(font="SegoeUI 14 bold", background='gray', foreground='white')
            for i in range(grid_amount):
                label = tk.Label(self.scrollable_frame2.scrollable_frame, text=f"Node {i}")
                entry = tk.Entry(self.scrollable_frame2.scrollable_frame)
                label.configure(font='SegoeUI 12')
                entry.configure(font='SegoeUI 12')
                if i == 0:
                    entry.insert(0, '0')
                    entry.configure(state="readonly")
                label.grid(row=i, column=0, padx=10, pady=5)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.ans2[i] = entry


    def ok1_button_click(self):
        print("ok1 clicked")
        try:
            # Initialize the graph matrix
            self.graph = [[0] * self.node_amount for _ in range(self.node_amount)]

            # Loop through only the upper triangle of the matrix (i < j)
            for i in range(self.node_amount):
                for j in range(i + 1, self.node_amount):
                    entry = self.ans1[i][j]

                    if entry is None:  # Skip uninitialized entries
                        continue

                    value = entry.get().strip()  # Get and strip the input value
                    print(f"value: {value}")

                    if not value:  # Check if input is empty
                        raise ValueError(f"Weight for edge {i}-{j} cannot be empty.")

                    # Try to convert the input to a float
                    try:
                        weight = float(value)
                    except ValueError:
                        raise ValueError(f"Weight for edge {i}-{j} must be a valid number.")

                    # Store the weight in both (i, j) and (j, i) directions
                    self.graph[i][j] = weight
                    self.graph[j][i] = weight

            # If all inputs are valid, mark as valid and close the window
            self.graph_valid = True
            messagebox.showinfo("Success", "Graph input stored successfully!")
            self.dictionary_window["1"].destroy()  # Close the graph input window
            del self.dictionary_window["1"]  # Remove the reference

            if "2" in self.dictionary_window:
                self.dictionary_window["2"].focus_force()

            self.check_and_submit()  # Check if both inputs are valid

        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
            self.graph_valid = False  # Mark as invalid if validation fails



    def ok2_button_click(self):
        try:
            # Validate and store node cost input
            self.nodecost = [0] * self.node_amount
            for i in range(1, self.node_amount):
                value = self.ans2[i].get().strip()
                if not value:
                    raise ValueError("Node cost cannot be empty.")

                self.nodecost[i] = float(value)

            # If validation passes, mark node cost as valid
            self.nodecost_valid = True
            messagebox.showinfo("Success", "Node cost input stored successfully!")
            self.dictionary_window["2"].destroy()  # Close the node cost window
            del self.dictionary_window["2"]  # Ensure the reference is removed
            if "1" in self.dictionary_window:
                self.dictionary_window["1"].focus_force()

            self.check_and_submit()  # Check if both windows are valid

        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
            self.nodecost_valid = False  # Mark as invalid if exception occurs


    def check_and_submit(self):
        if self.graph_valid: 
            self.prepareGen.set_graph(self.graph)
        
        if self.nodecost_valid:
            self.prepareGen.set_nodecost(self.nodecost)

        """Check if both graph and node cost inputs are valid, then proceed."""
        if self.graph_manual and not self.graph_valid:
            return  # Don't proceed if graph input is required but invalid

        if self.nodecost_manual and not self.nodecost_valid:
            return  # Don't proceed if node cost input is required but invalid

        # If both are valid, proceed to submission
        self.submit2()



    def submit2(self):
        # print(self.nodecost)
        # print(self.graph)
        # print(self.algo_chosen)
        # print(self.speed_chosen)
        # print(self.node_amount)
        # print(self.graph_manual)
        # print(self.nodecost_manual)
        self.prepareGen.printing()


        


PageMain()
