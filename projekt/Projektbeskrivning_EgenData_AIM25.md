# Projektbeskrivning — egen datakälla

**Data engineering och Agila metoder (YH-02032)**
Grupprojekt, vecka 3–9 · 25 augusti – 8 oktober 2026
Utvecklare inom AI och maskininlärning · IT-Högskolan · Kursansvarig: Mikael Huss

---

> **Vem det här dokumentet gäller.** Det här är projektbeskrivningen för team
> som fått godkänt på en ansökan om egen datakälla och egen modell. Kör ni
> standarduppgiften — elprisprediktion med SE1–SE4 och SMHI-väder — är det
> `Projektbeskrivning_DataEngineering_AIM25` som gäller för er, inte det här
> dokumentet.
>
> **Kraven är desamma.** Samma sex systemkomponenter, samma examination,
> samma lärandemål, samma betygskriterier. Det enda som skiljer är att ni
> själva står för datakällan, målvariabeln och modellen. Ni får varken
> lättare eller svårare krav — men ni får mindre färdigt material och mindre
> riktad handledning, eftersom jag inte har testat er datakälla i förväg.

---

## 1. Sammanfattning

Ni bygger ett system som på egen hand hämtar färsk data från en levande
källa, omvandlar den till features, tränar om en modell enligt schema,
exponerar modellen som en tjänst som går att fråga över internet, och som
loggar och följer upp kvaliteten på sina egna prediktioner över tid.

Arbetet görs i grupp med ett agilt arbetssätt och pågår i sju veckor
parallellt med lektionerna. Projektet utgör huvuddelen av kursens
examination.

Modellträning ingår inte i den här kursen. Den kunskapen har ni med er från
tidigare kurser i programmet. Här handlar allt om infrastrukturen runt
modellen: hur den matas med data, hur den paketeras, hur den driftsätts, och
hur ni vet att den fortfarande fungerar nästa vecka.

## 2. Vad ni får — och inte får

Till skillnad från standarduppgiften får ni **inget startrepo med färdig
modell och historisk data**. Det ni får är:

- Godkännandet av er ansökan, med eventuella villkor jag ställt i den.
- `db/schema.sql` och `.env.example` från standardrepot, som mönster att
  utgå från. Tabellnamnen kommer inte passa er men strukturen gör det.
- Samma handledning, samma lektioner, samma deadlines som alla andra.

Ni står själva för:

- **Datakällan.** Åtkomst, eventuella nycklar, och att den fortsätter
  fungera i sju veckor.
- **Modellen.** En enkel, färdigtränad basmodell som ni kan utgå från.
  Den behöver inte vara bra. Den behöver finnas, gå att ladda, och gå att
  träna om från er egen feature-tabell.
- **Historisk data.** Tillräckligt för att träna och utvärdera på. Har ni
  ingen historik alls går projektet inte att genomföra — se avsnitt 3E.

Skriv de här tre sakerna som de första ticketsen på er tavla. Ett team som
i vecka 5 fortfarande inte har en laddbar modell ligger illa till.

## 3. Vad ni ska bygga

Systemet består av sex delar. Alla sex ska finnas och fungera för godkänt
resultat. Det här är samma lista som i standarduppgiften, formulerad utan
referens till elpris och SMHI.

### A. Feature-pipeline

- Hämtar färsk data från er datakälla.
- **Validerar datan innan den sparas:** rimlighetskontroller, saknade
  värden, dubbletter.
- Omvandlar rådata till features — inklusive att koppla samman era källor i
  tid om ni har fler än en — och skriver dem till en tabell i er egen
  molnbaserade Postgres-databas (Neon eller Supabase).
- Körs schemalagt, minst en gång per dygn, utan att någon startar den
  manuellt.
- Är paketerad i en container.

### B. Träningspipeline

- Läser features från er Postgres-databas.
- Tränar om modellen på uppdaterad data.
- Registrerar resultatet som en ny version i Hugging Face Hub (model
  registry), tillsammans med utvärderingsmått.
- Körs schemalagt eller på en tydligt definierad trigger. Ni ska kunna
  motivera ert val.
- Vid projektets slut ska ni ha minst två registrerade modellversioner och
  kunna redogöra för vad som skiljer dem åt.

### C. Inferenstjänst

- En FastAPI-tjänst i en container.
- Laddar en specifik, versionsmärkt modell från Hugging Face Hub.
- Hämtar aktuella features och returnerar en prediktion.
- Minst två endpoints: `/predict` och `/health`.
- Driftsatt så att någon utanför gruppen kan anropa den över internet på en
  publik HTTPS-adress. Det räcker inte att den fungerar i er egen
  utvecklingsmiljö.

### D. Spårbarhet

För varje prediktion systemet gör ska ni i efterhand kunna svara på fyra
frågor:

1. Vilken data byggde modellen på? (tabell och tidpunkt i Postgres)
2. Vilken kod producerade prediktionen? (git-commit, taggad i containerimagen)
3. Vilken modellversion användes? (versionsnummer ur Hugging Face Hub)
4. När gjordes prediktionen?

Detta löser ni genom att logga varje prediktion till en egen tabell i
Postgres. Kan ni inte svara på alla fyra frågorna i efterhand är kravet
inte uppfyllt.

### E. Monitorering

**Det här är komponenten som avgjorde om er ansökan blev godkänd.**

Monitorering är bara meningsfull om facit kommer. En prognos måste gå att
jämföra med vad som faktiskt hände, och det måste hända inom projektets
sju veckor — annars har ni ingenting att mäta mot och ingenting att larma
på.

Er datakälla godkändes bara om ni kunde visa att facit anländer inom
**högst några dygn** efter prediktionen. Det kravet är inte förhandlingsbart
och det är inte något ni kan lösa i efterhand med ett resonemang. Ett
statiskt historiskt dataset uppfyller det inte. En prognos med sex månaders
utfallshorisont uppfyller det inte heller.

Ni ska:

- Jämföra loggade prediktioner mot faktiskt utfall när utfallet finns
  tillgängligt.
- Beräkna ett felmått över tid och visualisera utvecklingen. En enkel graf
  räcker.
- Definiera en tröskel för när modellen ska anses ha försämrats, och
  beskriva vad som ska hända då.
- Ha minst en automatisk datakvalitetskontroll som slår larm om pipelinen
  börjar leverera orimlig data.

**Om facit slutar komma** — källan lägger ner, API:et ändras, nyckeln slutar
gälla — hör av er till mig samma vecka. Ni går då över till reservplanen ni
angav i ansökan, i praktiken oftast standarduppgiften. Det är inte ett
misslyckande, men det måste ske i tid för att vara möjligt.

### F. CI/CD och kodgranskning

- GitHub Actions som kör tester och linting vid varje pull request.
- Vid merge till main byggs containerimagen och taggas med git-commit.
- All kod till main går via pull request med minst en granskare. Varje
  gruppmedlem ska ha granskat minst tre andras pull requests och fått minst
  tre av sina egna granskade. Granskningen ska synas som kommentarer, inte
  bara som ett godkännande.

### Valfritt: Hopsworks som fördjupning

I vecka 6 testar alla, i en handledd övning, Hopsworks — en europeisk
leverantör av feature stores (gratis, inget kreditkort). Ni är välkomna att
därefter låta er riktiga feature- och träningspipeline läsa och skriva mot
Hopsworks istället för Postgres. Det ger inte i sig ett högre betyg. Postgres
räcker gott och väl för att uppfylla alla krav i det här avsnittet.

## 4. Teknisk plattform

| Tjänst | Roll i projektet | Kostnad |
|---|---|---|
| GitHub | Kod, kodgranskning, CI/CD och schemaläggning av pipelines | Gratis |
| Neon eller Supabase (Postgres) | Datalagring: rådata, features, loggade prediktioner och spårbarhet | Gratis, inget kort |
| Render | Driftsättning av inferenstjänsten (Docker) | Gratis, inget kort |
| Hugging Face Hub | Model registry | Gratis, inget kort |
| **Er egen datakälla** | Datakälla | Enligt vad ni angav i ansökan |
| Databricks Free Edition | Används på lektion i vecka 4 för Spark och Databricks — ingår inte i projektet | Gratis, inget kort |
| Hopsworks Serverless (valfritt) | Feature store — handledd övning i vecka 6 | Gratis, inget kort |

Kursens grundplattform är gratis och kräver inget kreditkort. Vill ni köra
inferenstjänsten på Google Cloud eller Azure istället, prata med mig.

## 5. Data governance och etik

Standarduppgiften använder öppen väderdata och publika elpriser. Ingen
persondata, inga åtkomstbegränsningar, inga licensfrågor. **Er datakälla är
sannolikt inte lika enkel**, och det är delvis därför den är intressantare.

Innan sprint 1 är slut ska ni ha skrivit ner, i repot:

- **Vem äger datan** och på vilken licens eller vilka villkor ni använder
  den. Får ni spara den? Får ni publicera den vidare? Får ni exponera
  prediktioner byggda på den?
- **Innehåller den personuppgifter eller på annat sätt känslig
  information?** Om ja: vilka, varför är det nödvändigt, och vad gör ni för
  att begränsa det? Direkt eller indirekt identifierbara personer räknas
  båda.
- **Vad händer med datan när kursen är slut?**

## 6. Arbetssätt

Hur ni arbetar är en del av examinationen, inte bara vad ni bygger.
Lärandemål 9 och 10 handlar om agilt arbetssätt i praktiken, och de bedöms
på det som faktiskt syns i era artefakter under kursens gång.

**Tavlan i GitHub Projects och er commit-historik läses som underlag vid
bedömning.** Uppgifter ska flyttas när arbetet flyttas.

### Sprintar

Projektet drivs i tre sprintar om två veckor. Varje sprint inleds med
sprintplanering och avslutas med sprintgranskning och retrospektiv.

**Varför två veckor och inte en?** Ni har två lektionstillfällen i veckan.
En enveckorssprint skulle bara ge er två tillfällen totalt per sprint —
knappt utrymme för planering, faktiskt byggarbete, granskning och
retrospektiv innan nästa sprint redan måste planeras. Med två veckor får ni
fyra lektionstillfällen per sprint: nog för att hinna bygga något mellan
planeringen och granskningen, så att granskningen har något substantiellt
att visa upp och retrospektivet har mer att reflektera över än "vi kom
precis igång".

Det är standardvalet, inte ett orubbligt krav. Vill ert team köra
enveckorssprintar — till exempel för att få snabbare återkoppling på en viss
del av pipelinen — går det bra att föreslå det, med en motivering, i
sprintplaneringen för sprint 1. Ett övertygande argument kan få igenom det
för just ert team.

### Löpande

- Daglig avstämning (stand-up) i början av varje lektionsdag, max tio minuter.
- En tavla i GitHub Projects som speglar det verkliga läget.
- En skriven definition of done som gruppen enats om, och som ni faktiskt
  tillämpar.
- Dokumenterade retrospektiv: vad fungerade, vad fungerade inte, vad ändrar
  ni till nästa sprint.

Ni väljer själva om ni arbetar enligt Scrum, Kanban eller en kombination —
men ni ska kunna motivera valet och visa att ni följt det.

## 7. Tidsplan

Identisk med standarduppgiften.

| Vecka | Datum | Fokus i projektet | Milstolpe |
|---|---|---|---|
| 3 | 25/8, 27/8 | Uppstart: grupper bildas, projektplanering, backlog byggs | Projektplan + backlog senast 28/8 |
| 4 | 1/9, 3/9 | Sprint 1: feature-pipeline mot egen Postgres | Feature-pipeline kör schemalagt |
| 5 | 8/9, 10/9 | Sprint 1 forts.: träningspipeline och modellregistrering | Sprintgranskning + retrospektiv 10/9 |
| 6 | 15/9, 17/9 | Sprint 2: driftsättning av inferenstjänsten | **Redovisning i grupp 17/9** |
| 7 | 22/9, 24/9 | Sprint 2 forts.: spårbarhet, loggning, monitorering | Publik URL som fungerar; sprintgranskning 24/9 |
| 8 | 29/9, 1/10 | Sprint 3: omträning, datakvalitet, integration | |
| 9 | 6/10, 8/10 | Slutförande, redovisning | Slutpresentation + rapport |

**Extra milstolpe för er:** laddbar basmodell och historisk data i repot
senast **4/9**. Ligger ni efter där i vecka 5 tar vi ett samtal om att gå
över till standarduppgiften medan det fortfarande är möjligt.

## 8. Leveranser

| Vad | Form | Deadline |
|---|---|---|
| Projektplan och första backlog | Dokument + tavla i GitHub Projects | 28/8 |
| Data governance-uppgiften (avsnitt 5) | Dokument i repot | 11/9 |
| Redovisning i grupp | Muntlig presentation, 15 min + frågor | 17/9 |
| Fungerande system | Publik URL + kodrepo | se schema |
| Individuell analys av tekniskt bidrag | Skriftlig, 2–4 sidor, individuell | se schema |
| Slutpresentation med live-demo | Muntlig, 20 min + frågor | 6/10 eller 8/10 |
| Projektrapport | Skriftlig, gruppgemensam | se schema |
| Retrospektiv och utvärdering | Skriftlig, bifogas rapporten | med rapporten |

### Om projektrapporten

Utöver hur ni byggt ert system ska rapporten innehålla en teknisk
redogörelse där ni gör reda för fyra saker:

1. Hur er lösning är paketerad, och hur paketering med Docker och Kubernetes
   fungerar i större sammanhang.
2. Vilka molntjänster ni använt, och hur motsvarande lösning hade sett ut
   hos AWS, Azure respektive Google Cloud.
3. Hur databehandling i stor skala fungerar med Spark och Databricks, och
   var ert eget upplägg inte hade räckt till.
4. Vilka etiska frågeställningar er egen datahantering väcker.

## 9. Examination

Kursen har tre examinationsmoment enligt kursplanen. Varje moment prövar
sina egna lärandemål.

**Moment 1 — Projektarbete** (löpande, lärandemål 3–7, 9–14, 16)
Bedöms på det färdiga systemet, på koden, på rapporten och på hur arbetet
faktiskt bedrivits under de sju veckorna. Både produkten och processen
ingår. Slutpresentationen med live-demo är ett bedömningstillfälle inom det
här momentet, inte ett eget moment.

**Moment 2 — Redovisning i grupp** (17/9, lärandemål 1, 2, 8)
En presentation på cirka 15 minuter där gruppen redogör för sin projektplan,
hur ni arbetar agilt och varför ni valt det arbetssättet, samt en etisk
analys av er egen datahantering. Momentet ligger mitt i projektet, inte i
slutet — ni ska kunna visa hur ni planerar och arbetar, inte vad ni hann bli
klara med. Alla i gruppen ska tala, och frågor ställs till namngivna
personer.

**Moment 3 — Individuell analys av tekniskt bidrag** (lärandemål 15, 17)
En individuell text på 2–4 sidor där du redogör för vad just du byggt, vilka
tekniska val du gjort och varför, hur du anpassat verklig data för modellen,
och vad du hade gjort annorlunda. Skrivs enskilt, bedöms enskilt.

## 10. Avgränsningar

Följande ingår medvetet inte i projektet:

- Ni ska inte träna fram en modell från grunden med målet att den ska bli
  bra. En enkel basmodell räcker. Kursen handlar om infrastrukturen runt
  modellen.
- Ni ska inte sätta upp ett eget Kubernetes-kluster. 
- Ni ska inte bygga ett data warehouse eller dimensionsmodellera.
- Streaming ingår inte. Allt arbete i kursen är batch.


## 11. Praktiskt

**Grupper.** Fyra till fem studenter, satta i vecka 3. Team med godkänd egen
datakälla sätts samman utifrån vilken källa de föreslagit.

**Konton ni behöver.** GitHub (sedan vecka 1). Neon eller Supabase (vecka 3).
Hugging Face (vecka 5). Hopsworks (vecka 6, valfritt). Plus vad er egen
datakälla kräver.

**Stöd under projektet.** Handledning tre timmar per vecka, drop-in, onsdagar
9–12 online. Projektstudio på lektionstid varje tisdag- och torsdageftermiddag
från vecka 3. Frågor mellan lektionerna i kursens Teams-kanal — gärna öppet,
så att alla får svaret.

**En ärlig notis om handledningen.** Jag har testat standarduppgiftens
datakälla, API:er och modell från början till slut. Er har jag inte testat.
Jag hjälper er lika gärna och lika länge, men på er källa kommer vi ofta att
felsöka tillsammans från noll snarare än att jag vet svaret. Det är priset
för att göra något eget, och för de flesta team är det värt det.

---

*Denna projektbeskrivning kan komma att justeras under kursens gång.
Väsentliga ändringar meddelas på Itslearning och i Teams.*
