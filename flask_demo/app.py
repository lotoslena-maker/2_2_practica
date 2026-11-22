"""Навчальний Flask-застосунок: Web Scraping Lab, заняття 2.2."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import re

from flask import Flask, jsonify, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
ROOT = Path(__file__).resolve().parent
SOURCE_URL = "https://armyinform.com.ua/category/main/"
USER_AGENT = "MetIAZ-TeachingDemo/1.0 (educational demonstration; respectful rate)"
MAX_BYTES = 2_000_000


def extract_news(html, base_url):
    """BeautifulSoup: HTML -> список новин із заголовком і посиланням."""
    soup = BeautifulSoup(html, "html.parser")
    news = []
    seen = set()
    # Використовуємо заголовки в блоках статей і типові заголовки списків.
    for heading in soup.select("article h2, article h3, h2.entry-title, h3.entry-title, .post-title"):
        anchor = heading.find("a", href=True)
        if anchor is None:
            continue
        title = heading.get_text(" ", strip=True)
        url = urljoin(base_url, anchor["href"])
        parsed = urlparse(url)
        if not (12 <= len(title) <= 230 and parsed.hostname in ("armyinform.com.ua", "www.armyinform.com.ua")):
            continue
        if url in seen:
            continue
        seen.add(url)
        card = heading.find_parent("article") or heading.parent
        time_tag = card.find("time") if card else None
        date = (time_tag.get("datetime") or time_tag.get_text(" ", strip=True)) if time_tag else ""
        news.append({"title": title, "date": date, "url": url})
        if len(news) == 8:
            break
    return news


def html_summary(html):
    soup = BeautifulSoup(html, "html.parser")
    return {"html_length": len(html), "links": len(soup.find_all("a")), "headings": len(soup.find_all(["h1", "h2", "h3"]))}


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/demo")
def demo():
    html = (ROOT / "sample_news.html").read_text(encoding="utf-8")
    news = extract_news(html, SOURCE_URL)
    return jsonify({
        "mode": "demo", "source": "Вбудований навчальний HTML-зразок",
        "step_requests": "Локальний файл: мережевого GET немає",
        "step_bs4": "BeautifulSoup + CSS-селектор article h2/article h3",
        "statistics": html_summary(html), "articles": news, "html_excerpt": html[:1600],
    })


@app.get("/api/live")
def live():
    """Один добровільний запит до відкритої сторінки; без обходу обмежень."""
    # Відкритий доступ сайту не дорівнює дозволу на автоматизацію.
    # Перевіряємо robots.txt перед запитом, а за неможливості перевірки припиняємо.
    try:
        robots_response = requests.get(
            "https://armyinform.com.ua/robots.txt",
            timeout=(4, 8), headers={"User-Agent": USER_AGENT}
        )
        robots_response.raise_for_status()
        parser = RobotFileParser()
        parser.parse(robots_response.text.splitlines())
        if not parser.can_fetch(USER_AGENT, SOURCE_URL):
            return jsonify(error="Правила robots.txt не дозволяють цей шлях. Використайте навчальний режим."), 403
        response = requests.get(
            SOURCE_URL, headers={"User-Agent": USER_AGENT, "Accept": "text/html"},
            timeout=(4, 12), stream=True, allow_redirects=False
        )
        try:
            if response.status_code in (301, 302, 307, 308):
                return jsonify(error="Сторінка перенаправляє запит. Використайте навчальний режим."), 502
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if "html" not in content_type.lower():
                return jsonify(error="Сервер повернув не HTML."), 502
            chunks = []
            total = 0
            for chunk in response.iter_content(chunk_size=32768):
                total += len(chunk)
                if total > MAX_BYTES:
                    return jsonify(error="HTML перевищує навчальний ліміт 2 МБ."), 413
                chunks.append(chunk)
            raw = b"".join(chunks)
            encoding = response.encoding or "utf-8"
            html = raw.decode(encoding, errors="replace")
            code = response.status_code
        finally:
            response.close()
        articles = extract_news(html, SOURCE_URL)
        return jsonify({
            "mode": "live", "source": SOURCE_URL,
            "step_requests": f"GET {SOURCE_URL} → HTTP {code}",
            "step_bs4": "BeautifulSoup + пошук заголовків article h2, article h3",
            "statistics": html_summary(html),
            "articles": articles, "html_excerpt": html[:1600],
            "notice": "Якщо сайт змінив верстку, парсер може не знайти записів. Це навчальна демонстрація, не моніторинг."
        })
    except requests.RequestException as exc:
        return jsonify(error="Не вдалося отримати сторінку/robots.txt. Використайте навчальний режим.", detail=type(exc).__name__), 502
    except Exception:
        return jsonify(error="Непередбачена помилка обробки. Використайте навчальний режим."), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
