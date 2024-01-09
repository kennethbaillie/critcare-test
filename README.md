# critcare.github.io
Critical Care Guidelines - for use by appropriately-trained staff only.

### Contributors
- Kenneth Baillie - mkdocs site, accordion html and search indexing script, dropbox download and parsing, automation on github, document comparison check, web app installation.

## Creating a new directory

- copy index.md into the home directory for your new site
- find out what the hashed directory name is for your chosen username/password combination by entering it in a browser. you'll get an error because the page doesn't exist
- copy the full contents of the guidelines_browser directory into a new directory with the hash as the name
- customise `index.md` within your new directory
- create an actions file to automatically update your new browser

### To change password
The directory name has to change in the following places:
- the actual dir itself, and within it:
	- index.md
	- img/favicon/site.webmanifest 
- .github/workflows/makelist.yml
- .github/workflows/record_changes.yml
- /docs/index.md
- themes/mods/base.html


## Website updates

These steps occur to update the website. They are specified in yml file in the github "actions" tab:
- update files from dropbox (download.py)
- makelist.py - this makes a directory tree into an html menu, and makes a search index for pdfs
- mkdocs - this runs mkdocs to create the live online branch

## Changes

The record_changes.yml procedure takes the contents of .changes.json and formats them in an html file
../changes.html

## TODO

- write and automate script to create status reports for each folder (i.e. editor):
	- percentage of protocols that are public
	- file size optimisation
	- automatically read update dates from pdfs
- improve search - maybe solr rather than lunr?














