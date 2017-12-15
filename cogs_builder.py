#!/usr/bin/python

from collections import Counter
import os

"""
De functie opent de opgegeven filenaam, wat als een parameter meegegeven wordt,
en keert alle zinnen als een lijst terug. Ze zijn gesprlitst op een enter.
De functie gebruikt de volgende parameters:
    * of_file   bestand van interesse dat geopend moet worden. 
"""
def OpenFile(of_file):
    with open(of_file,'r') as f:
        return f.readlines()

"""
De functie kijkt of de opgegeven waarde (if_kans) in de lijst (if_lijst)
voorkomt. Als datwaar is dat wordt de waarde "true teruggegeven, zoniet dat
wordt de waarde "False" teruggegeven.
De functie gebruikt de volgende parameters (op volgorde):
    * if_kans   mogelijke combinatie van tekens.
    * if_lijst  lijst waar er in gezocht moet worden.
"""
def IndexFind(if_kans, if_lijst):
    try:
        if_lijst.index(if_kans)
        return True
    except ValueError:
        return False

"""
De functie doorloopt de lijst, twogdeellijst (dat teruggeleverd wordt door
de functie OpenFile) en zorgt ervoor dat elke mogelijke combinatie maar 1 maal
voorkomt. Dit is nodig omdat er soms bij de blastresultaten meerdere malen voor
kan komen dat een bepaalde beste hit voor kan komen. Alle mogelijke combinaties
worden dan als een lijst teruggekeerd.
De functie gebruikt de volgende parameters (op volgorde):
    * br_naam1  organisme naam van het eerste deel
    * br_naam2  organisme naam van het tweede deel
    * br_pos1   positie
    * br_pos2   positie
de posities kunnen alleen of 0 of 1 zijn. Als br_pos1 een 1 heeft, dan moet
br_pos2 de 0 hebben!
De functie keert het volgende terug:
    * singles.keys()    lijst van alle mogelijke combinaties   
"""
def BlastResults(br_naam1, br_naam2, br_pos1, tbr_pos2):
    singles = {}
    twogdeellijst = OpenFile(br_naam1+br_naam2)
    for zin in twogdeellijst:             
        singles[(zin.split()[br_pos1] + " " + zin.split()[br_pos2])] = 0
    return singles.keys()

"""
De functie zorgt ervoor dat in de file genaamd Twogs nieuwe twogcombinaties
bijgevoegd kunnen worden. De combinatie worden erkregen door een in een lege
lijst de mogelijke combinaties toe te voegen. De combinaties worden verkregen
door de functie Blastresult. als de lijst gevuld wordt, zullen het aantal
mogelijke combinaties geteld worden. Als de combinatie >= 2 dan wordt de
combinatie in de twoglijst gevuld.
Hierna wordt de file afgesloten.
De functie gebruikt de volgende parameters (op volgorde):
    * snt_naam1     organisme naam van het eerste deel
    * snt_naam1     organisme naam van het tweede deel
"""
def SchrijfNaarTwog(snt_naam1, snc_naam2):
    snt_twogfile = open("Twogs", "a")
    snt_lijst = []
    snt_lijst.extend(BlastResults(snt_naam1, snc_naam2, 0, 1))
    snt_lijst.extend(BlastResults(snc_naam2, snt_naam1, 1, 0))
    tellijst = Counter(snt_lijst)
    for keys in tellijst:
        if tellijst[keys] >= 2:
            snt_twogfile.write("%s\n"%(keys))
    snt_twogfile.close()

"""
De functie zorgt ervoor dat in de file genaamd cogs.txt nieuwe eiwitten met hun
cognummerscogs toegevoegd kunnen worden
Hierna wordt de file afgesloten.
De functie gebruikt de volgende parameters:
    * vtav_lijst    Lijst van alle mogelijke eiwitten en hun cognummers.
"""
def VoegToeAanCog(vtav_lijst):
    cogfile = open("cogs.txt","a")
    for zin in vtav_lijst:
        cogfile.write(zin)
    cogfile.close()

"""
de functie schrijft naar de file Twogs. Hij nneemt alle posities in de lijst
en schrijft ze naar de file. Daarna wordt de file afgesloten.
De functie gebruikt de volgende parameters :
    * ntf_twogs   lijst van twogs
"""    
def NewTwogFile(ntf_twogs):
    outfile = open("Twogs", "w")
    for x in ntf_twogs:
        outfile.write("%s\n"%(x))
    outfile.close()

"""
De functies zorgt ervoor dat van de twogslijst alle mogelijke combinaties
verwijderd worden.
De functie gebruikt de volgende parameters (op volgorde):
    * tr_twoglijst  lijst van mogelijke twogs die verwijderd moeten worden.
    * tr_twogs      lijst van alle twog combinatie.
"""
def TwogRemove(tr_twoglijst, tr_twogs):
    for b in tr_twoglijst:
        tr_twogs.remove(b)

"""
De functie zorgt ervoor dat er in een lijst gezocht wordt.
De functie gebruikt de volgende parameters (op volgorde):
    * zil_waarde    waarde wat aanwezig moet zijn in de lijst.
    * zil_lijst     lijst wat gezocht moet worden.
    * zil_switch    de mogelijkheid om een bepaalde lijst te doorzoeken.
De functie keert het volgende terug:
    * de lijsten van interresse
"""
def ZoekInLijst(zil_waarde, zil_lijst, zil_switch):
    if zil_switch == 0:
        return [x for x in zil_lijst if zil_waarde in x]
    elif zil_switch == 1:
        return [x.split()[0] for x in zil_lijst if zil_waarde in x]
    elif zil_switch == 2:
        return [x.split()[1] for x in zil_lijst if zil_waarde in x]
    
"""
De functie update een bestaande cog. Als er een eiwit gevonden wordt dat bij
een bepaalde cogs hoort, wordt in de twoglijst naar alle mogelijke combinaties
gezocht en worden ze (alle combinaties die bij de desbetreffende cog hoort)
verwijderd uit de twoglijst. Tevens wordt dan ook de eiwit uit de protlijst
verwijderd. 
De functie heeft 3 verschillende parameters nodig (op volgorde):
    * cogs      coglijst
    * twogs     twoglijst
    * prots     protlijst
"""
def CogUpdate(cogs, twogs, prots):
    cu_in_lijst_toevoegen = [] 
    for x in list(set([y.split()[0] for y in cogs])): 
        cu_gevondencog =  ZoekInLijst(x, cogs, 2)
        cu_lijstje = []
        nogteverwijderen = [] 
        for y in cu_gevondencog:
            cu_lijstje.extend( ZoekInLijst(y, twogs, 2))
            nogteverwijderen.extend(ZoekInLijst(y, twogs, 0))
        if len(Counter(cu_lijstje)) != 0 :
            max_prot = KeyWithMaxVal(dict(Counter(cu_lijstje)))
            cu_in_lijst_toevoegen.append("%s\t%s\n"%(x, max_prot))
            prots.remove(max_prot)
            nogteverwijderen.extend(ZoekInLijst(max_prot, twogs, 0))
            newlijst =  list(set(nogteverwijderen))
            TwogRemove(newlijst, twogs)
    VoegToeAanCog(cu_in_lijst_toevoegen)

"""
De functie doorzoekt de twoglijst en vindt alle mogelijke combinaties van de
eiwitten in de kleine lijst (prot_in_twogs). De combinaties worden allemaal
opgeslagen in de lokale variabel genaamd:
    vt_lijst
De functie heeft 3 parameters:
    * prot              het eiwit van interresse
    * twogs             de twoglijst
    * prot_in_twogs     de lijst van de nodige eiwitten
De functie keert het volgende terug:
    * vt_lijst      lijst van interresse 
"""
def VerbrogenTwogs(prot, twogs, prot_in_twogs):
    vt_lijst = []
    for x in prot_in_twogs:
        for y in prot_in_twogs:
            if IndexFind("%s %s"%(x,y), twogs):
                vt_lijst.append("%s %s"%(x,y))
                vt_lijst.append("%s %s"%(x,prot))
                vt_lijst.append("%s %s"%(y, prot))
    return vt_lijst

"""
De functie maakt een nieuwe cog aan. De functie zorgt ervoor dat als eerste
het hoogste bekende cognummer opgehaald wordt door de functie
"VindHoogsteCogNummer".
De functie doorloopt de eiwttenlijst en zoekt in de twoglijst naar alle
mogelijke combinatie behorend bij het eiwit. Waarna de functie "VerbrogenTwogs"
aangeroepen wordt. het resultaat wordt in de variabele posible_found_twogs
gezet. als deze variabele niet leeg is dan worden alle eiwitten in een nieuwe
variabele lijst (newcog) gestopt. Hier wordt per eiwit in de lijst dezelfde
cognummer toegekend. Alle mogelijke combinatie van twogs dat nog aanwezig is
in de twoglijst wordt ook meteen verwijderd.
Als laatste wordt de lijst met de nieuwe cognummer aan de cogfile toegevoegd.
Dit gebeurt door middel van de functie "VoegToeAanCog".
De functie heeft 3 verschillende parameters nodig (op volgorde):
    * ncf_cogs      coglijst
    * ncf_twogs     twoglijst
    * ncf_prots     protlijst
"""
def NewCogFind(ncf_cogs, ncf_twogs, ncf_prots):
    coglijst_hoogste_waarde = list(set([y.split()[0] for y in ncf_cogs]))
    werkgetal = VindHoogsteCogNummer(coglijst_hoogste_waarde)
    ncf_list = []
    for prot in ncf_prots:
        prot_in_twogs = ZoekInLijst(prot, ncf_twogs, 1)
        posible_found_twogs = VerbrogenTwogs(prot, ncf_twogs, prot_in_twogs)
        if posible_found_twogs != []:
            newcog = list(set(" ".join(posible_found_twogs).split()))
            werkgetal += 1 
            for incog in newcog:
                cogzin = "%s\t%s\n"%(("0000000000%s"%(werkgetal))[-8:], incog)
                ncf_list.append(cogzin)
                TwogRemove(ZoekInLijst(incog, ncf_twogs, 0), ncf_twogs)
    VoegToeAanCog(ncf_list)

 
"""
de functie keert het hoogste cognummer. Bestaat het nummer niet dan zal de
waarde 0 teruggegeven worden.
De functie gebruikt de volgende parameters :
    * vhcn_lijst   lijst waar er in gezocht moet worden.
De functie keert een getal terug

"""
def VindHoogsteCogNummer(vhcn_lijst):
    try:
        return int(max(vhcn_lijst)[0])        
    except IOError:
        return 0
    except IndexError:
        return 0
    except ValueError:
        return 0

"""
de functie keert de key van een dictionary waarbij de waarde de maximale waarde
heeft.
De functie gebruikt de volgende parameters :
    * kwmv_dict   dictionairy waar erin gezocht wordt
De functie keert key terug waarbij de value een hoogste maximale waarde heeft

"""    
def KeyWithMaxVal(kwmv_dict):
     values = list(kwmv_dict.values())
     keys = list(kwmv_dict.keys())
     return keys[values.index(max(values))]

"""
De functie doorzoekt:
    de protlijst, van de fastafile worden alleen de regels
waar een ">" in voorkomt gepakt.
    de twoglijst
    de coglijst
De functie gebruikt de volgende parameters :
    * onf_org   organismenaam
de functie keert (op volgorde) de volgende 3 lijsten terug:
    * protlijst
    * twoglijst
    * coglijst
"""
def OpenNeededFiles(onf_org):
    protlijst = [y[1:-1] for y in OpenFile("%s.fa"%(onf_org)) if ">" in y]
    twoglijst = [y[:-1] for y in OpenFile("Twogs")]
    coglijst = [y[:-1] for y in OpenFile("cogs.txt")]
    return protlijst, twoglijst, coglijst

"""
De functie doorzoekt in de cogs en in de twogs of de bestaande cogs geupdate
moeten worden of dat er nieuwe cogs moeten onstaan. tevens zorgt het ervoor
dat de twogfile geheel vernieuwe wordt.
De functie gebruikt de volgende parameters (op volgorde):
    * sfc_cogs      coglijst
    * sfc_twogs     twoglijst
    * sfc_prots     protlijst
"""
def SearchForCog(sfc_cogs, sfc_twogs, sfc_prots):
    CogUpdate(sfc_cogs, sfc_twogs, sfc_prots)
    NewCogFind(sfc_cogs, sfc_twogs, sfc_prots)
    NewTwogFile(sfc_twogs)

"""
de functie zorgt ervoor dat de cogs gemaakt worden van de bijgeleverde files.
Voor elk nieuwe organisme wordt de naam van het organisme geprint
Let op: bestaande files zoals de twogs en de cogs.txt zullen verwijderd worden!
"""
def Voorbeeld():
    os.system("rm Twogs cogs.txt")
    os.system("touch Twogs cogs.txt")
    orgslijst = [y[:-1] for y in OpenFile("orglijst") if "\n" in y]
    for x in range(len(orgslijst)):
        org1 = orgslijst[x]
        for y in range(len(orgslijst)):
            org2 = orgslijst[y]
            if x > y:
                SchrijfNaarTwog(org1, org2)
        print org1
        prots, twogs, cogs = OpenNeededFiles(org1)
        if x >= 2:
            SearchForCog(cogs, twogs, prots)

    

if __name__ == '__main__':
    Voorbeeld()

