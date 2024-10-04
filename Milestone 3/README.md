# UVSim: A Machine Language Simulator with GUI

## Overview

**UVSim** is a virtual machine simulator that executes instructions in BasicML, a hypothetical machine language. The simulator includes components for the CPU, memory, and an accumulator, processing BasicML programs step-by-step through a graphical user interface (GUI).

### Features

- **Memory Size**: 100-word memory.
- **Accumulator**: Used for arithmetic and data manipulation.
- **Operations**: Supports BasicML operations like reading, writing, loading, storing, arithmetic, and control operations.
- **Instruction Set**: Each instruction is a signed four-digit decimal number.
- **File Handling**: Supports loading BasicML programs from text files.
- **User Interface**: A graphical interface for improved interaction and user experience.

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
`python UVSim_GUI.py`
```

4. The GUI window will open, presenting options to open a file and run the program.

## Using the GUI

1. **Opening a File**:

- Click the "Open File" button to browse and select a BasicML program file.
- The selected file path will be displayed, and the program will be loaded into memory.

2. **Running the Program**:

- After loading a file, click the "Run File" button to execute the program.
- The output will be displayed in the main window.

3. **Inputting Data**:

- When the program requires input, type your response in the entry field at the bottom of the window.
- Press Enter to submit your input.

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

The program handles invalid memory locations, operations, and invalid input by displaying error messages in the GUI output area while continuing to the next instruction when possible.

## Troubleshooting

If you encounter issues:

- Ensure all required files (`UVSim_GUI.py`, `UVSim.py`, `UVSim_FileHandler.py`) are in the same directory.
- Check that your BasicML program files are correctly formatted, with one instruction per line.
- Verify that you have the necessary Python version and Tkinter installed.
- If the GUI doesn't respond, check the console for any error messages.
