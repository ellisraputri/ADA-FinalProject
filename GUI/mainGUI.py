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

        self.summaryTitle = tk.Label(self.root, text="Summary", font='SegoeUI 20 bold')
        self.summaryTitle.place(x=800, y=100)

        self.outputTitle = tk.Label(self.root, text="Output", font='SegoeUI 20 bold')
        self.outputTitle.place(x=800, y=460)

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
        self.R2.place(x=170, y=360)
        self.R2.configure(font='SegoeUI 16')

        self.nodecostTitle = tk.Label(self.root, text="Node Cost:", font='SegoeUI 20 bold')
        self.nodecostTitle.place(x=20, y=420)

        self.var2 = tk.IntVar()
        self.R3 = tk.Radiobutton(self.root, text="Randomize", variable=self.var2, value=1)
        self.R3.select()
        self.R3.place(x=20, y=460)
        self.R3.configure(font='SegoeUI 16')
        self.R4 = tk.Radiobutton(self.root, text="Manual Input", variable=self.var2, value=2)
        self.R4.place(x=170, y=460)
        self.R4.configure(font='SegoeUI 16')

        self.speedTitle = tk.Label(self.root, text="Speed:", font='SegoeUI 20 bold')
        self.speedTitle.place(x=20, y=620)

        options2 = ["Fast", "Moderate", "Slow"]
        self.clicked2 = tk.StringVar()
        self.clicked2.set("Moderate")
        self.dropdown2 = tk.OptionMenu(self.root, self.clicked2, *options2)
        self.dropdown2.configure(font="SegoeUI 14", background='white')
        self.dropdown2.place(x=20, y=660)
        menu2 = self.root.nametowidget(self.dropdown2.menuname)
        menu2.configure(font="SegoeUI 14")

        self.submitButton = tk.Button(self.root, text="Submit", command=self.submit)
        self.submitButton.place(x=20, y=740)
        self.submitButton.configure(font="SegoeUI 16 bold", background='gray', foreground='white')

        self.congestionTitle = tk.Label(self.root, text="Congestion:", font='SegoeUI 20 bold')
        self.congestionTitle.place(x=20, y=520)
        self.var3 = tk.IntVar()
        self.R5 = tk.Radiobutton(self.root, text="Randomize", variable=self.var3, value=1)
        self.R5.select()
        self.R5.place(x=20, y=560)
        self.R5.configure(font='SegoeUI 16')
        self.R6 = tk.Radiobutton(self.root, text="Manual Input", variable=self.var3, value=2)
        self.R6.place(x=170, y=560)
        self.R6.configure(font='SegoeUI 16')

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
            return  
        self.node_amount = int(self.node_amount)

        self.ans1 = [[None for _ in range(self.node_amount)] for _ in range(self.node_amount)]
        self.ans2 = [None] * self.node_amount
        self.ans3 = [[None for _ in range(self.node_amount)] for _ in range(self.node_amount)]

        self.graph = []
        graph_input_chosen = self.var1.get()
        self.graph_manual = False
        if graph_input_chosen == 2:
            self.graph_manual =True
            self.open_new_window('1')

        self.nodecost = []
        node_cost_chosen = self.var2.get()
        self.nodecost_manual=False
        if node_cost_chosen == 2:
            self.nodecost_manual=True
            self.open_new_window('2')
        
        self.congestion=[]
        congestion_input_chosen = self.var3.get()
        self.congestion_manual = False
        if congestion_input_chosen == 2:
            self.congestion_manual =True
            self.open_new_window('3')
        
        if not self.graph_manual and not self.nodecost_manual and not self.congestion_manual: 
            self.submit2()




    def open_new_window(self, graph_input_true):
        self.newWindow = tk.Toplevel(self.root)
        if graph_input_true=='1': title = "Graph Manual Input"
        elif graph_input_true=='2': title="Node Cost Manual Input"
        else: title="Congestion Manual Input"
        self.newWindow.title(title)
        self.newWindow.geometry("500x500")

        self.dictionary_window[graph_input_true] = self.newWindow

        if graph_input_true=="1":
            self.add_rows_new_window((self.node_amount * 2 - self.node_amount), graph_input_true)
        elif graph_input_true=="2" :
            self.add_rows_new_window(self.node_amount, graph_input_true)
        else: 
            self.add_rows_new_window((self.node_amount * 2 - self.node_amount), graph_input_true)



    def add_rows_new_window(self, grid_amount, graph_input):
        if graph_input=="1":
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


        elif graph_input=="2":
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
        
        else:
            self.scrollable_frame3 = ScrollableFrame(self.dictionary_window["3"])
            self.scrollable_frame3.pack(fill="both", expand=True)
            self.okbutton = tk.Button(self.newWindow, text="OK", command=self.ok3_button_click)
            self.okbutton.pack(padx=200, pady=30)
            self.okbutton.configure(font="SegoeUI 14 bold", background='gray', foreground='white')

            headers = ["Node", "Start Time", "End Time", "Congestion"]
            for col, header in enumerate(headers):
                header_label = tk.Label(self.scrollable_frame3.scrollable_frame, text=header, font='SegoeUI 14 bold')
                header_label.grid(row=0, column=col, padx=10, pady=5)

            num_row = 1  

            for i in range(self.node_amount):
                for j in range(self.node_amount):
                    if(i==j): continue
                    label = tk.Label(self.scrollable_frame3.scrollable_frame, text=f"{i} to {j}", font='SegoeUI 12')
                    label.grid(row=num_row, column=0, padx=10, pady=5)

                    start_entry = tk.Entry(self.scrollable_frame3.scrollable_frame, font='SegoeUI 12', width=10)
                    end_entry = tk.Entry(self.scrollable_frame3.scrollable_frame, font='SegoeUI 12', width=10)
                    percent_entry = tk.Entry(self.scrollable_frame3.scrollable_frame, font='SegoeUI 12', width=10)

                    start_entry.grid(row=num_row, column=1, padx=10, pady=5)
                    end_entry.grid(row=num_row, column=2, padx=10, pady=5)
                    percent_entry.grid(row=num_row, column=3, padx=10, pady=5)

                    self.ans3[i][j] = (start_entry, end_entry, percent_entry)

                    num_row += 1 



    def ok1_button_click(self):
        try:
            self.graph = [[0] * self.node_amount for _ in range(self.node_amount)]

            for i in range(self.node_amount):
                for j in range(i + 1, self.node_amount):
                    entry = self.ans1[i][j]

                    if entry is None:  
                        continue

                    value = entry.get().strip()  

                    if not value: 
                        raise ValueError(f"Weight for edge {i}-{j} cannot be empty.")

                    try:
                        weight = float(value)
                    except ValueError:
                        raise ValueError(f"Weight for edge {i}-{j} must be a valid number.")

                    self.graph[i][j] = weight
                    self.graph[j][i] = weight

            self.graph_valid = True
            messagebox.showinfo("Success", "Graph input stored successfully!")
            self.dictionary_window["1"].destroy()  
            del self.dictionary_window["1"]  

            if "2" in self.dictionary_window:
                self.dictionary_window["2"].focus_force()
            elif "3" in self.dictionary_window:
                self.dictionary_window["3"].focus_force()

            self.check_and_submit()  

        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
            self.graph_valid = False  
            self.dictionary_window["1"].focus_force()




    def ok2_button_click(self):
        try:
            self.nodecost = [0] * self.node_amount
            for i in range(1, self.node_amount):
                value = self.ans2[i].get().strip()
                if not value:
                    raise ValueError("Node cost cannot be empty.")

                self.nodecost[i] = float(value)

            self.nodecost_valid = True
            messagebox.showinfo("Success", "Node cost input stored successfully!")
            self.dictionary_window["2"].destroy()
            del self.dictionary_window["2"]  
            if "1" in self.dictionary_window:
                self.dictionary_window["1"].focus_force()
            elif "3" in self.dictionary_window:
                self.dictionary_window["3"].focus_force()

            self.check_and_submit()  

        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
            self.nodecost_valid = False  
            self.dictionary_window["2"].focus_force()
        
    
    def ok3_button_click(self):
        try:
            self.congestion = [[0] * self.node_amount for _ in range(self.node_amount)]

            for i in range(self.node_amount):
                for j in range(self.node_amount):
                    if(self.ans3[i][j]==None):continue

                    start_entry, end_entry, cost_entry = self.ans3[i][j]

                    if start_entry is None or end_entry is None or cost_entry is None:  
                        continue

                    start_value = start_entry.get().strip() 
                    end_value = end_entry.get().strip()
                    cost_value = cost_entry.get().strip() 

                    if not start_value or not end_value or not cost_value: 
                        self.congestion[i][j]=None
                        continue

                    try:
                        start = float(start_value)
                        end =float(end_value)
                        cost = float(cost_value)
                    except ValueError:
                        raise ValueError(f"Congestion for edge {i}-{j} must be a valid number.")

                    self.congestion[i][j] = (start,end,cost)

            self.congestion_valid = True
            messagebox.showinfo("Success", "Congestion input stored successfully!")
            self.dictionary_window["3"].destroy()  
            del self.dictionary_window["3"]  

            if "1" in self.dictionary_window:
                self.dictionary_window["1"].focus_force()
            elif "2" in self.dictionary_window:
                self.dictionary_window["2"].focus_force()

            self.check_and_submit()  

        except ValueError as e:
            messagebox.showwarning("Warning", str(e))
            self.congestion_valid = False  
            self.dictionary_window["3"].focus_force()


    def check_and_submit(self):
        if self.graph_manual and not self.graph_valid:
            return  

        if self.nodecost_manual and not self.nodecost_valid:
            return 
        
        if self.congestion_manual and not self.congestion_valid:
            return

        self.submit2()



    def submit2(self):
        self.prepareGen.set_graph(self.graph)
        self.prepareGen.set_nodecost(self.nodecost)
        self.prepareGen.set_congestion(self.congestion)
        self.prepareGen.set_algochosen(self.algo_chosen)
        self.prepareGen.set_nodeamount(self.node_amount)
        self.prepareGen.set_speedchosen(self.speed_chosen)
        self.prepareGen.set_manual_graph(self.graph_manual)
        self.prepareGen.set_manual_nodecost(self.nodecost_manual)
        self.prepareGen.set_manual_congestion(self.congestion_manual)
        self.prepareGen.set_root(self.root)
        self.prepareGen.running()
    

    


        


PageMain()
