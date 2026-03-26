---
title: "Why doesn’t an App’s PackageContents.xml have a schema?"
date: 2012-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Plugin
description: "A few people have asked my why we did not post a schema for the PackageContents.xml. We specifically do not have a schema because:"
author: Autodesk
---
# Why doesn’t an App’s PackageContents.xml have a schema?

发布日期: 2012-11-01

原始链接: https://adndevblog.typepad.com/autocad/2012/11/why-doesnt-an-apps-packagecontentsxml-have-a-schema.html

## 文章内容

by Fenton Webb
A few people have asked my why we did not post a schema for the PackageContents.xml. We specifically do not have a schema because:
1) We wanted to make a very general design for describing the way components are loaded into a host application, as you know each host application (Revit/AutoCAD/Inventor/Maya/etc etc) are different from each other in their plugin requirements, so we wanted to make sure that the XML could be easily adjusted to suit different needs as each host platform adopted the Exchange store.
2) The PackageContents.xml is meant to be extensible, for example, it can be used to store developer specific application settings.
3) The PackageContents.xml is currently used to load apps into host applications, like AutoCAD, but also in Autodesk to automate building installers and also by the AppManager. We see the XML file being used by 3rd party developers for their own needs too.
Finally, to be clear, each attribute definition inside of the PackageContents.xml must start with an upper-case letter and finish all in lower-case… e.g.
Url='””
not
URL=””

## 评论

**内容**: Maxence said...
Ok, but when the loading fail, please display an explicit error message, not a cryptic (and undocumented) error code. I've lost several hours in order to find why my bundle was not loaded by AutoCAD. If it was one of my guys (in fact, I've got only one) who wrote this kind of thing, I will have fired him :-P
Reply
11/29/2012 at 12:46 PM

---
**内容**: Fenton Webb said...
Hey Maxence!
ah, personally I think the error code guy should have been promoted actually :-)
The idea is to give you guys a tool which builds your app installers for you, but we haven't finished it yet, so that's why something's are not finalized...
Best thing next time is to just ask... The codes are bitwise as follows:
ERR_SETENV 1
ERR_COMMAND_REG 2
ERR_WRITE_REG 4
ERR_GROUPNAME_REG 8
ERR_LOAD_FAILED 16
ERR_NO_APPNAME 32
ERR_WRONG_SCHEMA_VERSION 64
Reply
11/29/2012 at 02:40 PM

---
**内容**: Kerry Brown said...
Fenton,
>> Best thing next time is to just ask... The codes are >>bitwise as follows:
I may eventually get tired of saying this :
This stuff should be documented ... If you can post it in a blog you can add it to the docs .. and not waste our time or yours either.
Regards
Kerry
Reply
11/29/2012 at 03:44 PM

---
**内容**: JeffH said in reply to Kerry Brown...
My problem is I can not find good fundamental documentation to know what I need to ask or if I am asking the right question.
Reply
11/29/2012 at 04:18 PM

---
**内容**: Fenton Webb said...
Hey Kerry!
it is, now... ;-)
Reply
11/29/2012 at 04:20 PM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
>A few people have asked...
It's me...
For me it is unconvincing arguments. Before starting writing a code, it is necessary to think over in advance architecture, instead of to change it in process.
Absence of detailed documentation (without errors) does almost impossible creation of GUI of application for operation with PackageContents.xml.
Reply
12/01/2012 at 12:58 AM

---
