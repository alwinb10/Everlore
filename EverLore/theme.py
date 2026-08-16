# EVERLORE Dynamic Theme System

# Current mode
CURRENT_THEME = "dark"


# ---------------- DARK MODE ----------------

DARK = {

    "BG": "#0D0D0D",
    "SIDEBAR": "#141414",
    "CARD": "#1C1C1C",
    "HOVER": "#2A2A2A",

    "TEXT": "#FFFFFF",
    "SUBTEXT": "#8F8F8F"

}


# ---------------- LIGHT MODE ----------------

LIGHT = {

    "BG": "#F2F2F2",
    "SIDEBAR": "#E5E5E5",
    "CARD": "#FFFFFF",
    "HOVER": "#D6D6D6",

    "TEXT": "#111111",
    "SUBTEXT": "#666666"

}


# Active colors

def load_theme():

    if CURRENT_THEME == "dark":
        return DARK

    else:
        return LIGHT



# ---------------- Theme Change ----------------

def set_theme(mode):

    global CURRENT_THEME

    if mode in ["dark", "light"]:

        CURRENT_THEME = mode



# ---------------- Color Access ----------------

def get_color(name):

    colors = load_theme()

    return colors.get(
        name,
        "#FFFFFF"
    )



# ---------------- Fonts ----------------

TITLE = ("Segoe UI", 28, "bold")

SUBTITLE = ("Segoe UI", 15)

HEADING = ("Segoe UI", 22, "bold")

BODY = ("Segoe UI", 15)

BIG = ("Segoe UI", 34, "bold")



# Default colors for compatibility
# (will be updated later when dashboard refresh is added)

BG = get_color("BG")
SIDEBAR = get_color("SIDEBAR")
CARD = get_color("CARD")
HOVER = get_color("HOVER")
TEXT = get_color("TEXT")
SUBTEXT = get_color("SUBTEXT")
