from tkinter import *
from tkinter import messagebox as ms
import sqlite3

class login:
    def __init__(self,window, advance, tipo, nombre, telefono):
        self.window = window
        self.window.title("Nanny")
        self.advance = advance
        self.tipo = tipo
        self.nombre = nombre
        self.telefono = telefono
        self.username = StringVar()
        self.password = StringVar()
        self.numero = StringVar()
        self.user_type = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.n_numero = StringVar()
        self.n_user_type = StringVar()
        self.widgets()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect('quit.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, (parameters, ))
            conn.commit()
        return result

    def login(self):
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if result:
            query = ('SELECT * FROM user WHERE username = ?')
            self.tipo = self.run_query(query, self.username.get())
            for row in self.tipo:
                self.tipo = row[3]
                self.telefono = row[2]
                self.nombre = row[0]
            self.logf.destroy()
            self.head.destroy()
            self.window.destroy()
            self.advance = True
        else:
            ms.showerror('Oops!','Username or password incorrect.')
            
    def new_user(self):
    	
        with sqlite3.connect('quit.db') as db:
            c = db.cursor()

        find_user = ('SELECT username FROM user WHERE username = ?')
        c.execute(find_user,[(self.n_username.get())])        
        if c.fetchall():
            ms.showerror('Error!','Username Taken Try a Different One.')
        else:
            find_numero = ('SELECT numero FROM user WHERE numero = ?')
            c.execute(find_numero,[(self.n_numero.get())])
            if c.fetchall():
                ms.showerror('Error!','Number Taken Try a Different One')
            else:
                ms.showinfo('Success!','Account Created!')
                self.log()
                insert = 'INSERT INTO user(username,password,numero,user_type) VALUES(?,?,?,?)'
                c.execute(insert,[(self.n_username.get()),(self.n_password.get()),(self.n_numero.get()),(self.n_user_type.get())])
                db.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.n_numero.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()
        
    def widgets(self):
        self.head = Label(self.window,text = 'LOGIN',font = ('',15),pady = 10)
        self.head.pack()
        self.logf = Frame(self.window,padx =10,pady = 10)

        Label(self.logf, text = 'Username: ', font = ('',10), pady=5,padx=5).grid(sticky = W)
        Entry(self.logf, textvariable = self.username, bd = 5, font = ('',15)).grid(row=0, column=1)

        Label(self.logf, text = 'Password: ', font = ('',10), pady=5, padx=5).grid(sticky = W)
        Entry(self.logf, textvariable = self.password, bd = 5, font = ('',15), show = '*').grid(row=1, column=1)

        Button(self.logf, text = ' Login ',bd = 3 , font = ('',10), command=self.login).grid(row = 2, column=1, sticky = W + E)
        Button(self.logf, text = ' Create Account ', bd = 3 , font = ('',10), command=self.cr).grid(row = 3, column = 1, sticky = W + E)
        self.logf.pack()
        
        self.crf = Frame(self.window, padx =10, pady = 10)
        Label(self.crf, text = 'Username: ', font = ('',10),pady=5, padx=5).grid(sticky = W)
        Entry(self.crf, textvariable = self.n_username, bd = 5, font = ('', 15)).grid(row=0, column=1)

        Label(self.crf, text = 'Password: ', font = ('',10), pady=5, padx=5).grid(sticky = W)
        Entry(self.crf, textvariable = self.n_password, bd = 5, font = ('', 15), show = '*').grid(row=1, column=1)

        Label(self.crf, text = 'Numero: ', font = ('',10), pady=5, padx=5).grid(sticky = W)
        Entry(self.crf, textvariable = self.n_numero, bd = 5, font = ('', 15)).grid(row=2, column=1)

        Label(self.crf, text = 'Tipo de Usuario: ', font = ('',10), pady=5, padx=5).grid(sticky = W)
        OptionMenu(self.crf, self.n_user_type, "Cliente", "Cuidador").grid(row=3, column=1)

        Button(self.crf, text = 'Create Account', bd = 3 , font = ('', 10), padx=5, pady=5, command=self.new_user).grid(row = 4, column = 1, sticky = W + E)
        Button(self.crf, text = 'Return to login', bd = 3 , font = ('', 10), padx=5, pady=5, command=self.log).grid(row=5,column=1, sticky = W + E)