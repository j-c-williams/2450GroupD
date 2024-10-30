Functional Requirements:

1. The system shall allow users to upload and read instruction files containing up to 100 signed 4-digit words, using the first 2 digits for the command and the last 2 for the memory address.
2. The system shall provide a GUI with buttons for loading files, running programs, and entering manual input when required by the program.
3. The system shall execute the loaded instruction files sequentially, processing each command based on its opcode (e.g., arithmetic, branching, halting).
4. The system shall contain an accumulator register to store results of operations and 100 memory registers to hold the input words.
5. The system shall perform basic arithmetic operations (addition, subtraction, multiplication, and division) on the accumulator, handling overflow and division by zero.
6. The system shall validate memory addresses and handle invalid memory locations safely without crashing.
7. The system shall execute branching commands (branch, branch if negative, branch if zero) to modify the instruction pointer based on program conditions.
8. The system shall halt execution when encountering a halt (HALT) command in the instruction file.
9. The system shall display file contents and execution results in an output window.
10. The system shall load values from specified memory locations into the accumulator using the LOAD command.
11. The system shall store the value in the accumulator into a specified memory location using the STORE command.
12. The system shall display error messages for invalid memory locations, unknown commands, or zero-division errors.
13. The system shall allow user input from the keyboard whenever the program requests it during execution.
14. The system shall skip unknown or unsupported instruction codes without crashing and continue execution.
15. The system shall reset the accumulator and instruction pointer when a new file is loaded for execution.

Non-Functional Requirements:

1. The system shall execute BasicML instructions and respond to user input within 1 second.
2. The system shall have a clear, intuitive interface with no more than five interactive elements on the main screen.
3. The system shall not crash when encountering invalid input or unknown instructions and shall handle such cases gracefully.
