This document is designed for the purpose of defining requirements for UVSim.py


1.a) The system shall accept a .txt file containing up to a maximum of 100 signed 4 digit words(b) i.e. +1234 representing the address to be used and command to be executed
b) Words shall use the first 2 digits to determine the Command to be performed and the last 2 digits to determine the address to be used when executing the command

2) The system shall contain an Accumulator register which holds the result of the last operation performed on it

3) The system shall contain 100 registers to hold signed 4 digit words read in from the user command file

4) The system shall allow the user to upload a file using a button on the GUI 

5) The system shall contain a run button to allow user to run the program

6) The system shall contain a Text Field to allow user input on the GUI when the corresponding command is executed

7) The system shall contain a LogicalOperater class which shall be used to execute commands using logic Methods within the class

8) The system shall execute the mathematical operation Addition when the corresponding command is executed
9) The system shall execute the mathematical operation Subtraction when the corresponding command is executed
10) The system shall execute the mathematical operation Division when the corresponding command is executed
The system shall execute the mathematical operation mulyiply when the corresponding command is executed


11) The system shall handle overflow in situations where the accumulator's value exeeds +9999 or exeeds -9999 in the negative direction









12) The system shall execute branch operations: Branch, Branch neg, Branch zero when a corresponding command is executed

13) The system shall Halt when the corresponding command is executed

14) The system shall Load the value at the specified location in the accumulator register when the corresponding command is executed

15) The system shall store the value stored in the accumulator register at the specified location in the UVsim words registers when the corresponding command is executed

16) The system shall handle incompatible user commands without crashing

Non-Functional Requirements: 
1) The system shall inform the user when an unknown command is encountered and automatically skip to the next command

2) The system shall use button press animations for the open and run file buttons when the user clicks the button

3) The system shall contain an escape button to close the GUI more easily











The system shall
