from AttrReferenceAnalyzer import AttrReferenceAnalyzer
import ast
import sys
from pprint import pprint

def printAll(analyzer, list):
    for class_name, class_record in analyzer.classes.items():
        print(f"class {class_name}()")
        for method_name, method_record in class_record.items():
            method_context = analyzer.method_context(class_name, method_name)
            print(f"    def {method_name}(): {method_context}")
            if not list:
                for attr_name, context in method_record.items():
                    print(f"        {attr_name} : {context}")
                print("")
        print("")

def printMethod(analyzer, full_name):
    class_name, method_name = full_name.split(".")

    method_record = analyzer.get_method(class_name, method_name)
    method_context = analyzer.method_context(class_name, method_name)
    print(f"    def {method_name}(): {method_context}")
    for attr_name, context in method_record.items():
        print(f"        {attr_name} : {context}")
    print("")

def printAttribute(analyzer, full_name):
    class_name, method_name = full_name.split(".")
    methods = analyzer.get_methods_for_attr(class_name, method_name)

    for method_name, method_record in methods.items():
        method_context = analyzer.method_context(class_name, method_name)
        print(f"    def {method_name}(): {method_context}")
        for attr_name, context in method_record.items():
            print(f"        {attr_name} : {context}")
        print("")        

def do_cmd_line(full_name, abbr_letter):
    index = -1
    if f"--{full_name}" in sys.argv:
        index = sys.argv.index(f"--{full_name}")
    elif f"-{abbr_letter}" in sys.argv:
        index = sys.argv.index(f"-{abbr_letter}")

    return index

if __name__ == "__main__":
    list = False
    method = None

    if len(sys.argv) < 2:
        print("Usage: python AttrReferenceAnalyzer.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    analyzer = AttrReferenceAnalyzer()
    analyzer.visit(tree)

    list_index = do_cmd_line("list", "l")
    method_index = do_cmd_line("method", "m")
    attr_index = do_cmd_line("attr", "a")


    if list_index >= 0:
        printAll(analyzer, True)
    elif method_index >= 0:
        if method_index + 1 < len(sys.argv):
            method_full_name = sys.argv[method_index + 1]
            printMethod(analyzer, method_full_name)
        else:
            print("Error: --method or -m requires an additional argument.")
    elif attr_index >= 0:
        if attr_index + 1 < len(sys.argv):
            attr_full_name = sys.argv[attr_index + 1]
            printAttribute(analyzer, attr_full_name)
        else:
            print("Error: --attr or -a requires an additional argument.")            
    else:
        printAll(analyzer, False)
