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

def CreateStructuredMask(rawMask):
    structuredMasks = []
    print('Call CreateStructuredMask with \'{}\''.format(rawMask))
    if type(rawMask[0]) != str:
        for mask in rawMask:
            print('Call CreateStructuredMask for \'{}\''.format(mask))
            structuredMasks = structuredMasks + [CreateStructuredMask(mask)]
    else:
        processingValue = rawMask if type(rawMask) == str else rawMask[0]
        print('Processing string \'{}\''.format(processingValue))
        objectTemplateCounter = 0
        optionalContentCounter = 0
        repeatableContentCounter = 0
        stringBuffer = ''
        for singleCharacter in processingValue:
            alternativeOption = False
            constantQuestionMark = False
            constantDotMark = False
            SymbolEndMarker = False
            objectEndMarker = False
            repeatableContentEndMarker = False
            optionalContentEndMarker = False
            # Pre-Interpretation
            if singleCharacter == '<' and optionalContentCounter == 0 and repeatableContentCounter == 0:
                objectTemplateCounter = objectTemplateCounter + 1
            elif singleCharacter == '>' and optionalContentCounter == 0 and repeatableContentCounter == 0:
                objectTemplateCounter = objectTemplateCounter - 1
                if objectTemplateCounter == 0:
                    objectEndMarker = True
            elif singleCharacter == '{' and objectTemplateCounter == 0 and optionalContentCounter == 0:
                repeatableContentCounter = repeatableContentCounter + 1
            elif singleCharacter == '}' and objectTemplateCounter == 0 and optionalContentCounter == 0:
                repeatableContentCounter = repeatableContentCounter - 1
                if repeatableContentCounter == 0:
                    repeatableContentEndMarker = True
            elif singleCharacter == '[' and objectTemplateCounter == 0 and repeatableContentCounter == 0:
                optionalContentCounter = optionalContentCounter + 1
            elif singleCharacter == ']' and objectTemplateCounter == 0 and repeatableContentCounter == 0:
                optionalContentCounter = optionalContentCounter - 1
                if optionalContentCounter == 0:
                    optionalContentEndMarker = True
            elif singleCharacter == '/' and objectTemplateCounter == 0 and optionalContentCounter == 0 and repeatableContentCounter == 0:
                alternativeOption = True
            elif singleCharacter == '?' and objectTemplateCounter == 0 and optionalContentCounter == 0 and repeatableContentCounter == 0:
                constantQuestionMark = True
            elif singleCharacter == '.' and objectTemplateCounter == 0 and optionalContentCounter == 0 and repeatableContentCounter == 0:
                constantDotMark = True
            elif singleCharacter == ' ' and objectTemplateCounter == 0 and optionalContentCounter == 0 and repeatableContentCounter == 0:
                SymbolEndMarker = True
            else:
                stringBuffer = stringBuffer + singleCharacter
            # Processing control variables
            if SymbolEndMarker:
                if stringBuffer!='':
                    structuredMasks = structuredMasks + [('raw',stringBuffer)]
                stringBuffer = ''
            elif objectEndMarker:
                print('CreateStructuredMask from objectEndMarker with content: {}'.format(stringBuffer))
                objectContent = CreateStructuredMask(stringBuffer)
                print('CreateStructuredMask from objectEndMarker with result: {}'.format(objectContent))
                structuredMasks = structuredMasks + [('object', objectContent)]
                stringBuffer = ''
            elif optionalContentEndMarker:
                structuredMasks = structuredMasks + [('optional', CreateStructuredMask(stringBuffer))]
                stringBuffer = ''
            elif constantQuestionMark:
                if stringBuffer!='':
                    structuredMasks = structuredMasks + [('raw', stringBuffer)]
                structuredMasks = structuredMasks + [('raw', '?')]
                stringBuffer = ''
            elif constantDotMark:
                if stringBuffer!='':
                    structuredMasks = structuredMasks + [('raw', stringBuffer)]
                structuredMasks = structuredMasks + [('raw', '.')]
                stringBuffer = ''
            elif alternativeOption:
                # print(">>>Alternative Option found {} for {}".format(structuredMasks, "" if len(structuredMasks) == 0 else structuredMasks[len(structuredMasks) - 1]))
                createdSubTree = CreateStructuredMask(stringBuffer)
                if len(structuredMasks) > 0 and structuredMasks[len(structuredMasks) - 1][0] == 'alternative':
                    #print(">>>Adding {} to alternative {}".format(createSubTree, structuredMasks[len(structuredMasks) - 1][1]))
                    structuredMasks[len(structuredMasks) - 1] = (structuredMasks[len(structuredMasks) - 1][0], structuredMasks[len(structuredMasks) - 1][1] + createdSubTree)
                else:
                    #print(">>>Creating with alternative")
                    structuredMasks = structuredMasks + [('alternative', createdSubTree)]
                stringBuffer = ''
            elif repeatableContentEndMarker:
                structuredMasks = structuredMasks + [('repeatable', CreateStructuredMask(stringBuffer))]
                stringBuffer = ''
        if stringBuffer != '':
            structuredMasks = structuredMasks + [('raw', stringBuffer)]
            stringBuffer = ''

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
masks = masks + [("Ist <Detail> [ein/eine/der/die/das/] <Prädikat>?", lambda library: print("Called the correct function with {}".format(library)))]
#masks = masks + [("Sind <Detail> [{,/und/ <Detail>}] und <Detail> [ein/eine/der/die/das/] <Prädikat>?", lambda library: print("Called the correct function with {}".format(library)))]
#masks = masks + [("<Detail>?", lambda library: print("Called the correct function with {}".format(library)))]
# Aussagesätze
#masks = masks + [("<Detail> ist <Prädikat>[.]", lambda library: print("Called the correct function with {}".format(library)))]
#masks = masks + [("<Detail> [{,/und/oder/ <Detail>}] sind <Prädikat>[.]", lambda library: print("Called the correct function with {}".format(library)))]
#masks = masks + [("<Detail> [{,/und/oder/ <Detail>}] sind alle <Prädikat>[.]", lambda library: print("Called the correct function with {}".format(library)))]
#masks = masks + [("<Detail> [{,/und/oder/ <Prädikat>}] sind wie <Prädikat>[.]", lambda library: print("Called the correct function with {}".format(library)))]

structured_mask = CreateStructuredMask(masks)

def IsStaticMask(singleMask):
    isStatic = True
    staticElementCounter = 0
    optionalEntries = []
    for singleElement in singleMask:
        staticElementCounter = staticElementCounter + 1
        if singleElement[0] not in ['raw', 'object', 'alternative']:
            isStatic = False
            if singleElement[0] == 'optional':
                subResult = IsStaticMask(singleElement[1])
                optionalEntries = optionalEntries + [subResult[1]] + subResult[2]
                staticElementCounter = staticElementCounter - 1
    return (isStatic, staticElementCounter, optionalEntries)

def CompareMaskEntry(maskEntry, word):
    if len(maskEntry) == 1:
        return CompareMaskEntry(maskEntry[0], word)
    print("Compare {} with {}".format(maskEntry, word))
    if maskEntry[0] == 'raw':
        if maskEntry[1] == word:
            return (True, maskEntry[0], word)
    elif maskEntry[0] == 'object':
        return (True, maskEntry[1][0][1], word)
    elif maskEntry[0] == 'alternative':
        for singleAlternative in maskEntry[1]:
            if singleAlternative[1] == word:
                return (True, singleAlternative[0], word)
    return (False, '', '')

def StaticMaskMatch(singleMask, maskLength, optionalLengthExtensions, satz, wortPosition):
    myDictionary = {}
    falseReturn = (False, {}, 0)
    print("Interpetiere Maske als statisch: {} mit {} und {} optionalen Elementen".format(singleMask, maskLength, optionalLengthExtensions))
    lengthFit = False
    minLengthFit = False
    senLength = len(satz)
    if senLength == maskLength:
        lengthFit = True
        minLengthFit = True
    else:
        for dLen in optionalLengthExtensions:
            if senLength == maskLength + dLen:
                lengthFit = True
                break
    if lengthFit:
        print("Anzahl der Elemente ist gleich, könnte die richtige Maske zum Satz sein")
        wordCounter = 0
        for singleElement in singleMask:
            if singleElement[0] == 'optional' and minLengthFit:
                continue
            res = CompareMaskEntry(singleElement, satz[wordCounter])
            if res[0]:
                print("Wort passt")
                if res[1] not in ['raw']:
                    previousEntry = [] if res[1] not in myDictionary else myDictionary[res[1]]
                    myDictionary[res[1]] = previousEntry + [satz[wordCounter]]
                wordCounter = wordCounter + 1
            else:
                return falseReturn
        print("Satz passt.")
        return (True, myDictionary, 0)
    else:
        print("Anzahl der Elemente ist nicht gleich")
        return falseReturn

def MatchToMask(singleMask, satz, wortPosition):
    isStatic = IsStaticMask(singleMask)
    staticResult = StaticMaskMatch(singleMask, isStatic[1], isStatic[2], satz, wortPosition)
    if staticResult[0]:
        return staticResult
    return (False, {}, 0)

def CompareToMask(singleMask, satz, wortPosition):
    maskFit = True
    details = []
    predicates = []
    print("Compare {} to sentence {}".format(singleMask, satz[wortPosition]))
    wortCounter = wortPosition
    maskPosition = 0
    while wortCounter < len(satz) and maskPosition < len(singleMask):
        print("Position in Prüfung: M{} - W{}".format(maskPosition, wortCounter))
        print("Content zur Prüfung: LM{} - LW{}".format(len(singleMask), len(satz)))
        print("Prüfe folgenden Abschnitt: {} gegen Wort {}".format(singleMask[maskPosition], satz[wortCounter]))
        if singleMask[maskPosition][0] == 'raw':
            if singleMask[maskPosition][1] == satz[wortCounter]:
                print("Wort passt")
                maskPosition = maskPosition + 1
            else:
                print("Wort passt nicht")
                maskFit = False
                break
        elif singleMask[maskPosition][0] == 'object':
            ergDetail = CompareToMask(singleMask[maskPosition][1], ['Detail'], 0)
            ergPredicate = CompareToMask(singleMask[maskPosition][1], ['Prädikat'], 0)
            if ergDetail[0] == True:
                details = details + [satz[wortCounter]]
                maskPosition = maskPosition + 1
            elif ergPredicate[0] == True:
                predicates = predicates + [satz[wortCounter]]
                maskPosition = maskPosition + 1
        elif singleMask[maskPosition][0] == 'optional':
            print("Optional entry found")
            ergOptional = CompareToMask(singleMask[maskPosition][1], satz, wortCounter)
            if ergOptional[0] == True:
                print("Optional entry {} filled by {}".format(singleMask[maskPosition][1], satz[wortCounter]))
                details = details + ergOptional[1]
                predicates = predicates + ergOptional[2]
                wortCounter = ergOptional[3]
                wortCounter = wortCounter - 1
            else:
                print("Optional entry not filled")
                wortCounter = wortCounter - 1
            maskPosition = maskPosition + 1
        elif singleMask[maskPosition][0] == 'alternative':
            foundHit = False
            while maskPosition < len(singleMask) and singleMask[maskPosition][0] == 'alternative':
                if foundHit == False:
                    print("Checking Alternatives: {}".format(singleMask[maskPosition][1]))
                    ergAlternative = CompareToMask(singleMask[maskPosition][1], satz, wortCounter)
                    if ergAlternative[0] == True:
                        wortCounter = ergAlternative[3]
                        wortCounter = wortCounter - 1
                        foundHit = True
                        details = details + ergAlternative[1]
                        predicates = predicates + ergAlternative[2]
                maskPosition = maskPosition + 1
            maskFit = foundHit
        elif singleMask[maskPosition][0] == 'repeatable':
            print("Going through repeatable options")
            foundHit = True
            while foundHit:
                ergRepeatable = CompareToMask(singleMask[maskPosition][1], satz, wortCounter)
                if ergRepeatable[0] == True:
                    wortCounter = ergRepeatable[3]
                    print("Repeating...")
                    details = details + ergRepeatable[1]
                    predicates = predicates + ergRepeatable[2]
                    #wortCounter = wortCounter + 1
                else:
                    print("Not repeating any more")
                    foundHit = False
                    wortCounter = wortCounter - 1
            maskPosition = maskPosition + 1
        wortCounter = wortCounter + 1
    print("Finished: {}/{}".format(maskPosition, len(singleMask)))
    if maskPosition != len(singleMask):
        maskFit = False
    return (maskFit, details, predicates, wortCounter)

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
    elif erg == 'lsm':
        value = erg.split(" ")
        print('{}'.format(structured_mask))
    elif erg.startswith('lsm '):
        splitErg = erg.split(" ")
        print('{}'.format(structured_mask[int(splitErg[1])]))
    elif erg == 'i':
        subErg = input('Bitte den Satz zur Interpretation eingeben:')
        foundMask = False
        satz = list(filter(lambda a: a != '', subErg.replace('?', ' ?').replace('.',' .').replace(',',' ,').split(" ")))
        for singleMask in structured_mask:
            compResult = CompareToMask(singleMask[1], satz, 0)
            if compResult[0]:
                print("Satz passt zur Maske: {} mit Ergebnis: {}".format(singleMask, compResult))
                singleMask[0](compResult[1], compResult[2])
                foundMask = True
                break
            if foundMask == False:
                print("Wie bitte?")
    elif erg == 's':
        subErg = input('Was gibt es?')
        foundMask = False
        satz = list(filter(lambda  a: a!='', subErg.replace('?', ' ?').replace('.', ' .').replace(',',' ,').split(" ")))
        for singleMask in structured_mask:
            compResult = MatchToMask(singleMask[1], satz, 0)
            if compResult[0]:
                print("Satz passt zur Maske: {} mit Ergebnis: {}".format(singleMask, compResult))
                singleMask[0](compResult[1])
                foundMask = True
                break
            if foundMask == False:
                print("Wie bitte?")
    elif erg == 'Hallo' or erg == 'Hallo!' or erg == 'Hi' or erg == 'Hi!':
        print('{}'.format('Hallo'))
    else:
        satz = erg.replace('?','').replace('.','').split(" ")
        satz_count = len(satz)
        # Maske: Ist <Detail> [ein/eine/der/die/das] <Prädikat>? -> Gleichsetzungfrage - Einzahl
        # Maske: Sind <Detail> und <Detail> [und ...] [ein/eine/der/die/das] <Prädikat>? -> Gleichsetzungsfrage - Mehrzahl
        # Maske: <Detail>?
        if '?' in erg:
            # Fragen
            #print('Frage erkannt')
            if satz_count >= 3:
                #print('Genug Wortteile verfügbar {}'.format(satz[0].lower()))
                if satz[0].lower() == 'ist':
                    #print('Erkenne Gleichsetzungfrage - Einzahl')
                    detail = satz[1]
                    predicate = satz[2]
                    qResult = CheckDetailsInPredicate([detail], predicate)
                    print('{}'.format(qResult))
                elif satz[0].lower() == 'sind':
                    #print('Erkenne Gleichsetzungsfrage - Mehrzahl')
                    predicate = satz[satz_count - 1]
                    details_raw = satz[1:satz_count - 1]
                    details = list(filter(lambda a: a != 'und', details_raw))
                    #print('..{}'.format(details_raw))
                    qResult = CheckDetailsInPredicate(details, predicate)
                    print('{}'.format(qResult))
                else:
                    print('Wie bitte?')
            elif satz_count == 1:
                detail = satz[0]
                qResult = GetPredicateFromDetail(detail)
                print('{}'.format(qResult))
            else:
                print('Wie bitte?')
        else:
            # Aussagesätze
            # Maske: <Detail> ist <Prädikat>[.]
            # Maske: <Detail> [{,/und/oder/ <Detail>}] sind <Prädikat>[.]
            # Maske: <Detail> [{,/und/oder/ <Detail>}] sind alle <Prädikat>[.]
            # Maske: <Prädikat> [{,/und/oder/ <Prädikat>}] sind wie <Prädikat>[.]
            if satz_count >= 3 and satz[satz_count - 2] in ['ist']:
                print('Gleichsetzungssatz erkannt')
                predicate = satz[satz_count - 1]
                details_raw = satz[:satz_count - 2]
                details = list(filter(lambda a: a != 'und', details_raw))
                print('..{}'.format(details))
                AddDetailToPredicate(details, predicate)
            elif satz_count >= 3 and satz[satz_count - 2] in ['sind']:
                print('Gleichsetzungssatz erkannt')
                predicate = satz[satz_count - 1]
                details_raw = satz[:satz_count - 2]
                details = list(filter(lambda a: a != 'und', details_raw))
                print('..{}'.format(details))
                AddDetailToPredicateGrouped(details, predicate)
            elif satz_count >= 4 and satz[satz_count - 3] in ['sind'] and satz[satz_count - 2] == 'alle':
                print('Gleichsetzungssatz erkannt')
                predicate = satz[satz_count - 1]
                details_raw = satz[:satz_count - 3]
                details = list(filter(lambda a: a != 'und', details_raw))
                print('..{}'.format(details_raw))
                AddDetailToPredicate(details, predicate)
            elif satz_count >= 3 and satz[satz_count - 3] in ['ist','sind'] and satz[satz_count - 2] == 'wie':
                print('Prädikatgleichsetzung erkannt')
                predicate = satz[satz_count - 1]
                eq_predicate_raw = satz[:satz_count - 3]
                eq_predicate = list(filter(lambda a: a != 'und', eq_predicate_raw))
                print('..{}'.format(eq_predicate))
                AddEqualsPredicate(eq_predicate, predicate)
            else:
                print('Wie bitte?')
    #print("{}".format(erg))