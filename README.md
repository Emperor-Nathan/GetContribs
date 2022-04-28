# GetContribs
This is a tool for tracking your Wiki editing statistics. It allows you to view your total contributions per wiki in edits, absolute bytes, or signed bytes.

To use this, you will need to modify the "userdata.txt" file as follows (see my personal example):
- Line 1: your username
- Line 2: start date/time (UTC) in ISO 8601 datetime format
- Line 3: end date/time (UTC) in ISO 8601 datetime format
- Line 4: list of language codes, separated by commas (spaces after commas required)
- Line 5: list of language-specific wikis, separated by commas (spaces after commas required)
- Line 6: list of non-language-specific wikis, separated by commas (spaces after commas required); also allows individual language wikis, e.g. "en.wikibooks"

Then run it on the command line. There is one argument, which represents how to count the number of contributions. It takes the following possible values:
- num: total number of edits
- abt: absolute number of bytes
- sbt: signed number of bytes