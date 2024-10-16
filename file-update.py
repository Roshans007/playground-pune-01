import re
import uuid

# Function to replace pattern with UUID
def replace_with_uuid(match):
    return f"'{uuid.uuid4()}'" if match.group(0).startswith("'") else f'"{uuid.uuid4()}"'

# Read the file and update the content
def update_file_with_uuid(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Regular expression to match patterns like '492181XXXXXXXXX1241-492181XXXXXXXXX1241'
    pattern = r"['\"][0-9]{6}X{9}[0-9]{4}-[0-9]{6}X{9}[0-9]{4}['\"]"
    
    # Replace the pattern with UUID
    updated_content = re.sub(pattern, replace_with_uuid, content)

    # Write the updated content back to the file
    with open(filename, 'w') as file:
        file.write(updated_content)

# Specify your file path here
file_path = 'your_file.txt'
update_file_with_uuid(file_path)