# digest_section.py
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Callable
import feedparser
from dateutil import parser as dtparser
from openai import OpenAI
from feeds import TITLE_BLOCKLIST, LINK_BLOCKLIST


def _parse_entry_time(entry) -> Optional[datetime]:
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


def _clean_text(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)  # remove html tags
    s = re.sub(r"\s+", " ", s).strip()
    return s


PromptFn = Callable[[List[Dict]], str]


@dataclass
class DigestSection:
    name: str
    feeds: list[tuple[str, str]]
    prompt_fn: PromptFn

    lookback_hours: int = 12
    max_items_per_feed: int = 30
    max_total_articles: int = 120
    model: str = "gpt-5-mini"

    def fetch_articles(self) -> List[Dict]:
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=self.lookback_hours)
        out: List[Dict] = []
        next_id = 1

        n_sources = max(1, len(self.feeds))
        per_source_cap = max(1, self.max_total_articles // n_sources)

        for source, url in self.feeds:
            feed = feedparser.parse(url)
            entries = feed.entries[: self.max_items_per_feed]
            per_source_out: List[Dict] = []

            for e in entries:
                dt = _parse_entry_time(e)
                if not dt or dt < cutoff:
                    continue

                title = (e.get("title") or "").strip()
                link = (e.get("link") or "").strip()
                summary = _clean_text((e.get("summary") or e.get("description") or "").strip())

                if not title or not link:
                    continue

                t_low = title.lower()
                if any(x in t_low for x in TITLE_BLOCKLIST):
                    continue
                if any(x in link for x in LINK_BLOCKLIST):
                    continue

                per_source_out.append(
                    {
                        "id": next_id,
                        "source": source,
                        "published_utc": dt.isoformat(),
                        "title": title,
                        "summary": summary[:400],
                        "link": link,
                    }
                )
                next_id += 1

            per_source_out.sort(key=lambda x: x["published_utc"], reverse=True)
            out.extend(per_source_out[:per_source_cap])

        out.sort(key=lambda x: x["published_utc"], reverse=True)
        return out[: self.max_total_articles]

    def generate_digest(self, articles: List[Dict]) -> str:
        prompt = self.prompt_fn(articles)

        client = OpenAI()  # reads OPENAI_API_KEY from environment
        response = client.responses.create(
            model=self.model,
            input=prompt,
            reasoning={"effort": "low"},
        )
        return response.output_text

    def run(self) -> str:
        articles = self.fetch_articles()
        return self.generate_digest(articles)
