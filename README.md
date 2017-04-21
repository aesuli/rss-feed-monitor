# Monitor and downloader of RSS feeds

feed_monitor.py is a script to monitor a set of RSS feeds and download the HTML pages they link.
The main loop of the script consists of loading the list of feeds to be monitored from a CSV file - more on format below - and then proceeding to read the feeds and downloading any HTML page linked in them that has not been already downloaded.
Multiple download of the same linked page is avoided by SHA hashing.
After all items have been downloaded the scripts goes on stand by for a predefined time, and then repeats the loop.
Every time the script loops it re-reads the CSV file, thus any modification to that file is effective without the need to stop and restart the script.

## CSV format

A row in the CSV file specifies a feed to be monitored, using the format:
```
"url of the rss feed","name of the feed","label 1","label 2","label 3",...
```
- The first column is the URL of the RSS feed.
- The second column is a name that identifies the source of the feed.
- Any successive column - at least one is required - assigns a label to the feed.

Any page downloaded from a feed will be saved in the path determined by the name and each of the labels.

For examples, given the row:
```
https://sports.yahoo.com/mlb/rss.xml,"yahoo","MLB","sports"
```
any downloaded page will be saved under the directories yahoo/MLB and yahoo/sports.

The idea is that more than one feed can contribute to a label, e.g.:
```
https://sports.yahoo.com/nba/rss.xml,"yahoo","NBA","sports"
```
will also contribute its pages to yahoo/sports (and save to the more specific label yahoo/NBA).

The whole HTML of downloaded pages is saved together with a JSON record of the original RSS item.
File names are determined by hashing the URL of the page.


## Extracting text from the HTML page

The feed_extractor.py script is a simple script that uses a few hand-made rules to isolate the relevant text of the page from the rest of the content (menus, ads, links, headers and footers).
The default heuristic is to keep all text that is visible, not part of a link, and that is long at least 25 characters.
A regex can be specified to further clean the text.
This is however just an example on how to extract text, each feed may need a dedicated processing to get a nice output.

## DISCLAIMER

The content you download from a feed will be likely covered by copyright and/or other IP rights, please check with the source of the feed what you can do with the content you download.