# critcare.github.io
NHS Lothian Critical Care Guidelines

### Contributors
- Kenneth Baillie - mkdocs site, accordion html and search indexing script, dropbox download and parsing, automation on github.

## Website updates

These steps occur to update the website. They are specified in yml file in the github "actions" tab:
- update files from dropbox
- makelist - this makes a directory tree into an html menu, and makes a search index for pdfs
- mkdocs - this runs mkdocs to create the live online branch

## To change password
The directory name has to change in the following places:
- .github/workflows/makelist.yml
- the actual dir itself
- the index file

## TODO

- write and automate script to create status reports for each folder (i.e. editor):
	- percentage of protocols that are public
	- file size optimisation
	- automatically read update dates from pdfs
- improve search - maybe solr rather than lunr?
- add "add to home screen" button
- make downloadable
- tidy up css on home screen to make it easier to enter on mobile
- speed up file copying by checking for identical files/more recently updated files and avoiding copying them
- speed up search indexing by storing extracted data from pdfs somewhere and only updating if file is changed/added/deleted
