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

Hvis PIDen allerede eksisterer, vil man få beskjed om det. Hvis man ønsker å overstyre URLen som den eksisterende PIDen viser til, kan man bruke parameteret --update.

```bash
uv run main.py create 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no --update
```

# Create PID (English)

This repository contains code for creating PIDs for language resources.

## Setup

The easiest way is to install [uv](https://docs.astral.sh/uv/#installation), and run:
```bash
uv sync
```
to install the correct version of Python and dependencies.

Alternatively, create a virtual environment manually and install with pip like this:
```bash
python3 -m venv .venv
. ./venv/bin/activate
pip install .
```

### Environment Variables
Ask a colleague for the username, password, and handle prefix for .env  
See [.env-example](.env-example) for how the `.env` file should look (make a copy, call it `.env`, and fill in username, password, and HANDLE_PREFIX)

## Run the Code

The script currently has two commands, __create__ and __list__:

### List
This function creates a list of all PIDs registered on the handle prefix and retrieves the URLs they point to.

```bash
uv run main.py list
```

The first column is the PID, the second column is the PID type (usually always URL), and the third column is the URL that the PID points to.

For example:
```csv
'76', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-76/'
'77', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-77/'
'78', 'URL', 'https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-78/'
```

### Create

This function allows you to create or modify a given PID:

```bash
uv run main.py create {PID} --url [URL-for-resource]
```

where PID is the ID that should be permanent (e.g., a UUID) and url is the URL the PID should point to.

For example:
```bash
uv run main.py create 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no
```

This will create a PID for the resource, which can be resolved via:
https://hdl.handle.net/{HANDLE_PREFIX}/23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a

If the PID already exists, you will be notified. If you want to override the URL that the existing PID points to, you can use the --update parameter.

```bash
uv run main.py create 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no --update
```
