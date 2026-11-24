# TechTable Standard: Strategic Tier v0.1

| | |
|---|---|
| **Status** | Draft |
| **Versiune** | v0.1-strategic |
| **Data** | 2026-04-26 |
| **Tier** | Strategic (extensie peste core) |
| **Compatibilitate core** | v0.1 |
| **Licență** | CC0 1.0 (vezi [LICENSE](../LICENSE)) |
| **Namespace** | `https://standard.techtable.ro/v0.1-strategic/` |
| **Context JSON-LD** | [`context.jsonld`](context.jsonld) |

## 1. Introducere

### 1.1 Scop

Strategic tier definește schema pentru documentarea **coordonării strategice a unui ecosistem urban**: entitatea `Ecosystem` în sine + cele 4 artefacte recurente ale ciclului anual de coordonare (`SWOT`, `Priorities`, `KPIs`, `Maturity`).

[Tier-ul core](../v0.1/spec.md) răspunde la întrebarea *„ce există în ecosistem?”*. Strategic tier răspunde la *„cum se coordonează ecosistemul în sine, ce-și propune, cum se evaluează?”*.

### 1.2 Audiență

- **Curatori de ecosistem**: persoane responsabile cu documentarea coordonării strategice a unui ecosistem (de regulă din organizația-facilitator)
- **Consumatori analitici**: agregatori, dashboards, agenți AI care răspund la întrebări de tipul *„care sunt prioritățile 2026 în tech vs. civic în Timișoara”*
- **Implementatori**: dezvoltatori care extind tooling-ul standardului pentru strategic tier

### 1.3 Statut

**Draft, în validare publică**, împreună cu core. A pornit de la artefactele reale ale unui ciclu anual de coordonare (SWOT, priorități, KPIs, maturitate) din ecosistemul tech din Timișoara. Schimbările până la v1.0-strategic pot fi *breaking* fără preaviz.

### 1.4 Convenții

Cuvintele cheie *MUST*, *SHOULD*, *MAY* sunt interpretate conform [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).

## 2. Conformanță

### 2.1 Document conform

Un document e conform v0.1-strategic dacă:

1. **Declară `@context`** care include URI-ul `https://standard.techtable.ro/v0.1-strategic/context.jsonld`. Dacă documentul referențiază entități core, MUST include și `https://standard.techtable.ro/v0.1/context.jsonld`.
2. **Declară `@type`** = `Ecosystem`, `SWOT`, `Priorities`, `KPIs` sau `Maturity`.
3. **Conține un `@id`** unic și rezolvabil (URI HTTP/HTTPS).
4. **Trece validarea** JSON Schema corespunzătoare (vezi [`schemas/`](schemas/)).
5. **Folosește vocabularul controlat** definit în §4.
6. **Referențiază entități core valide** prin `@id`. Strategic tier nu redefinește entități core - le folosește prin URI.

### 2.2 Compatibilitate core

Strategic v0.1 e compatibil cu **core v0.1**. Documentele strategic referențiază (`@id`) entități core publicate sub schema [`../v0.1/spec.md`](../v0.1/spec.md). În particular:

- `Ecosystem.facilitator` → `Organization` core
- `Ecosystem.member` → `Organization` core
- `Priorities.items[].relatedProjects` → `Project` core

### 2.3 Consumer conform

Un consumer e conform v0.1-strategic dacă:

1. **Recunoaște și parsează** documentele celor 5 entități strategice.
2. **Rezolvă URI-urile core** referențiate (best-effort).
3. **Tratează absența câmpurilor opționale** ca lipsă de informație, nu ca eroare.
4. **NU forțează** ca un Ecosystem să aibă SWOT/Priorities/KPIs/Maturity asociate - fiecare e independent publicabilă.

### 2.4 Severități

- *Error*: document non-conform; consumer poate refuza să-l indexeze
- *Warning*: document conform dar incomplet; consumer indexează, validator semnalează curatorului

## 3. Modele de entități

Toate entitățile MUST avea `@id` (URI), `@type` și câmpurile marcate **req**.

### 3.1 Ecosystem (`@type: Ecosystem`)

Reprezintă mecanismul de coordonare în sine - o federație, masă rotundă, cluster, sau alt vehicul prin care un grup de organizații se coordonează strategic.

| Câmp | Tip | Card. | URI semantic | Note |
|------|-----|-------|--------------|------|
| `@id` | URI | **req** | - | URI stabil sub namespace publisher |
| `@type` | string | **req** | - | `Ecosystem` |
| `name` | i18n string | **req** | `schema:name` | nume oficial (ex. „TechTable”) |
| `description` | i18n string | opt | `schema:description` | |
| `domain` | enum (core) | **req** | `core:domain` | una din §4.1 (reuse din core) |
| `facilitator` | object cu `@id` | **req** | `strategic:facilitator` | referință la `Organization.@id` (core): org-ul coordonator |
| `member` | object[] cu `@id` | opt | `schema:member` | referințe la `Organization.@id` (core): org-uri membre |
| `addressLocality` | string | opt | `schema:addressLocality` | oraș principal (ex. „Timișoara”) |
| `addressRegion` | string | opt | `schema:addressRegion` | regiune (ex. „Vest”, „Banat”) |
| `addressCountry` | string (ISO 3166-1 alpha-2) | opt | `schema:addressCountry` | ex. `RO` |
| `url` | URI | opt | `schema:url` | website ecosistem |
| `logo` | URI | opt | `schema:logo` | URL imagine |
| `tags` | string[] | opt | `schema:keywords` | hashtag-uri libere |
| `currentMaturity` | object cu `@id` | opt | `strategic:currentMaturity` | pointer denormalizat la `Maturity.@id` curent (vezi D-S006) |

### 3.2 SWOT (`@type: SWOT`)

Snapshot anual al analizei Strengths/Weaknesses/Opportunities/Threats pentru un ecosistem. Tipic produs în Q4 (cycle methodology).

| Câmp | Tip | Card. | URI semantic | Note |
|------|-----|-------|--------------|------|
| `@id` | URI | **req** | - | recomandat: `{base}/swot/{ecosystem-slug}-{year}` |
| `@type` | string | **req** | - | `SWOT` |
| `inEcosystem` | object cu `@id` | **req** | `strategic:inEcosystem` | referință la `Ecosystem.@id` |
| `year` | int | **req** | `strategic:year` | anul calendaristic la care se referă |
| `dateAssessed` | xsd:date | opt | `strategic:dateAssessed` | data efectivă a sesiunii de SWOT |
| `strengths` | i18n string[] | opt | `strategic:strengths` | array de bullets |
| `weaknesses` | i18n string[] | opt | `strategic:weaknesses` | |
| `opportunities` | i18n string[] | opt | `strategic:opportunities` | |
| `threats` | i18n string[] | opt | `strategic:threats` | |
| `notes` | i18n string | opt | `strategic:notes` | observații libere |

> **Constraint conform:** un SWOT MUST avea cel puțin una dintre `strengths`, `weaknesses`, `opportunities`, `threats` cu cel puțin un item. Validatorul respinge SWOT complet gol.

### 3.3 Priorities (`@type: Priorities`)

Setul de priorități strategice ale unui ecosistem pentru un an. Tipic produs în Q1 (cycle methodology).

| Câmp | Tip | Card. | URI semantic | Note |
|------|-----|-------|--------------|------|
| `@id` | URI | **req** | - | recomandat: `{base}/priorities/{ecosystem-slug}-{year}` |
| `@type` | string | **req** | - | `Priorities` |
| `inEcosystem` | object cu `@id` | **req** | `strategic:inEcosystem` | |
| `year` | int | **req** | `strategic:year` | |
| `dateAssessed` | xsd:date | opt | `strategic:dateAssessed` | data finalizării priorităților |
| `items` | object[] | **req** (min 1) | `strategic:items` | array de Priority items (vezi §3.3.1) |
| `notes` | i18n string | opt | `strategic:notes` | |

#### 3.3.1 Priority item (sub-obiect în `items[]`)

| Câmp | Tip | Card. | Note |
|------|-----|-------|------|
| `name` | i18n string | **req** | titlul priorității |
| `description` | i18n string | opt | detalii |
| `successMetric` | i18n string | opt | criteriu de succes (text liber, target inline) |
| `relatedProjects` | object[] cu `@id` | opt | referințe la `Project.@id` (core) care implementează prioritatea |

### 3.4 KPIs (`@type: KPIs`)

Indicatori de performanță pentru un ecosistem într-un an, organizați după formula din [metodologie](../docs/metodologie.md).

| Câmp | Tip | Card. | URI semantic | Note |
|------|-----|-------|--------------|------|
| `@id` | URI | **req** | - | recomandat: `{base}/kpis/{ecosystem-slug}-{year}` |
| `@type` | string | **req** | - | `KPIs` |
| `inEcosystem` | object cu `@id` | **req** | `strategic:inEcosystem` | |
| `year` | int | **req** | `strategic:year` | |
| `dateAssessed` | xsd:date | opt | `strategic:dateAssessed` | data ultimei revizuiri |
| `capacity` | i18n string[] | opt | `strategic:capacity` | „ce avem” - bullets |
| `strategicActions` | i18n string[] | opt | `strategic:strategicActions` | „ce facem” - bullets |
| `resultImpact` | i18n string[] | opt | `strategic:resultImpact` | „ce obținem” - bullets |
| `notes` | i18n string | opt | `strategic:notes` | |

> **Constraint conform:** un KPIs MUST avea cel puțin una dintre `capacity`, `strategicActions`, `resultImpact` cu cel puțin un item.

### 3.5 Maturity (`@type: Maturity`)

Auto-evaluare a maturității ecosistemului pe scala 5-level la un punct în timp.

| Câmp | Tip | Card. | URI semantic | Note |
|------|-----|-------|--------------|------|
| `@id` | URI | **req** | - | recomandat: `{base}/maturity/{ecosystem-slug}-{year}` |
| `@type` | string | **req** | - | `Maturity` |
| `inEcosystem` | object cu `@id` | **req** | `strategic:inEcosystem` | |
| `dateAssessed` | xsd:date | **req** | `strategic:dateAssessed` | data evaluării |
| `level` | int 1..5 | **req** | `strategic:level` | numărul nivelului |
| `levelName` | enum | **req** | `strategic:levelName` | una din §4.1 |
| `model` | URI | opt | `strategic:model` | model de maturitate folosit; implicit, modelul din §4.1, identificat prin `https://standard.techtable.ro/v0.1-strategic/maturity-model` |
| `notes` | i18n string | opt | `strategic:notes` | observații, justificare nivel |

> **Constraint conform:** `level` și `levelName` MUST fi consistente: `1↔inexistent`, `2↔incipient`, `3↔intentional`, `4↔integrated`, `5↔inspirational`.

### 3.6 Relații între entități

```
Ecosystem ──facilitator──→ Organization (core)
   │
   ├──member──────────────→ Organization[] (core)
   │
   └──currentMaturity ────→ Maturity
                              │
                              └──inEcosystem──┐
                                              │
   ┌──inEcosystem─── SWOT ─────────────────────┤
   │                                           │
   ├──inEcosystem─── Priorities ──items[]──┐  │
   │                                       │  │
   │                                       └─→ Project (core) [opt]
   │                                           │
   └──inEcosystem─── KPIs ─────────────────────┘
```

- Toate entitățile non-Ecosystem au `inEcosystem` **req** (FK către Ecosystem).
- Strategic FK-uri către core: `facilitator`, `member`, `relatedProjects`. Toate sunt referințe `@id`, niciodată embedded objects.
- Core nu are FK către strategic. NICIODATĂ.

## 4. Vocabular controlat

### 4.1 `levelName` enum (Maturity)

| Valoare | URI | Level # | Descriere |
|---------|-----|---------|-----------|
| `inexistent` | `https://standard.techtable.ro/v0.1-strategic/inexistent` | 1 | Niciun mecanism de coordonare; org-uri lucrează izolat |
| `incipient` | `https://standard.techtable.ro/v0.1-strategic/incipient` | 2 | Mecanism informal/emergent; întâlniri ad-hoc, conștientizare comună |
| `intentional` | `https://standard.techtable.ro/v0.1-strategic/intentional` | 3 | Coordonare cu cycle anual, output-uri agreate, măsurători de bază |
| `integrated` | `https://standard.techtable.ro/v0.1-strategic/integrated` | 4 | Strategie cross-ecosistem, infrastructură comună, raportare publică |
| `inspirational` | `https://standard.techtable.ro/v0.1-strategic/inspirational` | 5 | Reference model pentru alte ecosisteme; impact replicabil |

### 4.2 `domain` enum (reuse din core)

`Ecosystem.domain` folosește același enum din [core spec §4.1](../v0.1/spec.md#41-domain-enum):
- `tech`
- `entrepreneurial`
- `civic`
- `creative`

Vocabularul controlat e gestionat în core. Strategic nu adaugă valori.

## 5. i18n

Strategic tier folosește **același mecanism i18n ca core** (vezi [core spec §5](../v0.1/spec.md#5-i18n)):

- Două forme acceptate: string simplu (cu `@language` document-level) sau language map.
- Coduri de limbă: BCP 47.
- Default `ro` pentru standardul TechTable.

**Câmpuri multilinguale strategic:**

| Entitate | Câmpuri i18n |
|----------|--------------|
| Ecosystem | `name`, `description` |
| SWOT | items din `strengths` / `weaknesses` / `opportunities` / `threats`, `notes` |
| Priorities | `notes`, items din `items[]`: `name`, `description`, `successMetric` |
| KPIs | items din `capacity` / `strategicActions` / `resultImpact`, `notes` |
| Maturity | `notes` |

**Antroponime:** strategic nu conține antroponime. Câmpurile de tip persoană se află doar în core (`Person.name`: monolingual).

## 6. Format & serializare

### 6.1 JSON-LD canonical

Identic cu core (vezi [core spec §6.1](../v0.1/spec.md#61-json-ld-canonical-forma-autoritativă)). Documentele MUST referenția contextul strategic-ului:

```json
{
  "@context": [
    "https://schema.org",
    "https://standard.techtable.ro/v0.1/context.jsonld",
    "https://standard.techtable.ro/v0.1-strategic/context.jsonld"
  ],
  "@type": "SWOT",
  "@id": "...",
  ...
}
```

> **Notă:** referențierea contextului core (`v0.1/context.jsonld`) e necesară doar dacă documentul folosește terms din core (de regulă: oricând există FK către core). În practică, toate documentele strategic referențiază entități core, deci ambele context-uri SHOULD fi incluse.

### 6.2 Lite view

Identic cu core: `?view=lite` returnează formă simplificată cu `id`/`type` în loc de `@id`/`@type`, fără `@context`. Single source of truth = canonical.

### 6.3 Mapping schema.org

| Entitate strategic | schema.org type | Note |
|--------------------|-----------------|------|
| Ecosystem | `strategic:Ecosystem` (custom) | tip nou - vezi D-S002 |
| SWOT | `strategic:SWOT` (custom) | nu există echivalent schema.org |
| Priorities | `strategic:Priorities` (custom) | nu există echivalent schema.org |
| KPIs | `strategic:KPIs` (custom) | nu există echivalent schema.org |
| Maturity | `strategic:Maturity` (custom) | nu există echivalent schema.org |

Toate entitățile strategice sunt custom - schema.org nu modelează coordonare strategică de ecosistem. Câmpurile reuse schema.org unde e posibil (`name`, `description`, `member`, `address*`).

## 7. URI scheme

### 7.1 Namespace standard

```
https://standard.techtable.ro/v0.1-strategic/
```

URI-urile MUST fi rezolvabile (HTTP 200 sau redirect 3xx). Standardul în sine, contextul, schemele și modelul de maturitate sunt servite sub acest namespace.

### 7.2 Namespace publishers

Convenție recomandată pentru fiecare publisher:

```
https://{publisher.tld}/ecosystems/{slug}
https://{publisher.tld}/swot/{ecosystem-slug}-{year}
https://{publisher.tld}/priorities/{ecosystem-slug}-{year}
https://{publisher.tld}/kpis/{ecosystem-slug}-{year}
https://{publisher.tld}/maturity/{ecosystem-slug}-{year}
```

Reguli slug:
- `{slug}` MUST corespunde pattern-ului `^[a-z0-9-]+$`, max 64 caractere (consistent cu [core §7.2](../v0.1/spec.md#72-namespace-publishers)).
- Pentru artefactele anuale (SWOT/Priorities/KPIs/Maturity), recomandare: combinare `{ecosystem-slug}-{year}` (ex. `techtable-2026`).

### 7.3 Cross-ecosystem & federation

Un publisher care găzduiește mai multe ecosisteme (ex. portalul unui oraș care publică pentru tech, antreprenorial, civic și creativ) folosește slug-uri de ecosistem distincte:

```
https://oras.example/ecosystems/tech
https://oras.example/ecosystems/antreprenorial
https://oras.example/swot/tech-2026
https://oras.example/swot/antreprenorial-2026
```

Două documente strategic publicate de publisheri diferiți care declară același `@id` descriu aceeași entitate. Vezi [core §7.3](../v0.1/spec.md#73-federation-prin-id).

## 8. Validare

### 8.1 JSON Schema per entitate

Validarea structurală se face cu [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/release-notes), per entitate. Schemele sunt în [`schemas/`](schemas/):

- [`schemas/ecosystem.schema.json`](schemas/ecosystem.schema.json)
- [`schemas/swot.schema.json`](schemas/swot.schema.json)
- [`schemas/priorities.schema.json`](schemas/priorities.schema.json)
- [`schemas/kpis.schema.json`](schemas/kpis.schema.json)
- [`schemas/maturity.schema.json`](schemas/maturity.schema.json)

### 8.2 Validări cross-entity

Următoarele constrângeri NU sunt exprimabile complet în JSON Schema (necesită SHACL sau validator custom). Sunt definite ca **warnings** la nivel de tooling:

- `Ecosystem.currentMaturity` SHOULD pointer la cea mai recentă Maturity cu `inEcosystem = Ecosystem.@id`.
- `Maturity.level ↔ levelName` consistency - verificat de schema cu `oneOf`.
- `Priorities.items[].relatedProjects[].@id` SHOULD fi rezolvabilă la un Project core valid (warning dacă nu).

### 8.3 Errors vs warnings

| Severitate | Trigger | Comportament consumer |
|------------|---------|------------------------|
| **Error** | Lipsa câmp `req`, `@type` necunoscut, valoare în afara enum-ului, format URI/date invalid, `level/levelName` inconsistent, SWOT/KPIs complet gol | Document non-conform; refuz indexare |
| **Warning** | Câmp `opt` necompletat, `currentMaturity` lipsă pe Ecosystem, FK către Project core nerezolvabil | Conform; indexare; semnalat curatorului |

## 9. Versioning

### 9.1 Politică

Strategic tier folosește versioning paralel cu core, **nu cuplat**:

- `v0.1-strategic` (acest document)
- Iterații viitoare: `v0.2-strategic`, ..., `v1.0-strategic`

Vezi [D-S007 în README.md](README.md#d-s007-2026-04-26-versioning-paralel-cu-core-nu-cuplat) pentru motivație.

### 9.2 Compatibilitate cu core

Fiecare versiune strategic declară explicit cu ce versiune(i) core e compatibilă (în §1 antet).

| Strategic | Core compatibil |
|-----------|------------------|
| v0.1-strategic | v0.1 |

Dacă core ajunge la v0.2 cu schimbări breaking pe entitățile referențiate (Organization, Project), strategic emite errata pe versiunea curentă SAU release nou (v0.2-strategic) actualizat.

### 9.3 Forward compatibility

Identic cu core (vezi [core §9.2](../v0.1/spec.md#92-forward-compatibility)): consumer încarcă contextul versiunii declarată în document.

## 10. Governance

Strategic tier folosește **același proces de governance ca core** (vezi [core spec §10](../v0.1/spec.md#10-governance)). Grupul de curatori e același: nivelul strategic nu are un grup separat.

Modificări la spec strategic se fac prin issue/PR în același repository cu core, cu label `tier:strategic`.

## 11. Glosar

| Termen | Definiție |
|--------|-----------|
| **Strategic tier** | Extensie a standardului TechTable care modelează coordonarea strategică a unui ecosistem (Ecosystem, SWOT, Priorities, KPIs, Maturity) |
| **Core tier** | Setul de 5 entități baseline (Organisation, Member, Event, Project, Location): vezi [core spec](../v0.1/spec.md) |
| **Ecosystem** | Mecanism de coordonare formală/semi-formală a unui grup de organizații cu scop comun (federație, masă rotundă, cluster) |
| **Curator de ecosistem** | Persoană sau echipă care ține la zi documentația strategică a ecosistemului |
| **Compound PK** | Cheie primară compusă din `(inEcosystem, year)` (sau `dateAssessed` pentru Maturity): pattern pentru entitățile strategice anuale |
| **Maturity model** | Scala 5-level (Inexistent → Inspirational) folosită pentru auto-evaluarea ecosistemelor |
| **Adoption pathway** | Ordinea recomandată de adopție a entităților strategic (Ecosystem → SWOT/Maturity → Priorities → KPIs): vezi [README §4](README.md#4-adoption-pathway) |

## Anexa A: Exemple

Exemple complete pentru fiecare entitate strategic, în ambele forme (canonical JSON-LD + lite view):

- Ecosystem: [`examples/ecosystem.canonical.json`](examples/ecosystem.canonical.json) · [`examples/ecosystem.lite.json`](examples/ecosystem.lite.json)
- SWOT: [`examples/swot.canonical.json`](examples/swot.canonical.json) · [`examples/swot.lite.json`](examples/swot.lite.json)
- Priorities: [`examples/priorities.canonical.json`](examples/priorities.canonical.json) · [`examples/priorities.lite.json`](examples/priorities.lite.json)
- KPIs: [`examples/kpis.canonical.json`](examples/kpis.canonical.json) · [`examples/kpis.lite.json`](examples/kpis.lite.json)
- Maturity: [`examples/maturity.canonical.json`](examples/maturity.canonical.json) · [`examples/maturity.lite.json`](examples/maturity.lite.json)

Toate exemplele folosesc date **fictive** (`publisher.example`, „Innov West”) pentru consistență cu pattern-ul din core și pentru a evita probleme GDPR.

## Anexa B: Sheet template

Pentru publisheri care preferă să-și mențină datele strategice într-un Google Sheet (sau Excel) și să folosească tooling pentru conversia automată în JSON-LD canonical: [`sheet-template.md`](sheet-template.md) descrie structura recomandată și mapping-ul către câmpurile de mai sus.
