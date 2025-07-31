# matkailukokemukset

- ✓ Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- ✓ Käyttäjä pystyy lisäämään sovellukseen matkailukokemuksia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään matkailukokemuksia.
- ✓ Käyttäjä näkee sovellukseen lisätyt matkailukokemukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät matkailukokemukset.
- ✓ Käyttäjä pystyy etsimään matkailukokemuksia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä matkailukokemuksia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät matkailukokemukset.
- Käyttäjä pystyy valitsemaan matkailukokemuksille yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
- Sovelluksessa on pääasiallisen matkailukokemuksen lisäksi toissijainen tietokohde (esim kommentit), joka täydentää pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään toissijaisia (kommentteja) matkailukokemuksiin omiin ja muiden käyttäjien matkailukokemuksiin liittyen.

# Ohjelman testaaminen
Tämä ohjee koskee macOS/Linux käyttöjärjestelmiä.
- Kloonaa GitHub-repositorio --> "git clone https://github.com/hanskval/matkailukokemukset.git"
- Siirry ladattuun kansioon --> "cd matkailukokemukset"
- Luo Python virtuaaliympäristö --> "python3 -m venv venv"
- Aktvioi virtuaali ympäristö --> "source venv/bin/activate"
- Asenna tarvittavat Python kirjastot "pip install Flask"
- Luo tarvittava tietokanta schema.sql tiedoston avulla --> "sqlite3 database.db < schema.sql"
- Käynnistä flask --> "flask run"
- Jolloin nettisivut aukeavat terminaalin antamaan osoitteeseen.



