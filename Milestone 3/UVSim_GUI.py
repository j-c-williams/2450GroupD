import tkinter as tk
from tkinter.filedialog import askopenfilename
from UVSim import LogicalOperator
from UVSim_FileHandler import FileHandler


class Interface:
    def __init__(self):
        self.file_handler = FileHandler()

    def open_file(self):
        """Open a file for editing."""
        file_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            self.set_file_label_text("File not found")
            return

        self.set_file_label_text("Opening file...")
        logic.load_file(file_path)
        self.set_output_text("")
        self.add_output_text(f"File loaded: {file_path}")
        self.add_output_text("Program loaded into memory.")

        window.title(f"UVSim - {file_path}")

    def run_file(self):
        """Runs the loaded program."""
        logic.reset_to_default()  # Reset pointer and accumulator for a new run
        logic.run_command()       # Start execution of the first command

    def set_file_label_text(self, text):
        file_text["text"] = text

    def set_output_text(self, text):
        ''' Set the output text box '''
        output_text["text"] = text

    def add_output_text(self, text):
        ''' Add a new line to the output text '''
        output_text["text"] = output_text["text"] + str(text) + "\n"

    def save_input(self, _event):
        user_input = txt_edit.get()
        print(f"User input: {user_input}")
        logic.handle_input(user_input)  # Handle user input in LogicalOperator
        txt_edit.delete(0, tk.END)      # Clear input field after submission

# Set up the interface and logic layer
interface = Interface()
logic = LogicalOperator(interface, interface.file_handler)

# Full window setup
window = tk.Tk()
window.title("UVSim GUI")

window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(1, minsize=1000, weight=1)
window.rowconfigure(1, weight=1)

# Left Column
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, width=900)
frm_buttons.grid(row=0, column=0, sticky="ns")

btn_open = tk.Button(frm_buttons, text="Open File", command=interface.open_file)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_run = tk.Button(frm_buttons, text="Run File", command=interface.run_file)
btn_run.grid(row=1, column=0, padx=5, pady=5)

file_text = tk.Label(frm_buttons, text="-", justify="left")
file_text.grid(row=3, column=0, sticky="w")

# Right Column for Output
output_text = tk.Label(text="Output will appear here", justify="left")
output_text.grid(row=0, column=1, sticky="nw")

instruct = tk.Label(text="Enter your input: ", justify="left", height=1)
instruct.grid(row=0, column=1, sticky="sw")

txt_edit = tk.Entry(window)
txt_edit.grid(row=0, column=1, sticky="swe", padx=100)
txt_edit.bind('<Return>', interface.save_input)  # Process input on "Enter"

spacer = tk.Label(text="", justify="left", height=1)
spacer.grid(row=1, column=1, sticky="s")

# Start the GUI loop
window.mainloop()
