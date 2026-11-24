# Sheet Template: TechTable Standard v0.1-strategic

Structura recomandată pentru un Google Sheet (sau Excel) ca sursă editabilă pentru date strategice, din care un converter automat generează JSON-LD canonical conform [`spec.md`](spec.md).

> Acest doc descrie **ce coloane trebuie** și **cum se mapează la JSON-LD canonical**. Converter-ul însuși (Python sau Apps Script) nu există încă.

## Convenții generale

- **Un sheet = o entitate**: `Ecosystems`, `SWOT`, `Priorities`, `KPIs`, `Maturity` sunt 5 sheet-uri.
- **Prima coloană = ID** (slug, `^[a-z0-9-]+$`). Pentru entitățile compound (SWOT/Priorities/KPIs/Maturity), recomandare: `{ecosystem-slug}-{year}` (ex. `innov-west-2026`).
- **i18n în Sheet:** convenția identică cu [core sheet template](../v0.1/sheet-template.md): coloană de bază pentru limba implicită (`name`), suffix `_en`, `_hu` etc. pentru limbi adiționale.
- **FK-uri** se completează cu **slug-ul** entității țintă. Converter-ul construiește URI-ul.
- **Bullets multilinguale** (SWOT items, KPIs items): vezi §„i18n pentru arrays” mai jos.
- **Date:** ISO 8601 (`2026-01-15`).

## Configurare publisher

Sheet separat `_config` (același cu core dacă există deja):

| Cheie | Exemplu | Note |
|-------|---------|------|
| `publisher_base_url` | `https://publisher.example` | Domeniul publisher-ului (fără slash final) |
| `default_language` | `ro` | Limba implicită |
| `entity_paths_strategic` | `ecosystems`, `swot`, `priorities`, `kpis`, `maturity` | Path-uri pentru entitățile strategic |

## Sheet 1: Ecosystems

Tipic 1-N rânduri (un publisher publică de regulă 1 ecosistem; un publisher municipal poate publica N).

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/ecosystems/{id}`) | |
| `name` | text | **req** | `name` (i18n) | adaugă `name_en` etc. |
| `description` | text | opt | `description` (i18n) | |
| `domain` | enum | **req** | `domain` | una din `tech` / `entrepreneurial` / `civic` / `creative` |
| `facilitator_id` | slug | **req** | `facilitator: {@id: {base}/orgs/{id}}` | FK la Organisation core |
| `member_ids` | text (sep `;`) | opt | `member` (array de `@id`) | slug-uri Organisation core |
| `address_locality` | text | opt | `addressLocality` | |
| `address_region` | text | opt | `addressRegion` | |
| `address_country` | ISO 3166 alpha-2 | opt | `addressCountry` | ex. `RO` |
| `website` | URL | opt | `url` | |
| `logo_url` | URL | opt | `logo` | |
| `tags` | text (sep `;`) | opt | `tags` | |
| `current_maturity_id` | slug | opt | `currentMaturity: {@id: {base}/maturity/{id}}` | pointer la Maturity record |

## Sheet 2: SWOT

Un rând per (ecosistem × an). Câmpurile S/W/O/T conțin bullet-uri separate de un delimiter.

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/swot/{id}`) | recomandat: `{ecosystem-slug}-{year}` |
| `ecosystem_id` | slug | **req** | `inEcosystem: {@id: {base}/ecosystems/{id}}` | |
| `year` | int | **req** | `year` | |
| `date_assessed` | ISO date | opt | `dateAssessed` | |
| `strengths` | text (sep `\|`) | opt | `strengths` (array de i18n strings) | un bullet per linie sau separat de pipe |
| `weaknesses` | text (sep `\|`) | opt | `weaknesses` | |
| `opportunities` | text (sep `\|`) | opt | `opportunities` | |
| `threats` | text (sep `\|`) | opt | `threats` | |
| `notes` | text | opt | `notes` (i18n) | |

> **Constraint:** cel puțin una dintre coloanele `strengths`/`weaknesses`/`opportunities`/`threats` MUST conține minim 1 bullet (validatorul respinge SWOT complet gol).

## Sheet 3: Priorities

Un rând per (ecosistem × an), cu items reprezentate prin coloane numerotate.

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/priorities/{id}`) | |
| `ecosystem_id` | slug | **req** | `inEcosystem` | |
| `year` | int | **req** | `year` | |
| `date_assessed` | ISO date | opt | `dateAssessed` | |
| `priority_1_name` | text | **req** (cel puțin 1 item) | `items[0].name` (i18n) | suffix `_en` etc. acceptat |
| `priority_1_description` | text | opt | `items[0].description` (i18n) | |
| `priority_1_success_metric` | text | opt | `items[0].successMetric` (i18n) | |
| `priority_1_related_projects` | text (sep `;`) | opt | `items[0].relatedProjects` (array de `@id` Project core) | slug-uri |
| `priority_2_name` ... | text | opt | `items[1]...` | replicat per item |
| `priority_3_name` ... | text | opt | `items[2]...` | |
| ... | | | | converter detectează automat câte priorități există după pattern-ul coloanelor `priority_N_*` |
| `notes` | text | opt | `notes` (i18n) | |

> Pattern de coloane `priority_N_*` permite N variabil - converter-ul iterează și construiește array `items[]`.

## Sheet 4: KPIs

Un rând per (ecosistem × an).

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/kpis/{id}`) | |
| `ecosystem_id` | slug | **req** | `inEcosystem` | |
| `year` | int | **req** | `year` | |
| `date_assessed` | ISO date | opt | `dateAssessed` | |
| `capacity` | text (sep `\|`) | opt | `capacity` (array de i18n strings) | un KPI per bullet |
| `strategic_actions` | text (sep `\|`) | opt | `strategicActions` | |
| `result_impact` | text (sep `\|`) | opt | `resultImpact` | |
| `notes` | text | opt | `notes` (i18n) | |

> **Constraint:** cel puțin una dintre coloane MUST conține minim 1 bullet.

## Sheet 5: Maturity

Un rând per assessment (de regulă 1/an, dar pot fi mai multe).

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/maturity/{id}`) | |
| `ecosystem_id` | slug | **req** | `inEcosystem` | |
| `date_assessed` | ISO date | **req** | `dateAssessed` | |
| `level` | int 1..5 | **req** | `level` | |
| `level_name` | enum | **req** | `levelName` | `inexistent` / `incipient` / `intentional` / `integrated` / `inspirational` |
| `model_url` | URL | opt | `model` | default omis (folosește standardul) |
| `notes` | text | opt | `notes` (i18n) | |

> **Constraint:** `level` și `level_name` MUST fi consistente (1↔inexistent, 2↔incipient, etc.). Converter-ul poate auto-completa `level_name` dacă lipsește, pe baza `level`.

## i18n pentru arrays (SWOT, KPIs)

Bullet-urile multilinguale necesită convenție pentru a separa atât bullets-urile (un nivel) cât și limbile (alt nivel). Recomandări (în ordinea preferinței):

### Opțiunea A: coloane separate per limbă (recomandat)

`strengths` (limba implicită) + `strengths_en` + `strengths_hu` etc., fiecare cu același număr de bullets în aceeași ordine, separate cu `|`:

```
strengths:    "15+ org tech active|Hub multinaționale|3 universități tehnice"
strengths_en: "15+ active tech orgs|Multinational hub|3 technical universities"
```

Converter combină pe poziție:
```json
"strengths": [
  { "ro": "15+ org tech active", "en": "15+ active tech orgs" },
  { "ro": "Hub multinaționale", "en": "Multinational hub" },
  { "ro": "3 universități tehnice", "en": "3 technical universities" }
]
```

### Opțiunea B: singur limbaj (default ecosystem)

Dacă publisher-ul e monolingual, completează doar `strengths` (în limba implicită): converter generează JSON-LD cu `@language` document-level și string-uri simple:

```json
{
  "@language": "ro",
  "strengths": ["15+ org tech active", "Hub multinaționale", "3 universități tehnice"]
}
```

## Workflow recomandat

> **Schiță, neimplementată.** Componentele descrise aici (scripturi, API, store) nu sunt construite încă. Documentul arată cum ar putea funcționa o cale de intrare a datelor.

1. Curatorul de ecosistem ține sheet-urile strategice în paralel cu cele core.
2. Converter-ul rulează pe ambele seturi de sheet-uri și generează JSON-LD canonical sub publisher base URL.
3. Validatorul verifică documentele pe specificația strategică și pe cea core.
4. Erorile/warnings se traduc în mesaje plain pentru curator (ex. *„rândul 2 din SWOT: cel puțin una dintre S/W/O/T trebuie completată”*).
5. Documentele canonical se servesc HTTP la `@id` URIs; lite view se generează la cerere.
