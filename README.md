# Url-Scannner by Grzegorz Zygan
This project was created as a recruitment test.


## Description:
`
Develop a comprehensive Python script that automates the detection and analysis of phishing
websites using multiple data sources and detection engines.
`


## Technologies used:
`
Python, httpx, asyncio, playwright, lxml, html2text, click and pydantic.
`


## What does it do?
This tool basically integrates few mechanisms to detect potential threats related to Urls.

- Integration with VirusTotalApi, where I can request either a report for url or scan it.
- Integration with Google Safe Browsing Api - where I can check url against google base of malicious websites.
- Scraping Bot made with Playwright that looks for markers on requested webpage, 
that may indicate that a page has been blocked.
- Simple request check validation, that returns status code, content-type, server etc.


## Current state of development:
### Scanning:
`scan-single` and `scan-file` features are working.
Users can either scan a single url or collection of urls from the file.
Single scans are sent synchronously, while processing of urls from the file was implemented with asynchronous logic.

I also implemented a call to endpoint where you can request given Url to be scanned.
But right now single scan is returning data that VirusTotal actually has about url. 
#### Single scan important:
- `scan-single` is returning data that VirusTotal actually has for this url.
#### File scan important:
- `scan-file` is currently rate limited on Analyzer class to sent 4 request per 60 seconds.
Because I was using VirusTotal Free tier access.
- 

### Data sources:
`open-phish-file` and `cert-file` features are working.
Right now user can load urls from 2 data sources OpenPhish and Cert txt samples.

### Data assessment:
Depending on the type of scanning user will receive statistics about single url printed to stdout or .json report with all requested urls data.
And stdout statistics about liveness and percentage of positives per vendor etc..

### Integration:
Quick and simple CLI was created with `click` package.

### Todo:
Testing, Storing exceptions on Url object to track issues, Integration with database.


## How to use:
### Prepare your API Keys:
- Create a `.env` file according to schema of `.env-sample` file
- Provide API keys in `.env` file for VirusTotalApi and Google SafeBrowsing Api

### Install and use dependencies:
```commandline
python -m venv venv
```
&
```commandline
source venv/bin/activate
```

### Feed data from current sources:

- `OpenPhish sample:`
```commandline
python scanner.py open-phish-file
```
or
- `Cert.pl sample:`
```commandline
python scanner.py cert-file
```

### Run a full scan:
```commandline
python scanner.py scan-file <file_name>
```

### Run a single scan for url:
```commandline
python scanner.py scan-single <url>
```