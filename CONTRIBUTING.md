# Cum contribui

Standardul e al celor care îl folosesc. Poți contribui fără să scrii cod: cea mai utilă contribuție acum este să încerci să-ți descrii propriile date în format și să spui ce nu merge.

Poți scrie în română sau în engleză.

## Ai găsit o problemă sau ai o întrebare

Deschide un [issue](https://github.com/BanatIT/techtable-standard/issues/new/choose). Sunt trei tipuri:

- **Defect:** specificația, o schemă sau un exemplu e greșit ori se contrazice cu altceva.
- **Propunere:** un caz real pe care formatul nu îl poate exprima, cu schimbarea pe care o sugerezi.
- **Întrebare:** ceva ce nu e clar din specificație. Dacă nu e clar pentru tine, probabil nu e clar nici pentru alții.

Caută întâi printre cele existente. Un comentariu la un issue deschis ajută mai mult decât unul nou pe aceeași temă.

## Vrei să schimbi ceva

Nimeni nu scrie direct în `main`. Orice schimbare intră prin pull request.

1. Fă un fork și un branch cu nume scurt și clar, de exemplu `event-locatie-optionala`.
2. Fă schimbarea. Dacă atingi o schemă, actualizează și specificația, și exemplele, ca să spună același lucru.
3. Rulează validarea local:

   ```bash
   pip install -r tools/requirements.txt
   python tools/validate.py
   ```

4. Deschide pull requestul și completează șablonul.

Corecturile mici (greșeli de scriere, linkuri, formulări neclare) pot veni direct ca pull request. Pentru orice schimbă sensul specificației, deschide întâi un issue, ca discuția să aibă loc înainte de muncă.

## Ce conține o propunere

- **Cazul:** ce date reale nu poți descrie acum. Un exemplu concret valorează mai mult decât un principiu.
- **Schimbarea:** ce câmp, ce valoare sau ce regulă adaugi, modifici sau scoți.
- **Compatibilitatea:** documentele deja scrise rămân valide? Dacă nu, ce trebuie schimbat în ele.

## Cum se decide

- Un pull request are nevoie de verificarea automată trecută și de cel puțin o aprobare.
- Schimbările de sens se decid prin consens, în discuția publică din issue sau din pull request.
- Dacă nu există consens, votează grupul de curatori: o organizație, un vot.
- Grupul abia se formează. Până are 3 organizații, schimbările le integrează cei care întrețin repo-ul, pe baza discuției publice. O organizație intră în grup printr-un issue în care arată ce publică sau ce folosește.

Regulile complete sunt în [specificație, secțiunea 10](v0.1/spec.md#10-governance). Deciziile luate și motivele lor sunt în [`docs/decizii.md`](docs/decizii.md).

## Reguli de scriere

- Câmpurile și valorile din format sunt în engleză (`startDate`, `organizer`), ca în schema.org. Textul specificației este în română.
- Cuvintele MUST, SHOULD și MAY au sensul din [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119).
- Exemplele folosesc doar date fictive, pe domeniul rezervat `.example` (de exemplu `publisher.example`). Nu pune în repo nume, adrese de e-mail sau telefoane reale.
- Fișierele JSON au indentare de 2 spații.
- O schimbare de sens se trece și în [`CHANGELOG.md`](CHANGELOG.md).

## Licența contribuțiilor

Prin contribuție, ești de acord ca textul și schemele tale să fie publicate sub [CC0 1.0](LICENSE), iar codul din `tools/` sub [MIT](tools/LICENSE).

## Cum ne purtăm

Vezi [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
