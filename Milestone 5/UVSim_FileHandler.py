from UVSim_FileFormatConverter import FileFormatConverter
import re

class FileHandler:
    def __init__(self):
        self.converter = FileFormatConverter()
       
    def read_txt_file(self, file_path):
        """Read and process a file, converting if necessary"""
        try:
            with open(file_path, 'r') as file:
                content = file.read()
               
            # Validate line count
            if not self.converter.validate_line_count(content):
                raise ValueError("File cannot contain more than 250 lines")
               
            # Convert if needed
            converted_content, was_converted = self.converter.convert_legacy_to_new(content)
           
            if converted_content is None:
                raise ValueError("Invalid file format. File must contain only valid 4-digit or 6-digit words.")
               
            # Split into lines and filter empty lines
            words = [line.strip() for line in converted_content.split('\n') if line.strip()]
           
            # Pad array to max size with empty strings
            words.extend([''] * (250 - len(words)))
            
            # Return conversion status along with words
            return words, was_converted
           
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")