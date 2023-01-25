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
Well, it works... there are some bugs for sure. A major rewrite is in the near future, but I like to get the idea working,
and then fix... maybe. Please open issues for any bug you may find, and check back often.

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


**Busy**

![A preview image of the UI busy](/.github/ui-2.png)