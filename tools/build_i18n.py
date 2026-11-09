#!/usr/bin/env python3
"""Erzeugt die Sprachversionen (en, it, bs) aus public/index.html (Deutsch).

Nach jeder Textänderung in public/index.html ausführen:
    python3 tools/build_i18n.py
Neue oder geänderte deutsche Texte müssen unten in TEXTS ergänzt werden,
sonst bricht das Skript mit einer Meldung ab.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "public"
SRC = ROOT / "index.html"

LANGS = {
    "en": {"locale": "en_GB", "html": "en", "of": "of", "show": "Show image {}"},
    "it": {"locale": "it_CH", "html": "it", "of": "di", "show": "Mostra immagine {}"},
    "bs": {"locale": "bs_BA", "html": "bs", "of": "od", "show": "Prikaži sliku {}"},
}

# (Deutsch, Englisch, Italienisch, Bosnisch/Kroatisch). Längere Texte zuerst prüfen.
TEXTS = [
    # Head / SEO
    ("<title>Autotransport Schweiz &amp; Europa | Autotransport Europa &amp; Schweiz</title>",
     "<title>Car Transport Switzerland &amp; Europe | Autotransport Europa &amp; Schweiz</title>",
     "<title>Trasporto auto Svizzera &amp; Europa | Autotransport Europa &amp; Schweiz</title>",
     "<title>Prijevoz automobila Švicarska &amp; Europa | Autotransport Europa &amp; Schweiz</title>"),
    ('content="Autotransport mit Anhänger bis 3,5 t oder persönliche Überführung auf eigener Achse. In der ganzen Schweiz und in Europa, 24 Stunden erreichbar. Jetzt Offerte anfragen."',
     'content="Car transport by trailer up to 3.5 t or personal vehicle delivery on its own wheels. Throughout Switzerland and Europe, available 24 hours. Request a quote now."',
     'content="Trasporto auto con rimorchio fino a 3,5 t o trasferimento personale su strada. In tutta la Svizzera e in Europa, raggiungibile 24 ore su 24. Richiedi subito un preventivo."',
     'content="Prijevoz automobila prikolicom do 3,5 t ili osobni prijevoz vozila na vlastitim kotačima. U cijeloj Švicarskoj i Europi, dostupni 24 sata. Zatražite ponudu odmah."'),
    ('content="Autotransport Schweiz &amp; Europa | Autotransport Europa &amp; Schweiz"',
     'content="Car Transport Switzerland &amp; Europe | Autotransport Europa &amp; Schweiz"',
     'content="Trasporto auto Svizzera &amp; Europa | Autotransport Europa &amp; Schweiz"',
     'content="Prijevoz automobila Švicarska &amp; Europa | Autotransport Europa &amp; Schweiz"'),
    ('content="Autotransport mit Anhänger bis 3,5 t oder persönliche Überführung, in der Schweiz und in ganz Europa."',
     'content="Car transport by trailer up to 3.5 t or personal vehicle delivery, in Switzerland and all over Europe."',
     'content="Trasporto auto con rimorchio fino a 3,5 t o trasferimento personale, in Svizzera e in tutta Europa."',
     'content="Prijevoz automobila prikolicom do 3,5 t ili osobni prijevoz vozila, u Švicarskoj i cijeloj Europi."'),
    ('"description": "Autotransport mit Anhänger bis 3,5 t und Fahrzeugüberführung in der Schweiz und in ganz Europa."',
     '"description": "Car transport by trailer up to 3.5 t and vehicle delivery in Switzerland and all over Europe."',
     '"description": "Trasporto auto con rimorchio fino a 3,5 t e trasferimento di veicoli in Svizzera e in tutta Europa."',
     '"description": "Prijevoz automobila prikolicom do 3,5 t i prijevoz vozila u Švicarskoj i cijeloj Europi."'),
    ('{"@type": "Country", "name": "Schweiz"}', '{"@type": "Country", "name": "Switzerland"}',
     '{"@type": "Country", "name": "Svizzera"}', '{"@type": "Country", "name": "Švicarska"}'),

    # Attribute
    ('aria-label="Autotransport Europa &amp; Schweiz, zur Startseite"',
     'aria-label="Autotransport Europa &amp; Schweiz, to the home page"',
     'aria-label="Autotransport Europa &amp; Schweiz, alla pagina iniziale"',
     'aria-label="Autotransport Europa &amp; Schweiz, na početnu stranicu"'),
    ('aria-label="Hauptnavigation"', 'aria-label="Main navigation"', 'aria-label="Navigazione principale"', 'aria-label="Glavna navigacija"'),
    ('aria-label="Menü öffnen"', 'aria-label="Open menu"', 'aria-label="Apri menu"', 'aria-label="Otvori izbornik"'),
    ('aria-label="Sprache"', 'aria-label="Language"', 'aria-label="Lingua"', 'aria-label="Jezik"'),
    ('alt="Geländewagen zieht einen Autoanhänger mit zwei Limousinen"',
     'alt="SUV towing a car trailer carrying two saloon cars"',
     'alt="SUV che traina un rimorchio con due berline"',
     'alt="Terenac vuče prikolicu s dvije limuzine"'),
    # Galerie-Slideshow
    ('alt="20-Fuss-Container sicher gesichert"', 'alt="20-foot container securely fastened"', 'alt="Container da 20 piedi fissato in sicurezza"', 'alt="Kontejner od 20 stopa sigurno učvršćen"'),
    ('alt="Anhänger abgesenkt, bereit zum Verladen"', 'alt="Trailer lowered, ready for loading"', 'alt="Rimorchio abbassato, pronto per il carico"', 'alt="Spuštena prikolica, spremna za utovar"'),
    ('alt="Audi Q7 auf dem Autoanhänger"', 'alt="Audi Q7 on the car trailer"', 'alt="Audi Q7 sul rimorchio"', 'alt="Audi Q7 na auto prikolici"'),
    ('alt="Audi RS6 Abholung beim Autohaus"', 'alt="Audi RS6 pick-up at the dealership"', 'alt="Ritiro di un\'Audi RS6 dal concessionario"', 'alt="Preuzimanje Audija RS6 u autosalonu"'),
    ('alt="Audi RS6 bei der Abholung beim Händler"', 'alt="Audi RS6 being collected from the dealer"', 'alt="Audi RS6 al ritiro dal concessionario"', 'alt="Audi RS6 pri preuzimanju kod prodavača"'),
    ('alt="BMW 3er bei der Abholung beim Autohändler"', 'alt="BMW 3 Series being collected from the car dealer"', 'alt="BMW Serie 3 al ritiro dal concessionario"', 'alt="BMW serije 3 pri preuzimanju kod prodavača"'),
    ('alt="BMW 3er sicher verzurrt auf dem Anhänger"', 'alt="BMW 3 Series securely strapped on the trailer"', 'alt="BMW Serie 3 fissata in sicurezza sul rimorchio"', 'alt="BMW serije 3 sigurno pričvršćen na prikolici"'),
    ('alt="BMW X6 sicher auf dem Autoanhänger"', 'alt="BMW X6 secured on the car trailer"', 'alt="BMW X6 fissata sul rimorchio"', 'alt="BMW X6 sigurno na auto prikolici"'),
    ('alt="Container-Transport mit dem Dreiachs-Anhänger"', 'alt="Container transport with the three-axle trailer"', 'alt="Trasporto container con il rimorchio a tre assi"', 'alt="Prijevoz kontejnera troosovinskom prikolicom"'),
    ('alt="Doppeltransport BMW und Hyundai bei Sonnenschein"', 'alt="Double transport of a BMW and a Hyundai in the sunshine"', 'alt="Doppio trasporto BMW e Hyundai sotto il sole"', 'alt="Dvostruki prijevoz BMW-a i Hyundaija po suncu"'),
    ('alt="Doppeltransport bei Nacht"', 'alt="Double transport at night"', 'alt="Doppio trasporto di notte"', 'alt="Dvostruki prijevoz noću"'),
    ('alt="Doppeltransport in der Nacht"', 'alt="Double transport during the night"', 'alt="Doppio trasporto nella notte"', 'alt="Dvostruki prijevoz u noći"'),
    ('alt="Doppeltransport mit zwei BMW Limousinen"', 'alt="Double transport with two BMW saloons"', 'alt="Doppio trasporto con due berline BMW"', 'alt="Dvostruki prijevoz s dvije BMW limuzine"'),
    ('alt="Einzeltransport auf dem Tandem-Anhänger"', 'alt="Single transport on the tandem trailer"', 'alt="Trasporto singolo sul rimorchio tandem"', 'alt="Pojedinačni prijevoz na tandem prikolici"'),
    ('alt="Fahrzeugtransport mit Mercedes A-Klasse"', 'alt="Vehicle transport with a Mercedes A-Class"', 'alt="Trasporto di una Mercedes Classe A"', 'alt="Prijevoz Mercedesa A-klase"'),
    ('alt="Gespann bei Sonnenuntergang auf dem Weg zur Abholung"', 'alt="Car and trailer at sunset on the way to a pick-up"', 'alt="Auto con rimorchio al tramonto, in viaggio verso il ritiro"', 'alt="Vozilo s prikolicom u zalazak sunca na putu do preuzimanja"'),
    ('alt="Kastenwagen auf dem Anhänger, Nachtfahrt"', 'alt="Van on the trailer, night drive"', 'alt="Furgone sul rimorchio, viaggio notturno"', 'alt="Kombi na prikolici, noćna vožnja"'),
    ('alt="Mercedes A-Klasse bei der Abholung in der Werkstatt"', 'alt="Mercedes A-Class being collected from the garage"', 'alt="Mercedes Classe A al ritiro in officina"', 'alt="Mercedes A-klase pri preuzimanju u radionici"'),
    ('alt="Mercedes SUV wird auf den Anhänger gezogen"', 'alt="Mercedes SUV being winched onto the trailer"', 'alt="SUV Mercedes tirato sul rimorchio"', 'alt="Mercedes SUV se povlači na prikolicu"'),
    ('alt="Mercedes Vito auf dem Autoanhänger"', 'alt="Mercedes Vito on the car trailer"', 'alt="Mercedes Vito sul rimorchio"', 'alt="Mercedes Vito na auto prikolici"'),
    ('alt="Nachtfahrt mit beleuchtetem Autoanhänger"', 'alt="Night drive with an illuminated car trailer"', 'alt="Viaggio notturno con rimorchio illuminato"', 'alt="Noćna vožnja s osvijetljenom auto prikolicom"'),
    ('alt="Porsche Cayenne auf dem Autoanhänger"', 'alt="Porsche Cayenne on the car trailer"', 'alt="Porsche Cayenne sul rimorchio"', 'alt="Porsche Cayenne na auto prikolici"'),
    ('alt="Porsche Cayenne auf dem Weg zum Kunden"', 'alt="Porsche Cayenne on the way to the customer"', 'alt="Porsche Cayenne in viaggio verso il cliente"', 'alt="Porsche Cayenne na putu do kupca"'),
    ('alt="Porsche Cayenne bei der Übergabe"', 'alt="Porsche Cayenne at handover"', 'alt="Porsche Cayenne alla consegna"', 'alt="Porsche Cayenne pri predaji"'),
    ('alt="Porsche Cayenne bereit für die Überführung"', 'alt="Porsche Cayenne ready for delivery"', 'alt="Porsche Cayenne pronta per il trasferimento"', 'alt="Porsche Cayenne spreman za prijevoz"'),
    ('alt="Porsche Cayenne wird verzurrt"', 'alt="Porsche Cayenne being strapped down"', 'alt="Porsche Cayenne in fase di fissaggio"', 'alt="Porsche Cayenne se pričvršćuje"'),
    ('alt="Porsche Panamera auf dem Dreiachs-Anhänger"', 'alt="Porsche Panamera on the three-axle trailer"', 'alt="Porsche Panamera sul rimorchio a tre assi"', 'alt="Porsche Panamera na troosovinskoj prikolici"'),
    ('alt="Porsche Panamera bei Nacht unterwegs"', 'alt="Porsche Panamera on the road at night"', 'alt="Porsche Panamera in viaggio di notte"', 'alt="Porsche Panamera noću na putu"'),
    ('alt="Transport von mehreren Rasentraktoren"', 'alt="Transport of several ride-on lawn mowers"', 'alt="Trasporto di diversi trattorini tosaerba"', 'alt="Prijevoz više traktorskih kosilica"'),
    ('alt="Transporter-Überführung beim Autohaus"', 'alt="Van delivery at the dealership"', 'alt="Trasferimento di un furgone dal concessionario"', 'alt="Prijevoz kombija u autosalonu"'),
    ('alt="Unterwegs auch im Winter bei Schnee"', 'alt="On the road in winter too, even in snow"', 'alt="In viaggio anche d\'inverno con la neve"', 'alt="Na putu i zimi po snijegu"'),
    ('alt="Unterwegs bei Schneefall in der Nacht"', 'alt="On the road in falling snow at night"', 'alt="In viaggio di notte sotto la neve"', 'alt="Na putu noću dok pada snijeg"'),
    ('alt="Verladen mit der Seilwinde direkt vor der Garage"', 'alt="Loading with the winch right outside the garage"', 'alt="Carico con il verricello davanti al garage"', 'alt="Utovar vitlom ispred garaže"'),
    ('alt="Zwei BMW 3er unterwegs, Pause am See"', 'alt="Two BMW 3 Series on the road, break by the lake"', 'alt="Due BMW Serie 3 in viaggio, pausa al lago"', 'alt="Dva BMW-a serije 3 na putu, pauza kraj jezera"'),
    ('alt="Zwei Fahrzeuge auf dem Dreiachs-Autoanhänger"', 'alt="Two vehicles on the three-axle car trailer"', 'alt="Due veicoli sul rimorchio a tre assi"', 'alt="Dva vozila na troosovinskoj auto prikolici"'),
    ('alt="Zwei Fiat 500 auf dem Dreiachs-Anhänger"', 'alt="Two Fiat 500s on the three-axle trailer"', 'alt="Due Fiat 500 sul rimorchio a tre assi"', 'alt="Dva Fiata 500 na troosovinskoj prikolici"'),
    ('alt="Zwei Gespanne mit je zwei Autos beim Tankstopp"', 'alt="Two rigs with two cars each at a fuel stop"', 'alt="Due convogli con due auto ciascuno durante il rifornimento"', 'alt="Dvije prikolice s po dva auta na točenju goriva"'),
    ('alt="Zwei Kleinwagen sicher verzurrt im Schnee"', 'alt="Two small cars securely strapped down in the snow"', 'alt="Due utilitarie fissate in sicurezza nella neve"', 'alt="Dva mala auta sigurno pričvršćena u snijegu"'),
    ('alt="Zwei Transporter auf der Fahrt durch die Alpen"', 'alt="Two vans on the drive through the Alps"', 'alt="Due furgoni in viaggio attraverso le Alpi"', 'alt="Dva kombija na vožnji kroz Alpe"'),
    ('aria-label="Fotogalerie Autotransporte"', 'aria-label="Photo gallery of car transports"', 'aria-label="Galleria fotografica dei trasporti"', 'aria-label="Galerija fotografija prijevoza"'),
    ('aria-roledescription="Bild"', 'aria-roledescription="Image"', 'aria-roledescription="Immagine"', 'aria-roledescription="Slika"'),
    ('aria-label="Vorheriges Bild"', 'aria-label="Previous image"', 'aria-label="Immagine precedente"', 'aria-label="Prethodna slika"'),
    ('aria-label="Nächstes Bild"', 'aria-label="Next image"', 'aria-label="Immagine successiva"', 'aria-label="Sljedeća slika"'),
    ('aria-label="Slideshow pausieren"', 'aria-label="Pause slideshow"', 'aria-label="Metti in pausa"', 'aria-label="Pauziraj prezentaciju"'),

    # Startbereich
    (">Schweiz · Europa<", ">Switzerland · Europe<", ">Svizzera · Europa<", ">Švicarska · Europa<"),
    ('<h1>Ihr Fahrzeug, <span class="script">sicher</span> ans Ziel</h1>',
     '<h1>Your vehicle, <span class="script">safely</span> to its destination</h1>',
     '<h1>Il tuo veicolo, <span class="script">sicuro</span> a destinazione</h1>',
     '<h1>Vaše vozilo <span class="script">sigurno</span> na odredište</h1>'),
    (">Autotransport mit Anhänger bis 3,5 t oder persönliche Überführung: Ich bringe Ihr Auto zuverlässig ans Ziel, in der ganzen Schweiz und in Europa.<",
     ">Car transport by trailer up to 3.5 t or personal delivery: I bring your car reliably to its destination, throughout Switzerland and Europe.<",
     ">Trasporto auto con rimorchio fino a 3,5 t o trasferimento personale: porto la tua auto a destinazione in modo affidabile, in tutta la Svizzera e in Europa.<",
     ">Prijevoz automobila prikolicom do 3,5 t ili osobni prijevoz: pouzdano dovozim Vaš automobil na odredište, u cijeloj Švicarskoj i Europi.<"),
    (">Leistungen entdecken<", ">Discover services<", ">Scopri i servizi<", ">Pogledajte usluge<"),
    ("<strong>bis 3,5 t</strong><span>Autoanhänger</span>", "<strong>up to 3.5 t</strong><span>Car trailer</span>",
     "<strong>fino a 3,5 t</strong><span>Rimorchio auto</span>", "<strong>do 3,5 t</strong><span>Auto prikolica</span>"),
    ("<span>Schweiz und Europa</span>", "<span>Switzerland and Europe</span>", "<span>Svizzera ed Europa</span>", "<span>Švicarska i Europa</span>"),
    ("<span>Erreichbar</span>", "<span>Available</span>", "<span>Raggiungibile</span>", "<span>Dostupni</span>"),

    # Leistungen
    ('<p class="eyebrow">Leistungen</p>', '<p class="eyebrow">Services</p>', '<p class="eyebrow">Servizi</p>', '<p class="eyebrow">Usluge</p>'),
    ('<h2>Was ich für Sie <span class="script">transportiere</span></h2>',
     '<h2>What I <span class="script">transport</span> for you</h2>',
     '<h2>Cosa <span class="script">trasporto</span> per te</h2>',
     '<h2>Što za Vas <span class="script">prevozim</span></h2>'),
    (">Ob auf dem Anhänger oder auf eigener Achse: Ihr Fahrzeug kommt sicher und pünktlich an.<",
     ">Whether on the trailer or on its own wheels: your vehicle arrives safely and on time.<",
     ">Sul rimorchio o su strada: il tuo veicolo arriva in sicurezza e puntuale.<",
     ">Na prikolici ili na vlastitim kotačima: Vaše vozilo stiže sigurno i na vrijeme.<"),
    ("<h3>Transport mit Anhänger</h3>", "<h3>Transport by trailer</h3>", "<h3>Trasporto con rimorchio</h3>", "<h3>Prijevoz prikolicom</h3>"),
    (">Ihr Fahrzeug reist sicher verzurrt auf meinem Autoanhänger. Geeignet für Fahrzeuge bis 3,5 t Gesamtgewicht.<",
     ">Your vehicle travels securely strapped down on my car trailer. Suitable for vehicles up to 3.5 t total weight.<",
     ">Il tuo veicolo viaggia fissato in sicurezza sul mio rimorchio. Adatto a veicoli fino a 3,5 t di peso totale.<",
     ">Vaše vozilo putuje sigurno pričvršćeno na mojoj auto prikolici. Pogodno za vozila do 3,5 t ukupne težine.<"),
    ("<h3>Persönliche Überführung</h3>", "<h3>Personal delivery</h3>", "<h3>Trasferimento personale</h3>", "<h3>Osobni prijevoz vozila</h3>"),
    (">Ich fahre Ihr Auto auf eigener Achse ans Ziel: schnell, flexibel und mit Übergabeprotokoll.<",
     ">I drive your car to its destination myself: fast, flexible and with a handover report.<",
     ">Guido personalmente la tua auto fino a destinazione: veloce, flessibile e con verbale di consegna.<",
     ">Osobno vozim Vaš automobil do odredišta: brzo, fleksibilno i uz zapisnik o primopredaji.<"),
    ("<h3>Nicht fahrbereite Fahrzeuge</h3>", "<h3>Non-roadworthy vehicles</h3>", "<h3>Veicoli non marcianti</h3>", "<h3>Vozila koja nisu u voznom stanju</h3>"),
    (">Defekt, ohne Zulassung oder nach einem Unfall: Mit dem Anhänger kommt auch Ihr nicht fahrbereites Auto ans Ziel.<",
     ">Broken down, unregistered or after an accident: with the trailer, even a car that cannot be driven reaches its destination.<",
     ">Guasto, senza immatricolazione o dopo un incidente: con il rimorchio anche la tua auto non marciante arriva a destinazione.<",
     ">U kvaru, bez registracije ili nakon nesreće: prikolicom i Vaš automobil koji nije u voznom stanju stiže na odredište.<"),
    ("<h3>Autokauf &amp; Händler</h3>", "<h3>Car purchase &amp; dealers</h3>", "<h3>Acquisto auto &amp; concessionari</h3>", "<h3>Kupnja automobila &amp; prodavači</h3>"),
    (">Sie haben ein Auto gekauft? Ich hole es beim Verkäufer oder Händler ab und bringe es direkt zu Ihnen.<",
     ">Bought a car? I pick it up from the seller or dealer and bring it straight to you.<",
     ">Hai acquistato un'auto? La ritiro dal venditore o dal concessionario e te la porto direttamente.<",
     ">Kupili ste automobil? Preuzimam ga kod prodavača ili trgovca i dovozim ga izravno Vama.<"),
    ("<h3>Oldtimer &amp; Sportwagen</h3>", "<h3>Classic &amp; sports cars</h3>", "<h3>Auto d'epoca &amp; sportive</h3>", "<h3>Oldtajmeri &amp; sportski automobili</h3>"),
    (">Wertvolle Fahrzeuge transportiere ich besonders schonend und ohne zusätzliche Kilometer auf dem Tacho.<",
     ">I transport valuable vehicles with particular care and without adding any miles to the clock.<",
     ">Trasporto i veicoli di valore con particolare cura e senza chilometri aggiuntivi sul contachilometri.<",
     ">Vrijedna vozila prevozim posebno pažljivo i bez dodatnih kilometara na brojaču.<"),
    ("<h3>Schweiz &amp; Europa</h3>", "<h3>Switzerland &amp; Europe</h3>", "<h3>Svizzera &amp; Europa</h3>", "<h3>Švicarska &amp; Europa</h3>"),
    (">Transporte innerhalb der Schweiz und in ganz Europa, von der kurzen Strecke bis zur langen Reise.<",
     ">Transport within Switzerland and all over Europe, from short trips to long journeys.<",
     ">Trasporti all'interno della Svizzera e in tutta Europa, dal breve tragitto al lungo viaggio.<",
     ">Prijevozi unutar Švicarske i po cijeloj Europi, od kratkih relacija do dugih putovanja.<"),

    # Ablauf
    ('<p class="eyebrow">Ablauf</p>', '<p class="eyebrow">How it works</p>', '<p class="eyebrow">Come funziona</p>', '<p class="eyebrow">Postupak</p>'),
    ('<h2>In vier Schritten zum <span class="script">Transport</span></h2>',
     '<h2>Four steps to your <span class="script">transport</span></h2>',
     '<h2>In quattro passi al <span class="script">trasporto</span></h2>',
     '<h2>Četiri koraka do <span class="script">prijevoza</span></h2>'),
    ("<h3>Anfrage</h3>", "<h3>Request</h3>", "<h3>Richiesta</h3>", "<h3>Upit</h3>"),
    (">Sie schicken mir Abhol- und Zielort sowie die Angaben zu Ihrem Fahrzeug, per WhatsApp, Telefon oder E-Mail.<",
     ">You send me the pick-up and destination address and details of your vehicle by WhatsApp, phone or email.<",
     ">Mi invii luogo di ritiro e destinazione e i dati del tuo veicolo via WhatsApp, telefono o e-mail.<",
     ">Pošaljete mi mjesto preuzimanja i odredište te podatke o vozilu putem WhatsAppa, telefona ili e-maila.<"),
    ("<h3>Offerte</h3>", "<h3>Quote</h3>", "<h3>Preventivo</h3>", "<h3>Ponuda</h3>"),
    (">Sie erhalten von mir rasch eine verbindliche Offerte zum Fixpreis.<",
     ">You quickly receive a binding quote at a fixed price.<",
     ">Ricevi rapidamente un preventivo vincolante a prezzo fisso.<",
     ">Brzo dobivate obvezujuću ponudu po fiksnoj cijeni.<"),
    ("<h3>Abholung</h3>", "<h3>Pick-up</h3>", "<h3>Ritiro</h3>", "<h3>Preuzimanje</h3>"),
    (">Nach Zahlungseingang hole ich Ihr Fahrzeug zum vereinbarten Termin ab.<",
     ">Once payment is received, I pick up your vehicle at the agreed time.<",
     ">Dopo il ricevimento del pagamento ritiro il tuo veicolo alla data concordata.<",
     ">Nakon uplate preuzimam Vaše vozilo u dogovoreno vrijeme.<"),
    ("<h3>Übergabe</h3>", "<h3>Handover</h3>", "<h3>Consegna</h3>", "<h3>Predaja</h3>"),
    (">Ich liefere Ihr Fahrzeug sicher ab und übergebe es mit Übergabeprotokoll.<",
     ">I deliver your vehicle safely and hand it over with a handover report.<",
     ">Consegno il tuo veicolo in sicurezza con verbale di consegna.<",
     ">Sigurno isporučujem Vaše vozilo i predajem ga uz zapisnik o primopredaji.<"),

    # Galerie + CTA
    ('<p class="eyebrow">Galerie</p>', '<p class="eyebrow">Gallery</p>', '<p class="eyebrow">Galleria</p>', '<p class="eyebrow">Galerija</p>'),
    ('<h2>Einblicke in meine <span class="script">Transporte</span></h2>',
     '<h2>A look at my <span class="script">transports</span></h2>',
     '<h2>Uno sguardo ai miei <span class="script">trasporti</span></h2>',
     '<h2>Pogled na moje <span class="script">prijevoze</span></h2>'),
    ('<h2>Bereit für Ihren nächsten <span class="script">Transport?</span></h2>',
     '<h2>Ready for your next <span class="script">transport?</span></h2>',
     '<h2>Pronto per il prossimo <span class="script">trasporto?</span></h2>',
     '<h2>Spremni za sljedeći <span class="script">prijevoz?</span></h2>'),

    # Kontakt
    (">Grüezi! Schicken Sie mir Abholort, Zielort und Fahrzeug. Sie erhalten rasch eine unverbindliche Offerte.<",
     ">Hello! Send me the pick-up location, destination and vehicle. You will quickly receive a free, no-obligation quote.<",
     ">Buongiorno! Inviami luogo di ritiro, destinazione e veicolo. Riceverai rapidamente un preventivo senza impegno.<",
     ">Pozdrav! Pošaljite mi mjesto preuzimanja, odredište i vozilo. Brzo ćete dobiti neobvezujuću ponudu.<"),
    (">Ich bin 24 Stunden für Sie erreichbar.<", ">I am available for you 24 hours a day.<", ">Sono raggiungibile 24 ore su 24.<", ">Možete me kontaktirati 24 sata.<"),
    ('<p class="eyebrow">Direkt erreichbar</p>', '<p class="eyebrow">Direct contact</p>', '<p class="eyebrow">Contatto diretto</p>', '<p class="eyebrow">Izravan kontakt</p>'),
    ('<h2>Wählen Sie Ihren <span class="script">Kanal</span></h2>',
     '<h2>Choose your <span class="script">channel</span></h2>',
     '<h2>Scegli il tuo <span class="script">canale</span></h2>',
     '<h2>Odaberite svoj <span class="script">kanal</span></h2>'),
    (">Ein Klick verbindet Sie direkt mit mir.<", ">One click connects you directly with me.<", ">Un clic ti mette in contatto diretto con me.<", ">Jedan klik i izravno ste povezani sa mnom.<"),
    ("<span>Telefon <small>", "<span>Phone <small>", "<span>Telefono <small>", "<span>Telefon <small>"),
    ("<strong>Erreichbar</strong> 24 Stunden", "<strong>Available</strong> 24 hours", "<strong>Raggiungibile</strong> 24 ore su 24", "<strong>Dostupni</strong> 24 sata"),
    ("<strong>Standort</strong> Thurgau, Schweiz", "<strong>Location</strong> Thurgau, Switzerland", "<strong>Sede</strong> Turgovia, Svizzera", "<strong>Lokacija</strong> Thurgau, Švicarska"),

    # Footer
    (">Autotransport mit Anhänger und persönliche Überführung, in der Schweiz und in ganz Europa.<",
     ">Car transport by trailer and personal vehicle delivery, in Switzerland and all over Europe.<",
     ">Trasporto auto con rimorchio e trasferimento personale, in Svizzera e in tutta Europa.<",
     ">Prijevoz automobila prikolicom i osobni prijevoz vozila, u Švicarskoj i cijeloj Europi.<"),
    ("<span>Thurgau, Schweiz</span>", "<span>Thurgau, Switzerland</span>", "<span>Turgovia, Svizzera</span>", "<span>Thurgau, Švicarska</span>"),
    ("<h4>Navigation</h4>", "<h4>Navigation</h4>", "<h4>Navigazione</h4>", "<h4>Navigacija</h4>"),
    ("<span>E-Mail <small>", "<span>Email <small>", "<span>E-mail <small>", "<span>E-mail <small>"),
    ("<h4>Rechtliches</h4>", "<h4>Legal</h4>", "<h4>Note legali</h4>", "<h4>Pravne informacije</h4>"),
    ('>AGB<', '>Terms (German)<', '>CG (tedesco)<', '>Uvjeti poslovanja (njemački)<'),
    ('>Impressum<', '>Legal notice (German)<', '>Note legali (tedesco)<', '>Impresum (njemački)<'),
    ('>Datenschutz<', '>Privacy policy (German)<', '>Privacy (tedesco)<', '>Zaštita podataka (njemački)<'),
    ("Alle Rechte vorbehalten.", "All rights reserved.", "Tutti i diritti riservati.", "Sva prava pridržana."),
    # Allgemeine Wörter zuletzt (Navigation, Buttons)
    (">Startseite<", ">Home<", ">Home<", ">Početna<"),
    (">Ablauf<", ">How it works<", ">Come funziona<", ">Postupak<"),
    (">Galerie<", ">Gallery<", ">Galleria<", ">Galerija<"),
    (">Kontakt<", ">Contact<", ">Contatto<", ">Kontakt<"),
    (">Jetzt Offerte anfragen<", ">Request a quote now<", ">Richiedi un preventivo<", ">Zatražite ponudu odmah<"),
    (">Offerte anfragen<", ">Request a quote<", ">Richiedi preventivo<", ">Zatražite ponudu<"),

]


def build(lang, idx):
    html = SRC.read_text(encoding="utf-8")
    missing = []
    for row in TEXTS:
        de, tr = row[0], row[idx]
        if de not in html:
            missing.append(de)
            continue
        html = html.replace(de, tr)
    if missing:
        print(f"[{lang}] Nicht gefunden (Text in index.html geändert?):")
        for m in missing:
            print("   ", m[:90])

    cfg = LANGS[lang]
    html = html.replace('<html lang="de-CH">', f'<html lang="{cfg["html"]}">', 1)
    html = html.replace('content="de_CH"', f'content="{cfg["locale"]}"', 1)
    html = html.replace('<link rel="canonical" href="https://www.autotransport-europa.ch/">',
                        f'<link rel="canonical" href="https://www.autotransport-europa.ch/{lang}/">', 1)
    html = html.replace('<meta property="og:url" content="https://www.autotransport-europa.ch/">',
                        f'<meta property="og:url" content="https://www.autotransport-europa.ch/{lang}/">', 1)
    # Sprachwahl: aktive Sprache markieren
    html = html.replace(' aria-current="page">DE<', '>DE<')
    html = re.sub(rf'(<a href="/{lang}/" hreflang="{lang}" lang="{lang}")>', r'\1 aria-current="page">', html)
    # relative Pfade eine Ebene höher
    html = re.sub(r'(href|src)="(css|js|img|fonts)/', r'\1="../\2/', html)
    html = re.sub(r'href="(agb|impressum)\.html', r'href="../\1.html', html)

    # Slideshow-Zähler und Vorschaubilder
    html = re.sub(r'aria-label="(\d+) von (\d+)"', lambda m: f'aria-label="{m[1]} {cfg["of"]} {m[2]}"', html)
    html = re.sub(r'aria-label="Bild (\d+) anzeigen"', lambda m: f'aria-label="{cfg["show"].format(m[1])}"', html)

    left = [r[0] for r in TEXTS if r[0] in html and r[0] != r[idx]]
    if left:
        print(f"[{lang}] Noch deutsche Texte:", left)
    out = ROOT / lang / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return not missing


ok = all([build(lang, i + 1) for i, lang in enumerate(LANGS)])
sys.exit(0 if ok else 1)
