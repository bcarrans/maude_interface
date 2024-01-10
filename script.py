#!/C:/Python311/python.exe

import sys
import maude


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
        paramsAux = params.split(']')

        if(',' in paramsAux[0]):
            paramsAux2 = paramsAux[0].split(',')
            a = paramsAux2[0][1:].strip()
            b = paramsAux2[1].strip()
            
        else:
            a = paramsAux[0][1:]

        params = paramsAux[1]
        if a == '':
            a = None

    return params, a, b


def getCondition(params):
    if 's.t.' in params or 'such that' in params:

        if 's.t.' in params:
            paramsAux = params.split('s.t.')
        elif 'such that' in params:
            paramsAux = params.split('such that')

        condStr = paramsAux[1].strip()
        params = paramsAux[0]
        condFrags = condStr.split(' /\ ')

        try:
            cond = maude.Condition(3)
        except Exception as e:
            print("Error al declarar la condicion: {e}")

        #conditionFragments = []

        for x in condFrags:
            print("Fragmento: ", x)
            if '=' in x:
                condAux = x.split('=')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    #condFragment = maude.EqualityCondition(t1, t2)
                    print("aaa")
                except Exception as e:
                    print("Error en la equality condition: {e}")

            elif ' : ' in x:
                condAux = x.split(' : ')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())               
                try:
                    #condFragment = maude.SortTestCondition(t1, t2)
                    print("la 2")
                except Exception as e:
                    print("Error en la sorttest condition: {e}")

            elif ':=' in x:
                condAux = x.split(':=')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.AssignmentCondition(t1, t2)
                except Exception as e:
                    print("Error en la assigment condition: {e}")

            elif '=>' in x:
                condAux = x.split('=>')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.RewriteCondition(t1, t2)
                except Exception as e:
                    print("Error en la rewrite condition: {e}")

            cond.append(condFragment)
            #conditionFragments.append(condFragment)
        return params, cond

    else:
        return params, None



### INIT
maude.init()

maude_module = sys.argv[1].replace("^", "")
maude_command = sys.argv[2].replace("^", "")

print("Module: " + maude_module)

maude.input(maude_module)

command, params = getCommand(maude_command)
m,  params = getCommandModule(params)

p = params.split()

print("Command: " + command)
print("Parameters: " + params)

#term, bound, gas, condition, number, pattern, subjectTerm, searchtype, depth = None


#### quitar esto (condTest)
if command == "condition":
    print(' Getting condition...   ')
    params, condition = getCondition(params)
    print('Condition: Cant print condition')

### REWRITING
elif command == "reduce" or command == "red": #reduce {in module :} term .
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
    ans, nrew = t.erewrite(bound=bound, gas=gas)
    print(t,'->',ans,'in',nrew,'rewrites')


### MATCHING
elif command == "match": #match {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
    params, number, b = getSquareBrackets(params)
    params, condition = getCondition(params)
    pattern = params.split('<=?')[0].strip()
    subjectTerm = params.split('<=?')[1].strip()
    print("Number: ", number, " Pattern: ", pattern, " Subject-Term: ", subjectTerm, " Condition: ", condition)
    t = m.parseTerm(subjectTerm)
    for match in t.match(pattern=pattern, condition=condition, withExtension=False, minDepth=None, maxDepth=-1):
         print(match)

    #t.match(pattern=pattern, condition=condition, withExtension=False, minDepth=None, maxDepth=None)
#withExtension está obsoleto, utilizar maxDepth instead. En la extension dejo el bool o pongo None? en maxDepth de xmatch es 0, en el normal qué? None?
    
elif command == "xmatch": #xmatch {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
    #Misma que la anterior pero with extension(no, con maxDepth = 0
    params, number, b = getSquareBrackets(params)
    params, condition = getCondition(params)
    pattern = params.split('<=?')[0].strip()
    subject = params.split('<=?')[1].strip()
    print("Number: ", number, " Pattern: ", pattern, " Subject-Term: ", subject, " Condition: ", condition)
    t = m.parseTerm(subject)
    for match in t.match(pattern=pattern, condition=condition, withExtension=True, minDepth=None, maxDepth=0):
         print(match)



###SEARCHING
elif command == "search": #search {[ bound {,depth} ]} {in module :} subject searchtype pattern {such that condition} .
    params, bound, depth = getSquareBrackets(params)
    params, condition = getCondition(params)

    '''if 's.t.' in params:
        params_2 = params.split('s.t.')
        condition = params_2[1].strip()
        params = params_2[0]'''

    if "=>1" in params:
        searchtype = maude.ONE_STEP
    elif "=>+" in params:
        searchtype = maude.AT_LEAST_ONE_STEP
    elif "=>*" in params:
        searchtype = maude.ANY_STEPS
    elif "=>!" in params:
        searchtype = maude.NORMAL_FORM

    #searchtype = params[params.index('=>'):params.index('=>') + 3]
    subjectTerm = params.split(searchtype)[0].strip()
    pattern = params.split(searchtype)[1].strip()

    print("Bound: ", bound, "Depth: ", depth, "Module: ", m, "Subject term: ", subjectTerm, "Searchtype: ", searchtype, "Pattern: ", pattern, "Condition: ", condition)

    t = m.parseTerm(pattern) #espera era al reves creo
    t2 = m.parseTerm(subjectTerm)


    for sol, subs, path, nrew in t.search(ype=searchtype, pattern=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth):
	    print(sol, 'with', subs, 'by', path(), '(solution, subs, path)')
    

    ## hay otro ejemplo mas    
    # t.search(type=searchtype, pattern=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth)


### STRATEGIC REWRITING (ignorar de momento, no están suporteadas las estrategias aun)
elif command == "srewrite" or command == "srew": #srewrite {[ bound ]} {in module :} subject by strategyexpr .
    params, bound, b = getSquareBrackets(params)
    subject = params.split(' by ')[0].strip()
    strategyexpr = params.split(' by ')[1].strip()
    print("Bound: ", bound, " Subject: ", subject, " Strategyexpr: ", strategyexpr)
    t = m.parseTerm(subject) 

    for sol, nrew in t.srewrite(m.parseStrategy('swap *')): ## whatt
	    print(sol, 'in', nrew, 'rewrites')

    #t.srewrite(expr=strategyexpr,depth=bound) noooo depth es un booleano, es false para este y true para dstrewrite

elif command == "dsrewrite" or command == "dsrew": #dsrewrite {[ bound ]} {in module :} subject by strategyexpr .
    t = "Es igual que srewrite pero con depth a true"



### MISCELLANEOUS
elif command == "parse": #parse {in module :} term .
    t = m.parseTerm(params)

elif command == "select": #select module .
    t  = maude.getModule(params)

else:
    t = "The provided command could not be recognized"


### PRINT RESULT
print("<html><body>")
print("<h4>Result:</h4>")
print(str(t))
print("</body></html>")