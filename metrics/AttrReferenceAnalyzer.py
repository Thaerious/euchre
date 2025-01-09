import ast
import sys
from pprint import pprint
from ASTST import ASTST
from collections import defaultdict

class ContextRecord():
    def __init__(self):
        self.read = False
        self.write = False

    def applyContext(self, node):
        """
        Determine context from node (top level ctx field).
        """
        context = type(node.ctx).__name__

        if (context == "Load"):
            self.read = True
        elif (context == "Store"):
            self.write = True

    def setContext(self, context):
        if (context.lower() == "read"):
            self.read = True
        elif (context.lower() == "write"):
            self.write = True


    def __str__(self):
        if self.read and self.write: return "RW"
        elif self.read: return "R"
        elif self.write: return "W"
        else: return "X"

    def __repr__(self):        
        return str(self)

class AttrRecord(dict):
    def add_reference(self, attribute:ast.Attribute):
        """
        Track operations on primitives.
        """
        if attribute.attr not in self:
            self[attribute.attr] = ContextRecord()

        context = type(attribute.ctx).__name__

        if (context == "Load"):
            self[attribute.attr].read = True
        elif (context == "Store"):
            self[attribute.attr].write = True

    def add_list_operation(self, node: ast.Call):
        """
        Track list-specific operations like append, extend, or slicing.
        """
        attr = node.func.attr

        if attr in {"append", "extend", "insert"}:  # Writing operations
            self.add_reference(node.func)
            self[node.func.attr].write = True
        elif attr in {"copy", "count", "index"}:  # Reading operations
            self.add_reference(node.func)
            self[node.func.attr].read = True

    def __str__(self):
        sb = ""
        for key in self:
            value = self[key]
            sb = sb + f" - {key} {str(value)}\n"

        return sb

class MethodRecord(dict):
    def add_reference(self, method:ast.FunctionDef, child:ast.Attribute):
        if method not in self: self[method] = AttrRecord()
        self[method].add_reference(child)

    def add_list_operation(self, method:ast.FunctionDef, child:ast.Call):
        if method not in self: self[method] = AttrRecord()
        self[method].add_list_operation(child)

    def __str__(self):
        sb = ""

        for key in self.keys():
            sb = sb + f"# {key}()\n"
            sb = sb + f"{(str)(self[key])}\n"

        return sb

class AttrReferenceAnalyzer(ASTST):
    def __init__(self):
        ASTST.__init__(self)
        self.classes = {}   
        self.current_class = None;    
        self.current_method = None

    def visit_ClassDef(self, node):
        self.current_class = {};    
        self.classes[node.name] = self.current_class
        self.current_method = None        
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.current_method = defaultdict(ContextRecord)
        self.current_class[node.name] = self.current_method        
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if not is_attr(node): return        
        attr_id = node.attr
        attr_type = self.getSymbol(attr_id)
        self.current_method[attr_id].applyContext(node)

    def visit_Call(self, node):
        if not is_call(node): 
            self.generic_visit(node)
            return
        
        attr_id = node.func.value.attr
        attr_type = self.getSymbol(attr_id)

        if attr_type == "list":
            self.record_attr_list_ref(node)
        elif attr_type == "dict":
            self.record_attr_dict_ref(node)

    def record_attr_list_ref(self, node):
        attr_id = node.func.value.attr
        method_invoked = node.func.attr

        if method_invoked in {"append", "extend", "insert", "remove", "pop", "clear", "sort", "reverse", "__setitem__", "__delitem__"}:
            self.current_method[attr_id].setContext("write")
        elif method_invoked in {"copy", "count", "index", "__len__", "__getitem__", "__contains__"}:
            self.current_method[attr_id].setContext("read")

    def record_attr_dict_ref(self, node):
        attr_id = node.func.value.attr
        method_invoked = node.func.attr

        if method_invoked in {"clear", "pop", "popitem", "setdefault", "update", "__setitem__", "__delitem__"}:
            self.current_method[attr_id].setContext("write")
        elif method_invoked in {"copy", "get", "items", "keys", "values", "__getitem__", "__contains__", "__len__"}:
            self.current_method[attr_id].setContext("read")

    def get_methods_for_attr(self, class_name, attr_name):
        method_records = {}

        if not class_name in self.classes:
            raise Exception(f"Class not found: {class_name}")          
        
        class_record = self.classes[class_name]
        for method_name, method_record in class_record.items():
            if attr_name in method_record:
                method_records[method_name] = method_record

        return method_records

    def get_method(self, class_name, method_name):
        if not class_name in self.classes:
            raise Exception(f"Class not found: {class_name}")  

        class_record = self.classes[class_name]
        if not method_name in class_record:
            raise Exception(f"Method not found: {class_name}.{method_name}")

        method_record = class_record[method_name]
        return method_record

    def method_context(self, class_name, method_name):
        method_context_record = ContextRecord()
        method_record = self.get_method(class_name, method_name)

        for attr_context_record in method_record.values():
            if attr_context_record.read:
                method_context_record.read = True
            if attr_context_record.write:
                method_context_record.write = True

        return method_context_record

def is_attr(node):
    if not isinstance(node, ast.Attribute): return False
    if not isinstance(node.value, ast.Name): return False
    if not node.value.id in {'self', 'this'}: return False
    return True

def is_call(node):
    if not isinstance(node, ast.Call): return False    
    if not isinstance(node.func, ast.Attribute): return False
    if not isinstance(node.func.value, ast.Attribute): return False
    if not isinstance(node.func.value.value, ast.Name): return False
    if not node.func.value.value.id in {'self', 'this'}: return False  
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python AttrReferenceAnalyzer.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    analyzer = AttrReferenceAnalyzer()
    analyzer.visit(tree)

    print("* Symbol Table")
    pprint(analyzer.symbol_table)
    print("* References")

    for class_name, class_record in analyzer.classes.items():
        print(f"{class_name}")
        for method_name, method_record in class_record.items():
            print(f"- {method_name}")
            for attr_name, context in method_record.items():
                print(f"-- {attr_name} : {context}")
