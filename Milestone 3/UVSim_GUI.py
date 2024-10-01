import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from UVSim import LogicalOperator

logic = LogicalOperator()



def open_file():
    """Open a file for editing."""
    file_path = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not file_path:
        set_file_label_text("File not found")
    txt_edit.delete(0, "end")
    with open(file_path, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        read_in_words(file_path)
        set_output_text("")
        add_output_text(file_path)
        add_output_text(text)
        set_file_label_text("Opened")
        
    window.title(f"Simple Text Editor - {file_path}")

def run_file():
    logic.run_file(logic)

def set_file_label_text(text):
    file_text["text"] = text

def set_output_text(text):
    ''' Set the output text box '''
    output_text["text"] = text

def add_output_text(text):
    ''' Add a new line to the output text '''
    output_text["text"] = output_text["text"] + text + "\n"

def read_in_words(file_path):
    logic.read_txt_file(file_path)

# Full window
window = tk.Tk()
window.title("Simple Text Editor")

window.rowconfigure(0, minsize=200, weight=1)
window.columnconfigure(1, minsize=1200, weight=1)

# Left Column
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2, width=900)
frm_buttons.grid(row=0, column=0, sticky="ns")

btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_run = tk.Button(frm_buttons, text="Run File", command=run_file)
btn_run.grid(row=1, column=0, padx=5, pady=5)

file_text = tk.Label(frm_buttons, text="-", justify="left")
file_text.grid(row=3, column=0, sticky="w")

# Right Column
output_text = tk.Label(text="output will appear here", justify="left")
output_text.grid(row=0, column=1, sticky="nw")

txt_edit = tk.Entry(window)
txt_edit.grid(row=1, column=1, sticky="sew")


window.mainloop()