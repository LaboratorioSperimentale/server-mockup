#!/bin/sh
# Prepara la demo con i contenuti di esempio: corpora in NoSketchEngine e utenti,
# repository e rilascio in Forgejo. Si può rilanciare senza danni.
# Uso:  cd demo-locale && ./prepara-esempi.sh
set -e
cd "$(dirname "$0")"
PW=demo1234

echo "Avvio i servizi (la prima volta scarica le immagini)..."
docker compose --profile noske up -d

echo "Compilo i corpora di esempio..."
for c in dante manzoni giornale; do
  docker compose --profile noske run --rm noske compilecorp --no-ske --recompile-corpus /corpora/registry/$c >/dev/null
done
docker compose --profile noske restart noske >/dev/null

echo "Preparo Forgejo..."
until curl -sf -o /dev/null http://git.localhost:8080/; do sleep 2; done
for u in labadmin maria; do
  A=""; [ "$u" = labadmin ] && A="--admin"
  docker compose exec -T -u git forgejo forgejo admin user create $A --username $u \
    --email $u@lab.localhost --password $PW --must-change-password=false 2>&1 | grep -v "already exists" || true
done
python3 prepara-forgejo.py "$PW"

echo
echo "Pronto: apri http://localhost:8080"
echo "Forgejo: utente labadmin (amministratore) o maria, password $PW"
