def read(location):
    print(f"Reading from location: {location}")
    print(f"Value at location {location}: {words[location]}")
    return words[location]

def write(location):
    print(words[location])

def load(location):
    global accumulator 
    accumulator = words[location]

def store(location):
    print(f"Storing {accumulator} into location {location}")
    words[location] = accumulator

def add(location):
    
    acclimator = (int(acclimator) + int(words[location])) % 10000

def subtract(location):
    acclimator = (int(acclimator) - int(words[location])) % 10000

def multiply(location):
    acclimator = (int(acclimator) * int(words[location])) % 10000

def divide(location):
    try:
        acclimator = int(acclimator / int(words[location]))
    except (ZeroDivisionError, ValueError):
        print("Acclimator unable to be divided by zero, command failed to execute.")
        return

def branch(location):
    global pointer
    pointer = location
    print(f"Branching to location {location}")

def branch_neg(location):
    global accumulator
    if accumulator < 0:
        branch(location)
        print(f"Branchneg - acc is negative")
    else:
        print(f"Branchneg - acc is not negative")

def branch_zero(location):
    global accumulator
    if accumulator == 0:
        branch(location)
        print(f"Branchzero - acc is zero")
    else:
        print(f"Branchzero - acc is not zero")


def halt():
    pass

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
        word = words[pointer]
        operation = word[:3]  # Grab only the first 3 characters (operation code)
        location = int(word[3:])   # Grab the last 2 characters for the location
        
        print(f"Current instruction: {word}, Operation: {operation}, Location: {location}")
        
        match operation:
            case "+10":
                print("read")
                read(location)
            case "+11":
                print("write")
                write()
            case "+20":
                print("load")
                load(location)
            case "+21":
                print("store")
                store(location)
            case "+30":
                print("add")
                add()
            case "+31":
                print("subtract")
                subtract()
            case "+32":
                print("divide")
                divide()
            case "+33":
                print("multiply")
                mulitply()
            case "+40":
                print("branch")
                branch(location)
            case "+41":
                print("branchneg")
                branch_neg(location)
            case "+42":
                print("branchzero")
                branch_zero(location)
            case "+43":
                print("The program has been halted.")
                break
            case _:
                raise ValueError(f"Unrecognized operation code: {operation}")

        pointer += 1

if __name__ == "__main__":
    main()

