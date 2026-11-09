# autotransport-europa.ch

Onepage-Webseite (plus Seite für Impressum & Datenschutz). Reines HTML/CSS/JS, kein Build nötig. Gehostet auf Cloudflare Pages (automatisch bei jedem Push auf `main`). Kontakt läuft direkt über WhatsApp, Telefon, Viber, Telegram und E-Mail (kein Formular).

## Struktur

Alle Dateien der Webseite liegen im Ordner `public/`.

```
index.html          Startseite (Hero, Leistungen: Anhänger bis 3,5 t + Überführung, Ablauf, Galerie, Kontakt)
impressum.html      Impressum & Datenschutz
agb.html            AGB (Transport, Vorauszahlung, Verladung)
css/style.css       Design (Farben ganz oben unter :root)
js/main.js          Menü, Galerie-Lightbox, Animationen
fonts/              Schriften (lokal, datenschutzfreundlich)
img/                Bilder und Logo (logo.svg) (Platzhalter, gleich benannt ersetzen)
robots.txt, sitemap.xml   SEO
_headers            Caching-Regeln für Cloudflare
```

## Sprachen

Deutsch ist `public/index.html`. Englisch (`public/en/`), Italienisch (`public/it/`) und Bosnisch/Kroatisch (`public/bs/`) werden daraus erzeugt:

```
python3 tools/build_i18n.py
```

Wer einen deutschen Text ändert, muss die Übersetzung in `tools/build_i18n.py` (Liste `TEXTS`) anpassen und das Skript erneut ausführen. Das Skript meldet Texte, die es nicht mehr findet. AGB, Impressum und Datenschutz gibt es nur auf Deutsch.

## Texte und Bilder ersetzen

- Galerie (Slideshow): Fotos liegen in `img/galerie/` (max. 1280 px, unter ca. 350 KB) und als Vorschau in `img/galerie/thumbs/` (240 × 180 px). Neues Foto: in beide Ordner legen und in `index.html` je eine Zeile bei `slides` und `ss-thumbs` kopieren.
- Bilder im Ordner `img/` mit **gleichem Dateinamen** überschreiben. Empfohlene Grössen stehen auf den Platzhalterbildern. Fotos vorher komprimieren (z. B. squoosh.app, unter 300 KB pro Bild).
- Bild-Beschreibungen (`alt="..."`) sinnvoll ausfüllen, das hilft bei Google.
- Farben ändern: `--accent` usw. ganz oben in `css/style.css` (Braun #8B7355 (burlywood4) mit Verlauf, Babyblau #6CA6CD, Off-White #F6EFE4).
- Schreibschrift für Highlight-Wörter: Wort in `<span class="script">…</span>` setzen. Schriften liegen lokal in `fonts/` (Outfit + Allura, beide frei unter OFL), kein Google-Fonts-Aufruf nötig.

## Veröffentlichen mit Cloudflare (Workers)

1. Cloudflare Dashboard → **Workers & Pages** → **Create** → **Import a repository** → `autotransport-europa.ch` wählen.
2. Build-Befehl leer lassen, Bereitstellungsbefehl `npx wrangler deploy` (Standard). Die Einstellungen stehen in `wrangler.jsonc` (Ordner `public/`). → **Bereitstellen**. Danach ist die Seite unter `*.workers.dev` erreichbar.
3. Domain zu Cloudflare: **Add a domain** → `autotransport-europa.ch` → Free-Plan. Bei Hostpoint (Domains → Nameserver) die zwei Cloudflare-Nameserver eintragen (bis 24 h).
4. Im Worker → **Settings → Domains & Routes** → **Custom domain**: `www.autotransport-europa.ch` und `autotransport-europa.ch` hinzufügen.
5. Optional: **Rules → Redirect Rules** `autotransport-europa.ch` → `https://www.autotransport-europa.ch` (301).

Jede Änderung auf `main` wird automatisch veröffentlicht.

## Sichtbar auf Google

Die Seite enthält bereits: Titel & Beschreibung, Canonical-URL, Open-Graph-Vorschau, strukturierte Daten (LocalBusiness), `sitemap.xml`, `robots.txt`, HTTPS-/www-Weiterleitung.

1. **Google Search Console**: https://search.google.com/search-console → *Property hinzufügen* → Typ **Domain** → `autotransport-europa.ch`.
2. Google zeigt einen TXT-Eintrag (`google-site-verification=...`). Diesen bei Cloudflare unter **DNS → Records** als **TXT** für `@` eintragen, dann in der Search Console auf *Bestätigen* klicken (kann bis zu einigen Stunden dauern).
3. Links unter **Sitemaps** `sitemap.xml` einreichen.
4. Unter **URL-Prüfung** `https://www.autotransport-europa.ch/` eingeben → *Indexierung beantragen*.
5. **Google Unternehmensprofil** (https://business.google.com) anlegen, mit gleicher Adresse und Telefonnummer wie auf der Webseite. Das ist der wichtigste Schritt für lokale Suchen wie «Autotransport Bern» und für Google Maps.
6. Strukturierte Daten testen: https://search.google.com/test/rich-results

Tipps: Konkrete Orte/Regionen im Text nennen («Autotransport von Zürich nach Deutschland»), Bewertungen im Google-Profil sammeln, Seite von anderen Verzeichnissen (local.ch, search.ch) verlinken lassen.
