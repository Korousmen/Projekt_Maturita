# Projekt_Maturita - Matyáš Korous
Tento repositář by měl sloužit pro uložení projektu který je potřebný k maturitě

DŮLEŽITÉ!!!!! 
  Ve všech python souborech se nachází připojení na databázi "dbs.spskladno.cz/myadmin/", údaje jsou v něm napojené na účet student8, na který je i možné se přihlásit, pokud ale chce databázi jinde například v postgreSQL, musíte si zjistit vaše připojovací parametry a potřebnou instalaci dalších python knihoven.
  Admin není v aplikacích nijak předem nastaven a musí se určit SQL kodem přes databázi. Koho si určíte adminem je na vás. Uživatel který je admin má user_type_id = 1

Návod k použití 
  Nejdřív je nutné spusit create.py aby se nám vytvořily tabulky v databázi. Vytvoří to tabulky uziv a uziv_type. Tabulka uziv nám bude dávat informace o uživately a uziv_type skladuje různé typy uživatelů.
  Následně spustit main.py který nám ukáže krásnou tkinter aplikaci kde je možnost přihlášení a registrace. Aplikace se kvůli nově založenému účtu nemusí restartovat.
  A následně hurá na hraní piškvorek, kde můžete sledovat svůj počet výher

  Webová aplikace funguje jako každá jiná.
  Registrace a přihlášení, po přihlášení se může uživatel kochat jaké výsledky mají ostatní uživatelé. Když se přihlásí uživatel s user_type_id = 1 (tedy admin), může uživatelům měnit jména nebo je smazat.
