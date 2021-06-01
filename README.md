# critcare.github.io
NHS Lothian Critical Care Guidelines

### Contributors
- Kenneth Baillie - mkdocs site, accordion html and search indexing script, dropbox download and parsing, automation on github, document comparison check, web app installation.

## Website updates

These steps occur to update the website. They are specified in yml file in the github "actions" tab:
- update files from dropbox
- makelist - this makes a directory tree into an html menu, and makes a search index for pdfs
- mkdocs - this runs mkdocs to create the live online branch

## To change password
The directory name has to change in the following places:
- the actual dir itself
- .github/workflows/makelist.yml
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