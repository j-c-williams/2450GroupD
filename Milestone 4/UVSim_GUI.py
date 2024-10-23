import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from UVSim import LogicalOperator
from UVSim_FileHandler import FileHandler
import re

class Interface:
    def __init__(self):
        self.file_handler = FileHandler()
        self.file_loaded = False
        self.edit_filepath = ""

    def open_file(self):
        '''Open a file on the main screen to run.'''
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

    def open_file_edit(self):
        '''Open a file on the edit screen to edit.'''
        file_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.edit_filepath = file_path

            with open(file_path, 'r') as file:
                file_contents = file.read()

            file_edit.config(state="normal")
            file_edit.delete('1.0', tk.END)
            
            file_edit.insert(tk.END, file_contents)
            file_edit.config(state="disabled")

            btn_edit_save.config(state="normal")
            file_edit.config(state="normal")
            btn_edit_save_as.config(state="normal")
        else:
            btn_edit_save.config(state="disabled")
            file_edit.config(state="disabled")
            btn_edit_save_as.config(state="disabled")
    
    def save_as_file_edit(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),("All files", "*.*")])
        if not file_path:
            print("Invalid file_path in save_as")
            return
        if not self.validate_valid_edits():
            print("edit failed validation in save_as")
            return

        file_contents = file_edit.get('1.0', tk.END)

        with open(file_path, 'w') as file:
            file.write(file_contents)

        print(f"File saved at: {file_path}")
        messagebox.showinfo("Save As - Success", "File saved successfully!")
    
    def save_file_edit(self):
        if not self.edit_filepath:
            print("Invalid file_path in save_as")
            return
        if not self.validate_valid_edits():
            print("edit failed validation in save_as")
            return

        file_contents = file_edit.get('1.0', tk.END)

        with open(self.edit_filepath, 'w') as file:
            file.write(file_contents)

        print(f"File saved at: {self.edit_filepath}")
        messagebox.showinfo("Save As - Success", "File saved successfully!")

    def validate_valid_edits(self):
        file_contents = file_edit.get('1.0', tk.END)
        file_contents_list = file_contents.split("\n")
        print(file_contents_list)
        if len(file_contents_list) > 100:
            print("too many words, invalid")
            messagebox.showinfo("Save - Error", "Edited file is invalid, you may only have 100 registers.")
            return
        for word in file_contents_list:
            pattern = r"^[+-]\d{4}$"
    
            # check if the string follows the pattern, and has text otherwise its just extra newlines
            if not re.match(pattern, word) and word:
                print(f"\"{word}\" failed to validate")
                messagebox.showinfo("Save - Error", "Edited file is invalid, each line must be a 4 digit signed integer.")
                return False
                
        return True
    
    def limit_lines(self):
        # Get number of lines
        total_lines = int(file_edit.index('end-1c').split('.')[0])  # Line count
        
        # If its over the limit of 100 lines (words), delete the last one
        if total_lines > 100:
            messagebox.showwarning("Warning", "Maximum of 100 lines allowed.")
            file_edit.delete('100.0', tk.END)

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
edit_screen.grid(row=0, column=0, sticky="nesw")

left_col = tk.Frame(edit_screen)
left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

right_col = tk.Frame(edit_screen)
right_col.grid(row=0, column=1, sticky="ne", padx=30, pady=10)

edit_label = tk.Label(right_col, text="Edit File", font=("Arial", 18))
edit_label.grid(row=0, column=0)
edit_label.pack(pady=50)

file_edit = tk.Text(right_col, width=100, height=20)
file_edit.insert("1.0", "Open a file to edit it.")
file_edit.config(state="disabled")
file_edit.pack(pady=10)
file_edit.bind("<KeyRelease>", interface.limit_lines)

btn_edit_file = tk.Button(left_col, text="Open File", command=lambda: interface.open_file_edit(), width=20, padx=30)
btn_edit_file.pack(pady=10)

btn_edit_save = tk.Button(left_col, text="Save File", command=lambda: interface.save_file_edit(), width=20, padx=30)
btn_edit_save.pack(pady=10)
btn_edit_save.config(state="disabled")

btn_edit_save_as = tk.Button(left_col, text="Save As", command=lambda: interface.save_as_file_edit(), width=20, padx=30)
btn_edit_save_as.pack(pady=10)
btn_edit_save_as.config(state="disabled")

btn_main_screen = tk.Button(left_col, text="Back to Main Screen", command=lambda: interface.show_frame(main_screen), width=20, padx=30)
btn_main_screen.pack(pady=10)

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
