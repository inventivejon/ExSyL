# Prädikate
# Mann
# Frau
# Ehepaar

# Formel
# Mann(X)
# Frau(Y)
# Ehepaar(X, Y)

continueAsking = True
predicates = {}
predicate_equals = {}
functions = []

def AddEqualsPredicate(eqPrName, predicate):
    global predicates
    global predicate_equals
    if predicate in predicates:
        for singleEqPrName in eqPrName:
            if singleEqPrName not in predicate_equals:
                predicate_equals[singleEqPrName] = predicate
                print('Equal Predicate added')
            else:
                print('Equal Predicate already known')
    else:
        print('Predicate not found')
        
def GetOrigPredicate(predicate):
    global predicate_equals
    retVal = predicate
    if predicate in predicate_equals:
        retVal = predicate_equals[predicate]
    return retVal

def AddDetailToPredicate(detail, predicate):
    global predicates
    predicate = GetOrigPredicate(predicate)
    if predicate in predicates:
        print('Prädikat gefunden')
        predicates[predicate] = predicates[predicate] + detail
    else:
        print('Prädikat {} unbekannt'.format(predicate))
        predicates[predicate] = detail
        print('Prädikat wurde hinzugefügt')
        
def AddDetailToPredicateGrouped(detail, predicate):
    global predicates
    predicate = GetOrigPredicate(predicate)
    if predicate in predicates:
        print('Prädikat gefunden')
        predicates[predicate] = predicates[predicate] + [detail]
    else:
        print('Prädikat {} unbekannt'.format(predicate))
        predicates[predicate] = [detail]
        print('Prädikat wurde hinzugefügt')
        
def CheckDetailsInPredicate(details, predicate):
    global predicates
    retVal = 'Nein'
    predicate = GetOrigPredicate(predicate)
    print('Prüfe Prädikat {} mit Details {}'.format(predicate, details))
    if predicate in predicates:
        fulfilled = True
        for detail in details:
            if detail not in predicates[predicate]:
                fulfilled = False
                #print('Not found on predicate')
                # Check if this is in an array
                for dPredicate in predicates[predicate]:
                    #print('Check subarray {}'.format(dPredicate))
                    if detail in dPredicate:
                        fulfilled = True
                if fulfilled == False:
                    print('Detail {} ist nicht in Prädikat'.format(detail))
        if fulfilled:
            retVal = 'Ja'
    else:
        print('Prädikat {} unbekannt'.format(predicate))
        retVal = 'Weiß nicht'
    return retVal

def GetPredicateFromDetail(detail):
    if type(detail) is not str and len(detail) > 0:
        detail = detail[0]
    #print('Called GetPredicateFromDetail with {}'.format(detail))
    global predicates
    retVal = ''
    for predicate in predicates:
        #print("Prüfe Inhalt {} von {}".format(predicates[predicate], predicate))
        if detail in predicates[predicate]:
            retVal = predicate if retVal == '' else retVal + ' und ' + predicate
        for subpredicate in predicates[predicate]:
            if detail in subpredicate and type(subpredicate) is not str:
                retVal = predicate if retVal == '' else retVal + ' und ' + predicate
    #print("Processed. Return value {} now".format(retVal))
    return retVal

def CreateStructuredMask(rawMask, maskInterpreter):
    structuredMasks = []
    print('Call CreateStructuredMask with \'{}\''.format(rawMask))
    if type(rawMask[0]) != str:
        for mask in rawMask:
            print('Call CreateStructuredMask for \'{}\''.format(mask))
            # This is the highest mask level. Always starts with character zero.
            newStructuredMask = CreateStructuredMask(mask, maskInterpreter)
            print("Finished structuring mask with result: {}".format(newStructuredMask))
            structuredMasks = structuredMasks + [newStructuredMask]
            print("Content of structuredMasks now {}".format(structuredMasks))
        return structuredMasks
    else:
        processingValue = rawMask if type(rawMask) == str else rawMask[0]
        processingValue = processingValue.replace('?',' ?').replace('.',' .').replace('!',' !').replace(',',' ,')
        if processingValue.endswith(" ") == False:
            processingValue = processingValue + " " # Adding trail space character to force finish of last symbol
        print('Processing string \'{}\''.format(processingValue))
        initialState = 'raw' # Constant value to be set into searchState as initial and fallback
        characterBuffer = '' # Contains all characters buffered for next processing step
        bufferedSearchState = [initialState] # In case a stateJumps into a different state then this remembers the state before
        searchState = initialState # State control variable of maskBuilder
        bufferedStateContent = [{}]
        stateContent = {} # Store all state specific content here
        
        for singleCharacter in processingValue:
            if searchState == 'raw':
                if singleCharacter in maskInterpreter:
                    if maskInterpreter[singleCharacter]['type'] == 'subGroup': 
                        # Buffer all following character until endCharacter and call in recursive function call
                        # SubGroup control values
                        stateContent = {
                            "subGroupName": maskInterpreter[singleCharacter]['name'],
                            "startCharacter": singleCharacter,
                            "endCharacter": maskInterpreter[singleCharacter]['endCharacter'],
                            "controlCharacterCounter": 1
                        }
                    elif maskInterpreter[singleCharacter]['type'] == 'raw':
                        print("Stop Symbol detected with content: {}".format(characterBuffer))
                        # Raw means next state will be raw. Store the last content into structured mask
                        # Create raw entry for current content
                        if type(characterBuffer) == str:
                            if characterBuffer != '':
                                structuredMasks = structuredMasks + [('raw',characterBuffer)]
                        else:
                            structuredMasks = structuredMasks + characterBuffer
                    elif maskInterpreter[singleCharacter]['type'] == 'arrayCollection':
                        stateContent = {
                            "name": maskInterpreter[singleCharacter]['name'],
                            "arrayCollection": [('raw',characterBuffer)] if type(characterBuffer) == str else characterBuffer,
                            "collectionCharacter": singleCharacter,
                            "endCharacter": maskInterpreter[singleCharacter]['endCharacter']
                        }
                    characterBuffer = ''
                    searchState = maskInterpreter[singleCharacter]['type']
                else:
                    # No control character add current character to buffer
                    characterBuffer = characterBuffer + singleCharacter
            elif searchState == 'subGroup':
                # In SearchState 'subGroup'
                if singleCharacter == stateContent['startCharacter']:
                    stateContent['controlCharacterCounter'] = stateContent['controlCharacterCounter'] + 1
                elif singleCharacter == stateContent['endCharacter']:
                    stateContent['controlCharacterCounter'] = stateContent['controlCharacterCounter'] - 1
                else:
                    characterBuffer = characterBuffer + singleCharacter

                if stateContent['controlCharacterCounter'] == 0:
                    # End of subGroup
                    subContent = CreateStructuredMask(characterBuffer + " ", maskInterpreter)
                    print("Finished subCall with result {}".format(subContent))
                    characterBuffer = [(stateContent['subGroupName'], subContent)]
                    print("Finished subGroup: {}".format(characterBuffer))
                    # Reset subGroup control variables
                    stateContent = bufferedStateContent[len(bufferedSearchState) - 1]
                    searchState = bufferedSearchState[len(bufferedSearchState) - 1]
                    if bufferedSearchState[len(bufferedSearchState) - 1] != initialState:
                        print("Removing last buffered state {} with {}".format(bufferedSearchState, bufferedStateContent))
                        bufferedSearchState = bufferedSearchState[:-1]
                        bufferedStateContent = bufferedStateContent[:-1]
                        print("Result buffered state after removed entry {} with {}".format(bufferedSearchState, bufferedStateContent))
            elif searchState == 'arrayCollection':
                # bufferedSearchState
                if singleCharacter in maskInterpreter and maskInterpreter[singleCharacter]['type'] == 'subGroup':
                    # Buffer all following character until endCharacter and call in recursive function call
                    # Buffer last state
                    bufferedSearchState = bufferedSearchState + [searchState]
                    bufferedStateContent = bufferedStateContent + [stateContent]
                    # SubGroup control values
                    stateContent = {
                        "subGroupName": maskInterpreter[singleCharacter]['name'],
                        "startCharacter": singleCharacter,
                        "endCharacter": maskInterpreter[singleCharacter]['endCharacter'],
                        "controlCharacterCounter": 1
                    }
                    characterBuffer = ''
                    searchState = maskInterpreter[singleCharacter]['type']
                else:
                    # In SearchState 'Array Collection'
                    if singleCharacter == stateContent['collectionCharacter']:
                        # Another alternative will follow
                        if type(characterBuffer) == str:
                            stateContent['arrayCollection'] = stateContent['arrayCollection'] + [('raw',characterBuffer)]
                        else:
                            stateContent['arrayCollection'] = stateContent['arrayCollection'] + characterBuffer
                        characterBuffer = ''
                    elif singleCharacter == stateContent['endCharacter']:
                        if type(characterBuffer) == str:
                            stateContent['arrayCollection'] = stateContent['arrayCollection'] + [('raw',characterBuffer)]
                        else:
                           stateContent['arrayCollection'] = stateContent['arrayCollection'] + characterBuffer 
                        structuredMasks = structuredMasks + [('alternative', stateContent['arrayCollection'])]
                        stateContent = bufferedStateContent[len(bufferedSearchState) - 1]
                        characterBuffer = ''
                        searchState = bufferedSearchState[len(bufferedSearchState) - 1]
                        if bufferedSearchState[len(bufferedSearchState) - 1] != initialState:
                            bufferedSearchState = bufferedSearchState[:-1]
                            bufferedStateContent = bufferedStateContent[:-1]
                    else:
                        characterBuffer = characterBuffer + singleCharacter

    if type(rawMask) != str and len(rawMask) > 1 and type(rawMask[1]) != str:
        return [rawMask[1], structuredMasks]
    else:
        return structuredMasks

# Syntax
# <Keyword> Object (z.B. <Detail>)
# [] Optional (z.B. [ein]) 
# / alternativ (muss auch ans Ende der Alternative z.B. ein/eine/einer/)
# {} Kann sich beliebig oft wiederholen (z.B. {})

masks = []
# Fragesätze
masks = [("[Guten Tag]|Hi|[Grüß Gott]|Hallo| <Detail>", lambda library: print("Hallo"))]
masks = masks + [("Ist <Detail> ein|eine|der|die|das| <Prädikat>?", lambda library: print("Called the correct function with {}".format(library)))]
masks = masks + [("Sind <Detail> {,|und <Detail>}| und <Detail> ein|eine|der|die|das| <Prädikat>?", lambda library: print("Called the correct function with {}".format(library)))]
masks = masks + [("Was ist <Detail>?", lambda library: print("Called the correct function with {}".format(library)))]
# Aussagesätze
masks = masks + [("<Detail> ist <Prädikat>.|", lambda library: print("Called the correct function with {}".format(library)))]
masks = masks + [("<Detail> {,|und|oder <Detail>} sind <Prädikat>.|", lambda library: print("Called the correct function with {}".format(library)))]
masks = masks + [("<Detail> {,|und|oder <Detail>} sind alle <Prädikat>.|", lambda library: print("Called the correct function with {}".format(library)))]
masks = masks + [("<Detail> {,|und|oder <Prädikat>} sind wie <Prädikat>.|", lambda library: print("Called the correct function with {}".format(library)))]

maskInterpreter = {
    # Start and End Character need to be different in case of SubGroup
    # type is a key word. Currently supported: subGroup, alternative, raw
    "<": { "type": "subGroup", "name": "object", "endCharacter": ">" },
    "{": { "type": "subGroup", "name": "repeatable", "endCharacter": "}" },
    "[": { "type": "subGroup", "name": "subSentence", "endCharacter": "]" },
    "|": { "type": "arrayCollection", "name": "alternative", "endCharacter": " " },
    " ": { "type": "raw" }
}

structured_mask = CreateStructuredMask(masks, maskInterpreter)

def CompareToMask(mask, sentence):
    return (False, {})

def DrawStructuredMaskTree(structuredMask, level):
    indentCounter = 0
    indentCharacters = "   "
    realIndent = ""
    while indentCounter < level:
        indentCounter = indentCounter + 1
        realIndent = realIndent + indentCharacters

    entryCounter = 0
    for singleEntry in structuredMask:
        if entryCounter == 0 and level > 0:
            realIndent = realIndent[:-2]
            realIndent = realIndent + "->"
        elif len(realIndent) > 0:
            realIndent = realIndent[:-2]
            realIndent = realIndent + "  "
        if type(singleEntry[1]) != str:
            print("{}|{}".format(realIndent, singleEntry[0]))
            DrawStructuredMaskTree(singleEntry[1], level + 1)
        else:
            print("{}|{}".format(realIndent, singleEntry[1]))
        entryCounter = entryCounter + 1

while continueAsking:
    erg = input('Tippe etwas ein (q,h): ')
    
    if erg == 'q':
        print('End of Programm')
        continueAsking = False
    elif erg == 'h':
        print('''
        	      lp - Liste aller Prädikate
        	      leqp - Liste aller equal Prädikate
        	      p - Neues Prädikat
        	      lf - Liste aller Formeln
                  lm - Liste alle Masken auf
                  lsm - Liste alle strukturierten Masken auf
        	      f - Neue Formel
                  i - Interpreter
        	      h - Hilfe
        	      q - Beenden
        	      ''')
    elif erg == 'p':
        new_predicate = input('Gib das neue Prädikat ein: ')
        AddDetailToPredicate([], new_predicate)
        print('Neues Prädikat {} wurde hinzugefügt'.format(new_predicate))
    elif erg == 'lp':
        print('{}'.format(predicates))
    elif erg == 'leqp':
        print('{}'.format(predicate_equals))
    elif erg == 'f':
        new_function = input('Gib die neue Funktion ein:')
        functions = functions + [new_function]
        print('Neue Formel {} wurde hinzugefügt'.format(new_function))
    elif erg == 'lf':
        print('{}'.format(functions))
    elif erg == 'lm':
        print('{}'.format(masks))
    elif erg.startswith('lm '):
        splitErg = erg.split(" ")
        print('{}'.format(masks[int(splitErg[1])]))
    elif erg == 'lsm':
        value = erg.split(" ")
        print('{}'.format(structured_mask))
    elif erg.startswith('lsm '):
        splitErg = erg.split(" ")
        print('{}'.format(structured_mask[int(splitErg[1])]))
    elif erg.startswith('dsm '):
        splitErg = erg.split(" ")
        DrawStructuredMaskTree(structured_mask[int(splitErg[1])][1], 0)
    else:
        foundMask = False
        satz = list(filter(lambda a: a != '', erg.replace('?', ' ?').replace('.',' .').replace(',',' ,').split(" ")))
        for singleMask in structured_mask:
            compResult = CompareToMask(singleMask[1], satz)
            if compResult[0]:
                print("Satz passt zur Maske: {} mit Ergebnis: {}".format(singleMask, compResult))
                singleMask[0](compResult[1])
                foundMask = True
                break
            if foundMask == False:
                print("Wie bitte?")
    #print("{}".format(erg))