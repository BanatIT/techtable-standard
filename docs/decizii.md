# Decizii de design

Deciziile care au dat forma standardului și motivele lor. Fiecare are o condiție de revizuire: dacă se întâmplă, redeschidem discuția.

Deciziile nivelului strategic (D-S001 până la D-S007) sunt în [`v0.1-strategic/README.md`](../v0.1-strategic/README.md#6-decision-log).

O decizie nouă se adaugă la final, prin pull request, odată cu schimbarea pe care o explică.

## D001 (2026-04-25): temele se exprimă prin `tags` și `domain`, nu printr-o entitate Topic

- **Decizie:** v0.1 nu are entitate Topic. Tematica unui obiect stă în `tags` (texte libere) și în `domain` (listă controlată).
- **De ce:** o taxonomie de teme cere traduceri, ierarhii, sinonime și cineva care să o întrețină. E prea mult înainte să știm că e nevoie. Doar cu etichete libere, într-un sistem federat, apar „AI”, „ML” și „Artificial Intelligence” ca trei lucruri diferite, de aceea există și `domain`.
- **Revizuim când:** cel puțin 3 ecosisteme cer ierarhii de teme sau o etichetă apare în peste 40% din publicări.

## D002 (2026-04-25): Project este entitate din v0.1, în formă minimală

- **Decizie:** Project există ca entitate, cu puține câmpuri: nume, organizație lider, parteneri (text liber), domeniu, stare, date de început și sfârșit.
- **De ce:** multe inițiative au durată, dar nu au o dată fixă, deci nu pot fi evenimente. Fără Project, întrebarea „cine construiește ce” rămâne fără răspuns structurat.
- **Ce nu intră:** relația de la mai multe organizații la mai multe proiecte, etape, livrabile, finanțări.
- **Revizuim când:** apare repetat nevoia de mai multe organizații cu rol egal într-un proiect (vezi propunerile deschise).

## D003 (2026-04-25): `domain` are 4 valori: `tech`, `entrepreneurial`, `civic`, `creative`

- **Decizie:** `domain` este singura listă controlată de teme în v0.1.
- **De ce:** sunt domeniile în care orașele mari din România au deja organizații active și evenimente recurente. Sunt destul de largi ca aproape orice inițiativă să intre într-unul și destul de diferite ca filtrarea să ajute.
- **Alternative respinse:** o listă lungă (educație, cultură, sport) ar avea valori nefolosite; modelul Quadruple Helix descrie tipuri de actori, nu domenii.
- **Revizuim când:** un al doilea oraș adoptă standardul și cere o valoare nouă, cu cazuri concrete.

## D004 (2026-04-25): formatul este JSON-LD, cu o vedere simplificată („lite”)

- **Decizie:** forma de referință a unui document este JSON-LD, cu schema.org plus un context propriu pentru extensii. Vederea lite este o proiecție JSON simplă, generată automat din forma de referință.
- **De ce:** identificatorii sunt adrese web, deci documente publicate de organizații diferite se pot lega între ele fără coordonare centrală. Schema.org acoperă 4 din cele 5 entități. Modelele AI și motoarele de căutare cunosc deja vocabularul.
- **Alternative respinse:** un format JSON propriu (fără interoperabilitate), ActivityPub (protocol de mesagerie, nu de catalog).
- **Revizuim când:** mai multe ecosisteme cer simplificarea formei de referință.

## D005 (2026-04-25): namespace-ul este `https://standard.techtable.ro/v0.1/`

- **Decizie:** termenii proprii ai standardului stau sub `https://standard.techtable.ro/v0.1/`, pe un subdomeniu separat de site-ul TechTable.
- **De ce:** subdomeniul desparte standardul (infrastructură deschisă, a tuturor) de TechTable ca grup de lucru.
- **Compromis asumat:** numele „TechTable” din adresă poate sugera un standard doar pentru tech sau doar pentru Timișoara. Standardul este gândit pentru orice ecosistem urban.
- **Revizuim când:** standardul e adoptat în alt oraș. Atunci evaluăm un domeniu neutru, cu redirecționare de la cel vechi.

## D006 (2026-04-25): mai multe limbi, din prima versiune

- **Decizie:** câmpurile de text pot fi scrise într-o limbă sau în mai multe, în paralel. Codurile de limbă sunt BCP 47.
- **De ce:** adăugarea limbilor mai târziu ar însemna rescrierea tuturor documentelor publicate. Cine publică într-o singură limbă nu plătește nimic în plus.
- **Limba implicită:** română. Alți publisheri își pot alege alta.

## D007 (2026-04-25): câmpuri obligatorii puține

- **Decizie:** obligatorii sunt doar câmpurile fără de care un obiect nu poate fi identificat, clasificat și legat de altele. De exemplu, la organizație: identificator, nume, domeniu.
- **De ce:** fiecare câmp obligatoriu în plus e un motiv ca o organizație să renunțe la prima publicare. Câmpurile opționale lipsă se semnalează ca avertismente, nu ca erori.
- **Revizuim când:** un câmp opțional e completat în peste 70% din publicări. Atunci poate deveni obligatoriu.

## D008 (2026-04-25): cine publică nu scrie JSON-LD de mână

- **Decizie:** standardul va veni cu unelte care ascund formatul. Organizațiile lucrează în ce folosesc deja, iar uneltele vor produce și valida JSON-LD. Deocamdată există doar validatorul din `tools/`.
- **De ce:** un standard moare dacă cei care publică sunt obligați să învețe un format. Schema.org s-a răspândit pentru că sistemele de publicare îl generează singure.
- **Rolul de curator:** o persoană sau o echipă, din orice organizație a ecosistemului, care răspunde de calitatea datelor publicate sub o adresă comună.

## D009 (2026-04-25): validarea se face cu JSON Schema

- **Decizie:** fiecare entitate are o schemă JSON Schema (Draft 2020-12), aplicată pe forma compactă a documentului.
- **De ce:** unelte cunoscute, în orice limbaj și în orice sistem de integrare continuă. SHACL e mai expresiv, dar are puține unelte și se învață greu.
- **Revizuim când:** apar reguli pe care JSON Schema nu le poate exprima.

## D010 (2026-04-25): Location folosește `schema:Place`

- **Decizie:** nu definim un tip propriu pentru locuri. `isVirtual` este singura extensie.
- **De ce:** `Place` este bine modelat și folosit pe scară largă. Un tip propriu ar pierde interoperabilitate fără niciun câștig.

## D011 (2026-04-25): guvernanță tranzitorie

- **Decizie:** cât timp standardul e folosit într-un singur ecosistem, regulile de decizie sunt minime: propuneri prin issue sau pull request, decizie prin consens, o iterație majoră pe an.
- **De ce:** un proces complet (comitete, vot formal) e prea mult pentru început, dar lipsa oricărei reguli scrise îi face pe cei noi să se întrebe cine decide.
- **Modificată de D015:** forma inițială spunea că, fără consens, decide organizația care întreține standardul.

## D012 (2026-04-26): standardul nu impune cum îți ții datele

- **Decizie:** specificația descrie forma documentelor publicate, nu stocarea. Fișiere statice, bază de date sau o combinație, toate sunt în regulă.
- **De ce:** fiecare publisher are deja un mod de lucru. Contează doar ca adresele să răspundă și documentele să fie conforme.
- **Recomandare pentru implementări noi:** o bază de date, pentru căutare și filtrare.

## D013 (2026-04-26): `eventStatus` pentru evenimente anulate sau amânate

- **Decizie:** Event are câmpul opțional `eventStatus`, cu valorile din schema.org (`EventCancelled`, `EventPostponed` și celelalte).
- **De ce:** „scot evenimentul din listă” și „anunț public că s-a anulat” sunt lucruri diferite. Schema.org are deja vocabularul.

## D014 (2026-04-26): imaginile, în ghidul pentru Google Sheet

- **Decizie:** în ghidul operațional pentru cei care lucrează în Google Sheet, imaginile se țin în Google Drive și se transformă în adrese la publicare. Specificația vede doar adresa.
- **De ce:** niciun pas în plus pentru cei care lucrează deja în Drive.
- **Notă:** ghidul nu face parte din specificație. E o cale posibilă de intrare a datelor, nu singura.

## D015 (2026-11-24): fără consens, votează grupul de curatori

- **Decizie:** dacă o propunere nu ajunge la consens după două runde de discuție, în cel mult 30 de zile, votează grupul de curatori: o organizație, un vot, majoritate simplă. Nicio organizație nu are drept de decizie separat. Până când grupul are 3 organizații confirmate, cei care întrețin repository-ul integrează schimbările pe baza discuției publice.
- **De ce:** un standard comun nu poate avea un proprietar. Regula din D011, prin care decidea o singură organizație, contrazicea asta.
- **Tot de acum:** repository-ul este public, iar orice schimbare intră prin pull request, cu verificare automată și review.
