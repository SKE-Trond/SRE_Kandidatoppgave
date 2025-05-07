# Kandidatoppgave

Kandidatoppgaven viser at du kan sette opp et system for overvåkning av applikasjoner og 
løsningen vil bli brukt som utgangspunkt i neste intervju. 

Ting som er relevante å vise frem:
- Finne frem i kode for å finner porter, endepunkter og eventuelt endre på disse parameterene. 
- Containerization av koden/filene. 
- IaC
- Bruk av Grafana, med tilhørende konfigurasjon
- Oppsett og bruk av metrikker, log og trace.

Steget med å sette opp Grafana og dashboards som viser helsestatus er viktig, og mye av dette kan løses uten logg og trace. Husk derfor å bruke tiden fornuftig.  


## Forslag til løst oppgave

**Se i `oppgavepakke` mappen først. Der er det hjelp til å komme i gang med et grunnleggende oppsett.**

Klienten sender en forespørsler til server, og mange av dem er misslykket. 

Serveren tar imot json med beskrivelse av dyr hvor det er en del krav. Hester og hunder
trenger å ha 4 bein. Noen dyr tar lengre tid, og noen kan lage feil.

Under er et forslag til steg for løsning. Det vil være forskjellig erfaringsnivå på kandidater og derfor må du se selv hvordan det er fornuftig å bruke tiden. 

*Husk å legge ved screenshots i besvarelsen*.

Hvis du har god kontroll på oppgaven så er det positivt om du legger til flere elementer.

Husk at alle hjelpemidler, bortsett fra å få hjelp av andre personer, er tilgjengelig. ChatGPT er behjelpelig for mye av dette, samt Grafana blogger og forum m.m.

**Lever besvarelsen på GitHub.** Legg ved Dockerfiler, yaml filer, eller hva enn du velger å bruke for å løse oppgaven.
Legg også ved en **README.md** som beskriver løsningen og kjøring av systemet. 
**Lever oppgaven som et privat repo som du deler med følgende brukere: SKE-Trond, Salve, Rmyhren**

### Container

Sett opp et kubernetes cluster lokalt med f.eks. kind eller minikube.

Kjør server og klient som seperate pods. Gjennomfør resten av oppgaven i cluster. Nye komponenter som legges til bør leve i clusteret.

Husk å endre `SERVER_URL` i client koden.

( Hvis det ikke er mulig å få til lokalt cluster, så kan de andre stegene fint gjennomføres uten cluster. )

( Et annet alternativ er å bare bruke docker direkte, men helst sammen med docker-compose )

### Grafana

Legg til Grafana og sjekk at den kjører. Siste versjon burde fungere fint for denne oppgaven. 


### Metrikker

Legg til Prometheus og scrape metrikker.

DataSource for Prometheus må settes opp i Grafana.

Se at metrikkene er tilgjengelige i Grafana med å bruke riktig DataSource.

(Hvis du ikke får data i Grafana så er det lurt å sjekke Prometehus direkte først for å se om data er tilgjengelig der.)


### Logger

Legg til Loki som komponent. 

Bruk Promtail for å sende loggene. 

( Siden dette er lokalt og demo/oppgave så er det ok å mounte docker socket direkte til Promtail komponenten )

Se at loggene er tilgjengelig i Grafana fra Loki. Husk å sette opp DataSource for Loki og å ta den i bruk i Grafana.

Sett opp filter og søk. Finn relevante logglinjer. 

OBS: Loggene er enkle og har ikke mye å sortere på. Det er ikke forventet at det finnes gode labels annet enn å sortere på hvilken komponent det gjelder.


### Trace

(Avansert)

Legg til Tempo i cluster og lytt på rett port. Port finner du i logg og/eller server/klient koden.

Det kan hende noen kodeendringer må gjøres først, og rebuild av docker images.

Bruk Tempo data source i Grafana og finn traces.

( Her kan det være noen snubbletråder, og husk å bruk tiden fornuftig på andre steg først om du sitter fast. )


### Dashboard og oversikt

**Husk screenshots i besvarelsen.**

Bruk Grafana til å sette opp dashboard for å se hvordan applikasjonene oppfører seg. 

#### RED

En fin måte å se generell helsetilstand er å bruke Requests, Error og Delay til å lage dashboard.

Finn relevant metrikker fra sererapplikasjonen og sett opp en oversikt over hvor lang tid det tar å behandle forespørsler.
Histogram fra Prometheus metrikker kan være litt knot i Grafana, men det er fine guider lett tilgjengelig rundt forbi.

For Request delen så sjekk raten på forespørsler. 

Error er liknende, men sjekk f.eks. 500 responser. 

( Her kan du selvsagt også bruke data fra logger og trace )

#### SLO

Du trenger ikke å sette opp noe i Grafana, men tenk over hva som er relevant her i forhold til SLO. 

- Hvilken datakilde er relevant som SLI?
- Hvis vi tenker at applikasjonen kjører tilfredsstillende, hvilke grenseverdier er relevante for feil og forsinkelser?

#### Trace

Få opp trace hvis du har fått lagt det inn og legg ved screenshots.

#### Logger

Vis loggene i dashboards.

#### Alarmer

Ikke tenk på at alarmene må sendes en plass. Vis heller hva som er grunnlaget for alarmene. 

#### Provisioning

(Valgfritt)

Legg ved filer for provisioning av Grafana i løsningen.

### CI/CD

( Valgfritt, men nyttig )

Sett opp en pipeline i Github eller liknende hvor du viser at du forstår hvilke steg 
som er relevante. 

Du kan også legge dette til lokalt med Jenkins om du er konfortabel med det.


### Forslag til andre elementer

( Veldig valgfritt ) 

- Sikkerhet/nettverk i cluster
- Horisontal skalering i Kubernetes. Her lagres data direkte i server applikasjonen, slik at HA ikke er gunstig i praksis, men du kan vise konseptet om du er komfortabel med det.
