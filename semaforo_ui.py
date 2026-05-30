import tkinter as tk
from tkinter import messagebox
import serial
import serial.tools.list_ports
import time

class SemaforoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Semáforo")
        self.root.geometry("300x250")

        self.serial_port = None
        self.current_port_name = ""

        # Puerto COM
        tk.Label(root, text="Puerto COM:").pack(pady=5)
        self.port_var = tk.StringVar()
        self.port_menu = tk.OptionMenu(root, self.port_var, "")
        self.port_menu.pack()
        self.refresh_ports()

        # Botón para actualizar puertos
        tk.Button(root, text="Actualizar Puertos", command=self.refresh_ports).pack(pady=5)

        # Tiempo Verde
        tk.Label(root, text="Tiempo Verde (segundos):").pack()
        self.green_var = tk.StringVar(value="3")
        tk.Entry(root, textvariable=self.green_var, justify='center').pack()

        # Tiempo Rojo
        tk.Label(root, text="Tiempo Rojo (segundos):").pack()
        self.red_var = tk.StringVar(value="3")
        tk.Entry(root, textvariable=self.red_var, justify='center').pack()

        # Botón Enviar
        tk.Button(root, text="Enviar Tiempos", command=self.send_times, bg="lightblue").pack(pady=15)

        # Al cerrar la ventana, asegurar cierre del puerto
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def refresh_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        menu = self.port_menu["menu"]
        menu.delete(0, "end")
        if ports:
            for port in ports:
                menu.add_command(label=port, command=lambda p=port: self.port_var.set(p))
            self.port_var.set(ports[0])
        else:
            # Si no detecta, permite escribir manualmente
            self.port_var.set("COM1")

    def send_times(self):
        port = self.port_var.get()
        try:
            green_time = int(self.green_var.get())
            red_time = int(self.red_var.get())

            if green_time <= 0 or red_time <= 0:
                messagebox.showwarning("Error", "Los tiempos deben ser mayores a 0")
                return

            # Formato de envío: G,R\n
            data_to_send = f"{green_time},{red_time}\n"

            # Conexión serie
            if self.serial_port is None or not self.serial_port.is_open or self.current_port_name != port:
                if self.serial_port and self.serial_port.is_open:
                    self.serial_port.close()
                self.serial_port = serial.Serial(port, 9600, timeout=1)
                self.current_port_name = port
                # Pequeña pausa al abrir puerto si es Arduino real (para el auto-reset)
                time.sleep(1.5)

            self.serial_port.write(data_to_send.encode('utf-8'))
            self.serial_port.flush() # Asegurar que se vacie el buffer

            messagebox.showinfo("Éxito", f"Tiempos enviados:\nVerde: {green_time}s\nRojo: {red_time}s")

        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos")
        except serial.SerialException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar al puerto {port}.\n\nDetalle: {e}")

    def on_closing(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SemaforoApp(root)
    root.mainloop()
