# Consigli per la gestione del server

Appunti su come gestire il server condiviso, calibrati su un'infrastruttura piccola, con dati aperti e poche persone che se ne occupano.

## Persone e responsabilità

La parte più importante.

- **Almeno due amministratori**, non uno. Se la gestione dipende da una sola persona, il server dura finché quella persona resta in Dipartimento.
- **Una pagina di documentazione "cosa fare se"**, scritta per chi non ha costruito il server: come si riavvia, dove sono i backup, chi ha le credenziali del dominio e dell'hosting. Le credenziali vanno in un password manager condiviso, non in testa a qualcuno.
- **Un responsabile per ogni progetto ospitato**, scritto in un file (nome, contatto, licenza, data di inizio). Quando una persona se ne va, si sa a chi chiedere.

## Costi e sostenibilità

- Decidere prima **chi paga**: quota per progetto in fase di richiesta di finanziamento, fondo di Dipartimento o altro. L'idea di accorpare i costi regge solo se c'è una risposta chiara.
- Prevedere una **quota di ingresso** per i nuovi progetti, ad esempio una voce "hosting a lungo termine" nel budget. Così i costi dopo la fine del progetto sono già coperti.
- Tenere **dominio e hosting intestati al Dipartimento o all'Ateneo**, non a una persona.

## Regole per i progetti ospitati

- **Policy di ingresso breve**: licenza aperta dichiarata, dimensione massima, un responsabile, un contatto.
- **Policy di uscita**: se un progetto non ha più un responsabile o i dati non servono più, il servizio viene archiviato (ad esempio una copia su Zenodo, con DOI) e poi spento. Va deciso ora, altrimenti il server si riempie di servizi orfani.
- **Un servizio nuovo si aggiunge solo se qualcuno si impegna a mantenerlo.** Per ogni servizio nella tabella serve un referente.

## Tecnica

- **Backup fuori dalla macchina**, in un posto diverso dall'hosting, con un ripristino provato davvero almeno una volta. Un backup mai ripristinato non è una garanzia.
- Tenere **tutto in Git** (il Compose, il Caddyfile, la documentazione).
- **Aggiornamenti a cadenza fissa**, ad esempio una volta al mese. Con le immagini Docker, fissare le versioni invece di usare `latest`.
- **Uptime Kuma** con notifica a due persone, non a una.
- **Limiti di risorse** sui container (memoria e CPU): NoSketch Engine o eXist-db possono saturare la macchina e fermare gli altri servizi.
- Servizi come MySQL e INCEpTION vanno aggiunti solo quando servono davvero. Ogni servizio in più è manutenzione in più.

## Sicurezza, in proporzione a quanto si sa fare

- I dati aperti riducono il rischio, ma restano da proteggere gli account e gli accessi in scrittura. **Autenticazione a due fattori** per gli amministratori e per Forgejo.
- **Pochi account con permessi di scrittura**, e per ogni gruppo solo chi serve.
- **Accesso SSH solo con chiavi**, senza password, e firewall che lascia aperte solo le porte 80 e 443.

## Da decidere con il Dipartimento

1. Chi sono i due amministratori e quante ore ci possono dedicare?
2. Dove gira il server: macchina di Ateneo, hosting commerciale o cloud?
3. Chi paga e come si calcola la quota per un nuovo progetto?
4. Per quanto tempo si promette di ospitare un dataset (5 anni? 10?)? Meglio non promettere "per sempre".
