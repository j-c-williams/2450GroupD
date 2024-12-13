# UVSim: A Machine Language Simulator with GUI

## Overview

**UVSim** is a virtual machine simulator that executes instructions in BasicML, a hypothetical machine language. The simulator includes components for the CPU, memory, and an accumulator, processing BasicML programs step-by-step through a modern, customizable graphical user interface (GUI).

### Features

- **Memory Size**: 250-word memory.
- **Accumulator**: Used for arithmetic and data manipulation.
- **Operations**: Supports BasicML operations like reading, writing, loading, storing, arithmetic, and control operations.
- **Instruction Set**: Each instruction is a signed four or six-digit decimal number.
- **File Handling**: Supports loading and editing BasicML programs, including converting betwween 4-digit (legacy) and 6-digit formats.
- **User Interface**:
  - Multi-tab interface supporting muliple program instances
  - Modern graphical interface with customizable colors
  - Tab-specific file editing and execution
- **Color Customization**:
  - Personalize primary and secondary colors
  - Color settings persist between sessions
  - Quick reset to default UVU colors
  - Real-time color preview

## Getting Started

### Prerequisites

- **Python 3.12** or higher must be installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Tkinter**: This should be included with most Python installations.

### Files

- **TABS_UVSim.py** The main program file containing the GUI implementation and tab management.
- **UVSim.py**: Contains the `LogicalOperator` class for executing BasicML instructions.
- **UVSim_FileFormatConverter** contains the `FileFormatConverter` class for converting 4-digit instructions into 6-digit instructions.
- **UVSim_FileHandler.py**: Handles file operations for loading BasicML programs.

### How to Run

1. Ensure all project files are in the same directory.
2. Open a command line terminal and navigate to the folder containing the project files.
3. Run the program by executing the following command:

```bash
python TABS_UVSim.py
```

4. The GUI window will open with the main screen interface.

## Using the GUI

### Main Screen

1. **Opening a File**:

   - Click the "Open File" button to browse and select a BasicML program file.
   - The program supports both 4-digt (legacy) and 6-digit instruction formats. Legacy files are automatically
     converted to 6-digit format during loading, ensuring compatibility. Detailed logs notify users about the
     conversion process
   - The selected file path will be displayed, and the program will be loaded into memory.

2. **Running the Program**:

   - After loading a file, click the "Run File" button to execute the program.
   - The output will be displayed in the main window.

3. **Inputting Data**:

   - When the program requires input, the input field at the bottom will become active.
   - Type your response and press Enter or click "Submit" to provide input.

### Creating Tabs

1. **Creating Tabs**:

   - Click "Add Tab" to open a new program instance.
   - Each tab operates independently with its own memory and execution state. There is no fixed limit on the number of tabs,
     but system resources may affect performance when managing a large number of instances.

2. **Switching Tabs**:

   - When a new tab is created, you will need to manually select it by clicking its label.

3. **Exiting Exit Mode**:

   - To leave the file editor for a tab, save your changes and manually return to the main view.

4. **Closing Tabs**:

   - Use the "Close Tab" button within each tab.
   - Unsaved changes will be lost on tab closure.

### File Editor

1. **Accessing the Editor**:

   - Click the "Edit File" button on the main screen to open the editor interface.

2. **Editor Features**:

   - Open existing files for editing
   - Edit BasicML instructions directly in the text area
   - Save changes to the current file or save as a new file
   - Validate that each line contains a valid signed 4-digit or 6-digit number. Errors in validation
     are displayed as pop-up messages, guiding users to correct their input.

### Color Customization

1. **Accessing Color Settings**:

   - Click the "Edit Colors" button on the main screen to open the color configuration interface.

2. **Customization Options**:

   - Change primary color (affects main background and primary buttons)
   - Change secondary color (affects sidebar and secondary buttons)
   - Preview color changes in real-time
   - Reset to default UVU colors (green and white)

3. **Color Persistence**:

   - Custom colors are saved and persist between sessions

## BasicML Instructions

BasicML operations that UVSim can interpret include:

- **READ (10)**: Read a word from the keyboard into a memory location.
- **WRITE (11)**: Write a word from memory to the screen.
- **LOAD (20)**: Load a word from memory into the accumulator.
- **STORE (21)**: Store the word from the accumulator into memory.
- **ADD (30)**: Add a word from memory to the accumulator.
- **SUBTRACT (31)**: Subtract a word from memory from the accumulator.
- **DIVIDE (32)**: Divide the accumulator by a word from memory.
- **MULTIPLY (33)**: Multiply the accumulator by a word from memory.
- **BRANCH (40)**: Branch to a specific location in memory.
- **BRANCHNEG (41)**: Branch to a location if the accumulator is negative.
- **BRANCHZERO (42)**: Branch to a location if the accumulator is zero.
- **HALT (43)**: Stop the program.

## Error Handling

The program includes robust error handling for:

- Invalid memory locations and operations
- Invalid file formats and content
- Input validation in the file editor
- Memory size limitations
- Runtime errors during program execution

## Troubleshooting

If you encounter issues:

1. **File Operations**:

   - Ensure all required files are in the same directory
   - Check that BasicML files contain only valid signed 4-digit or 6-digit numbers
   - Verify file permissions allow reading and writing

2. **GUI Issues**:

   - If colors aren't saving, check write permissions in the application directory. For example, on Windows, ensure
     the application folder is not set to 'Read-Only' inits properties
   - If the interface becomes unresponsive, check the console for error messages
   - Restart the application if color settings become corrupted
   - Clear any saved color configurations by deleting the `.color_config.pkl` file

3. **Program Execution**:
   - Verify your BasicML program follows the correct format
   - Check that all memory references are within the 250-word limit
   - Ensure all instructions use valid operation codes

If problems persist:

- Verify your Python version (3.12 or higher required)
- Check that Tkinter is properly installed
- Try resetting to default colors
