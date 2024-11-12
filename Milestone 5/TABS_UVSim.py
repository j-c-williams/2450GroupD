import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from UVSim import LogicalOperator
from UVSim_FileHandler import FileHandler
import re
import pickle
import os

class Interface:
    def __init__(self):
        self.file_handler = FileHandler()
        self.file_loaded = False
        self.edit_filepath = ""
        self.accepting_input = False

        self.logic = LogicalOperator(self, self.file_handler)


        # References to the items in its tab
        self.run_screen = None
        self.text_edit = None
        self.user_entry = None
        self.submit_button = None

        # Edit screen
        self.edit_screen = None
        self.edit_textbox = None
        self.filepath_label = None

        self.primary_color = tk.StringVar(value=colors['primary_color'])
        self.secondary_color = tk.StringVar(value=colors['secondary_color'])
        self.text_color_on_primary = tk.StringVar(value=colors['text_color_on_primary'])
        self.text_color_on_secondary = tk.StringVar(value=colors['text_color_on_secondary'])    

        # previously a magic number, update when we change number of lines logic
        # found in validate_valid_edits() and limit_lines()
        self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE = 100

        # previously a magic pattern, update when we change words logic
        # found in validate_valid_edits()
        self.ACCEPTABLE_WORD_PATTERN = r"^[+-]\d{4}$"

    def open_file(self, preloaded_filepath = ""):
        '''Open a file on the main screen to run.'''

        if not preloaded_filepath:
            file_path = askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
        else:
            file_path = preloaded_filepath

        if not file_path:
            self.disable_user_input()
            return
        
        self.edit_filepath = file_path

        self.file_loaded = True

        self.logic.load_file(file_path)
        self.set_output_text("")
        self.add_output_text(f"File loaded: {file_path}")
        self.add_output_text("Program loaded into memory. Click 'Run File' to run the program.")

        root.title(f"UVSim - {file_path}")

    def run_file(self):
        '''Runs the loaded program.'''
        if not self.file_loaded:
            self.add_output_text("File not loaded, open a file to run commands.")
            return
        self.logic.reset_to_default()
        self.logic.run_command()

    def edit_file_transition(self):
        ''' On the normal run screen, open a text box to edit the file'''
        # raise the edit screen then open a file to edit
        if self.edit_screen:
            self.edit_screen.tkraise()

        # open a file if it's opened already, otherwise prompt for a new one
        self.open_file_edit(self.edit_filepath)

    def run_file_transition(self):
        ''' When transitioning back from the edit screen, load the edited file''' 
        # Raise run screen, then open the file that was edited
        # Discard changes button just raises screen without re-loading
        self.open_file(self.edit_filepath)
        self.add_output_text("Edited file loaded.")
        
        if self.run_screen:
            self.run_screen.tkraise()
        
    def set_output_text(self, text):
        ''' Set the output text box '''
        # References the text edit in it's tab directly
        if not self.text_edit:
            return
        self.text_edit.config(state="normal")
        self.text_edit.delete("1.0", tk.END)
        self.text_edit.insert("1.0", text)
        self.text_edit.config(state="disabled")

    def add_output_text(self, text):
        ''' Add a new line to the output text '''
        if not self.text_edit:
            return
        self.text_edit.config(state="normal")
        self.text_edit.insert(tk.END, str(text) + "\n")
        self.text_edit.config(state="disabled")

    def save_input(self, _event = None):
        ''' Save the input given from the user in the entry box'''
        user_input = self.user_entry.get()
        if user_input == "":
            # only accept if there is an input
            return
        if not self.accepting_input:
            # only run if the program is waiting for input
            return
        print(f"User input: {user_input}")
        self.logic.handle_input(user_input)

        # reference the user entry directly
        if self.user_entry:
            self.user_entry.delete(0, tk.END)

    def enable_user_input(self):
        ''' Enable the user entry textbox, show it is ready to accept input '''
        self.accepting_input = True

        if self.user_entry:
            self.user_entry.config(state="normal")
            self.user_entry.delete(0, tk.END)
        
        if self.submit_button:
            self.submit_button.config(state="normal")

    def disable_user_input(self):
        ''' Disables the user entry textbox, makes it clear it isn't waiting for input yet '''
        self.accepting_input = False
        
        if self.user_entry:
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, "Run a file with user input to enable text editing.")
            self.user_entry.config(state="disabled")
        
        if self.submit_button:
            self.submit_button.config(state="disabled")

    def open_file_edit(self, preloaded_filepath = ""):
        '''Open a file on the edit screen to edit. Use the given filepath if given'''
        
        # Load up given filepath if available, otherwise prompt
        if preloaded_filepath:
            file_path = preloaded_filepath
        else:
            file_path = askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
        
        if not file_path:
            self.disable_user_input()
            print("Opened file and no filepath was selected.")
            return
        

        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Reset the textbox to have the new file contents
        if self.edit_textbox:
            self.edit_textbox.config(state="normal")
            self.edit_textbox.delete('1.0', tk.END)
            self.edit_textbox.insert(tk.END, file_contents)
        
        # Set the label to show the current loaded file
        if self.filepath_label:
            self.filepath_label["text"] = file_path

        self.edit_filepath = file_path

    def save_as_file_edit(self):
        ''' Save As functionality for the edit screen. Prompt the user to choose how to save. '''
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"),("All files", "*.*")])
        
        if not self.edit_textbox:
            print("no edit screen textbox saved in interface")
            return
        
        file_contents = self.edit_textbox.get('1.0', tk.END)

        if not file_path:
            print("Invalid file_path in save_as")
            return
        if not self.validate_valid_edits(file_contents):
            print("edit failed validation in save_as")
            return
        
        # If we pass the sanity checks, execute

        with open(file_path, 'w') as file:
            file.write(file_contents)

        print(f"File saved at: {file_path}")
        messagebox.showinfo("Save As - Success", "File saved successfully!")

        # Transition back to the run screen with the new saved file.
        self.edit_filepath = file_path
        self.run_file_transition()
            
    def save_file_edit(self):
        ''' Save the file to the current filepath and go back to run screen '''

        if not self.edit_textbox:
            print("no edit textbox found in save_file")
        
        file_contents = self.edit_textbox.get('1.0', tk.END)

        if not self.edit_filepath:
            print("Invalid file_path in save_file")
            return
        if not self.validate_valid_edits(file_contents):
            print("edit failed validation in save_file")
            return

        with open(self.edit_filepath, 'w') as file:
            file.write(file_contents)

        print(f"File saved at: {self.edit_filepath}")
        messagebox.showinfo("Save As - Success", "File saved successfully!")

        self.run_file_transition()

    def validate_valid_edits(self, file_contents):
        ''' Check to see that the edits to the file are valid. ''' 
        file_contents_list = file_contents.split("\n")
        print(file_contents_list)
        if len(file_contents_list) > self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE:
            print("too many words, invalid")
            messagebox.showinfo("Save - Error", "Edited file is invalid, you may only have ",self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE, " registers.")
            return
        for word in file_contents_list:
            pattern = self.ACCEPTABLE_WORD_PATTERN
    
            # check if the string follows the pattern, and has text otherwise its just extra newlines
            if not re.match(pattern, word) and word:
                print(f"\"{word}\" failed to validate")
                messagebox.showinfo("Save - Error", "Edited file is invalid, each line must be a 4 digit signed integer.")
                return False
                
        return True
    
    def limit_lines(self, arg2 = ""):
        ''' Stop the user from creating more than the acceptable number of lines on the edit screen'''
        
        if not self.edit_textbox:
            print("Textbox not found in limit_lines")
            return

        # Get number of lines
        total_lines = int(self.edit_textbox.index('end-1c').split('.')[0])  # Line count
        
        # If its over the limit of 100 lines (words), delete the last one
        if total_lines > self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE:
            messagebox.showwarning("Warning", "Maximum of ",self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE, " lines allowed.")
            self.edit_textbox.delete(str(self.NUMBER_OF_ACCEPTABLE_LINES_IN_FILE), tk.END)
    
    def update_colors(self):
        ''' Update all widgets with new colors '''
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

class TabManager:
    def __init__(self, base, interface=None):
        self.base = base

        # Create the tabbed notebook
        self.notebook = ttk.Notebook(self.base)
        self.notebook.pack(expand=1, fill="both")

        self.tab_count = 0

        add_tab_button = tk.Button(self.base, text="Add Tab", command=self.add_tab)
        add_tab_button.pack(pady=5)

        self.tabbed_interfaces = {} # Dictionary to store interfaces by tab index

    def add_tab(self):
        ''' Adds a new tab with a close button inside the tab content. '''
        self.tab_count += 1

        # Create tab
        tab_frame = ttk.Frame(self.notebook)
        tab_name = f"Tab {self.tab_count}"
        
        # Add the created tab to the notebook
        self.notebook.add(tab_frame, text=tab_name)

        # Create new local tab interface
        self.tabbed_interfaces[tab_name] = Interface()

        # Create container to hold run and edit screens
        container = tk.Frame(tab_frame)
        container.pack()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create run screen ------------
        run_screen = tk.Frame(container)
        run_screen.pack(fill="both", expand=True)
        run_screen.grid(row=0, column=0, sticky="nsew")

        # Create columns for run screen
        left_col = tk.Frame(run_screen)
        left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        right_container = tk.Frame(run_screen)
        right_container.grid(row=0, column=1, sticky="w", padx=30, pady=10)

        # Left Column ----
        label = ttk.Label(left_col, text=f"This is {tab_name}")
        label.pack(padx=10, pady=10)

        open_button = ttk.Button(left_col, text="Open", command=self.tabbed_interfaces[tab_name].open_file)
        open_button.pack(pady=5)

        run_button = ttk.Button(left_col, text="Run File", command=self.tabbed_interfaces[tab_name].run_file)
        run_button.pack(pady=5)

        edit_button = ttk.Button(left_col, text="Edit File", command=lambda: self.tabbed_interfaces[tab_name].edit_file_transition())
        edit_button.pack(pady=5)

        color_button = ttk.Button(left_col, text="Change Colors", command=lambda: right_col.tkraise())
        color_button.pack(pady=5)

        close_button = ttk.Button(left_col, text="Close Tab", command=lambda: self.close_tab(tab_frame))
        close_button.pack(pady=5)

        # Right Column ----
        right_col = tk.Frame(right_container, height=35)
        right_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        # Title
        edit_label = tk.Label(right_col, text="Run File", font=("Arial", 18))
        edit_label.pack(pady=50)

        # Large text field
        file_edit = tk.Text(right_col, width=100)
        file_edit.insert("1.0", "Open a file to edit it.\n")
        file_edit.config(state="disabled")
        file_edit.pack(pady=10)

        # User input field
        txt_edit = tk.Entry(right_col, width=100)
        txt_edit.insert(0, "Run a file with user input to enable text editing.")
        txt_edit.bind('<Return>', self.tabbed_interfaces[tab_name].save_input)
        txt_edit.config(state="disabled")
        txt_edit.pack(padx=20)

        # Submit Button
        btn_submit = tk.Button(right_col, text="Submit", command=lambda: self.tabbed_interfaces[tab_name].save_input())
        style_button(btn_submit, False)
        btn_submit.config(state="disabled")
        btn_submit.pack(pady=10)

        # Resolve variables and save wigits into interface
        self.tabbed_interfaces[tab_name].run_screen = run_screen
        self.tabbed_interfaces[tab_name].text_edit = file_edit
        self.tabbed_interfaces[tab_name].user_entry = txt_edit
        self.tabbed_interfaces[tab_name].submit_button = btn_submit



        # Edit Screen ----------------
        edit_screen = tk.Frame(container)
        edit_screen.grid(row=0, column=0, sticky="nsew")

        edit_left_col = tk.Frame(edit_screen, height=35)
        edit_left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        edit_right_col = tk.Frame(edit_screen, height=35)
        edit_right_col.grid(row=0, column=1, sticky="w", padx=30, pady=10)
        
        # Left column ----
        label = ttk.Label(edit_left_col, text=f"This is {tab_name}")
        label.pack(padx=10, pady=10)

        color_button = ttk.Button(edit_left_col, text="Change Colors", command=lambda: right_col.tkraise())
        color_button.pack(pady=5)

        close_button = ttk.Button(edit_left_col, text="Close Tab", command=lambda: self.close_tab(tab_frame))
        close_button.pack(pady=5)

        # Right column ----
        filepath_label = ttk.Label(edit_right_col, text="filepath goes here")
        filepath_label.pack(padx=10, pady=10)

        edit_textbox = tk.Text(edit_right_col, width=100, height=30)
        edit_textbox.insert("1.0", "this is the edit screen.")
        edit_textbox.config(state="disabled")
        edit_textbox.pack(pady=0)
        edit_textbox.bind("<KeyRelease>", self.tabbed_interfaces[tab_name].limit_lines)

        # Four control buttons
        open_button = ttk.Button(edit_right_col, text="Open", command=lambda: self.tabbed_interfaces[tab_name].open_file_edit())
        open_button.pack(pady=5, padx=10, side="left")

        save_button = ttk.Button(edit_right_col, text="Save", command=lambda: self.tabbed_interfaces[tab_name].save_file_edit())
        save_button.pack(pady=5, padx=10, side="left")

        save_as_button = ttk.Button(edit_right_col, text="Save As", command=lambda: self.tabbed_interfaces[tab_name].save_as_file_edit())
        save_as_button.pack(pady=5, padx=10, side="left")

        discard_changes_button = ttk.Button(edit_right_col, text="Discard Changes", command=lambda: run_screen.tkraise())
        discard_changes_button.pack(pady=5, padx=10, side="left")

        # Resolve variables and save wigits into interface
        self.tabbed_interfaces[tab_name].edit_screen = edit_screen
        self.tabbed_interfaces[tab_name].edit_textbox = edit_textbox
        self.tabbed_interfaces[tab_name].filepath_label = filepath_label

        run_screen.tkraise()
        
    def close_tab(self, tab_frame):
        ''' Closes the tab containing the given tab_frame. '''
        self.notebook.forget(tab_frame)

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
    print("temporary color bypass on_button_hover")
    return
    button = event.widget
    current_bg = button.cget('bg')
    if current_bg == interface.primary_color.get():
        button.configure(bg=colors['primary_button_hover_color'])
    else:
        button.configure(bg=colors['secondary_button_hover_color'])

def on_button_leave(event):
    print("temporary color bypass on_button_leave")
    return
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

def show_frame(frame):
    ''' Raise the selected frame to switch screens '''
    frame.tkraise()

# Create the main application window
root = tk.Tk()
root.title("UVSim GUI")
root.geometry("1200x720")

tab_manager = TabManager(root)
tab_manager.add_tab()


root.mainloop()
