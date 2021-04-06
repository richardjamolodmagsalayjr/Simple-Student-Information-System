import csv
from tkinter import *
from tkinter import messagebox
import re

# ID number,Student Name,Gender,Year,Course put this label on the file before running the code
#assume records.csv don't have extra empty lines
#error and message prompts are present in this system, like if the entry is incomplete or ID number not found
window = Tk()
window.configure(bg='white')
mainframe = LabelFrame(window, bg="white", borderwidth=0)
frame = LabelFrame(mainframe)
header = LabelFrame(window,  borderwidth=4, bg="royal blue3")
sidebar_frame = LabelFrame(window)

#widow details
window.title("Student Infromation System")
window.geometry("1440x900")

#button layout on screen
def layout():

    header.grid(row=0, columnspan=6, sticky='we')
    sidebar_frame.grid(row=1, column=0, rowspan=3, pady=10,columnspan=1, sticky='n' )
    mainframe.grid(row=1, column=1, padx = 10, pady = 10 ,sticky='wne')

    display_button = Button(sidebar_frame, text="Display List of Students", padx =76, pady = 50, borderwidth = "1", bg='mint cream', font=("Helvetica", 12, "bold"), command=display) 
    add_button = Button(sidebar_frame, text="         Add Student         ", padx =83, pady = 50, borderwidth = "1", bg='mint cream', font=("Helvetica", 12, "bold"), command=addStudent)
    search_button = Button(sidebar_frame, text="      Search Student       ", padx =81, pady = 50, borderwidth = "1", bg='mint cream', font=("Helvetica", 12, "bold"), command=search)
    

    title = Label(header, text='Student Information System', padx=50, font=("Helvetica", 17, "bold"), bg="royal blue3", fg="white")
    title.grid(row=0, column = 1, columnspan = 2, sticky='we')

    display_button.grid(row=0, column=0, sticky="w", pady=1)
    add_button.grid(row=1, column=0, sticky="w", pady=1)
    search_button.grid(row=2, column=0, sticky="w", pady=1)
       
#define func buttons
def display():
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, padx = 10, pady = 0, rowspan = 6, columnspan = 6, sticky="n")
    
    
     
    with open("records.csv", "r", newline='') as records:
        records_reader = csv.reader(records)
        data = list(records_reader)
        display_label = Label(frame, text="List of Students", bg="mint cream", font=("Helvetica", 15, "bold"))
        display_label.grid(row=0, column=2, padx = 5, pady= 5, sticky="w", columnspan=2)
       
    for i in range(len(data)):
        for j in range(5):
            try:
                if i == 0:
                    if j==1  or j==4:
                        e = Entry(frame, width=30, fg='black', font=('Helvetica',12)) 
                        e.grid(row=i+1, column=j) 
                        e.insert(END, data[i][j])
                    else:
                        e = Entry(frame, width=15, fg='black', font=('Helvetica',12)) 
                        e.grid(row=i+1, column=j) 
                        e.insert(END, data[i][j])
                    
                elif i != 0:
                    e = Entry(frame, width=15, fg='black', font=('Helvetica',12, 'bold')) 
                    e.grid(row=i+1, column=j) 
                    e.insert(END, data[i][j].upper())
                    if j==1  or j==4:
                        e = Entry(frame, width=30, fg='black', font=('Helvetica',12, 'bold')) 
                        e.grid(row=i+1, column=j) 
                        e.insert(END, data[i][j].upper())
            except:
                pass
       
def addStudent():  
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, padx = 143, rowspan = 7, columnspan=6, sticky="n")

    func_title = Label(frame, text="Add Student", fg='black', font=('Helvetica',20,"bold"), bg="mint cream")
    func_title.grid(row=0, column=0, padx=5, pady=10)

    e_id = Entry(frame, width=80, borderwidth=2)
    e_id.grid(row=1, column=1, padx=20, pady=20)
    id_lbl = Label(frame, text="ID Number:", font=("Helvetica", 12), bg="mint cream").grid(row=1, column=0, padx=10, pady=20, sticky='e')

    e_name = Entry(frame,  width=80, borderwidth=2)
    e_name.grid(row=2, column=1, padx=20, pady=20)
    name_lbl = Label(frame, text="Name:", font=("Helvetica", 12), bg="mint cream").grid(row=2, column=0, padx=10, pady=20, sticky='e')

    e_gender = Entry(frame,  width=80, borderwidth=2)
    e_gender.grid(row=3, column=1, padx=20, pady=20)
    gender_lbl = Label(frame, text="Gender:", font=("Helvetica", 12), bg="mint cream").grid(row=3, column=0, padx=10, pady=20, sticky='e')

    e_year = Entry(frame,  width=80, borderwidth=2)
    e_year.grid(row=4, column=1, padx=20, pady=20)
    year_lbl = Label(frame, text="Year:", font=("Helvetica", 12), bg="mint cream").grid(row=4, column=0, padx=10, pady=20, sticky='e')

    e_course = Entry(frame,  width=80, borderwidth=2)
    e_course.grid(row=5, column=1, padx=20, pady=20)
    course_lbl = Label(frame, text="Course:", font=("Helvetica", 12), bg="mint cream").grid(row=5, column=0, padx=10, pady=20, sticky='e')

    def get_data():
    
        id_num = e_id.get()
        name = e_name.get()
        gender = e_gender.get()
        year = e_year.get()
        course = e_course.get()
        data = [id_num, name, gender, year, course]
        for var in data:
            if var == '':
                messagebox.showerror("Error", "Data incomplete, complete data to proceed!")
                run = False
                break
            
            else:
                run = True

        if check_ID(data[0]) == False:
                messagebox.showerror("Error", 'Invalid ID format must be in this format e.g "2019-0001"')
                run = False 
        elif run:
            e_id.delete(0,END)
            e_name.delete(0,END)
            e_gender.delete(0,END)
            e_year.delete(0,END)
            e_course.delete(0,END)

            messagebox.showinfo("Information", "Added!")

            with open("records.csv", "a+", newline='') as records:
                writer = csv.writer(records)
                writer.writerow(data)
            
    add_button = Button(frame, text="Add Student", padx=30, pady=10, borderwidth=2, bg='royal blue1', fg="white", font=("Helvetica", 12, "bold"), command=get_data)
    add_button.grid(row=6, column=1, padx=20, pady=30, sticky="e")

#search the key (ID number to see the edit and delete button) 
def search():
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, padx= 25, rowspan = 3, columnspan=6, sticky="n")

    func_title = Label(frame, text="Search Student", fg='black', font=('Helvetica',20,"bold"), bg="mint cream")
    func_title.grid(row=0, column=0, padx=10, pady=20)

    e_id = Entry(frame, width=110, borderwidth=2)
    e_id.grid(row = 1, column = 1, columnspan =3, padx=20, pady=20)
    e_id_lbl = Label(frame, text="Student ID number: ", font=("Helvetica", 12), bg="mint cream")
    e_id_lbl.grid(row = 1, column = 0, padx=10, pady=20, sticky='e')

    def get_data():
        try:
            res_frame.destroy()
        except:
            pass
        key = e_id.get()
        e_id.delete(0,END)
        count = 0
        if check_ID(key):
            res_frame = LabelFrame(frame, padx=6, pady=10, bg='mint cream', borderwidth='0')
            res_frame.grid(row=3, column=0, columnspan=5, sticky='we')
            res_label = Label(res_frame, text="Result:", font=("Helvetica", 15, "bold"),bg='mint cream')
            res_label.grid(row=0, column=0, padx = 5, pady= 5, sticky="w")
        
            with open("records.csv", 'r', newline='') as records:
                
                reader = csv.reader(records)
                for data in reader:
                    if data[0] == key:
                        count +=1
                        label = ['ID number','Student Name','Gender','Year','Course']
                        for i in range(1):
                            for j in range(5):
                                if i == 0:
                                    if j==1  or j==4:
                                        e = Entry(res_frame, width=27, fg='black', font=('Helvetica',12)) 
                                        e.grid(row=i+1, column=j) 
                                        e.insert(END, label[j])
                                    else:
                                        e = Entry(res_frame, width=15, fg='black', font=('Helvetica',12)) 
                                        e.grid(row=i+1, column=j) 
                                        e.insert(END, label[j])

                        #instead of using a loop, each cell is stored in a unique var for editing data purposes                         
                        e_ID = Entry(res_frame, width=15, fg='black', font=('Helvetica',12, 'bold')) 
                        e_name = Entry(res_frame, width=27, fg='black', font=('Helvetica',12, 'bold')) 
                        e_gender = Entry(res_frame, width=15, fg='black', font=('Helvetica',12, 'bold'))
                        e_year = Entry(res_frame, width=15, fg='black', font=('Helvetica',12, 'bold'))  
                        e_course = Entry(res_frame, width=27, fg='black', font=('Helvetica',12, 'bold'))

                        e_ID.grid(row=2, column=0)
                        e_name.grid(row=2, column=1)
                        e_gender.grid(row=2, column=2)
                        e_year.grid(row=2, column=3)
                        e_course.grid(row=2, column=4)

                        e_ID.insert(END, data[0].upper())
                        e_name.insert(END, data[1].upper())
                        e_gender.insert(END, data[2].upper())
                        e_year.insert(END, data[3].upper())
                        e_course.insert(END, data[4].upper())          
                        break
            
    
            edit_button = Button(res_frame, text="Edit Student", padx =20, pady = 10, borderwidth = "2", bg='royal blue1',fg='white', font=("Helvetica", 12, "bold"), command=lambda: edit(e_ID,e_name,e_gender, e_year,e_course))
            edit_button.grid(row=4, column=4, pady = 10)

            del_button = Button(res_frame, text="Delete Student", padx =10, pady = 10, borderwidth = "2", bg='antique white', font=("Helvetica", 11, "bold"), command=lambda: delete(e_ID,e_name,e_gender, e_year,e_course))
            del_button.grid(row=4, column=3, pady = 10)

            edit_tip = Label(res_frame, text="Tip: Change data and click edit button to update student's data", font=("Helvetica", 10, "bold"))
            edit_tip.grid(row=4, column=0, columnspan = 3, padx = 5, pady= 5, sticky="w")
        
        
        if count == 0:
            if check_ID(key) == False:
                try:
                    res_frame.destroy()
                except:
                    pass
                messagebox.showerror('Invalid ID Number', "Invalid ID format must be- e.g '2019-0001'")
            else:
                try:
                    res_frame.destroy()
                except:
                    pass
                messagebox.showerror('ID Number not found', "ID number '{}' is not in the records!".format(key))        

    e_button = Button(frame, text="Search", padx=30, pady=20, borderwidth=2, bg="royal blue1",font=('Helvetica', 12, 'bold'),fg='white', command=get_data)
    e_button.grid(row=2, column=3, sticky="e", padx= 40, pady=20)    
#if ID number is edited it will be added as new student and not override the current student data                      
def edit(id, name, gender, year, course):
   
    new_data = [id.get(), name.get(), gender.get(), year.get(), course.get()]
                
    with open("records.csv","r", newline='') as records:
        reader = csv.reader(records)
        lst  =list(reader)

        with open("records.csv","w", newline='') as records:
            writer = csv.writer(records)
            
            for data in lst:
                try:
                    if data[0] != new_data[0]:
                        writer.writerow(data)
                except:
                    pass
            writer.writerow(new_data)     
    messagebox.showinfo("Updated", "Student data is updated!")

def delete(id, name, gender, year, course):
    
    with open("records.csv","r", newline='') as records:
        reader = csv.reader(records)
        lst  =list(reader)

        with open("records.csv","w", newline='') as records:
            writer = csv.writer(records)
            
            for data in lst:
                try:
                    if data[0] != id.get():
                        writer.writerow(data)
                except:
                    pass
    id.delete(0,END)
    name.delete(0,END)
    gender.delete(0,END)
    year.delete(0,END)
    course.delete(0,END)

    messagebox.showinfo("Deleted", "Student deleted")
def frame_destroy():
    frame.destroy()
def frame_update():
    global frame
    frame = LabelFrame(mainframe, bg="mint cream", borderwidth=5)
def check_ID(key):
    pattern = re.compile(r'\d\d\d\d-\d\d\d\d')
    res = re.fullmatch(pattern, key)
    if res:
        return True
    else:
        return False

layout()

window.mainloop()