# TechTable Standard v0.1: date despre un ecosistem urban

| | |
|---|---|
| **Status** | Draft |
| **Versiune** | v0.1 |
| **Data** | 2026-04-25 |
| **Revizuit** | 2026-11-24 (publicare, guvernanță) |
| **Licență** | CC0 1.0 (vezi [LICENSE](../LICENSE)) |
| **Namespace** | `https://standard.techtable.ro/v0.1/` |
| **Context JSON-LD** | [`context.jsonld`](context.jsonld) |

## 1. Introducere

### 1.1 Scop

Standardul definește o schemă comună pentru publicarea și interconectarea datelor despre **organizații, persoane, evenimente, proiecte și locații** ce alcătuiesc un ecosistem urban (tech, antreprenorial, civic, creativ). Obiectivul primar este **discovery**: un cetățean, profesionist sau organizație trebuie să poată descoperi ce există în ecosistem, indiferent de cine publică datele.

Standardul e **federat by design**: fiecare publisher (organizație, oraș, vehicul de coordonare) publică sub propriul namespace, iar interoperabilitatea se obține prin URI-uri stabile și vocabular comun.

### 1.2 Audiență

- **Implementatori**: dezvoltatori care construiesc publishing tools, validators, agregatori, agenți AI care consumă datele
- **Curatori per ecosistem**: persoane responsabile cu calitatea publicării sub un namespace; mediază între publisheri umani și format
- **Publisheri** *(indirect)*: organizații care publică date prin tooling care ascunde JSON-LD de utilizatorul final

### 1.3 Statut

**Draft, în validare publică.** v0.1 e prima versiune citibilă cap-coadă. Nu are încă o implementare de referință și nu a fost folosită în producție. Problemele cunoscute sunt în [issues](https://github.com/BanatIT/techtable-standard/issues). Schimbările până la v1.0 pot fi *breaking* fără preaviz.

### 1.4 Convenții

Cuvintele cheie *MUST*, *SHOULD*, *MAY* sunt interpretate conform [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## 2. Conformanță

### 2.1 Document conform

Un document este conform v0.1 dacă:

1. **Declară `@context`** care include URI-ul `https://standard.techtable.ro/v0.1/context.jsonld` (sau context echivalent compatibil).
2. **Declară `@type`** = `Organization`, `Person`, `Event`, `Project` sau `Place`.
3. **Conține un `@id`** unic și rezolvabil (URI HTTP/HTTPS).
4. **Trece validarea** JSON Schema corespunzătoare entității (vezi `schemas/`).
5. **Folosește vocabularul controlat** definit în §4 pentru câmpurile cu valori restrânse (`domain`, `status`).

### 2.2 Consumer conform

Un consumer este conform v0.1 dacă:

1. **Recunoaște și parsează** documentele celor 5 entități (chiar dacă ignoră câmpurile pe care nu le folosește).
2. **Rezolvă URI-urile** referențiate prin `@id` (cel puțin best-effort).
3. **Tratează absența câmpurilor opționale** ca lipsă de informație, nu ca eroare.
4. **Suportă forma compactă cu context** (deferarea expansion-ului e opțională).

### 2.3 Severități

- *Error*: document non-conform; consumer poate refuza să-l indexeze
- *Warning*: document conform dar incomplet; consumer indexează, validator semnalează curatorului

## 3. Modele de entități

Toate entitățile MUST avea `@id` (URI), `@type` și câmpurile marcate **req** mai jos.

### 3.1 Organisation (`@type: Organization`)

Reprezintă o organizație ca actor în ecosistem (companie, ONG, instituție publică, comunitate, universitate).

| Câmp | Tip | Card. | schema.org / ecosystem | Note |
|------|-----|-------|------------------------|------|
| `@id` | URI | **req** | - | URI stabil sub namespace-ul publisher-ului |
| `@type` | string | **req** | - | `Organization` |
| `name` | i18n string | **req** | `schema:name` | nume oficial |
| `description` | i18n string | opt | `schema:description` | |
| `url` | URI | opt | `schema:url` | website oficial |
| `logo` | URI | opt | `schema:logo` | URL imagine |
| `role` | i18n string | opt | `ecosystem:role` | rol în ecosistem (text liber) |
| `domain` | enum | **req** | `ecosystem:domain` | una din §4.1 |
| `tags` | string[] | opt | `schema:keywords` (alias pentru `tags`) | hashtag-uri libere |

### 3.2 Member (`@type: Person`)

Reprezintă o persoană asociată unei organizații. Nu există Member „liber” în v0.1 - orice Person publicat MUST avea `affiliation`.

| Câmp | Tip | Card. | schema.org / ecosystem | Note |
|------|-----|-------|------------------------|------|
| `@id` | URI | **req** | - | |
| `@type` | string | **req** | - | `Person` |
| `name` | string | **req** | `schema:name` | numele afișat (un singur limbaj - antroponim) |
| `affiliation` | object cu `@id` | **req** | `schema:affiliation` | referință la `Organization.@id` |
| `email` | email | opt | `schema:email` | |
| `sameAs` | URI[] | opt | `schema:sameAs` | LinkedIn, GitHub, etc. |
| `image` | URI | opt | `schema:image` | foto |
| `description` | i18n string | opt | `schema:description` | bio scurt |

> Member nu are `domain` propriu - moștenit tranzitiv din `affiliation`.

### 3.3 Event (`@type: Event`)

Reprezintă o întâlnire/activitate cu dată fixă (meetup, conferință, hackathon, workshop, etc.).

| Câmp | Tip | Card. | schema.org / ecosystem | Note |
|------|-----|-------|------------------------|------|
| `@id` | URI | **req** | - | |
| `@type` | string | **req** | - | `Event` |
| `name` | i18n string | **req** | `schema:name` | |
| `short` | i18n string | opt | `ecosystem:short` | rezumat one-liner |
| `description` | i18n string | opt | `schema:description` | |
| `organizer` | object cu `@id` | **req** | `schema:organizer` | referință la `Organization.@id` |
| `location` | object cu `@id` | **req** | `schema:location` | referință la `Place.@id` |
| `project` | object cu `@id` | opt | `ecosystem:project` | referință la `Project.@id` |
| `startDate` | xsd:dateTime sau xsd:date | **req** | `schema:startDate` | ISO 8601, cu sau fără timp |
| `endDate` | xsd:dateTime sau xsd:date | opt | `schema:endDate` | ISO 8601 |
| `domain` | enum | **req** | `ecosystem:domain` | |
| `tags` | string[] | opt | `schema:keywords` | |
| `category` | string | opt | `ecosystem:category` | meetup, conferință, hackathon, workshop, etc. |
| `eventStatus` | enum | opt | `schema:eventStatus` | `EventScheduled` (default) / `EventCancelled` / `EventPostponed` / `EventRescheduled` / `EventMovedOnline` |
| `url` | URI | opt | `schema:url` | pagina oficială a evenimentului |
| `image` | URI | opt | `schema:image` | cover |
| `maximumAttendeeCapacity` | int | opt | `schema:maximumAttendeeCapacity` | |
| `isAccessibleForFree` | boolean | opt | `schema:isAccessibleForFree` | true = liber, false = plătit |
| `ticketsUrl` | URI | opt | `ecosystem:ticketsUrl` | |
| `photosUrl` | URI | opt | `ecosystem:photosUrl` | |
| `performer` | object[] cu `@id` | opt | `schema:performer` | referințe la `Person.@id` |
| `speakersCount` | int | opt | `ecosystem:speakersCount` | |
| `realParticipants` | int | opt | `ecosystem:realParticipants` | raportat post-event |

### 3.4 Project (`@type: Project`)

Reprezintă o inițiativă cu durată (fără dată unică), care poate genera evenimente, livrabile sau alte tipuri de output.

| Câmp | Tip | Card. | schema.org / ecosystem | Note |
|------|-----|-------|------------------------|------|
| `@id` | URI | **req** | - | |
| `@type` | string | **req** | - | `Project` (custom; vezi §6.3) |
| `name` | i18n string | **req** | `schema:name` | |
| `description` | i18n string | opt | `schema:description` | |
| `leadOrganisation` | object cu `@id` | **req** | `ecosystem:leadOrganisation` | |
| `partners` | i18n string | opt | `ecosystem:partners` | text liber în v0.1; promovat la array de referințe în v0.2 |
| `domain` | enum | **req** | `ecosystem:domain` | |
| `tags` | string[] | opt | `schema:keywords` | |
| `status` | enum | **req** | `ecosystem:status` | una din §4.2 |
| `startDateOnly` | xsd:date | opt | `ecosystem:startDateOnly` | data de început (fără timp) |
| `endDateOnly` | xsd:date | opt | `ecosystem:endDateOnly` | |
| `url` | URI | opt | `schema:url` | |
| `image` | URI | opt | `schema:image` | cover |

> Termenii `startDateOnly`/`endDateOnly` sunt ecosystem-specific pentru a evita coliziunea cu semantica de eveniment a `schema:startDate` (care implică ora).

### 3.5 Location (`@type: Place`)

Reprezintă o locație fizică sau virtuală.

| Câmp | Tip | Card. | schema.org / ecosystem | Note |
|------|-----|-------|------------------------|------|
| `@id` | URI | **req** | - | |
| `@type` | string | **req** | - | `Place` |
| `name` | i18n string | **req** | `schema:name` | |
| `address` | i18n string | opt | `schema:address` | adresa principală |
| `addressLocality` | string | opt | `schema:addressLocality` | oraș |
| `addressCountry` | string (ISO 3166-1 alpha-2) | opt | `schema:addressCountry` | ex. `RO` |
| `geo` | object | opt | `schema:geo` | conține `latitude` + `longitude` |
| `isVirtual` | boolean | opt | `ecosystem:isVirtual` | default `false` |
| `url` | URI | opt | `schema:url` | pentru locații virtuale (Zoom, Meet, etc.) |

### 3.6 Relații între entități

```
Organisation ←─affiliation── Person
       ↑
       └─organizer─── Event ──location──→ Place
                        │
                        └─project (opt)──→ Project
                                              │
                                              └─leadOrganisation─→ Organisation
```

- `Event.organizer` și `Event.location` sunt **req**.
- `Event.project` e opt (un eveniment poate fi standalone sau parte dintr-un proiect).
- `Project.leadOrganisation` e **req**; multiple Org per Project se modelează în v0.1 prin câmpul liber `partners`.

## 4. Vocabular controlat

### 4.1 `domain` enum

Aplicabil pe Organisation, Event, Project. Valori v0.1:

| Valoare | URI | Descriere |
|---------|-----|-----------|
| `tech` | `https://standard.techtable.ro/v0.1/tech` | Tehnologie inovativă (IT, software, hardware, telecom, automotive tech, R&D) |
| `entrepreneurial` | `https://standard.techtable.ro/v0.1/entrepreneurial` | Antreprenoriat și inovație de business (startup, accelerare, investiții, scaling) |
| `civic` | `https://standard.techtable.ro/v0.1/civic` | Implicare civică, governance, transparență, date deschise, advocacy |
| `creative` | `https://standard.techtable.ro/v0.1/creative` | Industrii creative (design, gaming, media, content, arte aplicate) |

Extensiile vocabularului se discută în procesul de governance (vezi §10).

### 4.2 `status` enum (Project)

| Valoare | URI | Descriere |
|---------|-----|-----------|
| `planning` | `https://standard.techtable.ro/v0.1/planning` | Definire scope, încă nu a început execuția |
| `active` | `https://standard.techtable.ro/v0.1/active` | În execuție |
| `completed` | `https://standard.techtable.ro/v0.1/completed` | Finalizat |
| `paused` | `https://standard.techtable.ro/v0.1/paused` | Suspendat temporar (poate fi reactivat) |

## 5. i18n

### 5.1 Câmpuri multilinguale

Următoarele câmpuri acceptă mai multe limbi:
`name` (Organisation, Event, Project, Location), `description`, `address`, `role`, `short`, `partners`.

`Person.name` este **monolingual** (antroponim - nu se traduce).

### 5.2 Forme acceptate

(a) **String simplu**: limba este cea implicită, declarată prin `@language` la nivel de document:

```json
{
  "@language": "ro",
  "name": "Atelier de tehnologii emergente"
}
```

(b) **Language map**: pentru valori multilinguale paralele:

```json
{
  "name": {
    "ro": "Atelier de tehnologii emergente",
    "en": "Emerging tech workshop"
  }
}
```

Documentele care **NU** declară `@language` la nivel de document MUST folosi forma (b) pentru câmpurile multilinguale.

### 5.3 Coduri de limbă

[BCP 47](https://www.rfc-editor.org/rfc/bcp47) (ex. `ro`, `en`, `hu`, `de`, `ro-RO`).

### 5.4 Default language pentru standardul TechTable

`ro` (limba de adopție inițială). Alți publisheri MAY seta default propriu.

## 6. Format & serializare

### 6.0 Storage independence

Spec-ul specifică **forma JSON-LD a output-ului**, nu cum se stochează datele intern la publisher. Un publisher poate ține datele în:

- **Static files** publicate la `@id` URIs
- **Database** (D1, Postgres, etc.) cu API care materializează JSON-LD la request
- **Mixed** (cache de fișiere statice peste DB)

Toate sunt conforme cât timp:
- `@id` URIs sunt rezolvabile (HTTP 200)
- Răspunsul e JSON-LD canonical conform §6.1
- Forma lite e disponibilă opțional via `?view=lite` conform §6.2

Recomandarea pentru implementări noi: DB-backed (permite search, filter, query dinamic - vezi `publisher-operations.md` pentru pattern Sheet → Worker → D1).

### 6.1 JSON-LD canonical (forma autoritativă)

Documentele MUST fi serializate în [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) și MUST referenția contextul standardului:

```json
{
  "@context": [
    "https://schema.org",
    "https://standard.techtable.ro/v0.1/context.jsonld"
  ],
  "@type": "Event",
  "@id": "...",
  ...
}
```

### 6.2 Lite view (proiecție pentru consumatori non-semantici)

Consumatorii care nu lucrează cu JSON-LD pot solicita o **lite view**: același document fără câmpurile JSON-LD specifice (`@context`, `@id`, `@type` păstrate ca `id`, `type`):

```
GET /events/jsmeetup-100              → JSON-LD canonical
GET /events/jsmeetup-100?view=lite    → JSON simplificat
```

Lite view e o **proiecție automată** din canonical. Single source of truth = canonical. Lite view NU e specificat formal în v0.1 - fiecare publisher îl generează, recomandarea e:
- Înlocuire `@id` → `id`, `@type` → `type`
- Eliminare `@context`
- Aplatizare obiectelor cu un singur `@id` la string-ul URI direct

### 6.3 Mapping schema.org

| Entitate v0.1 | schema.org type | Note |
|---------------|-----------------|------|
| Organisation | `schema:Organization` | direct |
| Member | `schema:Person` | cu `affiliation` |
| Event | `schema:Event` | direct |
| Place | `schema:Place` | direct |
| Project | `ecosystem:Project` | tip nou (schema.org nu are echivalent semantic exact: `CreativeWork` e prea narrow, `Action` e prea proces-focused) |

## 7. URI scheme

### 7.1 Namespace standard

Toți identificatorii standardului (tipuri custom, termeni, valori enum) folosesc namespace-ul:

```
https://standard.techtable.ro/v0.1/
```

URI-urile MUST fi rezolvabile (HTTP 200 sau redirect 3xx). Standardul în sine, contextul și schemele sunt servite sub acest namespace.

### 7.2 Namespace publishers

Fiecare publisher folosește propriul domeniu pentru URI-urile entităților publicate. Convenție recomandată:

```
https://{publisher.tld}/orgs/{slug}
https://{publisher.tld}/members/{slug}
https://{publisher.tld}/events/{slug}
https://{publisher.tld}/projects/{slug}
https://{publisher.tld}/locations/{slug}
```

`{slug}` MUST corespunde pattern-ului `^[a-z0-9-]+$`, max 64 caractere.

### 7.3 Federation prin `@id`

Două documente publicate de publisheri diferiți care declară același `@id` descriu aceeași entitate. Publisherii sunt responsabili cu unicitatea în propriul namespace; coliziunile cross-publisher trebuie rezolvate prin acord între publisheri (de regulă, unul cedează URI-ul, sau ambii adaugă `sameAs` reciproc).

## 8. Validare

### 8.1 JSON Schema per entitate

Validarea structurală se face cu [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/release-notes) per entitate. Schemele sunt în `schemas/`:

- [`schemas/organisation.schema.json`](schemas/organisation.schema.json)
- [`schemas/member.schema.json`](schemas/member.schema.json)
- [`schemas/event.schema.json`](schemas/event.schema.json)
- [`schemas/project.schema.json`](schemas/project.schema.json)
- [`schemas/location.schema.json`](schemas/location.schema.json)

### 8.2 Errors vs warnings

| Severitate | Trigger | Comportament consumer |
|------------|---------|------------------------|
| **Error** | Lipsa unui câmp `req`, `@type` necunoscut, valoare în afara enum-ului, format URI/email/date invalid | Document e non-conform; refuz indexare |
| **Warning** | Câmp `opt` necompletat, `description` lipsă, lipsa coordonatelor `geo` pe Location fizic | Document e conform; indexare cu calitate redusă; semnalat curatorului |

Consumer-ii MAY genera warnings adiționale specific business-ului lor.

## 9. Versioning

### 9.1 Politică milestone-only

Versiunile se identifică prin milestones simple: `v0.1`, `v0.2`, ..., `v1.0`. Nu se folosește SemVer cu patch până la stabilizarea v1.0.

### 9.2 Forward compatibility

Un consumer v0.x trebuie să poată parsa documente v0.y unde `y < x`, **prin încărcarea contextului versiunii documentului**. `@context` rezolvă la versiunea documentului, deci consumer v0.2 încarcă `https://standard.techtable.ro/v0.1/context.jsonld` când întâlnește document v0.1.

Schimbările breaking între versiuni MUST fi documentate în [CHANGELOG](../CHANGELOG.md).

## 10. Governance

### 10.1 Cum se schimbă standardul

Propunerile de modificare se fac prin issue sau pull request în [repository-ul standardului](https://github.com/BanatIT/techtable-standard). Nimeni nu scrie direct în `main`: orice schimbare trece prin pull request, cu review. Pașii sunt în [CONTRIBUTING](../CONTRIBUTING.md). O propunere conține:
- Motivația (ce caz nu poate fi modelat în versiunea curentă)
- Modificarea propusă (la nivel de schema, vocabular, format)
- Impactul asupra compatibilității

### 10.2 Grupul de curatori

Evoluția standardului o decide **grupul de curatori**. Din grup face parte câte un reprezentant al fiecărei organizații care publică date conform standardului (curatorul ei, vezi glosarul) sau care le folosește într-un produs. O organizație are un singur vot, indiferent câți oameni participă la discuții.

- O organizație intră în grup printr-un issue în care arată ce publică sau ce folosește. Grupul existent confirmă prin consens.
- Decizia se ia prin **consens**, în discuția publică din issue sau pull request.
- Dacă după două runde de discuție, în cel mult 30 de zile, nu există consens, grupul votează. Decide majoritatea simplă.
- Nicio organizație nu are drept de decizie separat. Banat IT facilitează procesul (ține repository-ul, convoacă discuțiile), cu un singur vot, ca oricare alt membru.
- **Regulă tranzitorie:** până când grupul are cel puțin 3 organizații confirmate, cei care întrețin repository-ul (lista este în [`CODEOWNERS`](../.github/CODEOWNERS)) integrează schimbările pe baza discuției publice și notează decizia în [`docs/decizii.md`](../docs/decizii.md).

### 10.3 Frecvență iterații

- **Iterație majoră**: o dată pe an, în Q4 (după evaluarea anuală a ecosistemelor active)
- **Corecturi non-breaking**: ad-hoc, fără calendar fix

> **Notă:** Modelul de guvernanță e *tranzitoriu* și se reformalizează când cel puțin 2 ecosisteme publică date conform standardului (vezi D011 și D015 în [`docs/decizii.md`](../docs/decizii.md)).

## 11. Glosar

| Termen | Definiție |
|--------|-----------|
| **Publisher** | Organizație sau vehicul de coordonare care publică date despre propriul ecosistem (ex: o comunitate tech, o fundație, un oraș) |
| **Curator** | Persoană sau echipă responsabilă cu calitatea publicării sub un namespace de publisher; mediază între publisheri umani și format |
| **Consumer** | Sistem care citește și utilizează datele publicate (agregator, agent AI, dashboard, motor de discovery) |
| **Canonical** | Forma autoritativă a unui document, în JSON-LD complet |
| **Lite view** | Proiecție simplificată din canonical, JSON plain pentru consumatori non-semantici |
| **Federation** | Capacitatea ca documente publicate de surse diferite să se poată referi unele la altele prin URI-uri stabile, fără coordonare centrală |
| **Document conform** | Document care satisface §2.1 |
| **Grupul de curatori** | Grupul care decide evoluția standardului: câte un reprezentant al fiecărei organizații care publică sau folosește date în format (vezi §10.2) |

## 12. Operații publisher

Workflow editor → curator → publicare, sync Sheet → store, convenții imagini Drive, sheet operațional cu coloane `_*`: vezi [`publisher-operations.md`](publisher-operations.md). Acest doc nu face parte din spec (e operațional, nu standard), dar e recomandare puternică pentru orice publisher care folosește Google Sheets ca sursă editorială.

## Anexa A: Exemple

Exemple complete pentru fiecare entitate, în ambele forme (canonical JSON-LD + lite view):

- Organisation: [`examples/organisation.canonical.json`](examples/organisation.canonical.json) · [`examples/organisation.lite.json`](examples/organisation.lite.json)
- Member: [`examples/member.canonical.json`](examples/member.canonical.json) · [`examples/member.lite.json`](examples/member.lite.json)
- Event: [`examples/event.canonical.json`](examples/event.canonical.json) · [`examples/event.lite.json`](examples/event.lite.json)
- Project: [`examples/project.canonical.json`](examples/project.canonical.json) · [`examples/project.lite.json`](examples/project.lite.json)
- Location: [`examples/location.canonical.json`](examples/location.canonical.json) · [`examples/location.lite.json`](examples/location.lite.json)

Toate exemplele folosesc date **fictive** (`publisher.example`, „Banat Innovation Hub”, „Ada Petrescu” etc.) pentru a evita probleme GDPR și pentru a rămâne stabile peste timp.

## Anexa B: Sheet template

Pentru publisheri care preferă să-și mențină datele într-un Google Sheet (sau Excel) și să folosească tooling pentru conversia automată în JSON-LD canonical: [`sheet-template.md`](sheet-template.md) descrie structura recomandată și mapping-ul către câmpurile de mai sus.
