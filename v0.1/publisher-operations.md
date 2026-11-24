# Publisher Operations Guide: TechTable Standard v0.1

Cum ar funcționa lanțul **Sheet → Store → API → Discovery** la nivel operațional. Spec-ul descrie *ce* publici (forma JSON-LD); acest doc descrie *cum* administrezi datele ca publisher.

> Acest workflow nu face parte din spec. E o cale posibilă de intrare a datelor, pentru cine ține deja informațiile într-un Google Sheet. Alte căi (de exemplu colectarea automată din locurile în care organizațiile publică deja) sunt la fel de valide cât timp output-ul JSON-LD e conform.

> **Schiță, neimplementată.** Componentele descrise aici (scripturi, API, store) nu sunt construite încă. Documentul arată cum ar putea funcționa o cale de intrare a datelor.

## Roluri

- **Editor**: adaugă/modifică conținut despre propria organizație. Mulți, ~1 per organizație activă. Acces edit la Sheet.
- **Curator**: validează conținutul nou propus. Puțini per ecosistem (~1-3). Acces edit la Sheet + permisiuni speciale (vezi mai jos).

## Workflow editor → curator → publicare

### 1. Editor propune

- Editor adaugă rând nou în Sheet (eveniment, organizație etc.)
- Apps Script `onEdit`:
  - Setează `_status = draft`
  - Completează `_created_by` = email-ul editorului (`Session.getActiveUser()`)
  - Completează `_created_at` = timestamp
- Editorul lucrează liber în draft (modifică, completează câmpuri)
- **Curatorul nu e notificat încă**

### 2. Editor submit pentru review

- Editor: meniu „TechTable → Submit for review” (Apps Script custom menu)
- Apps Script:
  - Validează că rândul are `req` fields populate (per JSON Schema corespunzător)
  - Setează `_status = pending_review`
  - Trimite **notificare imediată** curatorului (email + opțional WhatsApp/Slack via webhook)
- Curatorul primește o singură notificare per submit (nu per edit)

### 3. Curator validează

- Curator filtrează `_status = pending_review`
- Reviewuiește, opțional editează (corectează typo, completează câmpuri lipsă)
- Schimbă `_status = validated` (manual sau buton dedicat „TechTable → Validate”)
- Apps Script:
  - Completează `_validated_by` + `_validated_at`
  - Rândul devine eligibil pentru publicare la următorul sync

### 4. Modificări post-validare

- Editorul **poate** modifica un rând `validated` (de regulă ajustări de detaliu)
- `_status` rămâne `validated`; **publicarea continuă**
- Curatorul vede flag-ul **„modified after validation”** prin formulă derivată: `_last_edit_at > _validated_at` cu formatare condiționată (orange)
- Curatorul re-verifică pasiv; clear-uiește validând din nou (timestamp se actualizează → flag dispare)
- Niciun câmp boolean dedicat - formula e zero-overhead

### 5. Withdraw

- Editor sau curator schimbă `_status = withdrawn`, opțional cu motiv în `_status_reason`
- Cazuri tipice: typo, duplicate, eveniment programat dar anulat „silent” (audiența nu trebuie informată)
- **NU se publică**

### 6. Caz special: event cancelled / postponed

- Pentru evenimente anulate dar **relevante public** (audiența trebuie să știe), folosește câmpul **public** `eventStatus` (din schema.org), NU `_status = withdrawn`
- Valori acceptate: `EventScheduled` (default), `EventCancelled`, `EventPostponed`, `EventRescheduled`, `EventMovedOnline`
- Rândul rămâne `_status = validated` și e publicat - cu marcaj
- Regula pentru editor:
  - **„scoate din vedere”** → `_status = withdrawn`
  - **„anunță anularea”** → `eventStatus = EventCancelled`

### 7. Publicare

Apps Script „Publish” (manual din meniu sau scheduled hourly):

1. Citește toate rândurile `_status = validated` per entitate
2. Validează împotriva JSON Schema corespunzător (`v0.1/schemas/`)
3. Convertește Drive image IDs → URL-uri publice (vezi §Imagini)
4. POST către Worker `/admin/sync` cu API key (vezi §Sync)
5. Worker upsert în store (D1 default): vezi sync model

Eșec validare: rând `validated` care nu trece JSON Schema → log eroare în sheet `_publish_log` + email curator + **NU** se publică (alte rânduri continuă)

## Coloane operaționale în Sheet

Toate prefixate cu `_` pentru a marca natura non-publică:

| Coloană | Tip | Cine setează | Note |
|---|---|---|---|
| `_status` | enum | Apps Script + curator + editor | `draft` / `pending_review` / `validated` / `withdrawn` |
| `_status_reason` | text | curator sau editor | Opțional - motivul rejection/withdraw |
| `_created_by` | email | Apps Script | Editorul care a adăugat rândul |
| `_created_at` | timestamp | Apps Script | |
| `_validated_by` | email | Apps Script | Curatorul care a validat |
| `_validated_at` | timestamp | Apps Script | |
| `_last_edit_at` | timestamp | Apps Script | Pentru flag „modified after validation” (formulă derivată) |

> Câmpurile `_*` rămân **strict în Sheet**: NU intră în spec public, NU se publică în JSON-LD.

## Permisiuni Sheet

- Toți editorii au edit access (Sheets nu suportă row-level perms native)
- Coloana `_status` parțial protejată (Data → Protect range):
  - **Editorii pot:** `draft → pending_review`, `validated → withdrawn`, `pending_review → withdrawn`
  - **Doar curatorii pot:** `pending_review → validated`, `pending_review → withdrawn` cu motiv, `withdrawn → orice`
  - Implementare: Apps Script `onEdit` validează tranziția; dacă editorul încearcă tranziție rezervată, anulează modificarea și afișează un avertisment
- Audit trail: Sheets edit history nativ
- Cultural norm: editorii nu modifică conținutul altor organizații; deviațiile sunt detectabile via history

## Imagini: convenția Drive

**Editorii NU urcă URL-uri direct.** Convenția:

1. Editor pune imaginea în Google Drive, setează **„Anyone with link can view”**
2. Editor copiază Drive file ID în coloana corespunzătoare:
   - `logo_drive_id` (Organisation)
   - `image_drive_id` (Member, Project) sau `cover_drive_id` (Event)
3. Apps Script convertește la sync: `<Drive ID>` → `https://drive.google.com/thumbnail?id=<ID>&sz=w1600`
4. Store-ul (D1) păstrează URL-ul rezultant
5. Spec vede `image` / `logo` ca URL standard (no Drive concept)

### De ce Drive ca storage v0.1
- Zero friction pentru editori (sunt deja în Drive)
- Permission model nativ Google
- Nu adaugă încă o piesă de infra (R2, S3 etc.)
- Easy migration path la R2 mirror în v0.2 (fără schimbarea workflow-ului editor)

### Limitări de știut
- Drive nu e CDN dedicat imaginilor - performance suboptim la scale (>100 imagini per page load)
- Format URL-uri Drive l-a schimbat Google de câteva ori istoric - risc de break la upgrade
- SEO suboptim - Drive nu e canonic friendly pentru content public

### Path de upgrade (v0.2+)
- Worker face mirror Drive → R2 la prima request
- D1 stochează atât Drive ID cât și R2 URL (preferă R2 când există)
- Editorul nu observă nicio schimbare - convenția Sheet rămâne aceeași
- Migrare gradual sau bulk, oricând

## Sync Apps Script → Worker

### Endpoint

```
POST https://api.{publisher.tld}/admin/sync
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "entity": "events",
  "rows": [ {...row1...}, {...row2...}, ... ]
}
```

### Sync model: full replace per entitate (recomandat v0.1)

- Apps Script trimite TOATE rândurile `validated` pentru o entitate într-un POST
- Worker: `BEGIN TRANSACTION; DELETE FROM events; INSERT ... ; COMMIT;`
- Simplu, idempotent, atomic
- Pierde audit history a inserts/updates în store, dar audit-ul real e în Sheet (history)
- Pentru un ecosistem cu 15-30 de organizații și aproximativ 200 de evenimente pe an e adecvat

Alternativă: **upsert differential** by ID (păstrează istorie internă, mai complex). Pentru v0.2 dacă apare nevoie reală.

### API Key management

- Generat o singură dată per publisher
- Stocat în Apps Script Properties Service: *Project Settings → Script Properties* → `API_KEY`
- Worker validează cheia + scope-ul (`/admin/sync` doar)
- Rotire: regenerare cheie + update în Properties; nicio downtime perceptibilă

## Notificări curator

| Trigger | Mecanism | Conținut |
|---|---|---|
| Editor click „Submit for review” | Email instant + opțional webhook (WhatsApp/Slack) | „Editor X a propus {entity}: {name}. Link la rând” |
| Erori publicare | Email + entry în `_publish_log` sheet | „Rând {id} ({entity}) a eșuat validarea: {error}” |
| Digest (opt-in) | Email zilnic | „N rânduri pending review > 24h” |

> Recomandare default: doar **„Submit for review”** (instant). Restul opt-in.

## Sheet `_publish_log`

Sheet adițional în același document, scris de Apps Script la fiecare publish:

| Coloană | Note |
|---|---|
| `timestamp` | Când a rulat publish-ul |
| `entity` | Entitatea sync-uită |
| `count_validated` | Câte rânduri în starea `validated` |
| `count_published` | Câte au trecut JSON Schema și au ajuns în store |
| `errors` | JSON cu rânduri eșuate (ID + mesaj eroare) |

Curatorul îl monitorizează ocazional pentru sanity check.
