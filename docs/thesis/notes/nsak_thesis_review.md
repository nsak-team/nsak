- Verwendung von AI/Zitieren/Korrekturen/Ehrlichkeitserklärung: Gibt es dafür einen BFH Standard? In der Einleitung schreiben, ob und wie AI zur Erstellung der Thesis verwendet wurde.

  - ~~Tabelle 2.1 vergleicht Metasploit, Atomic Red Team und Caldera, aber NSAK fehlt als Spalte — der Vergleich ist nur in Prosatext (Section 2.1.4), nicht in der Tabelle selbst.~~

- ~~Was hat NSAK vor dieser Arbeit bereits gekonnt? Was habt ihr neu gebaut vs. übernommen? (Section 3.1 ist sehr knapp und zeigt das nicht klar.)~~

- Eventuell C4 Architektur-Diagramm, von den relevanten Teilen? Das System hat viele Schichten (CLI, Config, Drills, Scenarios, AI Agent, LangChain) — eine visuelle Übersicht würde helfen.

- ~~Seite 4: Querverweise "2.1.12.1.22.1.3": Sections 2.1.1, 2.1.2, 2.1.3 ohne Trennzeichen zusammengeschrieben, Formatierungsfehler.~~

- ~~Seite 8, Fehlt etwas:
  "...Recently, other concepts for call-ing tools were established, such as . ..."~~

- ~~Seite 8: "heavily relly on tool usage" → rely~~

- ~~Listing 28, Seite 154, Wäre es nicht `nsak device --help` statt `nsak device --list` ?~~

[//]: # (need to be confirmed)
- Seite 27, 4748 -> 47,48

[//]: # (need to be )
- Seite 41, Wie wird Success Factor gemessen? Ist das die Anzahl Durchläufe, um 10 Durchläufe mit  "minimalem" Resultat zu erhalten? Nenner ist immer 10. Wie wertet ihr einen Success?

- Seite 41/54, Die Durchschnittswerte in den Tabellen 6.2/6.3 sind nur über erfolgreiche Durchläufe berechnet ("the reported averages reflect a filtered best-case subset", Seite 54). Bei einem Success Factor von z.B. 10/23 ist das irreführend — bitte direkt bei den Tabellen darauf hinweisen, nicht nur in den Limitations.

- Seite 50, eine Theorie warum nur 6 von 109 Versuchen funktionierten? Was ist die "nicht-deterministische" Komponente?

- Seite 56: "show that teh operator must still be alert" → the

- Der Prompt wurde als fixe Konstante behandelt, aber seine Gestaltung beeinflusst die Resultate, insbesondere für kleinere Modelle. War der Prompt auf ein bestimmtes Modell optimiert? Wurde er iteriert? Das sollte als Limitation diskutiert werden.

- Das Schema des strukturierten Outputs (Feldnamen, Typen) beeinflusst möglicherweise, worauf das Modell beim Scannen achtet. Dieser Einfluss wird nicht diskutiert.

- Bibliographie: Generell fehlen bei vielen Webquellen URLs (z.B. [7], [8], [9], [24], [25], [26], [28], [30], [31]).

- Seite 68, Glossary fehlt
