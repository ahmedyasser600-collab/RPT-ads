"""Shared timeline for TOLX video 02 "When Excel stops working" (30 fps, 1030 frames = 34.3 s).

Imported by compose_02.py (picture) and audio/compose_audio.py (score, SFX, voiceover placement).
Scene starts are set around the measured Marcus voiceover takes. Frame n is shown at n/30 s.
"""
FPS, TOTAL = 30, 1030

HOOK = 0             # 0.0 s  "Your spreadsheet says 12."
SHELF = 100          # 3.3 s  "The shelf says 3."
FILES = 150          # 5.0 s  five versions of the stock file
QUESTIONS = 200      # 6.7 s  "Who updated it last?" ...
TURN = 285           # 9.5 s  files collapse into one product record: "One system. One number."
STEP_SELL = 365      # 12.2 s 1 a sale updates stock once
STEP_SYNC = 465      # 15.5 s 2 shop, warehouse and owner see the same number
STEP_REORDER = 595   # 19.8 s 3 low-stock flag + draft purchase order
STEP_SEE = 695       # 23.2 s 4 the day at a glance
STATEMENT = 780      # 26.0 s "Ready to move beyond Excel?" Odoo or custom software
END_CARD = 910       # 30.3 s discovery-call CTA

FILE_FRAMES = [FILES + 4 + 7 * i for i in range(5)]
QUESTION_FRAMES = [QUESTIONS + 6, QUESTIONS + 20, QUESTIONS + 34]
SALE_IN = STEP_SELL + 10
COUNT_DOWN = STEP_SELL + 40          # 6 -> 4
SYNC_PULSES = [STEP_SYNC + 30, STEP_SYNC + 42, STEP_SYNC + 54]
ALERT_IN = STEP_REORDER + 8
PO_CLICK = STEP_REORDER + 52
TILES = [STEP_SEE + 8, STEP_SEE + 16, STEP_SEE + 24]
STATEMENT_BEATS = [STATEMENT + 22, STATEMENT + 44, STATEMENT + 70]
