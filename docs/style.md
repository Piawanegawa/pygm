# Code Style für das Projekt pygm

* Modernes Python 3.11+, src/‑Layout, installierbares Package.
* Halte dich grob an PEP8, snake_case für Funktionen/Variablen,  
CamelCase für Klassen
* maximale Zeilenlänge 100.
* Jede Funktion/Klasse bekommt einen knappen Docstring  
(1–3 Zeilen, was sie tut). Funktionen bekommen im Docstring  
zusätzlich noch params und return.
* Alle Funktionen mit Typannotationen für Parameter und Rückgabe.
* Lieber mehrere kleine, gut benannte Funktionen als eine große  
mit tiefer Verschachtelung (max. ca. 3 Ebenen).
* Idealerweise maximal 20 Zeilen pro Funktion.
* Zu jedem nicht‑trivialen Feature: pytest‑Tests in tests/, keine  
Logik, die sich nur interaktiv/manuell testen lässt.
* Modularisierung: Jede Datei/Modul hat eine klar umrissene Aufgabe.
* Vermeide globale Variablen und Seiteneffekte.
* Fehlerbehandlung: Nutze Ausnahmen, keine stummen Fehler.
* Logging statt print() für Statusmeldungen.
* Schreibe Code so, dass er leicht testbar ist.