# Importeer de benodigde bibliotheken
import pandas as pd
import os
# Functie om het CSV-bestand te lezen
def lees_csv(bestandspad):
    try:
        return pd.read_csv(bestandspad)
    except FileNotFoundError:
        print("Bestand niet gevonden. Controleer het pad.")
        exit()

# Functie om unieke groepen te filteren op basis van een bepaald type
def filter_groepen(unieke_groepen, type_groep):
    return sorted([group for group in unieke_groepen if type_groep in group])

# Functie om het aantal leerlingen per groep te tellen
def tel_leerlingen(file, groepen):
    totaal_aantal = 0
    for groep in groepen:
        leerlingen_in_groep = file[file['klasgroep'] == groep]
        aantal_leerlingen = len(leerlingen_in_groep)
        totaal_aantal += aantal_leerlingen
        print(f"{groep} heeft {aantal_leerlingen} leerlingen")
    return totaal_aantal
# Functie om de gebruiker een keuze te laten maken tussen "lijst" en "groepen"
def keuze_f():
    while True:  # Blijf vragen totdat een geldige keuze is gemaakt
        keuze = input("Maak een keuze tussen 'lijst' of 'groepen': ").strip().lower()  # Invoer van de gebruiker
        if keuze in ['lijst', 'groepen']:  # Controleer of de invoer correct is
            return keuze  # Als correct, geef de keuze terug
        else:
            print("Ongeldige keuze. Kies 'lijst' of 'groepen'.")  
def groote_groep(llt):
    while True:  # Blijf vragen totdat een geldige invoer is gegeven
        try:
            groepsgrootte = int(input("Hoe groot zijn de groepjes: "))
            if groepsgrootte > llt:
                print("De groepsgrootte kan niet groter zijn dan het totale aantal leerlingen.")  # Foutmelding
                continue  # Vraag opnieuw om invoer
            return groepsgrootte  # Geef de geldige invoer terug
        except ValueError:
            print("Geef een nummer als waarde")  # Foutmelding als de invoer geen nummer is
            
def lees_groepsnamen(bestandspad_2):
    try:
        with open(bestandspad_2, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("Groepsnamen bestand niet gevonden. Controleer het pad.")
        exit()

# Functie om willekeurige groepjes studenten te maken op basis van de gebruikerskeuze
def maak_groepjes(file, groepsgrootte,groepsnamen,script_dir):
    
    bestandsnaam = os.path.join(script_dir, "samengestelde_groepjes.txt")
    
    # Vraag de gebruiker om de keuze van groepssamenstelling
    print("Kies een optie voor groepssamenstelling:")
    print("1. Willekeurige studenten uit MCT én CTAI")
    print("2. Willekeurige studenten van enkel MCT")
    print("3. Willekeurige studenten van enkel CTAI")
    print("4. Willekeurige studenten van 1 klasgroep (bv 1MCT3)")
    print("5. Willekeurige studenten van verschillende klasgroepen (bv 1MCT3 én 1MCT4 én 1CTAI2)")

    keuze = input("Voer de nummer van uw keuze in (1-5): ")

    if keuze == '1':
        groepen_t = file.sample(frac=1).reset_index(drop=True)  # Schud alle leerlingen
    elif keuze == '2':
        groepen_t = file[file['klasgroep'].str.contains('MCT')].sample(frac=1).reset_index(drop=True)  # MCT leerlingen
    elif keuze == '3':
        groepen_t = file[file['klasgroep'].str.contains('CTAI')].sample(frac=1).reset_index(drop=True)  # CTAI leerlingen
    elif keuze == '4':
        klasgroep = input("Voer de klasgroep in (bv 1MCT3): ")
        groepen_t = file[file['klasgroep'] == klasgroep].sample(frac=1).reset_index(drop=True)  # Specifieke klasgroep
    elif keuze == '5':
        klasgroepen_input = input("Voer de klasgroepen in gescheiden door een komma (bv 1MCT3,1MCT4,1CTAI2): ")
        klasgroepen = [group.strip() for group in klasgroepen_input.split(',')]
        groepen_t = file[file['klasgroep'].isin(klasgroepen)].sample(frac=1).reset_index(drop=True)  # Meerdere klasgroepen
    else:
        print("Ongeldige keuze.")
        return

    # Genereer en print de groepen
    aantal_groepen = len(groepen_t) // groepsgrootte
    groepjes = []
    gebruikte_groepsnamen = set()

    for i in range(aantal_groepen):
        groep = groepen_t.iloc[i * groepsgrootte:(i + 1) * groepsgrootte]  # Creëer groepen
        groepjes.append(groep[['voornaam', 'klasgroep']].values.tolist())  # Voeg de voornamen en klasgroep toe aan de groep
        groepsnaam = groepsnamen[i] if i < len(groepsnamen) else f"Groep {i + 1}"
        gebruikte_groepsnamen.add(groepsnaam)  # Houd de gebruikte groepsnamen bij
        print(f"{groepsnaam}:")
        print("{:<20} {:<10}".format("Naam", "Klasgroep"))  # Tabelkop
        for naam, klasgroep in groep[['voornaam', 'klasgroep']].values:
            print("{:<20} {:<10}".format(naam, klasgroep))  # Namen en klasgroep in tabelformaat
        print()

    # Controleer of er nog leerlingen over zijn
    if len(groepen_t) % groepsgrootte != 0:
        groep = groepen_t.iloc[aantal_groepen * groepsgrootte:]
        groepjes.append(groep[['voornaam', 'klasgroep']].values.tolist())
        groepsnaam = groepsnamen[aantal_groepen] if aantal_groepen < len(groepsnamen) else f"Groep {aantal_groepen + 1}"
        gebruikte_groepsnamen.add(groepsnaam)
        print(f"{groepsnaam}: (deze groep is kleiner dan {groepsgrootte})")
        print("{:<20} {:<10}".format("Naam", "Klasgroep"))  # Tabelkop
        for naam, klasgroep in groep[['voornaam', 'klasgroep']].values:
            print("{:<20} {:<10}".format(naam, klasgroep))
        print()


    # Schrijf de groepen naar een tekstbestand
    with open(bestandsnaam, 'w') as bestand:
        for i, groep in enumerate(groepjes):
            groepsnaam = groepsnamen[i] if i < len(groepsnamen) else f"Groep {i + 1}"
            bestand.write(f"{groepsnaam}:\n")
            bestand.write("{:<20} {:<10}\n".format("Naam", "Klasgroep"))  # Schrijf kop naar bestand
            for naam, klasgroep in groep:
                bestand.write("{:<20} {:<10}\n".format(naam, klasgroep))  # Namen en klasgroep naar bestand schrijven
            bestand.write("\n")

    print(f"De samengestelde groepjes zijn weggeschreven naar {bestandsnaam}.")
       


        


# Hoofdfunctie
def main():
    # Dynamisch pad naar de huidige scriptlocatie
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Bestandslocatie
    bestandspad = os.path.join(script_dir, "klasgroepen.csv")
    bestandspad_2 = os.path.join(script_dir, "groepsnamen.txt")
    
    
    # Lees het CSV-bestand
    file = lees_csv(bestandspad)
    
    # Lees de groepsnamen uit het tekstbestand
    groepsnamen = lees_groepsnamen(bestandspad_2)
    
    # Verkrijg unieke groepen
    unieke_groepen = file['klasgroep'].unique()
    print(f"Er zijn in totaal {len(unieke_groepen)} klasgroepen, namelijk:")
    
    # Vraag de gebruiker om een keuze te maken
    keuze = keuze_f()
    
    if keuze == "lijst":
       # Filter MCT en CTAI groepen
       mct_groepen = filter_groepen(unieke_groepen, 'MCT')
       ctai_groepen = filter_groepen(unieke_groepen, 'CTAI')

       # Tel het aantal leerlingen in de groepen
       t_aantal_mct = tel_leerlingen(file, mct_groepen)
       t_aantal_ctai = tel_leerlingen(file, ctai_groepen)

       # Print totaal aantal leerlingen
       print(f"Totaal aantal MCT leerlingen: {t_aantal_mct}")
       print(f"Totaal aantal CTAI leerlingen: {t_aantal_ctai}")
       input("Druk op Enter om af te sluiten...")
    
    elif keuze == "groepen":
        llt = len(file)  # Telt het totale aantal rijen (leerlingen)
        print(f"Er zijn in totaal {llt} leerlingen.")
        groepsgrootte = groote_groep(llt)  # Sla de groepsgrootte op
        rest = llt % groepsgrootte
        deling = llt  // groepsgrootte
        print(f"Er zijn {deling} volledige groepen mogelijk met {rest} als rest")
        maak_groepjes(file, groepsgrootte, groepsnamen,script_dir)  # Voeg groepsnamen toe
        input("Druk op Enter om af te sluiten...")


# Start het programma
main()