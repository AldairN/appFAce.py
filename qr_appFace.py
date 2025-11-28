import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk

# Metodo QR
def qr_iteration(A, tol=1e-8, max_iter=1000):
    A = np.array(A, dtype=float)
    for _ in range(max_iter):
        Q, R = np.linalg.qr(A)
        A_new = R @ Q
        if np.linalg.norm(A_new - A) < tol:
            break
        A = A_new
    return np.diag(A), A

# Funciones
def load_matrix():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
    if not file_path:
        return
    try:
        matriz = np.loadtxt(file_path, delimiter=",", dtype=float)
        entry.delete("1.0", tk.END)
        entry.insert(tk.END, "\n".join(",".join(map(str, row)) for row in matriz))
    except:
        messagebox.showerror("Error", "No se pudo leer el archivo.")
#leer matriz e imprimir resultado
def calculate():
    try:
        raw = entry.get("1.0", tk.END).strip().split("\n")
        matriz = [list(map(float, row.split(","))) for row in raw]
        eigenvalues, A_final = qr_iteration(matriz)

        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Autovalores de características faciales:\n")
        result_box.insert(tk.END, str(eigenvalues) + "\n\n")
        result_box.insert(tk.END, "Matriz procesada tras la Iteración QR:\n")
        result_box.insert(tk.END, str(A_final))
        result_box.config(state="disabled")
    except Exception as e:
        messagebox.showerror("Error", f"Entrada inválida.\n{e}")
# imprimir en archivo
def save_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if not file_path:
        return
    with open(file_path, "w") as f:
        f.write(result_box.get("1.0", tk.END))
    messagebox.showinfo("Guardado", "Resultados guardados exitosamente.")

# Interfaz
root = tk.Tk()
root.title("EigenFace Analyzer — Sistema QR para Reconocimiento Facial")
root.geometry("700x750")
root.configure(bg="#e9ecf2")

style = ttk.Style()
style.configure("TButton", padding=8, font=("Arial", 11), relief="flat")
style.map("TButton", background=[("active", "#d1d5db")])
style.configure("TLabel", font=("Arial", 12), background="#e9ecf2")
banner = tk.Frame(root, bg="#4a6fa5", height=70)
banner.pack(fill="x")
banner_title = tk.Label(
    banner, text="EigenFace Analyzer", 
    bg="#4a6fa5", fg="white", 
    font=("Arial", 20, "bold")
)
banner_title.pack(pady=15)

entry_label = ttk.Label(
    root, 
    text="Ingrese la matriz de características de la imagen (separada por comas):"
)
entry_label.pack(pady=5)
entry_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
entry_frame.pack(pady=5)
entry = tk.Text(entry_frame, height=8, width=65, font=("Consolas", 12), bd=0)
entry.pack(padx=5, pady=5)

button_frame = tk.Frame(root, bg="#e9ecf2")
button_frame.pack(pady=12)
ttk.Button(button_frame, text="Cargar matriz", command=load_matrix).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="Analizar Autovalores", command=calculate).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="Guardar resultados", command=save_results).grid(row=0, column=2, padx=10)

result_label = ttk.Label(root, text="Resultados del Análisis Facial:")
result_label.pack(pady=8)
result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="sunken")
result_frame.pack(pady=5)
result_box = tk.Text(result_frame, height=16, width=65, font=("Consolas", 12), bd=0, state="disabled")
result_box.pack(padx=5, pady=5)

root.mainloop()
