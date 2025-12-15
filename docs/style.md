# Code Style für das Projekt pygm

* Modernes Python 3.11+, src/‑Layout, installierbares Package.
* Halte dich grob an PEP8, snake_case für Funktionen/Variablen,  
CamelCase für Klassen
* maximale Zeilenlänge 100.
* Jede Funktion/Klasse bekommt einen knappen Docstring  
(1–3 Zeilen, was sie tut). Funktionen bekommen im Docstring  
zusätzlich noch params und return.
* Docstrings immer auf Englisch.
* Docstrings immer mit dreifachen Anführungszeichen in extra  
Zeilen am Anfang und am Ende.
* Alle Funktionen mit Typannotationen für Parameter und Rückgabe.
* Falls eine Methode keinen Rückgabewert hat, benutze "-> None".
* Auch Membervariablen, Klassenvariablen und globale Variablen haben Typannotationen.
* Lieber mehrere kleine, gut benannte Funktionen als eine große  
mit tiefer Verschachtelung (max. ca. 3 Ebenen).
* Idealerweise maximal 20 Zeilen pro Funktion.
* Zu jedem nicht‑trivialen Feature: pytest‑Tests in tests/, keine  
Logik, die sich nur interaktiv/manuell testen lässt.
* Modularisierung: Jede Datei/Modul hat eine klar umrissene Aufgabe.
* Vermeide globale Variablen und Seiteneffekte.
* Fehlerbehandlung: Nutze Ausnahmen, keine stummen Fehler.
* Logging (mit dem Modul logging) statt print() für Statusmeldungen.
* Schreibe Code so, dass er leicht testbar ist.
* Sortiere Methoden in Klassen nach Sichtbarkeit: public, protected, private.
* Nutze f-Strings für String-Formatierung.
* Vermeide frühe Rückgaben.
* Nutze List Comprehensions und Generator Expressions, wo sinnvoll.
* Nutze Kontextmanager (with) für Ressourcenmanagement.
* Halte dich an das Prinzip der geringsten Überraschung: Code sollte  
leicht verständlich sein.
* Vermeide "Code Smells" wie lange Methoden, große Klassen,  
zu viele Parameter, duplizierten Code.
* Nutze pydantic für Datenklassen.
* Benutze absolute Importe statt relative.
