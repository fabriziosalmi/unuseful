# Unuseful Web Interface

Questa è l'interfaccia web per l'archivio digitale di Unuseful. Fornisce una visualizzazione interattiva dei frammenti di codice raccolti, con funzionalità di ricerca, filtraggio e visualizzazione dei pattern cognitivi.

## Caratteristiche

- 🎨 Tema chiaro/scuro personalizzabile
- 📱 Design responsive per desktop e mobile
- 🔍 Ricerca full-text nei frammenti
- 🏷️ Filtraggio per tipo di file e pattern cognitivi
- 📊 Visualizzazioni interattive dei pattern
- ⌛ Timeline temporale dei frammenti
- ✨ Syntax highlighting per Python e Jupyter
- 📋 Vista a griglia/lista configurabile

## Struttura

```
docs/
├── index.html          # Pagina principale
├── css/
│   └── style.css      # Stili dell'interfaccia
├── js/
│   └── app.js         # Logica applicativa
└── README.md          # Documentazione
```

## Dipendenze

- [Prism.js](https://prismjs.com/) - Syntax highlighting
- [Chart.js](https://www.chartjs.org/) - Visualizzazioni interattive

## Sviluppo

Per lavorare sul sito localmente:

1. Clona il repository
2. Naviga nella directory `docs`
3. Avvia un server locale (es. `python -m http.server 8000`)
4. Apri `http://localhost:8000` nel browser

## Note

Il sito legge i dati dal file `memorie/_metadata/index.json` che viene generato e aggiornato automaticamente dall'archivist.
