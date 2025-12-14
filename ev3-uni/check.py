import ast
import sys

# List of EV3Dev2 libraries
EV3_LIBS = [
    "ev3dev2.motor",
    "ev3dev2.sensor",
    "ev3dev2.sound",
    "ev3dev2.button",
    "ev3dev2.led",
    "ev3dev2.display",
    "ev3dev2.sensor.lego"
]

# Optional: common libraries not available on EV3
UNSUPPORTED_LIBS = [
    "tkinter",
    "matplotlib",
    "numpy",  # unless installed manually
    "opencv",  # unless installed manually
]

def check_code(filename):
    with open(filename, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        return False

    success = True
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name in UNSUPPORTED_LIBS:
                    print(f"Warning: Library '{n.name}' may not be available on EV3.")
                    success = False
        elif isinstance(node, ast.ImportFrom):
            full_name = f"{node.module}"
            if full_name in UNSUPPORTED_LIBS:
                print(f"Warning: Library '{full_name}' may not be available on EV3.")
                success = False

    print("Analysis complete.")
    if success:
        print("Your code looks compatible with EV3 (basic check).")
    else:
        print("Your code may have compatibility issues with EV3.")
    return success

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_ev3_compat.py <your_script.py>")
        sys.exit(1)

    check_code(sys.argv[1])
