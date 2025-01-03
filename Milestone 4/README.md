# UVSim: A Machine Language Simulator with GUI

## Overview

**UVSim** is a virtual machine simulator that executes instructions in BasicML, a hypothetical machine language. The simulator includes components for the CPU, memory, and an accumulator, processing BasicML programs step-by-step through a modern, customizable graphical user interface (GUI).

### Features

- **Memory Size**: 100-word memory.
- **Accumulator**: Used for arithmetic and data manipulation.
- **Operations**: Supports BasicML operations like reading, writing, loading, storing, arithmetic, and control operations.
- **Instruction Set**: Each instruction is a signed four-digit decimal number.
- **File Handling**: Supports loading and editing BasicML programs.
- **User Interface**: A modern graphical interface with customizable colors and multiple screens.
- **Color Customization**: Personalize the interface with custom primary and secondary colors.

## Getting Started

### Prerequisites

- **Python 3.12** or higher must be installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
- **Tkinter**: This should be included with most Python installations.

### Files

- **UVSim_GUI.py**: The main program file containing the GUI implementation.
- **UVSim.py**: Contains the `LogicalOperator` class for executing BasicML instructions.
- **UVSim_FileHandler.py**: Handles file operations for loading BasicML programs.

### How to Run

1. Ensure all project files are in the same directory.
2. Open a command line terminal and navigate to the folder containing the project files.
3. Run the program by executing the following command:

```bash
python UVSim_GUI.py
```

4. The GUI window will open with the main screen interface.

## Using the GUI

### Main Screen

1. **Opening a File**:

   - Click the "Open File" button to browse and select a BasicML program file.
   - The selected file path will be displayed, and the program will be loaded into memory.

2. **Running the Program**:

   - After loading a file, click the "Run File" button to execute the program.
   - The output will be displayed in the main window.

3. **Inputting Data**:
   - When the program requires input, the input field at the bottom will become active.
   - Type your response and press Enter or click "Submit" to provide input.

### File Editor

1. **Accessing the Editor**:

   - Click the "Edit File" button on the main screen to open the editor interface.

2. **Editor Features**:
   - Open existing files for editing
   - Edit BasicML instructions directly in the text area
   - Save changes to the current file or save as a new file
   - Limited to 100 lines (memory size limit)
   - Validates that each line contains a valid signed four-digit number

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
   - Check that BasicML files contain only valid signed four-digit numbers
   - Verify file permissions allow reading and writing

2. **GUI Issues**:

   - If colors aren't saving, check write permissions in the application directory
   - If the interface becomes unresponsive, check the console for error messages
   - Restart the application if color settings become corrupted

3. **Program Execution**:
   - Verify your BasicML program follows the correct format
   - Check that all memory references are within the 100-word limit
   - Ensure all instructions use valid operation codes

If problems persist:

- Verify your Python version (3.12 or higher required)
- Check that Tkinter is properly installed
- Try resetting to default colors
- Clear any saved color configurations by deleting the `.color_config.pkl` file
