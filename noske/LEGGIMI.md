# NoSketchEngine

Si usa l'immagine `eltedh/nosketch-engine` (progetto [ELTE-DH/NoSketch-Engine-Docker](https://github.com/ELTE-DH/NoSketch-Engine-Docker)). Il progetto KIParla ne ha un fork, [KIParla/NoSketch-Engine-Docker](https://github.com/KIParla/NoSketch-Engine-Docker), che usa la stessa immagine e aggiunge un Makefile con i comandi per compilare i corpora.

Questa cartella è vuota di proposito: l'immagine è già pubblicata su Docker Hub e non serve un Dockerfile. Il servizio `noske` è definito in `docker-compose.yml`.

## Struttura della cartella dei corpora

`CORPORA_DIR` (in `.env`) punta a una cartella fatta così:

```
corpora/
  registry/
    NOME         file di configurazione del corpus
  NOME/
    vertical/
      source     file in formato verticale (.vert)
    indexed/     creata dalla compilazione
```

Nel file di registry, `PATH` deve essere `/corpora/NOME/indexed/` e `VERTICAL` deve essere `/corpora/NOME/vertical/source`: sono i percorsi dentro il container.

## Aggiungere o ricompilare un corpus

1. Metti il file verticale in `NOME/vertical/source` e il file di configurazione in `registry/NOME`.
2. Compila l'indice:

```sh
docker compose run --rm noske compilecorp --no-ske --recompile-corpus /corpora/registry/NOME
```

3. Riavvia il servizio per essere sicuro che lo veda: `docker compose restart noske`.

Altri comandi utili:

```sh
docker compose run --rm noske corpinfo -s NOME       # informazioni sul corpus
docker compose run --rm noske compile.sh             # compila tutti i corpora in registry/
```

## Da sapere

- Senza `HTACCESS` e `HTPASSWD` l'interfaccia è aperta a tutti. Per proteggerla con una password, vedi il README del fork KIParla (sezione "Basic auth").
- L'immagine pesa circa 1 GB.
- Il tetto di memoria nel file Compose (3 GB) è una stima da verificare con corpora grandi.
