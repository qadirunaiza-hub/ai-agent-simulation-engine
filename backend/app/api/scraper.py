"""
Live Internet Scraper
Pulls latest news from public sources (no API keys) for simulation seeding.
Sources: HackerNews, Reddit WorldNews, BBC RSS, Reuters RSS
"""

import time
import threading
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError
import json

from flask import Blueprint, jsonify, request
from ..utils.logger import get_logger

logger = get_logger("mirofish.api.scraper")
scraper_bp = Blueprint("scraper", __name__)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (MiroFish research bot; +https://github.com/mirofish)"
}
_TIMEOUT = 8

# In-memory cache: last successful scrape result
_cache: dict = {}
_cache_lock = threading.Lock()


def _get(url: str) -> bytes:
    req = Request(url, headers=_HEADERS)
    with urlopen(req, timeout=_TIMEOUT) as r:
        return r.read()


def _fetch_hackernews(limit: int = 8) -> list[dict]:
    try:
        ids = json.loads(_get("https://hacker-news.firebaseio.com/v0/topstories.json"))[:limit]
        articles = []
        for story_id in ids:
            try:
                item = json.loads(_get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"))
                if item.get("title"):
                    articles.append({
                        "title": item["title"],
                        "url": item.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "summary": item.get("text", ""),
                        "source": "HackerNews",
                        "score": item.get("score", 0),
                    })
            except Exception:
                pass
        return articles
    except Exception as e:
        logger.debug(f"HN fetch failed: {e}")
        return []


def _fetch_reddit(subreddit: str = "worldnews", limit: int = 8) -> list[dict]:
    try:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={limit}&t=day"
        data = json.loads(_get(url))
        posts = data.get("data", {}).get("children", [])
        articles = []
        for p in posts:
            d = p.get("data", {})
            if d.get("title") and not d.get("stickied"):
                articles.append({
                    "title": d["title"],
                    "url": d.get("url", ""),
                    "summary": d.get("selftext", "")[:300],
                    "source": f"r/{subreddit}",
                    "score": d.get("score", 0),
                })
        return articles
    except Exception as e:
        logger.debug(f"Reddit fetch failed: {e}")
        return []


def _fetch_rss(url: str, source_label: str, limit: int = 6) -> list[dict]:
    try:
        raw = _get(url).decode("utf-8", errors="replace")
        root = ET.fromstring(raw)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        articles = []
        # RSS 2.0
        for item in root.findall(".//item")[:limit]:
            title = (item.findtext("title") or "").strip()
            desc = (item.findtext("description") or "").strip()
            link = (item.findtext("link") or "").strip()
            if title:
                articles.append({"title": title, "url": link,
                                  "summary": desc[:300], "source": source_label, "score": 0})
        # Atom
        if not articles:
            for entry in root.findall(".//atom:entry", ns)[:limit]:
                title = (entry.findtext("atom:title", namespaces=ns) or "").strip()
                summary = (entry.findtext("atom:summary", namespaces=ns) or "").strip()
                link_el = entry.find("atom:link", ns)
                link = (link_el.get("href", "") if link_el is not None else "")
                if title:
                    articles.append({"title": title, "url": link,
                                      "summary": summary[:300], "source": source_label, "score": 0})
        return articles
    except Exception as e:
        logger.debug(f"RSS {source_label} failed: {e}")
        return []


RSS_FEEDS = [
    ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC World"),
    ("https://feeds.reuters.com/reuters/topNews", "Reuters"),
    ("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "NY Times"),
]


def _do_scrape(topic: str = "") -> dict:
    articles = []
    articles += _fetch_hackernews(8)
    articles += _fetch_reddit("worldnews", 8)
    articles += _fetch_reddit("technology", 5)
    for rss_url, label in RSS_FEEDS:
        articles += _fetch_rss(rss_url, label, 6)

    # Deduplicate by title
    seen = set()
    unique = []
    for a in articles:
        key = a["title"].lower()[:60]
        if key not in seen:
            seen.add(key)
            unique.append(a)

    # Topic filter (loose keyword match)
    if topic:
        kws = topic.lower().split()
        scored = []
        for a in unique:
            text = (a["title"] + " " + a["summary"]).lower()
            hits = sum(1 for kw in kws if kw in text)
            scored.append((hits, a))
        scored.sort(key=lambda x: -x[0])
        # Keep topic-relevant first, then fill with general news
        relevant = [a for h, a in scored if h > 0]
        general = [a for h, a in scored if h == 0]
        unique = relevant + general

    now = datetime.now(timezone.utc).isoformat()
    sources = list({a["source"] for a in unique})
    result = {
        "scraped_at": now,
        "topic": topic,
        "count": len(unique),
        "sources": sources,
        "articles": unique[:30],
    }
    logger.info(f"Scraped {len(unique)} articles from {sources}")
    return result


@scraper_bp.route("", methods=["GET"])
def get_scrape():
    """Return cached scrape result (or fetch if cache empty)."""
    topic = request.args.get("topic", "")
    with _cache_lock:
        if _cache:
            return jsonify({"success": True, "data": _cache})
    result = _do_scrape(topic)
    with _cache_lock:
        _cache.update(result)
    return jsonify({"success": True, "data": result})


@scraper_bp.route("/refresh", methods=["POST"])
def refresh_scrape():
    """Force a fresh scrape (ignores cache)."""
    topic = (request.get_json() or {}).get("topic", request.args.get("topic", ""))
    result = _do_scrape(topic)
    with _cache_lock:
        _cache.clear()
        _cache.update(result)
    return jsonify({"success": True, "data": result})


@scraper_bp.route("/seed-posts", methods=["GET"])
def seed_posts():
    """Return scraped articles formatted as simulation initial_posts."""
    with _cache_lock:
        articles = list(_cache.get("articles", []))
        scraped_at = _cache.get("scraped_at", "")

    if not articles:
        result = _do_scrape("")
        articles = result["articles"]
        scraped_at = result["scraped_at"]

    posts = []
    for a in articles[:20]:
        content = a["title"]
        if a.get("summary"):
            content += f"\n\n{a['summary'][:200]}"
        posts.append({
            "content": content,
            "source_url": a.get("url", ""),
            "source_label": a.get("source", ""),
        })
    return jsonify({"success": True, "data": {"posts": posts, "scraped_at": scraped_at}})
