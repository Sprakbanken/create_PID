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
Se [.env-example](.env-example) for hvordan `.env`-fila skal se ut (lag en kopi, kall den `.env` og fyll inn brukernavn og passord)

## Kjør koden 

```bash
uv run main.py {PID} --url [URL-for-ressurs}
```
hvor PID er IDen som skal være permanent (f.eks. en UUID) og url er URLen PIDen skal peke til.

F.eks: 
```bash
uv run main.py 23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a --url https://www.nb.no
```

Dette vil lage en PID for ressursen, som kan resolves via:
https://hdl.handle.net/{HANDLE_PREFIX}/23b9ce9d-14b9-4f7c-9b25-f305e3e7ca6a
