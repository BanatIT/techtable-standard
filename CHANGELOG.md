# Changelog

Schimbările care contează pentru cine scrie sau citește date în format. Versiunile sunt etape (`v0.1`, `v0.2`), nu SemVer, până la v1.0.

## În lucru

Validare publică a v0.1. Defectele cunoscute și propunerile pentru v0.2 sunt în [issues](https://github.com/BanatIT/techtable-standard/issues).

## 2026-11-24: publicare

- Standardul are un repository public. Schimbările intră doar prin pull request, cu verificare automată.
- Guvernanță: fără consens, votează grupul de curatori, nu o singură organizație (specificație §10.2, decizia D015).
- Validator în `tools/`, cu verificarea formatelor activă.
- Nicio schimbare în scheme sau în contextele JSON-LD.

## v0.1-strategic (draft), 2026-04-26

- Nivelul strategic, opțional: Ecosystem, SWOT, Priorities, KPIs, Maturity.
- Context JSON-LD, 5 scheme, exemple.

## v0.1 (draft), 2026-04-25

- Core: Organisation, Member, Event, Project, Location.
- Context JSON-LD peste schema.org, 5 scheme JSON Schema (Draft 2020-12), exemple în forma de referință și în forma lite.
- `eventStatus` pentru evenimente anulate sau amânate (adăugat pe 2026-04-26).
