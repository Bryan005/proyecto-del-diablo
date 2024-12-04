import tkinter as tk
from tkinter import ttk, messagebox


class BaseDeDatos:
    """Clase para gestionar los registros de la aplicación."""
    def __init__(self):
        self.registros = []  # Lista de diccionarios para almacenar los datos

    def agregar(self, registro):
        """Agrega un nuevo registro."""
        self.registros.append(registro)

    def editar(self, indice, registro):
        """Edita un registro existente."""
        if 0 <= indice < len(self.registros):
            self.registros[indice] = registro

    def eliminar(self, indice):
        """Elimina un registro existente."""
        if 0 <= indice < len(self.registros):
            return self.registros.pop(indice)
        return None


class AppElectrica:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación para Cálculos Eléctricos")
        self.root.geometry("900x700")
        self.root.configure(bg="#f7f7f7")

        # Base de datos en memoria
        self.db = BaseDeDatos()

        # Variables para navegación entre secciones
        self.seccion_actual = tk.StringVar(value="Datos del Usuario")

        # Crear interfaz principal
        self.crear_navegacion()
        self.crear_secciones()

    def crear_navegacion(self):
        """Crea la barra de navegación."""
        frame_nav = tk.Frame(self.root, bg="#4CAF50", height=50)
        frame_nav.pack(side="top", fill="x")

        opciones = ["Datos del Usuario", "Cálculos Eléctricos", "Diseño de Circuitos"]
        self.menu_navegacion = ttk.Combobox(frame_nav, values=opciones, textvariable=self.seccion_actual, state="readonly")
        self.menu_navegacion.pack(pady=10, padx=20, side="left")
        self.menu_navegacion.bind("<<ComboboxSelected>>", self.cambiar_seccion)

        tk.Label(frame_nav, text="Seleccione una sección", bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=10, side="left", padx=10)

    def crear_secciones(self):
        """Crea las secciones de la aplicación."""
        # Sección de Datos del Usuario
        self.frame_datos_usuario = tk.Frame(self.root, bg="#f7f7f7")
        self.crear_seccion_datos_usuario()

        # Sección de Cálculos Eléctricos
        self.frame_calculos = tk.Frame(self.root, bg="#f7f7f7")
        self.crear_seccion_calculos_electricos()

        # Sección de Diseño de Circuitos
        self.frame_circuitos = tk.Frame(self.root, bg="#f7f7f7")
        self.crear_seccion_circuitos()

    def crear_seccion_datos_usuario(self):
        """Crea la sección de gestión de usuarios."""
        tk.Label(self.frame_datos_usuario, text="Gestión de Usuarios", font=("Helvetica", 16, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        frame_usuario = tk.LabelFrame(self.frame_datos_usuario, text="Datos del Usuario", bg="#ffffff", font=("Helvetica", 10), padx=10, pady=10)
        frame_usuario.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_usuario, text="ID:", font=("Helvetica", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = tk.Entry(frame_usuario, font=("Helvetica", 10))
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_usuario, text="Nombre:", font=("Helvetica", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(frame_usuario, font=("Helvetica", 10))
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_usuario, text="Correo Electrónico:", font=("Helvetica", 10), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
        self.entry_correo = tk.Entry(frame_usuario, font=("Helvetica", 10))
        self.entry_correo.grid(row=2, column=1, padx=5, pady=5)

        # Botones para acciones
        frame_botones = tk.Frame(self.frame_datos_usuario, bg="#f7f7f7")
        frame_botones.pack(pady=10)

        self.estilizar_boton(frame_botones, "Agregar Usuario", self.agregar_usuario).pack(side="left", padx=5, pady=5)
        self.estilizar_boton(frame_botones, "Editar Usuario", self.editar_usuario).pack(side="left", padx=5, pady=5)
        self.estilizar_boton(frame_botones, "Eliminar Usuario", self.eliminar_usuario).pack(side="left", padx=5, pady=5)

        # Tabla para mostrar los usuarios
        frame_tabla = tk.Frame(self.frame_datos_usuario, bg="#ffffff")
        frame_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Correo"), show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo Electrónico")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Nombre", width=200, anchor="center")
        self.tree.column("Correo", width=300, anchor="center")
        self.tree.bind("<Double-1>", self.seleccionar_usuario)
        self.tree.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=2, sticky="ns")

    def crear_seccion_calculos_electricos(self):
        """Crea la sección para cálculos eléctricos."""
        tk.Label(self.frame_calculos, text="Cálculos Eléctricos", font=("Helvetica", 16, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        frame_calculos = tk.LabelFrame(self.frame_calculos, text="Ley de Ohm y Circuitos", bg="#ffffff", font=("Helvetica", 10), padx=10, pady=10)
        frame_calculos.pack(padx=20, pady=10, fill="x")

        # Entradas para Corriente, Voltaje y Resistencia
        tk.Label(frame_calculos, text="Corriente (A):", font=("Helvetica", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.entry_corriente = tk.Entry(frame_calculos, font=("Helvetica", 10))
        self.entry_corriente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_calculos, text="Voltaje (V):", font=("Helvetica", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
        self.entry_voltaje = tk.Entry(frame_calculos, font=("Helvetica", 10))
        self.entry_voltaje.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_calculos, text="Resistencia (Ω):", font=("Helvetica", 10), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
        self.entry_resistencia = tk.Entry(frame_calculos, font=("Helvetica", 10))
        self.entry_resistencia.grid(row=2, column=1, padx=5, pady=5)

        # Botones para calcular
        self.estilizar_boton(frame_calculos, "Calcular Valor Desconocido", self.calcular_desconocido).grid(row=3, column=0, columnspan=2, pady=10)

        # Mostrar resultado
        self.label_resultado_ohm = tk.Label(self.frame_calculos, text="Resultado: ", font=("Helvetica", 12), bg="#f7f7f7", fg="#555")
        self.label_resultado_ohm.pack(pady=10)

        # Circuitos en Serie y Paralelo
        frame_circuitos = tk.LabelFrame(self.frame_calculos, text="Circuitos", bg="#ffffff", font=("Helvetica", 10), padx=10, pady=10)
        frame_circuitos.pack(padx=20, pady=10, fill="x")

        self.estilizar_boton(frame_circuitos, "Resistencia Equivalente (Serie)", self.calcular_serie).grid(row=0, column=0, pady=5)
        self.estilizar_boton(frame_circuitos, "Resistencia Equivalente (Paralelo)", self.calcular_paralelo).grid(row=0, column=1, pady=5)

    def crear_seccion_circuitos(self):
        """Crea la sección para diseñar circuitos eléctricos simples."""
        tk.Label(self.frame_circuitos, text="Diseño de Circuitos", font=("Helvetica", 16, "bold"), bg="#f7f7f7", fg="#333").pack(pady=10)

        frame_componentes = tk.LabelFrame(self.frame_circuitos, text="Componentes del Circuito", bg="#ffffff", font=("Helvetica", 10), padx=10, pady=10)
        frame_componentes.pack(padx=20, pady=10, fill="x")

        tk.Label(frame_componentes, text="Resistencia (Ω):", font=("Helvetica", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.entry_resistencia_circuito = tk.Entry(frame_componentes, font=("Helvetica", 10))
        self.entry_resistencia_circuito.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_componentes, text="Voltaje (V):", font=("Helvetica", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
        self.entry_voltaje_circuito = tk.Entry(frame_componentes, font=("Helvetica", 10))
        self.entry_voltaje_circuito.grid(row=1, column=1, padx=5, pady=5)

        self.estilizar_boton(frame_componentes, "Agregar Componente", self.agregar_componente).grid(row=2, column=0, columnspan=2, pady=10)

        # Tabla para mostrar los componentes del circuito
        self.tree_circuito = ttk.Treeview(frame_componentes, columns=("Resistencia", "Voltaje"), show="headings", height=8)
        self.tree_circuito.heading("Resistencia", text="Resistencia (Ω)")
        self.tree_circuito.heading("Voltaje", text="Voltaje (V)")
        self.tree_circuito.column("Resistencia", width=150, anchor="center")
        self.tree_circuito.column("Voltaje", width=150, anchor="center")

        # Ahora usamos `grid` en vez de `pack` para mantener la coherencia
        self.tree_circuito.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame_componentes, orient="vertical", command=self.tree_circuito.yview)
        self.tree_circuito.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=3, column=2, sticky="ns")

    def estilizar_boton(self, parent, texto, comando):
        """Crea un botón estilizado."""
        return tk.Button(parent, text=texto, command=comando,
                         font=("Helvetica", 10), bg="#4CAF50", fg="white",
                         activebackground="#45a049", activeforeground="white", relief="flat", padx=10, pady=5)

    def agregar_usuario(self):
        """Agrega un nuevo usuario a la tabla."""
        if not self.validar_datos_usuario():
            return

        nuevo_usuario = {
            "ID": self.entry_id.get().strip(),
            "Nombre": self.entry_nombre.get().strip(),
            "Correo": self.entry_correo.get().strip(),
        }
        # Agregar a la base de datos
        self.db.agregar(nuevo_usuario)

        # Agregar a la tabla visual
        self.tree.insert("", "end", values=(nuevo_usuario["ID"], nuevo_usuario["Nombre"], nuevo_usuario["Correo"]))

        # Limpiar los campos de entrada
        self.limpiar_campos_usuario()

    def editar_usuario(self):
        """Edita el usuario seleccionado en la tabla."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona un usuario para editar.")
            return

        # Obtener el índice y los datos seleccionados
        item = self.tree.item(seleccion[0])
        indice = self.tree.index(seleccion[0])

        if not self.validar_datos_usuario():
            return

        usuario_actualizado = {
            "ID": self.entry_id.get().strip(),
            "Nombre": self.entry_nombre.get().strip(),
            "Correo": self.entry_correo.get().strip(),
        }

        # Actualizar la base de datos
        self.db.editar(indice, usuario_actualizado)

        # Actualizar en la tabla
        self.tree.item(seleccion[0], values=(usuario_actualizado["ID"], usuario_actualizado["Nombre"], usuario_actualizado["Correo"]))

        # Limpiar los campos de entrada
        self.limpiar_campos_usuario()

    def eliminar_usuario(self):
        """Elimina el usuario seleccionado de la tabla."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, selecciona un usuario para eliminar.")
            return

        # Obtener el índice seleccionado
        indice = self.tree.index(seleccion[0])

        # Eliminar de la base de datos
        eliminado = self.db.eliminar(indice)
        if eliminado:
            # Eliminar de la tabla
            self.tree.delete(seleccion[0])
            messagebox.showinfo("Éxito", f"Usuario eliminado: {eliminado['Nombre']}")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el usuario.")

        # Limpiar los campos de entrada
        self.limpiar_campos_usuario()

    def seleccionar_usuario(self, event):
        """Llena los campos con el usuario seleccionado en la tabla."""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, valores[0])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_correo.delete(0, tk.END)
            self.entry_correo.insert(0, valores[2])

    def limpiar_campos_usuario(self):
        """Limpia los campos de entrada."""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_correo.delete(0, tk.END)

    def validar_datos_usuario(self):
        """Valida que los datos del usuario sean correctos."""
        if not self.entry_id.get().strip():
            messagebox.showerror("Error", "El ID no puede estar vacío.")
            return False
        if not self.entry_nombre.get().strip():
            messagebox.showerror("Error", "El Nombre no puede estar vacío.")
            return False
        if not self.entry_correo.get().strip():
            messagebox.showerror("Error", "El Correo no puede estar vacío.")
            return False
        return True

    def calcular_desconocido(self):
        """Calcula el valor desconocido usando la Ley de Ohm."""
        try:
            corriente = self.entry_corriente.get()
            voltaje = self.entry_voltaje.get()
            resistencia = self.entry_resistencia.get()

            # Determinamos cuál valor falta
            if corriente == "":
                corriente = float(voltaje) / float(resistencia)
                self.entry_corriente.insert(0, f"{corriente:.2f}")
                self.label_resultado_ohm.config(text=f"Resultado: Corriente = {corriente:.2f} A")
            elif voltaje == "":
                voltaje = float(corriente) * float(resistencia)
                self.entry_voltaje.insert(0, f"{voltaje:.2f}")
                self.label_resultado_ohm.config(text=f"Resultado: Voltaje = {voltaje:.2f} V")
            elif resistencia == "":
                resistencia = float(voltaje) / float(corriente)
                self.entry_resistencia.insert(0, f"{resistencia:.2f}")
                self.label_resultado_ohm.config(text=f"Resultado: Resistencia = {resistencia:.2f} Ω")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos para los cálculos.")

    def calcular_serie(self):
        """Calcula la resistencia equivalente en un circuito en serie."""
        try:
            resistencias = [float(r) for r in self.entry_resistencia_circuito.get().split(",")]
            resistencia_eq = sum(resistencias)
            self.label_resultado_ohm.config(text=f"Resistencia Equivalente (Serie): {resistencia_eq:.2f} Ω")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa las resistencias separadas por comas.")

    def calcular_paralelo(self):
        """Calcula la resistencia equivalente en un circuito en paralelo."""
        try:
            resistencias = [float(r) for r in self.entry_resistencia_circuito.get().split(",")]
            resistencia_eq = 1 / sum(1 / r for r in resistencias)
            self.label_resultado_ohm.config(text=f"Resistencia Equivalente (Paralelo): {resistencia_eq:.2f} Ω")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa las resistencias separadas por comas.")

    def agregar_componente(self):
        """Agrega un componente al circuito."""
        try:
            resistencia = float(self.entry_resistencia_circuito.get())
            voltaje = float(self.entry_voltaje_circuito.get())

            # Agregar el componente a la tabla
            self.tree_circuito.insert("", "end", values=(resistencia, voltaje))

            # Limpiar los campos de entrada para el siguiente componente
            self.entry_resistencia_circuito.delete(0, tk.END)
            self.entry_voltaje_circuito.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores válidos para la resistencia y voltaje.")

    def cambiar_seccion(self, event):
        """Cambia entre las secciones según lo seleccionado en la lista desplegable."""
        seccion = self.seccion_actual.get()

        # Ocultar todas las secciones
        self.frame_datos_usuario.pack_forget()
        self.frame_calculos.pack_forget()
        self.frame_circuitos.pack_forget()

        # Mostrar la sección seleccionada
        if seccion == "Datos del Usuario":
            self.frame_datos_usuario.pack(fill="both", expand=True)
        elif seccion == "Cálculos Eléctricos":
            self.frame_calculos.pack(fill="both", expand=True)
        elif seccion == "Diseño de Circuitos":
            self.frame_circuitos.pack(fill="both", expand=True)


# Crear la ventana principal y ejecutar la aplicación
root = tk.Tk()
app = AppElectrica(root)
root.mainloop()
