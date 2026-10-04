"""Shared timeline for TOLX video 03 "Odoo 20 is here" (30 fps, 1010 frames = 33.7 s).

Imported by compose_03.py and audio/compose_audio.py. Scene starts are set around the measured
Marcus voiceover takes. Frame n is shown at n/30 s.
"""
FPS, TOTAL = 30, 1010

HOOK = 0            # 0.0 s  "ODOO 20" / released September 2026
PAIN = 115          # 3.8 s  "Still on chats and spreadsheets?"
AGENT = 200         # 6.7 s  1 AI agent: plain-words instruction -> plan -> approve -> active
ACCOUNT = 395       # 13.2 s 2 accounting assistant: "How much do customers owe me?"
OFFLINE = 560       # 18.7 s 3 POS keeps selling offline, then syncs
ONE = 690           # 23.0 s sales / stock / accounting / team in one system, AI built in
OFFER = 800         # 26.7 s Odoo 20 set up by TOLX, or custom software
END_CARD = 870      # 29.0 s discovery-call CTA + Odoo Ready Partner badge

PROMPT_TYPE = AGENT + 14            # owner types the instruction
PLAN_IN = AGENT + 74                # agent's plan card
PLAN_STEPS = [PLAN_IN + 10, PLAN_IN + 20, PLAN_IN + 30]
APPROVE = AGENT + 150               # approve pressed -> ACTIVE
Q_TYPE = ACCOUNT + 12
ANSWER_IN = ACCOUNT + 58
ANSWER_ROWS = [ANSWER_IN + 16, ANSWER_IN + 24, ANSWER_IN + 32]
GO_OFFLINE = OFFLINE + 24
POS_ORDERS = [OFFLINE + 40, OFFLINE + 56, OFFLINE + 72]
BACK_ONLINE = OFFLINE + 98
TILES_IN = [ONE + 6, ONE + 12, ONE + 18, ONE + 24]
MERGE = ONE + 46
OFFER_BEATS = [OFFER + 8, OFFER + 18, OFFER + 30]
