# Demo locale

Mini versione del server, da far partire sul proprio computer con Docker. Serve a vedere come Caddy smista gli indirizzi verso servizi diversi, con due servizi veri (Forgejo e Uptime Kuma) e le pagine del mockup.

È una demo, non una configurazione per il server vero: usa HTTP semplice, nessuna password e nessun backup.

## Cosa serve

Docker con Docker Compose (per esempio Docker Desktop) e una connessione a Internet: la prima volta scarica le immagini, e le pagine caricano i caratteri da Google Fonts.

## Avvio

```sh
cd demo-locale
docker compose up -d
```

Poi apri http://localhost:8080, che mostra l'elenco di tutti gli indirizzi.

Per spegnere:

```sh
docker compose down        # ferma i servizi e conserva i dati
docker compose down -v     # ferma tutto e cancella anche i dati di Forgejo e Uptime Kuma
```

## Indirizzi

| Indirizzo | Cosa c'è |
|---|---|
| http://lab.localhost:8080 | Interfaccia del mockup |
| http://lab.localhost:8080/schema | Schema e servizi |
| http://formazione.localhost:8080 | Sito statico di esempio |
| http://git.localhost:8080 | Forgejo |
| http://stato.localhost:8080 | Uptime Kuma |

Questi indirizzi mostrano solo un avviso, perché i servizi non sono inclusi: `corpora`, `annotazione`, `testi`, `progetto-a`, `progetto-b` (sempre con `.localhost:8080`).

I nomi che finiscono in `.localhost` di solito li risolve già il browser sul computer locale. Se un indirizzo non si apre (può succedere con Safari), aggiungi queste righe a `/etc/hosts`:

```
127.0.0.1 lab.localhost formazione.localhost git.localhost stato.localhost
127.0.0.1 corpora.localhost annotazione.localhost testi.localhost progetto-a.localhost progetto-b.localhost
```

## Primo avvio dei servizi

- **Forgejo** mostra la pagina di installazione: lascia i valori proposti (database SQLite) e crea il primo utente, che diventa amministratore.
- **Uptime Kuma** chiede di creare un utente alla prima visita.

## Cosa si può provare

- Cambiare la pagina del sito statico: modifica `siti/formazione/index.html` e ricarica la pagina. Non serve riavviare nulla.
- Aggiungere un nuovo sito statico: crea una cartella in `siti/`, copia il blocco `formazione.localhost` nel `Caddyfile` e riavvia Caddy con `docker compose restart caddy`.
- Modificare le pagine del mockup nella cartella principale: la demo le legge da lì, quindi basta ricaricare.

## Cosa non c'è

NoSketchEngine, INCEpTION, eXist-db con TEI Publisher, MySQL e il sito A non sono inclusi. Per NoSketchEngine non so se esista un'immagine pronta, e per gli altri non ho verificato i nomi delle immagini: sono nello scheletro del server vero (`docker-compose.yml` nella cartella principale).
