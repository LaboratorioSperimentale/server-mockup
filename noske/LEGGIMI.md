# NoSketchEngine

Questa cartella è vuota di proposito. Non conosco un'immagine Docker ufficiale di NoSketchEngine.

Da fare:

1. Cercare se esiste un'immagine mantenuta e aggiornata. In quel caso si usa direttamente in `docker-compose.yml`.
2. Altrimenti scrivere qui un `Dockerfile` che installi Manatee, Bonito e Crystal, e decomentare il blocco `noske` in `docker-compose.yml`.
3. Montare i corpora indicizzati (per esempio DiCCAS in formato `.vert`) nella cartella che NoSketchEngine si aspetta e verificare la porta da dare a Caddy.
