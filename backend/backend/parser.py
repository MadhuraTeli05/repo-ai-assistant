import ast                                                                 #Uses Python’s built-in AST module

def extract_python_chunks(code):
    """
    Extract functions and classes from Python code using AST where --> Input: code = complete Python file (string)
                                                                   --> Output: list of functions & classes
    """

    chunks = []                                                             #create empty list to store extracted code chunks (functions and classes)

    try:
        tree = ast.parse(code)                                              #converts code → tree 

        for node in ast.walk(tree):                                         #goes through all nodes..traverse the tree

            # Extract functions
            if isinstance(node, ast.FunctionDef):                           #FunctionDef--> detects functions in the code. If it finds a function, it extracts the code segment for that function and stores it in the chunks list with its name and type. 
                chunk = ast.get_source_segment(code, node)                  #Gets original code from file-->using get_source_segment() method
                chunks.append({
                    "type": "function",
                    "name": node.name,
                    "code": chunk
                })

            # Extract classes
            elif isinstance(node, ast.ClassDef):                           #ClassDef--> detects classes in the code. If it finds a class, it extracts the code segment for that class and stores it in the chunks list with its name and type.
                chunk = ast.get_source_segment(code, node)
                chunks.append({
                    "type": "class",
                    "name": node.name,
                    "code": chunk
                })

    except Exception as e:
        print("Parsing error:", e)

    return chunks