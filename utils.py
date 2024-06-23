import re

def read_md_file(file_path):
    """
    Reads the content of a Markdown file and returns it as a string.
    
    :param file_path: Path to the Markdown file
    :return: Content of the Markdown file as a string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        return str(e)

def write_to_file(file_path, content):
    """
    Writes the content to a file.
    
    :param file_path: Path to the file
    :param content: Content to write to the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        return str(e)

def generate_filename_from_h2(content):
    """
    Generates a file name based on the H2 title in the given content.
    
    :param content: String containing the H2 title
    :return: Generated file name based on the H2 title
    """
    # Regular expression to find the H2 title
    match = re.search(r'##\s+(.+)', content)
    if match:
        # Extract the title and convert it to lowercase
        title = match.group(1).strip().lower()
        # Replace spaces and special characters with underscores
        filename = re.sub(r'\W+', '_', title)
        # Append the file extension
        filename = f"test_{filename}.py"
        return filename
    else:
        raise ValueError("No H2 title found in the content")