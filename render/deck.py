"""Copy deck for Monday 23 November 2026. Every line is checked against reporting of that day."""

DAY = "MONDAY 23 NOVEMBER 2026"
DAY_SHORT = "23 NOVEMBER 2026"
EDITION = "THE DAY IN ONE PAGE"
STRAP = "SEVEN STORIES \u00b7 SIX CONTINENTS"

LEAD = {
    "kicker": "MARKETS",
    "lines": ["Nvidia takes back", "the chief who left it"],
    "body": [
        "Directors voted unanimously to reinstate Jensen Huang as chief",
        "executive and board member, less than two weeks after he quit.",
    ],
    "figure": "A THIRD",
    "figure_note": "added to Nvidia's value in a single day",
    "chips": ["Nasdaq +6.6%", "S&P 500 +5%", "Dow +1,500 pts"],
}

# Four cards, drawn big enough to read at 300px across.
CARDS = [
    {
        "desk": "AMERICAS",
        "head": ["Democrats win", "258 House seats"],
        "figure": "258",
        "line": "most since 1992",
        "art": "capitol",
    },
    {
        "desk": "CLIMATE",
        "head": ["Climate talks end", "without a deal"],
        "figure": "200",
        "line": "nations, no agreement",
        "art": "globe",
    },
]

STRIP = [
    ("AFRICA", "Mourners' boat sinks in Nigeria, killing 24 in Bayelsa State"),
    ("M. EAST", "Drone attack sinks a Russian warship at Benghazi port, Libya"),
    ("ASIA", "South Korea's education minister quits over an exam scandal"),
    ("EUROPE", "Canary Islands set a record for migrant arrivals from Africa"),
]

FOOT = "Reported 23 November 2026"
