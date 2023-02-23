# fking-spaghetti
**A fking bulk image downloader**

A small UI to bulk download thumbnail images from `gettyimages.com` by search term. This is for educational purposes only 
and should not be used in commercial products.

This project was original based on [saftle's repo](https://github.com/saftle/getty_images_thumbnail_scraper).
Thanks for the ideas, and the back and forth concepts.

See the [pretty UI here](#ui-example).

## How to use
Clone git repo and run main.
```commandline
py main.py
```

For search term lists, each term should be on its own line, maybe don't use special characters...
```text
tiger
lion
bear
shark
palm trees
```

## Status
Well, it's been rewritten, I hope the pythonic gods can forgive me for what I've done. 
Please open issues for any bug you may find, and check back often.

### Custom Scraping Source
Want to scrape your own location? Implement `fking.scrapers.IScraper` yourself, and you could (*potentially*) scrape
from anywhere.

### Feature Ideas

- Automatically crop on subject
- Automatically resize crops to standard SD sizes, i.e, `512x512` and `768x768`
- Write search term list directly from within UI
- Network/proxy manager from within the UI
- Preferences for number of search pages, number of threads

## Hidden Features
**(For those that don't read the code)**

Putting a file called `proxies.txt` next to the `main.py` file, you can instruct the scraper to use
proxies for each call, rotating through each. Automatically blacklisting ones that do not work with a cooldown.
Each proxy should be on its own like, with the port number appended to it.

```text
123.123.213.123:8080
13.123.213.124:8080
19.123.223.125:8080
```

## UI Example
A few examples of the UI on Windows 11.

**Idle**

![A preview image of the UI](/.github/ui-1.png)


**GettyImages Source**

![A preview image of the UI busy](/.github/ui-2.png)