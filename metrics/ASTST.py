import ast
import sys
from pprint import pprint
from collections import defaultdict

# Abstract Syntax Tree w/ Symbol Table 
class ASTST(ast.NodeVisitor):
    def __init__(self):
        self.symbol_table = {}
        self.parent_stack = []

    def getSymbol(self, id):
        if id not in self.symbol_table:
            return "#None"
        return self.symbol_table[id]          

    def visit_ClassDef(self, node):
        """
        Add the class name to the symbol table and continue visiting its children.
        """
        self.assign_class_to_table(node)
        self.generic_visit(node)

    def visit_Assign(self, node):      
        """
        Handle assignments by extracting the target and value.
        """ 

        for target in node.targets:
            if isinstance(target.ctx, ast.Store):
                if isinstance(target, ast.Attribute):
                    self.assign_attr_to_table(target, node.value)
                elif isinstance(target, ast.Tuple):                    
                    for tuple_target in target.elts:
                        self.assign_attr_to_table(tuple_target, node.value)

        self.generic_visit(node)                        

    def assign_attr_to_table(self, attribute, value):
        """
        Assign an attribute to the symbol table with its type inferred from the attribute node.
        """        

        if isinstance(value, ast.List):
            self.symbol_table[attribute.attr] = "list"
        elif isinstance(value, ast.Dict):
            self.symbol_table[attribute.attr] = "dict"            
        elif isinstance(value, ast.Call):
            if isinstance(value.func, ast.Attribute):
                self.symbol_table[attribute.attr] = "#other" 
            if isinstance(value.func, ast.Name):         
                self.symbol_table[attribute.attr] = value.func.id    
        else:
            self.symbol_table[attribute.attr] = "#other"    

    def assign_class_to_table(self, node):
        """
        Add a class definition to the symbol table with a placeholder for its type.
        The class type is the symbol table key.
        """        
        self.symbol_table[node.name] = "#type"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ASTST.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    analyzer = ASTST()
    analyzer.visit(tree)
    pprint(analyzer.symbol_table)
