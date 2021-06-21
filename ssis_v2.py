from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
import re
import mysql.connector
from tkinter import ttk

#connect and queries on the student_data
database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd= "richardjr041501mysql",
    database = "student_data"
)
cursor = database.cursor()

original_id  = "" #a global variable to retain original id of the student even edited
original_course_code = ""  
def frame_destroy():
    frame.destroy()

def frame_update():
    global frame
    frame = Frame(root, bg="#F0F0F0")
    frame.config(bd=1, relief=SOLID)

def table_destroy():
    table.destroy()

def table_update():
    global table
    table = ttk.Treeview(frame, height=12)

def check_ID(key):
    pattern = re.compile(r'\d\d\d\d-\d\d\d\d')
    res = re.fullmatch(pattern, key)
    if res:
        return True
    else:
        return False

def display():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 50, padx = 140)
    
    #define columns of the table
    table ["columns"] = ("Student ID", "Full Name", "Gender", "Year", "Course")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Student ID", width = 115, anchor = CENTER, stretch = NO)
    table.column("Full Name", width = 340, anchor = CENTER)
    table.column("Gender", width = 115, anchor = CENTER)
    table.column("Year", width = 115, anchor = CENTER)
    table.column("Course", width = 115, anchor = CENTER)
    #create headings
    table.heading("0")
    table.heading("Student ID", text = "Student ID", anchor = CENTER )
    table.heading("Full Name", text = "Full Name", anchor = CENTER )
    table.heading("Gender", text = "Gender", anchor = CENTER )
    table.heading("Year", text = "Year", anchor = CENTER )
    table.heading("Course", text = "Course", anchor = CENTER )

    count = 0
    display_query = "SELECT * FROM student"
    cursor.execute(display_query)
    for record in cursor:
        table.insert(parent = '', index='end', iid = count, values = (record[0], record[1], record[2], record[3], record[4]))
        count += 1
    table.grid(row=0, column=0, rowspan=6, columnspan=5)

    #entry boxes for update student info
    header = ["ID", "Student Full Name", "Gender", "Year", "Course"]
    for item in range(5):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=6, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    id_entry.grid(row = 7, column = 0, sticky = NSEW)

    name_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    name_entry.grid(row = 7, column = 1, sticky = NSEW)

    gender_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    gender_entry.grid(row = 7, column = 2, sticky = NSEW)

    year_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    year_entry.grid(row = 7, column = 3, sticky = NSEW)

    course_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    course_entry.grid(row = 7, column = 4, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit(id_entry, name_entry, gender_entry, year_entry, course_entry,  del_button, edit_button))
    edit_button.grid(row=8, column=1, pady = 5, padx = 15, sticky=W)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command= lambda: delete(id_entry.get(),id_entry, name_entry, gender_entry, year_entry, course_entry, del_button, edit_button))
    del_button.grid(row=8, column=3, pady = 5, sticky=W, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command= lambda: select(id_entry, name_entry, gender_entry, year_entry, course_entry,  del_button, edit_button))
    select_button.grid(row=8, column=2, pady = 5, sticky=W, padx = 15)

    if table.focus():
        select(id_entry, name_entry, gender_entry, year_entry, course_entry, del_button, edit_button)

#selected data in the table
def select(id_entry, name_entry, gender_entry, year_entry, course_entry, del_button, edit_button):
    
    try:
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        gender_entry.delete(0, END)
        year_entry.delete(0, END)
        course_entry.delete(0, END) 
    except:
        messagebox.showerror("Select Data", "No data was selected!")
    try:
        selected = table.focus()
        values = table.item(selected, "values")
        del_button["state"] = NORMAL
        edit_button["state"] = NORMAL
        id_entry.insert(0, values[0])
        name_entry.insert(0, values[1])
        gender_entry.insert(0, values[2])
        year_entry.insert(0, values[3])
        course_entry.insert(0, values[4])
        global original_id
        original_id = values[0]
    except:
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showerror("Select Data", "No data was selected!")

def select_course(course_code_entry, course_name_entry, del_button, edit_button):
    
    try:
        course_code_entry.delete(0, END)
        course_name_entry.delete(0, END)
    except:
        messagebox.showerror("Select Data", "No data was selected!")
    try:
        selected = table.focus()
        values = table.item(selected, "values")
        del_button["state"] = NORMAL
        edit_button["state"] = NORMAL
        course_code_entry.insert(0, values[0])
        course_name_entry.insert(0, values[1])
       
        global original_course_code
        original_course_code = values[0]
    except:
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showerror("Select Data", "No data was selected!")

#student_id, name, gender, year, course_code - "label of the columns in the database"
def edit(id_stud, name, gender, year, course,  del_button, edit_button):
    
    edit_prompt = messagebox.askyesno("Edit student data", "Are you sure to make this changes?")
    if edit_prompt:
        try:
            query = "UPDATE student SET student_id = %s, name = %s, gender = %s, year = %s, course_code = %s WHERE student_id = %s"
            query_param = (id_stud.get(), name.get(), gender.get(), year.get(), course.get(), original_id)
            cursor.execute(query, query_param)
            database.commit()
            #changes values in the table, where the values are from the entries provided
            selected = table.focus()
            values = table.item(selected, text = "", values=(id_stud.get(), name.get(), gender.get(), year.get(), course.get()))
            id_stud.delete(0, END)
            name.delete(0, END)
            gender.delete(0, END)
            year.delete(0, END)
            course.delete(0, END)
            del_button["state"] = DISABLED
            edit_button["state"] = DISABLED
        except:
            messagebox.showerror("ID already taken", "Student ID {} is already taken. Please provide unique ID number".format(id_stud.get()))

def edit_course(course_code, course_name, original_course_code, edit_button, del_button):
    
    edit_prompt = messagebox.askyesno("Edit course data", "Are you sure to make these changes?")
    if edit_prompt:
        try:
            query = "UPDATE student SET code = %s, course_name = %s WHERE student_id = %s"
            query_param = (course_code.get(), course_name.get(), original_course_code)
            cursor.execute(query, query_param)
            database.commit()
            #changes values in the table, where the values are from the entries provided
            selected = table.focus()
            values = table.item(selected, text = "", values=(course_code.get(), course_name.get()))
            course_code.delete(0, END)
            course_name.delete(0, END)
           
            del_button["state"] = DISABLED
            edit_button["state"] = DISABLED
        except:
            messagebox.showerror("Error", "Course code {} is already taken. Please provide unique course code".format(course_code.get()))        
def delete(id_key,id_entry, name_entry, gender_entry, year_entry, course_entry,  del_button, edit_button):
    
    delete_query = "DELETE FROM student_data.student WHERE student_id = %s"
    del_prompt = messagebox.askyesno("Delete student data", "Are you sure to delete it?") 
    if del_prompt:
        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)
        cursor.execute(delete_query, (id_key,))
        database.commit()
        id_entry.delete(0, END)
        name_entry.delete(0, END)
        gender_entry.delete(0, END)
        year_entry.delete(0, END)
        course_entry.delete(0, END)
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showinfo("Deleted Data", "Data is/are deleted!")

def delete_course(course_code, course_name, del_button, edit_button):
    
    delete_query = "DELETE FROM student_data.courses WHERE code = %s"
    del_prompt = messagebox.askyesno("Delete student data", "Are you sure to delete it?") 
    if del_prompt:
        del_data = table.selection()[0] #deletes selected data in treeview
        table.delete(del_data)
        cursor.execute(delete_query, (course_code.get().upper(),))
        database.commit()
        course_code.delete(0,END)
        course_name.delete(0,END)
        del_button["state"] = DISABLED
        edit_button["state"] = DISABLED
        messagebox.showinfo("Deleted Data", "Data is/are deleted!")

def search(key):
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="nw", pady = 50, padx = 140)

    #define columns of the table
    table ["columns"] = ("Student ID", "Full Name", "Gender", "Year", "Course")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Student ID", width = 115, anchor = CENTER, stretch = NO)
    table.column("Full Name", width = 340, anchor = W)
    table.column("Gender", width = 115, anchor = W)
    table.column("Year", width = 115, anchor = CENTER)
    table.column("Course", width = 115, anchor = CENTER)
    #create headings
    table.heading("0")
    table.heading("Student ID", text = "Student ID", anchor = CENTER )
    table.heading("Full Name", text = "Full Name", anchor = CENTER )
    table.heading("Gender", text = "Gender", anchor = CENTER )
    table.heading("Year", text = "Year", anchor = CENTER )
    table.heading("Course", text = "Course", anchor = CENTER )
    
    #keyword must be complete
    query = "SELECT * FROM Student WHERE student_id LIKE %s or name LIKE %s or gender LIKE %s or year LIKE %s or course_code LIKE %s"
    keys = (key.get(), key.get(), key.get(), key.get(), key.get(),)
    key.delete(0,END)
    cursor.execute(query, keys)

    count = 0
    for record in cursor:
        table.insert(parent = '', index='end', iid = count, values = (record[0], record[1], record[2], record[3], record[4]))
        count += 1
    table.grid(row=0, column=0, rowspan=6, columnspan=5)

    #entry boxes for update student info
    header = ["ID", "Student Full Name", "Gender", "Year", "Course"]
    for item in range(5):

        if item == 1:
            e = Entry(frame, width=20, font=('Helvetica',8, "bold"), justify = CENTER)
            e.grid(row=6, column=item,sticky = NSEW) 
            e.insert(END, header[item])
            e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
        else:
            if item == 1:
                e = Entry(frame, width=10, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW, padx = 5) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")
            else:
                e = Entry(frame, width=12, font=('Helvetica',8, "bold"), justify = CENTER)
                e.grid(row=6, column=item, sticky = NSEW) 
                e.insert(END, header[item])
                e.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    id_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    id_entry.grid(row = 7, column = 0, sticky = NSEW)

    name_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    name_entry.grid(row = 7, column = 1, sticky = NSEW)

    gender_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    gender_entry.grid(row = 7, column = 2, sticky = NSEW)

    year_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    year_entry.grid(row = 7, column = 3, sticky = NSEW)

    course_entry = Entry(frame, width=10, font=('Helvetica',8), justify = CENTER)
    course_entry.grid(row = 7, column = 4, sticky = NSEW)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit(id_entry, name_entry, gender_entry, year_entry, course_entry,  del_button, edit_button))
    edit_button.grid(row=8, column=1, pady = 5, padx = 15, sticky=W)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command= lambda: delete(id_entry.get(),id_entry, name_entry, gender_entry, year_entry, course_entry, del_button, edit_button))
    del_button.grid(row=8, column=3, pady = 5, sticky=W, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command= lambda: select(id_entry, name_entry, gender_entry, year_entry, course_entry,  del_button, edit_button))
    select_button.grid(row=8, column=2, pady = 5, sticky=W, padx = 15)
                  
def addStudent():  
    try:
        table_destroy()
    except:
        pass
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 50, padx=170)

    add_title = Label(frame, text="Add Student", fg='black', font=('Open Sans',20,"bold"), bg="#F0F0F0")
    add_title.grid(row=0, column=0, pady=10,  padx = 2, columnspan = 3, sticky=NSEW)

    id_lbl = Label(frame, text="ID Number:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=20, sticky='w')
    e_id = Entry(frame, width=50, borderwidth=2)
    e_id.grid(row=1, column=1, padx=(0,20), pady=20, columnspan=2)
   
    name_lbl = Label(frame, text="Full Name:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=20, sticky='w')
    e_name = Entry(frame,  width=50, borderwidth=2)
    e_name.grid(row=2, column=1, padx=(0,20), pady=20, columnspan=2)
    

    
    gender_lbl = Label(frame, text="Gender:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=20, sticky='w')
    gender_options = ["Select Gender", "Male", "Female", "Others"]
    gender_dropdown = ttk.Combobox(frame, values = gender_options)
    gender_dropdown.current(0)

#if gender is not in the dropdown options, provide entry 
    e_others = Entry(frame, width=20, borderwidth=2)
    def others_selection(event):
        if gender_dropdown.get() == "Others":
            e_others.grid(row=3, column = 2, pady=20)
        else:
            try:
                e_others.grid_forget()
            except:
                pass

    gender_dropdown.bind("<<ComboboxSelected>>", others_selection)
    gender_dropdown.grid(row=3, column=1, pady=20, sticky="w")
    year_lbl = Label(frame, text="Year:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=4, column=0, padx=10, pady=20, sticky='w')
    #dropdown box for year, val to 1-5
    year_options = ["Select Year",1,2,3,4,5] #options in the combobox
    year_dropdown = ttk.Combobox(frame, values = year_options)
    year_dropdown.grid(row=5, column=1, padx=(0,20), pady=20, sticky="w")
    year_dropdown.current(0) #initially set combobox to Select Course

    year_dropdown.grid(row=4, column=1, padx=(0,20), pady=20, sticky="w")

    course_lbl = Label(frame, text="Course:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=5, column=0, padx=10, pady=20, sticky='w')
    #query to get course code from database to be used as options in the combobox
    course_codes = ["Select Course"] #options in the combobox
    query = "SELECT code FROM courses"
    cursor.execute(query)
    for code in cursor:         #iterate to store course_code on the list
        course_codes.append(code)

    course_dropdown = ttk.Combobox(frame, values = course_codes)
    course_dropdown.grid(row=5, column=1, padx=(0,20), pady=20, sticky="w")
    course_dropdown.current(0) #initially set combobox to Select Course
    course_dropdown.grid(row=5, column=1, padx=(0,20), pady=20)
   
    def get_data():
       
        id_num = e_id.get()
        name = e_name.get()
        if gender_dropdown.get() == "Others":
            gender = e_others.get()
        else:
            gender = gender_dropdown.get()
        year = year_dropdown.get()
        course = course_dropdown.get()
        data = [id_num, name.upper(), gender.upper(), year, course]
        #checks if all variable are completed, else it breaks loop
        for var in data:
            if var == '':
                messagebox.showerror("Error", "Data incomplete, complete data to proceed!")
                run = False
                break
            elif gender == "Select Gender" or year  == "Select Year" or course == "Select Course":
                messagebox.showerror("Error", "Data incomplete, complete data to proceed!")
                run = False
                break
            else:
                run = True
            
        if check_ID(data[0]) == False: #checks if the id's format is valid
            messagebox.showerror("Error", 'Invalid ID format must be in this format e.g "2019-0001"')
            run = False 

        if run:           
            try:
                cursor.execute("INSERT INTO student VALUES(%s, %s, %s, %s, %s)", (data[0],data[1],data[2],data[3],data[4]))
                database.commit()
                #delete the entries if inputs are valid
                e_id.delete(0,END)
                e_name.delete(0,END)
                gender_dropdown.current(0)
                year_dropdown.current(0)
                course_dropdown.current(0)
                try:    #used try and except here because error is thrown if gender dropdown is not male or female
                    e_others.grid_forget()
                except:
                    pass
            except:
                messagebox.showinfo("Invalid", "ID number {} is already used!".format(data[0]))
           
    add_button = Button(frame, text="Add Student", padx=10, pady=10, borderwidth=2, bg='royal blue1', fg="white", font=("Helvetica", 12, "bold"), command=get_data)
    add_button.grid(row=6, column=0, columnspan=3, padx=20, pady=30, sticky=N)

def add_course():
    try:
        table_destroy()
    except:
        pass
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="NW", pady = 130, padx=150)

    title = Label(frame, text="Add Course", fg='black', font=('Open Sans',20,"bold"), bg="#F0F0F0")
    title.grid(row=0, column=0, padx=5, pady=10, columnspan = 4, sticky=NSEW)

    course_code = Entry(frame, width=50, borderwidth=2)
    course_code.grid(row=1, column=1, padx=(0,20), pady=20, columnspan=2)
    course_code_lbl = Label(frame, text="Course Code:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=20, sticky='w')

    course_name = Entry(frame,  width=50, borderwidth=2)
    course_name.grid(row=2, column=1, padx=(0,20), pady=20, columnspan=2)
    course_name_lbl = Label(frame, text="Course Name:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=20, sticky='w')

    def getdata():
        
        #checks if all variable are completed, else it breaks loop
        data = [course_code.get().upper(), course_name.get().upper()]
        run = True
        for var in data:
            if var == '':
                messagebox.showerror("Error", "Data incomplete, complete data to proceed!")
                run = False
                break
        if run:
            try:
                if check_course_code(course_code.get()):
                    cursor.execute("INSERT INTO courses VALUES (%s, %s)", (data[0], data[1]))
                    database.commit()
                    course_code.delete(0, END)
                    course_name.delete(0, END)
                    messagebox.showinfo("ADDED", "Course Added!")
                else:
                    messagebox.showinfo("Invalid","Course code is not valid, e.g BSCS")
            except: 
                messagebox.showinfo("Invalid","Course code {} was already used.".format(data[0]))
        
    add_course_button = Button(frame, text="Add Course", padx=10, pady=10, borderwidth=2, bg='royal blue1', fg="white", font=("Helvetica", 8, "bold"), command=getdata)
    add_course_button.grid(row=4, column=1, pady=30, sticky=NSEW, columnspan = 1)

def display_course():
    try:
        frame_destroy()
        table_destroy()
    except:
        pass
    frame_update()
    table_update()
    frame.grid(row=1, column=1, rowspan = 7, columnspan=5, sticky="nw", pady = 50, padx = 140)
    
    #define columns of the table
    table ["columns"] = ("Course Code", "Course Name")
    #Format columns
    table.column("#0", width = 0, stretch = NO)
    table.column("Course Code", width = 115, anchor = CENTER, stretch = NO)
    table.column("Course Name", width = 500, anchor = W)
    #create headings
    table.heading("0")
    table.heading("Course Code", text = "Course Code", anchor = CENTER )
    table.heading("Course Name", text = "Course Name", anchor = CENTER )
  
    count = 0
    display_courses_query = "SELECT * FROM courses"
    cursor.execute(display_courses_query)
    for record in cursor:
        table.insert(parent = '', index='end', iid = count, values = (record[0], record[1]))
        count += 1
    table.grid(row=0, column=0, rowspan=6, columnspan=5)

    #entry boxes for update student info
    header = ["Course Code", "Course Name"]
    course_code_header = Entry(frame, width=20, font=('Helvetica',8))
    course_code_header.grid(row = 6, column = 0, sticky = NSEW, columnspan = 2)
    course_code_header.insert(END, header[0])
    course_code_header.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    course_name_header = Entry(frame, width=20, font=('Helvetica',8))
    course_name_header.grid(row = 6, column = 1, sticky = NSEW, columnspan=4)
    course_name_header.insert(END, header[1])
    course_name_header.config(state="disabled", disabledbackground = "white", disabledforeground = "black")

    # entry for update inputs
    course_code_entry = Entry(frame, width=20, font=('Helvetica',8))
    course_code_entry.grid(row = 7, column = 0, sticky = NSEW, columnspan = 2)

    course_name_entry = Entry(frame, width=20, font=('Helvetica',8))
    course_name_entry.grid(row = 7, column = 1, sticky = NSEW, columnspan=4)

    edit_button = Button(frame, text="Edit", padx =33, pady = 10, state = "disabled",  borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit_course(course_code_entry, course_name_entry, original_course_code, edit_button, del_button))
    edit_button.grid(row=8, column=0, pady = 5, padx = (55,0), sticky=W)

    del_button = Button(frame, text="Delete", padx =25, pady = 10, state = "disabled",  borderwidth = "2", bg='#e64e4e', fg = "white", font=("Open Sans", 8, "bold"), command= lambda: delete_course(course_code_entry, course_name_entry, del_button, edit_button))
    del_button.grid(row=8, column=4, pady = 5, sticky=W, padx = 15)

    select_button = Button(frame, text="Select Data", padx =25, pady = 10, borderwidth = "2", bg='#B99976', fg = "black", font=("Open Sans", 8, "bold"), command= lambda: select_course(course_code_entry, course_name_entry, del_button, edit_button))
    select_button.grid(row=8, column=2, pady = 5, sticky=W)

    # if table.focus():
    #     select_course(course_code_entry, course_name_entry, del_button, edit_button)
   
def check_course_code(course_code):
    pattern = re.compile(r'BS\w+')
    res = re.fullmatch(pattern, course_code.upper())
    if res:
        return True

root = Tk()
root.title("Student Information System")
root.geometry("1228x720")
root.configure(bg="#EEEEEE")
root.iconbitmap("images/app_icon.ico")

#UI for main layout
#use image coffee.jpg as root background
bg = ImageTk.PhotoImage(Image.open("images/coffee.jpg"))
bg_lbl = Label(root, image = bg )
bg_lbl.grid(row=1, column=1, sticky=NSEW)

#frames, 
sidebar = LabelFrame(root, bg = "#EEEEEE", borderwidth = 2)
header = LabelFrame(root, bg= "#cbcac8", borderwidth = 1.5)
frame = Frame(root, bg="#F0F0F0", borderwidth=1.5)          #destroyed after every function
frame.config(bd=1, relief=SOLID)

table = ttk.Treeview(frame, height = 12)

#table style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background = "#EEEEEE", rowheight = 30, fieldbackground="#EEEEEE")
style.configure("Treeview",font=("Montserrat", 12))
style.configure("Treeview.Heading",font=("Montserrat", 12, "bold"))
style.map("Treeview", background=[("selected", "#B99976")])

#grid bar
sidebar.grid(row=1, column=0, sticky="ns", rowspan = 5)
header.grid(row=0, column=0, columnspan=2, sticky = "we")
#main_frame.grid(row=1, column=1, sticky = 'n', pady = 50)

#title in located at the header
title = Label(header, text='Student Information System', font=("Open Sans", 17, "bold"), bg="#cbcac8", fg="black", padx = 28, pady=20 )
title.grid(row=0, column = 0, columnspan=3)

#button icons
icon_display  = ImageTk.PhotoImage(Image.open("images/list_icon.png"))
icon_lbl_1 = Label(sidebar, image=icon_display)
icon_lbl_1.grid(row=0, column=0, pady=(20,0))

icon_add  = ImageTk.PhotoImage(Image.open("images/add_icon.png"))
icon_lbl_2 = Label(sidebar, image=icon_add)
icon_lbl_2.grid(row=2, column=0, pady=(20,0))

icon_display_course = ImageTk.PhotoImage(Image.open("images/display_course.png"))
icon_lbl_3 = Label(sidebar, image=icon_display_course)
icon_lbl_3.grid(row=4, column=0, pady=(20,0))

icon_add_course = ImageTk.PhotoImage(Image.open("images/add_course.png"))
icon_lbl_4 = Label(sidebar, image=icon_add_course)
icon_lbl_4.grid(row=6, column=0, pady=(20,0))



#buttons in the sidebar
display_button = Button(sidebar, text="Display\nStudents",  padx = 30,bg='#EEEEEE', font=("Open Sans", 12, "bold"), borderwidth = 0, command = display) 
add_button = Button(sidebar, text="Add\nStudent",  bg='#EEEEEE', padx = 30, font=("Open Sans", 12, "bold"), borderwidth = 0, command=addStudent)
display_course_button = Button(sidebar, text="Display\nCourse",  bg='#EEEEEE', padx = 30,font=("Open Sans", 12, "bold"), borderwidth = 0, command=display_course)
add_course_button = Button(sidebar, text="Add\nCourse",  bg='#EEEEEE', padx = 30,font=("Open Sans", 12, "bold"), borderwidth = 0, command=add_course)

display_button.grid(row=1, column=0, pady = (0, 15))
add_button.grid(row=3, column=0, pady = (0, 15))
display_course_button.grid(row=5, column=0, pady=(0,15))
add_course_button.grid(row=7, column=0, pady=(0,15))


search_button = Button(header, text="Search", bg='royalblue1',fg="white", padx = 20, font=("Open Sans", 10, "bold"), borderwidth = 0, command = lambda: search(search_entry))
search_entry = Entry(header, width=20,fg='black', font=('Open Sans',12, 'bold'), borderwidth="1")
search_label = Label(header, text="Search Student: ", bg='#cbcac8', font=("Open Sans", 12, "bold"), fg='black')
search_label.grid(row=0, column=3, padx=(400,0))
search_entry.grid(row=0, column=4, padx=(2,0))
search_button.grid(row=0, column=5,padx=(5,0))

root.mainloop()