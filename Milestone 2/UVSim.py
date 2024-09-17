def read(location):
    print(f"Reading from location: {location}")
    print(f"Value at location {location}: {words[location]}")
    return words[location]

def write():
    pass

def load():
    pass

def store(location):
    print(f"Storing {accumulator} into location {location}")
    words[location] = accumulator

def add():
    pass

def subtract():
    pass

def divide():
    pass

def mulitply():
    pass

def branch():
    pass

def branch_neg():
    pass

def branch_zero():
    pass

def halt():
    pass

def read_txt_file(file_path):
    global words
    with open(file_path, 'r') as f:
        for i, word in enumerate(f.read().split()):
            words[i] = word
    
    if len(words) == 0:
        raise ValueError("Text file must have at least one word")

accumulator = 0
words = [""] * 100
pointer = 0

def main():
    file_input = input('What is the file location? ')
    read_txt_file(file_input)

    while(True):
        global pointer
        word = words[pointer]
        operation = word[:3]  # Grab only the first 3 characters (operation code)
        location = word[3:]   # Grab the last 2 characters for the location
        location = int(location)
        
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
                load()
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
                branch()
            case "+41":
                print("branchneg")
                branch_neg()
            case "+42":
                print("branchzero")
                branch_zero()
            case "+43":
                print("The program has been halted.")
                break
            case _:
                raise ValueError(f"Unrecognized operation code: {operation}")
 
        pointer += 1

if __name__ == "__main__":
    main()

