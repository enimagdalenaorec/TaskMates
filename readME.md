# TaskMates

## Opis projekta

Ovaj projekt rezultat je timskog rada razvijenog u sklopu projektnog zadatka kolegija [Programsko inženjerstvo](https://www.fer.unizg.hr/predmet/proinz) na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu.

TaskMates je web aplikacija koja korisnicima omogućuje organizaciju i praćenje kućanskih poslova unutar zajednica poput cimerstva, obitelji ili prijateljskih grupa. Aplikacija omogućuje kreiranje grupa, dodavanje zadataka, definiranje težine i rokova te praćenje izvršavanja zadataka putem Leaderboarda i raznih statistika.

 
## **Pokretanje frontenda (Angulara)**
- Prvo pokretanje:
    1. Ukoliko nemate instaliran Angular treba ga globalno instalirati s naredbom: npm install -g @angular/cli
    2. U folderu gdje je frontend (task-mates) izvrsiti naredbu: npm install  (kako biste u folder povukli sve potrebne pakete iz node modules)
    3. U folderu gdje je frontend (task-mates) izvrsiti naredbu: ng serve
    4. Otvorit adresu u browseru (vjerojatno localhost:4200)
- Svako sljedeće pokretanje:
    1. U folderu gdje je frontend (task-mates) izvrsiti naredbu: ng serve
    2. Otvorit adresu u browseru (vjerojatno localhost:4200)

## **Pokretanje Django projekta za VSC**

Potrebno:
    Python 3.x.x (najnovija verzija je 3.13.0, ali bi i starije verzije trebale biti ok)
    Visual Studio Code
     
Postupak prije 1. pokretanja:
    
 Ako ExecutionPolicy nije RemoteSigned (to se može pogledati u poweshellu sa komandom Get-ExecutionPolicy)  potrebno ga postaviti sa
          Set-ExecutionPolicy RemoteSigned
 (Powershell je potrebno runnati kao admin)

Nakon toga potrebno instalirati virtual environment preko powershella:
     pip install virtualenv (ako imate pip u PATH-u) 
      ili
     py -m pip install virtualenv
 (ako ne radi instalirajte noviju verziju pythona)

Postupak pri pokretanju:

 1. U VSC-u otvorite folder Backend

 2. U terminalu VSC-a u direktoriju Backend runnate komandu py -m venv myenv
    To će stvoriti virtualno okruženje

 3. Onda runnate kommandu
     myenv/Scripts/Activate
   Sada bi trebali biti u virtualnom okruženju (prije direktorija u terminalu će pisati (myenv) zelenim slovima)

 4. Zatim runnate pip install -r requirements.txt
   Ovo će instalirati sve pakete koji se koriste za backend, uključujući i django

Za pokrenuti django server potrebno je runnati komandu 
  py manage.py runserver
Sa Ctrl+C se gasi server
## Upute pri pushanju na github:
 prije pushanja potrebno runnati pip freeze > requirements.txt, myenv folder se ne uploada na github.

## Značajke

- **Upravljanje grupama**: Kreirajte grupe (npr. "Cimerstvo" ili "Obitelj") i pozovite članove putem koda ili linka za pridruživanje.
- **Dodjela zadataka**: Dodajte zadatke s definiranom težinom (1-5), vremenskim rokom, optimalnom količinom ljudi potrebnih za zadatak te mu dodjelite simbol koji će kasnije biti vidljiv u kalendaru.
- **Leaderboard i Gamifikacija**:
  - Leaderboard rangira korisnike prema bodovima skupljenim izvršavanjem zadataka.
  - Bedževi i razine za postizanje određenih ciljeva.
- **Praćenje zadataka**: Pratite status zadataka (npr. "Active", "Inactive", "In progress") i pratite napredak.
- **ChatBot**: Personalizirani ChatBot koji pomaže korisnicima u korištenju aplikacije i odgovara na pitanja.

## Načini rada

1. **Gost način rada**:
   - Gosti mogu vidjeti osnovne funkcionalnosti aplikacije i komunicirati s ChatBotom.
   - Za aktivno sudjelovanje potrebno je kreirati korisnički račun.

2. **Korisnički način rada**:
   - **Registracija i prijava**: Prijava putem emaila i lozinke.
   - **Kreiranje i pridruživanje grupama**: Kreirajte grupe i pozovite druge putem koda ili linka.
   - **Praćenje zadataka**: Vidite listu članova, pregledajte aktivne zadatke i statistike.
   - **Profil korisnika**: Pregled aktivnih zadataka, bodova i osobnih statistika. Sadrži kalendar s rokovima zadataka.
   - **Grupni razgovor:** Zajednički razgovor kojeg dijeli jedna grupa kako bi lakše komunicirali.

3. **Admin način rada**:
   - **Administratori**: Upravljanje grupama, brisanje grupa, i dodjela admin prava drugim članovima.

## Vanjski servisi

- **Slanje notifikacija** (npr. putem SendGrid-a):
  - Obavijesti o propuštenim zadacima, novim zadacima i približavanju rokova.
- **Gamifikacija** (npr. putem Gamiphy):
  - Leaderboard, bedževi i razine za motivaciju korisnika.
- **Integracija kalendara** (npr. putem Google Calendar API):
  - Pregled svih rokova unutar osobnog kalendara korisnika.
- **Personalizirani ChatBot** (npr. putem Rasa servisa):
  - Pomaže korisnicima s pitanjima i informacijama o aplikaciji.

## Sigurnost

Aplikacija koristi **OAuth 2.0** za autentifikaciju i autorizaciju korisnika, pri čemu se prijava odvija putem emaila i lozinke koji se provjeravaju izravno u našoj bazi podataka (lozinka je naravno hashirana).

- **Prijava/Autentifikacija**: Korisnik se prijavljuje pomoću emaila i lozinke. Nakon uspješne prijave, backend generira i vraća pristupni token (access token) koji se koristi za autentifikaciju daljnjih zahtjeva.
- **Frontend** koristi `http interceptore` za automatsko dodavanje pristupnog tokena u zaglavlja svakog HTTP zahtjeva prema backendu, omogućujući siguran prijenos podataka.
- **Backend** provjerava valjanost pristupnih tokena te omogućuje pristup zaštićenim resursima samo ovlaštenim korisnicima. Također, nakon dulje sesije token ce isteći.
- **Pohrana tokena**: Pristupni tokeni i osvježavajući tokeni pohranjuju se lokalno na klijentskoj strani, omogućujući kontinuirani pristup bez potrebe za ponovnim prijavljivanjem.
- **Autorizacija**: Uloge poput user i admin biti će razlikovane pomoću role atributa unutar claimova tokena.

## Tehnologije i alati

- **Voditelj tima**: Eni Magdalena Oreč (eo54656@fer.hr)
- **Praćenje koda**: Git
- **Komunikacija tima**: Slack, WhatsApp
- **Backend**: Django
- **Frontend**: Angular
- **Baza podataka**: SQL

## Članovi tima i doprinosi

- Eni Magdalena Oreč
- Ana Gašperov
- Ena Dvojak
- Lovre Marasović
- Antonio Vito Šprljan
- Sven Đukić
- Tomislav Kušek

## Funkcijski zahtjevi

| ID zahtjeva | Opis                                                                                          | Prioritet | Izvor                     | Kriteriji prihvaćanja                                                                                         |
|-------------|-----------------------------------------------------------------------------------------------|-----------|---------------------------|---------------------------------------------------------------------------------------------------------------|
| F-001       | Kreiranje i upravljanje grupama                       | Visok     | Zahtjev dionika          | Korisnik se može registrirati e-mailom, primiti e-mail za potvrdu i uspješno se prijaviti.                  |
| F-002       | Registracija i autentifikacija korisnika                       | Visok     | Zahtjev dionika          | Korisnik može kreirati grupu i unijeti naziv grupe, sustav generira kod za pristup grupi i opciju dijeljenja linka, novi članovi mogu koristiti kod ili link za pridruživanje grupi.                   |
| F-003       | Dodavanje i praćenje zadataka                      | Visok     | Zahtjev dionika, povratne informacije korisnika          | Korisnik može unijeti naziv, težinu i rok zadatka, zadaci su prikazani prema statusu, korisnik može vidjeti tko je preuzeo zadatak i status svakog zadatka u grupi.                 |
| F-004       | Slanje notifikacija putem e-maila                       | Srednji     | Povratne informacije korisnika          | E-mail notifikacija se šalje kada zadatak nije izvršen u predviđenom roku, kad je zadatak preuzet, korisnici primaju e-mail podsjetnike prije roka zadatka.                  |
| F-005       | Gamifikacija aplikacije (Leaderboard, bodovanje i bedževi)                       | Srednji     | Povratne informacije korisnika          | Korisnici vide bodove u leaderboardu, korisnik prima bedževe pri dosegu određenog broja bodova ili recenzija, leaderboard prikazuje rang članova grupe na temelju bodova.          |
| F-006       | Kalendar zadataka                       | Srednji     | Zahtjev dionika, postojeći sustavi          | Korisnik može pregledati kalendar u svakom trenutku, kalendar prikazuje sve preuzete zadatke s rokovima, klikom na zadatak u kalendaru korisnik se preusmjerava na pojedinosti zadatka.                  |
| F-007       | Uređivanje korisničkog profila                       | Srednji     | Zahtjev dionika, povratne informacije korisnika          | Korisnik može uređivati ime, e-mail i profilnu sliku, korisnik može vidjeti aktivne zadatke unutar profila, korisnik može otkazati preuzete zadatke i pristupiti kalendaru s rokovima zadataka.                  |
| F-008       | Administratorski panel za upravljanje grupama i zadacima                       | Nizak     | Zahtjev dionika          | Admin tim (developeri) može pristupiti panelu s prikazom svih grupa, podataka o grupama i bazom podataka za administraciju, administrator može pregledati sve grupe i podatke o članovima i zadacima, može ukloniti grupe ili zadatke prema potrebi, panel omogućuje pregled i uređivanje baze podataka unutar administrativnog sučelja.                  |
| F-009       | Ocjenjivanje zadataka - nakon izvršenja zadatka, članovi grupe mogu ocijeniti zadatak bodovima i napisati recenziju                     | Srednji     | Zahtjev dionika          | Korisnik može ocijeniti zadatak od 1 do 5, ocjene se bilježe i spremaju u statistike, članovi mogu dodati pisanu recenziju na završeni zadatak.                  |
