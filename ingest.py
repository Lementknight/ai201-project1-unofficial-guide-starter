#!/usr/bin/env python3
"""
Milestone 3: Document Ingestion & Semantic Chunking
Fetches 10 source URLs, extracts clean text, chunks semantically, saves JSON files.
"""

import json
import os
import re
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    import trafilatura
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False

try:
    from readability import Document
    READABILITY_AVAILABLE = True
except ImportError:
    READABILITY_AVAILABLE = False

SOURCES = [
    # Original 10 sources
    "https://anderscpa.com/learn/blog/understanding-employee-benefits-guide-for-recent-graduates/",
    "https://turbotax.intuit.com/tax-tips/jobs-and-career/guide-to-your-employers-benefits-programs-tax-wise-401k-matching-hsas-flexible-etc/L74Iljjyz",
    "https://www.fhb.com/en/resource-center/life-stages/workplace-financial-benefits-a-beginners-guide",
    "https://www.metlife.com/stories/benefits/hdhp-vs-ppo/",
    "https://www.cigna.com/knowledge-center/hdhp-vs-ppo-plans",
    "https://www.dol.gov/general/topic/health-plans/erisa",
    "https://www.dol.gov/agencies/ebsa/about-ebsa/our-activities/resource-center/publications/filing-a-claim-for-your-health-benefits",
    "https://www.wovencapital.net/how-to-evaluate-equity-compensation-in-your-first-tech-job-offer-rsus-stock-options-and-vesting-schedules-explained/",
    "https://www.reddit.com/r/personalfinance/wiki/commontopics",
    "https://www.randstadusa.com/job-seeker/career-advice/salary/how-to-negotiate-benefits-package/",
    # New 5 sources (commuter benefits, enrollment decisions, general benefits)
    "https://livelyme.com/blog/pre-tax-commuter-benefit-contribution-limits",
    "https://getbenepass.com/blog/pre-tax-commuter-benefits",
    "https://www.healthcare.gov/have-job-based-coverage/",
    "https://thatch.com/blog/opting-out-employer-health-insurance-special-considerations",
    "https://www.deel.com/blog/types-of-employee-benefits/",
]

CHUNK_SIZE = 1500
OVERLAP = 200
OUTPUT_DIR = "documents"
MIN_CONTENT_LENGTH = 200

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; AI201-RAG-Bot/1.0; student project)"
}


def fetch_html(url: str) -> Optional[str]:
    """
    Fetch HTML from URL with a realistic User-Agent header.
    First tries requests (fast), then falls back to Playwright for JS-heavy sites.
    Returns raw HTML string, or None on failure.
    """
    # Try requests first (fast)
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        html = response.text
        # If we got a reasonable amount of content AND it has article-like structure, use it
        if len(html) > 10000 and any(tag in html for tag in ["<article", "<main", "<body"]):
            return html
    except requests.RequestException as e:
        pass

    # Fall back to Playwright for JS-heavy sites
    if not PLAYWRIGHT_AVAILABLE:
        return None

    try:
        print(f"  (requests insufficient or JS-heavy, using Playwright...)")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=30000)
            html = page.content()
            browser.close()
            return html if len(html) > 2000 else None
    except Exception as e:
        return None


def extract_with_trafilatura(html: str) -> Optional[str]:
    """
    Try extracting text with trafilatura (optimized for articles).
    Returns clean article text or None.
    """
    if not TRAFILATURA_AVAILABLE:
        return None
    try:
        extracted = trafilatura.extract(html, include_comments=False, favor_precision=True)
        return extracted if extracted and len(extracted) > MIN_CONTENT_LENGTH else None
    except Exception:
        return None


def extract_with_readability(html: str) -> Optional[str]:
    """
    Try extracting text with readability (Mozilla's algorithm).
    Returns clean article text or None.
    """
    if not READABILITY_AVAILABLE:
        return None
    try:
        doc = Document(html)
        text = doc.summary()
        # Convert HTML summary to plain text
        soup = BeautifulSoup(text, "html.parser")
        clean_text = soup.get_text(separator="\n", strip=True)
        return clean_text if len(clean_text) > MIN_CONTENT_LENGTH else None
    except Exception:
        return None


def extract_with_beautifulsoup(html: str) -> Optional[list[tuple[str, str]]]:
    """
    Fallback: Parse HTML with BeautifulSoup and extract clean text.
    Removes noise tags (script, style, nav, footer, ads, etc.).
    Returns list of (section_heading, text_block) tuples, or None if extraction fails.
    """
    try:
        soup = BeautifulSoup(html, "html.parser")

        # Remove noise tags and elements
        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Remove cookie banners, modals, ads
        for tag in soup.find_all(class_=re.compile(r"cookie|banner|modal|ad|popup")):
            tag.decompose()
        for tag in soup.find_all(id=re.compile(r"cookie|banner|modal|ad|nav|sidebar")):
            tag.decompose()

        # Find article body with priority
        article = (
            soup.find("article")
            or soup.find("main")
            or soup.find(role="main")
            or soup.find("div", class_=re.compile(r"content|article"))
            or soup.find("body")
        )

        if not article:
            return None

        # Walk DOM and collect (heading, text) pairs
        sections = []
        current_section = "Introduction"

        for element in article.find_all(recursive=True):
            if element.name in ["h2", "h3"]:
                current_section = element.get_text(strip=True)
            elif element.name in ["p", "li"]:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # filter short fragments
                    sections.append((current_section, text))

        if not sections or sum(len(t) for _, t in sections) < MIN_CONTENT_LENGTH:
            return None

        return sections
    except Exception as e:
        return None


def extract_text(html: str, url: str) -> Optional[list[tuple[str, str]]]:
    """
    Extract clean text from HTML using multiple extraction methods in sequence.
    Tries: trafilatura → readability → BeautifulSoup.
    Returns list of (section_heading, text_block) tuples, or None if all fail.
    """
    # Try trafilatura first (best for articles)
    trafilatura_text = extract_with_trafilatura(html)
    if trafilatura_text:
        sections = [(f"Article Content", line) for line in trafilatura_text.split("\n") if line.strip() and len(line.strip()) > 20]
        if sections:
            return sections

    # Try readability next (Mozilla algorithm)
    readability_text = extract_with_readability(html)
    if readability_text:
        sections = [(f"Article Content", line) for line in readability_text.split("\n") if line.strip() and len(line.strip()) > 20]
        if sections:
            return sections

    # Fall back to BeautifulSoup
    bs_sections = extract_with_beautifulsoup(html)
    if bs_sections:
        return bs_sections

    return None


def chunk_text(
    sections: list[tuple[str, str]],
    chunk_size: int = CHUNK_SIZE,
    overlap: int = OVERLAP,
) -> list[str]:
    """
    Chunk text while respecting semantic boundaries (section headers).
    Prepends section heading to each text block for context.
    Cuts at sentence boundaries when possible.
    """
    chunks = []
    buffer = ""
    buffer_heading = ""

    for heading, text in sections:
        # Prepend heading to the first text in a new section
        if heading != buffer_heading and buffer:
            buffer_heading = heading

        # Add text to buffer with heading context
        if not buffer:
            buffer = f"{heading}: {text}"
            buffer_heading = heading
        else:
            buffer += " " + text

        # When buffer exceeds chunk size, flush it
        if len(buffer) >= chunk_size:
            # Try to cut at sentence boundary
            cut_pos = chunk_size
            for pattern in [". ", "? ", "! "]:
                pos = buffer.rfind(pattern, 0, chunk_size)
                if pos > chunk_size * 0.8:  # at least 80% of intended size
                    cut_pos = pos + len(pattern)
                    break
            else:
                # Fall back to last space before chunk_size
                cut_pos = buffer.rfind(" ", 0, chunk_size)
                if cut_pos == -1:
                    cut_pos = chunk_size

            chunk = buffer[:cut_pos].strip()
            chunks.append(chunk)

            # Start next buffer with overlap from end of current chunk
            buffer = buffer[max(0, cut_pos - overlap) :].strip()

    # Flush remaining buffer
    if buffer and len(buffer) > 50:
        chunks.append(buffer)

    return chunks


def save_chunks(chunks: list[str], source_url: str, output_dir: str) -> int:
    """
    Save chunks as JSON files.
    Returns the number of chunks saved.
    """
    Path(output_dir).mkdir(exist_ok=True)

    # Find the next global chunk index
    existing_files = list(Path(output_dir).glob("chunk_*.json"))
    next_index = len(existing_files)

    saved_count = 0
    for i, chunk_text in enumerate(chunks):
        chunk_index = next_index + i
        filename = Path(output_dir) / f"chunk_{chunk_index:04d}.json"

        data = {
            "source_url": source_url,
            "chunk_index": chunk_index,
            "chunk_text": chunk_text,
            "char_count": len(chunk_text),
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        saved_count += 1

    return saved_count


def main():
    """
    Main ingestion loop: fetch, extract, chunk, and save each source.
    """
    print("Starting document ingestion...\n")

    total_chunks = 0

    for url in SOURCES:
        print(f"Processing: {url}")

        html = fetch_html(url)
        if not html:
            continue

        sections = extract_text(html, url)
        if not sections:
            print(f"  WARNING: {url} returned insufficient content. Skipped.\n")
            continue

        chunks = chunk_text(sections)
        saved = save_chunks(chunks, url, OUTPUT_DIR)
        total_chunks += saved

        print(f"  ✓ Extracted {len(sections)} sections, created {saved} chunks\n")

    print(f"Done! Total chunks saved: {total_chunks}")
    print(f"Chunks stored in: {Path(OUTPUT_DIR).absolute()}")


if __name__ == "__main__":
    main()
