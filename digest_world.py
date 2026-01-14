import os
import re
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import feedparser
from dateutil import parser as dtparser
from openai import OpenAI
import smtplib
from email.message import EmailMessage
import html
import smtplib
from email.message import EmailMessage

# --------- RSS FEEDS (WORLD) ----------
WORLD_FEEDS = [
    ("BBC World", "https://feeds.bbci.co.uk/news/world/rss.xml"),
    ("DW World", "https://rss.dw.com/rdf/rss-en-world"),
    ("Al Jazeera", "https://www.aljazeera.com/xml/rss/all.xml"),
    ("Guardian World", "https://www.theguardian.com/world/rss"),
    ("FT World", "https://www.ft.com/world?format=rss"),
]

LOOKBACK_HOURS = 12 #alebo 24
MAX_ITEMS_PER_FEED = 30 #alebo 50
MAX_TOTAL_ARTICLES = 120 # safety cap so prompt doesn't explode

# Filter out noisy "live" / video-ish items
TITLE_BLOCKLIST = [" as it happened", " live", "live updates", "latest updates"]
LINK_BLOCKLIST = ["/live/", "/video/", "newsfeed"]


def parse_entry_time(entry) -> Optional[datetime]:
    for key in ("published", "updated"):
        if key in entry and entry[key]:
            try:
                dt = dtparser.parse(entry[key])
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt.astimezone(timezone.utc)
            except Exception:
                pass

    for key in ("published_parsed", "updated_parsed"):
        if key in entry and entry[key]:
            try:
                import time
                return datetime.fromtimestamp(time.mktime(entry[key]), tz=timezone.utc)
            except Exception:
                pass

    return None


def clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)  # remove html tags
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch_world_articles() -> List[Dict]:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=LOOKBACK_HOURS)
    out: List[Dict] = []
    next_id = 1

    n_sources = len(WORLD_FEEDS)
    per_source_cap = max(1, MAX_TOTAL_ARTICLES // n_sources)  # napr. 120//5 = 24

    for source, url in WORLD_FEEDS:
        feed = feedparser.parse(url)
        entries = feed.entries[:MAX_ITEMS_PER_FEED]

        per_source_out = []

        for e in entries:
            dt = parse_entry_time(e)
            if not dt or dt < cutoff:
                continue

            title = (e.get("title") or "").strip()
            link = (e.get("link") or "").strip()
            summary = clean_text((e.get("summary") or e.get("description") or "").strip())

            if not title or not link:
                continue

            t_low = title.lower()
            if any(x in t_low for x in TITLE_BLOCKLIST):
                continue
            if any(x in link for x in LINK_BLOCKLIST):
                continue

            per_source_out.append({
                "id": next_id,
                "source": source,
                "published_utc": dt.isoformat(),
                "title": title,
                "summary": summary[:400],
                "link": link,
            })
            next_id += 1

        # zoraď články v rámci jedného zdroja a vezmi len kvótu
        per_source_out.sort(key=lambda x: x["published_utc"], reverse=True)
        out.extend(per_source_out[:per_source_cap])

    # na konci ešte raz zoraď a orež na MAX_TOTAL_ARTICLES (pre istotu)
    out.sort(key=lambda x: x["published_utc"], reverse=True)
    return out[:MAX_TOTAL_ARTICLES]



def build_prompt(articles: List[Dict]) -> str:
    return f"""
Si editor denného spravodajského digestu. Dostaneš zoznam článkov (len titulok + krátky popis + zdroj + čas + link).
Tvoja úloha: vybrať TOP 5 najzásadnejších udalostí zo sveta z týchto článkov.

PRAVIDLÁ (dôležité):
- Použi LEN informácie, ktoré sú priamo v poskytnutých článkoch. Nevymýšľaj nič mimo nich.
- Každý uvedený fakt musí byť podporený minimálne 2 rôznymi zdrojmi v rámci poskytnutého zoznamu. (nemusis uz priamo v texte casto pisat zdroje, len tam kde treba)
- Ak sa zdroje líšia v číslach (napr. obete), uveď rozsah a priraď hodnoty ku konkrétnym zdrojom (napr. „BBC: 32, Guardian: 22“).
- Píš po slovensky, vecne, bez clickbait štýlu, čo najviac faktov.

HODNOTENIE DÔLEŽITOSTI (X/10) - na hodnotenie dôležitosti používaj toto:
10/10: extrémna globálna kríza (napr. veľká vojna medzi veľmocami, jadrová hrozba, plošná evakuácia, kolaps štátu, masové civilné obete vo veľkom meradle).
9/10: veľmi vážna eskalácia (prevrat, masové represie s vysokým počtom potvrdených obetí, zásadná energetická alebo finančná kríza s globálnym dopadom).
8/10: zásadné geopolitické rozhodnutie alebo veľká katastrofa s desiatkami obetí, veľké sankcie alebo veľká vojenská operácia.
7/10: veľká udalosť s výrazným dopadom (napr. veľká havária, významné politické rozhodnutie, vážny regionálny konflikt).
6/10: dôležitý diplomatický alebo ekonomický krok, regionálna kríza s citeľným dopadom.
3–5/10: stredne významné udalosti s obmedzeným dopadom.
1–2/10: drobné udalosti bez širšieho významu.

VÝSTUP (presne 5 položiek):
1.[NÁZOV UDALOSTI]
(DÔLEŽITOSŤ: X/10)
Zdroje: názvy zdrojov (minimálne 2 nezávislé)

Nasleduje 3 až 8 samostatných viet v súvislom texte:
- veta, ktorá presne popíše čo sa stalo (kto, čo, kde, kedy),
- veta s konkrétnymi rozhodnutiami, číslami alebo dátumami (len potvrdené fakty),
- veta o overenom dopade alebo následku, ak je známy,
- veta o tom, čo bude nasledovať, iba ak je to potvrdené,
- prípadne ďalšie 1–4 vety, len ak sú potrebné na pochopenie kontextu, bez špekulácií.

Tu sú články (JSON):
{articles}
""".strip()


def generate_digest_with_openai(prompt: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Chýba OPENAI_API_KEY v environment variables.")

    client = OpenAI()  # reads OPENAI_API_KEY from environment :contentReference[oaicite:3]{index=3}

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt,
        # voliteľne: znížime množstvo „premýšľania“, aby to bolo rýchlejšie/konzistentnejšie
        reasoning={"effort": "low"},
    )

    return response.output_text


def digest_to_html(digest_text: str) -> str:
    """
    Prevedie digest (plain text) do jednoduchého HTML:
    - riadky typu '1.[NÁZOV UDALOSTI]' dá do <strong>
    - zachová nové riadky cez <br>
    - text escapuje, aby sa nerozbilo HTML
    """
    lines = digest_text.splitlines()
    out = []

    for raw in lines:
        line = raw.rstrip("\n")
        if not line.strip():
            out.append("<br>")
            continue

        safe = html.escape(line)

        # Nadpisy položiek: "1. ..." / "1) ..." / prípadne "[...]"
        if re.match(r"^\s*([1-5][\.\)]\s+.+|\[.+\])\s*$", line):
            out.append(f"<strong>{safe}</strong><br>")
        else:
            out.append(f"{safe}<br>")


    return "".join(out)


def send_email(subject: str, body: str):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    SENDER_EMAIL = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # RECIPIENTS = [
    #     "matus.nebus@gmail.com",
    #     # sem hocikedy pridáš ďalšie
    # ]

    recipients_raw = os.getenv("EMAIL_RECIPIENTS", "")
    RECIPIENTS = [r.strip() for r in recipients_raw.split(",") if r.strip()]

    if not RECIPIENTS:
        raise RuntimeError("Chýba EMAIL_RECIPIENTS (aspoň jeden email).")


    if not SENDER_EMAIL or not EMAIL_PASSWORD:
        raise RuntimeError("Chýbajú emailové environment variables.")

    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = ", ".join(RECIPIENTS)
    msg["Subject"] = subject

    # plain text
    msg.set_content(body)

    # html (bold nadpisy 1.[...] až 5.[...])
    html_body = f"""\
<html>
  <body style="font-family: Arial, sans-serif; line-height: 1.5;">
    {digest_to_html(body)}
  </body>
</html>
"""
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.send_message(msg)




def main():
    print("Fetching world RSS articles (last 24h)...")
    articles = fetch_world_articles()
    print(f"Fetched {len(articles)} articles (after filter).")

    prompt = build_prompt(articles)
    print("Calling OpenAI API...")
    digest = generate_digest_with_openai(prompt)

    with open("output_world.txt", "w", encoding="utf-8") as f:
        f.write(digest.strip() + "\n")

    print("Done. Written to output_world.txt")

    send_email(
    subject="Objektívne správy za posledných 12 hodín",
    body=digest)

    print("Sent to email.")



if __name__ == "__main__":
    main()
