"""Shared timeline for TOLX video 04 "UAE e-invoicing is coming" (30 fps, 1020 frames = 34 s).

Imported by compose_04.py and audio/compose_audio.py. Scene starts are set around the measured
Gia voiceover takes (1.06x energetic read). Frame n is shown at n/30 s.
"""
FPS, TOTAL = 30, 1020

HOOK = 0            # 0.0 s  UAE / E-INVOICING / JULY 2027 / IS YOUR BUSINESS READY?
DEADLINES = 125     # 4.2 s  vertical timeline (MoF Ministerial Decisions 243/244 of 2025, as amended)
FORMAT = 350        # 11.7 s PDF -> structured data -> accredited provider -> buyer + FTA
EXCEL = 525         # 17.5 s Word / Excel invoices: NOT E-INVOICE READY
READY = 640         # 21.3 s readiness checklist
OFFER = 810         # 27.0 s Odoo or custom software
END_CARD = 880      # 29.3 s discovery-call CTA + Odoo Ready Partner badge

REVEALS = [2, 12, 24, 40]                       # UAE, E-INVOICING, JULY 2027, READY? (smooth reveals)
MILESTONES_IN = [DEADLINES + 8, DEADLINES + 16, DEADLINES + 24, DEADLINES + 32]
HL_JULY = DEADLINES + 46                         # "July 2027" highlighted (voice line 1)
HL_MARCH = DEADLINES + 126                       # "31 March 2027" highlighted (voice line 2)
PDF_IN = FORMAT + 10
PDF_X = FORMAT + 30
MORPH = FORMAT + 44
DATA_ROWS = [FORMAT + 62, FORMAT + 70, FORMAT + 78]
ASP_IN = FORMAT + 96
SPLIT_IN = FORMAT + 116
PACKET = FORMAT + 128
DOCS_IN = [EXCEL + 8, EXCEL + 16]
STAMP = EXCEL + 40
CHECKS = [READY + 26, READY + 54, READY + 82, READY + 110]
OFFER_BEATS = [OFFER + 8, OFFER + 18, OFFER + 30]
