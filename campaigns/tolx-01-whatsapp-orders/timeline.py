"""Shared timeline for the TOLX "WhatsApp orders" video (30 fps, 900 frames = 30 s).

Imported by compose_tolx.py (picture) and audio/compose_audio.py (music + SFX) so that
message pops, step changes and board moves stay frame-locked. Frame n is shown at n/30 s.
"""
FPS, TOTAL = 30, 900

# ---- scenes (start frames)
HOOK = 0            # 0.0 s  chat floods in: "Taking orders on WhatsApp?"
KEY_IN = 115        # 3.8 s  the order message arrives (highlighted)
BURY = 150          # 5.0 s  more chat buries it
QUESTIONS = 200     # 6.7 s  "Who's handling it?" ...
TURN = 270          # 9.0 s  rewind to the order, it lifts out of the chat
STEP_LOG = 345      # 11.5 s 1 Log it
STEP_ASSIGN = 430   # 14.3 s 2 Assign it
STEP_TRACK = 510    # 17.0 s 3 Track it
STEP_FOLLOW = 615   # 20.5 s 4 Follow up
STATEMENT = 690     # 23.0 s owner / status / next step
END_CARD = 780      # 26.0 s logo + guide CTA

# ---- team-group chat. (frame, sender, text); sender "You" = the owner, drawn on the right
CHAT = [
    (8, "Ravi", "Customer asking price for 50 pcs"),
    (22, "Ali", "Is the black case in stock??"),
    (36, "Sara", "Checking..."),
    (50, "You", "Who is doing the JLT delivery?"),
    (64, "Ravi", "Not me"),
    (78, "Ali", "Any update on Mrs Fatima's order?"),
    (92, "Sara", "She called again"),
    (KEY_IN, "Sara", "New order: Khalid, 12 phone cases, deliver Thursday"),
]
KEY_INDEX = len(CHAT) - 1
_BURY_LINES = [
    ("Ali", "Ok"), ("Ravi", "Send pic pls"), ("You", "Price list?"), ("Ali", "Delivery charge to Deira?"),
    ("Sara", "Done"), ("Ravi", "Can he pay cash?"), ("Ali", "Still open today?"), ("Sara", "Received, thanks"),
    ("Ravi", "How much for 3?"), ("You", "Call me"), ("Ali", "Ok noted"), ("Sara", "Any discount?"),
    ("Ravi", "Tomorrow possible?"), ("Ali", "Which size?"), ("Sara", "Location?"), ("Ravi", "Sent"),
    ("Ali", "Who took the Karama order?"), ("Sara", "Not sure"),
]
CHAT += [(BURY + 4 + 4 * i, s, t) for i, (s, t) in enumerate(_BURY_LINES)]
QUESTION_FRAMES = [QUESTIONS + 6, QUESTIONS + 20, QUESTIONS + 34]

# ---- workflow board moves (frame the card starts moving into column 1, 2, 3)
BOARD_IN = STEP_TRACK + 6
MOVE_CONFIRMED = STEP_TRACK + 40
MOVE_DELIVERED = STEP_TRACK + 72
FOLLOW_CHIP = STEP_FOLLOW + 8
STATEMENT_PILLS = [STATEMENT + 18, STATEMENT + 26, STATEMENT + 34]
