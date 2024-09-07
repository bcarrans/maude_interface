#!/usr/bin/env python3

import sys
import maude
import base64
import traceback


### DEFINITIONS
  
def decode_arg(encoded_arg):
    return base64.b64decode(encoded_arg).decode('utf-8')


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
        moduleName = aux[0][3:].strip()
        params = aux[1]
        return moduleName, maude.getModule(moduleName), params
    
    else:
        aux = str(maude.getCurrentModule()).split()
        if len(aux) < 2:
            return aux[0], maude.getCurrentModule(), params
        else:
            return aux[1], maude.getCurrentModule(), params


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

    return a, b, params


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
    ### Initialize all possible input parameters (the ones used in matching and strategies are missing creo)
    m = command = params = term = moduleName = bound = number = condition = pattern = subject = searchtypeAux = None
    maxIter = 20
    i = 0
    result = ""

    inputModule = decode_arg(sys.argv[1])
    inputCommand = decode_arg(sys.argv[2])
    
    maude.init()

    maude.input(inputModule)

    ### Parse input
    command, params = getCommand(inputCommand)
    bound, number, term = getSquareBrackets(params)
    moduleName, m, term = getCommandModule(term)

    ### Optional parameters
    if bound is None:
        bound = -1
    if number is None:
        number = -1


    ### REWRITING COMMANDS

    if command == "reduce" or command == "red": #reduce {in module :} term .
        command = "reduce"
        print("4")
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)
            t.reduce()

    elif command == "rewrite" or command == "rew": #rewrite {[ bound ]} {in module :} term .
        command = "rewrite"
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)
            t.rewrite(bound)
            
    elif command == "frewrite" or command == "frew": #frewrite {[ bound {,number} ]} {in module :} term .
        command = "frewrite"
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)
            t.frewrite(bound, number)

    elif command == "erewrite" or command == "erew": #erewrite {[ bound {,number} ]} {in module :} term .
        command = "erewrite"
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(term)        
            ans, nrew = t.erewrite(bound, number)


    ### MATCHING COMMANDS

    elif command == "match": #match {[ number aka bound]} {in module :} pattern <=? subject-term {such that condition} .
        term, condition = getCondition(term)
        pattern = term.split('<=?')[0].strip()
        subject = term.split('<=?')[1].strip()
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(subject)
            if condition is None:
                for match in t.match(pattern, bound, -1):
                    print(match)
            else:
                for match in t.match(pattern, condition, bound, -1):
                    print(match)
        
    elif command == "xmatch": #xmatch {[ number aka bound]} {in module :} pattern <=? subject-term {such that condition} .
        term, condition = getCondition(term)
        pattern = term.split('<=?')[0].strip()
        subject = term.split('<=?')[1].strip()
        if m is None:
            raise Exception("No module found.")
        else:
            t = m.parseTerm(subject)
            if condition is None:
                for match in t.match(pattern, bound, 0):
                    print(match)
            else:
                for match in t.match(pattern, condition, bound, 0):
                    print(match)


    ### SEARCHING COMMANDS

    elif command == "search": #search {[ bound {,depth aka number} ]} {in module :} subject searchtype pattern {such that condition} .
        #term, condition = getCondition(term)
        condition = None

        if "=>1" in term:
            searchtypeAux = "=>1"
            searchtype = maude.ONE_STEP
        elif "=>+" in term:
            searchtypeAux = "=>+"
            searchtype = maude.AT_LEAST_ONE_STEP
        elif "=>*" in term:
            searchtypeAux = "=>*"
            searchtype = maude.ANY_STEPS
        elif "=>!" in term:
            searchtypeAux = "=>!"
            searchtype = maude.NORMAL_FORM
        
        subject = term.split(searchtypeAux)[0].strip()
        pattern = term.split(searchtypeAux)[1].strip()
        
        if m is None:
            raise Exception("No module found.")
        else:
            t2 = m.parseTerm(pattern) #espera era al reves creo
            t = m.parseTerm(subject)
            if bound == -1:
                print("sin bound")
                for sol, subs, path, nrew in t.search(searchtype, t2, condition, number):                    
                    result += sol, 'with', subs, 'by', path(), '(solution, subs, path)'
                    i += 1
                    if i >= maxIter:
                        break
            else:
                print("con bound")
                for sol, subs, path, nrew in t.search(searchtype, t2, m.parseStrategy(bound), condition, number):
                    result += str(sol) + " with " + str(subs) + " by " + str(path()) +  " (solution, subs, path)"
                    i += 1
                    if i >= maxIter:
                        break


    else:
        raise Exception("The provided command could not be recognized.")


    ### PRINT RESULT, EXCEPTIONS AND FEEDBACK
    if t is None:
        print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
        #+ "<!-- SPLIT -->" + "0s")

    else:
    #print(maude_module + "<!-- SPLIT -->" + command + "<!-- SPLIT -->" + params + "<!-- SPLIT -->" + str(t.getSort()) + "<!-- SPLIT -->" + str(t))
        print("Empty module" + "<!-- SPLIT -->" + "Empty command" + "<!-- SPLIT -->" + "No params" + "<!-- SPLIT -->" + "Nopes" + "<!-- SPLIT -->" + "Nopes")
        #print((inputModule if inputModule else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (result if result else (str(t) if t else "Nopes")))
            # + "<!-- SPLIT -->" + (start_time if start_time else "0s"))

    #print((inputModule if inputModule else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (str(t) if t else "Nopes"))


#except Exception as e:
    #print(f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
#    print(inputModule + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "Nopes") + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + 
#          f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
          #"<!-- SPLIT -->" + start_time)
#    exit()

except Exception as e:

    feedback = "<br>Module: " + (str(m) if m else "None") + \
        "<br>Command: " + (str(command) if command else "None") + \
        "<br>Params: " + (str(params) if params else "None") + \
        "<br>Term: " + (str(term) if term else "None") + \
        "<br>In-line module: " + (str(moduleName) if moduleName else "None") + \
        "<br>Bound: " + (str(bound) if bound else "None") + \
        "<br>Number: " + (str(number) if number else "None") + \
        "<br>Condition: " + (str(condition) if condition else "None") + \
        "<br>Pattern: " + (str(pattern) if pattern else "None") + \
        "<br>Subject-Term: " + (str(subject) if subject else "None") + \
        "<br>Searchtype: " + (str(searchtypeAux) if searchtypeAux else "None")
        #si bound y number son -1 tb son none. si son ciertos comandos no es bound si no number y no es number si no depth

    stack_trace = traceback.format_exc()
    #print(inputModule + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "Nopes") + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + f"{e}<br><br>{stack_trace}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")#<br>{feedback}")
    #print(feedback)
    html_feedback = f"<br>__________________<br>Feedback:{feedback}<br>{e}<br><br>{stack_trace}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage."

    print(html_feedback)
    exit()
    

