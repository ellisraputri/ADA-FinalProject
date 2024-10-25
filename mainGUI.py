import tkinter as tk

class PageMain:
    def __init__(self):
        self.root = tk.Tk()
        width= self.root.winfo_screenwidth() 
        height= self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (width, height))
        self.root.title("Main Page")
        
        self.title = tk.Label(self.root, text="TSP Visualizer", font='SegoeUI 32 bold')
        self.title.pack(padx=400, pady=5)

        self.algorithmTitle = tk.Label(self.root, text="Algorithm:", font='SegoeUI 20 bold')
        self.algorithmTitle.place(x=20, y=100)

        options = ["Brute Force", "Dynamic Programming", "Branch and Bound"] 
        clicked = tk.StringVar() 
        clicked.set("Brute Force") 
        self.dropdown = tk.OptionMenu(self.root , clicked , *options) 
        self.dropdown.configure(font="SegoeUI 14", background='white')
        self.dropdown.place(x=20, y=150) 
        menu = self.root.nametowidget(self.dropdown.menuname)  
        menu.configure(font="SegoeUI 14")  

        self.nodenum = tk.Label(self.root, text="Node amount:", font='SegoeUI 20 bold')
        self.nodenum.place(x=20, y=220)

        self.nodenumField = tk.Entry(self.root, background='white', foreground='black', font=('SegoeUI',16), width=15)
        self.nodenumField.place(x=22, y=260)
        self.nodenumField.insert(0,'3')

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
        clicked2 = tk.StringVar() 
        clicked2.set("Moderate") 
        self.dropdown2 = tk.OptionMenu(self.root , clicked2 , *options2) 
        self.dropdown2.configure(font="SegoeUI 14", background='white')
        self.dropdown2.place(x=20, y=640) 
        menu2 = self.root.nametowidget(self.dropdown2.menuname)  
        menu2.configure(font="SegoeUI 14")  

        self.submitButton = tk.Button(self.root, text ="Submit", command = self.submit)
        self.submitButton.place(x=20,y=720)
        self.submitButton.configure(font="SegoeUI 16 bold", background='gray', foreground='white')

        self.root.mainloop()


    def submit():
        pass




PageMain()

