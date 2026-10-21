<div align="center">

  <h1>🖼️ Generatore ASCII & Braille Ultra-HD</h1>

  <p><strong>Trasforma qualsiasi immagine in arte testuale ASCII o Braille ad altissima risoluzione, con output ottimizzato per Blocco Note, terminale o HTML interattivo a colori.</strong></p>

  <p>
    <a href="https://github.com/Federazione/Image-to-Ascii">
      <img src="https://img.shields.io/badge/licenza-MIT-blue.svg" alt="Licenza MIT">
    </a>
    <a href="https://github.com/Federazione/Image-to-Ascii">
      <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
    </a>
    <a href="https://github.com/Federazione/Image-to-Ascii">
      <img src="https://img.shields.io/badge/stato-attivo-success.svg" alt="Stato attivo">
    </a>
    <a href="https://github.com/Federazione/Image-to-Ascii">
      <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Piattaforma">
    </a>
    <a href="https://github.com/Federazione/Image-to-Ascii">
      <img src="https://img.shields.io/badge/dipendenze-Pillow%20%7C%20NumPy-orange.svg" alt="Dipendenze">
    </a>
  </p>

</div>

---

<h2>✨ Panoramica</h2>

<p>
  <strong>Generatore ASCII & Braille Ultra-HD</strong> è uno strumento Python avanzato che converte qualsiasi immagine in arte testuale di alta qualità, preservando i dettagli visivi anche a risoluzioni molto ridotte.
  Il progetto nasce dall'obiettivo di ottenere la <em>massima chiarezza possibile</em> nei file <code>.txt</code> per Windows Blocco Note, ma supporta anche terminale, VS Code e Discord.
</p>

<p>
  Tre modalità di rendering, un'esportazione HTML interattiva a colori con zoom in tempo reale, e un'interfaccia da riga di comando semplice e immediata.
</p>

---

<h2>🚀 Funzionalità</h2>

<ul>
  <li>🧠 <strong>Algoritmo a due stadi</strong> con downsampling piramidale Lanczos e maschera di contrasto (Unsharp Mask) multi-frequenza.</li>
  <li>⣿ <strong>Modalità Braille Ultra-HD</strong>: risoluzione effettiva 8× per carattere (2×4 dot), perfetta per dettagli fini.</li>
  <li>✍️ <strong>ASCII Crisp</strong>: rampe di caratteri calibrate per font monospace Windows (Consolas/Courier).</li>
  <li>█ <strong>Blocchi Shading</strong>: effetto pixel-art retrò con caratteri Unicode.</li>
  <li>🌐 <strong>Esportazione HTML a colori</strong>: visualizzatore interattivo con zoom in tempo reale, copia negli appunti e download del testo.</li>
  <li>🎯 <strong>Riconoscimento automatico dello sfondo</strong>: adatta l'output per Blocco Note (sfondo chiaro) o terminale (sfondo scuro).</li>
  <li>🧹 <strong>Pulizia automatica del rumore</strong>: niente pixel sporchi o "polvere" nelle zone di sfondo.</li>
  <li>📁 Supporto a <strong>PNG, JPG, WEBP</strong> e immagini con <strong>trasparenza alfa</strong>.</li>
  <li>⚡ Rendering fulmineo con <strong>NumPy vectorized</strong>: elabora immagini in millisecondi.</li>
  <li>🖱️ Interfaccia interattiva guidata + <strong>CLI completa</strong> per automazione.</li>
  <li>🪟 Launcher <strong>.bat</strong> per Windows con supporto drag-and-drop.</li>
</ul>

---

<h2>🛠️ Installazione</h2>

```bash
git clone https://github.com/Federazione/Image-to-Ascii.git
cd Image-to-Ascii
pip install Pillow numpy
```

> **Nota**: Python 3.10 o superiore è richiesto.

---

<h2>📌 Utilizzo</h2>

<h3>🖱️ Modalità Interattiva (consigliata)</h3>

Avvia semplicemente lo script e segui le istruzioni a schermo:

```bash
python image.py
```

Oppure su Windows fai doppio click su `avvia_ascii.bat` — puoi anche **trascinarci sopra un'immagine** direttamente!

<h3>⌨️ Modalità Riga di Comando (CLI)</h3>

```bash
python image.py foto.jpg --width 90 --mode all --bg light
```

```bash
python image.py foto.png -w 150 --mode braille --bg dark -o ./output
```

<h3>⚙️ Opzioni disponibili</h3>

```
percorso          Percorso del file immagine (PNG, JPG, WEBP)
-w, --width       Larghezza in caratteri (default: 90)
-m, --mode        Formato: all | braille | ascii | blocks (default: all)
--bg              Sfondo target: light (Blocco Note) | dark (Terminale) (default: light)
--no-html         Non generare la versione HTML
-o, --outdir      Cartella di destinazione dei file generati
```

---

<h2>🎨 Modalità di Output</h2>

<table>
  <thead>
    <tr>
      <th>Modalità</th>
      <th>File generato</th>
      <th>Caratteristiche</th>
      <th>Uso consigliato</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>⭐ <strong>Braille Ultra-HD</strong></td>
      <td><code>*_braille_w90.txt</code></td>
      <td>Risoluzione 8× per cella (2×4 dot)</td>
      <td>Massimo dettaglio in Blocco Note</td>
    </tr>
    <tr>
      <td>✍️ <strong>ASCII Crisp</strong></td>
      <td><code>*_ascii_w90.txt</code></td>
      <td>Rampa calibrata per monospace</td>
      <td>Look classico ad alta leggibilità</td>
    </tr>
    <tr>
      <td>█ <strong>Blocchi Shading</strong></td>
      <td><code>*_blocchi_w90.txt</code></td>
      <td>Caratteri Unicode █▓▒░</td>
      <td>Effetto pixel-art retrò</td>
    </tr>
    <tr>
      <td>🌐 <strong>HTML a Colori</strong></td>
      <td><code>*_colori_w90.html</code></td>
      <td>Colori originali, zoom in tempo reale</td>
      <td>Presentazione e condivisione</td>
    </tr>
  </tbody>
</table>

---

<h2>📐 Grandezze disponibili</h2>

<table>
  <thead>
    <tr>
      <th>Scelta</th>
      <th>Colonne</th>
      <th>Descrizione</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>40</td><td>Molto piccolo — ultra-compatto, tascabile</td></tr>
    <tr><td>2</td><td>60</td><td>Piccolo — ottimo per finestre ridotte</td></tr>
    <tr><td>3 ⭐</td><td>90</td><td><strong>Medio (consigliato)</strong> — perfetto per Blocco Note standard</td></tr>
    <tr><td>4</td><td>150</td><td>Grande — pieno schermo, molto dettagliato</td></tr>
    <tr><td>5</td><td>250</td><td>Gigante HD — risoluzione massima da poster</td></tr>
    <tr><td>–</td><td>Personalizzata</td><td>Digita qualsiasi valore (es. 45, 75, 120…)</td></tr>
  </tbody>
</table>

---

<h2>💡 Consigli d'oro per Blocco Note</h2>

> **Suggerimento**: Per la migliore esperienza con i file `.txt` su Windows Blocco Note:
> 1. Apri il file con **Blocco Note**.
> 2. Vai su **Visualizza → A capo automatico** e assicurati che sia **disattivato**.
> 3. Usa **Ctrl + rotella del mouse** per regolare lo zoom e goderti l'immagine!

---

<h2>📁 Struttura del progetto</h2>

```text
Image-to-Ascii/
├── image.py              ← Script principale (menu interattivo + CLI)
├── avvia_ascii.bat       ← Launcher Windows con supporto drag-and-drop
└── README.md
```

I file generati vengono salvati nella **stessa cartella dell'immagine sorgente** (o nella directory specificata con `-o`):

```text
mia_foto/
├── mia_foto_braille_w90.txt
├── mia_foto_ascii_w90.txt
├── mia_foto_blocchi_w90.txt
└── mia_foto_colori_w90.html
```

---

<h2>📦 Dipendenze</h2>

```bash
pip install Pillow numpy
```

| Libreria | Versione minima | Utilizzo |
|----------|----------------|---------|
| `Pillow` | 9.0+ | Caricamento, ridimensionamento e miglioramento delle immagini |
| `NumPy`  | 1.21+ | Elaborazione vettoriale ad altissima velocità |

---

<h2>🤝 Contribuire</h2>

<p>
  I contributi sono benvenuti! Se vuoi migliorare il progetto, aggiungere nuove rampe di caratteri, modalità di output o qualsiasi altra funzionalità, sentiti libero di aprire una issue o inviare una pull request.
</p>

```bash
# Crea un branch per la tua modifica
git checkout -b feature/nuova-funzionalita

# Fai le tue modifiche, poi:
git commit -m "Aggiunge nuova modalità di rendering"
git push origin feature/nuova-funzionalita
```

---

<h2>📜 Licenza</h2>

<p>
  Questo progetto è rilasciato sotto licenza <a href="https://github.com/Federazione/Image-to-Ascii">MIT</a> — libero di usare, modificare e distribuire.
</p>

---

<div align="center">
  <p><strong>Fatto con ❤️ per l'arte testuale retrò e la creatività digitale.</strong></p>
  <p><em>Massima risoluzione. Nessun compromesso.</em></p>
</div>

