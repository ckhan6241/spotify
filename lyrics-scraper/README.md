# Lyrics-scraper
A genius.com lyrics scraper script. Import function scrape or scrape_multi to scrape the lyrics. The lyrics of each song
will be stored in the output directory provided.  
  
Note:  
1. The lyrics will be stored in a txt file named [song name]_[artist name].txt, all lower cased plus removal of symbols '/'
and '\\'.
2. There are cases where the spotify song name is very deliberated (eg. "call on me - ryan riback extended remix" or 
"despacito (featuring daddy yankee)" ). Usually no results will be returned if this name is search on genius.com. So, the
scraper is designed to repeat the scraping process using a extracted shorter song name if it fails at the first try.

## Usage
### Scraping one song
```
...
scrape("Shape of you", "Ed Sheeran", "lyrics-data") # song name, artist name, output directory
...
```

### Scraping multiple data
```
...
top_100_songs # let say you have a pandas' dataframe of top 100 songs
scrape_multi(top_100_songs["name"], top_100_songs["artists"], "lyrics-data")
  # sequence of song name, sequence of artists name, output directory
...
```
