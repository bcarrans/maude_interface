#!/C:/Python311/python.exe

import sys
import maude
import regex
import re


### DEFINITIONS
def getCommand(c):
    c2 = c.split()
    command = c2[0]
    term = ' '.join(c2[1:])[:-1]
    return command, term


def getCommandModule(params):
    if 'in' in params:
        aux = params.split(':')
        mod = aux[0][3:].strip()
        params = aux[1]
        return maude.getModule(mod), params

    else:
        return maude.getCurrentModule(), params


def getSquareBrackets(params):
    a = None
    b = None
    if'[' in params:
        params_2 = params.split(']')

        if(',' in params_2[0]):
            params_3 = params_2[0].split(',')
            a = params_3[0][1:].strip()
            b = params_3[1].strip()
            
        else:
            a = params_2[0][1:]

        params = params_2[1]
        if a == '':
            a = None

    return params, a, b





### INIT
maude.init()

maude_module = sys.argv[1].replace("^", "")
maude_command = sys.argv[2].replace("^", "")

print("Module: " + maude_module)

maude.input(maude_module)

command, params = getCommand(maude_command)
m, params = getCommandModule(params)

p = params.split()

print("Command: " + command)
print("Parameters: " + params)




### REWRITING
if command == "reduce" or command == "red": #reduce {in module :} term .
    t = m.parseTerm(params)
    t.reduce()

elif command == "rewrite" or command == "rew": #rewrite {[ bound ]} {in module :} term .
    term, bound, b = getSquareBrackets(params)
    print("Bound: ", bound)
    t = m.parseTerm(term)
    t.rewrite(bound=bound)

elif command == "frewrite" or command == "frew": #frewrite {[ bound {,number} ]} {in module :} term .
    term, bound, gas = getSquareBrackets(params)
    print("Bound: ", bound, " Gas: ", gas)
    t = m.parseTerm(term)
    t.frewrite(bound=bound, gas=gas)

elif command == "erewrite" or command == "erew": #erewrite {[ bound {,number} ]} {in module :} term .
    term, bound, gas = getSquareBrackets(params)
    print("Bound: ", bound, " Gas: ", gas)
    t = m.parseTerm(term)
    t.erewrite(bound=bound, gas=gas)


elif command == "continue": #continue {number} .
    #t.frewrite[number, ] del ultimo frewite que se hubiese ejecutado? eing
    t = "Continue no está supporteado todavía"

#loop {in module :} term .(deprecated)

#( identifier* ) (deprecated)


### MATCHING
elif command == "match": #match {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
    params, number, b = getSquareBrackets(params)

    if 's.t.' in params:
        params_2 = params.split('s.t.')
        condition = params_2[1].strip()
        params = params_2[0]

    pattern = params.split('<=?')[0].strip()
    subject = params.split('<=?')[1].strip()

    print("Number: ", number, " Pattern: ", pattern, " Subject-Term: ", subject, " Condition: ", condition)
    t = m.parseTerm(subject)
    t.match(pattern=pattern, condition=condition, withExtension=False,minDepth=None,maxDepth=None) #cual es cual??

elif command == "xmatch": #xmatch {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
    #Misma que la anterior pero with extension
    params, a, b = getSquareBrackets(params)

    if 's.t.' in params:
        params_2 = params.split('s.t.')
        condition = params_2[1].strip()
        params = params_2[0]

    pattern = params.split(' <=? ')[0].strip()
    subject = params.split(' <=? ')[1].strip()

    print("Number: ", a, " Pattern: ", pattern, " Subject-Term: ", subject, " Condition: ", condition)
    t = m.parseTerm(subject)
    t.match(pattern=pattern, condition=condition, withExtension=True,minDepth=None,maxDepth=None)


###SEARCHING
elif command == "search": #search {[ bound {,depth} ]} {in module :} subject searchtype pattern {such that condition} .
    bound = None
    depth = None
    subject = None
    searchtype = None
    pattern = None
    condition = None

    params, bound, depth = getSquareBrackets(params)

    if 's.t.' in params:
        params_2 = params.split('s.t.')
        condition = params_2[1].strip()
        params = params_2[0]

    searchtype = params[params.index('=>'):params.index('=>') + 3]
    subject = params.split(searchtype)[0].strip()
    pattern = params.split(searchtype)[1].strip()

    print("Bound: ", bound)
    print("Depth: ", depth)
    print("Module: ", m)
    print("Subject: ", subject)
    print("Searchtype: ", searchtype)
    print("Pattern: ", pattern)   
    print("Condition: ", condition)

    t = m.parseTerm(subject)
    t.search(type=searchtype, pattern=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth)




### STRATEGIC REWRITING
elif command == "srewrite" or command == "srew": #srewrite {[ bound ]} {in module :} subject by strategyexpr .
    params, bound, b = getSquareBrackets(params)
    subject = params.split(' by ')[0].strip()
    strategyexpr = params.split(' by ')[1].strip()
    print("Bound: ", bound, " Subject: ", subject, " Strategyexpr: ", strategyexpr)
    t = m.parseTerm(subject) 
    t.srewrite(expr=strategyexpr,depth=bound)

elif command == "dsrewrite" or command == "dsrew": #dsrewrite {[ bound ]} {in module :} subject by strategyexpr .
    t = "Ups"


### UNIFICATION, VARIANTS, AND NARROWING

#{irredundant} unify {[ bound ]} {in module :} term1 =? term’1 { /∖ … /∖ termk =? term’k } .
##########con este que hago como que irredumdant????

#{filtered} variant unify {[ bound ]} {in module :} term1 =? term’1 { /∖ … /∖ termk =? term’k } {such that term”1, …, term”n irreducible}.
##### y esto??? que es esto

elif command == "variant": #variant match {[ bound ]} {in module :} term1 <=? term’1 { /∖ … /∖ termk <=? term’k } {such that term”1, …, term”n irreducible} .
    t = m.parseTerm(params)
    t.rewrite()

elif command == "get": #get {irredundant} variants {[ bound ]} {in module :} term {such that term”1, …, term”n irreducible} .
    t = m.parseTerm(params)
    t.rewrite()

#{{fold}} vu-narrow {{variantopts}} {[ bound {,depth} ]} {in module :} pattern1 searchtype pattern2 .
####????????

elif command == "fvu-narrow": #fvu-narrow {[ bound {,depth} ]} {in module :} pattern1 searchtype pattern2 .
    params, bound, depth = getSquareBrackets(params)
    pattern1, serachtype, pattern2 = None
    #t.vu_narrow(type=None, target=None, depth=depth, fold=True, filter=None, delay=None)



### SMT
elif command == "check": #check {in module :} term .
    t = m.parseTerm(params)
    t.check()



### MISCELLANEOUS
elif command == "parse": #parse {in module :} term .
    t = m.parseTerm(params)

elif command == "select": #select module .
    t  = maude.getModule(params)

elif command == "do": #do clear memo { module } .
    if "clear" in params and "memo" in params:
        params = ' '.join(p[2:]).strip()
        if params == '': params = None
        # vale pues no lo encuentro
        # solo está maude.OP_MEMO en operatos attributes, algo de las rules, solo veo el apply que no sea getter, hay 5mil get rules ??

else:
    t = "The provided command could not be recognized"


### PRINT RESULT
print("<html><body>")
print("<h4>Result:</h4>")
print(str(t))
print("</body></html>")