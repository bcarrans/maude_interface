#!/usr/bin/env python3

import sys
import maude
import base64
import traceback
import multiprocessing
import time


### DEFINITIONS
  
def decode_arg(encoded_arg):
    return base64.b64decode(encoded_arg).decode('utf-8')


def getCommand(c):
    c2 = c.split()

    if not c.endswith(' .'):
        raise Exception("Missing . at the end of the command input.")
    
    if len(c2) < 3 or not c.endswith(' .'):
        raise Exception("Incorrect number of arguments.")
    
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
                    pass
                except Exception as e:
                    print("Equality condition error: {e}")

            elif ' : ' in x:
                condAux = x.split(' : ')
                t1 = m.parseTerm(condAux[0].strip())
                t2 = m.parseTerm(condAux[1].strip())               
                try:
                    #condFragment = maude.SortTestCondition(t1, t2)
                    pass
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
                    result += sol, 'with', subs, 'by', path(), '(solution, subs, path)'
                    i += 1
                    if i >= maxIter:
                        break
            else:
                for sol, subs, path, nrew in t.search(searchtype, t2, m.parseStrategy(bound), condition, number):
                    result += str(sol) + " with " + str(subs) + " by " + str(path()) +  " (solution, subs, path)"
                    i += 1
                    if i >= maxIter:
                        break


    else:
        raise Exception("The provided command could not be recognized.")


    ### PRINT RESULT, EXCEPTIONS AND FEEDBACK
    if t is None:
        raise Exception("The command could not be executed successfully")

    else:
        print((inputModule if inputModule else "None") + "<!-- SPLIT -->" + 
              (command if command else "None") + "<!-- SPLIT -->" + 
              (params if params else "None") + "<!-- SPLIT -->" + 
              str(t.getSort()) + "<!-- SPLIT -->" + str(t) + "<!-- SPLIT -->" + "" + "<!-- SPLIT -->" + "")
              # + "<!-- SPLIT -->" + (start_time if start_time else "0s"))

    time.sleep(20)


def maude_command_with_timeout(inputCommand, timeout):
    p = multiprocessing.Process(target=execute_maude_command, args=(inputCommand,))
    p.start()

    p.join(timeout)

    if p.is_alive():
        print("Process exceeded timeout. Terminating...")
        p.terminate()
        p.join()  # Ensure process termination
    else:
        print("Process completed within timeout.")



if __name__ == '__main__':

    try: 
        m = command = params = term = moduleName = bound = number = condition = pattern = subject = searchtypeAux = None
        maxIter = 20
        i = 0
        result = ""

        inputModule = decode_arg(sys.argv[1])
        inputCommand = decode_arg(sys.argv[2])
        
        maude.init()

        maude.input(inputModule)

        timeout = 10
        maude_command_with_timeout(inputCommand, timeout)

        
    except Exception as e:

        feedback = "<br>Term: " + (str(term) if term else "None") + \
            "<br>In-line module: " + (str(moduleName) if moduleName else "None") + \
            ("<br>Bound: " + str(bound) if bound  else "") + \
            ("<br>Number: " + str(number) if number else "") + \
            ("<br>Condition: " + str(condition) if condition else "") + \
            ("<br>Pattern: " + str(pattern) if pattern else "") + \
            ("<br>Subject-Term: " + str(subject) if subject else "") + \
            ("<br>Searchtype: " + str(searchtypeAux) if searchtypeAux else "")
            
        #stack_trace = traceback.format_exc()

        print((inputModule if inputModule else "None") + "<!-- SPLIT -->" + 
                (command if command else "None") + "<!-- SPLIT -->" + 
                (params if params else "None") + "<!-- SPLIT -->" + 
                "" + "<!-- SPLIT -->" + "Error" + "<!-- SPLIT -->" +
                str(e) + "<!-- SPLIT -->" + feedback)
        exit()