15 Functional
1. The system shall use the LOAD function to store values in memory locations with bounds checking
2. The system shall use the READ function to write values into specified memory locations
3. The system shall use the WRITE function to write to the screen
4. The system shall use the ADD function to add a value from a memory location to the accumulator, supporting positive and negative numbers
5. The system shall use the SUBTRACT function to subtract from the accumulator and handle positive and negative numbers
6. The system shall use the MULTIPLY function to multiply the accumulator by a stored value
7. The system shall use the DIVIDE function to divide the accumulator and handle divide by zero 
8. The system shall use the BRANCH function to change the pointer to a given value
9. The system shall use the BRANCHNEG to check the accumulator and branch if it is negative
10. The system shall use the BRANCHZERO to check if the accumulator and branch if it is zero
11. The system shall accept a valid filepath from the user
12. The system shall read from the given file and load the instructions into the logic system
13. The system shall execute commands based off of a set of previously inputted instructions
14. The system shall halt the instructions when it encounters a HALT command.
15. The system shall handle unknown instruction codes without crashing the program
3 Non-functional
- The UI shall be one screen with five or less interactable UI elements
- The program shall launch in one second or less from first opening it
- The program will not crash when user input is invalid and should handle standard use cases