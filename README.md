# matkailukokemukset

- ✓ Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- ✓ Käyttäjä pystyy lisäämään sovellukseen matkailukokemuksia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään matkailukokemuksia.
- ✓ Käyttäjä näkee sovellukseen lisätyt matkailukokemukset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät matkailukokemukset.
- ✓ Käyttäjä pystyy etsimään matkailukokemuksia hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä matkailukokemuksia.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät matkailukokemukset.
- Käyttäjä pystyy valitsemaan matkailukokemuksille yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
- Sovelluksessa on pääasiallisen matkailukokemuksen lisäksi toissijainen tietokohde (esim kommentit), joka täydentää pääasiallista tietokohdetta. Käyttäjä pystyy lisäämään toissijaisia (kommentteja) matkailukokemuksiin omiin ja muiden käyttäjien matkailukokemuksiin liittyen.

# Ohjelman testaaminen
- Kloonaa github lisäämällä terminaaliin --> "git clone https://github.com/hanskval/matkailukokemukset.git"
- Tämän jälkeen mene ladattuun kansioon --> "cd matkailukokemukset"
- Asennetaan virtuaali ympäristö missä voit ajaa ohjelmaa --> "python3 -m venv venv"
- Nyt sinulla on virtuaali ympäristö. aktivoi se --> "source venv/bin/activate" jonka jälkeen voit asentaa sinne vaadittavan python kirjaston "pip install Flask"
- schema.sql avulla voit luoda tarvittavan database.db tiedoston kirjoittamalla terminaaliin --> "sqlite3 database.db < schema.sql"
- Nyt voit ajaa koodin terminaaliin kirjoittamalla --> "flask run"


