import re

class FileFormatConverter:
    def __init__(self):
        self.LEGACY_WORD_PATTERN = r'^[+-]\d{4}$'
        self.NEW_WORD_PATTERN = r'^[+-]\d{6}$'
        
    def detect_format(self, content):
        """
        Detects if file is in legacy (4-digit) or new (6-digit) format
        Returns: 'legacy', 'new', or 'invalid'
        """
        if not content:
            return 'invalid'
            
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if not lines:
            return 'invalid'
            
        # Check first line to determine format
        first_line = lines[0]
        
        if re.match(self.LEGACY_WORD_PATTERN, first_line):
            # Verify all lines match legacy format
            return 'legacy' if all(re.match(self.LEGACY_WORD_PATTERN, line) for line in lines) else 'invalid'
            
        elif re.match(self.NEW_WORD_PATTERN, first_line):
            # Verify all lines match new format
            return 'new' if all(re.match(self.NEW_WORD_PATTERN, line) for line in lines) else 'invalid'
            
        return 'invalid'

    def convert_legacy_to_new(self, content):
        """
        Converts 4-digit format to 6-digit format
        Returns: (converted_content, was_converted)
        """
        if not content:
            return None, False
            
        format_type = self.detect_format(content)
        
        if format_type == 'new':
            return content, False  # Already in new format
        elif format_type == 'invalid':
            return None, False  # Invalid format
            
        converted_lines = []
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        for line in lines:
            # Split into sign, operation, and address
            sign = line[0]
            operation = line[1:3]
            address = line[3:]
            
            # Add leading 0 to operation and pad address
            new_operation = '0' + operation
            new_address = address.zfill(3)
            
            # Combine into new format
            new_line = f"{sign}{new_operation}{new_address}"
            converted_lines.append(new_line)
            
        return '\n'.join(converted_lines), True

    def validate_line_count(self, content):
        """Ensures file doesn't exceed 250 lines"""
        if not content:
            return False
            
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return len(lines) <= 250