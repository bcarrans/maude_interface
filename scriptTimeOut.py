#!/C:/Python311/python.exe

import sys
import maude
import base64
import threading

### DEFINITIONS
  
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Execution timed out")

def decode_arg(encoded_arg):
    return base64.b64decode(encoded_arg).decode('utf-8')

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
            print(f"Condition syntax error: {e}")

        for x in condFrags:
            print("Fragment: ", x)
            if '=' in x:
                condAux = x.split('=')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    # condFragment = maude.EqualityCondition(t1, t2)
                    print("aaa")
                except Exception as e:
                    print(f"Equality condition error: {e}")

            elif ' : ' in x:
                condAux = x.split(' : ')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())               
                try:
                    # condFragment = maude.SortTestCondition(t1, t2)
                    print("la 2")
                except Exception as e:
                    print(f"Sort test condition error: {e}")

            elif ':=' in x:
                condAux = x.split(':=')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.AssignmentCondition(t1, t2)
                except Exception as e:
                    print(f"Assignment condition error: {e}")

            elif '=>' in x:
                condAux = x.split('=>')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())
                try:
                    condFragment = maude.RewriteCondition(t1, t2)
                except Exception as e:
                    print(f"Rewrite condition error: {e}")

            cond.append(condFragment)
        return params, cond
    else:
        return params, None

def execute_maude_command():
    global t
    command, params = getCommand(maude_command)
    m, params = getCommandModule(params)
    p = params.split()

    if command == "condition":
        print('Getting condition...')
        params, condition = getCondition(params)
        print('Condition: Cant print condition')

    elif command == "reduce" or command == "red":
        command = "reduce"
        t = m.parseTerm(params)
        t.reduce()

    elif command == "rewrite" or command == "rew":
        command = "rewrite"
        term, bound, b = getSquareBrackets(params)
        print("Bound: ", bound)
        t = m.parseTerm(term)
        t.rewrite(bound=bound)

    elif command == "frewrite" or command == "frew":
        command = "frewrite"
        term, bound, gas = getSquareBrackets(params)
        print("Bound: ", bound, " Gas: ", gas)
        t = m.parseTerm(term)
        t.frewrite(bound=bound, gas=gas)

    elif command == "erewrite" or command == "erew":
        command = "erewrite"
        term, bound, gas = getSquareBrackets(params)
        print("Bound: ", bound, " Gas: ", gas)
        t = m.parseTerm(term)
        ans, nrew = t.erewrite(bound=bound, gas=gas)
        print(t, '->', ans, 'in', nrew, 'rewrites')

    elif command == "match":
        params, number, b = getSquareBrackets(params)
        params, condition = getCondition(params)
        pattern = params.split('<=?')[0].strip()
        subjectTerm = params.split('<=?')[1].strip()
        print("Number: ", number, " Pattern: ", pattern, " Subject-Term: ", subjectTerm, " Condition: ", condition)
        t = m.parseTerm(subjectTerm)
        for match in t.match(pattern=pattern, condition=condition, withExtension=False, minDepth=None, maxDepth=-1):
            print(match)

    elif command == "xmatch":
        params, number, b = getSquareBrackets(params)
        params, condition = getCondition(params)
        pattern = params.split('<=?')[0].strip()
        subject = params.split('<=?')[1].strip()
        print("Number: ", number, " Pattern: ", pattern, " Subject-Term: ", subject, " Condition: ", condition)
        t = m.parseTerm(subject)
        for match in t.match(pattern=pattern, condition=condition, withExtension=True, minDepth=None, maxDepth=0):
            print(match)

    elif command == "search":
        params, bound, depth = getSquareBrackets(params)
        feedback = feedback + "<br>Bound: " + (bound if bound else "None") + "<br>Depth: " + (depth if depth else "None") + "<br>Remainig params: " + params
        params, condition = getCondition(params)
        feedback = feedback + "<br>Condition: " + (condition if condition else "None") + "<br>Remainig params: " + params
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
        
        feedback = feedback + "<br>Searchtype: " + (searchtypeAux if searchtypeAux else "None")
        subjectTerm = params.split(searchtypeAux)[0].strip()
        feedback = feedback + "<br>SubjectTerm: " + (subjectTerm if subjectTerm else "None") + "<br>Remainig params: " + params
        pattern = params.split(searchtypeAux)[1].strip()
        print("Bound: ", bound, "Depth: ", depth, "Module: ", m, "Subject term: ", subjectTerm, "Searchtype: ", searchtype, "Pattern: ", pattern, "Condition: ", condition)

        t = m.parseTerm(pattern) #espera era al reves creo
        t2 = m.parseTerm(subjectTerm)
        
        #for sol, subs, path, nrew in t.search(type=searchtype, target=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth):
        for sol, subs, path, nrew in t.search(searchtype, t2, m.parseStrategy(bound)): #, condition=condition, depth=depth):
            print(sol, 'with', subs, 'by', path(), '(solution, subs, path)')
        

        ## hay otro ejemplo mas    
        # t.search(type=searchtype, pattern=m.parseTerm(pattern), strategy=m.parseStrategy(bound), condition=condition, depth=depth)

    elif command == "srewrite" or command == "srew":
        command = "srewrite"
        params, bound, b = getSquareBrackets(params)
        subject = params.split(' by ')[0].strip()
        strategyexpr = params.split(' by ')[1].strip()
        print("Bound: ", bound, " Subject: ", subject, " Strategyexpr: ", strategyexpr)
        t = m.parseTerm(subject)
        for sol, nrew in t.srewrite(m.parseStrategy('swap *')):
            print(sol, 'in', nrew, 'rewrites')

    elif command == "dsrewrite" or command == "dsrew":
        command == "dsrewrite"
        t = "Es igual que srewrite pero con depth a true"

    elif command == "parse":
        t = m.parseTerm(params)

    elif command == "select":
        t = maude.getModule(params)

    else:
        raise Exception("The provided command could not be recognized.")

    if t is None:
        print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
    else:
        print((maude_module if maude_module else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (str(t) if t else "Nopes"))

try: 
    timeout_duration = 1

    maude_module = decode_arg(sys.argv[1])
    maude_command = decode_arg(sys.argv[2])
    
    maude.init()
    maude.input(maude_module)

    t = None
    command = None  # Initialize command variable
    execution_thread = threading.Thread(target=execute_maude_command)
    execution_thread.start()
    execution_thread.join(timeout_duration)

    if execution_thread.is_alive():
        raise TimeoutException("Execution timed out")

except TimeoutException as e:
    print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
    #print(maude_module + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + "Nopes" + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
except Exception as e:
    print(maude_module + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + "Nopes" + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
