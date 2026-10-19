# Server virtuale del Laboratorio Sperimentale

Mockup per la riunione sull'acquisto del server virtuale. Mostra quali servizi saranno installati, come sono collegati tra loro e come appariranno alle persone che li usano.

Il progetto è composto da due pagine web statiche, senza dipendenze da installare:

| Pagina | Contenuto |
|---|---|
| `index.html` | Schema del server, tabella dei servizi, esempi d'uso, stima delle risorse, punti da decidere |
| `interfaccia.html` | Schermate indicative di portale, corpora, siti di progetto, annotazione, codice, formazione e stato dei servizi |

Tutti i nomi di progetto e di persona nelle schermate sono inventati. I nomi dei servizi (NoSketchEngine, INCEpTION, Forgejo, ecc.) sono quelli veri.

## Specifiche del server

### Taglia consigliata

| Risorsa | Valore | Note |
|---|---|---|
| RAM | 16 GB | I servizi usano circa 8,5 GB. Con 8 GB non c'è margine |
| CPU | 4 vCPU | |
| Disco | almeno 160 GB | Dipende soprattutto dalla dimensione dei corpora indicizzati, da verificare |
| Sistema | Linux con Docker Compose | Un container per servizio |

Le cifre di RAM sono **stime**, non misure. In particolare eXist-db, INCEpTION e NoSketchEngine dipendono dalla quantità di dati e di utenti.

### Servizi

| Servizio | A cosa serve | Indirizzo (esempio) | RAM stimata | Stato |
|---|---|---|---|---|
| Caddy | Ingresso unico, certificati HTTPS automatici | porta 443 | 0,1 GB | proposto |
| NoSketchEngine | Interrogazione dei corpora | corpora.lab.it | 2,0 GB | confermato |
| INCEpTION | Annotazione di testi, usa MySQL | annotazione.lab.it | 2,0 GB | richiesto |
| eXist-db + TEI Publisher | Sito e database XML di un progetto, pubblicazione di testi TEI | progetto-b.lab.it, testi.lab.it | 2,0 GB | confermato |
| Sito di progetto A | Banca dati con sito pubblico e backoffice con login, usa MySQL | progetto-a.lab.it | 0,4 GB | confermato (modello ListTyp) |
| Forgejo | Repository di codice, issue e revisioni, usa MySQL | git.lab.it | 0,4 GB | confermato |
| MySQL | Database del sito A, di Forgejo e di INCEpTION | solo interno | 0,6 GB | |
| Siti statici | Pagine HTML servite direttamente da Caddy | nome.lab.it | trascurabile | confermato |
| Sito della formazione | Note di Obsidian trasformate in HTML (per esempio con Quartz), pubblico | formazione.lab.it | trascurabile | confermato |
| Uptime Kuma | Pagina di stato e avvisi se un servizio non risponde | stato.lab.it | 0,15 GB | proposto |
| restic | Backup notturno cifrato su storage esterno | solo interno | trascurabile | proposto |

Sistema operativo e Docker occupano circa 0,8 GB.

### Come sono collegati

- Tutto il traffico entra da Caddy, che sceglie il servizio in base al nome dell'indirizzo. Nessun servizio è esposto direttamente.
- Il sito A, Forgejo e INCEpTION salvano in MySQL.
- eXist-db è già un database XML e scrive nel volume dati. TEI Publisher gira dentro eXist-db.
- NoSketchEngine legge gli indici dei corpora dal volume dati.
- I siti statici sono file su disco, serviti da Caddy.
- Il backup legge database e volume ogni notte (03:00) e li copia, cifrati, su uno storage esterno di un altro provider.

### Come si aggiorna il contenuto

- **Nuovo corpus**: si converte il TEI in formato `.vert` sul proprio computer (come per DiCCAS), si carica in `/data` e si indicizza con gli strumenti di NoSketchEngine.
- **Sito della formazione**: poche persone aggiornano le note in Obsidian, generano il sito sul proprio computer e caricano i file sul server. La generazione automatica da Forgejo richiede un runner e un po' di RAM in più e si valuterà solo se i redattori aumentano.
- **Siti di progetto**: l'amministratore del progetto lavora dal backoffice del sito.

## Da decidere

- Provider e taglia definitiva della VPS (16 GB bastano per i primi anni?).
- Dominio e chi gestisce i record DNS.
- Dove vanno i backup: storage di un altro provider o disco in laboratorio.
- Quali corpora caricare all'inizio e quanto spazio occupano una volta indicizzati.
- Quali altri siti portare sul server oltre ai due di partenza, con che tecnologia e chi li mantiene.
- Chi amministra il server: account, aggiornamenti, avvisi di Uptime Kuma.
- Come i redattori caricano i file dei siti statici (per esempio accesso SFTP riservato).

## Ipotesi da verificare

- **prepararsi-al-presente**: il repository non ha un README e non è chiaro se la sua interfaccia sia solo statica. L'ho trattato come sito statico, ma va controllato.
- **DiCCAS** è un corpus TEI convertito in formato `.vert`, quindi si ospita in NoSketchEngine. La sua pagina HTML oggi è su GitHub Pages ed è generata con XSLT.
- Le righe in arabo della scheda Corpora e il numero di occorrenze sono esempi inventati, non estratti di DiCCAS.
- La schermata di NoSketchEngine, INCEpTION e Forgejo imitano solo in modo generico l'aspetto reale dei programmi.
- Il colore dei quattro riquadri nella striscia sotto la fascia è stimato a occhio dal logo.

## Struttura dei file

```
index.html            pagina dello schema (solo struttura)
interfaccia.html      pagina delle schermate (solo struttura)
css/
  stile.css           colori, caratteri e componenti comuni
  schema.css          stile specifico di index.html
  interfaccia.css     stile specifico di interfaccia.html
js/
  interfaccia.js      schede, login finto, barre dello stato dei servizi
img/
  logo-laboratorio.png  logo del laboratorio, ridimensionato a 900 px di larghezza
docker-compose.yml    scheletro dei servizi del server
Caddyfile             ingresso unico: un blocco per ogni indirizzo
.env.example          variabili da compilare (dominio, password, versioni)
mysql/init/           script che crea i database alla prima creazione
config/inception/     modello delle impostazioni di INCEpTION
exist/autodeploy/     pacchetti .xar di TEI Publisher e dei progetti
siti/                 siti statici, una cartella per sito
noske/                note su NoSketchEngine
demo-locale/          mini demo da avviare in locale con Docker (vedi il suo README)
```

## Docker

Il server si gestisce con Docker Compose: `docker-compose.yml` definisce i servizi e `Caddyfile` instrada gli indirizzi. Sono uno **scheletro non testato su un server vero**: la sintassi dei due file è stata controllata, ma i servizi non sono mai stati avviati.

Per provarlo:

1. Copia `.env.example` in `.env` e compila dominio, email e password.
2. Copia `config/inception/settings.properties.example` in `config/inception/settings.properties` e inserisci la password.
3. Controlla i punti segnati `TODO` nei file: versioni e nomi delle immagini, impostazioni di INCEpTION, percorsi di eXist-db e TEI Publisher.
4. Avvia con `docker compose up -d`.

Ancora da fare:

- **NoSketchEngine**: non è definito, perché non so se esista un'immagine ufficiale (vedi `noske/LEGGIMI.md`).
- **Sito A**: dipende da come è fatto il sito; nel file c'è un blocco commentato da adattare.
- **Backup**: non è nel file Compose. Serve un job notturno con un dump di MySQL e la copia cifrata dei volumi su uno storage esterno.
- **Git via SSH** su Forgejo: richiede una porta in più.
- **Segreti**: `.env` e `settings.properties` sono esclusi dal repository. Non committarli.
- **Memoria**: i `mem_limit` sono circa 1,5 volte le stime e vanno regolati dopo aver misurato l'uso reale.

## Come modificare

1. Apri `index.html` o `interfaccia.html` nel browser per vedere il risultato. I caratteri vengono caricati da Google Fonts, quindi serve la connessione.
2. Modifica il testo nell'HTML. La RAM nella tabella, nella barra e nella legenda va aggiornata in tutti e tre i punti di `index.html`.
3. Per cambiare l'aspetto, i colori sono variabili all'inizio di `css/stile.css`. Esiste anche la versione per il tema scuro.
4. Le larghezze delle barre (RAM, disco, grafico delle occorrenze) sono scritte inline nell'HTML perché sono i dati del grafico.
5. Per aggiungere una schermata in `interfaccia.html`: crea un blocco `<div class="screen" id="...">`, un pulsante nelle schede con `data-s="..."` e l'indirizzo in alto in `js/interfaccia.js` (oggetto `urls`).

## Stile

Lo stile riprende il sito del laboratorio (https://site.unibo.it/laboratorio-sperimentale/it): blu `#00457c`, bordeaux `#81042d` all'hover, fondo grigio chiaro, angoli quadrati, Merriweather per titoli ed etichette, Source Sans per il testo.

