Example Scrapers in Python
=============

These are three fairly simple scrapers.

The first is `chess_scraper.py` which scrapes pgn data from the front page articles of ChessBase.com.

The next, `chess_scraper_with_cache.py`, does the same thing but uses `simple_cache.py` for a noticable speed improvement.

Finally, `classes_scraper.py` is a more practical scraper which uses selenium to accesss the Monmouth University class registry.

Installing
---------

You can install selenium and BeautifulSoup manually, or if necessary run `setup_local.py` 
which will download and build the necessary libraries locally.
