# Selenium + LXML unholy marriage
This is a general monitor crawler. It works as follows:

```
python poc_selenium_lxml.py file.txt webpage_url
```

where webpage_url is the address of the page needed to be crawled and file.txt is a file containing the XPath selectors for the data that interests us. The format of the data is as follows:

```
key,xpath
key2,xpath2,xpath3
```

The output of the monitor will be a json of the form:

```
{
    'key': ['info', 'possibly_more'],
    'key2': ['info2', 'info3', 'info4']
}
```

Attached are examples for three websites: cultpens, jetpens and miestilografica.
