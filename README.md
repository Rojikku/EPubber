# EPubber
A basic script that uses the ebooklib library, and some others, to convert systematic webpages into epubs using jQuery selectors.

As of 0.1 release, the script is capable of taking a link to the table of contents- In my case, often to a fan-translation site- and using jQuery selectors to get a list of links.
Using the --mode flag, you can set it to index mode, and test the link selection.
Once you have a proper selection of links, with no extra ones, you can use the page flag to make sure you get the content from each chapter as desired, without much extra.

After you've finished your test runs- likely saving your jQuery strings in notepad, you can do an actual run, with no flags. The script will check a cache/database for the link provided, and pull settings from there if possible. This is a local file, unique to the user. If there is nothing in the cache, it will ask the user for the necessary settings, and book Title. It can then automatically download content, and output an epub file.
