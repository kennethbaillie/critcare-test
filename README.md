# critcare.github.io
Critical Care Guidelines - for use by appropriatel-trained staff only.

### Contributors
- Kenneth Baillie - mkdocs site, accordion html and search indexing script, dropbox download and parsing, automation on github, document comparison check, web app installation.

## Website updates

These steps occur to update the website. They are specified in yml file in the github "actions" tab:
- update files from dropbox
- makelist - this makes a directory tree into an html menu, and makes a search index for pdfs
- mkdocs - this runs mkdocs to create the live online branch

## Changes

The record_changes.yml procedure takes the contents of .changes.json and formats them in an html file
../changes.html

## To change password
The directory name has to change in the following places:
- the actual dir itself
- .github/workflows/makelist.yml
- .github/workflows/record_changes.yml
- /docs/index.md
- /themes/mods/base.html

## TODO

- write and automate script to create status reports for each folder (i.e. editor):
	- percentage of protocols that are public
	- file size optimisation
	- automatically read update dates from pdfs
- improve search - maybe solr rather than lunr?
- make downloadable using PWA & Service Worker
- tidy up css on home screen to make it easier to enter on mobile

