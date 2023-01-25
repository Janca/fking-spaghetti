# fking-spaghetti
**A fking bulk image downloader**

A small UI to bulk download images from a site similar to `spaghettiimages.com`. This is for educational purposes only 
and should not be used in commercial products.

This project was original based on [saftle's repo](https://github.com/saftle/getty_images_thumbnail_scraper).
Thanks for the ideas, and the back and forth concepts.

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
Well, it works... there are some bugs for sure. Need to go through it once more. Pretty sure it cannot
be stopped currently, and exiting the UI while it is busy is sure the keep the process running.
All that being said, it will work.

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

## Example
![A preview image of the UI](/.github/ui-1.png)