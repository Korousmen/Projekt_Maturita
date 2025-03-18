# Projekt_Maturita - Matyáš Korous
Tento repositář by měl sloužit pro uložení projektu který je potřebný k maturitě

DŮLEŽITÉ!!!!! 
  Ve všech python souborech se nachází připojení na databázi "dbs.spskladno.cz/myadmin/", údaje jsou v něm napojené na účet student8, na který je i možné se přihlásit, pokud ale chce databázi jinde například v postgreSQL, musíte si zjistit vaše připojovací parametry a potřebnou instalaci dalších python knihoven.
Návod k použití (zatím bez html stránky)
  Nejdřív je nutné spusit create.py aby se nám vytvořily tabulky v databázi. Vytvoří to tabulky uziv a uziv_type. Tabulka uziv nám bude dávat informace o uživately a uziv_type skladuje různé typy uživatelů.
  Následně se spustí main.py který nám ukáže krásnou tkinter aplikaci kde bude nutné se nejdřív zaregistrovat a následně přihlásit. Aplikace se kvůli nově založenému účtu nemusí restartovat.
  A následně hurá na hraní piškvorek, kde můžete sledovat svůj počet výher
