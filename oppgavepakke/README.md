# TL;DR

Lag docker images og kjør docker-compose

# Hjelp til å komme igang

Vi har lagt ved et lite sett med filer for å komme i gang.

Docker og docker-compose på være installert og tilgjengelig.

## Lag docker images

Kopier `Dockerfile_server` sammen med `requirements.txt` og `animals_server.py` til en 
ny mappe og kjør `docker build -t animals_server_image .`.

Sjekk at du har et image med det gitte navnet, `docker images`.

Sjekk at du kan kjøre image med `docker run -p 5000:5000 animals_server_image`. 
Og se at du har metrikker tilgjengelig på endepunktet `/metrics` på den gitte porten lokalt.

Gjør tilsvarende for klienten. Lag ny mappe, legg ved filene du trenger for image og kjør tilsvarende kommandoer.

## Kjør docker-compose

Etter at du har laget riktig image for server og klient, så skal det bare være å kjøre: `docker-compose up`.

Det skal være satt opp datakilder i Grafana for logg, trace og metrikker, men det er kun lagt ved 
metrikker i startpakken her.

Startpakken her skal da ha satt opp Prometheus, Grafana, klienten og server. 
Klienten begynner å mase på server som får en del feil forespørsler. 

Prometheus "scraper" metrikker og du kan finne dem på port 9090 hvis du vil se dem direkte fra Prometheus.
Søk på f.eks. `animal_added_total`.

## Grafana

Metrikkene skal være tilgjengelig i Grafana med Prometheus DataSource. Sett opp dashboard eller bruk "explore" 
for å undersøke metrikker. 

## Feilsøk

- Sjekk at du bruker riktige navn på images i forhold til hva som er i docker-compose
- Kjøre docker-compose i detached mode, og se på logger individuelt
- Vær sikker på at du legger ved riktige filer når du bygger image. Sjekk at hvert image starter greit.
- CURL/Postman e.l. mot server for å sjekke at den fungerer
- Bruk `docker ps`, `docker images` osv. for å verifisere hvert steg.

## Klar til oppgaveløsning

Se på oppgaven i rootfolder `README.md` og gjør videre arbeid.



