# critcare.github.io
NHS Lothian Critical Care Guidelines


## Website updates

These steps occur to update the website. They are specified in yml files in the github "actions" tab:
- update files from dropbox [this bit not coded yet]
- makelist - this makes a directory tree into an html menu, and makes a search index for pdfs
- mkdocs - this runs mkdocs to create the live online branch

## TODO

- improve search - maybe solr rather than lunr?


## To change password
The directory name has to change in the following places:
- .github/workflows/makelist.yml
- the actual dir itself
- the index file

