
# UVSim: A Machine Language Simulator

## Overview

**UVSim** is a virtual machine simulator. This program simulates a simple virtual machine that executes instructions in BasicML, a hypothetical machine language. The UVSim has CPU, memory, and accumulator components, and processes machine language programs step-by-step as students input commands or instructions.

### Features
- Memory size: 100-word memory.
- Accumulator: Used for arithmetic and data manipulation.
- Operations: Supports BasicML operations like reading, writing, loading, storing, arithmetic, and control operations.
- Instruction Set: Each instruction is a signed four-digit decimal number.

## Getting Started

### Prerequisites
- **Python 3.12** or higher must be installed on your system. You can download it at (https://www.python.org/downloads/).
  
### Files
- **UVSim.py**: This is the main program file where the virtual machine logic is implemented.
- **Test Files**: These files contain sample BasicML instructions that can be loaded and executed in the simulator (e.g., `Test2.txt`).

### How to Run

1. Clone or download the project repository to your local machine.
2. Ensure you have a BasicML program file (such as `Test1.txt`) with valid instructions.
3. Open a command line terminal and navigate to the folder where `UVSim.py` is located.
4. Run the program by executing the following command:

   `python UVSim.py`
   

5. The simulator will prompt you to input the file location. Enter the path to your BasicML file (e.g., `C:\Users\User\Desktop\Test2.txt`).
6. Follow the prompts to input values or interact with the machine.

### BasicML Instructions

Here is a list of BasicML operations that UVSim can interpret:

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

### Error Handling

The program handles invalid memory locations, operations, and invalid input by either skipping unrecognized instructions or outputting error messages while continuing to the next instruction.

### Troubleshooting

If you encounter errors, check the following:
- Ensure you are inputting valid BasicML commands.
- Make sure your input file is formatted correctly, with one instruction per line.
