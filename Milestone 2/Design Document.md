# Milestone 2 Design Document

# High-level Overview

The UVSim software is a simulator for computer science students to use to execute machine language programs. UVSim can only interperet the BasicML language, which is composed of signed 4 digit integers. These integers will trigger different commands to move, manipulate, store and view data.

# User Stories

User Story 1: Running a Program with Input and Output

As a computer science student, I want to write a BasicML program that reads multiple values from the keyboard then outputs the results of various calculations to the screen.

List of steps the student will complete:

1. The student writes a BasicML program that includes READ (opcode 10) and WRITE (opcode 11) instructions.
2. The student loads the program into the UVSim and starts execution.
3. The UVSim prompts the student for input when encountering a READ instruction and stores the input value at the specified memory location.
4. When encountering a WRITE instruction, the UVSim outputs the value stored at the specified memory location to the screen.
5. The program continues executing, displaying results until a HALT instruction is executed.

User Story 2: Arithmetic Operations in the Accumulator

As a computer science student, I want to execute a BasicML program that performs arithmetic operations on data stored in memory.

List of steps the student will complete:

1.The student writes a BasicML program that loads values into the accumulator and performs operations such as ADD (opcode 30), SUBTRACT (opcode 31), MULTIPLY (opcode 33), and DIVIDE (opcode 32). 2. The student loads the program into the UVSim and starts execution. 3. The UVSim loads values from specified memory locations into the accumulator using the LOAD instruction. 4. The UVSim performs operations on the value in the accumulator and a value from another memory location, storing the result back in the accumulator. 5. The program continues executing until a HALT instruction is encountered, and the final result is displayed to the student.

# Use Cases (10-15)

**READ command use case:**

- Actor: The program and the user
- System: Memory management and input processor
- Goal: Successfully read user input and store it at a given memory location

Steps:

1. Parse function code ("+10" for READ)
2. Extract location from the last two digits of the word
3. Validate the memory location
   If location is negative or out of bounds, raise an IndexError
4. Prompt the user for input
5. Read the user's input
6. Store the input at the specified memory location
7. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message

Notes:

- The READ command interacts with the user, unlike most other commands which operate solely on the program's internal state

**WRITE command use case:**

- Actor: The program and the user
- System: Memory management and output processor
- Goal: Successfully output the value stored at a given memory location

Steps:

1. Parse function code ("+11" for WRITE)
2. Extract location from the last two digits of the word
3. Validate the memory location:
   If location is negative, raise an IndexError with message "Negative memory location: {location} is not allowed."
   If location is out of bounds (>= len(words)), raise an IndexError with message "Memory location {location} is out of bounds."
4. Retrieve the value from the specified memory location
5. Output the retrieved value to the console
6. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message

**STORE command use case:**

- Actor: The program
- System: Memory management and accumulator
- Goal: Successfully store the value of the accumulator at a given memory location

Steps:

1. Parse function code ("+21" for STORE)
2. Extract location from the last two digits of the word
3. Validate the memory location
   If location is negative, raise an IndexError with message "Negative memory location: {location} is not allowed."
   If location is out of bounds (>= len(words)), raise an IndexError with message "Memory location {location} is out of bounds."
4. Retrieve the current value of the accumulator
5. Store the accumulator value at the specified memory location
6. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message

**ADD command use case:**

- Actor: The program
- System: Memory management and accumulator
- Goal: Successfully add a value stored at a given memory location to the value of the accumulator

Steps:

1. Parse function code ("+30" for ADD)
2. Extract location from the last two digits of the word
3. Validate the memory location:
   If location is negative, raise an IndexError with message "Negative memory location: {location} is not allowed."
   If location is out of bounds (>= len(words)), raise an IndexError with message "Memory location {location} is out of bounds."
4. Retrieve the value from the specified memory location
5. Add the retrieved value to the accumulator
6. Handle overflow by taking the result modulo 10000 or making it negative as appropriate
7. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message

**SUBTRACT command use case:**

- Actor: The program
- System: Memory management and accumulator
- Goal: Successfully subtract a value stored at a given memory location from the value of the accumulator

Steps:

1. Parse function code ("+31" for SUBTRACT)
2. Extract location from the last two digits of the word
3. Validate the memory location:
   If location is negative, raise an IndexError with message "Negative memory location: {location} is not allowed."
   If location is out of bounds (>= len(words)), raise an IndexError with message "Memory location {location} is out of bounds."
4. Retrieve the value from the specified memory location
5. Subtract the retrieved value from the accumulator
6. Handle underflow by taking the result modulo 10000 or making it negative as appropriate
7. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message
  **MULTIPLY command use case:**

- Actor: The program
- System: Memory management and accumulator
- Goal: Successfully multiply the value of the accumulator by a value stored at a given memory location

Steps:

1. Parse function code ("+33" for MULTIPLY)
2. Extract location from the last two digits of the word
3. Validate the memory location:
   If location is negative, raise an IndexError with message "Negative memory location: {location} is not allowed."
   If location is out of bounds (>= len(words)), raise an IndexError with message "Memory location {location} is out of bounds."
4. Retrieve the value from the specified memory location
5. Multiply the accumulator by the retrieved value
6. Handle overflow by taking the result modulo 10000 or making it negative as appropriate
7. Move to the next instruction (increment the pointer)

Exceptions:

- If an invalid memory location is provided, the system raises an IndexError with an appropriate error message

**DIVIDE command use case:**

- Actor: The program
- System: Arithmetic processor and accumulator
- Goal: Successfully divide the accumulator by the value stored at a given memory location

Steps:

1. Parse function code ("+32" for DIVIDE)
2. Extract location from the last two digits of the word
3. Retrieve the value stored at the specified memory location
4. Convert the retrieved value to a float (divisor)
5. Check if the divisor is zero
   If divisor is zero, raise a ZeroDivisionError with message "Cannot divide by zero."
6. Perform the division: accumulator = float(accumulator) / divisor
7. Update the accumulator with the result of the division
8. Move to the next instruction (increment the pointer)

Exceptions:

- If division by zero is attempted, the system raises a ZeroDivisionError with an appropriate error message

**LOAD command use case:**

- Actor: the program
- System: Memory management and code processor
- Goal: Successfully change the accumulator to the data at a given location
  Steps

1. Parse function code
2. Extract location from the last two digits of the word
3. Locate the word at the location assigned
4. Set that word equal to the accumulator
5. Pass to the next word

**BRANCH command use case:**

- Actor: the program
- System: Memory management and code processor
- Goal: Successfully change the pointer to an assigned value
  Steps

1. Parse function code
2. Extract location from the last two digits of the word
3. Check the location if it is a valid memory address
4. Set the pointer to that location

**BRANCHNEG command use case:**

- Actor: the program
- System: Memory management and code processor
- Goal: Successfully change the pointer to an assigned value when the accumulator is negative
  Steps

1. Parse function code
2. Extract location from the last two digits of the word
3. Look at the accumulator and detect if it is negative
4. If it is negative, set the pointer equal to the assigned value
5. If it is not negative, simply pass to the next word

**BRANCHZERO command use case:**

- Actor: the program
- System: Memory management and code processor
- Goal: Successfully change the pointer to an assigned value when the accumulator is zero
  Steps

1. Parse function code
2. Extract location from the last two digits of the word
3. Look at the accumulator and detect if it is negative
4. If it is zero, set the pointer equal to the assigned value
5. If it is not zero, simply pass to the next word
6. Write 8 unit tests that test those use cases and other useful tests

**HALT command use case:**

- Actor: The program
- System: Execution control
- Goal: Successfully terminate the program execution

Steps:

1. Parse function code ("+43" for HALT)
2. Print a message indicating that the program has been halted
3. Terminate the program execution

Exceptions:

- None specific to this command

**read_txt_file function use case:**

- Actor: The program
- System: File I/O and memory management
- Goal: Successfully load a program from a text file into memory

Steps:

1. Prompt the user for the file location
2. Open the specified file
3. Read the contents of the file
4. Split the file contents into individual words
5. Store each word in the corresponding memory location
6. Close the file

Exceptions:

- If the file cannot be opened or read, handle the appropriate file I/O exceptions

**main function use case:**

- Actor: The program and the user
- System: Program execution control
- Goal: Successfully execute a BasicML program

Steps:

1. Call the read_txt_file function to load the program
2. Initialize the program counter (pointer) to 0
3. Enter the main execution loop
4. For each instruction:
   a. Parse the operation code
   b. Execute the corresponding function
   c. Handle any exceptions that occur
   d. Increment the program counter (unless modified by a branch instruction)
5. Continue execution until a HALT instruction is encountered or the end of the program is reached

Exceptions:

- Handle any exceptions raised by individual instructions
- Print error messages for unrecognized operation codes
