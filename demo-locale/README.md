# Demo locale

Mini versione del server, da far partire sul proprio computer con Docker. Serve a mostrare come apparirà il server, con contenuti di esempio inventati: NoSketchEngine con tre corpora, Forgejo con due repository e un dataset da scaricare, e tre siti di progetto finti che riprendono le schermate del mockup. Caddy smista gli indirizzi verso i servizi.

È una demo, non una configurazione per il server vero: usa HTTP semplice, password di esempio e nessun backup.

## Cosa serve

Docker con Docker Compose (per esempio Docker Desktop) e una connessione a Internet: la prima volta scarica le immagini, e le pagine caricano i caratteri da Google Fonts.

## Avvio

```sh
cd demo-locale
./prepara-esempi.sh
```

Lo script avvia i servizi, compila i corpora di esempio e riempie Forgejo (la prima volta scarica anche le immagini, NoSketchEngine pesa circa 1 GB). Si può rilanciare senza danni. Poi apri http://localhost:8080, che mostra l'elenco di tutti gli indirizzi.

Per spegnere:

```sh
docker compose --profile noske down        # ferma i servizi e conserva i dati
docker compose --profile noske down -v     # ferma tutto e cancella anche i dati di Forgejo e Uptime Kuma
```

## Indirizzi

| Indirizzo | Cosa c'è |
|---|---|
| http://lab.localhost:8080 | Interfaccia del mockup, con tutte le schede |
| http://lab.localhost:8080/schema | Schema e servizi |
| http://corpora.localhost:8080 | NoSketchEngine con tre corpora di esempio |
| http://git.localhost:8080 | Forgejo con due repository di esempio |
| http://progetto-alpha.localhost:8080 | Sito di esempio: banca dati con backoffice |
| http://progetto-beta.localhost:8080 | Sito di esempio: corpus annotato |
| http://progetto-gamma.localhost:8080 | Sito di esempio: edizione di testi TEI |
| http://formazione.localhost:8080 | Sito statico di esempio |
| http://stato.localhost:8080 | Uptime Kuma (chiede di creare un utente) |

I tre siti di progetto sono pagine statiche che riprendono le schermate del mockup (`../interfaccia.html`): niente è collegato a un database vero. In Progetto Beta si può cambiare lemma, significato e periodo e il grafico si aggiorna (con lemmi `posse`, `debere`, `uelle`); in Progetto Gamma si sfogliano i versi, si clicca sulle note, si cerca nel testo e si passa a facsimile e XML. I numeri sono inventati. Il backoffice accetta qualsiasi password.

I nomi che finiscono in `.localhost` di solito li risolve già il browser sul computer locale. Se un indirizzo non si apre (può succedere con Safari), aggiungi queste righe a `/etc/hosts`:

```
127.0.0.1 lab.localhost formazione.localhost git.localhost stato.localhost
127.0.0.1 corpora.localhost progetto-gamma.localhost progetto-alpha.localhost progetto-beta.localhost
```

## Contenuti di esempio

- **Forgejo**: utente `maria` o amministratore `labadmin`, password `demo1234`. Contiene l'organizzazione `lab` con cinque repository: `tokenizer` e `corpus-tools` (codice e issue), `dati-esempio` (con un rilascio `dataset.zip` da scaricare), `edizione-gamma` (un testo TEI) e `guida-nuovi-membri`. Le registrazioni sono chiuse.
- **NoSketchEngine**: tre corpora piccoli in `corpora-esempio/`: il primo canto dell'Inferno (30 versi), l'inizio dei *Promessi sposi* (testi di pubblico dominio) e tre notizie di giornale inventate. Lemmi e categorie grammaticali sono indicativi, assegnati da `genera.py` con poche regole: servono solo a far vedere l'interfaccia. Per sostituirli con corpora veri, usa `CORPORA_DIR=/percorso/dei/corpora` (struttura in `../noske/LEGGIMI.md`).
- **Uptime Kuma** chiede di creare un utente alla prima visita.

## Cosa si può provare

- Cambiare la pagina del sito statico: modifica `siti/formazione/index.html` e ricarica la pagina. Non serve riavviare nulla.
- Aggiungere un nuovo sito statico: crea una cartella in `siti/`, copia il blocco `formazione.localhost` nel `Caddyfile` e riavvia Caddy con `docker compose restart caddy`.
- Modificare le pagine del mockup nella cartella principale: la demo le legge da lì, quindi basta ricaricare.

## Cosa non c'è

INCEpTION, eXist-db con TEI Publisher, MySQL e Progetto Alpha non sono inclusi: i siti di progetto sono pagine finte. Gli stessi servizi sono nello scheletro del server vero (`docker-compose.yml` nella cartella principale).
