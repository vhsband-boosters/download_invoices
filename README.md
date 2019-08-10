# VHSBand invoice downloader

This script downloads invoice Google Sheets as PDFs in Landscape for bulk printing.

This script uses `pipenv` so you'll need that installed. It's written and tested using Python 3.7.4 and should work with basically any version of Python 3.7.x

### GCP credentials.json file

You'll need a `credentials.json` file for running this. Go to the [Google Cloud Platform Console](https://console.cloud.google.com), login using admin credentials for vhsband.com, select `ggbackup` as the project and then click on *Left Nav -> API & Services -> Credentials*
download the credential for `Invoice-Downloads` and save the file as `credentials.json`

## Running

Once you've pulled the source down, the first thing to do is setup a pipenv enviroment. Do this by doing `pipenv install`. [Full documentation for pipenv](https://docs.pipenv.org/en/latest/)

Once all dependent packages are installed, edit `invoices.py` and make sure the following line references the correct folderId for the Google Drive folder containing invoices:

```
INVOICES_FOLDER_ID = '<google drive folderId'
```

To run, execute `python invoices.py`. The first time you run this, it will print a URL to complete the OAuth2 authentication process. Paste this URL into a browser, login using your vhsband.com credentials, accept the permissions that the program is requesting and you'll get back a token. Copy this token and paste it back into the program run and the program will proceed to download invoices into the `invoices` sub-directory of the code.

## Splitting out By page

On Mac, an Automator script (in the `automator` sub-directory) may be used to separate all downloaded invoices by page. We only care about printing page 1 of each invoice as all of the rest are superfluous lookup data that does NOT need to be printed.