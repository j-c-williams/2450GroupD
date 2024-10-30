class FileHandler:
    def __init__(self):
        self.words = [""] * 99

    def read_txt_file(self, file_path):
        #Reads a text file and stores words into the memory array.
        try:
            with open(file_path, 'r') as f:
                for i, word in enumerate(f.read().split()):
                    self.words[i] = word
            return self.words
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {str(e)}")
        