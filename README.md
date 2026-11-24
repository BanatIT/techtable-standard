# TechTable Standard

Un format comun și deschis pentru datele despre un ecosistem urban: organizații, evenimente, proiecte, oameni și locuri.

[![Validare](https://github.com/BanatIT/techtable-standard/actions/workflows/validate.yml/badge.svg)](https://github.com/BanatIT/techtable-standard/actions/workflows/validate.yml)
[![Licență: CC0 1.0](https://img.shields.io/badge/licen%C8%9B%C4%83-CC0%201.0-blue.svg)](LICENSE)
![Stadiu: draft v0.1](https://img.shields.io/badge/stadiu-draft%20v0.1-orange.svg)

## De ce

Fiecare organizație publică deja informații în locul ei: site, Meetup, Luma, LinkedIn. Nimeni nu are imaginea întreagă. Apar evenimente suprapuse în aceeași seară, iar cine vine nou în oraș nu știe de unde să înceapă.

De obicei răspunsul e încă o platformă, în care cineva reintroduce totul de mână. Asta nu ține în timp.

Aici scriem altceva: un acord despre forma datelor. O aplicație e un produs, o specificație e un acord, iar pe un acord poate construi oricine: aplicația orașului, site-ul unei comunități, un agent AI, o cercetare anuală. Aplicațiile se schimbă, acordul rămâne. Așa știu hărțile online orarul autobuzelor din orașe diferite: operatorii de transport publică datele într-un format comun (GTFS).

## Principii

- **Fiecare publică unde publică deja.** Datele se colectează automat de la sursă și păstrează sursa. Nimeni nu reintroduce nimic de mână într-un loc comun.
- **Federat.** Fiecare organizație publică sub domeniul ei. Legăturile se fac prin adrese stabile, fără un registru central.
- **Fără vocabular inventat.** Standardul stă pe [schema.org](https://schema.org) și [JSON-LD](https://json-ld.org), cu extensii doar unde lipsește ceva.
- **Strictul necesar.** Câmpurile obligatorii sunt puține. Un eveniment se poate publica doar cu nume, organizator, loc, dată și domeniu.
- **Ownership comun.** Standardul e al celor care îl folosesc. Orice schimbare trece prin pull request, cu discuție publică.

## Stadiu

**Draft v0.1, în validare publică.** Specificația e scrisă cap-coadă, dar nu are încă o implementare de referință și nu a fost folosită în producție.

**Până duminică, 29 noiembrie 2026, validăm specificația.** După aceea trecem la implementare: colectoarele automate și primii consumatori ai datelor.

| Nivel | Entități | Specificație |
|---|---|---|
| **Core v0.1** | Organisation, Member, Event, Project, Location | [`v0.1/spec.md`](v0.1/spec.md) |
| **Strategic v0.1** (opțional) | Ecosystem, SWOT, Priorities, KPIs, Maturity | [`v0.1-strategic/spec.md`](v0.1-strategic/spec.md) |

Core e strictul necesar ca să pornim. Nivelul strategic e o extensie pentru ecosistemele care își documentează și coordonarea (analiză anuală, priorități, indicatori).

## Cum arată

Un eveniment, doar cu câmpurile obligatorii:

```json
{
  "@context": [
    "https://schema.org",
    "https://standard.techtable.ro/v0.1/context.jsonld"
  ],
  "@type": "Event",
  "@id": "https://publisher.example/events/js-west-meetup-100",
  "name": { "ro": "JS West Meetup #100" },
  "organizer": { "@id": "https://publisher.example/orgs/js-west-community" },
  "location": { "@id": "https://publisher.example/locations/atelier-central" },
  "startDate": "2026-09-15T18:00:00+03:00",
  "domain": "tech"
}
```

Exemple complete pentru fiecare entitate: [`v0.1/examples/`](v0.1/examples/) și [`v0.1-strategic/examples/`](v0.1-strategic/examples/). Toate folosesc date fictive.

## Cum validezi specificația

Nu ai nevoie de cod. Durează cam o oră.

1. Citește [specificația core](v0.1/spec.md) (20 de minute).
2. Ia un eveniment real al organizației tale și scrie-l în format, pornind de la [exemplul de eveniment](v0.1/examples/event.canonical.json). Notează ce nu ai putut exprima și ce câmp nu ai înțeles.
3. Scrie ce ai găsit într-un [issue](https://github.com/BanatIT/techtable-standard/issues/new/choose) sau comentează la unul existent. Pentru corecturi mici, deschide direct un pull request.

Întrebarea de control: ai putea scrie un program care citește aceste date doar din specificație, fără să întrebi pe nimeni?

Pașii pentru contribuții sunt în [CONTRIBUTING.md](CONTRIBUTING.md).

## Probleme cunoscute

Le-am găsit rulând specificația prin validatoare. Sunt deschise ca issues, cu propuneri de rezolvare:

- [#1](https://github.com/BanatIT/techtable-standard/issues/1): în nivelul strategic, textele bilingve din liste se pierd la procesarea JSON-LD.
- [#2](https://github.com/BanatIT/techtable-standard/issues/2): limba implicită a unui document (`@language`) e descrisă greșit în specificație.
- [#3](https://github.com/BanatIT/techtable-standard/issues/3): o dată invalidă trece validarea dacă validatorul nu verifică formatele.
- [#4](https://github.com/BanatIT/techtable-standard/issues/4): ordinea din `@context` contează, dar specificația nu o spune.
- [#5](https://github.com/BanatIT/techtable-standard/issues/5): adresa `standard.techtable.ro` nu răspunde încă, deci contextul JSON-LD nu se poate încărca de acolo.

Propunerile pentru versiunea următoare au eticheta [`propunere`](https://github.com/BanatIT/techtable-standard/issues?q=is%3Aissue+is%3Aopen+label%3Apropunere).

## Ce găsești în repo

| Cale | Conținut |
|---|---|
| [`v0.1/`](v0.1/) | Core: specificație, context JSON-LD, 5 scheme JSON, exemple |
| [`v0.1-strategic/`](v0.1-strategic/) | Nivelul strategic: specificație, context, 5 scheme, exemple, [note de design](v0.1-strategic/README.md) |
| [`docs/decizii.md`](docs/decizii.md) | Deciziile de design și motivele lor |
| [`docs/metodologie.md`](docs/metodologie.md) | Metodologia de dezvoltare a unui ecosistem, pe care se sprijină nivelul strategic |
| [`tools/`](tools/) | Validatorul rulat automat la fiecare pull request |
| [`CHANGELOG.md`](CHANGELOG.md) | Ce s-a schimbat între versiuni |

## Validare locală

```bash
pip install -r tools/requirements.txt
python tools/validate.py
```

Scriptul verifică schemele și exemplele, cu verificarea formatelor activă. Aceeași verificare rulează la fiecare pull request.

## Guvernanță

- Schimbările se propun prin issue sau pull request. Nimeni nu scrie direct în `main`.
- Deciziile se iau prin consens, în discuție publică.
- Dacă nu există consens, votează grupul de curatori: o organizație, un vot. Nicio organizație nu decide singură.
- Grupul abia se formează. Până are 3 organizații, schimbările le integrează cei care întrețin repo-ul, pe baza discuției publice.

Regulile complete sunt în [specificație, secțiunea 10](v0.1/spec.md#10-governance).

## Licență

- Specificația, contextele, schemele, exemplele și deciziile de design: [CC0 1.0](LICENSE). Le poți folosi, modifica și republica fără să ceri voie și fără atribuire.
- [Metodologia](docs/metodologie.md): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ro), cu menționarea autorului.
- Codul din `tools/`: [MIT](tools/LICENSE).
- Numele „TechTable” și logourile asociate nu sunt acoperite de aceste licențe. Dacă publici o variantă modificată, dă-i alt nume, ca să nu se confunde.

## Despre

TechTable este masa comună a organizațiilor tech din Timișoara. Standardul a pornit de acolo și e facilitat de [Banat IT](https://banatit.ro). Curatorii și contribuitorii pot veni din orice organizație.

## In English

TechTable Standard is an open data format for describing an urban ecosystem: organizations, events, projects, people and places. It builds on schema.org and JSON-LD, is federated by design (each organization publishes under its own domain) and is dedicated to the public domain under CC0. The specification is written in Romanian and is currently a draft under public review. Issues and pull requests in English are welcome.
