def write(location, words):
    if location < 0:
        raise IndexError(f"Negative memory location: {location} is not allowed.")
    elif location >= len(words):
        raise IndexError(f"Memory location {location} is out of bounds.")
    print(words[location])
    return words[location] if words[location] is not None else ""

def read(location):
    if location < 0 or location >= len(words):
        raise IndexError(f"Invalid memory location: {location}")
    user_input = input(f"What would you like to write to register {location}? ")
    words[location] = user_input


def load(location):
    if location < 0 or location > 99:
        raise IndexError("Load attempted to load value out of bounds")
    global accumulator 
    data = words[location]
    if data == "":
        accumulator = 0
    else:
        accumulator = int(data)

def store(location):
    if location < 0:
        raise IndexError(f"Negative memory location: {location} is not allowed.")
    elif location >= len(words):
        raise IndexError(f"Memory location {location} is out of bounds.")
    words[location] = accumulator

def add(location):
    global accumulator
    if (int(accumulator) + int(words[location])) > 0:
        accumulator = (int(accumulator) + int(words[location])) % 10000
    else: accumulator = -(abs(int(accumulator) + int(words[location]))%10000)
    
def subtract(location):
    global accumulator
    if (int(accumulator) - int(words[location])) > 0:
        accumulator = (int(accumulator) - int(words[location])) % 10000
    else: accumulator = -(abs(int(accumulator) - int(words[location]))%10000)

def multiply(location):
    global accumulator
    if (int(accumulator) * int(words[location])) > 0:
        accumulator = (int(accumulator) * int(words[location])) % 10000
    else: accumulator = -(abs(int(accumulator) * int(words[location]))%10000)

def divide(location):
    global accumulator
    divisor = float(words[location]) 
    if divisor == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    accumulator = float(accumulator) / divisor 

def branch(location):
    if location < 0 or location > 99:
        raise IndexError("Branch attempted to set pointer out of bounds")
    global pointer
    pointer = location

def branch_neg(location):
    if location < 0 or location > 99:
        raise IndexError("Branch_neg attempted to set pointer out of bounds")
    global accumulator
    accumulator = int(accumulator)
    if accumulator < 0:
        branch(location)
    else:
        global pointer
        pointer += 1

def branch_zero(location):
    if location < 0 or location > 99:
        raise IndexError("Branchzero attempted to set pointer out of bounds")
    global accumulator
    accumulator = int(accumulator)
    if accumulator == 0:
        branch(location)
    else:
        global pointer
        pointer += 1

def read_txt_file(file_path):
    global words
    with open(file_path, 'r') as f:
        for i, word in enumerate(f.read().split()):
            words[i] = word
    
accumulator = 0
words = [""] * 100
pointer = 0

def main():
    file_input = input('What is the file location? ')
    read_txt_file(file_input)

    while True:
        global pointer
        if pointer >= len(words):
            print("End of program reached. Exiting.")
            break

        word = words[pointer]
        if word.strip() == "":
            pointer += 1
            continue

        operation = word[:3]  # Grab only the first 3 characters (operation code)
        location = int(word[3:])   # Grab the last 2 characters for the location

        try:
            match operation:
                case "+10":
                    read(location)
                    pointer += 1
                case "+11":
                    write(location, words)
                    pointer += 1
                case "+20":
                    load(location)
                    pointer += 1
                case "+21":
                    store(location)
                    pointer += 1
                case "+30":
                    add(location)
                    pointer += 1
                case "+31":
                    subtract(location)
                    pointer += 1
                case "+32":
                    divide(location)
                    pointer += 1
                case "+33":
                    multiply(location)
                    pointer += 1
                case "+40":
                    branch(location)
                case "+41":
                    branch_neg(location)
                case "+42":
                    branch_zero(location)
                case "+43":
                    print("The program has been halted.")
                    break
                case _:
                    print(f"Unrecognized operation code: {operation}, skipping this operation")
                    pointer += 1
        except Exception as e:
            print(f"Error encountered: {str(e)}")
            print("Continuing with the next instruction.")
            pointer += 1

if __name__ == "__main__":
    main()