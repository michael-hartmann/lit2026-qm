# Quantencomputer - Funktionsweise, Anwendungen und Grenzen

Vortragsfolien zu meinem Vortrag zu Quantencomputer:

* [Vortragsbeschreibung](https://www.luga.de/static/LIT-2026/talks/quantencomputer_funktionsweise_anwendungen_und_grenzen/)
* [Präsentation](https://www.speicherleck.de/michael/lit2026-qm/)

## Präsentation bauen

Das geht am einfachsten mit [uv](https://docs.astral.sh/uv/). Erstmal ein Virtual Environment erstellen
```
uv venv
```
und aktivieren, dann die Abähngigkeiten installieren:
```
uv pip install -r requirements.txt
```

Danach können die Folien gerendert werden:
```
manim-slides render talk.py TitleSlide Overview ClassicalComputing QubitSuperposition QubitMeasurement QubitBloch QubitEntanglement QubitSummary Gates Algorithms StateOfTheArt Summary
```

Zum Präsentieren:
```
manim-slides present TitleSlide Overview ClassicalComputing QubitSuperposition QubitMeasurement QubitBloch QubitEntanglement QubitSummary Gates Algorithms StateOfTheArt Summary
```
Wenn das Präsentationsfenster sofort "abstürtzt" unter Linux, hilft es folgende Umgebungsvariable zu setzen:
```
export LIBVA_DRIVER_NAME=none
```

Und um die Präsentation nach HTML zu exportieren:
```
manim-slides convert TitleSlide Overview ClassicalComputing QubitSuperposition QubitMeasurement QubitBloch QubitEntanglement QubitSummary Gates Algorithms StateOfTheArt Summary lit2026-qm/index.html
```