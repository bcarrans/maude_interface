#!/C:/Python311/python.exe

import sys
import maude
import base64
import traceback
import re


### DEFINITIONS
  
def decode_arg(encoded_arg):
    return base64.b64decode(encoded_arg).decode('utf-8')


def inputModule(m): # unused, might be useful for error statistics
    pattern = r'mod.*?endm' #or fmod endfm
    matches = re.findall(pattern, m)
    for substring in enumerate(matches, 1):
        maude.input(substring)
    return ", ".join(matches)


def getCommand(c):
    c2 = c.split()
    #if len(c2) < 2 or not c2[-1].endswith(' .'):
        #raise Exception("Incorrect sytanx.")
    command = c2[0]
    term = ' '.join(c2[1:])[:-1]
    return command, term


def getCommandModule(params):
    if 'in' in params:
        aux = params.split(':')
        mod = aux[0][3:].strip()
        params = aux[1]
        return mod, maude.getModule(mod), params
    
    else:
        return None, maude.getCurrentModule(), params


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
            print("Condition syntax error: {e}")

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
                    print("Equality condition error: {e}")

            elif ' : ' in x:
                condAux = x.split(' : ')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())               
                try:
                    #condFragment = maude.SortTestCondition(t1, t2)
                    print("la 2")
                except Exception as e:
                    print("Sort test condition error: {e}")

            elif ':=' in x:
                condAux = x.split(':=')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.AssignmentCondition(t1, t2)
                except Exception as e:
                    print("Assigment condition error: {e}")

            elif '=>' in x:
                condAux = x.split('=>')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.RewriteCondition(t1, t2)
                except Exception as e:
                    print("Rewrite condition error: {e}")

            cond.append(condFragment)
            #conditionFragments.append(condFragment)
        return params, cond

    else:
        return params, None

try: 
    #Initialize all possible Maude parameters (the ones used in matching and strategies are missing creo)
    m = command = params = term = mod = condition = number = pattern = subject = searchtypeAux = None
    bound = gas = depth = -1

    maude_module = decode_arg(sys.argv[1])
    maude_command = decode_arg(sys.argv[2])
    
    maude.init()

    #modules = inputModule(maude_module)
    maude.input(maude_module)

    command, params = getCommand(maude_command)
    #m,  params = getCommandModule(params) # esto no va aqui pedazo de estúpida (see notes)

    p = params.split()

    #### quitar esto (condTest)
    if command == "condition":
        print(' Getting condition...   ')
        params, condition = getCondition(params)
        print('Condition: Cant print condition')



    ### COMMAND PARSING:


    ### REWRITING COMMANDS

    elif command == "reduce" or command == "red": #reduce {in module :} term .
        command = "reduce"
        mod, m, term = getCommandModule(params)
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(params)
            t.reduce()
        

    elif command == "rewrite" or command == "rew": #rewrite {[ bound ]} {in module :} term .
        command = "rewrite"
        term, bound, gas = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)
            if bound is None:            
                t.reduce()  
            else:
                t.rewrite(bound)
            
    elif command == "frewrite" or command == "frew": #frewrite {[ bound {,number} ]} {in module :} term .
        command = "frewrite"
        term, bound, gas = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        t = m.parseTerm(term)
        t.frewrite(bound, gas)

        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)
            if bound is None:            
                t.reduce()  
            else:
                t.rewrite(bound)

    elif command == "erewrite" or command == "erew": #erewrite {[ bound {,number} ]} {in module :} term .
        command = "erewrite"
        term, bound, gas = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        t = m.parseTerm(term)
        ans, nrew = t.erewrite(bound, gas)

    ### MATCHING COMMANDS

    elif command == "match": #match {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
        params, number, b = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        params, condition = getCondition(params)
        pattern = params.split('<=?')[0].strip()
        subject = params.split('<=?')[1].strip()
        t = m.parseTerm(subject)
        for match in t.match(pattern=pattern, condition=condition, withExtension=False, minDepth=None, maxDepth=-1):
            print(match)

        #t.match(pattern=pattern, condition=condition, withExtension=False, minDepth=None, maxDepth=None)
    #withExtension está obsoleto, utilizar maxDepth instead. En la extension dejo el bool o pongo None? en maxDepth de xmatch es 0, en el normal qué? None?
        
    elif command == "xmatch": #xmatch {[ number ]} {in module :} pattern <=? subject-term {such that condition} .
        #Misma que la anterior pero with extension(no, con maxDepth = 0
        params, number, b = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        params, condition = getCondition(params)
        pattern = params.split('<=?')[0].strip()
        subject = params.split('<=?')[1].strip()
        t = m.parseTerm(subject)
        for match in t.match(pattern=pattern, condition=condition, withExtension=True, minDepth=None, maxDepth=0):
            print(match)


    ### SEARCHING COMMANDS

    elif command == "search": #search {[ bound {,depth} ]} {in module :} subject searchtype pattern {such that condition} .
        params, bound, depth = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        params, condition = getCondition(params)
        '''if 's.t.' in params:
            params_2 = params.split('s.t.')
            condition = params_2[1].strip()
            params = params_2[0]'''

        if "=>1" in params:
            searchtypeAux = "=>1"
            searchtype = maude.ONE_STEP
        elif "=>+" in params:
            searchtypeAux = "=>+"
            searchtype = maude.AT_LEAST_ONE_STEP
        elif "=>*" in params:
            searchtypeAux = "=>*"
            searchtype = maude.ANY_STEPS
        elif "=>!" in params:
            searchtypeAux = "=>!"
            searchtype = maude.NORMAL_FORM
        
        subject = params.split(searchtypeAux)[0].strip()
        pattern = params.split(searchtypeAux)[1].strip()

        t = m.parseTerm(pattern) #espera era al reves creo
        t2 = m.parseTerm(subject)
        
        #for sol, subs, path, nrew in t.search(type=searchtype, target=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth):
        for sol, subs, path, nrew in t.search(searchtype, t2, m.parseStrategy(bound)): #, condition=condition, depth=depth):
            print(sol, 'with', subs, 'by', path(), '(solution, subs, path)')
        

        ## hay otro ejemplo mas    
        # t.search(type=searchtype, pattern=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth)


    ### STRATEGIC REWRITING (ignorar de momento, no están suporteadas las estrategias aun)

    elif command == "srewrite" or command == "srew": #srewrite {[ bound ]} {in module :} subject by strategyexpr .
        command = "srewrite"
        params, bound, b = getSquareBrackets(params)
        mod, m, term = getCommandModule(term)
        subject = params.split(' by ')[0].strip()
        strategyexpr = params.split(' by ')[1].strip()
        #print("Bound: ", bound, " Subject: ", subject, " Strategyexpr: ", strategyexpr)
        t = m.parseTerm(subject) 

        for sol, nrew in t.srewrite(m.parseStrategy('swap *')): ## whatt
            print(sol, 'in', nrew, 'rewrites')

        #t.srewrite(expr=strategyexpr,depth=bound) noooo depth es un booleano, es false para este y true para dstrewrite

    elif command == "dsrewrite" or command == "dsrew": #dsrewrite {[ bound ]} {in module :} subject by strategyexpr .
        command == "dsrewrite"
        t = "Es igual que srewrite pero con depth a true"


    ### MISCELLANEOUS

    elif command == "parse": #parse {in module :} term .
        mod, m, term = getCommandModule(params)
        t = m.parseTerm(term)

    elif command == "select": #select module .
        t  = maude.getModule(params)


    else:
        raise Exception("The provided command could not be recognized.")
    

    ### PRINT RESULT, EXCEPTIONS AND FEEDBACK
    
    if t is None:
        print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
        #+ "<!-- SPLIT -->" + "0s")

    else:
    #print(maude_module + "<!-- SPLIT -->" + command + "<!-- SPLIT -->" + params + "<!-- SPLIT -->" + str(t.getSort()) + "<!-- SPLIT -->" + str(t))
        print((maude_module if maude_module else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (str(t) if t else "Nopes"))
            # + "<!-- SPLIT -->" + (start_time if start_time else "0s"))


#except Exception as e:
    #print(f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
#    print(maude_module + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "Nopes") + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + 
#          f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
          #"<!-- SPLIT -->" + start_time)
#    exit()

except Exception as e:
    feedback = "<br>Module: " + (m if m else "None") + \
        "<br>Command: " + (command if command else "None") + \
            "<br>Params: " + (params if params else "None") + \
            "<br>In-line module: " + (mod if mod else "None") + \
            "<br>Term: " + (term if term else "None") + \
        "<br>Bound: " + (bound if bound else "None") + \
        "<br>Gas: " + (gas if gas else "None") + \
       "<br>Condition: " + (condition if condition else "None") + \
       "<br>Number: " + (number if number else "None") + \
        "<br>Pattern: " + (pattern if pattern else "None") + \
       "<br>Subject-Term: " + (subject if subject else "None") + \
        "<br>Searchtype: " + (searchtypeAux if searchtypeAux else "None")
    stack_trace = traceback.format_exc()
    #print(maude_module + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "Nopes") + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + f"{e}<br><br>{stack_trace}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")#<br>{feedback}")
    #print(feedback)
    
    html_feedback = f"<br>__________________<br>Feedback:{feedback}<br>{e}<br><br>{stack_trace}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage."

    print(html_feedback)
    exit()
    

