# TechTable Standard: Strategic Tier v0.1, note de design

Note de design pentru extensia **strategic tier** a standardului TechTable. Acest tier descrie **cum își documentează un ecosistem propria coordonare strategică** (entitatea Ecosystem însăși + SWOT, Priorities, KPIs, Maturity).

> Pentru core-ul standardului (Organisation, Member, Event, Project, Location), vezi [`../v0.1/spec.md`](../v0.1/spec.md) și [`../docs/decizii.md`](../docs/decizii.md).

| | |
|---|---|
| **Status** | Draft |
| **Versiune** | v0.1-strategic |
| **Data** | 2026-04-26 |
| **Tier** | Strategic (extensie opt-in peste core v0.1) |
| **Spec formală** | [`spec.md`](spec.md) |
| **Namespace** | `https://standard.techtable.ro/v0.1-strategic/` |

## 1. De ce un tier separat

Standardul core (Organisation/Member/Event/Project/Location) are un singur scop: **discovery**. Funcționează la orice nivel de maturitate al unui ecosistem - chiar și un publisher solitar (o singură organizație care publică câteva evenimente) îl poate adopta cu beneficiu imediat.

Strategic tier-ul există într-un alt strat de realitate: **coordonarea conștientă a unui ecosistem**. Entitățile sale (Ecosystem, SWOT, Priorities, KPIs, Maturity) au sens doar acolo unde:

1. Există conceptul de „ecosistem” ca entitate de sine - un grup de organizații care se recunosc reciproc ca parte a unui scop comun.
2. Există un mecanism de coordonare (facilitator, întâlniri periodice, output-uri agreate).
3. Există voință de a documenta și măsura această coordonare.

Pe scala de maturitate din [specificație, §4.1](spec.md#41-levelname-enum-maturity) (Inexistent → Incipient → Intentional → Integrated → Inspirational), strategic tier-ul devine relevant de la **Incipient** în sus. Pentru un oraș la Inexistent, strategic tier-ul nu e doar inutil - e un *concept străin*.

**Implicație de design:** strategic tier-ul **nu** e o cerință a standardului. E o extensie pe care un ecosistem o adoptă **când e gata pentru ea**.

## 2. Regula de separare core ↔ strategic

| | Core | Strategic |
|---|------|-----------|
| **Audiență primară** | publisheri (orice org) | curatori de ecosistem |
| **Entitățile** | Organisation, Member, Event, Project, Location | Ecosystem, SWOT, Priorities, KPIs, Maturity |
| **Threshold adopție** | Maturity Level 1+ („avem org-uri”) | Maturity Level 2+ („ne recunoaștem ca ecosistem”) |
| **FK direction** | nu cunoaște strategic-ul | referențiază liber core (FK out) |
| **Pot exista fără** | strategic-ul | core-ul deja publicat |

**Regula:** core nu are FK către strategic. Adopția strategic-ului e aditivă, niciodată retrofitting destructiv pe core. Un publisher poate înceta să mențină strategic tier oricând fără să-și invalideze publicările core.

## 3. Cele 5 entități strategice

| Entitate | Scop | Cardinalitate tipică |
|----------|------|----------------------|
| **Ecosystem** | Mecanismul de coordonare în sine (ex. TechTable) | 1 per publisher (uneori N, când portalul unui oraș găzduiește mai multe ecosisteme) |
| **SWOT** | Snapshot anual: Strengths/Weaknesses/Opportunities/Threats | 1 per ecosistem × an |
| **Priorities** | Priorități strategice (~3 per an) cu success metric | 1 per ecosistem × an |
| **KPIs** | Indicatori de capacitate / acțiune strategică / impact (din formula methodology) | 1 per ecosistem × an |
| **Maturity** | Auto-evaluare pe scala 5-level la un punct în timp | 1+ per ecosistem |

Toate cele 4 entități non-Ecosystem au PK compus `(ecosystem, year)` (sau `(ecosystem, dateAssessed)` pentru Maturity).

## 4. Adoption pathway

Strategic tier nu se adoptă „totul deodată”. Recomandare:

| Stadiu adopție | Entități recomandate | Threshold |
|----------------|----------------------|-----------|
| **Recunoaștere** | `Ecosystem` (declarație: „suntem un ecosistem”) | facilitator desemnat + 5+ org membre |
| **Auto-cunoaștere** | + `SWOT` + `Maturity` | proces anual de evaluare |
| **Direcție** | + `Priorities` | proces anual de planificare cu consens |
| **Măsurare** | + `KPIs` | infrastructură minimă de raportare |

Validatorul (vezi [§8 din spec](spec.md#8-validare)) acceptă orice subset - nu există cerință că dacă publici Ecosystem trebuie să publici și SWOT.

## 5. Relația cu methodology

[Metodologia](../docs/metodologie.md) definește cadrul abstract:

```
Impact relevant = Capacitate + Acțiune strategică
Acțiune strategică = Guvernanță × Metodologie
```

Strategic tier-ul oferă **schema de date** pentru a documenta și publica fiecare componentă a formulei:

| Componentă methodology | Entitate strategic | Câmp(uri) |
|------------------------|---------------------|-----------|
| Capacitate | KPIs | `capacity[]` |
| Acțiune strategică | KPIs + Priorities | `strategicActions[]` + `Priorities.items[]` |
| Impact | KPIs | `resultImpact[]` |
| Evaluare anuală (Q4) | SWOT + Maturity | toate câmpurile |
| Planificare anuală (Q1) | Priorities | `items[]` |

Un ecosistem care urmează methodology-ul **automat produce** datele care se mapează pe strategic tier. Strategic tier nu introduce activități noi - formalizează output-urile existente.

## 6. Decision log

Deciziile nivelului strategic au prefixul `D-S`, ca să se distingă de seria `D` din [`docs/decizii.md`](../docs/decizii.md).

### D-S001 (2026-04-26): Strategic = tier separat, nu parte din core v0.1

- **Decizie:** Entitățile Ecosystem, SWOT, Priorities, KPIs, Maturity formează un **tier separat** (`v0.1-strategic`), nu se adaugă la cele 5 core (Organisation/Member/Event/Project/Location).
- **Motivație:**
  - Threshold de adopție diferit: core funcționează la Maturity Level 1; strategic presupune Level 2+ și voință de coordonare conștientă.
  - Audiențe distincte: core e pentru orice publisher; strategic e pentru curatorul de ecosistem.
  - Pretenția de „standard universal” devine fragilă dacă forțezi orice publisher să modeleze conceptul de ecosistem ca precondiție de publicare.
  - Permite adopție gradată: orașele la Level 1 publică doar core; pe măsură ce maturizează, layer-ează strategic.
- **Implicație:** core **nu** are FK către strategic. Strategic referențiază core (FK out).
- **Alternative considerate:**
  - *Ecosystem ca a 6-a entitate core* - respins: forțează threshold-ul ridicat de adopție pe baseline; oferă un standard care exclude din start orașe puțin organizate.
  - *Toate cele 5 strategice ca entități core opționale* - respins pe jumătate: opt-in nu e suficient ca semnal; e nevoie de o separare clară de tier, ca un publisher să poată adopta core fără să fie un ecosistem matur.
- **Revisit when:** dacă >70% din publishers care adoptă core ajung să adopte și strategic într-un an de la onboarding, semnal că threshold-urile aproape că nu sunt distincte și unificarea ar simplifica.

### D-S002 (2026-04-26): Ecosystem ca tip propriu, nu subclasă schema:Organization

- **Decizie:** `Ecosystem` e un tip custom (`strategic:Ecosystem`), nu o subclasă semantică de `schema:Organization`.
- **Motivație:**
  - Un Ecosystem nu e o organizație: nu are angajați, nu vinde, nu e necesarmente persoană juridică. E un *mecanism de coordonare* (federație, masă rotundă, cluster).
  - schema.org nu are echivalent semantic exact (nici `Consortium`, nici tip pentru „federation of organizations” cu coordinator desemnat).
  - Tip propriu evită confuzii la consumeri: un agent care caută „organizații în Timișoara” nu vrea să primească Ecosystem ca rezultat amestecat cu org-uri reale.
- **Reuse semantic:** câmpurile `name`, `description`, `url`, `logo`, `addressLocality`, `addressRegion`, `addressCountry`, `member` reuse direct schema.org (alias-uri în context). Doar tipul în sine și relația `facilitator` sunt strategic-specific.
- **Alternative considerate:**
  - *Ecosystem extends schema:Organization* - respins: implicații semantice greșite (Person poate fi `affiliation` la Organization, dar nu vrei Persons cu affiliation la un Ecosystem ca primary semantic).
  - *Ecosystem = `schema:OrganizationRole`* - respins: Role e relație, nu entitate.

### D-S003 (2026-04-26): Compound scoping prin `inEcosystem` + `year` (sau `dateAssessed`)

- **Decizie:** SWOT, Priorities, KPIs au PK compus `(inEcosystem, year)`. Maturity are `(inEcosystem, dateAssessed)`. URI pattern: `{base}/{entity}/{ecosystem-slug}-{year}` (sau `-{date}`).
- **Motivație:**
  - Aceste entități sunt anuale prin definiție (cycle Q4-Q1 din methodology). `year` ca parte din PK reflectă natural cum se produc.
  - Maturity poate fi reasessată mid-year (de ex. după un eveniment major), deci `dateAssessed` e mai corect decât `year`.
  - Slug compus cu `-` în URI menține pattern-ul slug `^[a-z0-9-]+$` din core.
- **Property name `inEcosystem`:** ales în loc de `ecosystem` pentru a evita coliziunea cu prefix-ul namespace `ecosystem:` folosit în context. Semantic: „acest SWOT există în contextul unui ecosistem”.
- **Alternative considerate:**
  - *Embed strategic în Ecosystem ca array de SWOT-uri* - respins: face Ecosystem-ul un mega-document; pierdem URI-uri stabile per artifact strategic; consumeri trebuie să descarce tot pentru a citi un singur SWOT.
  - *PK simplu = `year`, scoping implicit prin publisher URI* - respins: rupe federation (portalul unui oraș care publică pentru 4 ecosisteme nu ar putea distinge SWOT-urile).

### D-S004 (2026-04-26): KPIs lean shape (arrays de bullet i18n strings, fără structură per item)

- **Decizie:** `KPIs.capacity`, `strategicActions`, `resultImpact` sunt arrays de **i18n strings** (text bullet), nu arrays de obiecte structurate `{name, target, currentValue, unit}`.
- **Motivație:**
  - Realitatea curentă: KPI-urile sunt formulate ca propoziții cu target inline („organizații active 15+”, „>20K EUR resurse atrase”). Parsing automat al target-urilor e ambiguu.
  - Adopție rapidă > completitudine: cere structura per KPI înainte ca ecosistemele să se obișnuiască să le și formuleze.
  - Layer structurat (cu `target`, `currentValue`, `unit`, `dueDate`) candidat pentru v0.2-strategic, după ce v0.1 demonstrează patterns reale de utilizare.
- **Cele 3 categorii (capacity / strategicActions / resultImpact)** sunt fixate prin formula din methodology. Nu sunt opționale.
- **Trade-off acceptat:** consumeri care vor să facă reporting structurat trebuie să facă NLP / pattern matching pe text. Compensăm prin recomandare de format („un KPI = o propoziție cu target inline”).

### D-S005 (2026-04-26): Maturity = enum 5-level cu nume umane

- **Decizie:** `Maturity.level` = `xsd:integer` în range `1..5`. `Maturity.levelName` = enum cu valorile `inexistent` / `incipient` / `intentional` / `integrated` / `inspirational` (corespund 1-1 cu `level`).
- **Motivație:**
  - Modelul 5-level e cel folosit deja în auto-evaluarea TechTable și seamănă cu modele cunoscute din industrie (CMM), adaptat la ecosistem.
  - `level` (numeric) e ușor de comparat și agregat. `levelName` e citibil de oameni.
  - Redundanța e intenționată: validatorul verifică că `level=2 ⟺ levelName=incipient` etc.
- **Maturity model URI:** opțional - un câmp `model: URI` indică modelul folosit, implicit modelul din specificație §4.1, identificat prin `https://standard.techtable.ro/v0.1-strategic/maturity-model`. Permite ecosisteme să folosească alt model dacă vor (de ex. CMM clasic, sau model propriu) păstrând schema.
- **Alternative considerate:**
  - *Doar `levelName`, fără număr* - respins: face dificilă agregarea/sortarea consumerilor.
  - *Custom levels per ecosistem* - respins pentru v0.1: nu poți compara cross-ecosistem dacă fiecare are scala lui.

### D-S006 (2026-04-26): Ecosystem.currentMaturity = pointer denormalizat (opt)

- **Decizie:** Ecosystem are câmp opțional `currentMaturity` care referențiază (`@id`) cea mai recentă Maturity assessment. E o **denormalizare deliberată**.
- **Motivație:**
  - Discovery flow tipic: consumer ia URI-ul unui Ecosystem și vrea să știe imediat „la ce nivel sunt”. Forțarea unei interogări secundare (toate Maturity-urile cu `inEcosystem=X`, sortat după `dateAssessed`, ia primul) e overhead disproporționat.
  - Pointer-ul rămâne autoritativ în URI - Maturity entity rămâne sursa de adevăr completă.
  - Consumer-ii care nu suportă referințe pot derefera pointer-ul opțional.
- **Trade-off acceptat:** publisher trebuie să updateze `Ecosystem.currentMaturity` când publică o Maturity nouă. Validatorul poate emite warning dacă există Maturity mai recentă nereferențiată.
- **Alternative considerate:**
  - *Doar `Maturity.inEcosystem` (lookup invers)* - respins: forțează N+1 queries pentru un consumer care vrea „toate ecosistemele cu maturity-ul lor curent”.
  - *Embed Maturity întreg în Ecosystem* - respins: pierdem URI stabilă pentru Maturity; rupem pattern-ul „o entitate, un URI”.

### D-S007 (2026-04-26): Versioning paralel cu core, nu cuplat

- **Decizie:** Strategic tier are propriul versioning: `v0.1-strategic`, `v0.2-strategic`, etc. NU e cuplat cu versiunile core (`v0.1`, `v0.2`).
- **Motivație:**
  - Strategic e mai puțin matur decât core (date puține la momentul redactării: un SWOT, un set de priorități, un set de KPIs). Iterațiile vor fi mai dese sau mai rare decât la core.
  - Cuplarea ar bloca progresul independent: dacă strategic are nevoie de breaking change, n-ar trebui să forțeze și un release nou de core.
  - Compatibilitatea între tier-uri se asigură prin `@context` rezolvabil (consumer încarcă versiunea declarată în document).
- **Convenție:** un strategic v0.X-strategic declară explicit cu ce versiuni core e compatibil (în spec §2 Conformanță). Strategic v0.1-strategic e compatibil cu core v0.1.
- **Implicație:** dacă core ajunge la v0.2 cu schimbări breaking pe Organisation/Project, strategic v0.1-strategic va emite errata sau v0.2-strategic care actualizează FK-urile.
- **Alternative considerate:**
  - *Versioning unificat (v0.1 înseamnă core+strategic)* - respins: cuplaj dur, blochează iterații independente.
  - *Strategic ca patch al core (v0.1.1-strategic)* - respins: ascunde că e tier separat conceptual.

