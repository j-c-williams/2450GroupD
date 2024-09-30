class LogicalOperator():
    def __init__(self, words = [""] * 99, accumulator = 0, pointer = 0):
        self.pointer = pointer
        self.accumulator = accumulator
        self.words = words

    def write(self, location):
        if location < 0:
            raise IndexError(f"Negative memory location: {location} is not allowed.")
        elif location >= len(self.words):
            raise IndexError(f"Memory location {location} is out of bounds.")
        print(self.words[location])
        return self.words[location] if self.words[location] is not None else ""

    def read(self, location):
        if location < 0 or location >= len(self.words):
            raise IndexError(f"Invalid memory location: {location}")
        user_input = input(f"What would you like to write to register {location}? ")
        self.words[location] = user_input


    def load(self, location):
        if location < 0 or location > 99:
            raise IndexError("Load attempted to load value out of bounds")
         
        data = self.words[location]
        if data == "":
            self.accumulator = 0
        else:
            self.accumulator = int(data)

    def store(self, location):
        if location < 0:
            raise IndexError(f"Negative memory location: {location} is not allowed.")
        elif location >= len(self.words):
            raise IndexError(f"Memory location {location} is out of bounds.")
        self.words[location] = self.accumulator

    def add(self, location):
        
        if (int(self.accumulator) + int(self.words[location])) > 0:
            self.accumulator = (int(self.accumulator) + int(self.words[location])) % 10000
        else: self.accumulator = -(abs(int(self.accumulator) + int(self.words[location]))%10000)
        
    def subtract(self, location):
        
        if (int(self.accumulator) - int(self.words[location])) > 0:
            self.accumulator = (int(self.accumulator) - int(self.words[location])) % 10000
        else: self.accumulator = -(abs(int(self.accumulator) - int(self.words[location]))%10000)

    def multiply(self, location):
        
        if (int(self.accumulator) * int(self.words[location])) > 0:
            self.accumulator = (int(self.accumulator) * int(self.words[location])) % 10000
        else: self.accumulator = -(abs(int(self.accumulator) * int(self.words[location]))%10000)

    def divide(self, location):
        
        divisor = float(self.words[location]) 
        if divisor == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        self.accumulator = float(self.accumulator) / divisor 

    def branch(self, location):
        if location < 0 or location > 99:
            raise IndexError("Branch attempted to set pointer out of bounds")
        
        self.pointer = location

    def branch_neg(self, location):
        if location < 0 or location > 99:
            raise IndexError("Branch_neg attempted to set pointer out of bounds")
        
        self.accumulator = int(self.accumulator)
        if self.accumulator < 0:
            self.branch(location)
        else:
            self.pointer += 1

    def branch_zero(self, location):
        if location < 0 or location > 99:
            raise IndexError("Branchzero attempted to set pointer out of bounds")
        self.accumulator = int(self.accumulator)
        if self.accumulator == 0:
            self.branch(location)
        else:
            self.pointer += 1

def read_txt_file(file_path):
    global words
    with open(file_path, 'r') as f:
        for i, word in enumerate(f.read().split()):
            words[i] = word
    


def main():
    file_input = input('What is the file location? ')
    read_txt_file(file_input)
    UVsimLogic = LogicalOperator()
    while True:
        
        if UVsimLogic.pointer >= len(UVsimLogic.words):
            print("End of program reached. Exiting.")
            break

        word = UVsimLogic.words[UVsimLogic.pointer]
        if word.strip() == "":
            UVsimLogic.pointer += 1
            continue

        operation = word[:3]  # Grab only the first 3 characters (operation code)
        location = int(word[3:])   # Grab the last 2 characters for the location

        try:
            match operation:
                case "+10":
                    UVsimLogic.read(location)
                    pointer += 1
                case "+11":
                    UVsimLogic.write(location)
                    pointer += 1
                case "+20":
                    UVsimLogic.load(location)
                    pointer += 1
                case "+21":
                    UVsimLogic.store(location)
                    pointer += 1
                case "+30":
                    UVsimLogic.add(location)
                    pointer += 1
                case "+31":
                    UVsimLogic.subtract(location)
                    pointer += 1
                case "+32":
                    UVsimLogic.divide(location)
                    pointer += 1
                case "+33":
                    UVsimLogic.multiply(location)
                    pointer += 1
                case "+40":
                    UVsimLogic.branch(location)
                case "+41":
                    UVsimLogic.branch_neg(location)
                case "+42":
                    UVsimLogic.branch_zero(location)
                case "+43":
                    print("The program has been halted.")
                    break
                case _:
                    print(f"Unrecognized operation code: {operation}, skipping this operation")
                    UVsimLogic.pointer += 1
        except Exception as e:
            print(f"Error encountered: {str(e)}")
            print("Continuing with the next instruction.")
            UVsimLogic.pointer += 1

if __name__ == "__main__":
    main()