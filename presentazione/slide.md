# Un server condiviso per la ricerca del Dipartimento

Obiettivi, servizi possibili e le vostre esigenze

Laboratorio Sperimentale · LILEC · Riunione di Dipartimento, ottobre 2026

> Note: durata prevista circa 45 minuti (15 di presentazione, 30 di discussione). Lo scopo non è presentare una soluzione già decisa, ma raccogliere le esigenze dei gruppi prima di scegliere la soluzione tecnica.

---

## L'obiettivo

Uno spazio comune per ospitare dati e servizi usati nei diversi progetti di ricerca.

Pensato per l'intero Dipartimento, non solo per il Laboratorio.

> Note: ripartire dalla mail inviata al Dipartimento. L'iniziativa nasce da esigenze già emerse negli scorsi anni nel Laboratorio, ma la progettazione non deve essere dettata solo da quelle.

---

## Perché un server condiviso

- **Il problema**: i progetti producono piccoli dataset che, per essere accessibili, richiedono un po' di infrastruttura. Alla fine del progetto i costi non sono più sostenibili.
- **L'idea**: poiché i dataset sono piccoli, accorpiamo i costi e gestiamo una sola infrastruttura per tutti.

> Note: questo è il motivo per cui il server esiste: dare una casa duratura agli output dei progetti dopo la fine dei finanziamenti. Dataset piccoli, quindi poche risorse da condividere.

---

## Cosa è, cosa non è

**È**

- Un'infrastruttura server condivisa
- Uno spazio per dati e servizi di ricerca
- Un luogo per pubblicare gli output dei progetti
- Una risorsa a disposizione di tutti i gruppi

**Non è**

- Un'infrastruttura di calcolo
- Un cluster per training o elaborazioni pesanti
- Una soluzione già decisa nei dettagli tecnici
- Un servizio solo per il Laboratorio

> Note: sottolineare subito che non si tratta di calcolo: niente GPU o code di job.

---

## Le esigenze emerse finora

- **Consultare corpora**: NoSketch Engine per interrogare i corpora, anche con accesso riservato.
- **Pubblicare pagine**: siti statici di presentazione e navigazione degli output di ricerca.
- **Ospitare dati**: un luogo stabile per dati e risorse, oltre il singolo progetto o portatile.

**E le vostre?** Queste vengono dal Laboratorio. Il punto della riunione è scoprire cosa serve agli altri gruppi.

> Note: la lista è parziale. Invitare già a pensare alle proprie esigenze; le domande specifiche arrivano alla slide 11.

---

## Servizi nel mockup

| Servizio | A cosa serve | Tecnologia |
|---|---|---|
| Corpora | Interrogazione di corpora annotati | NoSketch Engine |
| Siti statici | Pagine di progetto e output | Caddy |
| Versionamento | Codice, dati e siti dei progetti | Forgejo |
| Annotazione | Annotazione testuale collaborativa | INCEpTION |
| Archivi XML | Testi marcati e edizioni digitali | eXist-db |
| Database | Dati strutturati dei progetti | MySQL |
| Monitoraggio | Controllo che i servizi siano attivi | Uptime Kuma |

> Note: non è una lista chiusa. Alcuni servizi sono già provati in locale (NoSketch Engine, Forgejo), altri sono segnaposto. Chiedere se manca qualcosa di importante.

---

## Come potrebbe funzionare

**Utenti** (browser, un solo dominio) → **Caddy** (un indirizzo per servizio, HTTPS automatico) → **Servizi** (un container Docker per ciascuno, aggiornabili separatamente)

Tutto descritto in Docker Compose: riproducibile, documentato e spostabile su un'altra macchina.

> Note: ogni servizio è isolato, quindi aggiungerne uno nuovo non rompe gli altri. Rimandare alla demo.

---

## Uno spazio per ogni gruppo

- **Indirizzi separati**: ogni progetto o gruppo ha il suo indirizzo, ad esempio un sottodominio dedicato.
- **Permessi propri**: chi può modificare e chi può solo consultare lo decide ciascun gruppo.
- **Gestione condivisa**: backup, aggiornamenti e monitoraggio sono gestiti una volta sola, non da ogni gruppo.

> Note: restano aperte le domande su chi amministra il server e come si decidono le richieste di spazio. Le portiamo in discussione, non le decidiamo noi.

---

## Solo dati con licenza aperta

- Ospitiamo solo dataset con licenza open source o aperta
- Non abbiamo le competenze per gestire livelli di sicurezza avanzati
- Niente dati riservati o sensibili

> Note: scelta di prudenza: un'infrastruttura gestita da pochi non può garantire sicurezza avanzata, quindi il perimetro è ciò che è già pubblico per licenza. Chiarire il caso dei corpora ad accesso riservato citati tra le esigenze: restano compatibili solo se la licenza lo consente.

---

## Demo

- La pagina iniziale con i servizi
- Una consultazione in NoSketch Engine
- Un sito di progetto di esempio

> Note: demo locale in Docker (cartella `demo-locale`). Per NoSketch Engine usare il profilo opzionale: l'immagine pesa circa 1 GB. Se la demo non parte, usare il mockup statico.

---

## Domande per la discussione

1. Che dati o servizi usa o userebbe il vostro gruppo?
2. Oggi dove li tenete e quali problemi avete?
3. Quanto spazio e quanti utenti prevedete?
4. Serve un accesso pubblico, riservato o entrambi?
5. Quanto conta la durata nel tempo di ciò che pubblicate?
6. Chi potrebbe occuparsi della gestione?

> Note: cuore della riunione, 25-30 minuti. Giro di tavolo, una domanda alla volta, appunti per gruppo. La domanda 6 (gestione e sostenibilità) è la più delicata: non lasciarla per ultima senza tempo.

---

## Prossimi passi

1. Raccogliere le esigenze dei gruppi, anche dopo la riunione
2. Definire la soluzione tecnica più adatta
3. Condividere una proposta con il Dipartimento

**Scadenza per i contributi:** [data] · **Referente:** [nome ed email]

> Note: chiudere con una scadenza concreta e un referente. I campi tra parentesi quadre vanno compilati prima della riunione.
