# Milestone 2 Design Document

High level description on how the program works

2 User stories

10-15 Use cases

# Use Cases (10-15)

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
