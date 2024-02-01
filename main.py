# main.py

import tkinter as tk
from tkinter import filedialog, messagebox
import processing  # Make sure processing.py is in the same directory or its path is added to sys.path


def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("NDAX files", "*.ndax")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)


def execute():
    file_path = file_path_entry.get()
    try:
        theoretical_capacity = float(theoretical_capacity_entry.get())
        min_cycle = int(min_cycle_entry.get()) if min_cycle_entry.get() else 0  # Defaulting to 0 if empty
        max_cycle = int(max_cycle_entry.get()) if max_cycle_entry.get() else None  # No default, stays None if empty
        save_image = save_image_var.get()

        # Assuming you have these functions properly defined in processing.py
        processing.print_ndax_as_csv(file_path)
        processing.plot_capacity(file_path, theoretical_capacity, {}, min_cycle, max_cycle, save_image)

        messagebox.showinfo("Success", "Operation completed successfully")
    except ValueError as e:
        messagebox.showerror("Error", "Please check your input values")


app = tk.Tk()
app.title("Capacity Plotter")

# Setup the UI
file_path_entry = tk.Entry(app, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=browse_file).grid(row=0, column=2, padx=10, pady=10)
tk.Label(app, text="File Path:").grid(row=0, column=0, padx=10, pady=10)

theoretical_capacity_entry = tk.Entry(app)
theoretical_capacity_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Label(app, text="Theoretical Capacity:").grid(row=1, column=0, padx=10, pady=10)

min_cycle_entry = tk.Entry(app)
min_cycle_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Label(app, text="Min Cycle:").grid(row=2, column=0, padx=10, pady=10)

max_cycle_entry = tk.Entry(app)
max_cycle_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Label(app, text="Max Cycle:").grid(row=3, column=0, padx=10, pady=10)

save_image_var = tk.BooleanVar()
tk.Checkbutton(app, text="Save Image", variable=save_image_var).grid(row=4, column=1, padx=10, pady=10, sticky='w')
tk.Label(app, text="Save Image:").grid(row=4, column=0, padx=10, pady=10)

tk.Button(app, text="Execute", command=execute).grid(row=5, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()
