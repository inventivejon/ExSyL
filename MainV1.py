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
    global predicates
    retVal = ''
    for predicate in predicates:
        #print("Prüfe Inhalt {} von {}".format(predicates[predicate], predicate))
        if detail in predicates[predicate]:
            retVal = predicate if retVal == '' else retVal + ' und ' + predicate
        for subpredicate in predicates[predicate]:
            if detail in subpredicate and type(subpredicate) is not str:
                retVal = predicate if retVal == '' else retVal + ' und ' + predicate
    return retVal

def CreateStructuredMask(rawMask):
    structuredMasks = []

    # print('Call CreateStructuredMask with \'{}\''.format(rawMask))

    if type(rawMask) != str:
        for mask in rawMask:
            # print('Call CreateStructuredMask for \'{}\''.format(mask))
            structuredMasks = structuredMasks + [CreateStructuredMask(mask)]
    else:
        print('Processing string \'{}\''.format(rawMask))
        objectTemplateCounter = 0
        optionalContentCounter = 0
        repeatableContentCounter = 0
        stringBuffer = ''
        for singleCharacter in rawMask:
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
                structuredMasks = structuredMasks + [('alternative', CreateStructuredMask(stringBuffer))]
                stringBuffer = ''
            elif repeatableContentEndMarker:
                structuredMasks = structuredMasks + [('repeatable', CreateStructuredMask(stringBuffer))]
                stringBuffer = ''
        if stringBuffer != '':
            structuredMasks = structuredMasks + [('raw', stringBuffer)]
            stringBuffer = ''
    return structuredMasks

# Syntax
# <Keyword> Object (z.B. <Detail>)
# [] Optional (z.B. [ein]) 
# / alternativ (muss auch ans Ende der Alternative z.B. ein/eine/einer/)
# {} Kann sich beliebig oft wiederholen (z.B. {})

masks = []
# Fragesätze
masks = masks + ["Ist <Detail> [ein/eine/der/die/das/] <Prädikat>?"]
masks = masks + ["Sind <Detail> [{,/und/ <Detail>}] [ein/eine/der/die/das/] <Prädikat>?"]
masks = masks + ["<Detail>?"]
# Aussagesätze


structured_mask = CreateStructuredMask(masks)

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