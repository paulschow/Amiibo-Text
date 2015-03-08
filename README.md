# Amiibo-Text
Program to search Amazon.com for new Amiibo product and send a text/email when it is released.
This program only looks for a certain Amiibo, in this case Ness.

Use something like this is cron to make it run every minute:

```
* * * * * cd /home/paul/Amiibo-Text && /home/paul/Amiibo-Text/AmiiboText.py
```

See original project for more information:
https://github.com/ansario/Amiibo-Search
