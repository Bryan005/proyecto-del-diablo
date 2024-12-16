import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from tkinter import PhotoImage
import re

users = []

def is_valid_email(email):
    """Función que valida si el email tiene un formato correcto."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# Función para agregar un usuario
def add_user(user_window):
    # Obtener datos de los campos
    id_val = validate_positive_number(entry_id.get(), "ID", user_window)
    name = entry_name.get().title()
    email = entry_email.get()

    # Verificar si el ID ya está en uso
    if any(i[0] == id_val for i in users):  
        messagebox.showerror("ID Error", "ID ya en uso, por favor ingrese otro ID.", parent=user_window)
        clear_fields()
        return  # Salir de la función si el ID está duplicado

    # Verificar que todos los campos estén llenos
    if not id_val or not name or not email:
        messagebox.showerror("Input Error", "Todos los campos deben estar llenos.", parent=user_window)
        clear_fields()
        return
    
    # Validar formato de correo electrónico
    if not is_valid_email(email):
        messagebox.showerror("Email Error", "Por favor ingrese una dirección de email valida.", parent=user_window)
        return

    # Agregar el usuario y guardar los cambios
    users.append([id_val, name, email])
    load_users()

    # Limpiar los campos
    clear_fields()

# Función para centrar la ventana
def centrar(ventana):
    ventana.update_idletasks()
    ancho = ventana.winfo_reqwidth()
    alto = ventana.winfo_reqheight()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def edit_user(user_window):
    selected_item = user_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Por favor seleeciona un usuario para editar.", parent=user_window)
        return

    # Obtener datos del usuario seleccionado
    id_val = validate_positive_number(entry_id.get(), "ID", user_window)
    name = entry_name.get().title()
    email = entry_email.get()

    # Verificar que todos los campos estén llenos
    if not id_val or not name or not email:
        messagebox.showerror("Input Error", "Todos los campos deben estar llenos.", parent=user_window)
        clear_fields()
        return
    
    # Validar formato de correo electrónico
    if not is_valid_email(email):
        messagebox.showerror("Email Error", "Por favor ingrese una dirección de email valida.", parent=user_window)
        return

    # Verificar si el ID ya está en uso (excepto el usuario seleccionado)
    selected_index = user_table.index(selected_item[0])  # Obtener el índice del usuario seleccionado
    if any(i[0] == id_val for i in users if users.index(i) != selected_index):
        messagebox.showerror("Error", "ID en uso, por favor ingrese un ID diferente.", parent=user_window)
        clear_fields()
        return
     
    # Actualizar el usuario en la lista
    users[selected_index] = [id_val, name, email]

    # Actualizar el Treeview
    user_table.item(selected_item[0], values=(id_val, name, email))

    # Guardar y recargar
    load_users()  # Asegúrate de que esta función actualice el Treeview
    clear_fields()
    messagebox.showinfo("Éxito", "Usuario actualizado correctamente!", parent=user_window)


# Función para eliminar un usuario
def delete_user(user_window):
    selected_item = user_table.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Por favor selecciona un usuario para eliminar.", parent=user_window)
        return

    selected_index = user_table.index(selected_item)
    users.pop(selected_index)
    load_users()
    clear_fields()

# Función para cargar los usuarios en la tabla
def load_users():
    # Limpiar el Treeview
    for item in user_table.get_children():
        user_table.delete(item)
    
    # Cargar datos desde la lista users
    for user in users:
        user_table.insert("", "end", values=user)


# Función para validar número positivo
def validate_positive_number(value, field_name, user_window):
    try:
        value = float(value)
        if value <= 0:
            raise ValueError
        return int(value)
    except ValueError:
        messagebox.showerror("Input Error", f"Por favor ingresa un número positivo valido para {field_name}.", parent=user_window)
        return None

# Función para limpiar los campos de entrada
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)

# Función para manejar la selección de los usuarios desde la tabla
def select_user(event):
    selected_item = user_table.selection()
    if selected_item:
        selected_user = user_table.item(selected_item)
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
        entry_email.delete(0, tk.END)

        entry_id.insert(0, selected_user['values'][0])
        entry_name.insert(0, selected_user['values'][1])
        entry_email.insert(0, selected_user['values'][2])

def open_user_window():
    user_window = tk.Toplevel(root)
    user_window.title("Usuarios")
    user_window.configure(bg="#add8e6")  # Color celeste
    user_window.grab_set()
    user_window.resizable(False, False)
    
    global entry_id, entry_name, entry_email, user_table

    # Etiquetas y entradas
    ttk.Label(user_window, text="ID:", background="#add8e6", font=("Arial", 10, "bold"))\
        .grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_id = ttk.Entry(user_window)
    entry_id.grid(row=0, column=1, padx=10, pady=5, sticky="e")

    ttk.Label(user_window, text="Nombre:", background="#add8e6", font=("Arial", 10, "bold"))\
        .grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_name = ttk.Entry(user_window)
    entry_name.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    ttk.Label(user_window, text="Email:", background="#add8e6", font=("Arial", 10, "bold"))\
        .grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_email = ttk.Entry(user_window)
    entry_email.grid(row=2, column=1, padx=10, pady=5, sticky="e")

    # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    # Crear un frame para los botones
    button_frame = ttk.Frame(user_window, style='Custom.TFrame')
    button_frame.grid(row=3, column=0, columnspan=2, pady=10)

    # Botones dentro del frame
    ttk.Button(button_frame, text="Agregar", command=lambda: add_user(user_window), style='TButton')\
        .pack(side="left", padx=5, pady=5)
    ttk.Button(button_frame, text="Editar", command=lambda: edit_user(user_window), style='TButton')\
        .pack(side="left", padx=5, pady=5)
    ttk.Button(button_frame, text="Eliminar", command=lambda: delete_user(user_window), style='Delete.TButton')\
        .pack(side="left", padx=5, pady=5)


    # Tabla de usuarios
    user_table = ttk.Treeview(user_window, columns=("ID", "Name", "Email"), show="headings", height=8)
    user_table.heading("ID", text="ID")
    user_table.heading("Name", text="Nombre")
    user_table.heading("Email", text="Email")
    user_table.column("ID", width=50)
    user_table.column("Name", width=150)
    user_table.column("Email", width=200)
    user_table.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    user_table.bind("<<TreeviewSelect>>", select_user)

    # Botón de retroceso
    ttk.Button(user_window, text="Atrás", command=user_window.destroy, style='TButton')\
        .grid(row=6, column=0, columnspan=2, pady=10)

    # Configurar proporciones
    user_window.columnconfigure(0, weight=1)
    user_window.columnconfigure(1, weight=1)
    user_window.rowconfigure(5, weight=1)  # La fila de la tabla es la única que se expande

    load_users()
    centrar(user_window)

def extract_value(entry):
    try:
        return float(entry.get()) if entry.get() else None
    except ValueError:
        return None

def clear_and_insert(entry, value):
    if entry:
        entry.delete(0, tk.END)
        entry.insert(0, f"{value:.2f}")

# ----------------------Ley de ohmm--------------------------------------

def calculate_ohm_law(entries, calc_window):

    entry_voltage, entry_current, entry_resistance = entries
    v = extract_value(entry_voltage)
    i = extract_value(entry_current)
    r = extract_value(entry_resistance)

    # Validar que todos los campos estén llenos
    if not any([v, i, r]):
        messagebox.showerror("Input Error", "Al menos dos campos deben estar llenos para realizar el cálculo.", parent=calc_window)
        return

    if sum(1 for x in [v, i, r] if x is not None) != 2:
        messagebox.showerror("Invalid Calculation", "Exactamente dos campos deben estar llenos para realizar el cálculo.", parent=calc_window)
        return

    result = None
    if v and i and not r:
        result = v / i
        clear_and_insert(entry_resistance, result)
        messagebox.showinfo("Resultado", f"Resistencia (R) = {result} Ω", parent=calc_window)
    elif v and r and not i:
        result = v / r
        clear_and_insert(entry_current, result)
        messagebox.showinfo("Resultado", f"Corriente (I) = {result} A", parent=calc_window)
    elif i and r and not v:
        result = i * r
        clear_and_insert(entry_voltage, result)
        messagebox.showinfo("Resultado", f"Voltaje (V) = {result} V", parent=calc_window)

def show_ohm_law_fields(calculate_for, calc_window):
    # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    """Muestra los campos necesarios según la selección del usuario."""
    calc_window = tk.Toplevel(root)
    calc_window.title("Calculadora Ley de Ohm")
    calc_window.configure(bg="#add8e6")  # Color celeste
    calc_window.grab_set()
    calc_window.resizable(False, False)

    entry_voltage = None
    entry_current = None
    entry_resistance = None

    if calculate_for == 'V':
        label_current = tk.Label(calc_window, text="Corriente (I):", background="#add8e6")
        label_current.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_current = tk.Entry(calc_window)
        entry_current.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        label_resistance = tk.Label(calc_window, text="Resistencia (R):", background="#add8e6")
        label_resistance.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_resistance = tk.Entry(calc_window)
        entry_resistance.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    elif calculate_for == 'I':
        label_voltage = tk.Label(calc_window, text="Voltaje (V):", background="#add8e6")
        label_voltage.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_voltage = tk.Entry(calc_window)
        entry_voltage.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        label_resistance = tk.Label(calc_window, text="Resistencia (R):", background="#add8e6")
        label_resistance.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_resistance = tk.Entry(calc_window)
        entry_resistance.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    elif calculate_for == 'R':
        label_voltage = tk.Label(calc_window, text="Voltaje (V):", background="#add8e6")
        label_voltage.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_voltage = tk.Entry(calc_window)
        entry_voltage.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        label_current = tk.Label(calc_window, text="Corriente (I):", background="#add8e6")
        label_current.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_current = tk.Entry(calc_window)
        entry_current.grid(row=1, column=1, padx=10, pady=5, sticky="e")

    entries = (entry_voltage, entry_current, entry_resistance)

    button_calculate = ttk.Button(calc_window, text="Calcular", command=lambda: calculate_ohm_law(entries, calc_window), style='TButton')
    button_calculate.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    ttk.Button(calc_window, text="Atrás", command=calc_window.destroy, style='Delete.TButton').grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="e")

    centrar(calc_window)


def open_calculations_window():

    # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    """Muestra una ventana con opciones de cálculo."""
    calc_window = tk.Toplevel(root)
    calc_window.title("Elegir cálculo")
    calc_window.configure(bg="#add8e6")  # Color celeste
    calc_window.grab_set()
    calc_window.resizable(False, False)

    global icon_voltage, icon_current, icon_resistance, icon_others

    # Cargar imágenes (asegúrate de que las rutas sean correctas)
    icon_voltage = PhotoImage(file="imgs/v.png")
    icon_current = PhotoImage(file="imgs/i.png")
    icon_resistance = PhotoImage(file="imgs/r.png")
    icon_others = PhotoImage(file="imgs/c.png")

    # Crear los botones con fondo transparente
    button_voltage = tk.Button(calc_window, text="Voltaje (V)", image=icon_voltage, compound="top", 
                               command=lambda: show_ohm_law_fields('V', calc_window), bg="white")
    button_voltage.grid(row=0, column=0, padx=10, pady=10)

    button_current = tk.Button(calc_window, text="Corriente (I)", image=icon_current, compound="top", 
                               command=lambda: show_ohm_law_fields('I', calc_window), bg="white")
    button_current.grid(row=0, column=1, padx=10, pady=10)

    button_resistance = tk.Button(calc_window, text="Resistencia (R)", image=icon_resistance, compound="top", 
                                  command=lambda: show_ohm_law_fields('R', calc_window), bg="white")
    button_resistance.grid(row=1, column=0, padx=10, pady=10)

    button_others = tk.Button(calc_window, text="Otros cálculos", image=icon_others, compound="top", 
                              command=open_circuit_design_window, bg="white")
    button_others.grid(row=1, column=1, padx=10, pady=10)

    # Crear el botón de "Back" con fondo transparente
    ttk.Button(calc_window, text="Atrás", command=calc_window.destroy, style='Delete.TButton').grid(row=2, column=0, columnspan=2, pady=10)

    centrar(calc_window)


# ----------------------Circuitos en Serie y Paralelo--------------------------------------
def calculate_circuits(entries, calc_window, mode):
    resistances = extract_list_values(entries[:-1])  # Excluir el campo de voltaje

    if not resistances:
        messagebox.showerror("Input Error", "Se debe prever al menos una resistencia.", parent=calc_window)
        return

    if mode == 'serie':
        equivalent_resistance = sum(resistances)
    elif mode == 'paralelo':
        try:
            equivalent_resistance = 1 / sum(1 / r for r in resistances)
        except ZeroDivisionError:
            messagebox.showerror("Error", "La resistencia no puede ser cero en circuitos paralelos.", parent=calc_window)
            return

    voltage = extract_value(entries[-1]) or 0  # Campo de voltaje, usar 0 si está vacío
    total_current = voltage / equivalent_resistance

    messagebox.showinfo(
        "Resultado",
        f"Resistencia equivalente = {equivalent_resistance:.2f} Ω\nVoltaje = {voltage:.2f} V\nCorriente Total = {total_current:.2f} A",
        parent=calc_window
    )

def show_circuit_fields(mode, calc_window):
    # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    calc_window = tk.Toplevel(root)
    calc_window.title(f"Cálculo circuitos ({mode.capitalize()})")
    calc_window.configure(bg="#add8e6")  # Color celeste
    calc_window.grab_set()
    calc_window.resizable(False, False)

    entries = []

    def update_widgets():
        # Eliminar etiquetas existentes
        for widget in calc_window.winfo_children():
            if isinstance(widget, tk.Label):  # Sólo destruir etiquetas
                widget.destroy()

        # Reorganizar los campos dinámicamente
        for idx, entry in enumerate(entries[:-1]):
            tk.Label(calc_window, text=f"Resistancia (R) {idx + 1}:", background="#add8e6").grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            entry.grid(row=idx, column=1, padx=10, pady=5, sticky="e")

        # Campo de voltaje siempre al final
        tk.Label(calc_window, text="Voltaje (V):", background="#add8e6").grid(row=len(entries) - 1, column=0, padx=10, pady=5, sticky="w")
        entries[-1].grid(row=len(entries) - 1, column=1, padx=10, pady=5, sticky="e")

        # Los botones
        # Botón Agregar
        button_add.grid(row=len(entries), column=0, padx=10, pady=10, sticky="w")
        # Botón Calcular
        button_calculate.grid(row=len(entries), column=1, padx=10, pady=10, sticky="e")
        # Botón Volver
        button_back.grid(row=len(entries) + 1, column=0, columnspan=2, pady=10)

        # Ajustar tamaño de la ventana
        calc_window.update_idletasks()
        calc_window.geometry(f"{calc_window.winfo_reqwidth()}x{calc_window.winfo_reqheight()}")

    def add_resistance_field():
        entry = tk.Entry(calc_window)
        entries.insert(-1, entry)  # Insertar antes del campo de voltaje
        update_widgets()

    # Inicializar los campos
    entry_r1 = tk.Entry(calc_window)
    entry_r2 = tk.Entry(calc_window)
    entry_voltage = tk.Entry(calc_window)
    entries.extend([entry_r1, entry_r2, entry_voltage])

    # Botones con estilo
    button_add = ttk.Button(calc_window, text="Agregar", command=add_resistance_field, style='TButton')
    button_calculate = ttk.Button(calc_window, text="Calcular", command=lambda: calculate_circuits(entries, calc_window, mode), style='TButton')
    button_back = ttk.Button(calc_window, text="Atrás", command=calc_window.destroy, style='Delete.TButton')

    update_widgets()

    centrar(calc_window)


# ----------------------Ventanas de Opciones--------------------------------------
def open_circuit_design_window():

    # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    circuit_window = tk.Toplevel(root)
    circuit_window.title("Cálculo de circuitos")
    circuit_window.configure(bg="#add8e6")  # Color celeste
    circuit_window.grab_set()
    circuit_window.resizable(False, False)

    button_serie = ttk.Button(circuit_window, text="Circuito en Serie", command=lambda: show_circuit_fields('serie', circuit_window), style='TButton')
    button_serie.grid(row=0, column=0, padx=10, pady=10)

    button_parallel = ttk.Button(circuit_window, text="Circuito en Parelelo", command=lambda: show_circuit_fields('paralelo', circuit_window),style='TButton')
    button_parallel.grid(row=0, column=1, padx=10, pady=10)

    centrar(circuit_window)

def extract_list_values(entries):
    return [extract_value(entry) for entry in entries if entry.get()]

def extract_value(entry):
    """Extrae un valor flotante de un campo de entrada."""
    try:
        return float(entry.get()) if entry and entry.get() else None
    except ValueError:
        return None

def clear_and_insert(entry, value):
    """Limpia el campo de entrada y escribe un nuevo valor."""
    if entry:
        entry.delete(0, tk.END)
        entry.insert(0, value)

# -------------------------Diseño circuitos-------------------------------------------
def open_circuit_draw_window():
    draw_window = tk.Toplevel(root)
    draw_window.title("Diseño de Circuitos")
    draw_window.grab_set()
    draw_window.resizable(False, False)

    canvas = tk.Canvas(draw_window, bg="white", width=800, height=600)
    canvas.grid(row=1, column=0, columnspan=7)
    components = []
    connections = []
    simulation_results = {}

    # Dibujar cuadrícula
    def draw_grid():
        for i in range(0, 800, 20):
            canvas.create_line(i, 0, i, 600, fill="lightgray")
        for i in range(0, 600, 20):
            canvas.create_line(0, i, 800, i, fill="lightgray")

    def add_component(type_name, unit, symbol, width=80, height=40):
        value = simpledialog.askfloat(f"Agregar {type_name}", f"Ingrese el valor del/la {type_name} ({unit}):")
        if value is not None:
            x, y = 100 + len(components) * 100, 100
            rect = canvas.create_rectangle(x, y, x + width, y + height, fill="white", outline="black")
            text = canvas.create_text(x + width / 2, y + height / 2, text=f"{symbol}\n{value}{unit}", font=("Arial", 10))
            components.append({"type": type_name, "x": x, "y": y, "value": value, "rect": rect, "text": text})
            make_draggable(rect, text)

    def make_draggable(rect, text):
        def on_drag(event):
            dx, dy = event.x - canvas.coords(rect)[0] - 40, event.y - canvas.coords(rect)[1] - 20
            canvas.move(rect, dx, dy)
            canvas.move(text, dx, dy)
            for connection in connections:
                update_connection(connection)

        canvas.tag_bind(rect, "<B1-Motion>", on_drag)
        canvas.tag_bind(text, "<B1-Motion>", on_drag)

    def get_component_center(component):
        coords = canvas.coords(component)
        return (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2

    def connect_components():
        if len(components) < 2:
            messagebox.showwarning("Conectar Componentes", "Se necesitan al menos dos componentes para conectar.", parent=draw_window)
            return

        for connection in connections:
            canvas.delete(connection["line"])
        connections.clear()

        for i, comp1 in enumerate(components):
            x1, y1 = get_component_center(comp1["rect"])
            for j, comp2 in enumerate(components):
                if i != j and not any(
                    c for c in connections if (c["comp1"] == comp1 and c["comp2"] == comp2) or 
                    (c["comp1"] == comp2 and c["comp2"] == comp1)
                ):
                    x2, y2 = get_component_center(comp2["rect"])
                    distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
                    if distance < 150:  # Conectar solo si están cerca
                        line = canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
                        connections.append({"line": line, "comp1": comp1, "comp2": comp2})

    def update_connection(connection):
        x1, y1 = get_component_center(connection["comp1"]["rect"])
        x2, y2 = get_component_center(connection["comp2"]["rect"])
        canvas.coords(connection["line"], x1, y1, x2, y2)

    def delete_circuit():
        for connection in connections:
            canvas.delete(connection["line"])
        connections.clear()

        for component in components:
            canvas.delete(component["rect"])
            canvas.delete(component["text"])
        components.clear()

        simulation_results.clear()

    def delete_component():
        if not components:
            messagebox.showwarning("Eliminar Componente", "No hay componentes para eliminar.", parent=draw_window)
            return

        component_to_delete = simpledialog.askinteger("Eliminar Componente", "Ingrese el índice del componente a eliminar (1 a N):", minvalue=1, maxvalue=len(components), parent=draw_window)
        if component_to_delete is not None:
            component_to_delete -= 1
            component = components.pop(component_to_delete)

            canvas.delete(component["rect"])
            canvas.delete(component["text"])

            to_remove = [c for c in connections if c["comp1"] == component or c["comp2"] == component]
            for connection in to_remove:
                canvas.delete(connection["line"])
                connections.remove(connection)

    def classify_circuit():
        if not connections:
            return "Sin conexiones"

        visited = set()
        stack = [get_component_center(connections[0]["comp1"]["rect"])]

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                for connection in connections:
                    comp1_center = get_component_center(connection["comp1"]["rect"])
                    comp2_center = get_component_center(connection["comp2"]["rect"])

                    if comp1_center == current and comp2_center not in visited:
                        stack.append(comp2_center)
                    elif comp2_center == current and comp1_center not in visited:
                        stack.append(comp1_center)

        if len(visited) == len(components):
            return "Circuito en Serie"
        else:
            return "Circuito en Paralelo"

    def start_simulation():

        if not connections:
            messagebox.showwarning("Iniciar Simulación", "No hay componentes conectados.", parent=draw_window)
            return

        total_voltage = sum(c["value"] for c in components if c["type"] == "Fuente de Voltaje")
        total_resistance = sum(c["value"] for c in components if c["type"] == "Resistencia")
        total_current = total_voltage / total_resistance if total_resistance > 0 else 0

        circuit_type = classify_circuit()

        simulation_results["total_voltage"] = total_voltage
        simulation_results["total_current"] = total_current
        simulation_results["circuit_type"] = circuit_type

        messagebox.showinfo("Simulación", f"Voltaje total: {total_voltage}V\nCorriente total: {total_current}A\nTipo de circuito: {circuit_type}", parent=draw_window)

    def show_message():
        if not simulation_results:
            messagebox.showwarning("Resultados de Simulación", "No se ha realizado ninguna simulación.", parent=draw_window)
            return
        messagebox.showinfo("Resultados de Simulación", f"Voltaje total: {simulation_results['total_voltage']}V\nCorriente total: {simulation_results['total_current']}A\nTipo de circuito: {simulation_results['circuit_type']}", parent=draw_window)

    # Panel de control

     # Estilo de los botones
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 10, 'bold'))
    style.configure('Delete.TButton', background='#e60902', font=('Arial', 10, 'bold')) 
    style.configure('Custom.TFrame', background="#add8e6")

    buttons = [
        ("Agregar Fuente", lambda: add_component("Fuente de Voltaje", "V", "V")),
        ("Agregar Resistencia", lambda: add_component("Resistencia", "\u03A9", "R")),
        ("Agregar LED", lambda: add_component("LED", "mA", "LED")),
        ("Agregar Motor", lambda: add_component("Motor", "W", "M")),
        ("Conectar Componentes", connect_components),
        ("Eliminar Circuito", delete_circuit),
        ("Eliminar Componente", delete_component),
        ("Iniciar Simulación", start_simulation),
        ("Mostrar Mensaje", show_message)
    ]

    for i, (text, command) in enumerate(buttons):
        ttk.Button(draw_window, text=text, command=command, style='TButton').grid(row=0, column=i)
    
    draw_grid()
    centrar(draw_window)

# Ventana principal
root = tk.Tk()
root.title("Cálculos Electrónicos")
root.configure(bg="#add8e6")  # Color celeste
root.resizable(False, False)

# Configuración de columnas y filas para centrar los widgets
root.columnconfigure(0, weight=1)  # Hacer que la única columna ocupe todo el espacio
root.rowconfigure([0, 1, 2, 3], weight=1)  # Hacer que las filas también ocupen espacio proporcional

# Etiqueta de bienvenida
ttk.Label(
    root,
    text="Bienvenido, esta es una aplicación para cálculos eléctricos y \nanálisis de circuitos.",
    font=("Arial", 14),
    background="#add8e6",
    anchor="center",  # Asegurar que el texto esté centrado dentro del widget
    justify="center"  # Centrar el texto en múltiples líneas
).grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

# Etiqueta de instrucciones centrada
ttk.Label(
    root,
    text="Selecciona una opción para continuar:",
    font=("Arial", 14),
    background="#add8e6",
    anchor="center",  # Asegurar que el texto esté centrado dentro del widget
    justify="center"  # Centrar el texto en caso de varias líneas
).grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

# Menú desplegable
menu = ttk.Combobox(root, values=["Usuarios", "Ley de Ohm", "Diseño de Circuitos"], state="readonly")
menu.grid(row=2, column=0, padx=20, pady=10, sticky="ns")

# Botón para navegar
def navigate_menu():
    if menu.get() == "Usuarios":
        open_user_window()
    elif menu.get() == "Ley de Ohm":
        open_calculations_window()
    elif menu.get() == "Diseño de Circuitos":
        open_circuit_draw_window()

ttk.Button(
    root,
    text="Continuar",
    command=navigate_menu
).grid(row=3, column=0, padx=20, pady=10, sticky="ns")

centrar(root)

root.mainloop()