import ast, os

def find_stub_files(directory="."):
    stubs = []
    for root, _, files in os.walk(directory):
        if "env" in root or "venv" in root or "node_modules" in root or ".git" in root or "site-packages" in root:
            continue
        for file in files:
            if file.endswith(".py") and file != "find_stubs.py":
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        source = f.read()
                    
                    if "raise NotImplementedError" in source or "pass" in source or "..." in source or "TODO" in source:
                        # deeper check
                        tree = ast.parse(source)
                        
                        is_stub = False
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                # check if body is just pass, ..., or raise NotImplementedError
                                if len(node.body) == 1:
                                    stmt = node.body[0]
                                    if isinstance(stmt, ast.Pass):
                                        is_stub = True
                                    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
                                        is_stub = True
                                    elif isinstance(stmt, ast.Raise):
                                        if isinstance(stmt.exc, ast.Name) and stmt.exc.id == "NotImplementedError":
                                            is_stub = True
                                        elif isinstance(stmt.exc, ast.Call) and isinstance(stmt.exc.func, ast.Name) and stmt.exc.func.id == "NotImplementedError":
                                            is_stub = True
                                            
                        if is_stub or "TODO" in source:
                            stubs.append(path)
                except Exception as e:
                    pass
    return stubs

if __name__ == "__main__":
    stubs = find_stub_files()
    for s in stubs:
        print(s)
