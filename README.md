# autotransport-europa.ch

Onepage-Webseite (plus Seite für Impressum & Datenschutz). Reines HTML/CSS/JS, kein Build nötig. Das Kontaktformular läuft über PHP auf Hostpoint.

## Struktur

```
index.html          Startseite (Hero, Leistungen: Anhänger bis 3,5 t + Überführung, Ablauf, Galerie, Über uns, Kontakt)
impressum.html      Impressum & Datenschutz (2. Seite)
kontakt.php         Versand des Kontaktformulars per E-Mail
css/style.css       Design (Farben ganz oben unter :root)
js/main.js          Menü, Galerie-Lightbox, Formular
fonts/              Schriften (lokal, datenschutzfreundlich)
img/                Bilder (Platzhalter, gleich benannt ersetzen)
robots.txt, sitemap.xml, .htaccess   SEO und Weiterleitungen
.github/workflows/deploy.yml         Automatischer Upload zu Hostpoint
```

## Texte und Bilder ersetzen

- Alle Stellen mit `[PLATZHALTER]` in `index.html`, `impressum.html` und `kontakt.php` ersetzen.
- Bilder im Ordner `img/` mit **gleichem Dateinamen** überschreiben. Empfohlene Grössen stehen auf den Platzhalterbildern. Fotos vorher komprimieren (z. B. squoosh.app, unter 300 KB pro Bild).
- Bild-Beschreibungen (`alt="..."`) sinnvoll ausfüllen, das hilft bei Google.
- Farben ändern: `--accent` usw. ganz oben in `css/style.css` (Braun #8B7355 (burlywood4) mit Verlauf, Babyblau #6CA6CD, Off-White #F6EFE4).
- Schreibschrift für Highlight-Wörter: Wort in `<span class="script">…</span>` setzen. Schriften liegen lokal in `fonts/` (Outfit + Great Vibes, beide frei unter OFL), kein Google-Fonts-Aufruf nötig.

## Veröffentlichen auf Hostpoint (automatisch via GitHub)

1. Im Hostpoint Control Panel unter **Webhosting → FTP-Benutzer** einen FTP-Benutzer anlegen (oder den bestehenden nehmen). Notieren: Server, Benutzername, Passwort.
2. Prüfen, in welchem Ordner die Domain liegt (**Domains → autotransport-europa.ch → Zielverzeichnis**, z. B. `www/autotransport-europa.ch`). Falls abweichend, `server-dir` in `.github/workflows/deploy.yml` anpassen.
3. Im GitHub-Repo unter **Settings → Secrets and variables → Actions** drei Secrets anlegen: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.
4. Ab jetzt wird bei jedem Push auf `main` automatisch hochgeladen. Status unter dem Tab **Actions**.
5. SSL: Im Control Panel für die Domain das kostenlose **Let's Encrypt-Zertifikat** aktivieren (die `.htaccess` leitet dann auf `https://www.` um).
6. E-Mail: Die Adresse `info@autotransport-europa.ch` muss bei Hostpoint als Postfach oder Weiterleitung existieren, sonst kommen Formular-Anfragen nicht an.

## Sichtbar auf Google

Die Seite enthält bereits: Titel & Beschreibung, Canonical-URL, Open-Graph-Vorschau, strukturierte Daten (LocalBusiness), `sitemap.xml`, `robots.txt`, HTTPS-/www-Weiterleitung.

1. **Google Search Console**: https://search.google.com/search-console → *Property hinzufügen* → Typ **Domain** → `autotransport-europa.ch`.
2. Google zeigt einen TXT-Eintrag (`google-site-verification=...`). Diesen im Hostpoint Control Panel unter **Domains → DNS-Einträge** als **TXT** für `@` eintragen, dann in der Search Console auf *Bestätigen* klicken (kann bis zu einigen Stunden dauern).
3. Links unter **Sitemaps** `sitemap.xml` einreichen.
4. Unter **URL-Prüfung** `https://www.autotransport-europa.ch/` eingeben → *Indexierung beantragen*.
5. **Google Unternehmensprofil** (https://business.google.com) anlegen, mit gleicher Adresse und Telefonnummer wie auf der Webseite. Das ist der wichtigste Schritt für lokale Suchen wie «Autotransport Bern» und für Google Maps.
6. Strukturierte Daten testen: https://search.google.com/test/rich-results

Tipps: Konkrete Orte/Regionen im Text nennen («Autotransport von Zürich nach Deutschland»), Bewertungen im Google-Profil sammeln, Seite von anderen Verzeichnissen (local.ch, search.ch) verlinken lassen.
