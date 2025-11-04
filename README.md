# Lag PID 
Dette repo inneholder kode for å lage PID til ressurser i ressurskatalogen (for å føre opp i COMEDI metadata)
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
. .venv/bin/activate
pip install .
```

### Miljøvariabler
Spør en kollega om brukernavn og passord til .env  
Se .env-example for hvordan .env fila skal se ut (lag en kopi, kall den .env og fyll inn brukernavn og passord)

## Kjør koden 

```bash
uv run main.py {sbr-num}
```
hvor sbr-num er språkbank-ressurs-nummeret, altså tallet i urlen i ressurskatalogen (https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-{sbr-num}). 

F.eks: 
```bash
uv run main.py 105
```

Dette vil lage en PID for ressursen, og printe det du skal putte i PID-feltet i COMEDI 

### Flagg
Du kan kjøre skriptet med flagget -c for å sjekke om alle nummer fra 1 opp til sbr-num har en PID  
Du kan kjøre skriptet med flagget -c og -a for å lage PID for alle nummer fra 1 opp til sbr-num som ikke har en PID


# Create PID

This repository contains code for creating PIDs (Persistent Identifiers) for resources in the resource catalog (for inclusion in COMEDI metadata).

## Setup

The easiest way is to install [uv](https://docs.astral.sh/uv/#installation) and run:
```bash
uv sync
```
to install the correct version of Python and dependencies.

Alternatively, create a virtual environment manually and install with pip:
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install .
```

### Environment Variables
Ask a colleague for the username and password for the `.env` file.  
See `.env-example` for how the `.env` file should look (make a copy, name it `.env`, and fill in the username and password).

## Run the Code

```bash
uv run main.py {sbr-num}
```
where `sbr-num` is the language bank resource number, i.e. the number in the url of the resource catalogue (https://www.nb.no/sprakbanken/ressurskatalog/oai-nb-no-sbr-{sbr-num}).

For example:
```bash
uv run main.py 105
```

This will create a PID for the resource and print what you should enter in the PID field in COMEDI.

### Flags
You can run the script with the `-c` flag to check if all numbers from 1 up to sbr-num have a PID.  
You can run the script with the `-c` and `-a` flags to create PIDs for all numbers from 1 up to sbr-num that don't have a PID.
