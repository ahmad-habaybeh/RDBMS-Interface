import tkinter as tk
from tkinter import ttk
import mysql.connector
import mysql.connector as mysql
import json
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from PIL import ImageTk, Image


connection = mysql.connect(
		user="root",
		password="Admn",
		database="dwh",
		host="localhost"
    )


class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		self.state("zoomed")
		container.grid(row=0, column=0, sticky = NSEW)

		container.rowconfigure(0, weight = 1)
		container.columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2, Page3):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky =NSEW)

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		imgfrm = Frame(self, bg = 'white')
		imgfrm.grid(row=0, column=1,  sticky = NSEW)
        
        # Create an object of tkinter ImageTk
		im = Image.open('Logo.jpg').resize((400, 300), Image.ANTIALIAS)
		img = ImageTk.PhotoImage(im)
        
        # Create a Label Widget to display the text or Image
		label_img = Label(imgfrm, image = img)
		label_img.image = img
		label_img.grid(row = 0,column = 2)
 
		label = tk.Label(imgfrm, text ="Graphical User Interface for an Educational System Using Relational Database",padx = 200, pady = 30, font=("Arial", 22))
		label.config(bg="white")	
		# label of frame Layout 2
		strtfrm = Frame(self, bg = 'white')
		strtfrm.grid(row=1, column=1,  sticky = NSEW)
		strtfrm.grid_rowconfigure(1, weight=1)
		strtfrm.grid_columnconfigure(1, weight=1)


		# putting the grid in its place by using
		# grid
		label.grid(row = 1, column = 2, padx = 10, pady = 10, rowspan=4, sticky = NSEW)

		button1 = ttk.Button(strtfrm, width=20, text ="Search By Professor",
		command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 3, column = 1, padx = 10, pady = 10)
		button1.grid_rowconfigure(1, weight=1)
		## button to show frame 2 with text layout2
		button2 = ttk.Button(strtfrm, width=20, text ="Department Statistics",
		command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 4, column = 1, padx = 10, pady = 10)
		button2.grid_rowconfigure(1, weight=1)
		## button to show frame 2 
		button3 = ttk.Button(strtfrm, width=20, text ="More Statistics",
		command = lambda : controller.show_frame(Page3))
	
		# putting the button in its place by
		# using grid
		button3.grid(row = 5, column = 1, padx = 10, pady = 10)
		button3.grid_rowconfigure(1, weight=1)


# second window frame page1
class Page1(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
        
        ################ahmad code #################
        
        # function for search by professor


		def db_connect(src):
			connection = mysql.connect(
                user="root",
                password="Admn",
                database="nlidb",
                host="localhost"
            )
			if entry1.get().upper() != '':
				df = pd.read_sql_query(r"SELECT p.first_name,p.last_name,p.gender,d.department_name, p.contact_email,p.contact_phone, p.professor_id " +
                        "FROM nlidb.professors p,nlidb.department d where p.department_id = d.department_id " + 
						"and upper(CONCAT(p.first_name,' ',p.last_name)) like '%"+entry1.get().upper()+"%';", connection)                # Clear the treeview list items
				for item in tree.get_children():
				    tree.delete(item)
				for index, row in df.iterrows():
				    tree.insert("", 0, text=index, values=list(row),iid=row["professor_id"])

        # function used to filter by department


		def db_connect_cmb(event):
			connection = mysql.connect(
                user="root",
                password="Admn",
                database="nlidb",
                host="localhost"
				)
			if combo.get().upper() != 'Select Department':
				if combo.get().upper() != 'ALL':
					df = pd.read_sql_query(r"SELECT p.first_name,p.last_name,p.gender,d.department_name, p.contact_email,p.contact_phone, p.professor_id FROM nlidb.professors p,nlidb.department d where p.department_id = d.department_id and d.department_name= '"+combo.get().upper()+"';", connection)
                    # Clear the treeview list items
				else:
					df = pd.read_sql_query(r"SELECT p.first_name,p.last_name,p.gender,d.department_name, p.contact_email,p.contact_phone, p.professor_id FROM nlidb.professors p,nlidb.department d where p.department_id = d.department_id;", connection)

				for item in tree.get_children():
					tree.delete(item)
				for index, row in df.iterrows():
					tree.insert("", 0, text=index, values=list(row), iid=row["professor_id"])

        # function to open a new window
        # on a button click


		def openNewWindow(tiid):

            # Toplevel object which will
            # be treated as a new window
			newWindow = Toplevel(rt_frame)

            # sets the title of the
            # Toplevel widget
			newWindow.title("Publications")

            # sets the geometry of toplevel
			newWindow.geometry("900x300")
			nfrm = LabelFrame(newWindow, text='Research Students', bd=3,
                            relief='groove', height=180, width=580)
			cols1=['Student Name', 'Research Project Title','Student Email']
            # Treeview Scrollbar horizontal
			tree_scroll_hor1 = Scrollbar(nfrm, orient=HORIZONTAL)
            
            
            # Create Treeview
			tree1 = ttk.Treeview(
                nfrm, xscrollcommand=tree_scroll_hor1.set, selectmode='browse')
			tree1['show'] = 'headings'
            
            # Configure the scrollbar
			tree_scroll_hor1.config(command=tree1.xview)
			
			tree1["columns"] = cols1
			for i in cols1:
			    tree1.column(i, anchor="w")
			    tree1.heading(i, text=i, anchor='w')
            
			connection = mysql.connect(
                user="root",
                password="Admn",
                database="dwh",
                host="localhost"
                )
			qry = '''SELECT DISTINCT
                    rs.student_name,
                    rs.research_project_title,
                    rs.student_email
                FROM
                    dwh.research_fact_table a,
                    dwh.department_dim d,
                    dwh.professors_dim p,
                    dwh.research_students_dim rs
                WHERE
                    a.department_id = d.department_id
                        AND a.professor_id = p.professor_id
                        AND a.student_id = rs.student_id'''
			df = pd.read_sql_query(qry + ' and a.professor_id='+tiid, connection)
            # Clear the treeview list items
			for item in tree1.get_children():
			    tree1.delete(item)
			for index, row in df.iterrows():
			    tree1.insert("", 0, text=index, values=list(row))
                
			tree1.pack()
			tree_scroll_hor1.pack(side=BOTTOM, fill=X)
            
			Button(nfrm, text='Exit', width=20, command=newWindow.destroy).pack()

			nfrm.pack()
            


        #root.minsize(800, 600)

        # Add some style
		style = ttk.Style()
        # Pick a theme
		style.theme_use("clam")

        # Open Window expaned
        #root.state('zoomed')

        # Create the main frame
		rt_frame = Frame(self)
		rt_frame.grid(row = 1, column = 0, padx = 10, pady = 10)
        # Create three labelframes
		frame1 = LabelFrame(rt_frame, text='Search By Professor',
                            bd=3, relief='groove', height=50, width=580)
		frame2 = LabelFrame(rt_frame, text='Filter By Department',
                            bd=3, relief='groove', height=50, width=580)
		frame3 = LabelFrame(rt_frame, text='Result', bd=3,
                            relief='groove', height=180, width=580)

        # adding content to search by professor frame
		Label(frame1, text='Search By Professor', width=20, anchor='e').grid(
            sticky='news', row=0, column=0, padx=15, pady=15)

		entry1 = ttk.Entry(frame1, width=60)
        #entry1.insert(0, 'Please fill in value')
		entry1.grid(row=0, column=1, padx=5, pady=15, sticky='news')

		Button(frame1, text='Enter', width=20, command=lambda: db_connect(
            'BTN')).grid(row=0, column=2, padx=15, pady=15, sticky='news')

        # adding content to filter by department frame
        # fill the name of departments from DB
		connection = mysql.connect(
            user="root",
            password="Admn",
            database="dwh",
            host="localhost"
        )
		df = pd.read_sql_query(
            "SELECT department_name FROM department_dim;", connection)

        # convert the dataframe to list in order to add it to the combobox
		combo_values = df['department_name'].values.tolist()

		combo_values.append('ALL')

		combo = ttk.Combobox(frame2, values=combo_values, width=60)
		combo.insert(0, 'Select Department')
		combo.pack(pady=15)

        # call the filter function upon changing the value of the combobox
		combo.bind('<<ComboboxSelected>>', db_connect_cmb)


        # fill the content of the frame 3 (result frame)
        # set the treeview headers.
		cols = ['First Name', 'Last Name',  'Gender', 'Department Name', 'Contact Email', 'Contact Phone']

        # Treeview Scrollbar horizontal
		self.tree_scroll_hor = Scrollbar(frame3, orient=HORIZONTAL)


        # Create Treeview
		tree = ttk.Treeview(
            frame3, xscrollcommand=self.tree_scroll_hor.set, selectmode='browse')
		tree['show'] = 'headings'

        # Configure the scrollbar
		self.tree_scroll_hor.config(command=tree.xview)

		tree["columns"] = cols
		for i in cols:
		    tree.column(i, anchor="w")
		    tree.heading(i, text=i, anchor='w')


		tree.pack()
		self.tree_scroll_hor.pack(side=BOTTOM, fill=X)
		tree.bind('<Double-1>', lambda e: openNewWindow(tree.focus()))

		frame1.pack(fill='both', anchor='center')
		frame2.pack(fill='both', anchor='center')
        # frame3.pack_propagate(0)
		frame3.pack(fill=BOTH)
        # frame3.propagate(FALSE)

		#rt_frame.pack(fill='y')
        
        ############ end ###################
		#label = ttk.Label(self, text ="Page 1", font = LARGEFONT)
		#label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		frmpg1 = Frame(self)
		frmpg1.grid(row = 0, column=0)
		button1 = ttk.Button(frmpg1, width=20, text ="Start Page",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 0, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(frmpg1, width=20,text ="Department Statistics",
							command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 0, column = 2, padx = 10, pady = 10)
        
		button3 = ttk.Button(frmpg1, width=20, text ="More Statistics",
							command = lambda : controller.show_frame(Page3))
	
		# putting the button in its place by
		# using grid
		button3.grid(row = 0, column = 3, padx = 10, pady = 10)
        




# third window frame page2
class Page2(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		############################ hussam code ######################################## 

		########################################## Departments Statistics#########################################################

		  ###### Department Professor Statistics
		dept_prof = pd.read_sql_query("SELECT deptDim.department_name, resFact.professor_id FROM research_fact_table resFact" + 
								" join department_dim deptDim on resFact.department_id = deptDim.department_id "+ 
								" where resFact.department_id IS NOT NULL group by deptDim.department_name,resFact.professor_id;", connection)
		#sn.countplot(x='department_name', data = dept_prof)
		#print(dept_prof)

		  ###### Department Publication Statistics
		dept_public = pd.read_sql_query("SELECT deptDim.department_name, resFact.publication_id FROM research_fact_table resFact" + 
								" join department_dim deptDim on resFact.department_id = deptDim.department_id "+ 
								" where resFact.department_id IS NOT NULL group by deptDim.department_name,resFact.publication_id;", connection)
		#sn.countplot(x='department_name', data = dept_public)
		#print(dept_public)
		  ###### Department Projects Statistics
		dept_proj = pd.read_sql_query("SELECT deptDim.department_name, resFact.research_project_id FROM research_fact_table resFact" + 
								" join department_dim deptDim on resFact.department_id = deptDim.department_id "+ 
								" where resFact.department_id IS NOT NULL && resFact.research_project_id IS NOT NULL group by deptDim.department_name,resFact.research_project_id;", connection)
		#sn.countplot(x='department_name', data = dept_proj)
		#print(dept_proj)

		########################################## Professors By Gender #########################################################
		prof_gender = pd.read_sql_query("SELECT resFact.professor_id , profDim.gender FROM research_fact_table resFact" + 
								" join professors_dim profDim on profDim.professor_id = resFact.professor_id "+ 
								" where resFact.professor_id IS NOT NULL  group by resFact.professor_id;", connection)
		#plt.figure(figsize=(10,7))
		#prof_gender['gender'].value_counts().plot(kind='pie')
		#plt.grid(False)
		#plt.tight_layout()
		#print(prof_gender)

		############################################ functions part #########################################

		#this function will return gender pie plot
		def gender_figure() -> Figure:  
		    # plot the data
		    figure = Figure(figsize=(20, 4))
		    axes = figure.subplots()
		    gender_pie = prof_gender['gender'].value_counts().plot(kind='pie', autopct='%.0f%%',shadow = True, explode = [0, 0.05],ax=axes)
		    gender_pie.set_title("Gender Distribution")
		    return figure


		# this function will embed all department statistcs on frame 3 using subplots
		def department_figure_all():
		    global bar1
		    clear_charts()
		    # plot the data
		    figure = Figure(figsize=(20, 5))
		    axes = figure.subplots(1,3)
		    prfo = sn.countplot(x='department_name', data = dept_prof, ax=axes[0])
		    public = sn.countplot(x='department_name', data = dept_public, ax=axes[1])
		    proj = sn.countplot(x='department_name', data = dept_proj, ax=axes[2])
		    self.bar1 = FigureCanvasTkAgg(figure, f3)
		    self.bar1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=TRUE)
		    prfo.set_xlabel("")
		    public.set_xlabel("Department Name")
		    proj.set_xlabel("")
            
		    prfo.set_ylabel("Professors")
		    public.set_ylabel("Publications")
		    proj.set_ylabel("Projects")
            #label size for department names
		    prfo.tick_params(labelsize=8)
		    public.tick_params(labelsize=8)
		    proj.tick_params(labelsize=8)
            ### plot color
		    prfo.tick_params(labelsize=8)
		    public.tick_params(labelsize=8)
		    
		    
		    public.set_title("Department Statistics")
            
		# this function will embed one of department statistcs on frame 3 using subplots    
		def department_figure_for(dept_df, y_label = ""): 
		    global bar2
		    clear_charts()
		    # plot the data
		    figure = Figure(figsize=(20, 5))
		    axes = figure.subplots()
		    plot_for = sn.countplot(x='department_name', data = dept_df, ax=axes)
		    self.bar2 = FigureCanvasTkAgg(figure, f3)
		    self.bar2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=TRUE) 
		    plot_for.set_xlabel("Department Name")
		    plot_for.set_ylabel(y_label)
		    plot_for.set_title("Number of " + y_label + " per Department")

		# will make combobox control on charts display
		def combo_dept():   
		    if combo.get().upper() != 'Select Department Statistics':
		    	if combo.get().upper() == 'ALL':
				    department_figure_all()				    
		    	elif combo.get() == 'Professors':
				    department_figure_for(dept_prof,'Professors')
		    	elif combo.get()== 'Publications':
				    department_figure_for(dept_public,'Publications')
		    	elif combo.get() == 'Projects':
				    department_figure_for(dept_proj,'Projects')
                    
		  #clear charts		  
		def clear_charts():
		   self.bar1.get_tk_widget().pack_forget()
		   self.bar2.get_tk_widget().pack_forget()



		############################# end hussam code ##################################3
 
		#######hussam start ######
		#root.minsize(800, 600)

        # Add some style
		style = ttk.Style()
        # Pick a theme
		style.theme_use("clam")

        # Open Window expaned
		#root.state('zoomed')
		root_frame = Frame(self)
		root_frame.grid(row = 1, column = 0, padx = 10, pady = 10)
		#scroll_ver = Scrollbar(root_frame,orient= VERTICAL)
		#scroll_ver.pack(side=RIGHT, fill=Y)

		# Create three labelframes
		f1 = LabelFrame(root_frame, text='Professor By Gender',
						    bd=3, relief='groove', height=40, width=850)
		f2 = LabelFrame(root_frame, text='Departments Statistics',
						    bd=3, relief='groove', height=40, width=850)
		f3 = LabelFrame(root_frame, text='Result', bd=3,
						    relief='groove', height=170, width=850)


		#gender chart define
		fig_gender = gender_figure()
		bar0 = FigureCanvasTkAgg(fig_gender, f1) 
		bar0.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)


		#define count plots that will change based on combobox
		figure1 = Figure(figsize=(20, 5))
		axes1 = figure1.subplots(1,3)
		figure2 = Figure(figsize=(20, 5))
		axes2 = figure2.subplots()
		self.bar1 = FigureCanvasTkAgg(figure1, f3) 
		self.bar2 = FigureCanvasTkAgg(figure2, f3) 
		

		#combobox values for department
		combo_values = ['Professors','Publications','Projects']
		combo_values.append('ALL')

		combo = ttk.Combobox(f2, values=combo_values, width=60)
		combo.insert(0, 'Select Department Statistics')
		combo.pack(pady=12)

		# call the filter function upon changing the value of the combobox
		combo.bind('<<ComboboxSelected>>', lambda _: combo_dept())



		#scroll_ver = Scrollbar(root_frame, orient=VERTICAL)
		#scroll_ver.pack(side=RIGHT, fill=Y)

		f1.pack(fill='both', anchor='center')
		f2.pack(fill='both', anchor='center')
		#root_frame.pack_propagate(1)
		f3.pack(fill=BOTH)



		frmpg1 = Frame(self)
		frmpg1.grid(row = 0, column=0)
		button1 = ttk.Button(frmpg1, width=20, text ="Start Page",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 0, column = 1, padx = 10, pady = 5)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(frmpg1, width=20, text ="Search By Professor",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 0, column = 2, padx = 10, pady = 5)
        
		button3 = ttk.Button(frmpg1, width=20, text ="More Statistics",
							command = lambda : controller.show_frame(Page3))
	
		# putting the button in its place by
		# using grid
		button3.grid(row = 0, column = 3, padx = 10, pady = 5)


# third window frame page2
class Page3(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		############################ abed code ######################################## 


		########################################## Projects By Research Area #########################################################
		area_proj = pd.read_sql_query("SELECT  areaDim.research_area_title,resFact.research_project_id  FROM research_fact_table resFact" + 
								" join research_interest_dim areaDim on resFact.research_area_id = areaDim.research_area_id "+ 
								" where resFact.research_area_id IS NOT NULL && resFact.research_project_id  IS NOT NULL  group by resFact.research_area_id,resFact.research_project_id;", connection)
		#print(area_proj)
		#sn.countplot(x='research_area_title', data = area_proj)

		########################################## Puplications By Professors #########################################################
		prof_publcations = pd.read_sql_query("SELECT  resFact.professor_id,profDim.first_name as Name,resFact.publication_id  FROM research_fact_table resFact" + 
								" join professors_dim profDim on resFact.professor_id = profDim.professor_id "+ 
								" where resFact.professor_id IS NOT NULL && resFact.publication_id  IS NOT NULL  group by resFact.professor_id,resFact.publication_id;", connection)
		#print(prof_publcations)
		#test = sn.countplot(x='Name', data = prof_publcations)
		############################################ functions part #########################################

		    
		# this function will embed one of department statistcs on frame 3 using subplots    
		def new_figure_for(other_df,gr_name): 
		    global bar3
		    clear_charts_oth()
		    # plot the data
		    figure = Figure(figsize=(20, 5))
		    axes = figure.subplots()
		    new_plot = sn.countplot(x=gr_name, data = other_df, ax=axes)
		    self.bar3 = FigureCanvasTkAgg(figure, f5)
		    self.bar3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=TRUE)
		    
		    if(gr_name == 'research_area_title'):
		    	new_plot.set_xlabel("Research Area")
		    	new_plot.set_ylabel("Projects")
		    	new_plot.set_title("Number of Projects per Research Area")
		    elif (gr_name == 'Name'):
		    	new_plot.set_xlabel("Professors")
		    	new_plot.set_ylabel("Puplications")
		    	new_plot.set_title("Number of Puplications for each Professor")
		# will make combobox control on charts display ## other types
		def combo_other():   
		    if combo1.get().upper() != 'Select Statistics Type':		
		    	if combo1.get() == 'Projects By Research Area':
				    new_figure_for(area_proj,'research_area_title')
		    	elif combo1.get()== 'Puplications By Professors':
				    new_figure_for(prof_publcations,'Name')

		def clear_charts_oth():
		    self.bar3.get_tk_widget().pack_forget()

		############################# end abed code ##################################3
 
		#######abed start ######
		#root.minsize(800, 600)

        # Add some style
		style = ttk.Style()
        # Pick a theme
		style.theme_use("clam")

        # Open Window expaned
		#root.state('zoomed')
		root_frame = Frame(self)
		root_frame.grid(row = 1, column = 0, padx = 10, pady = 10)

		#page 3
		f4 = LabelFrame(root_frame, text='Other Statistics',
						    bd=3, relief='groove', height=50, width=1200)
		f5 = LabelFrame(root_frame, text='Result', bd=5,
						    relief='groove', height=180, width=1200)


		#### other type of statistics define count plots that will change based on combobox
		figure3 = Figure(figsize=(20, 6))
		axes3 = figure3.subplots()
		self.bar3 = FigureCanvasTkAgg(figure3, f5)

		#combobox values for other statistics
		combo_values1 = ['Projects By Research Area','Puplications By Professors']

		combo1 = ttk.Combobox(f4, values=combo_values1, width=60)
		combo1.insert(0, 'Select Statistics Type')
		combo1.pack(pady=15)

		# call the filter function upon changing the value of the combobox
		combo1.bind('<<ComboboxSelected>>', lambda _: combo_other())




		#scroll_ver = Scrollbar(root_frame, orient=VERTICAL)
		#scroll_ver.pack(side=RIGHT, fill=Y)

		f4.pack(fill=BOTH)
		f5.pack(fill=BOTH)


		#scroll configuration
		#scroll_ver.config(command=root_frame)

		frmpg1 = Frame(self)
		frmpg1.grid(row = 0, column=0)
		button1 = ttk.Button(frmpg1, width=20, text ="Start Page",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 0, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(frmpg1, width=20, text ="Search By Professor",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 0, column = 2, padx = 10, pady = 10)
        
		button3 = ttk.Button(frmpg1, width=20, text ="Depatrment Statistics",
							command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button3.grid(row = 0, column = 3, padx = 10, pady = 10)



# Driver Code
app = tkinterApp()
app.mainloop()
