# Sheet Template: TechTable Standard v0.1

Structura recomandată pentru un Google Sheet (sau Excel) ca sursă editabilă, din care un converter automat generează JSON-LD canonical conform [`spec.md`](spec.md).

> Acest doc descrie **ce coloane trebuie** și **cum se mapează la JSON-LD canonical**. Converter-ul însuși (Python sau Apps Script) nu există încă.

## Convenții generale

- **Un sheet = o entitate**: Organisations, Members, Events, Projects, Locations sunt 5 sheet-uri.
- **Prima coloană = ID** (slug, fără spații, `^[a-z0-9-]+$`). Converter-ul construiește `@id` ca `{publisher_base_url}/{entity_path}/{id}`.
- **Câmpuri marcate `req`** în spec MUST fi completate. Validatorul respinge rândurile cu `req` lipsă.
- **i18n în Sheet:** când e o singură limbă, completează în coloana de bază (ex. `name`). Pentru multilingvism, adaugă coloane suffix `_en`, `_hu`, etc. (ex. `name_en`). Converter-ul construiește language map din toate coloanele cu același prefix.
- **FK-uri** (referințe la alte entități) se completează cu **slug-ul** entității țintă (nu cu URI complet). Converter-ul construiește URI-ul.
- **Tags / arrays** se completează ca string separat cu `;` sau `,` (ex. `javascript;meetup;frontend`).
- **Booleans:** `true` / `false` (sau `da`/`nu` cu mapping în converter).
- **Date:** ISO 8601 (`2026-09-15` pentru dată; `2026-09-15T18:00:00+03:00` pentru dată+timp).
- **Imagini:** convenție Drive - coloana stochează **Drive file ID** (nu URL). Apps Script convertește la `https://drive.google.com/thumbnail?id=<ID>&sz=w1600` la sync. Detalii: [`publisher-operations.md` §Imagini](publisher-operations.md).
- **Coloane operaționale `_*`** (status workflow, audit, timestamps): adăugate la fiecare sheet, **nu** intră în spec public. Detalii: [`publisher-operations.md` §Coloane operaționale](publisher-operations.md).

## Configurare publisher (un singur loc)

Înainte de a publica primul document, publisher-ul setează variabilele de bază (de regulă într-un sheet separat `_config`):

| Cheie | Exemplu | Note |
|-------|---------|------|
| `publisher_base_url` | `https://publisher.example` | Domeniul publisher-ului (fără slash final) |
| `default_language` | `ro` | Limba implicită pentru documentele fără `@language` map |
| `entity_paths` | `orgs`, `members`, `events`, `projects`, `locations` | Path-uri sub publisher base URL |

## Sheet 1: Organisations

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (construit ca `{publisher_base_url}/orgs/{id}`) | |
| `name` | text | **req** | `name` (i18n) | adaugă `name_en` etc. dacă multilingual |
| `description` | text | opt | `description` (i18n) | |
| `website` | URL | opt | `url` | |
| `logo_drive_id` | Drive ID | opt | `logo` (URL transformat) | converter: `https://drive.google.com/thumbnail?id=<ID>&sz=w1600` |
| `role` | text | opt | `role` (i18n) | |
| `domain` | enum | **req** | `domain` | una din `tech` / `entrepreneurial` / `civic` / `creative` |
| `tags` | text (separat cu `;`) | opt | `tags` (array) | |

## Sheet 2: Members

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/members/{id}`) | |
| `organisation_id` | slug | **req** | `affiliation: {@id: {base}/orgs/{organisation_id}}` | FK la Organisation |
| `name` | text | **req** | `name` | monolingual |
| `email` | email | opt | `email` | |
| `linkedin` | URL | opt | `sameAs[0]` | poate fi extins cu coloane `github`, `twitter` etc. |
| `photo_drive_id` | Drive ID | opt | `image` (URL transformat) | converter: `https://drive.google.com/thumbnail?id=<ID>&sz=w800` |
| `short_bio` | text | opt | `description` (i18n) | |

## Sheet 3: Events

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/events/{id}`) | |
| `name` | text | **req** | `name` (i18n) | |
| `short` | text | opt | `short` (i18n) | one-liner |
| `description` | text | opt | `description` (i18n) | |
| `organisation_id` | slug | **req** | `organizer: {@id: {base}/orgs/{organisation_id}}` | FK |
| `location_id` | slug | **req** | `location: {@id: {base}/locations/{location_id}}` | FK |
| `project_id` | slug | opt | `project: {@id: {base}/projects/{project_id}}` | FK |
| `date` | ISO date | **req** | combinat cu `start_time` → `startDate` | dacă nu există `start_time`, `startDate` rămâne doar dată |
| `start_time` | ISO time | opt | combinat cu `date` | |
| `end_time` | ISO time | opt | combinat cu `date` → `endDate` | |
| `domain` | enum | **req** | `domain` | |
| `tags` | text (`;`) | opt | `tags` | |
| `category` | text | opt | `category` | meetup, conferință, hackathon, workshop |
| `event_url` | URL | opt | `url` | |
| `cover_drive_id` | Drive ID | opt | `image` (URL transformat) | converter: `https://drive.google.com/thumbnail?id=<ID>&sz=w1600` |
| `max_participants` | int | opt | `maximumAttendeeCapacity` | |
| `access_type` | enum | opt | derivat în `isAccessibleForFree` | `free` → `true`; `paid`/`invite` → `false` |
| `tickets_url` | URL | opt | `ticketsUrl` | |
| `photos_url` | URL | opt | `photosUrl` | |
| `event_status` | enum | opt | `eventStatus` | `EventScheduled` (default) / `EventCancelled` / `EventPostponed` / `EventRescheduled` / `EventMovedOnline` |
| `speakers` | text (`;` cu slug-uri) | opt | `performer` (array de `@id`) | dacă speaker e un Member înregistrat; altfel ignorăm sau folosim `description` |
| `speakers_count` | int | opt | `speakersCount` | |
| `real_participants` | int | opt | `realParticipants` | post-event |

## Sheet 4: Projects

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/projects/{id}`) | |
| `name` | text | **req** | `name` (i18n) | |
| `description` | text | opt | `description` (i18n) | |
| `lead_organisation_id` | slug | **req** | `leadOrganisation: {@id: {base}/orgs/{lead_organisation_id}}` | FK |
| `partners` | text | opt | `partners` (i18n, text liber) | |
| `domain` | enum | **req** | `domain` | |
| `tags` | text (`;`) | opt | `tags` | |
| `status` | enum | **req** | `status` | `planning` / `active` / `completed` / `paused` |
| `start_date` | ISO date | opt | `startDateOnly` | |
| `end_date` | ISO date | opt | `endDateOnly` | |
| `url` | URL | opt | `url` | |
| `cover_drive_id` | Drive ID | opt | `image` (URL transformat) | converter: `https://drive.google.com/thumbnail?id=<ID>&sz=w1600` |

## Sheet 5: Locations

| Coloană Sheet | Tip | Card. | JSON-LD canonical | Note |
|---------------|-----|-------|-------------------|------|
| `id` | slug | **req** | `@id` (`{base}/locations/{id}`) | |
| `name` | text | **req** | `name` (i18n) | |
| `address` | text | opt | `address` (i18n) | |
| `city` | text | opt | `addressLocality` | |
| `country` | ISO 3166 alpha-2 | opt | `addressCountry` | ex. `RO` |
| `lat` | float | opt | `geo.latitude` | converter construiește `geo: {@type: GeoCoordinates, latitude, longitude}` |
| `lng` | float | opt | `geo.longitude` | |
| `is_virtual` | boolean | opt | `isVirtual` | default `false` |
| `url` | URL | opt | `url` | pentru virtuale: link Zoom/Meet |

## Workflow recomandat

> **Schiță, neimplementată.** Componentele descrise aici (scripturi, API, store) nu sunt construite încă. Documentul arată cum ar putea funcționa o cale de intrare a datelor.

Pattern complet (editor / curator / sync / publish): vezi [`publisher-operations.md`](publisher-operations.md).

Pe scurt:
1. Editorii adaugă rânduri în `_status = draft` și apasă „Submit for review” când sunt gata
2. Curatorii validează (`_status = validated`)
3. Apps Script „Publish” trimite rândurile validated către Worker `/admin/sync` → Worker upsert în store (D1)
4. API + MCP + website citesc din store și materializează JSON-LD la request
5. Erorile de validare se loghează în sheet `_publish_log` + email curator (rândul nu se publică, restul continuă)
