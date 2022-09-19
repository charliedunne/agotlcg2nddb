from db import models

import os
import json
# delete: models.Cycle.objecs.all().delete()

# Languages 
print("Running Languages:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Add the original laguage (english)
try:
    models.Language.objects.create(short='en', name='English')
    print('Saving "English" language')
except Exception as e:
    if 'UNIQUE' in str(e):
         pass
    else:          
        print("ERROR adding 'English' language")

# Manage each language translation
for lang in dirs:

    longName = ''

    if lang == 'es':
        longName = 'Spanish'

    if lang == 'de':
        longName = 'German'

    if lang == 'fr':
        longName = 'French'

    temp = models.Language(short=lang, name=longName)

    try:
        temp.save()
        print('Saving "' + longName + '" language')
    except Exception as e:
        if 'UNIQUE' in str(e):
            pass
        else:          
            print('ERROR adding "' + lang + '"')

# Cycles
print("\nRunning Cycles:")
print("..................................\n")
f = open('../throneteki-json-data/cycles.json', 'r')
data_cycles = json.load(f)
f.close()
counter = 0
packsOnCycles = []
for i in data_cycles:
    temp = models.Cycle(short=i['id'], name=i['name'])
    packsOnCycles.append(i['packs'])
    try:
        temp.save()
        print('Saving "'  + temp.name + '".')
    except Exception as e:
        if 'UNIQUE' in str(e):
            pass
        else:          
            print('Bypass "'  + temp.name + '". ERROR: ' + str(e))

    counter = counter + 1

# Cycles translation
print("\nRunning CyclesTranslation:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Manage each language translation
for lang in dirs:
    f = open(path + lang + '/cycles.json')
    translate_cycle_data = json.load(f)

    for i in translate_cycle_data:

        # Find the cycle in DB
        row = models.Cycle.objects.all().get(short=i['code'])

        # Find Language in DB
        lg = models.Language.objects.all().get(short=lang)
        
        if (row is not None) and (lg is not None):
            temp = models.TranslateCycle(cycle=row, language=lg, name=i['name'])

            # Find duplicates
            duplicates = models.TranslateCycle.objects.all().filter(cycle=row, language=lg, name=i['name'])

            if len(duplicates) == 0:
                try:
                    temp.save()
                    print('Saving "' + i['name'] + '" Cycle')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        pass
                    else:          
                        print('Bypass "'  + i['name'] + '". ERROR: ' + str(e))                

# Packs
print("\nRunning packs")
print("..................................\n")
path = "../throneteki-json-data/packs"
dirs = os.listdir(path)
for filename in dirs:
    f = open(path + '/' + filename)
    data_pack = json.load(f)
    f.close()
    
    # Find to what cycle the current packet is associated
    for cycle in data_cycles:
        if data_pack['code'] in cycle['packs']:
            # Pack found in the current cycle
            cycle_id = cycle['id']

    # Query to find the specific cycle
    row = models.Cycle.objects.all().get(short=cycle_id)

    if row is not None:
        temp = models.Pack(short=data_pack['code'], 
                            name=data_pack['name'], 
                            cycle=row)
        try:
            temp.save()            
            print('Saving "' + temp.name + '" (' + temp.short + ') for cycle "' + row.name + '".')
        except Exception as e:
            if 'UNIQUE' in str(e):
                pass
            else:              
                print('Bypassing "' + temp.name + '" (' + temp.short + ') for cycle "' + row.name + '". ERROR: ', str(e))

# Packs translation
print("\nRunning PacksTranslation:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Manage each language translation
for lang in dirs:
    f = open(path + lang + '/packs.json')
    translate_cycle_data = json.load(f)

    for i in translate_cycle_data:

        # Find the cycle in DB
        row = models.Pack.objects.all().get(short=i['code'])

        # Find Language in DB
        lg = models.Language.objects.all().get(short=lang)
        
        if (row is not None) and (lg is not None):
            temp = models.TranslatePack(pack=row, language=lg, name=i['name'])

            # Find duplicates
            duplicates = models.TranslatePack.objects.all().filter(pack=row, language=lg, name=i['name'])

            if len(duplicates) == 0:
                try:
                    temp.save()
                    print('Saving "' + i['name'] + '" Pack')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        pass
                    else:          
                        print('Bypass "'  + i['name'] + '". ERROR: ' + str(e))  


# Factions
print("\nRunning factions")
print("..................................\n")
path = "../throneteki-json-data/packs"
dirs = os.listdir(path)

# Faction's array
factions = []

# Obtain the faction's list
for filename in dirs:
    f = open(path + '/' + filename)
    data_pack = json.load(f)
    f.close()
    # Create array of factions
    for card in data_pack['cards']:
        if card['faction'] not in factions:
            factions.append(card['faction'])

# Save data into DB
for faction in factions:

    if faction == 'thenightswatch':
        temp = models.Faction(short=faction, name="The Night's Watch")
    else:
        temp = models.Faction(short=faction, name=faction.capitalize())
    
    try:
        temp.save()            
        print('Saving "' + temp.name + '" (' + temp.short + ').')
    except Exception as e:
        if 'UNIQUE' in str(e):
            pass
        else:        
            print('Bypassing "' + temp.name + '" (' + temp.short + '). ERROR: ' + str(e))


# Faction translation
print("\nRunning FactionTranslation:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Manage each language translation
for lang in dirs:
    f = open(path + lang + '/factions.json')
    translate_cycle_data = json.load(f)

    for i in translate_cycle_data:

        # Find the cycle in DB
        row = models.Faction.objects.all().get(short=i['code'])

        # Find Language in DB
        lg = models.Language.objects.all().get(short=lang)
        
        if (row is not None) and (lg is not None):
            temp = models.TranslateFaction(faction=row, language=lg, name=i['name'])

            # Find duplicates
            duplicates = models.TranslateFaction.objects.all().filter(faction=row, language=lg, name=i['name'])

            if len(duplicates) == 0:            
                try:
                    temp.save()
                    print('Saving "' + i['name'] + '" faction')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        pass
                    else:          
                        print('Bypass "'  + i['name'] + '". ERROR: ' + str(e))  

# Traits
print("\nRunning traits")
print("..................................\n")
path = "../throneteki-json-data/packs"
dirs = os.listdir(path)

# Faction's array
traits = []

# Obtain the faction's list
for filename in dirs:
    f = open(path + '/' + filename)
    data_pack = json.load(f)
    f.close()
    # Create array of factions
    for card in data_pack['cards']:
        for trait in card['traits']:
             if trait not in traits:
                traits.append(trait)

# Save data into DB
for trait in traits:
    temp = models.Trait(name=trait)
    try:
        temp.save()            
        print('Saving "' + temp.name + '".')
    except Exception as e:
        if 'UNIQUE' in str(e):
            pass
        else:        
            print('Bypassing "' + temp.name + '". ERROR: ' + str(e))

# Types
print("\nRunning types")
print("..................................\n")
path = "../throneteki-json-data/packs"
dirs = os.listdir(path)

# Faction's array
types = []

# Obtain the faction's list
for filename in dirs:
    f = open(path + '/' + filename)
    data_pack = json.load(f)
    f.close()
    # Create array of factions
    for card in data_pack['cards']:
        if card['type'] not in types:
                types.append(card['type'])

# Save data into DB
for type in types:
    temp = models.Type(name=type.capitalize())
    try:
        temp.save()            
        print('Saving "' + temp.name + '".')
    except Exception as e:
        if 'UNIQUE' in str(e):
            pass
        else:
            print('Bypassing "' + temp.name + '". ERROR:' + str(e))        

# Cards
print("\nRunning cards")
print("..................................\n")
path = "../throneteki-json-data/packs"
dirs = os.listdir(path)

# Faction's array
types = []

# Obtain the faction's list
for filename in dirs:
    f = open(path + '/' + filename)
    data_pack = json.load(f)
    f.close()

    # Save data into DB
    for card in data_pack['cards']:

        # Constants        
        cUnique = card['unique'] if 'unique' in card else False
        cCost = card['cost'] if 'cost' in card else None
        cMilitary = card['icons']['military'] if 'icons' in card else None
        cIntrigue = card['icons']['intrigue'] if 'icons' in card else None
        cPower = card['icons']['power'] if 'icons' in card else None
        cLoyal = True if 'loyal' in card else False
        cStrenght = card['strength'] if 'strength' in card else None
        cText = card['text'] if 'text' in card else None
        cFlavor = card['flavor'] if 'flavor' in card else None
        cIllustrator = card['illustrator'] if 'illustrator' in card else None
        cDeckLimit = card['deckLimit'] if 'deckLimit' in card else None
        cIncome = card['plotStats']['income'] if 'plotStats' in card else None
        cInitiative = card['plotStats']['initiative'] if 'plotStats' in card else None
        cClaim = card['plotStats']['claim'] if 'plotStats' in card else None
        cReserve = card['plotStats']['reserve'] if 'plotStats' in card else None

        # References to other Tables
        rTypeId = models.Type.objects.all().get(name=card['type'].capitalize())
        rFactionId = models.Faction.objects.all().get(short=card['faction'])

        temp = models.Card(
            code=card['code'],
            type=rTypeId,
            name=card['name'],
            quantity=card['quantity'],
            unique=cUnique,
            faction=rFactionId,
            loyal=cLoyal,
            cost=cCost,
            iMilitary=cMilitary,
            iIntrigue=cIntrigue,
            iPower=cPower,
            strenght=cStrenght,
            illustrator=cIllustrator,
            decklimit=cDeckLimit,
            text=cText,
            flavor=cFlavor,
            pIncome=cIncome,
            pInitiative=cInitiative,
            pClaim=cClaim,
            pReserve=cReserve)

        try:
            temp.save()

            if 'traits' in card:
                for trait in card['traits']:
                    tempTrait = models.Trait.objects.all().get(name=trait)
                    temp.traits.add(tempTrait)            
        
            print('Saving [' + temp.code + "]' " + temp.name + '".')
        except Exception as e:
            if 'UNIQUE' in str(e):
                pass
            else:
                print('ERROR [' + temp.code + "]'" + temp.name + '". ' + str(e))

 

# Traits translation
print("\nRunning TraitsTranslation:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Manage each language translation
for lang in dirs:
#for lang in ['es']:
    dirPacks = os.listdir(path + lang + '/pack/')

    # Find Language in DB
    lg = models.Language.objects.all().get(short=lang)

    for pack in dirPacks:
        f = open(path + lang + '/pack/' + pack)
        translate_pack_data = json.load(f)

        for i in translate_pack_data:
            
            # Extract the traits from the translation
            traits = list(filter(None, i['traits'].split('.')))

            # Find the same traits in DB
            orTraits = models.Card.objects.get(code=i['code']).traits.all()

            
            if len(orTraits) == 1:
                # print(traits[0].lstrip() + "=> " + orTraits[0].name)

                # Trait object (many2many relationship)
                row = models.Trait.objects.get(name=orTraits[0].name)

                # Row to be inserted in DB (if no duplicates already)
                temp = models.TranslateTrait(trait=row, language=lg, name=traits[0].lstrip())

                # Find duplicates
                duplicates = models.TranslateTrait.objects.all().filter(trait=row, language=lg, name=traits[0].lstrip())

                if len(duplicates) == 0:
                    try:
                        temp.save()
                        print('Saving "' + orTraits[0].name + '" => "' +  traits[0].lstrip() + '" Trait')
                    except Exception as e:
                        if 'UNIQUE' in str(e):
                            pass
                        else:          
                            print('Bypass "'  + orTraits[0].name + '" => "' +   traits[0].lstrip() + '". ERROR: ' + str(e))  


# Cards translation
print("\nRunning CardsTranslation:")
print("..................................\n")
path = "../translations-json-data/translations/"
dirs = os.listdir(path)

# Manage each language translation
for lang in dirs:
#for lang in ['es']:
    dirPacks = os.listdir(path + lang + '/pack/')

    # Find Language in DB
    lg = models.Language.objects.all().get(short=lang)

    for pack in dirPacks:
        f = open(path + lang + '/pack/' + pack)
        translate_pack_data = json.load(f)

        for card in translate_pack_data:
            
            # Card object 
            row = models.Card.objects.get(code=card['code'])

            # Row to be inserted in DB (if no duplicates already)
            temp = models.TranslateCard(card=row, language=lg, name=card['name'], text=card['text'], flavor=card['flavor'])

            # Find duplicates
            duplicates = models.TranslateCard.objects.all().filter(card=row, language=lg, name=card['name'])

            if len(duplicates) == 0:
                try:
                    temp.save()
                    print('Saving "' + card['name'] + '" Card')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        pass
                    else:          
                        print('Bypass "'  + card['name'] + '" Card. ERROR: ' + str(e))  
