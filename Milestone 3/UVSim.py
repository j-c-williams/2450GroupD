class LogicalOperator:
    def __init__(self, interface, file_handler, words=None, accumulator=0, pointer=0):
        self.pointer = pointer
        self.accumulator = accumulator
        self.file_handler = file_handler
        self.words = words or [""] * 99
        self.interface = interface
        self.input = ""
        self.wait_for_input = True
    
    def load_file(self, file_path):
        #Uses the FileHandler to load a file.
        self.words = self.file_handler.read_txt_file(file_path)

    def write(self, location):
        if location < 0:
            raise IndexError(f"Negative memory location: {location} is not allowed.")
        elif location >= len(self.words):
            raise IndexError(f"Memory location {location} is out of bounds.")
        self.interface.add_output_text(self.words[location])
        return self.words[location] if self.words[location] is not None else ""

    def read(self, location, interface):
        if location < 0 or location >= len(self.words):
            raise IndexError(f"Invalid memory location: {location}")

        if self.wait_for_input:
            interface.add_output_text(f"What would you like to write to register {location}? ")
            # Ready to read again and get input
            self.wait_for_input = False
        else:
            # used stored input
            interface.add_output_text(f"Input: {self.input}")
            self.words[location] = self.input
            interface.add_output_text(f"Word {self.input} read into index {location}")
            self.input = ""
            self.wait_for_input = True

            # Conditionally go to the next command
            self.pointer += 1
            self.run_command()

    def handle_input(self, user_input):
        if len(user_input) == 0:
            return
        if not self.check_int(user_input):
            self.interface.add_output_text("Input is invalid, try again.")
            return
        if int(user_input) > -10_000 and int(user_input) < 10_000:
            self.input = user_input
            if not self.wait_for_input:
                self.run_command()
        else:
            self.interface.add_output_text("Input out of range, try again.")
            return

    def check_int(self, s):
        if s[0] in ('-', '+'):
            return s[1:].isdigit()
        return s.isdigit()


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
    
    def run_command(self):
        # use self instead of defining an instance
        
        # Run command now has to be called by the instructions to be run again at the next command.
        # By default, only one command is executed and resolved so that it can always be paused to get user input.

        if self.pointer >= len(self.words):
            print("End of program reached. Exiting.")

        word = self.words[self.pointer]
        if word.strip() == "":
            self.pointer += 1

        operation = word[:3]  # Grab only the first 3 characters (operation code)
        location = int(word[3:])   # Grab the last 2 characters for the location

        try:
            match operation:
                case "+10":
                    self.read(location, self.interface)
                    # Repeat executing the read line over and over until input is handled and ready to accept.
                        # self.pointer += 1
                        # self.run_command()
                case "+11":
                    self.write(location)
                    self.pointer += 1
                    self.run_command()
                case "+20":
                    self.load(location)
                    self.pointer += 1
                    self.run_command()
                case "+21":
                    self.store(location)
                    self.pointer += 1
                    self.run_command()
                case "+30":
                    self.add(location)
                    self.pointer += 1
                    self.run_command()
                case "+31":
                    self.subtract(location)
                    self.pointer += 1
                    self.run_command()
                case "+32":
                    self.divide(location)
                    self.pointer += 1
                    self.run_command()
                case "+33":
                    self.multiply(location)
                    self.pointer += 1
                    self.run_command()
                case "+40":
                    self.branch(location)
                    self.run_command()
                case "+41":
                    self.branch_neg(location)
                    self.run_command()
                case "+42":
                    self.branch_zero(location)
                    self.run_command()
                case "+43":
                    self.interface.add_output_text("Program is halted.\n")
                    print("The program has been halted.")
                case _:
                    print(f"Unrecognized operation code: {operation}, skipping this operation")
                    self.pointer += 1
        except Exception as e:
            print(f"Error encountered: {str(e)}")
            print("Continuing with the next instruction.")
            self.pointer += 1
        
    
    def reset_to_default(self):
        # Resets the pointer and accumulator and is called after a file is run.
        # This makes it able to run the same program immediately after it finishes running once.
        # Words is not reset because we want the current program to stay loaded.
        self.pointer = 0
        self.accumulator = 0
        # self.words = [""] * 99