#!/C:/Python311/python.exe

import sys
import maude

def getCommand(c):
    c2 = c.split()
    command = c2[0]
    term = ' '.join(c2[1:])[:-1]
    return command, term


maude.init()

maude_module = sys.argv[1].replace("^", "")
maude_command = sys.argv[2].replace("^", "")

print("Module: " + maude_module)

#m = maude.getModule(maude_module)
#m = maude.downModule()
maude.input(maude_module)
m = maude.getCurrentModule()

command, term = getCommand(maude_command)

print("Command: " + command)
print("Term: " + term)

t = m.parseTerm(term)


if command == "red" or command == "reduce":
    t.reduce()
elif command == "rew":
    t.rewrite()
else:
    t = "No se ha reconocido el comando introducido"

print("<html><body>")
print("<h4>Result:</h4>")
print(str(t))
print("</body></html>")
