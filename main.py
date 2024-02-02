# main.py

import tkinter as tk
from tkinter import filedialog, messagebox
import processing  # Ensure processing.py is accessible
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("NDAX files", "*.ndax")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)


def execute():
    file_path = file_path_entry.get()
    print_csv = print_csv_var.get()
    save_image = save_image_var.get()
    plot_type = plot_type_var.get()
    try:
        theoretical_capacity = float(theoretical_capacity_entry.get())
        min_cycle = int(min_cycle_entry.get()) if min_cycle_entry.get() else 0  # Default to 0 if empty
        max_cycle = int(max_cycle_entry.get()) if max_cycle_entry.get() else None  # Stay None if empty

        # Conditional execution based on user choices
        if print_csv:
            processing.print_ndax_as_csv(file_path)

        if plot_type == "Capacity":
            fig = processing.plot_capacity(file_path, theoretical_capacity, {}, min_cycle, max_cycle, save_image)
        elif plot_type == "Voltage":
            fig = processing.plot_voltage(file_path, min_cycle, max_cycle, save_image)

        fig = processing.plot_capacity(file_path, theoretical_capacity, {}, min_cycle, max_cycle, save_image)

        for widget in app.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

        # Display the plot in the UI
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().grid(row=7, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)

        # Add the toolbar
        toolbar_frame = tk.Frame(master=app)  # Creating a frame for the toolbar
        toolbar_frame.grid(row=8, column=0, columnspan=3, padx=10, pady=10)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()

        app.grid_rowconfigure(7, weight=1)
        app.grid_columnconfigure(0, weight=1)

        messagebox.showinfo("Success", "Operation completed successfully", parent=app)
    except ValueError as e:
        messagebox.showerror("Error", "Please check your input values", parent=app)


app = tk.Tk()
app.title("Capacity Plotter")

app.iconbitmap('assets/app_icon.ico')

# Apply dark theme colors
dark_bg = "#333333"
light_fg = "#ffffff"
button_bg = "#555555"
entry_bg = "#505050"

app.configure(bg=dark_bg)

# Configure widget styles for dark theme
style_options = {'bg': dark_bg, 'fg': light_fg}

# File path selection
file_path_entry = tk.Entry(app, width=50, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=browse_file, bg=button_bg, fg=light_fg).grid(row=0, column=2, padx=10, pady=10)
tk.Label(app, text="File Path:", **style_options).grid(row=0, column=0, padx=10, pady=10)

# Theoretical capacity entry
theoretical_capacity_entry = tk.Entry(app, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
theoretical_capacity_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Label(app, text="Theoretical Capacity (mAh):", **style_options).grid(row=1, column=0, padx=10, pady=10)

# Min cycle entry
min_cycle_entry = tk.Entry(app, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
min_cycle_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Label(app, text="Min Cycle (optional):", **style_options).grid(row=2, column=0, padx=10, pady=10)

# Max cycle entry
max_cycle_entry = tk.Entry(app, bg=entry_bg, fg=light_fg, insertbackground=light_fg)
max_cycle_entry.grid(row=3, column=1, padx=10, pady=10)
tk.Label(app, text="Max Cycle (optional):", **style_options).grid(row=3, column=0, padx=10, pady=10)

# Checkboxes for CSV and image saving
print_csv_var = tk.BooleanVar()
save_image_var = tk.BooleanVar()
tk.Checkbutton(app, text="Print CSV", variable=print_csv_var, selectcolor=dark_bg, **style_options).grid(row=4,
                                                                                                         column=1,
                                                                                                         sticky='w',
                                                                                                         padx=10,
                                                                                                         pady=10)
tk.Checkbutton(app, text="Save Image", variable=save_image_var, selectcolor=dark_bg, **style_options).grid(row=4,
                                                                                                           column=2,
                                                                                                           sticky='w',
                                                                                                           padx=10,
                                                                                                           pady=10)

#capacity or V plot
plot_type_var = tk.StringVar(value="Capacity")
tk.Radiobutton(app, text="Capacity", variable=plot_type_var, value="Capacity", bg=dark_bg, fg=light_fg).grid(row=5, column=1, sticky='w', padx=10, pady=10)
tk.Radiobutton(app, text="Voltage", variable=plot_type_var, value="Voltage", bg=dark_bg, fg=light_fg).grid(row=5, column=2, sticky='w', padx=10, pady=10)


# Execute button
tk.Button(app, text="Execute", command=execute, bg=button_bg, fg=light_fg).grid(row=6, column=0, columnspan=3, padx=10,
                                                                                pady=10)

app.mainloop()
