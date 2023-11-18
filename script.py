#!/C:/Python311/python.exe

import sys
import maude

maude.init()

maude_module = sys.argv[1]
maude_command = sys.argv[2]

print("Module: " + maude_module)
print(" Command: " + maude_command)

m = maude.getModule(maude_module)

t = m.parseTerm(maude_command)
t.reduce()

print("<html><body>")
print("<h4>Result:</h4>")
print(str(t))
print("</body></html>")