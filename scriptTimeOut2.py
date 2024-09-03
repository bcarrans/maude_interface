#!/C:/Python311/python.exe

import sys
import maude
import base64
import traceback
import threading
import signal


### DEFINITIONS

class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Execution timed out")


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

def execute_maude_command(inputCommand):
    global t
    
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
                for sol, subs, path, nrew in t.search(searchtype, t2, condition, number):
                    print(sol, 'with', subs, 'by', path(), '(solution, subs, path)')
            else:
                for sol, subs, path, nrew in t.search(searchtype, t2, m.parseStrategy(bound), condition, number):
                    print(sol, 'with', subs, 'by', path(), '(solution, subs, path)')


    else:
        raise Exception("The provided command could not be recognized.")
    ### PRINT RESULT, EXCEPTIONS AND FEEDBACK
    if t is None:
        print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
        #+ "<!-- SPLIT -->" + "0s")

    else:
    #print(maude_module + "<!-- SPLIT -->" + command + "<!-- SPLIT -->" + params + "<!-- SPLIT -->" + str(t.getSort()) + "<!-- SPLIT -->" + str(t))
        print((inputModule if inputModule else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (str(t) if t else "Nopes"))
            # + "<!-- SPLIT -->" + (start_time if start_time else "0s"))

    #print((inputModule if inputModule else "Empty module") + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "No params") + "<!-- SPLIT -->" + (str(t.getSort()) if t else "Nopes") + "<!-- SPLIT -->" + (str(t) if t else "Nopes"))
def maude_command_with_timeout(inputCommand, timeout):
    def target():
        try:
            execute_maude_command(inputCommand)
        except Exception as e:
            print(f"Error: {e}")

    thread = threading.Thread(target=target)
    thread.start()

    # Join the thread with the specified timeout
    thread.join(timeout)

    # Check if the thread is still alive after the timeout
    if thread.is_alive():
        # If the thread is still alive, it means it has not finished executing
        # Forcefully terminate the thread
        thread.join(0)  # Join with a timeout of 0 to force the thread to exit immediately

        # Check if the thread is still alive after the forced termination
        if thread.is_alive():
            # If the thread is still alive, it means the execution has exceeded the timeout
            raise TimeoutException("Execution timed out")


try: 
    print("1")
    timeout = 1
    
    print("2")
    ### Initialize all possible input parameters (the ones used in matching and strategies are missing creo)
    m = command = params = term = moduleName = bound = number = condition = pattern = subject = searchtypeAux = None
    print("3")
    inputModule = decode_arg(sys.argv[1])
    inputCommand = decode_arg(sys.argv[2])
    
    maude.init()

    maude.input(inputModule)
    t = None
    command = None  # Initialize command variable
    
    try:
        maude_command_with_timeout(inputCommand, timeout)
    except TimeoutException as e:
        print(e)
    
   


    
#except Exception as e:
    #print(f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
#    print(inputModule + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + (params if params else "Nopes") + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + 
#          f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")
          #"<!-- SPLIT -->" + start_time)
#    exit()
except TimeoutException as e:
    print("Esto" + "<!-- SPLIT -->" + "No" + "<!-- SPLIT -->" + "funciona" + "<!-- SPLIT -->" + "parece" + "<!-- SPLIT -->" + "no")
    #print(maude_module + "<!-- SPLIT -->" + (command if command else "Empty command") + "<!-- SPLIT -->" + "Nopes" + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + f"{e}<br><br>You can find <a href='https://github.com/bcarrans/maude_interface/blob/main/README.md'>here</a> a list of the currently supported commands<br>or consult the <a href='https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf'>Maude Manual</a> for more information about their usage.")

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