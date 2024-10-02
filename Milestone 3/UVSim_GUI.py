import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from UVSim import LogicalOperator


class Interface():
    def open_file(self):
        """Open a file for editing."""
        file_path = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            set_file_label_text("File not found")
        txt_edit.delete(0, "end")
        with open(file_path, mode="r", encoding="utf-8") as input_file:
            text = input_file.read()
            self.read_in_words(file_path)
            self.set_output_text("")
            self.add_output_text(file_path)
            self.add_output_text(text)
            self.set_file_label_text("Opened")
            
        window.title(f"Simple Text Editor - {file_path}")

    def run_file(self):
        logic.reset_to_default()
        logic.run_command()

    def set_file_label_text(self, text):
        file_text["text"] = text

    def set_output_text(self, text):
        ''' Set the output text box '''
        output_text["text"] = text

    def add_output_text(self, text):
        ''' Add a new line to the output text '''
        output_text["text"] = output_text["text"] + str(text) + "\n"

    def read_in_words(self, file_path):
        logic.read_txt_file(file_path)

    def save_input(self, _event):
        user_input = txt_edit.get()
        print(f"input is {user_input}")
        logic.handle_input(user_input)
        txt_edit.delete(0, tk.END)

interface = Interface()
logic = LogicalOperator(interface)


# Full window
window = tk.Tk()
window.title("Simple Text Editor")

window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(1, minsize=1000, weight=1)
 
window.rowconfigure(1,weight=1)

# Left Column
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, width=900)
frm_buttons.grid(row=0, column=0, sticky="ns")

btn_open = tk.Button(frm_buttons, text="Open", command=interface.open_file)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_run = tk.Button(frm_buttons, text="Run File", command=interface.run_file)
btn_run.grid(row=1, column=0, padx=5, pady=5)

file_text = tk.Label(frm_buttons, text="-", justify="left")
file_text.grid(row=3, column=0, sticky="w")

# Right Column
output_text = tk.Label(text="output will appear here", justify="left")
output_text.grid(row=0, column=1, sticky="nw")

instruct = tk.Label(text="Enter your input: ", justify="left", height=1)
instruct.grid(row=0, column=1, sticky="sw")

txt_edit = tk.Entry(window)
txt_edit.grid(row=0, column=1, sticky="swe", padx=100)
txt_edit.bind('<Return>', interface.save_input)

spacer = tk.Label(text="", justify="left", height=1)
spacer.grid(row=1, column=1, sticky="s")


window.mainloop()