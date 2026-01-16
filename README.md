# DenneSpravy
Automatický systém na vytváranie denného spravodajského digestu.  
Projekt slúži na rýchly a prehľadný súhrn najdôležitejších udalostí bez potreby manuálne čítať množstvo článkov.

Výsledkom je jeden e-mail obsahujúci tri časti:
- správy zo sveta,
- správy zo Slovenska,
- technologické správy.

## Účel projektu
Cieľom je poskytovať stručné a objektívne zhrnutie aktuálneho diania.

Systém automaticky:
- načíta články z viacerých RSS zdrojov,
- vyfiltruje ich podľa času a relevancie,
- pomocou OpenAI API vyberie najdôležitejšie udalosti,
- vytvorí zrozumiteľný textový prehľad,
- odošle výsledok e-mailom.

## Štruktúra projektu
Projekt je rozdelený na menšie moduly:

**main.py**  
Hlavný skript, ktorý spúšťa spracovanie všetkých sekcií a odosiela finálny e-mail.

**digest_section.py**  
Obsahuje triedu `DigestSection`, ktorá zabezpečuje:
- načítanie RSS článkov,
- filtrovanie a spracovanie,
- generovanie promptu,
- volanie OpenAI API,
- vytvorenie textového súhrnu.

**feeds.py**  
Definuje RSS zdroje pre jednotlivé kategórie správ.

**prompts.py**  
Obsahuje prompty pre generovanie digestu:
- svetové správy v angličtine,
- slovenské správy po slovensky,
- technologické správy v angličtine.

**email_sender.py**  
Modul na odoslanie e-mailu vrátane HTML formátovania.

**requirements.txt**  
Zoznam potrebných Python knižníc.

**.github/workflows/digest.yml**  
GitHub Actions workflow pre automatické spúšťanie projektu.

## Ako systém funguje
1. GitHub Actions spustí skript podľa nastaveného času.  
2. Pre každú sekciu sa načítajú a spracujú najnovšie články.  
3. OpenAI API vytvorí súhrn najdôležitejších udalostí.  
4. Všetky sekcie sa spoja do jedného textu.  
5. Výsledný digest je odoslaný e-mailom.

Zoznam príjemcov nie je uložený v tomto repozitári, ale v samostatnom súkromnom repozitári.

## Použité technológie
- Python  
- OpenAI API  
- RSS (feedparser)  
- Gmail SMTP  
- GitHub Actions

## Príklad výstupu:

Subject: Správy (svet, Slovensko, technológie) za posledných 12 hodín
Message:

[WORLD]
1. Uganda election: Museveni leads amid reports of intimidation and violence
(IMPORTANCE: 8/10)
Sources: BBC World; FT World; The Guardian; DW World

President Yoweri Museveni held a strong early lead in the Ugandan presidential vote, with BBC reporting he had about 75% of the vote from results in more than half of polling stations and DW noting an early lead. FT says the contest has been clouded by an internet blackout, widespread reports of rigging and intimidation, and opposition arrests. The Guardian reports a senior opposition MP saying security forces stormed his home and that 10 campaign staff were killed; FT and the Guardian both record broader allegations of violence and intimidation. Election authorities’ next steps were not confirmed in the sources provided.

2. Iran: protests continue under internet blackout as opposition calls for outside help
(IMPORTANCE: 9/10)
Sources: Al Jazeera; BBC World; The Guardian; FT World

Iran remains under a government-imposed internet blackout as mass protests continue and armed forces have a heavy presence on the streets, Al Jazeera and BBC report. BBC and the Guardian note US-based opposition figure Reza Pahlavi has publicly urged international action targeting Iran’s Revolutionary Guards leadership and said he is positioned to lead a successor government. FT and Al Jazeera detail an unprecedented crackdown as authorities retook the streets, but the immediate political outcome inside Iran is not confirmed by multiple sources.

3. CIA director meets Venezuela’s new leader amid political upheaval
(IMPORTANCE: 8/10)
Sources: FT World; BBC World; The Guardian

The US intelligence director held a two-hour meeting in Caracas with Venezuela’s new interim leader, FT and BBC report, with a US official saying discussions covered economic opportunities and preventing Venezuela from becoming a base for “America’s adversaries.” The Guardian and FT add that the visit came less than two weeks after US agents were reported to have helped remove Nicolás Maduro and as opposition figure María Corina Machado vowed she would become the country’s president. The talks signal active US engagement with Venezuela’s new authorities; no formal outcomes of the meeting were reported in the cited pieces.

4. Canada and China agree to cut tariffs on key goods as ties are rebuilt
(IMPORTANCE: 6/10)
Sources: FT World; BBC World; Al Jazeera; The Guardian

Canada’s prime minister Mark Carney made a rare visit to Beijing and announced a deal with China to slash tariffs on goods including electric vehicles and canola, BBC and Al Jazeera report. FT says the tariff relief and other measures came during the first visit by a Canadian leader to Beijing in almost a decade, part of an effort to mend strained ties and diversify trade. Al Jazeera notes Canada agreed to allow 49,000 Chinese EVs into its market at a reduced tariff (down from 100% to 15% per one report), prompting criticism from the United States. The deal is presented as the start of a broader strategic partnership but further implementation details were not jointly confirmed across sources.

5. Russia-Ukraine conflict: strikes damage infrastructure and civilians face detention and hardship
(IMPORTANCE: 9/10)
Sources: Al Jazeera; DW World; The Guardian

Russian attacks have struck Ukraine’s infrastructure, worsening energy shortages and forcing emergency electricity imports as civilians endure sub-freezing temperatures, Al Jazeera reports. DW documents widespread abuses connected to the conflict, including alleged torture and false arrests of Ukrainian civilians, noting thousands are held in Russian custody and more than 2,000 of them are women. The combined reporting indicates both immediate humanitarian impacts from attacks on energy systems and broader concerns about civilian detention and mistreatment; specific casualty or damage totals were not consistently reported across the sources.

[SLOVENSKO]
1. Evakuácia a dočasné zatvorenie veľvyslanectva SR v Iráne
(DÔLEŽITOSŤ: 7/10)
Zdroje: Aktuality Domáce, teraz.sk (TASR), SME Domov

Minister J. Blanár rozhodol 16. januára 2026 o evakuácii a dočasnom uzatvorení zastupiteľského úradu Slovenskej republiky v Iráne ako preventívne opatrenie pri zhoršujúcej sa bezpečnostnej situácii (Aktuality; teraz.sk). Minister ocenil pripravenosť a koordináciu zapojených zložiek pri evakuácii a označil rozhodnutie za preventívny krok (teraz.sk; Aktuality). SME tiež informuje o rozhodnutí ministra a uvádza dôvod v podobe zhoršenej bezpečnostnej situácie v Iráne. Nie sú v poskytnutých zdrojoch detailné informácie o počte evakuovaných osôb ani o termíne opätovného otvorenia; ide o dočasné uzatvorenie podľa vyjadrení ministra.

2. Minister Šaško nariadil audit verejných obstarávaní v rezorte zdravotníctva
(DÔLEŽITOSŤ: 6/10)
Zdroje: teraz.sk (TASR), Pravda, SME Domov, Aktuality Domáce

Minister zdravotníctva Kamil Šaško nariadil audit verejných obstarávaní na svojom rezorte po podnetoch zamestnancov; oznámenie zverejnili 16. januára 2026 (teraz.sk; Pravda; SME; Aktuality). Cieľom auditu má byť preverenie, či obstarávania prebehli v súlade so zákonom a zabezpečenie transparentnosti; Pravda citovala vyjadrenie ministra o nulovej tolerancii voči pochybeniam. SME a ďalšie zdroje uvádzajú, že audit nasledoval po otázkach a podnetoch (whistlebloweri) a prišiel v deň, keď denník SME položil rezortu otázky o údajne predražených zákazkách. V článkoch nie sú uvedené konkrétne výsledky auditu ani termín jeho ukončenia.

3. Polícia obvinila vládneho splnomocnenca Petra Kotlára; opozícia a politici žiadajú odchod alebo ďalšie kroky
(DÔLEŽITOSŤ: 7/10)
Zdroje: Pravda, SME Domov, teraz.sk (TASR)

Podľa viacerých správ polícia obvinila Petra Kotlára zo šírenia poplašnej správy; informácie o obvinení sú v článkoch z 16. januára 2026 (Pravda; SME). Pravda uvádza, že trestné stíhanie voči Kotlárovi začalo už vlani v polovici októbra a Kotlár sa z funkcie splnomocnenca odstúpiť neplánuje (Pravda). Poslanec Oskar Dvořák z Progresívneho Slovenska vyzval ministra Šaška, aby trval na odchode Kotlára z funkcie (teraz.sk; SME). V zverejnených materiáloch nie sú podrobné informácie o obsahu obvinenia alebo o viacerých procesných krokoch; Kotlár podľa dostupných textov zatiaľ neoznámil odstúpenie.

4. Rada prokurátorov SR sa postavila proti novele Trestného zákona z dielne SNS
(DÔLEŽITOSŤ: 6/10)
Zdroje: SME Domov, Aktuality Domáce, teraz.sk (TASR), Pravda

Rada prokurátorov SR oficiálne nesúhlasí s navrhovanou novelou Trestného zákona predloženej stranou SNS; vyjadrenie o odmietnutí a upozornení na právne a kriminologické riziká publikovali 16. januára 2026 (SME; Aktuality; teraz.sk; Pravda). Rada konštatovala, že návrh nie je odbornou revíziou, ale predstavuje nebezpečný zásah do mechanizmov ochrany demokracie, ktorý môže viesť k nárastu násilia a intolerancie (Aktuality; SME). V materiáloch sa uvádza aj varovanie pred právnymi deficitmi a kriminologickým rizikom návrhu (teraz.sk; Pravda). Z dostupných zdrojov nie je potvrdené, či vláda alebo predkladateľ plánujú upraviť návrh v reakcii na výhrady.

5. Cesta premiéra Fica do USA a spor o jadrovú energetiku (Jaslovské Bohunice); opozícia žiada mimoriadny výbor
(DÔLEŽITOSŤ: 6/10)
Zdroje: teraz.sk (TASR), SME Domov, Aktuality Domáce, Pravda

Premiér Robert Fico odcestoval do USA (správy 16. januára 2026) a obhajoval cestu ako v súlade so suverénnou zahraničnou politikou; TASR a SME citujú jeho vyjadrenia, že Slovensko potrebujú nové zdroje pre výrobu elektrickej energie (teraz.sk; SME). Fico v súvislosti s jadrovou energiou tvrdí, že treba využiť pripravenosť územia v Jaslovských Bohuniciach na výstavbu nového jadrového bloku (Pravda; SME). Opozícia (Progresívne Slovensko) žiada zvolanie mimoriadneho hospodárskeho výboru k premiérovej ceste do USA a PS aj ďalšími subjektmi spochybňujú plán na novú atómku a varujú pred zadlžením generácií (Aktuality; SME; Pravda). V článkoch nie sú uvedené konkrétne zmluvné detaily ani schválené finančné záväzky súvisiace s projektom.

[TECH]
1. Trump administration and Mid‑Atlantic governors push PJM to hold emergency power auction for new plants
(IMPORTANCE: 6/10)
Sources: The Verge; TechCrunch

The White House, joined by a bipartisan group of Mid‑Atlantic governors, is pressuring PJM Interconnection—the largest U.S. electricity market—to run an “emergency” capacity auction that would spur a large buildout of new power plants. Officials want the auction to secure long‑term (15‑year) contracts for generating capacity; the administration is also seeking to have major tech companies bid in order to underwrite roughly $15 billion of new plants, a proposal framed as a response to rising electricity prices. The push has raised concern that companies could be asked to buy generation they may not ultimately need and creates political pressure on PJM’s market design decisions.

2. OpenAI to start showing ads in ChatGPT and expands lower‑cost ChatGPT Go tier globally
(IMPORTANCE: 5/10)
Sources: The Verge; TechCrunch; Wired

OpenAI will begin testing clearly labeled, targeted ads in ChatGPT for logged‑in U.S. users of the free app and some paying tiers, starting with shopping links and related sponsored products; the company says ads won’t change ChatGPT’s responses and that it will not sell user data to advertisers. At the same time, OpenAI is rolling out a lower‑cost subscription tier, ChatGPT Go, globally after earlier launches in India and other markets. The company says users impacted by ads will have some controls over what they see; the moves mark a shift in OpenAI’s consumer monetization strategy by combining cheaper subscriptions with ad testing.

3. X (formerly Twitter) suffers a global outage — second major downtime this week
(IMPORTANCE: 4/10)
Sources: The Verge; TechCrunch

X and its Grok chatbot experienced a widespread outage affecting web and app access, with outage reports spiking on DownDetector and ThousandEyes showing problems across many servers; this was the service’s second significant outage within the same week. Reports noted tens of thousands of user complaints and degraded availability that affected global user access for an hour or more, highlighting ongoing reliability challenges for the platform.

4. Canada agrees to sharply cut tariffs on Chinese electric vehicles, opening market to imports
(IMPORTANCE: 4/10)
Sources: The Verge; TechCrunch

Canada announced a deal with China to significantly reduce tariffs on Chinese electric vehicles, initially allowing up to 49,000 Chinese EVs at a 6.1% tariff (down from much higher duties), in exchange for lower duties on Canadian canola exports. The move lowers a major barrier to Chinese EVs entering North American markets and could shift regional auto‑trade dynamics, prompting questions about whether the U.S. will follow with similar tariff changes.

5. xAI faces legal and regulatory scrutiny in separate reports
(IMPORTANCE: 4/10)
Sources: TechCrunch; Ars Technica

Two separate pieces in the news list report legal and regulatory troubles involving Elon Musk’s xAI: TechCrunch reports the EPA ruled that xAI installed and operated 35 natural‑gas turbines without required permits, finding that use illegal; Ars Technica reports that the mother of one of Musk’s children has sued xAI, alleging the company’s Grok chatbot produced numerous sexualized deepfake images of her without consent. Taken together, the reports indicate xAI is confronting both environmental‑regulatory scrutiny and litigation over alleged harms from its AI outputs.


