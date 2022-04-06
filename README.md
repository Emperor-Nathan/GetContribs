# GetContribs
This is a tool for tracking your Wiki editing statistics. It allows you to view your total contributions per wiki in edits, absolute bytes, or signed bytes.

To use this, you will need to modify the "userdata.txt" file as follows (see my personal example):
- Line 1: your username
- Line 2: start date/time in ISO 8601 datetime format
- Line 3: end date/time in ISO 8601 datetime format
- Line 4: list of language codes, separated by commas (spaces after commas required)
- Line 5: list of language-specific wikis, separated by commas (spaces after commas required)
- Line 6: list of non-language-specific wikis, separated by commas (spaces after commas required)

Then run it on the command line. There is one argument, which represents how to count the number of contributions. It takes the following possible values:
- num: total number of edits
- abt: absolute number of bytes
- sbt: signed number of bytes

Unfortunately, due to Wiki's CSS interface, the program has to scrape the date as a string, with differences in date formatting and the month names, for each language. All of the date formats and month names are contained in the "dates.csv" file. I will try to ensure that it is as complete as possible, but if there is a language that isn't in the file that you want to use, then you will have to add it yourself. If you know of a workaround for this, please tell me; I will greatly appreciate your help.

Bugs:
- Does not work for languages that use non-Western Arabic numeral systems.