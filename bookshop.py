from tkinter import *
from time import strftime
from tkinter import ttk, messagebox
from database import Database

db = Database('database.db')

root = Tk()
root.title("Book Shop Manger")
root.geometry("1300x600+0+0")
photo = PhotoImage(file="favicon.png")
root.iconphoto(False, photo)

#****************Frames*******************
lefttop = Frame(root)
lefttop.grid(row=0, column=0, padx=20,  pady=10, sticky=NW)

righttop = Frame(root)
righttop.grid(row=0, column=1, sticky=NW)

timerFrame = Frame(root)
timerFrame.grid(row=0, column=2, sticky=NE)

bottum = Frame(root, padx=20)
bottum.grid(row=1, column=0, columnspan=3)

#*****************Variables******************
bookname = StringVar()
publication = StringVar()
author = StringVar()
price = StringVar()
availability = StringVar()
quantity = StringVar()
comment = StringVar()
num = 0

#***************Functions*********************
def details():
    table.delete(*table.get_children())
    for row in db.fetch():
        table.insert('', END, values=row)

def selectItem(event):
    curItem = table.focus()
    content = table.item(curItem)
    data = content['values']

    bookEntry.delete(0, END)
    bookEntry.insert(END, data[0])
    quantityEntry.delete(0, END)
    quantityEntry.insert(END, data[5])
    authorEntry.delete(0, END)
    authorEntry.insert(END, data[2])
    priceEntry.delete(0, END)
    priceEntry.insert(END, data[3])
    availabilityEntry.delete(0, END)
    availabilityEntry.insert(END, data[4])
    publicationEntry.delete(0, END)
    publicationEntry.insert(END, data[1])
    commentEntry.delete(0, END)
    commentEntry.insert(END, data[6])

    for row in db.match():
        if data[0]==row[1] and data[1]==row[2] and data[2]==row[3] and data[3]==row[4] and data[4]==row[5] and data[5]==row[6] and data[6]==row[7]:
            global num
            num=row[0]
            
def add():
    fields={'Book Name':bookname.get(), 'Publication':publication.get(), 'Author':author.get(), 'Price':price.get(), 'Availability':availability.get(), 'Quantity':quantity.get()}
    for i in fields:
        if fields[i] == '':
            messagebox.showinfo('Error',i+' field is required !!')
            break
    if bookname.get()!='' and publication.get()!='' and author.get()!='' and price.get()!='' and availability.get()!='' and quantity!='':
        if price.get().isdigit() == False:
                messagebox.showinfo('Error', 'Enter Price !!')
        elif quantity.get().isdigit() == False:
                messagebox.showinfo('Error', 'Enter Quantity !!')
        else:
            entities = (bookname.get(), publication.get(), author.get(), price.get(), availability.get(), quantity.get(), comment.get())
            db.insert(entities)
            details()
            clear()

def update():
    global num
    if num > 0:
        fields={'Book Name':bookname.get(), 'Publication':publication.get(), 'Author':author.get(), 'Price':price.get(), 'Availability':availability.get(), 'Quantity':quantity.get()}
        for i in fields:
            if fields[i] == '':
                messagebox.showinfo('Error',i+' field is required !!')
                break
        if bookname.get()!='' and publication.get()!='' and author.get()!='' and price.get()!='' and availability.get()!='' and quantity!='':
            if price.get().isdigit() == False:
                    messagebox.showinfo('Error', 'Enter Price !!')
            elif quantity.get().isdigit() == False:
                    messagebox.showinfo('Error', 'Enter Quantity !!')
            else:
                db.update(bookname.get(), publication.get(), author.get(), price.get(), availability.get(), quantity.get(), comment.get(), num)
                details()
                clear()
                num = 0
    else:
        messagebox.showinfo('Error', 'Select proper record !!')

def deleteBtn():
    global num
    warning = messagebox.askyesno('Warning!', 'Do you want to delete?')
    if warning == True:
        db.delete(num)
        details()
        clear()
        num = 0

def delete(event):
    global num
    warning = messagebox.askyesno('Warning!', 'Do you want to delete?')
    if warning == True:
        db.delete(num)
        details()
        clear()
        num = 0

def clear():
    bookEntry.delete(0, END)
    quantityEntry.delete(0, END)
    authorEntry.delete(0, END)
    priceEntry.delete(0, END)
    availabilityEntry.delete(0, END)
    publicationEntry.delete(0, END)
    commentEntry.delete(0, END)
    searchEntry.delete(0, END)
    bookEntry.focus_set()
    availabilityEntry.set('')

def search():
    if searchbyEntry.get()=='':
        messagebox.showerror('Error', 'Select proper field !!')
    elif searchEntry.get()=='':
        messagebox.showerror('Error', 'Enter something !!')
    elif searchbyEntry.get() == 'Book Name':
        rows = db.search(searchEntry.get().lower()+'%', None, None)
        table.delete(*table.get_children())
        if len(rows) != 0:
            for row in rows:
                table.insert('', END, values=row)
        else:
            messagebox.showerror('Error', searchEntry.get()+' is not found!')
            
    elif searchbyEntry.get() == 'Author':
        rows = db.search(None, None, searchEntry.get().lower()+'%')
        table.delete(*table.get_children())
        if len(rows) != 0:
            for row in rows:
                table.insert('', END, values=row)
        else:
            messagebox.showerror('Error', searchEntry.get()+' is not found!')

    elif searchbyEntry.get() == 'Publication':
        rows = db.search(None, searchEntry.get().lower()+'%', None)
        table.delete(*table.get_children())
        if len(rows) != 0:
            for row in rows:
                table.insert('', END, values=row)
        else:
            messagebox.showerror('Error', searchEntry.get()+' is not found!') 
        
def timer():
    clock = strftime("%a %d/%m/%y \n%H:%M:%S %p")
    timeLabel.config(text=clock)
    timeLabel.after(1000, timer)
    
#*****************Enteries*******************
bookLabel = Label(lefttop, text="Book Name :")
bookLabel.grid(row=0, column=0, pady=10, padx=10)
bookEntry = Entry(lefttop, textvariable=bookname)
bookEntry.grid(row=0, column=1)

quantityLabel = Label(lefttop, text="Quantity :")
quantityLabel.grid(row=0, column=2, pady=10, padx=10)
quantityEntry = Entry(lefttop, textvariable=quantity)
quantityEntry.grid(row=0, column=3)

publicationLabel = Label(lefttop, text="Publication :")
publicationLabel.grid(row=1, column=0, pady=10)
publicationEntry = Entry(lefttop, textvariable=publication)
publicationEntry.grid(row=1, column=1)

availabilityLabel = Label(lefttop, text="Availability :")
availabilityLabel.grid(row=1, column=2, pady=10)
availabilityEntry = ttk.Combobox(lefttop, textvariable=availability, state='readonly', width=17)
availabilityEntry['values'] = ('Yes', 'No')
availabilityEntry.grid(row=1, column=3)

authorLabel = Label(lefttop, text="Author :")
authorLabel.grid(row=2, column=0, pady=10)
authorEntry = Entry(lefttop, textvariable=author)
authorEntry.grid(row=2, column=1)

priceLabel = Label(lefttop, text="Price :")
priceLabel.grid(row=2, column=2, pady=10)
priceEntry = Entry(lefttop, textvariable=price)
priceEntry.grid(row=2, column=3 )

commentLabel = Label(lefttop, text="Comment :")
commentLabel.grid(row=3, column=0, pady=10)
commentEntry = Entry(lefttop, textvariable=comment, width=57)
commentEntry.grid(row=3, column=1, columnspan=3)

#***************Buttons**************************
addBtn = Button(lefttop, text="ADD", command=add).grid(row=4, column=0, ipadx=20)
updateBtn = Button(lefttop, text="UPDATE", command=update).grid(row=4, column=1, ipadx=20)
deleteBtn = Button(lefttop, text="DELETE", command=deleteBtn).grid(row=4, column=2, ipadx=20)
clearBtn = Button(lefttop, text="CLEAR", command=clear).grid(row=4, column=3, ipadx=20)

#*****************SearchBar********************
searchLabel = Label(righttop, text="Search By :", font = ('calibri', 15, 'bold'))
searchLabel.grid(row=0, column=0)
searchbyEntry = ttk.Combobox(righttop, state='readonly', width=15)
searchbyEntry['values'] = ('Book Name', 'Author', 'Publication')
searchbyEntry.grid(row=0, column=1, padx=10)

searchEntry = Entry(righttop)
searchEntry.grid(row=0, column=2, ipadx=40)

searchBtn = Button(righttop, text="Search", command=search)
searchBtn.grid(row=0, column=3, padx=10, ipadx=10)
showallBtn = Button(righttop, text="Show All", command=details)
showallBtn.grid(row=0, column=4, ipadx=10, pady=30)

#****************Timer**************************
timeLabel = Label(timerFrame, font = ('calibri', 12, 'bold'))
timeLabel.grid(sticky=NE, padx=5)
timer()

#***************Details**********************
table = ttk.Treeview(bottum,  columns=('bookname','publication','author','price','availability','quantity','comment'))
scrollbar = ttk.Scrollbar(bottum, orient=VERTICAL, command=table.yview)
scrollbar.pack(side=RIGHT, fill=Y)
table.configure(yscrollcommand=scrollbar.set)
table.heading("bookname", text="Book Name")
table.heading("author", text="Author")
table.heading("price", text="Price")
table.heading("publication", text="Publication")
table.heading("availability", text="Availability")
table.heading("quantity", text="Quantity")
table.heading("comment", text="Comment")
table.column("bookname", width=100)
table.column("author", width=50)
table.column("price", width=50)
table.column("publication", width=100)
table.column("availability", width=50)
table.column("quantity", width=50)
table.column("comment", width=200)
table['show'] = 'headings'
table.pack(ipadx=325, ipady=70)
details()
table.bind('<<TreeviewSelect>>', selectItem)
table.bind('<Delete>', delete)

root.mainloop()
