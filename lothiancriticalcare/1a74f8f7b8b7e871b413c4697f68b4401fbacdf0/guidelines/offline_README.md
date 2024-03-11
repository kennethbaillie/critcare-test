---
title: Local guidelines access system
author: Kenneth Baillie
layout: page
---

# Summary


This system is designed to make local guidelines easy to maintain and easily accessible through a web browser on a mobile phone or other personal device. It can be accessed at: [critcare.net](https://critcare.net).

```
username: crit
password: care
```

The aim is to make uploading and maintaining guidelines very easy for busy clinicians. We use pdf guidelines because everyone can make them, and they always have a consistent appearance. To manage guidelines, all that the editors and administrators need to do is put files in a dropbox folder.

The folder names and file names are automatically converted into menu links and uploaded every 2 hours. (You may need to refresh your browser, or use incognito mode, to see changes straight away).

## NHS Lothian intranet

Guidelines should not be emailed to Heather for update any longer. They are uploaded to dropbox by the responsible section editor, and picked up by Heather, who will copy them to the intranet weekly. Heather finds any changes you make by looking at [this web page](https://critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/changes). If this system is followed, the guidelines on the intranet cannot get out of sync with the guidelines here. 

# Basic use

## Rules

- Each folder has *one* editor. If it is you, arrange the contents of the folder as you want the files to appear online. The master list of editors is in the dropbox and you can see the list (without email addresses) online [here](https://critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/editors).
- Folder/Filenames will become the links - make them simple and comprehensible. Do not include version numbers, dates, and try to avoid redundant words such as "guideline", "protocol", "final" or "in critical care" unless they are useful to users.
- Each guideline should appear *only once* in this site. Put it where you'd expect to find it. Duplicates aren't allowed because they can lead to two different versions of the same guideline, which is potentially dangerous. Check for duplicates using the [automatic duplicate detector](https://critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/duplicates)
- You can add subfolders but don't go crazy

## Getting started

- The best way to do this is to install Dropbox on your own non-NHS computer or mobile phone. That way you can keep a local copy of all the documents in your folder, and make changes in seconds
- if you already use dropbox, get access using the same email address that you use for dropbox

## Adding files

1. Put your pdf files into your folder.
2. That's it.

## offline_DRAFTS folders

You have an `offline_DRAFTS` folder in every dropbox folder that you edit. Use this to keep the editable (e.g. microsoft word) versions of every guideline that you are responsible for. That way, anyone who takes over your guidelines in future will be able to make changes easily.

# Governance and sustainability

Each editor is responsible for the content of their own directories. 

The back end program is hosted on github and automatically updates from a github "actions" script. It does not need routine maintentance but from time to time will require software updates. 

The code is available here `https://github.com/critcare/critcare.github.io` and can be edited by the following people who have access to the code: 

- Kenny Baillie
- Johnny Millar

Additional users can be added by any of these people and cost $44/year. In the worst case scenario if everyone was unavailable or incapacitated, the code is public so the site could be set up again by anyone with basic command line computing skills - anyone in Kenny's research lab could do this, for example. 

# Advanced use

## Special tags in filenames

- any file with a name beginning with the word `offline` or an underscore `_` will be ignored by the app.
- label emergency protocols by adding `_em` will be duplicated in the `Emergencies` folder and highlighted in red.
- when you are ready to make a protocol public, add `_pub` to the end of the filename. e.g.:
	- `Emergency Caesarean Section Action Cards_em.pdf` is flagged for the emergency section
	- `C-spine clearance flowchart and guidance_pub.pdf` is public
	- `Air_Embolism_em_pub.pdf` is both public and flagged as an emergency protocol

## Adding videos or links

You can add links to videos by copying the redirect files like this one: `COVID19/videos/COVID Intubation Simulation Video.md`. These filenames must end in .md and can be opened with any text editor, such as notepad or textedit. If they don't open when you double click them, right click and choose `Open with`, or google it.

The file name becomes the menu item. In the top of the file there is a special syntax called YAML that indicates that this file should redirect to another page, like this: 

```
---
redirect_to: https://youtu.be/o08B9es8JVE
---
```

## Adding a web page

A couple of files in the app are simple web pages written in markdown. If you want to do this, simply end your filename in .md and it will be handled as markdown and made into a web page. The site is compiled using jekyll, so you have to add some YAML at the top. This is enough: 

```
---
layout: page
---
```

If this doesn't make any sense to you, just ignore it.

## Automatic searching

You can trigger an automatic search directly from the URL by adding a query string to specify the `searchterm`. For example, to search for `deep vein thromobosis`, us this URL:

[critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/?searchterm=deep vein thrombosis](https://critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/?searchterm=deep vein thrombosis)

## Automatic redirecting

If you enter a slightly incorrect file link, or a link to an old file, the 404 error page will automatically redirect you to a search of the guidelines, as long as you have entered the right "stem" so that the guidelines aren't exposed on the open internet. Try it with this link: 

[critcare.net/lothiancriticalcare/ 1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/ guidelines/Airway/ Cook Staged Extubation Set Wrong Link.pdf](https://critcare.net/lothiancriticalcare/1a74f8f7b8b7e871b413c4697f68b4401fbacdf0/guidelines/Airway/Cook Staged Extubation Set Wrong Link.pdf)








