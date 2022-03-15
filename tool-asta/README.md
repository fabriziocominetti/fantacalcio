# Tool Asta Fantacalcio

-- Project status: [Completed]

## About

Tool per guida asta fantacalcio. Prende in input i dati delle quotazioni dei giocatori e delle statistiche delle ultime tre stagioni scaricabili dal sito ufficiale di Fantagazzetta. L'output consiste in 4 fogli excel contenenti alcuni indici relativi alla convenienza d'acquisto dei vari giocatori all'asta.

## Repository overview

```
├── README.md
├── data
    ├── input
    ├── output
└── fanta.py
```

## Installation & Usage

Per utilizzare questo tool è necessario scaricare i file excel di interesse dal sito fantagazzetta ed inserirli nella cartella "data/input". Una volta eseguito, il notebook produrrà in output i quattro dataset finali.

Download data:

- quotazioni: https://www.fantacalcio.it/quotazioni-fantacalcio
- votazioni: https://www.fantacalcio.it/statistiche-serie-a/2021-22/fantacalcio/medie

#### Acknowledgments & Inspiration

Thank you to:

- https://github.com/piopy/fantacalcio-py