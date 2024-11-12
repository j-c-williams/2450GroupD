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

class TabManager:
    def __init__(self, base, color_manager):
        self.base = base
        self.color_manager = color_manager

        style=ttk.Style()
        style.layout("TNotebook", [])
        style.configure("TNotebook", highlightbackground="#848a98",tabmargins=0)
        # Create the tabbed notebook
        self.notebook = ttk.Notebook(self.base, style="TNotebook")
        self.notebook.pack(expand=1, fill="both", pady = 10)

        self.tab_count = 0

        add_tab_button = tk.Button(self.base, text="Add Tab", command=self.add_tab)
        add_tab_button.pack(pady=5, side="left", padx=(500, 20))

        self.color_manager.button_secondary_hover_wigits.append(add_tab_button)

        pick_color_button = tk.Button(self.base, text="Change Colors", command=lambda: color_manager.open_color_selection_window())
        pick_color_button.pack(pady=5, side="left")

        self.color_manager.button_secondary_hover_wigits.append(pick_color_button)

        self.tabbed_interfaces = {} # Dictionary to store interfaces by tab index

    def add_tab(self):
        ''' Adds a new tab with a close button inside the tab content. '''
        self.tab_count += 1
        button_width = 15

        # Create tab
        tab_frame = tk.Frame(self.notebook, highlightthickness=0, borderwidth=0)
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
        left_col = tk.Frame(run_screen, padx=5, pady=200)
        left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        right_container = tk.Frame(run_screen, padx=30, pady=10)
        right_container.grid(row=0, column=1, sticky="w", padx=30, pady=10)

        # Left Column ----
        label = tk.Label(left_col, text=f"This is {tab_name}")
        label.pack(padx=10, pady=10)

        open_button = tk.Button(left_col, text="Open", command=self.tabbed_interfaces[tab_name].open_file, width=button_width)
        open_button.pack(pady=5)

        run_button = tk.Button(left_col, text="Run File", command=self.tabbed_interfaces[tab_name].run_file, width=button_width)
        run_button.pack(pady=5)

        edit_button = tk.Button(left_col, text="Edit File", command=lambda: self.tabbed_interfaces[tab_name].edit_file_transition(), width=button_width)
        edit_button.pack(pady=5)

        close_button = tk.Button(left_col, text="Close Tab", command=lambda: self.close_tab(tab_frame), width=button_width)
        close_button.pack(pady=5)

        # Right Column ----
        right_col = tk.Frame(right_container, height=35)
        right_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        # Title
        edit_label = tk.Label(right_col, text="Run File", font=("Arial", 18))
        edit_label.pack(pady=50)

        # Large text field
        file_edit = tk.Text(right_col, width=100)
        file_edit.insert("1.0", "Open a file to run it.\n")
        file_edit.config(state="disabled")
        file_edit.pack(pady=10)

        # User input field
        txt_edit = tk.Entry(right_col, width=100)
        txt_edit.insert(0, "Run a file with user input to enable text editing.")
        txt_edit.bind('<Return>', self.tabbed_interfaces[tab_name].save_input)
        txt_edit.config(state="disabled")
        txt_edit.pack(padx=20, side="left")

        # Submit Button
        btn_submit = tk.Button(right_col, text="Submit", command=lambda: self.tabbed_interfaces[tab_name].save_input(), width=button_width)
        #style_button(btn_submit, False)
        btn_submit.config(state="disabled")
        btn_submit.pack(pady=10, side="left")

        # Resolve variables and save wigits into interface
        self.tabbed_interfaces[tab_name].run_screen = run_screen
        self.tabbed_interfaces[tab_name].text_edit = file_edit
        self.tabbed_interfaces[tab_name].user_entry = txt_edit
        self.tabbed_interfaces[tab_name].submit_button = btn_submit

        self.color_manager.primary_bg_wigits.append(run_screen)
        self.color_manager.primary_bg_wigits.append(right_container)
        self.color_manager.primary_bg_wigits.append(right_col)
        self.color_manager.primary_bg_wigits.append(edit_label)
        self.color_manager.primary_bg_wigits.append(label)
        self.color_manager.primary_bg_wigits.append(left_col)

        self.color_manager.secondary_bg_wigits.append(open_button)
        self.color_manager.secondary_bg_wigits.append(run_button)
        self.color_manager.secondary_bg_wigits.append(edit_button)
        self.color_manager.secondary_bg_wigits.append(close_button)
        self.color_manager.secondary_bg_wigits.append(file_edit)
        self.color_manager.secondary_bg_wigits.append(txt_edit)



        self.color_manager.text_on_primary_wigits.append(label)
        self.color_manager.text_on_primary_wigits.append(edit_label)

        self.color_manager.text_on_secondary_wigits.append(open_button)
        self.color_manager.text_on_secondary_wigits.append(run_button)
        self.color_manager.text_on_secondary_wigits.append(edit_button)
        self.color_manager.text_on_secondary_wigits.append(close_button)
        self.color_manager.text_on_secondary_wigits.append(file_edit)

        self.color_manager.button_secondary_hover_wigits.append(open_button)
        self.color_manager.button_secondary_hover_wigits.append(run_button)
        self.color_manager.button_secondary_hover_wigits.append(edit_button)
        self.color_manager.button_secondary_hover_wigits.append(close_button)
        self.color_manager.button_secondary_hover_wigits.append(btn_submit)






        # Edit Screen ----------------
        edit_screen = tk.Frame(container)
        edit_screen.grid(row=0, column=0, sticky="nsew")

        edit_left_col = tk.Frame(edit_screen, height=35)
        edit_left_col.grid(row=0, column=0, sticky="w", padx=30, pady=10)

        edit_right_col = tk.Frame(edit_screen, height=35)
        edit_right_col.grid(row=0, column=1, sticky="w", padx=30, pady=10)
        
        # Left column ----
        edit_tab_label = tk.Label(edit_left_col, text=f"This is {tab_name}")
        edit_tab_label.pack(padx=10, pady=10)

        close_button = tk.Button(edit_left_col, text="Close Tab", command=lambda: self.close_tab(tab_frame), width=button_width)
        close_button.pack(pady=5)

        # Right column ----
        filepath_label = tk.Label(edit_right_col, text="filepath goes here")
        filepath_label.pack(padx=10, pady=10)

        edit_textbox = tk.Text(edit_right_col, width=100, height=30)
        edit_textbox.insert("1.0", "this is the edit screen.")
        edit_textbox.config(state="disabled")
        edit_textbox.pack(pady=0)
        edit_textbox.bind("<KeyRelease>", self.tabbed_interfaces[tab_name].limit_lines)

        # Four control buttons
        open_edit_button = tk.Button(edit_right_col, text="Open", command=lambda: self.tabbed_interfaces[tab_name].open_file_edit(), width=button_width)
        open_edit_button.pack(pady=5, padx=10, side="left")

        save_button = tk.Button(edit_right_col, text="Save", command=lambda: self.tabbed_interfaces[tab_name].save_file_edit(), width=button_width)
        save_button.pack(pady=5, padx=10, side="left")

        save_as_button = tk.Button(edit_right_col, text="Save As", command=lambda: self.tabbed_interfaces[tab_name].save_as_file_edit(), width=button_width)
        save_as_button.pack(pady=5, padx=10, side="left")

        discard_changes_button = tk.Button(edit_right_col, text="Discard Changes", command=lambda: run_screen.tkraise(), width=button_width)
        discard_changes_button.pack(pady=5, padx=10, side="left")

        # Resolve variables and save wigits into interface
        self.tabbed_interfaces[tab_name].edit_screen = edit_screen
        self.tabbed_interfaces[tab_name].edit_textbox = edit_textbox
        self.tabbed_interfaces[tab_name].filepath_label = filepath_label

        self.color_manager.primary_bg_wigits.append(edit_screen)
        self.color_manager.primary_bg_wigits.append(edit_left_col)
        self.color_manager.primary_bg_wigits.append(edit_tab_label)

        self.color_manager.button_secondary_hover_wigits.append(open_edit_button)
        self.color_manager.button_secondary_hover_wigits.append(save_button)
        self.color_manager.button_secondary_hover_wigits.append(save_as_button)
        self.color_manager.button_secondary_hover_wigits.append(discard_changes_button)
        self.color_manager.button_secondary_hover_wigits.append(close_button)

        self.color_manager.text_on_primary_wigits.append(edit_tab_label)



        color_manager.update_colors()

        run_screen.tkraise()
        
    def close_tab(self, tab_frame):
        ''' Closes the tab containing the given tab_frame. '''
        self.notebook.forget(tab_frame)

class ColorManager():
    def __init__(self):
        self.primary_bg_wigits = []
        self.secondary_bg_wigits = []
        self.text_on_primary_wigits = []
        self.text_on_secondary_wigits = []
        self.button_primary_hover_wigits = []
        self.button_secondary_hover_wigits = []

        self.colors = {
            "primary_color": "#4C721D",
            "secondary_color": "#FFFFFF",
            "text_color_on_primary": "#FFFFFF",
            "text_color_on_secondary": "#330000",
            "primary_button_hover_color": "#5d8b24",
            "secondary_button_hover_color": "#F0F0F0" 
        }

        self.load_color_scheme()

    def update_colors(self):
        ''' Update all widgets with set colors '''
    
        for wigit in self.primary_bg_wigits:
            try:
                wigit.config(bg=self.colors["primary_color"])
            except Exception as e:
                print("error changing bg color of wigit ", e)
        
        for wigit in self.secondary_bg_wigits:
            try:
                wigit.config(bg=self.colors["secondary_color"])
            except Exception as e:
                print("error changing bg color of wigit ", e)
        
        for wigit in self.text_on_primary_wigits:
            try:
                wigit.config(fg=self.colors["text_color_on_primary"])
            except Exception as e:
                print("error changing bg color of wigit ", e)
        
        for wigit in self.text_on_secondary_wigits:
            try:
                wigit.config(fg=self.colors["text_color_on_secondary"])
            except Exception as e:
                print("error changing bg color of wigit ", e)

        for wigit in self.button_primary_hover_wigits:
            try:
                wigit.config(bg=self.colors["primary_color"], fg=self.colors["text_color_on_primary"], activebackground=self.colors["primary_button_hover_color"], activeforeground=self.colors["text_color_on_secondary"])
            except Exception as e:
                print("error changing bg color of wigit ", e)

        for wigit in self.button_secondary_hover_wigits:
            try:
                wigit.config(bg=self.colors["secondary_color"], fg=self.colors["text_color_on_secondary"], activebackground=self.colors["secondary_button_hover_color"], activeforeground=self.colors["text_color_on_primary"])
            except Exception as e:
                print("error changing bg color of wigit ", e)
            
    def pick_primary_color(self):
        """Open color picker for primary color"""
        color = askcolor(color=self.colors["primary_color"], title="Choose Primary Color")
        if color[1]:  # If a color was chosen (not cancelled)
            #colors['primary_color'] = color[1]
            self.colors["primary_color"] = color[1]
            
            # Calculate text colors based on brightness
            rgb = tuple(int(color[1][i:i+2], 16) for i in (1, 3, 5))
            brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
            
            # Set text colors
            new_text_color = "#FFFFFF" if brightness < 128 else "#000000"
            self.colors["text_color_on_primary"] = new_text_color
            
            # Text on secondary uses primary color
            self.colors["text_color_on_secondary"] = color[1]
            
            # Calculate hover color - lighten the primary color
            hover_rgb = tuple(min(255, int(c * 1.1)) for c in rgb)  # Lighten by 10%
            self.colors["primary_button_hover_color"] = '#{:02x}{:02x}{:02x}'.format(*hover_rgb)
            
            self.save_color_scheme()
            self.update_colors()

    def pick_secondary_color(self):
        """Open color picker for secondary color"""
        color = askcolor(color=self.colors["secondary_color"], title="Choose Secondary Color")
        if color[1]:  # If a color was chosen (not cancelled)
            self.colors["secondary_color"] = color[1]
            
            # Calculate hover color - for white/light colors, slightly darken
            rgb = tuple(int(color[1][i:i+2], 16) for i in (1, 3, 5))
            hover_rgb = tuple(int(c * 0.9) for c in rgb)  # Darken by 10%
            self.colors["secondary_button_hover_color"] = '#{:02x}{:02x}{:02x}'.format(*hover_rgb)
            
            self.save_color_scheme()
            self.update_colors()

    def reset_colors(self):
        """Reset colors to UVU default"""
        self.colors = {
            'primary_color': "#4C721D",
            'secondary_color': "#FFFFFF",
            'text_color_on_primary': "#FFFFFF",
            'text_color_on_secondary': "#4C721D",
            'primary_button_hover_color': "#5d8b24",  
            'secondary_button_hover_color': "#F0F0F0" 
        }
                
        self.save_color_scheme()
        self.update_colors()

    def load_color_scheme(self):
        """Load saved color scheme or return defaults"""
        try:
            with open('.color_config.pkl', 'rb') as f:
                self.colors = pickle.load(f)
        except FileNotFoundError:
            return {
                'primary_color': "#4C721D",  # UVU Green
                'secondary_color': "#FFFFFF",  # White
                'text_color_on_primary': "#FFFFFF",
                'text_color_on_secondary': "#4C721D",
                'primary_button_hover_color': "#5d8b24",
                'secondary_button_hover_color': "#F5F5F5"
            }

    def save_color_scheme(self):
        """Save color scheme to file"""
        with open('.color_config.pkl', 'wb') as f:
            pickle.dump(self.colors, f)

    def on_button_hover(self, event):
        print("temporary color bypass on_button_hover")
        return
        button = event.widget
        current_bg = button.cget('bg')
        if current_bg == interface.primary_color.get():
            button.configure(bg=colors['primary_button_hover_color'])
        else:
            button.configure(bg=colors['secondary_button_hover_color'])

    def on_button_leave(self, event):
        print("temporary color bypass on_button_leave")
        return
        button = event.widget
        # Check if this is a primary or secondary button based on its foreground color
        is_primary = button.cget('fg') == interface.text_color_on_primary.get()
        button.configure(bg=interface.primary_color.get() if is_primary else interface.secondary_color.get())

    def style_button(self, button, is_primary=True):
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

    def open_color_selection_window(self):
        """Open a new screen for color selection."""
        color_window = tk.Toplevel()
        color_window.title("Select Colors")

        tk.Label(color_window, text="Select a color for Primary and Secondary:").pack(pady=10)

        tk.Button(color_window, text="Choose Primary Color", command=self.pick_primary_color).pack(pady=5)

        tk.Button(color_window, text="Choose Secondary Color", command=self.pick_secondary_color).pack(pady=5)

        tk.Button(color_window, text="Reset to UVU Colors", command=self.reset_colors).pack(pady=5)

        tk.Button(color_window, text="Close", command=color_window.destroy).pack(pady=10)

# Create the main application window
root = tk.Tk()
root.title("UVSim GUI")
root.geometry("1200x720")

main_container = tk.Frame(root, highlightthickness=0, borderwidth=0)
main_container.pack()

color_manager = ColorManager()
color_manager.primary_bg_wigits.append(root)
color_manager.primary_bg_wigits.append(main_container)

tab_manager = TabManager(main_container, color_manager)

tab_manager.add_tab()

root.mainloop()
