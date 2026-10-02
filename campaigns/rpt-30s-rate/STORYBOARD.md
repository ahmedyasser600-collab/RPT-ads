# RPT — Reel 30" "Pagamento a rate" — storyboard tecnico (bozza v0)

Stato: **in revisione**. Stile di movimento da confermare con 2–3 video di riferimento.
Formato 1080×1920, 30 fps, 900 fotogrammi. Fotogramma `n` = tempo `(n-1)/30`.

## Stage (uguale per tutto il film)

`blender/stage.blend`, generato da `blender/build_stage.py` partendo da `RPT_Master_Library.blend`
(libreria in sola lettura). Si spostano solo i `*_ROOT`.

| Zona | Elemento | Posizione root (m) |
|---|---|---|
| Parete di fondo, sinistra | Piatto doccia, soffione, parete vetro (divisorio) | x −0.50 / −0.60 / +0.10 |
| Parete di fondo, destra | Mobile rovere cannettato, lavabo, miscelatore, specchio LED | x +0.58 |
| Parete sinistra | Sospeso WC | y −0.45, ruotato −90° |
| Nascosti (spaccato) | Kit idraulico dietro il mobile; stratigrafia pavimento sotto la doccia | — |

Luce: key caldo dal fronte-sinistra (direzione fissa), pannello a soffitto, fill freddo leggero da destra.

## Shot list

| Shot | Tempo | Fotogrammi | Camera | Animazione (controlli della libreria) | Testo a schermo |
|---|---|---|---|---|---|
| S1 | 0–4" | 1–120 | Dal vano porta: parte stretta su mobile/lavabo/specchio, dolly indietro e leggero arco fino all'inquadratura intera | LED specchio si accende (emission 0→1) | Il bagno che desideri. |
| S2 | 4–9" | 121–270 | Taglio a spaccato 3/4 dall'alto, ruotato per il verticale | `Floor_01..04` (Z, range del manifest) si separano e poi si ricompongono; kit idraulico visibile dietro il mobile (pareti/mobile in trasparenza o nascosti) | Ogni dettaglio conta. |
| S3 | 9–16" | 271–480 | Orbita lenta a 3/4 | Piastrelle si posano a cascata; vetro scorre in posizione; sanitari/miscelatore entrano con montaggio controllato; `Vanity_Drawer_2.location.y` 0 → −0.30 → 0 | Spazi pensati per te. |
| S4 | 16–23" | 481–690 | Movimento lento sul bagno completo | Nessuna (bagno finito) | Pannello giallo: **Più modi per pagare,** / **anche a rate.** (min. 4" leggibile) |
| S5 | 23–30" | 691–900 | Inquadratura migliore (23–26"), poi end card 2D (26–30", ≥3" di CTA) | — | Parliamo del tuo nuovo bagno. / Padova e provincia / ristrutturareperte.it |

Logo RPT: piccolo in sovraimpressione S1–S4 (alto a destra, fuori dalle aree UI); grande nell'end card.
Testi, sottotitoli e logo sono livelli 2D separati, mai nella geometria 3D.

## Tempi di render (misurati su questa macchina: 4 CPU, nessuna GPU)

- Cycles 1080×1920, 24 campioni + denoise OIDN: ~51 s/fotogramma → ~12 h per ~810 fotogrammi 3D.
- EEVEE in software: 73 s/fotogramma (non conveniente).
- Revisione: 540×960, 12 campioni: stimato ~6–8 s/fotogramma → ~1,5 h.

## Bloccanti per la versione pubblicabile

1. Video di riferimento (2–3) per lo stile di movimento.
2. ~~Voce fuori campo~~: fatta (Higgsfield, ElevenLabs, voce "Gia"; `audio/place_vo.py`).
3. ~~Musica~~: traccia originale upbeat composta in codice (`audio/compose_music.py`).
4. ~~Note legali~~: il cliente ha approvato "Più modi per pagare, anche a rate." senza
   ulteriori dettagli (il claim "fino a 10 anni" è stato tolto).
5. Conferma URL `ristrutturareperte.it`.
6. File mancanti nel caricamento: `brand/` (logo originale), immagini di riferimento RPT;
   `CATALOG.png` è troncato, 4 fotogrammi di `animation/frames` mancano (non bloccante).
