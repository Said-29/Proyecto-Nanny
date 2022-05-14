from calendar import calendar
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
import sqlite3
from Nanny.Login import login
from tkcalendar import *

class Cuidador():
    #Bases de datos y variables necesitadas
    database = 'database.db'
    personal_db = 'quit.db'
    id_num = 0
    numero = ''

    def __init__(self, window, nombre, numero):
        global id_num
        #Crear ventana y nombrarla
        self.window = window
        self.window.title('Nanny Cuidador')

        #Nombre y numero de telefono del usuario
        self.nombre = nombre 
        self.numero = numero
        self.selected = ()

        #Frame donde estaran todos los widgets
        frame = Frame(self.window)
        frame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        #Tabla de datos en forma de arbol
        self.tree = ttk.Treeview(height = 10, columns=("#0","#1","#2","#3","#4"))
        self.tree.grid(row = 4, column = 0, columnspan = 1)
        self.tree.heading('#0', text = 'Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Dia', anchor = CENTER)
        self.tree.heading('#2', text = 'Amount of kids', anchor = CENTER)
        self.tree.heading('#3', text = 'From', anchor = CENTER)
        self.tree.heading('#4', text = 'To', anchor = CENTER)
        self.tree.heading('#5', text = 'Special Care', anchor = CENTER)

        #Botones para aceptar oferta, o refrescar las ofertas
        ttk.Button(self.window, text = 'ACCEPT', command=lambda: [self.accept(), self.Update(), self.get_products()]).grid(row = 5, column = 0, columnspan = 1, sticky = W + E)
        ttk.Button(self.window, text = 'REFRESH', command=self.get_products).grid(row = 5, column = 1, columnspan = 2, sticky = W + E)

        #Barra de scroll para cuando se llene la pagina de ordenes
        scroll = ttk.Scrollbar(self.window, orient = VERTICAL, command= self.tree.yview)
        self.tree['yscroll'] = scroll.set
        self.tree.grid(in_=frame, row=0, column=0, sticky=NSEW)
        scroll.grid(in_=frame, row=0, column=2, sticky=NS)
        
        #Llenar la pagina de datos
        self.get_products()
    
    #Funcion para hacer cualquier accion dentro de la base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    #Obtener todos los datos de la base de datos, y ordenarlos por id
    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = 'SELECT * FROM ordenes ORDER BY id DESC'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[8] == "Yes":
                pass
            else:
                self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4], row[5]))

    #Funcion del boton aceptar, acepta la orden y manda los datos del cliente, si la orden ya ha sido aceptada envia un mensaje
    #y refresca la pagina, ademas de enviarle los datos al cliente
    def accept(self):
        global id_num, numero
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            ms.showerror('Error!', 'Please select an order')
            return
        self.selected = self.tree.item(self.tree.selection())
        nombre = self.tree.item(self.tree.focus())
        query = f'SELECT * FROM ordenes'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[0] == nombre.get("text") and row[8] == 'No':
                numero = row[7]
                break
        code = f"{nombre.get('text')[0]}{nombre.get('values')[0][3]}{str(nombre.get('values')[1])}{nombre.get('values')[2][1]}{nombre.get('values')[3][1]}{nombre.get('values')[4][0]}{numero[-4:]}"
        query = f'SELECT * FROM ordenes WHERE code = "{code}"'
        db_rows = self.run_query(query)
        for row in db_rows:
            if row[0] == nombre.get("text") and row[8] == 'No':
                ms.showinfo('Detalles', f'Nombre: {nombre.get("text")}\nNumero de telefono: {row[7]}')
                id_num = row[6]
                break
    
    #Funcion para eliminar alguna orden la base de datos
    def Update(self):
        global id_num
        query = 'UPDATE ordenes SET accepted = "Yes", nombre_c = ?, telefono = ? WHERE id = ?'
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (self.nombre, self.numero, id_num, ))
            conn.commit()
            self.selected = {}
        self.get_products()

class Cliente():
    #Bases de datos y variables necesarias
    database = 'database.db'
    personal_db = 'quit.db'
    id_num = 0

    def __init__(self, window, nombre, numero):
        #Definir la pantalla principal, ademas de definir las variables que se estaran usando
        self.window = window
        self.window.title('Nanny')
        self.n_kids = StringVar()
        self.n_kids.set('1')  
        self.dia = StringVar()
        self.dia.set('')
        self.care = StringVar()
        self.care.set('No')
        self.nombre = nombre 
        self.numero = numero
        self.ordenes = []

        #Frame en el que estaran todos los widgets
        frame = Frame(self.window)
        frame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        Label(frame, text = 'Dia: ').grid(row = 1, column = 0)
        ttk.Button(frame, text = "Set Date", command=self.calendar).grid(row = 1, column = 1)

        Label(frame, text = 'Cantidad de infantes: ').grid(row = 2, column = 0)
        self.kids = OptionMenu(frame, self.n_kids, '1', '2', '3')
        self.kids.grid(row = 2, column = 1)

        Label(frame, text = 'Desde: (Formato 24hr, Ej. 15:30)').grid(row = 3, column = 0)
        self.in_time = Entry(frame)
        self.in_time.grid(row = 3, column = 1)

        Label(frame, text = 'Hasta: (Formato 24hr, Ej. 19:00)').grid(row = 4, column = 0)
        self.end_time = Entry(frame)
        self.end_time.grid(row = 4, column = 1)

        Label(frame, text = 'Special Care: ').grid(row = 5, column = 0)
        self.special_care = OptionMenu(frame, self.care, 'Yes', 'No')
        self.special_care.grid(row = 5, column = 1)

        ttk.Button(frame, text='ORDER', command = self.add_order).grid(row=6, column = 1)
        ttk.Button(frame, text='CHECK', command = self.check).grid(row=6, column = 0)

    #Misma funcion que para cuidadores
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    #Abre un calendario para seleccionar una fecha, asi evitamos errores del usuario
    def calendar(self):
        cal_page = Toplevel()
        frame = Frame(cal_page)
        frame.grid(row=0, columnspan=2)
        cal = Calendar(frame, selectmode = 'day', year = 2020, month = 11, textvariable = self.dia)
        cal.grid()
        ttk.Button(frame, text='SET', command = cal_page.withdraw).grid()

    #Envia la orden a la base de datos, y en caso de que falten datos en el registro se le avisa al usuario para que pueda continuar ocn su orden
    def add_order(self):
        if self.validation():
            query = 'INSERT INTO ordenes VALUES(?,?,?,?,?,?,NULL,?,?,NULL,NULL,?)'
            codigo = f"{self.nombre[0]}{self.dia.get()[3]}{self.n_kids.get()[0]}{self.in_time.get()[1]}{self.end_time.get()[1]}{self.care.get()[0]}{self.numero[-4:]}"
            parameters = (self.nombre, self.dia.get(), self.n_kids.get(), self.in_time.get(), self.end_time.get(), self.care.get(), self.numero, 'No', codigo)
            self.run_query(query, parameters)
            ms.showinfo("Codigo", f"Codigo: {codigo}\nNo pierda este codigo! Lo necesitara para checar su orden.")
            self.dia.set('')
            self.in_time.delete(0, END)
            self.end_time.delete(0, END)
            self.n_kids.set('1')
            self.care.set('No')
        else:
            ms.showerror("Error!", "Oops! Faltan elementos por seleccionar")

    #Funcion para checar si una orden ya ha sido aceptada, esto mediante un codgio que crea la pagina al momento de pedir la orden
    #El codigo es unico a menos que el usuario haya hecho la misma orden 2 veces
    def check(self):
        check_page = Toplevel()

        frame = Frame(check_page)
        frame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        Label(frame, text = 'Codigo: ').grid(row = 1, column = 0)
        code = Entry(frame)
        code.grid(row = 1, column = 1)

        ttk.Button(frame, text = "CHECK", command=lambda: [self.check_code(code),check_page.withdraw()]).grid(row=2, columnspan=2)

    def check_code(self, code):
        if len(code.get()) != 0:
            query = f'SELECT * FROM ordenes WHERE code = "{code.get()}"'
            db_rows = self.run_query(query)
            for row in db_rows:
                if row[8] == 'Yes':
                    ms.showinfo('Orden Aceptada', f'Nombre del Cuidador: {row[9]}\nNumero del cuidador: {row[10]}')
                else:
                    ms.showinfo('Orden siendo procesada', 'Su orden no ha sido aceptada todavia')
    
    def validation(self):
        return len(self.dia.get()) != 0 and len(self.in_time.get()) != 0 and len(self.end_time.get()) != 0 and len(self.care.get()) != 0

#El proceso que se hara siempre que se inicialize la aplicacion
if __name__ == "__main__":
    avanzar = False
    tipo = ''
    nombre = ''
    telefono = ''
    window = Tk()
    aplicacion = login(window, avanzar, tipo, nombre, telefono)
    window.mainloop()
    avanzar = aplicacion.advance
    tipo = aplicacion.tipo
    nombre = aplicacion.nombre
    numero = aplicacion.telefono
    if avanzar == True:
        if tipo == 'Cliente':
            window2 = Tk()
            aplicacion = Cliente(window2, nombre, numero)
            window2.mainloop()
        elif tipo == 'Cuidador':
            window2 = Tk()
            aplicacion = Cuidador(window2, nombre, numero)
            window2.mainloop()