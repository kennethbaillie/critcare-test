---
title: Local guidelines access system
author: Kenneth Baillie
---

# Summary


This system is designed to make local guidelines easy to maintain and easily accessible through a web browser on a mobile phone or other personal device. It can be accessed at: [critcare.net](https://critcare.net).

```
username: crit
password: care
```

Uploading and maintaining the guidelines is very easy - all that the editors and administrators need to do is maintain a dropbox folder containing the guidelines in each category. The folder names and file names are automatically converted into menu links and uploaded every 2 hours. (You may need to refresh your browser, or use incognito mode, to see changes straight away).

Guidelines should not be emailed to Heather for update any longer. They are uploaded to dropbox by the responsible section editor, and picked up by Heather, who will copy them to the intranet weekly. Any changes you make are recorded on this [web page](https://critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/changes.html).

# Basic use

## Rules

- Each folder has *one* editor. If it is you, arrange the contents of the folder as you want the files to appear online. The master list of editors is in the dropbox and you can see the list (without email addresses) online [here](https://critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/criticalcare/editors/).
- Each guideline should appear only *once* in the dropbox. This is mitigate the chance of confusion/error
- You can add subfolders but don't go crazy
- Folder/Filenames will become the links - make them simple and comprehensible. Do not include version numbers, dates, and try to avoid redundant words such as "guideline" or "protocol" or "in critical care" unless they are useful to users.
- Each guideline should appear *only once* in this site. Put it where you'd expect to find it.

## Getting started

- The best way to do this is to install Dropbox on your own non-NHS computer or mobile phone. That way you can keep a local copy of all the documents in your folder, and make changes in seconds
- if you already use dropbox, get access using the same email address that you use for dropbox

## Adding files

1. Put your pdf files into the right directory. 
2. That's it.

## offline_DRAFTS folders

- you have an `offline_DRAFTS` folder in every dropbox folder that you edit
- use this to keep the editable (e.g. microsoft word) versions of every guideline that you are responsible for

# Advanced use

- any file with a name beginning with the word `offline` or an underscore `_` will be ignored by the app.
- label emergency protocols by adding `_em` will be duplicated in the `Emergencies` folder and highlighted in red.
- when you are ready to make a protocol public, add `_pub` to the end of the filename. e.g.:
	- `Emergency Caesarean Section Action Cards_em.pdf` is flagged for the emergency section
	- `C-spine clearance flowchart and guidance_pub.pdf` is public
	- `Air_Embolism_em_pub.pdf` is both public and flagged as an emergency protocol
	
## Automatic checks

The app produces some automatic checks, which aren't perfect, but can help keep the guidelines in good shape:

- a list of [duplicate files](https://critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/duplicates/)
- a list of [estimated review dates](https://critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/reviewdates/)

## Adding videos or links

You can add links to videos by copying the text files like this one: `COVID19/videos/COVID Intubation Simulation Video.txt`

These filenames must end in .txt

The file name becomes the menu item.

The contents of the file become the link target, so the only thing that should appear in the file is the plain text link, e.g.

https://youtu.be/HDyKJ4FOX9o


## Adding a web page

A couple of files in the app are simple web pages written in markdown. If you want to do this, simply end your filename in .md and it will be handled as markdown and made into a web page. If this doesn't make any sense to you, just ignore it.

## Automatic searching

You can trigger an automatic search directly from the URL by adding a query string to specify the `searchterm`. For example, to search for `deep vein thromobosis`, us this URL:
`https://critcare.net/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/?searchterm=deep%20vein%20thrombosis`











