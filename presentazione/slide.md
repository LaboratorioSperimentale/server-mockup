# Un server condiviso per i dati del Dipartimento

Laboratorio Sperimentale · LILEC · Riunione di Dipartimento, ottobre 2026

---

## L'obiettivo

Scopo della riunione: raccogliere le esigenze dei gruppi prima di vagliare la soluzione tecnica.

**Il server:** uno spazio **in comune** per ospitare dati prodotti nell'ambito di piccoli (e grandi) progetti di ricerca del Dipartimento.

---

## Perché un server condiviso

L'iniziativa nasce da esigenze già emerse negli scorsi anni nel Laboratorio, ma la progettazione non deve essere dettata solo da quelle.

- **Il problema**: i progetti producono piccoli dataset che, per essere accessibili esternamente, richiedono un po' di infrastruttura. Alla fine del progetto i costi non sono più sostenibili.

- **L'idea**: poiché i dataset sono generalmente piccoli in termini di risorse di calcolo necessarie, accorpiamo i costi e gestiamo una sola infrastruttura per tutti.

---

## Cosa vorremmo

- Un'infrastruttura co-costruita e condivisa
- Uno spazio per dati di ricerca
- Un luogo per pubblicare (semplici) output dei progetti
- Una risorsa stabile a disposizione di tutti i gruppi

---

## Cosa **non** vogliamo o possiamo sostenere

- Un'infrastruttura di calcolo
- Account privati
- Servizi personalizzati sul progetto (questo va concordato con il Laboratorio in fase di progettazione)
- Supporto 24/7
- Alto numero di accessi
- Dati che richiedono controllo sul riuso (sensibili, con licenze restrittive)

---

## Le esigenze emerse finora in Laboratorio

- **Consultare corpora**: NoSketchEngine o ANNIS per interrogare i corpora
- **Pubblicare pagine**: siti statici di presentazione e navigazione degli output di ricerca
- **Ospitare dati**: un luogo "facile" per depositare dati e risorse e offrire un link per il download

**E le vostre?**

---

## Servizi nel mockup

| Servizio      | A cosa serve                         | Tecnologia      |
| ------------- | ------------------------------------ | --------------- |
| Corpora       | Interrogazione di corpora annotati   | NoSketch Engine |
| Siti statici  | Pagine di progetto e output          | Caddy           |
| Versionamento | Codice, dati e siti dei progetti     | Forgejo         |
| Archivi XML   | Testi marcati e edizioni digitali    | eXist-db / TEI Publisher |
| Database      | Dati strutturati dei progetti        | MySQL           |

---

## Alcuni servizi condivisi e uno spazio per ogni progetto

- **Indirizzi separati**: ogni servizio o "progetto" ha il suo indirizzo, ad esempio un sottodominio dedicato.
- **Un accesso per progetto**: lo gestisce il responsabile del gruppo.
- **Gestione condivisa**: backup, aggiornamenti e monitoraggio sono gestiti una volta sola, non da ogni gruppo.

> Note: tecnicamente è un proxy (Caddy) davanti a un container Docker per servizio, descritto in Docker Compose e spostabile su un'altra macchina; entrare nel dettaglio solo se qualcuno lo chiede, e rimandare alla demo. Le questioni di gestione (chi amministra, finanziamento, richieste di spazio) sono nella slide con le domande per la discussione.

---

## Domande per la discussione

### Le vostre esigenze

1. Che **dati o servizi** usa o userebbe il vostro gruppo?
2. Oggi dove li tenete e quali **problemi** avete?
3. Quanto **spazio** e quanti **utenti** prevedete?

### La gestione

1. **Come si finanzia?** Una quota per progetto, un fondo di Dipartimento, o altro? E dopo la fine dei finanziamenti?
2. **Chi lo amministra?** Chi si occupa di aggiornamenti, backup e problemi, e chi lo sostituisce?
3. **Come si gestiscono le richieste di spazio?** Chi decide, con quali criteri e con quali limiti?

> Note: cuore della riunione, 25-30 minuti. Giro di tavolo, una domanda alla volta, appunti per gruppo. Le domande sulla gestione sono le più delicate: non lasciarle per ultime senza tempo. Le portiamo in discussione, non le decidiamo noi. Un solo account per progetto evita di gestire le persone una per una, ma non dice chi ha fatto cosa e va cambiato quando qualcuno lascia il gruppo; per il codice (Forgejo) sono meglio account personali.
