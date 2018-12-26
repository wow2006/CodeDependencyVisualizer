simple_file_name = "simple.cpp"
simple_file_string = """
struct Simple {
    int x;
    int y;
    int z;
};
"""
simple_result_string = """
- Simple
  - int x
  - int y
  - int z
"""
import sys
from io import StringIO
from context import CreateAST, printClass 


# 1. Create file contain "simple_file_string" called "simple.cpp"
with open(simple_file_name, "w") as f:
    f.write(simple_file_string)

# 2. Parse "simple.cpp"
tu = CreateAST({simple_file_name: []})

# 3. print
# - Simple
#   - int x
#   - int y
#   - int z
old_stdout = sys.stdout
sys.stdout = temp_stdout = StringIO()
printClass(tu, "Simple")
sys.stdout = old_stdout

if(temp_stdout.read() == simple_file_string):
    print("Finish!")

# 4. clean file
os.remove(simple_file_name)

