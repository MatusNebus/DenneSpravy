from __future__ import annotations

# Filter out noisy "live" / video-ish items
TITLE_BLOCKLIST = [" as it happened", " live", "live updates", "latest updates"]
LINK_BLOCKLIST = ["/live/", "/video/", "newsfeed"]

WORLD_FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("DW World", "https://rss.dw.com/rdf/rss-en-world"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("Guardian World", "https://www.theguardian.com/world/rss"),
    ("FT World", "https://www.ft.com/world?format=rss"),
]

SLOVAK_FEEDS = [
    ("teraz.sk (TASR)", "https://www.teraz.sk/rss/slovensko.rss"),
    ("Aktuality Domáce", "https://www.aktuality.sk/rss/domace/"),
    # ("TA3", "https://www.ta3.com/rss/"), #pozor to je asi nie zamerane uplne na slovensko
    # ("RTVS Správy", "https://spravy.rtvs.sk/rss/"), #aj toto
    ("SME Domov", "https://domov.sme.sk/rss"),
    ("Denník N Správy", "https://dennikn.sk/slovensko/feed/"),
    ("Pravda", "https://spravy.pravda.sk/domace/rss/xml/"),
]

TECH_FEEDS = [
    # ("The Verge", "https://www.theverge.com/rss/index.xml"),
    ("Ars Technica", "https://feeds.arstechnica.com/arstechnica/index"),
    ("MIT Technology Review", "https://www.technologyreview.com/feed/"),
    ("Robot Report", "https://www.therobotreport.com/feed/"),
    ("IEEE Spectrum", "https://spectrum.ieee.org/feeds/topic/robotics.rss"),
    ("TechCrunch", "https://techcrunch.com/feed/"),
    # ("Wired", "https://www.wired.com/feed/rss"),
    
]
