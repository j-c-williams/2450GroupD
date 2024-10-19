import tkinter as tk
from tkinter.filedialog import askopenfilename
from UVSim import LogicalOperator
from UVSim_FileHandler import FileHandler


class Interface:
    def __init__(self):
        self.file_handler = FileHandler()
        self.file_loaded = False

    def open_file(self):
        '''Open a file for editing.'''
        file_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            self.disable_user_input()
            return

        self.file_loaded = True

        logic.load_file(file_path)
        self.set_output_text("")
        self.add_output_text(f"File loaded: {file_path}")
        self.add_output_text("Program loaded into memory. Click 'Run File' to run the program.")

        root.title(f"UVSim - {file_path}")

    def run_file(self):
        '''Runs the loaded program.'''
        if not self.file_loaded:
            self.add_output_text("File not loaded, open a file to run commands.")
            return
        logic.reset_to_default()
        logic.run_command()

    def set_output_text(self, text):
        ''' Set the output text box '''
        output_text["text"] = text

    def add_output_text(self, text):
        ''' Add a new line to the output text '''
        output_text["text"] = output_text["text"] + str(text) + "\n"

    def save_input(self, _event):
        user_input = txt_edit.get()
        print(f"User input: {user_input}")
        logic.handle_input(user_input)
        txt_edit.delete(0, tk.END)
    
    def show_frame(self, frame):
        ''' Raise the selected frame to switch screens '''
        frame.tkraise()

    def enable_user_input(self):
        self.file_loaded = True
        txt_edit.config(state="normal")
        txt_edit.delete(0, tk.END)
        btn_submit.config(state="normal")

    def disable_user_input(self):
        self.file_loaded = False
        txt_edit.delete(0, tk.END)
        txt_edit.insert(0, "Run a file with user input to enable text editing.")
        txt_edit.config(state="disabled")
        btn_submit.config(state="disabled")


interface = Interface()
logic = LogicalOperator(interface, interface.file_handler)

# Root setup
root = tk.Tk()
root.title("UVSim GUI")
root.geometry("1200x700")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a container to stack all screens
container = tk.Frame(root)
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Main screen Frame
main_screen = tk.Frame(container)
main_screen.grid(row=0, column=0, sticky="nsew")

main_screen.grid_rowconfigure(0, weight=1)
main_screen.grid_columnconfigure(0, weight=1)
main_screen.grid_columnconfigure(1, weight=10)

# ----- Main Screen Layout -----
# Left Column
frm_buttons = tk.Frame(main_screen, relief=tk.RAISED, bd=2, width=900)
frm_buttons.grid(row=0, column=0, sticky="ns")

buttons_text = tk.Label(frm_buttons, text="Run/Open", justify="left")
buttons_text.grid(row=0, column=0, sticky="w", pady=5)

btn_open = tk.Button(frm_buttons, text="Open File", command=interface.open_file, width=12)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

btn_run = tk.Button(frm_buttons, text="Run File", command=interface.run_file, width=12)
btn_run.grid(row=2, column=0, padx=5, pady=5)

# Right Column
output_text = tk.Label(main_screen, text="Output will appear here\n", justify="left")
output_text.grid(row=0, column=1, sticky="nw")

### Input frame to hold label, input and submit button
input_frame = tk.Frame(main_screen)
input_frame.grid(row=0, column=1, sticky="swe", padx=100, pady=20)
input_frame.grid_columnconfigure(1, weight=1)

instruct = tk.Label(input_frame, text="Enter your input: ", justify="left", height=1)
instruct.grid(row=0, column=0, sticky="sw")

txt_edit = tk.Entry(input_frame)
txt_edit.insert(0, "Run a file with user input to enable text editing.")
txt_edit.grid(row=0, column=1, sticky="we", padx=(0, 5))
txt_edit.bind('<Return>', interface.save_input)
txt_edit.config(state="disabled")

btn_submit = tk.Button(input_frame, text="Submit", command=lambda: interface.save_input(None), state="disabled")
btn_submit.grid(row=0, column=2, sticky="e")

# Button to navigate to the Edit screen
settings_text = tk.Label(frm_buttons, text="Settings/Edit", justify="left")
settings_text.grid(row=3, column=0, sticky="w", pady=(50,5))

btn_edit_screen = tk.Button(frm_buttons, text="Edit File", command=lambda: interface.show_frame(edit_screen), width=12)
btn_edit_screen.grid(row=4, column=0, padx=5, pady=5)

btn_color_screen = tk.Button(frm_buttons, text="Edit Colors", command=lambda: interface.show_frame(color_screen), width=12)
btn_color_screen.grid(row=5, column=0, padx=5, pady=5)

# ----- Edit Screen Layout -----
edit_screen = tk.Frame(container)
edit_screen.grid(row=0, column=0, sticky="nsew")

edit_label = tk.Label(edit_screen, text="Edit Screen", font=("Arial", 18))
edit_label.pack(pady=50)

btn_main_screen = tk.Button(edit_screen, text="Back to Main Screen", command=lambda: interface.show_frame(main_screen))
btn_main_screen.pack()

# ----- Color Screen Layout -----
color_screen = tk.Frame(container)
color_screen.grid(row=0, column=0, sticky="nsew")

color_label = tk.Label(color_screen, text="Edit Colors", font=("Arial", 18))
color_label.pack(pady=50)

btn_main_screen = tk.Button(color_screen, text="Back to Main Screen", command=lambda: interface.show_frame(main_screen))
btn_main_screen.pack()

interface.show_frame(main_screen)

# Start the GUI loop
root.mainloop()
