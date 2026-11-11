# Trym Dokumentasjon

Appen viser en Chuck Norris-vits for dagen. Den er laget i Python med Flask. Før jeg kunne endre noe måtte jeg lære meg hvordan koden til mine med partnere fungerte. app.py henter en vits fra et API og lagrer den i filen jokeVault det er bare en vits per dato. Så sender den vitsen til index.html. Ny vits kommer klokka 09:00.

Alt under her er det jeg har lagt til eller rettet. Jeg ville ikke egentlig endre den gamle koden til mine partnere mer enn jeg måtte og jeg ville ikke bruke penger. Derfor ligger nesten alt i en egen fil og betalingsmuren er gratis.

## Hva jeg har gjort

Jeg rettet en feil med nedtellingen la til fire annonser laget en knapp for å fjerne annonser laget en donasjonsknapp og koblet til Google AdSense.

Filer jeg har endret

paywall/paywall.py. Nå ligger annonsene knappene og betalingsmuren der lagde fra scratch.

app.py har fått noen nye linjer. Den importerer nå paywall-filen, registrerer den og har en ny rute til nedtellingen. Jeg har ikke endret eller fjernet noe som sto der fra før.

templates/index.html har fått et lite JavaScript nederst til nedtellingen. Resten er likt.

Feilen med nedtellingen

På siden sto det "Calculating..." under "Time remaining until next Chuck Norris joke" Det fantes ingen kode som byttet ut teksten så den sto sånn hele tiden.

Jeg la til ruten /seconds-until-next-joke i app.py. Den regner ut hvor mange sekunder det er til neste klokka 09:00 med samme regel som timeForNewJoke() bruker. I index.html la jeg til JavaScript som henter tallet og teller ned hvert sekund. Når det blir null lastes siden på nytt én gang og da kommer den nye vitsen.

Jeg lot serveren regne ut tiden og ikke nettleseren. Vitsen bytter nemlig etter klokka på serveren og hvis serveren står i en annen tidssone enn den som besøker siden ville nedtellingen blitt feil.

Det er en annonse på toppen en nederst en til venstre og en til høyre. De ligger fast på skjermen. For at de ikke skal dekke teksten la jeg til litt luft rundt innholdet men bare når annonsene vises. På mobil (smalere enn 720 px) skjules annonsene på sidene fordi det ikke er plass til dem. Når annonsene er fjernet ser siden ut som før bare med to nye knapper. Hva som står i annonsene styres i listen ADS øverst i paywall.py.

Knappen "Remove ads" åpner en popup som sier "Free". Når man trykker på "Remove ads for free" sender nettleseren en POST til /paywall/remove-ads. Serveren lagrer da en cookie som heter ads_removed i ett år. Etter det sendes ikke annonsene med i siden. Knappen heter da "Ads are off" og i popupen kan man trykke "Bring ads back" for å få dem tilbake.

Jeg gjorde den gratis fordi jeg ikke vil bruke penger. Ulempen er at alle kan fjerne annonsene og at det bare gjelder i den nettleseren man brukte. Hvis jeg vil ta betalt senere er det i funksjonen remove_ads() jeg må sjekke betalingen før cookien lagres. For å slippe å endre index.html setter paywall.py inn annonser og knapper rett før </body> på hver HTML-side, etter at siden er laget.

Knappen "Donate" åpner en donasjonsside i en ny fane. Adressen står i DONATE_URL øverst i paywall.py. . Akkurat nå står det https://ko-fi.com/Zzyzx_x som er min egen kofi du burde donere til.

Google AdSense. Google ga meg en kodebit for en annonseenhet. Jeg la den inn i paywall.py. ADSENSE_CLIENT er min utgiver-ID og ADSENSE_SLOT er annonseenheten. Alle fire annonsene bruker samme enhet, og Google-skriptet lastes bare en gang. dette gjorde jeg for å senere legge til ekte ads vist me blir approved av google og me tenker det blir nødvendig

På localhost vises grå plassholdere i stedet for ekte annonser så jeg ikke klikker på mine egne annonser (det er mot reglene til Google). Hvis man har fjernet annonsene, lastes ingen Google-kode. Man kan også skru av AdSense med ADSENSE_ENABLED = False.

Jeg kan legge til siden min i AdSense og vente på godkjenning. sjansen er da at google sier nei siden me har lite faktisk innhold
tror det skal fint kjøre i Docker

Hvis jeg åpner siden som localhost får jeg plassholdere i stedet for AdSense.

Jeg ryddet også opp i oppsettet slik at appen bruker pakkestrukturen konsekvent. Flask finner nå templates og paywall inne i pakken, og Docker starter appen som en Python-modul. jokeVault blir også kopiert inn i Docker-containeren. Jeg testet at appen starter lokalt og at forsiden svarer med HTTP 200.



# Noah Dokumentasjon:
Min arbeidsoppgave var og gjøre det visuele delen av prosjekte, det var for det meste gjort av sebastian, han hjalp til med og lage noen containers og boxes for for meg til og endre farge på, vi endte opp med engrålig svart gradient farge på nettsiden, etter vi hadde gjort det skulle vi lage til så det fungerer på mobilen som jeg aldri gjorde, men tror trym fiksa det etter hvert


# Sebastian Dokumentasjon:
Min arbeidsoppgave har vært å programmere selve funksjonen av appen. Altså at du får en tilfeldig chuck norris vits klokken 9 hver morgen. Jeg begynte først med å sette opp flask og lage en super simpel template html fil å jobbe i. Jeg satt først opp JavaScript i HTML som sjekket hva klokken var, og om det hadde passert klokken 9 enda, hentet en vits fra APIet til api.chucknorris.io også viste den på tekst objektet. Jeg hadde det satt opp slik at den sjekke om det allerede fins en vits i localStorage, og hvis der gjør, vis den frem. Hvis ikke, hent en vits fra APIet og lagre den i localStorage. Sondre viste meg at det vil si at vitsen er bare lokal. Hver maskin hadde fått en annerledes vits, men målet var at alle fikk den samme nye vitsen. Derfor begynte jeg å kode logikken igjen i flask. Da fikk jeg satt opp en nokså lik funksjon. Der er en JSON jokeVault fil som lagrer alle vitsene og datoene de var på. Først sjekker koden om det er en vits lagret for dagens dato, og om klokken er 9 eller mer. Hvis den finner en lagret vits for dagen så viser den vitsen frem. Hvis ikke henter den en vits fra APIet og lagrer den i JSON filen. Om klokken ikke har nådd 9 henter den vitsen fra forrige dag ved samme metode.

## Problemer:
- Proxmox orker ikke koble seg til. Måtte endre IP utallige ganger
- Docker og nginx er svært forvirrende og jeg hadde ikke fått det til uten Kevin
- Koden var client sided til å begynne med, måtte endre til server side ved å skrive på nytt i python

## Teknisk
Applikasjonen bruker Python, Flask, Docker og Nginx. Docker starte, stoppe og oppdatere applikasjonen, mens Nginx videresender trafikken.
Applikasjonen blir oppdatert via Nginx i proxmox der me bruke comandoen git pull

## Docker
Dockerfilen henter en python modell fra Docker Hub og angir hvilket directory den skal se på. Så laster den ned UV og henter kravene. Etterpå oppdaterer den seg selv og prøve å innstalere kravene og blir kvitt restene av de gamle utdaterte filene. Deretter prøver den å synce med uv, også henter den src folderen, kopierer jokeVault JSON filen og åpner port 5000 før den starter appen.

## Tilgansplan
Port 5000 brukes internt, og Nginx videresender trafikken til applikasjonen. Vi tester at tilgangen fungerer, og at applikasjonen er tilgjengelig gjennom nettleseren.

## Forklaring
Formålet ved appen er å skape glede i en potensielt dårlig dag ved hjelp av Chuck Norris vitser. Klokken ni om morgenen hver dag henter vi en ny Chuck Norris vits for å vise frem på nettsiden vårs. Vitsene blir lagret ned med dato slik at alle vitser som har blitt vist kan ses.
    