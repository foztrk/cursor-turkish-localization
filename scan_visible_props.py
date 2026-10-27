# -*- coding: utf-8 -*-
"""Hover/tooltip ve diğer görünür prop adaylarını düşük gürültüyle tarar."""
import collections
import io
import json
import os
import re

FILES = ["workbench.desktop.main.js", "workbench.glass.main.js"]
HOVER_PROPS = {"title", "tooltip", "ariaLabel", "aria-label"}
PROPS = (
    "title", "tooltip", "ariaLabel", "aria-label", "label", "placeholder",
    "heading", "header", "subtitle", "emptyMessage", "buttonLabel",
    "primaryButtonLabel", "secondaryButtonLabel", "confirmLabel",
    "cancelLabel", "okLabel", "message", "detail", "description",
)
VALUE_RE = re.compile(
    r'(?P<prop>(?:"aria-label"|' + "|".join(re.escape(p) for p in PROPS if p != "aria-label") +
    r')):(?P<value>"(?:\\.|[^"\\])*")'
)
TURKISH = re.compile("[çğıöşüÇĞİÖŞÜ]")
TECHNICAL = re.compile(
    r"^(?:[a-z0-9_.:/@-]+|[A-Z0-9_]+|#[0-9a-fA-F]+|--[a-z-]+)$"
)
ACTION_WORDS = {
    "account", "actions", "add", "apply", "archive", "back", "branches",
    "browse", "cancel", "check", "clear", "close", "collapse", "command",
    "copy", "create", "delete", "dismiss", "download", "edit", "exit",
    "expand", "export", "file", "folder", "forward", "help", "history",
    "import", "install", "kill", "marketplace", "menu", "more", "move",
    "open", "options", "pin", "refresh", "remove", "rename", "restore",
    "retry", "save", "search", "settings", "share", "start", "stop",
    "terminal", "unpin", "update", "upload",
}
TURKISH_ASCII_WORDS = {"ajan", "denetimli", "eylemleri", "listesi", "terminal", "yeni"}
DEVELOPER_ONLY_WORDS = {"profiler", "trace"}


def visible_english_candidate(value):
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not (2 <= len(value) <= 240):
        return False
    if TURKISH.search(value) or TECHNICAL.match(value):
        return False
    if not re.search("[A-Za-z]", value):
        return False
    # Kısa hover etiketlerini (Archive, Pin, Restore vb.) kaçırmamak için eski
    # İngilizce sözcük listesine bağlı kalma. Görünür bir prop ve Başlık Biçimi
    # veya cümle biçimi olması yeterlidir.
    return value[0].isupper() or " " in value


def high_confidence_hover(value):
    """Kisa eylem tooltiplerini öne çıkar; kod/test cümlelerini raporun altına iter."""
    words = re.findall(r"[A-Za-z]+", value.lower())
    if not words or len(words) > 8:
        return False
    if (value.startswith("Developer:")
            or any(word in TURKISH_ASCII_WORDS for word in words)
            or any(word in DEVELOPER_ONLY_WORDS for word in words)):
        return False
    return any(word in ACTION_WORDS for word in words)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    translations = json.load(io.open("cursor-ui-tm.json", encoding="utf-8"))
    translated_values = {value for value in translations.values()
                         if isinstance(value, str)}
    known = set(json.load(io.open("bilinen-ingilizce.json", encoding="utf-8")))
    found = collections.defaultdict(lambda: {"count": 0, "props": set(), "files": set()})
    for filename in FILES:
        if not os.path.exists(filename):
            continue
        source = io.open(filename, encoding="utf-8").read()
        for match in VALUE_RE.finditer(source):
            try:
                value = json.loads(match.group("value"))
            except (TypeError, ValueError):
                continue
            if (value in translations or value in translated_values or value in known
                    or not visible_english_candidate(value)):
                continue
            item = found[value]
            item["count"] += 1
            item["props"].add(match.group("prop").strip('"'))
            item["files"].add(filename)

    hover = {value: item for value, item in found.items()
             if item["props"] & HOVER_PROPS}
    priority = {value: item for value, item in hover.items()
                if high_confidence_hover(value)}
    other_hover = {value: item for value, item in hover.items()
                   if value not in priority}
    visible = {value: item for value, item in found.items()
               if not (item["props"] & HOVER_PROPS)}

    def write_section(handle, title, items):
        handle.write("=== %s (%d) ===\n" % (title, len(items)))
        for value in sorted(items, key=str.casefold):
            item = items[value]
            handle.write("[%s | %dx] %s\n" % (
                ",".join(sorted(item["props"])), item["count"], value
            ))
        handle.write("\n")

    output = "YENI-HOVER-ETIKETLER.txt"
    with io.open(output, "w", encoding="utf-8") as handle:
        handle.write("Yuksek guvenli hover adayi: %d\n" % len(priority))
        handle.write("Diger hover adayi: %d\n" % len(other_hover))
        handle.write("Diger gorunur prop adayi: %d\n\n" % len(visible))
        write_section(handle, "ONCELIKLI HOVER / TOOLTIP", priority)
        write_section(handle, "DIGER HOVER / TOOLTIP", other_hover)
        write_section(handle, "DIGER GORUNUR PROPLAR", visible)
    print("%s: %d oncelikli, %d diger hover, %d gorunur prop" % (
        output, len(priority), len(other_hover), len(visible)
    ))


if __name__ == "__main__":
    main()
