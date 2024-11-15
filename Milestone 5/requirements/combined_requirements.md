Functional Requirements

1. The system shall allow users to create and manage multiple program instances through tabs, with each tab supporting upload and editing of files containing up to 100 signed 4-digit words.
2. The system shall provide a GUI with buttons for loading files, running programs, entering manual input, creating tabs, closing tabs, and customizing interface colors.
3. The system shall execute loaded instruction files sequentially within each tab instance, processing each command based on its opcode while maintaining separate program states.
4. The system shall maintain separate accumulators and 100 memory registers for each tab instance to store results and input words independently.
5. The system shall perform basic arithmetic operations (addition, subtraction, multiplication, and division) on the accumulator, handling overflow and division by zero within each tab context.
6. The system shall validate memory addresses and handle invalid memory locations safely without crashing or affecting other tab instances.
7. The system shall execute branching commands (branch, branch if negative, branch if zero) to modify the instruction pointer based on program conditions within each tab.
8. The system shall halt execution when encountering a halt (HALT) command in the instruction file while maintaining other tabs' states.
9. The system shall display file contents and execution results in a dedicated output window for each tab instance.
10. The system shall load values from specified memory locations into the accumulator using the LOAD command within the current tab's memory space.
11. The system shall store the value in the accumulator into a specified memory location using the STORE command within the current tab's memory space.
12. The system shall display error messages for invalid memory locations, unknown commands, or zero-division errors within the appropriate tab context.
13. The system shall allow user input from the keyboard whenever a program requests it during execution, with input/output managed separately per tab.
14. The system shall skip unknown or unsupported instruction codes without crashing and continue execution while maintaining tab isolation.
15. The system shall reset the accumulator and instruction pointer when a new file is loaded for execution within each tab instance.

Non-Functional Requirements

1. The system shall execute BasicML instructions and respond to user input within 1 second across all active tab instances.
2. The system shall have a clear, intuitive interface with consistent layout across tabs and no more than five primary interactive elements per screen.
3. The system shall not crash when encountering invalid input or unknown instructions and shall handle such cases gracefully while maintaining color preferences between sessions.
