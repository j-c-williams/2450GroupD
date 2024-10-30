import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from UVSim import LogicalOperator
from UVSim_FileHandler import FileHandler
import re
import pickle
import os

def load_color_scheme():
    """Load saved color scheme or return defaults"""
    try:
        with open('.color_config.pkl', 'rb') as f:
            colors = pickle.load(f)
            return colors
    except FileNotFoundError:
        return {
            'primary_color': "#4C721D",  # UVU Green
            'secondary_color': "#FFFFFF",  # White
            'text_color_on_primary': "#FFFFFF",
            'text_color_on_secondary': "#4C721D",
            'primary_button_hover_color': "#5d8b24",
            'secondary_button_hover_color': "#F5F5F5"
        }

def save_color_scheme(colors):
    """Save color scheme to file"""
    with open('.color_config.pkl', 'wb') as f:
        pickle.dump(colors, f)

# Initial color scheme setup
colors = load_color_scheme()

def on_button_hover(event):
    button = event.widget
    current_bg = button.cget('bg')
    if current_bg == interface.primary_color.get():
        button.configure(bg=colors['primary_button_hover_color'])
    else:
        button.configure(bg=colors['secondary_button_hover_color'])

def on_button_leave(event):
    button = event.widget
    # Check if this is a primary or secondary button based on its foreground color
    is_primary = button.cget('fg') == interface.text_color_on_primary.get()
    button.configure(bg=interface.primary_color.get() if is_primary else interface.secondary_color.get())

def style_button(button, is_primary=True):
    button.configure(
        bg=colors['primary_color'] if is_primary else colors['secondary_color'],
        fg=colors['text_color_on_primary'] if is_primary else colors['text_color_on_secondary'],
        activebackground=colors['primary_button_hover_color'] if is_primary else colors['secondary_button_hover_color'],
        activeforeground=colors['text_color_on_primary'] if is_primary else colors['text_color_on_secondary'],
        bd=0,
        relief="flat"
    )
    button.bind("<Enter>", on_button_hover)
    button.bind("<Leave>", on_button_leave)

# Root setup
root = tk.Tk()
root.title("UVSim GUI")
root.geometry("1200x700")

class Interface:
    def __init__(self):
        self.file_handler = FileHandler()
        self.file_loaded = False
        self.edit_filepath = ""

        self.primary_color = tk.StringVar(value=colors['primary_color'])
        self.secondary_color = tk.StringVar(value=colors['secondary_color'])
        self.text_color_on_primary = tk.StringVar(value=colors['text_color_on_primary'])
        self.text_color_on_secondary = tk.StringVar(value=colors['text_color_on_secondary'])


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
    
    def update_colors(self):
        """Update all widgets with new colors"""
        # Update root and container
        root.configure(bg=self.primary_color.get())
        container.configure(bg=self.primary_color.get())
        
        # Update main screen
        main_screen.configure(bg=self.primary_color.get())
        frm_buttons.configure(bg=self.secondary_color.get())
        buttons_text.configure(bg=self.secondary_color.get(), fg=self.text_color_on_secondary.get())
        output_text.configure(bg=self.primary_color.get(), fg=self.text_color_on_primary.get())
        input_frame.configure(bg=self.primary_color.get())
        instruct.configure(bg=self.primary_color.get(), fg=self.text_color_on_primary.get())
        txt_edit.configure(
            bg=self.primary_color.get(),
            fg=self.text_color_on_primary.get(),
            insertbackground=self.text_color_on_primary.get()
        )
        settings_text.configure(bg=self.secondary_color.get(), fg=self.text_color_on_secondary.get())
        
        # Update edit screen
        edit_screen.configure(bg=self.primary_color.get())
        left_col.configure(bg=self.secondary_color.get())
        right_col.configure(bg=self.primary_color.get())
        edit_label.configure(bg=self.primary_color.get(), fg=self.text_color_on_primary.get())
        file_edit.configure(
            bg=self.primary_color.get(),
            fg=self.text_color_on_primary.get(),
            insertbackground=self.text_color_on_primary.get()
        )
        
        # Update color screen
        color_screen.configure(bg=self.primary_color.get())
        color_content.configure(bg=self.primary_color.get())
        color_label.configure(bg=self.primary_color.get(), fg=self.text_color_on_primary.get())
        controls_frame.configure(bg=self.primary_color.get())
        primary_section.configure(bg=self.primary_color.get())
        secondary_section.configure(bg=self.primary_color.get())
        primary_preview.configure(bg=self.primary_color.get())
        secondary_preview.configure(bg=self.secondary_color.get())
        
         # Update all buttons and ensure their hover states are correctS
        buttons = [btn_open, btn_run, btn_submit, btn_edit_screen, btn_color_screen,
                btn_edit_file, btn_edit_save, btn_edit_save_as, btn_main_screen, btn_edit_main_screen,
                btn_primary, btn_secondary, btn_reset]
        
        for button in buttons:
            # List only the secondary buttons
            is_secondary = button in [btn_primary, btn_secondary, btn_main_screen, btn_submit, btn_edit_save, btn_edit_save_as, btn_edit_file, btn_edit_main_screen]
            button.configure(
                bg=self.secondary_color.get() if is_secondary else self.primary_color.get(),
                fg=self.text_color_on_secondary.get() if is_secondary else self.text_color_on_primary.get(),
                activebackground=colors['secondary_button_hover_color'] if is_secondary else colors['primary_button_hover_color'],
                activeforeground=self.text_color_on_secondary.get() if is_secondary else self.text_color_on_primary.get()
            )

    def pick_primary_color(self):
        """Open color picker for primary color"""
        color = askcolor(color=self.primary_color.get(), title="Choose Primary Color")
        if color[1]:  # If a color was chosen (not cancelled)
            colors['primary_color'] = color[1]
            self.primary_color.set(color[1])
            
            # Calculate text colors based on brightness
            rgb = tuple(int(color[1][i:i+2], 16) for i in (1, 3, 5))
            brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
            
            # Set text colors
            new_text_color = "#FFFFFF" if brightness < 128 else "#000000"
            colors['text_color_on_primary'] = new_text_color
            self.text_color_on_primary.set(new_text_color)
            
            # Text on secondary uses primary color
            colors['text_color_on_secondary'] = color[1]
            self.text_color_on_secondary.set(color[1])
            
            # Calculate hover color - lighten the primary color
            hover_rgb = tuple(min(255, int(c * 1.1)) for c in rgb)  # Lighten by 10%
            colors['primary_button_hover_color'] = '#{:02x}{:02x}{:02x}'.format(*hover_rgb)
            
            save_color_scheme(colors)
            self.update_colors()

    def pick_secondary_color(self):
        """Open color picker for secondary color"""
        color = askcolor(color=self.secondary_color.get(), title="Choose Secondary Color")
        if color[1]:  # If a color was chosen (not cancelled)
            colors['secondary_color'] = color[1]
            self.secondary_color.set(color[1])
            
            # Calculate hover color - for white/light colors, slightly darken
            rgb = tuple(int(color[1][i:i+2], 16) for i in (1, 3, 5))
            hover_rgb = tuple(int(c * 0.9) for c in rgb)  # Darken by 10%
            colors['secondary_button_hover_color'] = '#{:02x}{:02x}{:02x}'.format(*hover_rgb)
            
            save_color_scheme(colors)
            self.update_colors()

    def reset_colors(self):
        """Reset colors to UVU default"""
        global colors  
        colors = {
            'primary_color': "#4C721D",
            'secondary_color': "#FFFFFF",
            'text_color_on_primary': "#FFFFFF",
            'text_color_on_secondary': "#4C721D",
            'primary_button_hover_color': "#5d8b24",  
            'secondary_button_hover_color': "#F0F0F0" 
        }
        
        # Update all tkinter variables
        self.primary_color.set(colors['primary_color'])
        self.secondary_color.set(colors['secondary_color'])
        self.text_color_on_primary.set(colors['text_color_on_primary'])
        self.text_color_on_secondary.set(colors['text_color_on_secondary'])
        
        save_color_scheme(colors)
        self.update_colors()

interface = Interface()
logic = LogicalOperator(interface, interface.file_handler)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Create a container to stack all screens
container = tk.Frame(root, bg=interface.primary_color.get())
container.pack(fill="both", expand=True)

container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Main screen Frame
main_screen = tk.Frame(container, bg=interface.primary_color.get())
main_screen.grid(row=0, column=0, sticky="nsew")

main_screen.grid_rowconfigure(0, weight=1)
main_screen.grid_columnconfigure(0, weight=1)
main_screen.grid_columnconfigure(1, weight=10)

# ----- Main Screen Layout -----
# Left Column
frm_buttons = tk.Frame(main_screen, relief=tk.RAISED, bd=2, width=900, bg=interface.secondary_color.get())
frm_buttons.grid(row=0, column=0, sticky="ns")

buttons_text = tk.Label(frm_buttons, text="Run/Open", justify="left")
buttons_text.configure(
    bg=interface.secondary_color.get(),
    fg=interface.text_color_on_secondary.get()
)
buttons_text.grid(row=0, column=0, sticky="w", pady=5)

btn_open = tk.Button(frm_buttons, text="Open File", command=interface.open_file, width=12)
style_button(btn_open, True)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

btn_run = tk.Button(frm_buttons, text="Run File", command=interface.run_file, width=12)
style_button(btn_run, True)
btn_run.grid(row=2, column=0, padx=5, pady=5)

# Right Column
output_text = tk.Label(main_screen, text="Output will appear here\n", justify="left")
output_text.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get()
)
output_text.grid(row=0, column=1, sticky="nw")

# Input frame
input_frame = tk.Frame(main_screen, bg=interface.primary_color.get())
input_frame.grid(row=0, column=1, sticky="swe", padx=100, pady=20)
input_frame.grid_columnconfigure(1, weight=1)

instruct = tk.Label(input_frame, text="Enter your input: ", justify="left", height=1)
instruct.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get()
)
instruct.grid(row=0, column=0, sticky="sw")

txt_edit = tk.Entry(input_frame)
txt_edit.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get(),
    insertbackground=interface.text_color_on_primary.get()
)
txt_edit.insert(0, "Run a file with user input to enable text editing.")
txt_edit.grid(row=0, column=1, sticky="we", padx=(0, 5))
txt_edit.bind('<Return>', interface.save_input)
txt_edit.config(state="disabled")

btn_submit = tk.Button(input_frame, text="Submit", command=lambda: interface.save_input(None))
style_button(btn_submit, False)
btn_submit.grid(row=0, column=2, sticky="e")
btn_submit.config(state="disabled")

# Settings section
settings_text = tk.Label(frm_buttons, text="Settings/Edit", justify="left")
settings_text.configure(
    bg=interface.secondary_color.get(),
    fg=interface.text_color_on_secondary.get()
)
settings_text.grid(row=3, column=0, sticky="w", pady=(50,5))

btn_edit_screen = tk.Button(frm_buttons, text="Edit File", 
                           command=lambda: interface.show_frame(edit_screen), width=12)
style_button(btn_edit_screen, True)
btn_edit_screen.grid(row=4, column=0, padx=5, pady=5)

btn_color_screen = tk.Button(frm_buttons, text="Edit Colors",
                            command=lambda: interface.show_frame(color_screen), width=12)
style_button(btn_color_screen, True)
btn_color_screen.grid(row=5, column=0, padx=5, pady=5)

# ----- Edit Screen Layout -----
edit_screen = tk.Frame(container, bg=interface.primary_color.get())
edit_screen.grid(row=0, column=0, sticky="nesw")

left_col = tk.Frame(edit_screen, bg=interface.secondary_color.get())
left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

right_col = tk.Frame(edit_screen, bg=interface.primary_color.get())
right_col.grid(row=0, column=1, sticky="ne", padx=30, pady=10)

edit_label = tk.Label(right_col, text="Edit File", font=("Arial", 18))
edit_label.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get()
)
edit_label.pack(pady=50)

file_edit = tk.Text(right_col, width=100, height=20)
file_edit.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get(),
    insertbackground=interface.text_color_on_primary.get()
)
file_edit.insert("1.0", "Open a file to edit it.")
file_edit.config(state="disabled")
file_edit.pack(pady=10)
file_edit.bind("<KeyRelease>", interface.limit_lines)

# Style edit screen buttons
btn_edit_file = tk.Button(left_col, text="Open File", 
                         command=lambda: interface.open_file_edit(), width=20)
style_button(btn_edit_file, False)
btn_edit_file.pack(pady=10)

btn_edit_save = tk.Button(left_col, text="Save File",
                         command=lambda: interface.save_file_edit(), width=20)
style_button(btn_edit_save, False)
btn_edit_save.pack(pady=10)
btn_edit_save.config(state="disabled")

btn_edit_save_as = tk.Button(left_col, text="Save As",
                            command=lambda: interface.save_as_file_edit(), width=20)
style_button(btn_edit_save_as, False)
btn_edit_save_as.pack(pady=10)
btn_edit_save_as.config(state="disabled")

btn_edit_main_screen = tk.Button(left_col, text="Back to Main Screen",
                           command=lambda: interface.show_frame(main_screen), width=20)
style_button(btn_edit_main_screen, False)
btn_edit_main_screen.pack(pady=10)

# ----- Color Screen Layout -----
color_screen = tk.Frame(container, bg=interface.primary_color.get())
color_screen.grid(row=0, column=0, sticky="nsew")

color_content = tk.Frame(color_screen, bg=interface.primary_color.get())
color_content.place(relx=0.5, rely=0.5, anchor="center")

color_label = tk.Label(color_content, text="Color Configuration", font=("Arial", 24))
color_label.configure(
    bg=interface.primary_color.get(),
    fg=interface.text_color_on_primary.get()
)
color_label.pack(pady=(0, 30))

# Create a frame for all controls in a column
controls_frame = tk.Frame(color_content, bg=interface.primary_color.get())
controls_frame.pack(pady=20)

# Primary color section
primary_section = tk.Frame(controls_frame, bg=interface.primary_color.get())
primary_section.pack(pady=10)

btn_primary = tk.Button(primary_section, text="Change Primary Color",
                       command=lambda: interface.pick_primary_color())
style_button(btn_primary, False)
btn_primary.pack(side="left", padx=10)

primary_preview = tk.Frame(primary_section, width=50, height=50)
primary_preview.configure(
    bg=interface.primary_color.get(),
    highlightbackground="black",
    highlightthickness=1
)
primary_preview.pack(side="left", padx=10)
primary_preview.pack_propagate(False)

# Secondary color section
secondary_section = tk.Frame(controls_frame, bg=interface.primary_color.get())
secondary_section.pack(pady=10)

btn_secondary = tk.Button(secondary_section, text="Change Secondary Color",
                         command=lambda: interface.pick_secondary_color())
style_button(btn_secondary, False)
btn_secondary.pack(side="left", padx=10)

secondary_preview = tk.Frame(secondary_section, width=50, height=50)
secondary_preview.configure(
    bg=interface.secondary_color.get(),
    highlightbackground="black",
    highlightthickness=1
)
secondary_preview.pack(side="left", padx=10)
secondary_preview.pack_propagate(False)

# Reset button
btn_reset = tk.Button(controls_frame, text="Reset to Default Colors",
                     command=lambda: interface.reset_colors())
style_button(btn_reset, True)
btn_reset.pack(pady=10)

# Back button
btn_main_screen = tk.Button(controls_frame, text="Back to Main Screen",
                           command=lambda: interface.show_frame(main_screen))
style_button(btn_main_screen, False)
btn_main_screen.pack(pady=10)

interface.show_frame(main_screen)

# Start the GUI loop
root.mainloop()