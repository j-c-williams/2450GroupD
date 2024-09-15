def read():
    pass

def write():
    pass

def load():
    pass

def store():
    pass

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

def read_txt_file():
  global words
  with open(file, 'r') as f:
    for word in f.read().split():
      words.append(word)
  
  if len(words) == 0:
    raise ValueError("text file must have at least one word")

file = "Test1.txt"
accumulator = 0
words = []
pointer = 0


def main():
  read_txt_file()

  while(True):
    global pointer
    word = words[pointer]
    word = word[:3] # grab only first 3 characters
    
    match word:
      case "+10":
        print("read")
        read()
      case "+11":
        print("write")
        write()
      case "+20":
        print("load")
        load()
      case "+21":
        print("store")
        store()
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
        print("halt")
        break

    pointer += 1



if __name__ == "__main__":
    main()