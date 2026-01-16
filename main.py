# main.py
from __future__ import annotations
from digest_section import DigestSection
from email_sender import send_email
from feeds import WORLD_FEEDS, SLOVAK_FEEDS, TECH_FEEDS
from prompts import prompt_world_en, prompt_slovakia_sk, prompt_tech_en


def main() -> None:
    sections = [
        DigestSection(
            name="WORLD",
            feeds=WORLD_FEEDS,
            prompt_fn=prompt_world_en,
            lookback_hours=12,
            max_items_per_feed=30,
            max_total_articles=120,
        ),
        DigestSection(
            name="SLOVENSKO",
            feeds=SLOVAK_FEEDS,
            prompt_fn=prompt_slovakia_sk,
            lookback_hours=12,
            max_items_per_feed=30,
            max_total_articles=120,
        ),
        DigestSection(
            name="TECH",
            feeds=TECH_FEEDS,
            prompt_fn=prompt_tech_en,
            lookback_hours=12,
            max_items_per_feed=30,
            max_total_articles=120,
        ),
    ]

    parts: list[str] = []

    for s in sections:
        print(f"=== Fetching & generating: {s.name} ===")
        try:
            digest = s.run().strip()
            parts.append(f"[{s.name}]\n{digest}")
        except Exception as e:
            # Fail-soft: pošleme aspoň zvyšok
            parts.append(f"[{s.name}]\nSection unavailable due to an error.")
            print(f"ERROR in section {s.name}: {e}")

    body = "\n\n".join(parts)

    send_email(
        subject="Správy (svet, Slovensko, technológie) za posledných 12 hodín",
        body=body,
    )

    print("Sent email.")


if __name__ == "__main__":
    main()
