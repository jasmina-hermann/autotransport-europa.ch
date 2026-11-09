<?php
// Kontaktformular für Hostpoint (PHP mail() funktioniert dort ohne Zusatzkonfiguration).
// [PLATZHALTER] Empfänger-Adresse anpassen:
$empfaenger = 'info@autotransport-europa.ch';
$absender   = 'website@autotransport-europa.ch'; // muss eine Adresse Ihrer Domain sein

header('Content-Type: application/json; charset=utf-8');

function antwort($ok, $msg) { echo json_encode(['ok' => $ok, 'message' => $msg]); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); antwort(false, 'Ungültige Anfrage.'); }
if (!empty($_POST['website'])) { antwort(true, 'Vielen Dank für Ihre Anfrage!'); } // Spam-Honeypot

$f = fn($k) => trim(str_replace(["\r", "\n"], ' ', strip_tags($_POST[$k] ?? '')));
$name = $f('name'); $email = $f('email'); $von = $f('von'); $nach = $f('nach');

if ($name === '' || $von === '' || $nach === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || empty($_POST['datenschutz'])) {
  http_response_code(422);
  antwort(false, 'Bitte füllen Sie alle Pflichtfelder (*) korrekt aus.');
}

$text  = "Neue Offertanfrage über autotransport-europa.ch\n\n";
$text .= "Name: $name\nE-Mail: $email\nTelefon: " . $f('telefon') . "\n";
$text .= "Transportart: " . $f('art') . "\nAbholort: $von\nZielort: $nach\nFahrzeug: " . $f('fahrzeug') . "\nWunschtermin: " . $f('termin') . "\n\n";
$text .= "Nachricht:\n" . trim(strip_tags($_POST['nachricht'] ?? '')) . "\n";

$headers  = "From: Autotransport-Europa Website <$absender>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$betreff = '=?UTF-8?B?' . base64_encode("Offertanfrage: $von → $nach") . '?=';

if (mail($empfaenger, $betreff, $text, $headers, "-f$absender")) {
  antwort(true, 'Vielen Dank! Wir melden uns so schnell wie möglich bei Ihnen.');
}
http_response_code(500);
antwort(false, 'Senden fehlgeschlagen. Bitte kontaktieren Sie uns telefonisch oder per E-Mail.');
