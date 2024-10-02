import nbformat

file_path = "K:\RAG Application\Rag\Simplerag1 copy.ipynb"

try:
    # Try to read the notebook file
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    print(f"Notebook '{file_path}' is valid.")
except nbformat.reader.NotJSONError:
    print(f"Notebook '{file_path}' does not appear to be valid JSON.")
except Exception as e:
    print(f"An error occurred: {e}")
