#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
         ✨ GENERATORE ASCII & BRAILLE ULTRA-HD PER BLOCCO NOTE ✨
          Massima Risoluzione e Chiarezza anche in Formati Piccoli
================================================================================
Caratteristiche:
- Qualità assurda nei file .txt per Blocco Note anche a dimensioni ridotte (30-80 col)
- Algoritmo a due stadi con preservazione attiva dei contorni e maschera di contrasto
- Pulizia automatica dello sfondo (niente pixel sporchi o muri di testo nero)
- Modalità Braille Ultra-HD: risoluzione 8x sub-pixel (2x4 dots per carattere)
- Rampe ad alto contrasto calibrate per i font monospace di Windows (Consolas/Courier)
- Riconoscimento intelligente sfondo scuro/chiaro dell'immagine
- Esportazione HTML interattiva a colori con zoom in tempo reale
- Interfaccia semplice, carina e veloce (premi Invio e fa tutto da solo!)
================================================================================
"""

import sys
import os
import math
import time
import json
import argparse
import shutil
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np

# Configurazione UTF-8 per la console Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ==============================================================================
# RAMPE DI CARATTERI PER BLOCCO NOTE
# ==============================================================================
# Rampa Micro ad Alta Leggibilità: perfetta per formati piccoli (40-100 colonne)
# Ogni carattere ha un peso visivo netto e distinto nei font monospace
RAMP_CRISP_SMALL = "@#WM8&o*+=~:,. "

# Rampa Estesa a 70 caratteri per formati grandi (150+ colonne)
RAMP_ULTRA_70 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Rampa Blocchi Unicode (stile pixel-art retrò solido e nitidissimo)
RAMP_BLOCKS = "█▓▒░ "

# Rampa Classica minimale a 10 caratteri
RAMP_STANDARD_10 = "@%#*+=-:. "


# ==============================================================================
# PULIZIA PERCORSI E FILE
# ==============================================================================
def pulisci_percorso(path: str) -> str:
    """Pulisce percorsi con apici, virgolette o sintassi PowerShell drag-and-drop (& 'path')."""
    if not path:
        return ""
    p = path.strip()
    if p.startswith("&"):
        p = p[1:].strip()
    p = p.strip("\"'")
    p = os.path.expanduser(os.path.expandvars(p))
    return p


def formatta_dimensione(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    elif b < 1024 * 1024:
        return f"{b / 1024:.1f} KB"
    return f"{b / (1024 * 1024):.2f} MB"


# ==============================================================================
# ANALISI INTELLIGENTE DELL'IMMAGINE
# ==============================================================================
def rileva_sfondo_scuro(img_gray: Image.Image) -> bool:
    """
    Analizza i bordi perimetrali dell'immagine per capire se ha uno sfondo scuro o chiaro.
    Restituisce True se lo sfondo originale è scuro.
    """
    arr = np.array(img_gray)
    h, w = arr.shape
    if h < 4 or w < 4:
        return False
    # Campiona i bordi esterni (primi 2 pixel di bordo)
    bordi = np.concatenate([
        arr[0:2, :].flatten(),
        arr[-2:, :].flatten(),
        arr[:, 0:2].flatten(),
        arr[:, -2:].flatten()
    ])
    luminanza_media_bordo = float(np.mean(bordi))
    return luminanza_media_bordo < 115.0


def carica_e_ottimizza_sorgente(percorso: str) -> tuple[Image.Image, Image.Image, bool]:
    """
    Carica l'immagine, gestisce i canali alfa trasparenti e rileva lo sfondo.
    Restituisce (img_rgb, img_gray, ha_sfondo_scuro).
    """
    p = pulisci_percorso(percorso)
    if not os.path.isfile(p):
        raise FileNotFoundError(f"Impossibile trovare il file: '{p}'")

    img = Image.open(p)

    # Gestione trasparenze (PNG / WEBP)
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        rgba = img.convert("RGBA")
        # Composita su sfondo bianco per rilevamento pulito
        sfondo_bianco = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        img_rgb = Image.alpha_composite(sfondo_bianco, rgba).convert("RGB")
    else:
        img_rgb = img.convert("RGB")

    img_gray = img_rgb.convert("L")
    ha_sfondo_scuro = rileva_sfondo_scuro(img_gray)

    return img_rgb, img_gray, ha_sfondo_scuro


# ==============================================================================
# MOTORE DI DOWN-SAMPLING AD ALTISSIMA DEFINIZIONE PER FORMATI PICCOLI
# ==============================================================================
def downsample_ad_alta_definizione(
    img_gray: Image.Image,
    target_w: int,
    target_h: int,
    per_blocco_note: bool = True,
    ha_sfondo_scuro: bool = False,
    contrasto: float = 1.8,
    nitidezza: float = 1.8
) -> np.ndarray:
    """
    Segreto dell'alta risoluzione nei formati piccoli:
    1. Autocontrasto dinamico iniziale
    2. Ridimensionamento a due stadi (piramide 2.5x) per non perdere dettagli sottili
    3. Maschera di contrasto locale (Unsharp Mask) a frequenze multiple
    4. Adattamento invertito intelligente per Blocco Note:
       Lo sfondo diventa sempre CARTA BIANCA PULITA (spazi), mentre il soggetto
       ha linee e tratti definiti in inchiostro scuro.
    5. Curva a S (Sigmoide) con soppressione del rumore di fondo.
    """
    # 1. Autocontrasto per saturare lo spettro dinamico
    img_opt = ImageOps.autocontrast(img_gray, cutoff=0.5)

    # 2. Piramide a due stadi per formati piccoli (<= 140 colonne)
    if target_w <= 140:
        inter_w = max(target_w * 2, 120)
        inter_h = max(target_h * 2, 60)
        inter = img_opt.resize((inter_w, inter_h), Image.Resampling.LANCZOS)
        # Esaltazione contorni a scala intermedia
        inter = ImageEnhance.Contrast(inter).enhance(contrasto)
        inter = inter.filter(ImageFilter.UnsharpMask(radius=2.2, percent=240, threshold=1))
        # Scalatura finale a target
        final_img = inter.resize((target_w, target_h), Image.Resampling.LANCZOS)
        final_img = final_img.filter(ImageFilter.UnsharpMask(radius=0.9, percent=180, threshold=1))
    else:
        # Per formati grandi, unsharp mask diretto
        img_opt = ImageEnhance.Contrast(img_opt).enhance(contrasto)
        img_opt = img_opt.filter(ImageFilter.UnsharpMask(radius=1.8, percent=170, threshold=2))
        final_img = img_opt.resize((target_w, target_h), Image.Resampling.LANCZOS)
        final_img = final_img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=140, threshold=1))

    arr = np.array(final_img, dtype=np.float32)

    # 3. Adattamento sfondo per Blocco Note (carta bianca) vs Terminale (sfondo scuro)
    if per_blocco_note:
        # In Blocco Note (sfondo bianco):
        # I tratti del disegno devono essere scuri (valori bassi = caratteri densi @ #)
        # Lo sfondo deve essere bianco puro (valori alti = spazi ' ')
        if ha_sfondo_scuro:
            # L'immagine originale era su sfondo scuro: invertiamo per avere soggetto su carta bianca
            arr = 255.0 - arr
        # Pulizia dello sfondo bianco per eliminare il 'rumore' di puntini grigi
        arr[arr >= 222.0] = 255.0
        # Rafforzamento dei contorni scuri per renderli netti
        arr[arr <= 65.0] = 0.0
    else:
        # Su terminale / VS Code (sfondo scuro):
        # Valori alti = caratteri densi luminosi; Valori bassi = spazi scuri
        if not ha_sfondo_scuro:
            arr = 255.0 - arr
        arr[arr <= 35.0] = 0.0
        arr[arr >= 195.0] = 255.0

    # 4. Curva tonale sigmoidea per chiaroscuri incisivi
    norm = arr / 255.0
    k = 6.0
    x0 = 0.5
    sig = 1.0 / (1.0 + np.exp(-k * (norm - x0)))
    sig = (sig - sig.min()) / (sig.max() - sig.min())
    arr_final = sig * 255.0

    return np.clip(arr_final, 0.0, 255.0)


# ==============================================================================
# GENERAZIONE TESTO ASCII AD ALTA DEFINIZIONE
# ==============================================================================
def genera_testo_ascii(
    arr_luminanza: np.ndarray,
    rampa: str,
    per_blocco_note: bool = True
) -> str:
    """
    Mappa i valori di luminanza nella rampa scelta con vettorizzazione istantanea NumPy.
    """
    # Se per Blocco Note (sfondo bianco):
    # 0 (inchiostro scuro) -> rampa[0] (carattere denso @ #)
    # 255 (carta bianca) -> rampa[-1] (spazio ' ')
    if per_blocco_note:
        rampa_usata = rampa
    else:
        # Su sfondo scuro: 0 (sfondo nero) -> spazio; 255 (luce) -> carattere denso
        rampa_usata = rampa[::-1]

    n_livelli = len(rampa_usata)
    ramp_arr = np.array(list(rampa_usata))

    indici = (arr_luminanza * (n_livelli - 1) / 255.0).round().astype(np.int32)
    np.clip(indici, 0, n_livelli - 1, out=indici)

    grid = ramp_arr[indici]
    righe = ["".join(r) for r in grid]
    return "\n".join(righe)


# ==============================================================================
# GENERAZIONE BRAILLE ULTRA-HD (RISOLUZIONE 8X PER BLOCCO NOTE)
# ==============================================================================
def genera_braille_ultra_hd(
    img_gray: Image.Image,
    target_w: int,
    aspect: float = 0.45,
    per_blocco_note: bool = True,
    ha_sfondo_scuro: bool = False,
    contrasto: float = 1.8
) -> str:
    """
    Genera arte testuale Braille Unicode (2x4 dots per carattere cella).
    A parità di colonne, genera 8 VOLTE più dettagli grafici!
    Anche a sole 50 colonne, la risoluzione effettiva è 100x92 punti!
    """
    dot_w = target_w * 2
    # I dot Braille hanno proporzione ~1:1, quindi correggiamo l'altezza
    dot_h = int(dot_w * (img_gray.height / img_gray.width) * (aspect * 2.05))
    dot_w = max(2, ((dot_w + 1) // 2) * 2)
    dot_h = max(4, ((dot_h + 3) // 4) * 4)

    # Ridimensionamento ad alta precisione
    res = img_gray.resize((dot_w, dot_h), Image.Resampling.LANCZOS)
    res = ImageOps.autocontrast(res, cutoff=1)
    res = ImageEnhance.Contrast(res).enhance(contrasto)
    res = res.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=1))

    arr_res = np.array(res, dtype=np.float32)

    # Pulizia soglie per evitare polvere di dithering nello sfondo
    if per_blocco_note:
        if ha_sfondo_scuro:
            arr_res = 255.0 - arr_res
        arr_res[arr_res >= 225.0] = 255.0
        arr_res[arr_res <= 55.0] = 0.0
    else:
        if not ha_sfondo_scuro:
            arr_res = 255.0 - arr_res
        arr_res[arr_res <= 30.0] = 0.0
        arr_res[arr_res >= 200.0] = 255.0

    img_cleaned = Image.fromarray(np.clip(arr_res, 0, 255).astype(np.uint8))

    # Dithering a 1 bit
    bw = img_cleaned.convert("1", dither=Image.Dither.FLOYDSTEINBERG)
    arr_bw = np.array(bw)

    # In Blocco Note (carta bianca): i punti attivi Braille (neri) sono i pixel scuri (0)
    if per_blocco_note:
        dots = (arr_bw == 0)
    else:
        dots = (arr_bw > 0)

    # Pesi Braille Unicode
    pesi = np.array([
        [1,  8],
        [2, 16],
        [4, 32],
        [64, 128]
    ], dtype=np.uint16)

    h_chars = dot_h // 4
    w_chars = dot_w // 2

    blocchi = dots.reshape(h_chars, 4, w_chars, 2).transpose(0, 2, 1, 3)
    codici = 0x2800 + (blocchi * pesi).sum(axis=(-2, -1))

    # Sostituiamo il carattere Braille vuoto (0x2800) con un vero spazio ASCII ' '
    # per garantire la totale trasparenza e allineamento perfetto in Blocco Note
    righe = []
    for riga in codici:
        righe.append("".join((' ' if c == 0x2800 else chr(c)) for c in riga))

    return "\n".join(righe)


# ==============================================================================
# GENERATORE HTML A COLORI INTERATTIVO HD (COMPRESSIONE RLE)
# ==============================================================================
def genera_html_hd(
    img_rgb: Image.Image,
    target_w: int,
    target_h: int,
    percorso_output: str,
    titolo: str = "ASCII Art HD"
) -> str:
    """Genera visualizzatore HTML interattivo con controlli di zoom in tempo reale."""
    resized_rgb = img_rgb.resize((target_w, target_h), Image.Resampling.LANCZOS)
    resized_rgb = ImageEnhance.Contrast(resized_rgb).enhance(1.4)
    gray = resized_rgb.convert("L")

    rgb_arr = np.array(resized_rgb, dtype=np.uint8)
    gray_arr = np.array(gray, dtype=np.float32)

    rampa = RAMP_CRISP_SMALL[::-1]
    n_lev = len(rampa)
    ramp_arr = np.array(list(rampa))
    indici = (gray_arr * (n_lev - 1) / 255.0).round().astype(np.int32)
    np.clip(indici, 0, n_lev - 1, out=indici)
    char_grid = ramp_arr[indici]

    righe_html = []
    righe_txt = []
    for y in range(target_h):
        parti = []
        riga_t = []
        cur_col = None
        cur_chars = []
        for x in range(target_w):
            r, g, b = rgb_arr[y, x]
            ch = char_grid[y, x]
            riga_t.append(ch)
            r_q, g_q, b_q = (r // 4) * 4, (g // 4) * 4, (b // 4) * 4
            hex_c = f"#{r_q:02x}{g_q:02x}{b_q:02x}"
            if hex_c == cur_col:
                cur_chars.append(ch)
            else:
                if cur_col:
                    t_safe = "".join(cur_chars).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    parti.append(f"<span style='color:{cur_col}'>{t_safe}</span>")
                cur_col = hex_c
                cur_chars = [ch]
        if cur_chars:
            t_safe = "".join(cur_chars).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            parti.append(f"<span style='color:{cur_col}'>{t_safe}</span>")
        righe_html.append("".join(parti))
        righe_txt.append("".join(riga_t))

    html_body = "\n".join(righe_html)
    raw_text = "\n".join(righe_txt)
    raw_json = json.dumps(raw_text)

    doc = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titolo} - Visualizzatore HD</title>
    <style>
        :root {{
            --bg: #0d1117;
            --panel: rgba(22, 27, 34, 0.85);
            --text: #e6edf3;
            --accent: #58a6ff;
        }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            background: var(--bg);
            color: var(--text);
            font-family: system-ui, -apple-system, sans-serif;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }}
        .toolbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: var(--panel);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .title {{ font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 8px; }}
        .badge {{ background: rgba(88,166,255,0.2); color: var(--accent); padding: 3px 8px; border-radius: 10px; font-size: 11px; }}
        .controls {{ display: flex; align-items: center; gap: 12px; font-size: 13px; }}
        button {{
            background: rgba(255,255,255,0.08);
            color: var(--text);
            border: 1px solid rgba(255,255,255,0.15);
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 12px;
            transition: 0.15s;
        }}
        button:hover {{ background: #1f6feb; color: #fff; }}
        input[type="range"] {{ accent-color: var(--accent); cursor: pointer; width: 80px; }}
        .viewer {{ flex: 1; padding: 25px; display: flex; justify-content: center; overflow: auto; }}
        #art {{
            font-family: "Cascadia Code", "Consolas", monospace;
            font-size: 8px;
            line-height: 0.55;
            letter-spacing: 0;
            white-space: pre;
            font-variant-ligatures: none;
            user-select: text;
        }}
        .light {{ --bg: #ffffff; --panel: rgba(246,248,250,0.9); --text: #1f2328; }}
        .toast {{
            position: fixed; bottom: 20px; right: 20px; background: #238636; color: #fff;
            padding: 8px 16px; border-radius: 6px; font-size: 12px; font-weight: 600;
            opacity: 0; transition: opacity 0.3s; pointer-events: none;
        }}
        .toast.show {{ opacity: 1; }}
    </style>
</head>
<body>
    <div class="toolbar">
        <div class="title">
            🖼️ <span>{titolo}</span>
            <span class="badge">{target_w}×{target_h}</span>
        </div>
        <div class="controls">
            <label>Zoom:</label>
            <input type="range" id="zoom" min="2" max="28" value="8" step="0.5">
            <span id="zoom-val" style="min-width:30px;">8px</span>
            <label>Altezza riga:</label>
            <input type="range" id="lh" min="0.35" max="1.1" value="0.55" step="0.02">
            <span id="lh-val" style="min-width:32px;">0.55</span>
            <button id="btn-theme">🌓 Sfondo</button>
            <button id="btn-copy">📋 Copia</button>
            <button id="btn-save">💾 Scarica TXT</button>
        </div>
    </div>
    <div class="viewer">
        <pre id="art">{html_body}</pre>
    </div>
    <div id="toast" class="toast">Copiato negli appunti!</div>
    <script>
        const art = document.getElementById('art');
        const zoom = document.getElementById('zoom');
        const zoomVal = document.getElementById('zoom-val');
        const lh = document.getElementById('lh');
        const lhVal = document.getElementById('lh-val');
        const rawText = {raw_json};
        zoom.oninput = (e) => {{ art.style.fontSize = e.target.value + 'px'; zoomVal.textContent = e.target.value + 'px'; }};
        lh.oninput = (e) => {{ art.style.lineHeight = e.target.value; lhVal.textContent = e.target.value; }};
        document.getElementById('btn-theme').onclick = () => document.body.classList.toggle('light');
        document.getElementById('btn-copy').onclick = async () => {{
            await navigator.clipboard.writeText(rawText);
            const t = document.getElementById('toast');
            t.classList.add('show');
            setTimeout(() => t.classList.remove('show'), 2000);
        }};
        document.getElementById('btn-save').onclick = () => {{
            const b = new Blob([rawText], {{type:'text/plain;charset=utf-8'}});
            const a = document.createElement('a');
            a.href = URL.createObjectURL(b);
            a.download = '{titolo}.txt';
            a.click();
        }};
    </script>
</body>
</html>
"""
    with open(percorso_output, "w", encoding="utf-8") as f:
        f.write(doc)
    return percorso_output


# ==============================================================================
# SALVATAGGIO DEI FILE TXT (UTF-8-SIG PER WINDOWS NOTEPAD)
# ==============================================================================
def salva_txt(contenuto: str, percorso_file: str, titolo: str = "Testo"):
    """Salva con codifica UTF-8 con BOM così Blocco Note non sbaglia mai."""
    with open(percorso_file, "w", encoding="utf-8-sig") as f:
        f.write(contenuto)
    sz = os.path.getsize(percorso_file)
    print(f"  [✓] {titolo:<25} -> {Path(percorso_file).name} ({formatta_dimensione(sz)})")


# ==============================================================================
# PIPELINE GENERALE DI ELABORAZIONE
# ==============================================================================
def processa_immagine(
    percorso_immagine: str,
    larghezza: int = 90,
    modalita: str = "all",      # 'all', 'braille', 'ascii', 'blocks'
    per_blocco_note: bool = True,
    esporta_html: bool = True,
    cartella_output: str = None
):
    """
    Esegue l'elaborazione con il massimo livello di nitidezza,
    generando i file .txt ottimizzati per Blocco Note.
    """
    t0 = time.perf_counter()

    img_rgb, img_gray, ha_sfondo_scuro = carica_e_ottimizza_sorgente(percorso_immagine)
    orig_w, orig_h = img_gray.size
    p_obj = Path(pulisci_percorso(percorso_immagine))
    nome_base = p_obj.stem
    dir_out = Path(cartella_output) if cartella_output else p_obj.parent
    dir_out.mkdir(parents=True, exist_ok=True)

    # Calcolo altezza standard (compensazione monospace 0.45)
    aspect = 0.45
    altezza = max(1, int(larghezza * (orig_h / orig_w) * aspect))

    # Selezione della rampa ottimale:
    # Per formati piccoli (<= 110) usiamo la rampa micro ad alto contrasto per evitare 'polvere'
    rampa_ascii = RAMP_CRISP_SMALL if larghezza <= 110 else RAMP_ULTRA_70

    print(f"\n✨ Elaborazione: '{p_obj.name}' ({orig_w}×{orig_h} px)")
    print(f"📐 Risoluzione ASCII scelta: {larghezza} colonne × {altezza} righe")
    print(f"🎯 Target visualizzazione: {'📄 Blocco Note Windows (Sfondo Bianco)' if per_blocco_note else '💻 Sfondo Scuro (Terminale/VS Code)'}")
    print("─" * 60)

    # 1. Calcolo luminanza ad altissima definizione
    arr_lum = downsample_ad_alta_definizione(
        img_gray=img_gray,
        target_w=larghezza,
        target_h=altezza,
        per_blocco_note=per_blocco_note,
        ha_sfondo_scuro=ha_sfondo_scuro,
        contrasto=1.8,
        nitidezza=1.8
    )

    file_prodotti = []

    # A. Generazione Braille Ultra-HD (sempre consigliata per Blocco Note)
    if modalita in ("all", "braille"):
        testo_braille = genera_braille_ultra_hd(
            img_gray=img_gray,
            target_w=larghezza,
            aspect=aspect,
            per_blocco_note=per_blocco_note,
            ha_sfondo_scuro=ha_sfondo_scuro,
            contrasto=1.8
        )
        f_braille = dir_out / f"{nome_base}_braille_w{larghezza}.txt"
        salva_txt(testo_braille, str(f_braille), "⭐ Braille Ultra-HD TXT")
        file_prodotti.append(str(f_braille))

    # B. Generazione ASCII Crisp
    if modalita in ("all", "ascii"):
        testo_ascii = genera_testo_ascii(arr_lum, rampa_ascii, per_blocco_note=per_blocco_note)
        f_ascii = dir_out / f"{nome_base}_ascii_w{larghezza}.txt"
        salva_txt(testo_ascii, str(f_ascii), "✍️  ASCII Art Crisp TXT")
        file_prodotti.append(str(f_ascii))

    # C. Generazione Blocchi Shading
    if modalita in ("all", "blocks"):
        testo_blocchi = genera_testo_ascii(arr_lum, RAMP_BLOCKS, per_blocco_note=per_blocco_note)
        f_blocchi = dir_out / f"{nome_base}_blocchi_w{larghezza}.txt"
        salva_txt(testo_blocchi, str(f_blocchi), "█  Blocchi Shading TXT")
        file_prodotti.append(str(f_blocchi))

    # D. Generazione HTML a colori
    if esporta_html:
        f_html = dir_out / f"{nome_base}_colori_w{larghezza}.html"
        genera_html_hd(img_rgb, larghezza, altezza, str(f_html), titolo=nome_base)
        sz = os.path.getsize(str(f_html))
        print(f"  [✓] {'🌐 HTML a Colori HD':<25} -> {f_html.name} ({formatta_dimensione(sz)})")
        file_prodotti.append(str(f_html))

    elapsed = (time.perf_counter() - t0) * 1000
    print("─" * 60)
    print(f"🚀 Fatto in appena {elapsed:.1f} ms!")
    print("\n💡 CONSIGLIO D'ORO PER BLOCCO NOTE WINDOWS:")
    print("   1. Apri il file .txt generato con Blocco Note.")
    print("   2. Assicurati che 'A capo automatico' sia DISATTIVATO (Visualizza > A capo automatico).")
    print("   3. Premi Ctrl + rotella mouse per regolare lo zoom e goderti l'immagine!\n")

    return file_prodotti


# ==============================================================================
# MENU INTERATTIVO CARINO, SEMPLICE ED EFFICACE
# ==============================================================================
def menu_interattivo():
    banner = """
  ╔══════════════════════════════════════════════════════════════════════╗
  ║       ✨ GENERATORE ASCII & BRAILLE ULTRA-HD PER BLOCCO NOTE ✨      ║
  ║             Massima Risoluzione anche in Formati Piccoli             ║
  ╚══════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

    # 1. Immagine
    while True:
        percorso = input("👉 Trascina qui il file dell'immagine e premi Invio: ").strip()
        p = pulisci_percorso(percorso)
        if os.path.isfile(p):
            break
        print("❌ File non trovato. Trascina un'immagine valida (PNG, JPG, WEBP).")

    # 2. Grandezza dell'ASCII nel file TXT
    print("\n📏 QUANTO DEVE ESSERE GRANDE L'ASCII NEL BLOCCO NOTE?")
    print("   [1] Molto Piccolo (40 colonne)  - Tascabile, ultra-compatto")
    print("   [2] Piccolo (60 colonne)        - Ottimo per finestre piccole")
    print("   [3] Medio (90 colonne)         - Perfetto per Blocco Note standard [CONSIGLIATO]")
    print("   [4] Grande (150 colonne)       - Pieno schermo, molto dettagliato")
    print("   [5] Gigante HD (250 colonne)   - Risoluzione massima da poster")
    print("   Oppure scrivi direttamente qualsiasi numero (es. 45, 75, 120...)")

    scelta_g = input("\nScegli grandezza [default: 3 (90 colonne)]: ").strip()
    mappa = {"1": 40, "2": 60, "3": 90, "4": 150, "5": 250}

    if scelta_g in mappa:
        larghezza = mappa[scelta_g]
    elif scelta_g.isdigit() and int(scelta_g) >= 15:
        larghezza = int(scelta_g)
    else:
        larghezza = 90

    print(f"-> Larghezza impostata: {larghezza} caratteri.")

    # 3. Formato desiderato
    print("\n🎨 COSA VUOI GENERARE?")
    print("   [1] ⭐ TUTTO INSIEME (Braille Ultra-HD + ASCII + Blocchi + HTML) [CONSIGLIATO]")
    print("   [2] ⣿ Solo Braille Ultra-HD (Risoluzione 8x nei file .txt - Dettaglio Folle!)")
    print("   [3] ✍️  Solo ASCII Crisp (Caratteri classici nitidissimi)")
    print("   [4] █ Solo Blocchi Shading (Effetto pixel-art retrò solido)")

    scelta_m = input("\nScegli formato [default: 1 (Tutto Insieme)]: ").strip()
    if scelta_m == "2":
        modalita = "braille"
    elif scelta_m == "3":
        modalita = "ascii"
    elif scelta_m == "4":
        modalita = "blocks"
    else:
        modalita = "all"

    # 4. Dove verrà aperto
    print("\n🌓 DOVE VISUALIZZERAI IL FILE DI TESTO?")
    print("   [1] 📄 Blocco Note Windows (Sfondo Bianco - Carta Chiara) [Default]")
    print("   [2] 💻 Terminale / VS Code / Discord (Sfondo Scuro)")
    scelta_bg = input("Scegli sfondo [default: 1]: ").strip()
    per_blocco_note = (scelta_bg != "2")

    print("\n" + "─" * 60)
    processa_immagine(
        percorso_immagine=p,
        larghezza=larghezza,
        modalita=modalita,
        per_blocco_note=per_blocco_note,
        esporta_html=True
    )


# ==============================================================================
# CLI PARSER (AUTOMAZIONE DA RIGA DI COMANDO)
# ==============================================================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generatore ASCII & Braille Ultra-HD per Blocco Note."
    )
    parser.add_argument("percorso", nargs="?", default=None, help="Percorso del file immagine")
    parser.add_argument("-w", "--width", type=int, default=90, help="Larghezza caratteri nel file .txt (default: 90)")
    parser.add_argument("-m", "--mode", choices=["all", "braille", "ascii", "blocks"], default="all",
                        help="Formato da generare: all, braille, ascii, blocks (default: all)")
    parser.add_argument("--bg", choices=["light", "dark"], default="light",
                        help="Target: 'light' per Blocco Note Windows, 'dark' per Terminale/VS Code (default: light)")
    parser.add_argument("--no-html", dest="html", action="store_false", help="Non generare la versione HTML")
    parser.add_argument("-o", "--outdir", type=str, default=None, help="Cartella di destinazione")

    return parser.parse_args()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parse_arguments()
        if args.percorso:
            p = pulisci_percorso(args.percorso)
            if not os.path.isfile(p):
                print(f"❌ Errore: File non trovato: '{p}'")
                sys.exit(1)
            processa_immagine(
                percorso_immagine=p,
                larghezza=args.width,
                modalita=args.mode,
                per_blocco_note=(args.bg == "light"),
                esporta_html=args.html,
                cartella_output=args.outdir
            )
        else:
            menu_interattivo()
    else:
        try:
            menu_interattivo()
        except KeyboardInterrupt:
            print("\nOperazione annullata.")
        except Exception as e:
            print(f"\n❌ Errore: {e}")
            import traceback
            traceback.print_exc()