# autotransport-europa.ch

Onepage-Webseite (plus Seite für Impressum & Datenschutz). Reines HTML/CSS/JS, kein Build nötig. Gehostet auf Cloudflare Pages (automatisch bei jedem Push auf `main`). Kontakt läuft direkt über WhatsApp, Telefon, Viber, Telegram und E-Mail (kein Formular).

## Struktur

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

## Texte und Bilder ersetzen

- Galerie-Fotos: `img/galerie-1.jpg` bis `galerie-6.jpg` (1200 × 900 px) mit eigenen Fotos überschreiben.
- Bilder im Ordner `img/` mit **gleichem Dateinamen** überschreiben. Empfohlene Grössen stehen auf den Platzhalterbildern. Fotos vorher komprimieren (z. B. squoosh.app, unter 300 KB pro Bild).
- Bild-Beschreibungen (`alt="..."`) sinnvoll ausfüllen, das hilft bei Google.
- Farben ändern: `--accent` usw. ganz oben in `css/style.css` (Braun #8B7355 (burlywood4) mit Verlauf, Babyblau #6CA6CD, Off-White #F6EFE4).
- Schreibschrift für Highlight-Wörter: Wort in `<span class="script">…</span>` setzen. Schriften liegen lokal in `fonts/` (Outfit + Allura, beide frei unter OFL), kein Google-Fonts-Aufruf nötig.

## Veröffentlichen mit Cloudflare Pages

1. Cloudflare Dashboard → **Workers & Pages** → **Create** → Tab **Pages** → **Connect to Git** → Repo `autotransport-europa.ch` wählen.
2. Einstellungen: Framework preset **None**, Build command **leer lassen**, Build output directory **`/`**. → **Save and Deploy**. Die Seite ist danach unter `*.pages.dev` erreichbar.
3. Domain zu Cloudflare: **Add a domain** → `autotransport-europa.ch` → Free-Plan. Cloudflare zeigt zwei Nameserver.
4. Bei Hostpoint (Control Panel → Domains → autotransport-europa.ch → **Nameserver**) die beiden Cloudflare-Nameserver eintragen. Dauert bis zu 24 h.
5. Im Pages-Projekt → **Custom domains** → `www.autotransport-europa.ch` und `autotransport-europa.ch` hinzufügen. SSL macht Cloudflare automatisch.
6. Optional: Unter **Rules → Redirect Rules** `autotransport-europa.ch` → `https://www.autotransport-europa.ch` (301) weiterleiten.

Ab dann wird jede Änderung auf `main` automatisch veröffentlicht.

## Sichtbar auf Google

Die Seite enthält bereits: Titel & Beschreibung, Canonical-URL, Open-Graph-Vorschau, strukturierte Daten (LocalBusiness), `sitemap.xml`, `robots.txt`, HTTPS-/www-Weiterleitung.

1. **Google Search Console**: https://search.google.com/search-console → *Property hinzufügen* → Typ **Domain** → `autotransport-europa.ch`.
2. Google zeigt einen TXT-Eintrag (`google-site-verification=...`). Diesen bei Cloudflare unter **DNS → Records** als **TXT** für `@` eintragen, dann in der Search Console auf *Bestätigen* klicken (kann bis zu einigen Stunden dauern).
3. Links unter **Sitemaps** `sitemap.xml` einreichen.
4. Unter **URL-Prüfung** `https://www.autotransport-europa.ch/` eingeben → *Indexierung beantragen*.
5. **Google Unternehmensprofil** (https://business.google.com) anlegen, mit gleicher Adresse und Telefonnummer wie auf der Webseite. Das ist der wichtigste Schritt für lokale Suchen wie «Autotransport Bern» und für Google Maps.
6. Strukturierte Daten testen: https://search.google.com/test/rich-results

Tipps: Konkrete Orte/Regionen im Text nennen («Autotransport von Zürich nach Deutschland»), Bewertungen im Google-Profil sammeln, Seite von anderen Verzeichnissen (local.ch, search.ch) verlinken lassen.
