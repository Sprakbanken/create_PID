# Lag PID 
Dette repoet inneholder kode for å lage PID til språkressurser.
(Scroll down for English)

## Oppsett

Det enkleste er å installere [uv](https://docs.astral.sh/uv/#installation), og kjøre 
```bash
uv sync
```
for å installere riktig versjon av python og avhengigheter.

Eventuelt lag et virtuelt miljø manuelt og installer med pip slik:
```bash
python3 -m venv .venv
. ./venv/bin/activate
pip install .
```

### Miljøvariabler
Spør en kollega om brukernavn, passord og handle-prefiks til .env  
Se [.env-example](.env-example) for hvordan `.env`-fila skal se ut (lag en kopi, kall den `.env` og fyll inn brukernavn, passord og HANDLE_PREFIX)

## Kjør koden

Scriptet har foreløpig to kommandoer, __create__ og __list__:

### List
Denne funksjonen lager en liste over alle PIDer registrert på handle-prefikset og henter ut URLene disse peker til.

```bash
uv run main.py list
```

Første kolonne er PID, andre kolonne er PID-type (stort sett alltid URL), og tredje kolonne URLen som PIDen peker til.

F.eks.:
```csv
'76', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-76/'
'77', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-77/'
'78', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-78/'
```

### Create

Denne funksjonen lar deg opprette eller endre en gitt PID:

```bash
uv run main.py create {PID} --url [URL-for-ressurs}
```

hvor PID er IDen som skal være permanent (f.eks. en UUID) og url er URLen PIDen skal peke til.

F.eks: 
```bash
uv run main.py create 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no
```

Dette vil lage en PID for ressursen, som kan resolves via:
https://hdl.handle.net/{HANDLE_PREFIX}/23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a

Hvis PIDen allerede eksisterer, vil man få beskjed om det. Hvis man ønsker å overstyre URLen som den eksisterende PIDen viser til, kan man bruke parameteret --override.

```bash
uv run main.py create 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no --override
```
