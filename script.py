#!/C:/Python311/python.exe

import sys
import maude
import regex
import re


def getCommand(c):
    c2 = c.split()
    command = c2[0]
    term = ' '.join(c2[1:])[:-1]
    #term = c2[1:-1]
    return command, term

maude.init()

maude_module = sys.argv[1].replace("^", "")
maude_command = sys.argv[2].replace("^", "")

print("Module: " + maude_module)

#m = maude.getModule(maude_module)
#m = maude.downModule()
#maude_module = 'fmod FOO is pr NAT . op f : Nat Nat -> Nat . eq f(M:Nat, N:Nat) = M:Nat + N:Nat . endfm'
maude.input(maude_module)

m = maude.getCurrentModule()
#m = maude.getModule('DIE-HARD')


command, term = getCommand(maude_command)

print("Command: " + command)
print("Term: ", term)

#t = m.parseTerm(term)


if command == "red" or command == "reduce":
    #t = m.parseTerm(' '.join(term))
    t = m.parseTerm(term)
    t.reduce()
elif command == "rewrite" or command == "rew":
    #t = m.parseTerm(' '.join(term))
    t = m.parseTerm(term)
    t.rewrite()

elif command == "search":
    
    i = 0
    bound = None
    depth = None
    mod = None
    subject = None
    searchtype = None
    pattern = None
    condition = None
    '''
    for x in term:
        if '[' in x and ']' in x:
            bd = x[1:-1].split(',')
            if len(bd) == 2:
                bound, depth = bd
        elif 'in' in x and mod is None:
            mod = term[term.index(x) + 1]
        elif '=>' in x and searchtype is None:
            if subject is None:
                subject = term[term.index(x) - 1]
            if x[-1] == '1':
                searchtype = '=>1'
            elif x[-1] == '+':
                searchtype = '=>+'
            elif x[-1] == '*':
                searchtype = '=>*'
            elif x[-1] == '!':
                searchtype = '=>!'
            if pattern is None:
                pattern = term[term.index(x) + 1]

        elif x == 's.t.' and condition is None: # no sé si se pondrá such that o s.t. o las dos cosas
            break
    condition = ' '.join(term[term.index('s.t.') + 1:])
    
    if '[' in term:
        bd = regex.search('\[[^\]]*\]' )
        b = bd.split(',')[0]
    '''

    if(']' in term):
        term2 = term.split(']')
        if(',' in term2[0]):
            term3 = term2[0].split(',')
            bound = term3[0][1:].strip()
            depth = term3[1].strip()
        else:
            bound = term2[1:]
        term = term2[1]

    if 'in' in term:
        term2 = term.split(':')
        mod = term2[0][3:].strip()
        term = term2[1]

    if 's.t.' in term:
        term2 = term.split('s.t.')
        condition = term2[1].strip()
        term = term2[0]
    searchtype = term[term.index('=>'):term.index('=>') + 3]
    subject = term.split(searchtype)[0].strip()
    pattern = term.split(searchtype)[1].strip()



    '''
    st = '[nn n, m mm] t1 =>* t2 s.t. c1 c2'
    bd = regex.search('\[[^\]]*\]', st)
    print(bd.group(0))
    bd2=bd.group(0).split(',')
    b = bd2[0]
    d = bd2[1]
    print("n: ", b[1:])
    print(" m: ", d[:-1])
    '''
    print("Bound:", bound)
    print("Depth:", depth)
    print("Module:", mod)
    print("Subject:", subject)
    print("Searchtype:", searchtype)
    print("Pattern:", pattern)   
    print("Condition:", condition)
    if mod != None:
        m = maude.getModule(mod)

    t = m.parseTerm(subject)#añadir trycatches en todo esto? o fuera del ifelse?
    t.search(0, m.parseTerm(pattern),m.parseStrategy(bound),condition,depth)
 

else:
    t = "No se ha reconocido el comando introducido"

print("<html><body>")
print("<h4>Result:</h4>")
print(str(t))
print("</body></html>")
