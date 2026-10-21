"""Genera i tre corpora di esempio in formato verticale (NoSketchEngine).

Lemmi e categorie sono INDICATIVI: li assegna un'euristica con poche regole, non un
analizzatore morfologico. Servono solo a mostrare l'aspetto dell'interfaccia.
Uso:  python3 genera.py
"""
import re
from pathlib import Path

DANTE = """Nel mezzo del cammin di nostra vita
mi ritrovai per una selva oscura,
ché la diritta via era smarrita.
Ahi quanto a dir qual era è cosa dura
esta selva selvaggia e aspra e forte
che nel pensier rinova la paura!
Tant'è amara che poco è più morte;
ma per trattar del ben ch'i' vi trovai,
dirò de l'altre cose ch'i' v'ho scorte.
Io non so ben ridir com'i' v'intrai,
tant'era pien di sonno a quel punto
che la verace via abbandonai.
Ma poi ch'i' fui al piè d'un colle giunto,
là dove terminava quella valle
che m'avea di paura il cor compunto,
guardai in alto e vidi le sue spalle
vestite già de' raggi del pianeta
che mena dritto altrui per ogne calle.
Allor fu la paura un poco queta,
che nel lago del cor m'era durata
la notte ch'i' passai con tanta pieta.
E come quei che con lena affannata,
uscito fuor del pelago a la riva,
si volge a l'acqua perigliosa e guata,
così l'animo mio, ch'ancor fuggiva,
si volse a retro a rimirar lo passo
che non lasciò già mai persona viva."""

MANZONI = """Quel ramo del lago di Como, che volge a mezzogiorno, tra due catene non interrotte di monti, tutto a seni e a golfi, a seconda dello sporgere e del rientrare di quelli, vien, quasi a un tratto, a ristringersi, e a prender corso e figura di fiume, tra un promontorio a destra, e un'ampia costiera dall'altra parte; e il ponte, che ivi congiunge le due rive, par che renda ancor più sensibile all'occhio questa trasformazione, e segni il punto in cui il lago cessa, e l'Adda rincomincia, per ripigliar poi nome di lago dove le rive, allontanandosi di nuovo, lascian l'acqua distendersi e rallentarsi in nuovi golfi e in nuovi seni.
La costiera, formata dal deposito di tre grossi torrenti, scende appoggiata a due monti contigui, l'uno detto di san Martino, l'altro, con voce lombarda, il Resegone, dai molti suoi cocuzzoli in fila, che in vero lo fanno somigliare a una sega: talmente che non è chi, al primo vederlo, purché sia di fronte, come per esempio di sulle mura di Milano che guardano a settentrione, non lo discerna tosto, a un tal contrassegno, in quella lunga e vasta giogaia, dagli altri monti di nome più oscuro e di forma più comune."""

# Testi inventati, come i nomi di persona e di luogo
GIORNALE = {
 "giornale_0317": """Il presidente ha ribadito di non voler parlare di candidature prima dell'autunno.
Nel pomeriggio il sindaco tornerà a parlare alla cittadinanza dal balcone del municipio.
Il consiglio comunale ha approvato il bilancio con una larga maggioranza.
La biblioteca resterà aperta fino a tardi durante la settimana degli esami.
I lavori sul ponte vecchio finiranno entro la fine del mese.""",
 "giornale_0318": """Il museo ha inaugurato ieri una mostra dedicata ai manoscritti del Quattrocento.
Molti studenti hanno visitato la mostra e hanno posto domande ai curatori.
La direttrice ha detto che il progetto continuerà anche l'anno prossimo.
Il comune ha annunciato nuove corse notturne per gli autobus del centro.
Nessuno ha voluto commentare la notizia fino a ieri sera.""",
 "giornale_0319": """Il torneo di scacchi si è chiuso con la vittoria di una giovane giocatrice di Parma.
Gli organizzatori sperano di ripetere l'evento in primavera.
Il presidente della società ha parlato di un risultato storico per la città.
Domani il tempo sarà instabile, con piogge sparse sulla pianura.
La festa del paese si terrà comunque nella piazza davanti alla chiesa.""",
}

DET = {"il","lo","la","i","gli","le","un","uno","una","l'","un'","quel","quella","quei","quello","questa","questo"}
PREP = {"di","a","da","in","con","su","per","tra","fra","del","dello","della","dei","degli","delle","al","allo","alla","ai","agli","alle","dal","dallo","dalla","dai","dagli","dalle","nel","nello","nella","nei","negli","nelle","sul","sullo","sulla","sui","sugli","sulle","all'","dall'","nell'","sull'","de'","de","d'","dell'","dell","sulle","dagli","all'occhio"}
CONJ = {"e","ed","o","ma","che","se","come","purché","perché","quando","dove","poi","né","ch'"}
PRON = {"io","tu","mi","ti","si","ci","vi","lo","li","ne","m'","t'","s'","v'","ch'i'","i'","chi","cui","qual","quei","altrui","mio","sua","suoi","sue","nostra","tanta","tutto","nessuno","molti","molto","tali","tal"}
AUX = {"è","era","fu","sono","sarà","essere","ha","ho","hanno","avea","ho","è'"}
ADV = {"non","più","già","ancor","ancora","così","là","anche","quasi","ben","mai","ivi","tosto","ieri","domani","comunque","poco","fino"}
LEMMI = {"è":"essere","era":"essere","fu":"essere","sono":"essere","sarà":"essere","si":"si","ha":"avere","ho":"avere","hanno":"avere","avea":"avere",
         "sua":"suo","suoi":"suo","sue":"suo","nostra":"nostro","vita":"vita","gli":"il","le":"il","i":"il","la":"il","lo":"il","del":"di","della":"di","dei":"di","delle":"di","nel":"in","nella":"in","al":"a","alla":"a","dal":"da","dalla":"da"}

TOKEN = re.compile(r"\w+'|\w+(?:-\w+)*|[^\w\s]", re.UNICODE)

def tag(w, first):
    lw = w.lower()
    if not re.match(r"\w", w): return "PUNCT" if w in ",;:.!?()" else "SYM"
    if lw in DET: return "DET"
    if lw in PREP: return "ADP"
    if lw in CONJ: return "CONJ"
    if lw in AUX: return "AUX"
    if lw in ADV or lw.endswith("mente"): return "ADV"
    if lw in PRON: return "PRON"
    if w[0].isupper() and not first: return "PROPN"
    if re.search(r"(are|ere|ire|ato|ata|ati|ate|uto|uta|ndo|ò|ì|ano|ono|ero|isce|ono|ava|eva|iva)$", lw) and len(lw) > 3: return "VERB"
    if re.search(r"(oso|osa|ose|osi|ale|ali|ivo|iva|ivi|ive|ico|ica|ichi|iche|ente|enti|ante|anti)$", lw): return "ADJ"
    return "NOUN"

def lemma(w):
    lw = w.lower()
    return LEMMI.get(lw, lw)

def sentences(text):
    out = []
    for line in text.split("\n"):
        out.append(line)
    return out

def verticale(docs, split_on_punct):
    righe = []
    for did, titolo, testo in docs:
        righe.append(f'<doc id="{did}" title="{titolo}">')
        if split_on_punct:
            unita = re.split(r"(?<=[.!?])\s+", testo.replace("\n", " "))
        else:
            unita = testo.split("\n")
        for u in unita:
            if not u.strip(): continue
            righe.append("<s>")
            toks = TOKEN.findall(u)
            for k, t in enumerate(toks):
                righe.append(f"{t}\t{lemma(t)}\t{tag(t, k == 0)}")
            righe.append("</s>")
        righe.append("</doc>")
    return "\n".join(righe) + "\n"

REGISTRY = """NAME "{nome}"
PATH /corpora/{id}/indexed/
VERTICAL /corpora/{id}/vertical/source
ENCODING "utf-8"
LANGUAGE "Italian"
INFO "{info}"
DEFAULTATTR word
MAXCONTEXT 80
MAXDETAIL 200

ATTRIBUTE word
ATTRIBUTE lemma
ATTRIBUTE tag
ATTRIBUTE lc {{
  DYNAMIC utf8lowercase
  DYNLIB internal
  ARG1 "C"
  FUNTYPE s
  FROMATTR word
  TYPE index
  TRANSQUERY yes
}}

STRUCTURE doc {{
  ATTRIBUTE id
  ATTRIBUTE title
}}
STRUCTURE s
"""

CORPORA = [
  ("dante", "Dante · Inferno, canto I (esempio)", "Primi trenta versi. Testo di pubblico dominio; lemmi e categorie indicativi.",
   [("inf1", "Inferno I, vv. 1-30", DANTE)], False),
  ("manzoni", "Manzoni · I promessi sposi, incipit (esempio)", "Primi due paragrafi. Testo di pubblico dominio; lemmi e categorie indicativi.",
   [("ps1", "I promessi sposi, cap. I", MANZONI)], True),
  ("giornale", "Giornale di esempio (inventato)", "Notizie inventate per la demo; lemmi e categorie indicativi.",
   [(k, k + ".txt", v) for k, v in GIORNALE.items()], False),
]

base = Path(__file__).parent
(base / "registry").mkdir(exist_ok=True)
for cid, nome, info, docs, split in CORPORA:
    (base / cid / "vertical").mkdir(parents=True, exist_ok=True)
    (base / cid / "vertical" / "source").write_text(verticale(docs, split), encoding="utf-8")
    (base / "registry" / cid).write_text(REGISTRY.format(id=cid, nome=nome, info=info), encoding="utf-8")
    print(cid, sum(1 for l in (base / cid / "vertical" / "source").read_text().splitlines() if l and l[0] != "<"), "token")
