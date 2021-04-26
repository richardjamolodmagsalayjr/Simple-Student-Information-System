from tkinter import *
from PIL import ImageTk,Image
import csv
from tkinter import messagebox
import re

root = Tk()
root.title("Student Information System")
root.geometry("1228x720")
root.configure(bg="#EEEEEE")
root.iconbitmap("images/app_icon.ico")

def frame_destroy():
    frame.destroy()

def frame_update():
    global frame
    frame = LabelFrame(main_frame, bg="#F0F0F0", borderwidth=1.5)

def check_ID(key):
    pattern = re.compile(r'\d\d\d\d-\d\d\d\d')
    res = re.fullmatch(pattern, key)
    if res:
        return True
    else:
        return False

def unique_ID(ID):
    with open("records.csv", "r") as records:
        reader = csv.reader(records)
        for data in reader:
            if data[0] == ID:
                return False
    return True

def display():
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, rowspan = 6, columnspan = 6, sticky="n")
    
    with open("records.csv", "r", newline='') as records:
        records_reader = csv.reader(records)
        data = list(records_reader)
        display_label = Label(frame, text="List of Students", bg="#EEEEEE", font=("Helvetica", 15, "bold"))
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
    frame.grid(row=1, column=1, rowspan = 7, columnspan=6, sticky="n")

    func_title = Label(frame, text="Add Student", fg='black', font=('Open Sans',20,"bold"), bg="#F0F0F0")
    func_title.grid(row=0, column=0, padx=5, pady=10)

    e_id = Entry(frame, width=80, borderwidth=2)
    e_id.grid(row=1, column=1, padx=20, pady=20)
    id_lbl = Label(frame, text="ID Number:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=20, sticky='w')

    e_name = Entry(frame,  width=80, borderwidth=2)
    e_name.grid(row=2, column=1, padx=20, pady=20)
    name_lbl = Label(frame, text="Name:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=20, sticky='w')

    e_gender = Entry(frame,  width=80, borderwidth=2)
    e_gender.grid(row=3, column=1, padx=20, pady=20)
    gender_lbl = Label(frame, text="Gender:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=3, column=0, padx=10, pady=20, sticky='w')

    e_year = Entry(frame,  width=80, borderwidth=2)
    e_year.grid(row=4, column=1, padx=20, pady=20)
    year_lbl = Label(frame, text="Year:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=4, column=0, padx=10, pady=20, sticky='w')

    e_course = Entry(frame,  width=80, borderwidth=2)
    e_course.grid(row=5, column=1, padx=20, pady=20)
    course_lbl = Label(frame, text="Course:", font=("Open Sans", 12), bg="#F0F0F0").grid(row=5, column=0, padx=10, pady=20, sticky='w')

    def get_data():
       
        id_num = e_id.get()
        name = e_name.get()
        gender = e_gender.get()
        year = e_year.get()
        course = e_course.get()
        data = [id_num, name.upper(), gender.upper(), year.upper(), course.upper()]

        if unique_ID(id_num):
            for var in data:
                if var == '':
                    messagebox.showerror("Error", "Data incomplete, complete data to proceed!")
                    run = False
                    break
            
                else:
                    run = True

            if check_ID(data[0]) == False: #checks if the id's format is valid
                    messagebox.showerror("Error", 'Invalid ID format must be in this format e.g "2019-0001"')
                    run = False 

            elif run:           #delete the entries if inputs are valid
                e_id.delete(0,END)
                e_name.delete(0,END)
                e_gender.delete(0,END)
                e_year.delete(0,END)
                e_course.delete(0,END)

                messagebox.showinfo("Student Added", "Added!")

                with open("records.csv", "a+", newline='') as records:
                    writer = csv.writer(records)
                    writer.writerow(data)
        else:
            messagebox.showinfo("Invalid", "ID number is already used!")

    add_button = Button(frame, text="Add Student", padx=30, pady=10, borderwidth=2, bg='royal blue1', fg="white", font=("Helvetica", 12, "bold"), command=get_data)
    add_button.grid(row=6, column=1, padx=20, pady=30, sticky="e")

#search the key (ID number to see the edit and delete button) 
def search():
    frame_destroy()
    frame_update()
    frame.grid(row=1, column=1, rowspan = 3, columnspan=6, sticky="n")

    func_title = Label(frame, text="Search Student", fg='black', font=('Open Sans',20,"bold"), bg="#f0f0f0")
    func_title.grid(row=0, column=0, padx=10, pady=20)

    e_id = Entry(frame, width=100, borderwidth=2)
    e_id.grid(row = 1, column = 1, columnspan =3, padx=25, pady=20)
    e_id_lbl = Label(frame, text="Student ID number: ", font=('Open Sans',16,"bold"), bg="#f0f0f0")
    e_id_lbl.grid(row = 1, column = 0, padx=10, pady=20, sticky='e')

    def get_data():
        try:
            res_frame.destroy()
        except:
            pass
        key = e_id.get()
        e_id.delete(0,END)
        count = 0
        if check_ID(key) == False:
            messagebox.showerror('Invalid ID Number', "Invalid ID format must be- e.g '2019-0001'")

        elif check_ID(key):
            res_frame = LabelFrame(frame, padx=6, pady=10, bg='#f0f0f0', borderwidth='0')
            res_frame.grid(row=3, column=0, columnspan=5, sticky='we')

            id_label = Label(res_frame, text="")
        
            with open("records.csv", 'r', newline='') as records:
                reader = csv.reader(records)
                read = list(reader)     #put it in a list to close the r file 
            for data in read:
                try:
                    if data[0] == key:
                        label = ['Student Name','Gender','Year','Course']

                        res_frame = LabelFrame(frame, padx=6, pady=10, bg='#f0f0f0', borderwidth='0')
                        res_frame.grid(row=3, column=0, columnspan=5, sticky='we')

                        res_label = Label(res_frame, text="Result:", font=("Open Sans", 15, "bold"),bg='#f0f0f0')
                        res_label.grid(row=0, column=0, padx = 5, pady= 5, sticky="w")

                        id_label = Label(res_frame, text= "{}: {}".format("ID number", data[0]), font=("Open Sans", 10, "bold"), bg="#f0f0f0")
                        id_label.grid(row=1, column=0, padx = 5, pady = 5, sticky="w")

                        count +=1 #increment count if search is successful else prompt will pop up if none
                      

                        for i in range(1): #
                            for j in range(0,4):
                                if j==0  or j==3:
                                    e = Entry(res_frame, width=27, fg='black', font=('Open Sans',12), borderwidth="1") 
                                    e.grid(row=i+2, column=j) 
                                    e.insert(END, label[j])
                                else:
                                    e = Entry(res_frame, width=20, fg='black', font=('Open Sans',12), borderwidth="1") 
                                    e.grid(row=i+2, column=j) 
                                    e.insert(END, label[j])

                        #instead of using a loop, each cell is stored in a unique var for editing data purposes                         
                        e_ID = data[0]
                        e_name = Entry(res_frame, width=27, fg='black', font=('Open Sans',12, 'bold'), borderwidth="1") 
                        e_gender = Entry(res_frame, width=20, fg='black', font=('Open Sans',12, 'bold'), borderwidth="1")
                        e_year = Entry(res_frame, width=20, fg='black', font=('Open Sans',12, 'bold'), borderwidth="1")  
                        e_course = Entry(res_frame, width=27, fg='black', font=('Open Sans',12, 'bold'), borderwidth="1")

                        e_name.grid(row=3, column=0)
                        e_gender.grid(row=3, column=1)
                        e_year.grid(row=3, column=2)
                        e_course.grid(row=3, column=3)

                        
                        e_name.insert(END, data[1].upper())
                        e_gender.insert(END, data[2].upper())
                        e_year.insert(END, data[3].upper())
                        e_course.insert(END, data[4].upper())          
                       
                        edit_button = Button(res_frame, text="Edit Student", padx =20, pady = 10, borderwidth = "2", bg='royal blue1',fg='white', font=("Open Sans", 8, "bold"), command=lambda: edit(e_ID,e_name,e_gender, e_year,e_course))
                        edit_button.grid(row=4, column=3, pady = 10)

                        del_button = Button(res_frame, text="Delete Student", padx =18, pady = 10, borderwidth = "2", bg='#CEBFA2', font=("Open Sans", 8, "bold"), command=lambda: delete(e_ID,e_name,e_gender, e_year,e_course))
                        del_button.grid(row=4, column=2, pady = 10)

                        edit_tip = Label(res_frame, text="Tip: Change data and click edit button to update student's data", font=("Helvetica", 10, "bold"))
                        edit_tip.grid(row=4, column=0, columnspan = 3, padx = 5, pady= 5, sticky="w")
                        break

                except:
                    pass
            if count == 0:
                try:
                    res_frame.destroy()
                except:
                    pass
                messagebox.showerror('ID Number not found', "ID number '{}' is not in the records!".format(key)) 
    
    search_button = Button(frame, text="Search", padx=30, pady=20, borderwidth=2, bg="royal blue1",font=('Helvetica', 12, 'bold'),fg='white', command=get_data)      
    search_button.grid(row=2, column=3, sticky="e", padx= 40, pady=20)  

#if ID number is edited it will be added as new student and not override the current student data                      
def edit(ID, name, gender, year, course):
   
    new_data = [ID, name.get(), gender.get(), year.get(), course.get()]
                
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

def delete(ID, name, gender, year, course):
    
    with open("records.csv","r", newline='') as records:
        reader = csv.reader(records)
        lst  =list(reader)

        with open("records.csv","w", newline='') as records:
            writer = csv.writer(records)
            
            for data in lst:
                try:
                    if data[0] != ID:
                        writer.writerow(data)
                except:
                    pass
    
    name.delete(0,END)
    gender.delete(0,END)
    year.delete(0,END)
    course.delete(0,END)

    try: #use try exception since res_frame is not initialized or defined within this function, destroy only if necessary
        res_frame.destroy()
    except:
        pass

    messagebox.showinfo("Deleted", "Student deleted")



#use image coffee.jpg as root background
bg = ImageTk.PhotoImage(Image.open("images/coffee.jpg"))
bg_lbl = Label(root, image = bg )
bg_lbl.grid(row=1, column=1)

#frames
sidebar = LabelFrame(root, bg = "#EEEEEE", borderwidth = 2)
header = LabelFrame(root, bg= "#828284", borderwidth = 1.5)
main_frame = LabelFrame(root, bg = '#F0F0F0', borderwidth= 0)
frame = LabelFrame(main_frame, bg="#F0F0F0", borderwidth=1.5) #frame to be destroy 

#grid bar
sidebar.grid(row=1, column=0, sticky="ns")
header.grid(row=0, column=0, columnspan=2, sticky = "we")
main_frame.grid(row=1, column=1, sticky = 'n', pady = 50)

#title in located at the header
title = Label(header, text='Student Information System', font=("Open Sans", 17, "bold"), bg="#828284", fg="white", padx = 50, pady=20)
title.grid(row=0, column = 0)

#button icons

icon_1  = ImageTk.PhotoImage(Image.open("images/list_icon.png"))
icon_lbl_1 = Label(sidebar, image=icon_1)
icon_lbl_1.grid(row=0, column=0, pady=(50,0))

icon_2  = ImageTk.PhotoImage(Image.open("images/add_icon.png"))
icon_lbl_2 = Label(sidebar, image=icon_2)
icon_lbl_2.grid(row=2, column=0, pady=(50,0))

icon_3  = ImageTk.PhotoImage(Image.open("images/search_icon.png"))
icon_lbl_3 = Label(sidebar, image=icon_3)
icon_lbl_3.grid(row=4, column=0, pady=(50,0))

display_button = Button(sidebar, text="Display\nStudents",  padx = 30, bg='#EEEEEE', font=("Open Sans", 12, "bold"), borderwidth = 0, command=display) 
add_button = Button(sidebar, text="Add\nStudent",  bg='#EEEEEE', padx = 30,font=("Open Sans", 12, "bold"), borderwidth = 0, command=addStudent)
search_button = Button(sidebar, text="Search\nStudent", bg='#EEEEEE', padx = 30, font=("Open Sans", 12, "bold"), borderwidth = 0, command = search)

display_button.grid(row=1, column=0)
add_button.grid(row=3, column=0)
search_button.grid(row=5, column=0)



root.mainloop()



