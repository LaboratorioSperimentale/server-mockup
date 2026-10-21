"""Riempie Forgejo con utenti, repository, issue e un rilascio di esempio (tutto inventato).

Lo lancia prepara-esempi.sh; si può rilanciare senza danni: ciò che esiste già viene saltato.
"""
import base64, io, json, sys, urllib.error, urllib.request, zipfile
from pathlib import Path

BASE = "http://git.localhost:8080/api/v1"
ADMIN = ("labadmin", sys.argv[1])
AUTH = "Basic " + base64.b64encode(f"{ADMIN[0]}:{ADMIN[1]}".encode()).decode()


def api(metodo, percorso, dati=None, grezzo=None, tipo="application/json"):
    corpo = grezzo if grezzo is not None else (json.dumps(dati).encode() if dati is not None else None)
    r = urllib.request.Request(BASE + percorso, data=corpo, method=metodo,
                               headers={"Authorization": AUTH, "Content-Type": tipo})
    try:
        with urllib.request.urlopen(r) as f:
            b = f.read()
            return json.loads(b) if b else {}
    except urllib.error.HTTPError as e:
        if e.code in (409, 422):  # esiste già
            return None
        raise SystemExit(f"{metodo} {percorso}: {e.code} {e.read().decode()[:200]}")


def file(repo, nome, testo, msg):
    api("POST", f"/repos/{repo}/contents/{nome}",
        {"content": base64.b64encode(testo.encode()).decode(), "message": msg})


api("POST", "/orgs", {"username": "lab", "full_name": "Laboratorio Sperimentale", "visibility": "public",
                       "description": "Codice e dati del Laboratorio (esempio)"})

# --- lab/tokenizer
api("POST", "/orgs/lab/repos", {"name": "tokenizer", "description": "Tokenizzatore per l'italiano (esempio)",
                                "auto_init": True, "default_branch": "main"})
file("lab/tokenizer", "README.md",
     "# tokenizer\n\nSegmenta testi italiani in token, gestendo apostrofi ed elisioni.\n\n"
     "```sh\npython -m tokenizer testo.txt\n```\n\nRepository di esempio per la demo.\n",
     "Istruzioni per riprodurre i risultati")
file("lab/tokenizer", "environment.yml",
     "name: tokenizer\ndependencies:\n  - python=3.12\n  - regex\n", "Fissa le versioni delle dipendenze")
file("lab/tokenizer", "src/tokenizer.py",
     'import regex\n\nTOKEN = regex.compile(r"\\w+\'|\\w+|[^\\w\\s]")\n\n\ndef tokenize(testo):\n    return TOKEN.findall(testo)\n',
     "Gestisce apostrofi nelle forme elise")
file("lab/tokenizer", "tests/test_tokenizer.py",
     "from src.tokenizer import tokenize\n\n\ndef test_elisione():\n    assert tokenize(\"l'anno\") == [\"l'\", \"anno\"]\n",
     "Aggiunge casi per l'italiano")
for titolo, corpo in [("Apostrofo tipografico non riconosciuto", "Con ’ al posto di ' l'elisione non viene divisa."),
                      ("Numeri con la virgola", "1,5 viene diviso in tre token."),
                      ("Aggiungere i trattini", "Le parole con trattino andrebbero tenute unite.")]:
    api("POST", "/repos/lab/tokenizer/issues", {"title": titolo, "body": corpo})

# --- lab/dati-esempio, con un rilascio da scaricare
api("POST", "/orgs/lab/repos", {"name": "dati-esempio", "description": "Dataset di esempio con licenza aperta",
                                "auto_init": True, "default_branch": "main"})
file("lab/dati-esempio", "README.md",
     "# dati-esempio\n\nDataset inventato per la demo, con licenza **CC BY 4.0**.\n\n"
     "Per scaricarlo, vai alla sezione *Rilasci* e prendi `dataset.zip`.\n\n"
     "Come citare: Laboratorio Sperimentale (2026), *Dataset di esempio*, v1.0.\n",
     "Descrive il dataset")
file("lab/dati-esempio", "LICENSE", "Creative Commons Attribution 4.0 International (CC BY 4.0)\n"
     "https://creativecommons.org/licenses/by/4.0/\n", "Aggiunge la licenza")
file("lab/dati-esempio", "lessico-frequenze.csv", "parola,frequenza\nlingua,120\ncorpus,87\ndato,64\n",
     "Aggiunge il lessico delle frequenze")

rel = api("POST", "/repos/lab/dati-esempio/releases",
          {"tag_name": "v1.0", "name": "v1.0 · dataset di esempio",
           "body": "Prima versione. Licenza CC BY 4.0. Contiene il lessico delle frequenze e il corpus di esempio.",
           "target_commitish": "main"})
if rel:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("lessico-frequenze.csv", "parola,frequenza\nlingua,120\ncorpus,87\ndato,64\n")
        z.write(Path(__file__).parent / "corpora-esempio/giornale/vertical/source", "giornale.vert")
        z.writestr("LICENSE.txt", "CC BY 4.0 - https://creativecommons.org/licenses/by/4.0/\n")
    api("POST", f"/repos/lab/dati-esempio/releases/{rel['id']}/assets?name=dataset.zip",
        grezzo=buf.getvalue(), tipo="application/zip")

# --- altri repository di esempio
def repo(org, nome, descr, argomenti=()):
    api("POST", f"/orgs/{org}/repos", {"name": nome, "description": descr, "auto_init": True, "default_branch": "main"})
    if argomenti:
        api("PUT", f"/repos/{org}/{nome}/topics", {"topics": list(argomenti)})


repo("lab", "corpus-tools", "Strumenti per preparare i corpora per NoSketchEngine (esempio)", ["corpora", "python"])
file("lab/corpus-tools", "README.md",
     "# corpus-tools\n\nConverte testi annotati in formato verticale (`.vert`) per NoSketchEngine.\n\n"
     "```sh\npython tei2vert.py testo.xml > source\n```\n\nDopo la conversione l'amministratore carica il file sul server e compila l'indice.\n",
     "Descrive l'uso")
file("lab/corpus-tools", "tei2vert.py",
     "import sys\nimport xml.etree.ElementTree as ET\n\n\ndef main(percorso):\n    for riga in ET.parse(percorso).iter('{http://www.tei-c.org/ns/1.0}l'):\n"
     "        print('<s>')\n        for parola in ''.join(riga.itertext()).split():\n            print(parola)\n        print('</s>')\n\n\nmain(sys.argv[1])\n",
     "Aggiunge il convertitore da TEI")
file("lab/corpus-tools", "tests/test_vert.py", "def test_vuoto():\n    assert True\n", "Aggiunge un test")
for titolo, corpo in [("Lemmi e categorie dal TEI", "Oggi il convertitore stampa solo le forme."),
                      ("Supportare i file di grandi dimensioni", "Il file viene letto tutto in memoria.")]:
    api("POST", "/repos/lab/corpus-tools/issues", {"title": titolo, "body": corpo})

repo("lab", "edizione-gamma", "Testo TEI di esempio per Progetto Gamma (CC BY-SA 4.0)", ["tei", "edizione-digitale"])
file("lab/edizione-gamma", "README.md",
     "# edizione-gamma\n\nTesto in TEI per la pubblicazione con TEI Publisher. Licenza **CC BY-SA 4.0**.\n\n"
     "Per aggiungere un testo: copia il file XML in `testi/` e apri una richiesta di revisione.\n", "Descrive il repository")
file("lab/edizione-gamma", "testi/canto1.xml",
     '<?xml version="1.0" encoding="UTF-8"?>\n<TEI xmlns="http://www.tei-c.org/ns/1.0">\n  <teiHeader><fileDesc>\n'
     '    <titleStmt><title>Esempio di testo, canto I</title></titleStmt>\n    <publicationStmt><p>Esempio per la demo</p></publicationStmt>\n'
     '    <sourceDesc><p>Testo di pubblico dominio</p></sourceDesc>\n  </fileDesc></teiHeader>\n  <text><body><lg>\n'
     '    <l n="1">Nel mezzo del <term>cammin</term> di nostra vita</l>\n    <l n="2">mi ritrovai per una <term>selva oscura</term>,</l>\n'
     '    <l n="3">ché la diritta via era smarrita.</l>\n  </lg></body></text>\n</TEI>\n', "Aggiunge il canto I")
file("lab/edizione-gamma", "LICENSE", "Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)\n"
     "https://creativecommons.org/licenses/by-sa/4.0/\n", "Aggiunge la licenza")

repo("lab", "guida-nuovi-membri", "Guida per chi arriva in Laboratorio (esempio)", ["guida"])
file("lab/guida-nuovi-membri", "README.md",
     "# Guida per nuovi membri\n\n1. Chiedi un account all'amministratore.\n2. Leggi la guida alle licenze dei dati.\n"
     "3. Clona un repository e prova a proporre una modifica.\n\nPer i dati da pubblicare: solo licenze aperte, niente dati sensibili.\n", "Prima versione")
file("lab/guida-nuovi-membri", "licenze.md",
     "# Licenze dei dati\n\nPubblichiamo solo dati con licenza aperta (per esempio CC0, CC BY, CC BY-SA).\n"
     "Le licenze NC e ND non vanno bene. Chi deposita garantisce di avere i diritti.\n", "Aggiunge la guida alle licenze")

print("Forgejo: altri repository pronti")
print("Forgejo pronto")
