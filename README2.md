var redd for at jeg ville overide readme.md vist jeg skrev i den så jeg skriver min dokumentasjon her

Appen viser en Chuck Norris-vits for dagen. Den er laget i Python med Flask. Før jeg kunne endre noe måtte jeg lære meg hvordan koden til mine med partnere fungerte. app.py henter en vits fra et API og lagrer den i filen jokeVault det er bare en vits per dato. Så sender den vitsen til index.html. Ny vits kommer klokka 09:00.

Alt under her er det jeg har lagt til eller rettet. Jeg ville ikke egentlig endre den gamle koden til mine partnere mer enn jeg måtte og jeg ville ikke bruke penger. Derfor ligger nesten alt i en egen fil og betalingsmuren er gratis.

Hva jeg har gjort

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

Jeg ble ferdig å sett opp appen på nginx proxt manager så nå kan du gå på gimegennychucknorrisvitsklokkennihvermorgenhverdag.no.com.it3.iktim.no og se at appen fungerte det tok lang tid med mye feilsøking men jeg fikk det til. for å være mer spesefikk måtte jeg endre på alt hele tiden men også uten å endre mye.

Jeg testet appen og alt virker som det skal for nå og er helt perfekt.