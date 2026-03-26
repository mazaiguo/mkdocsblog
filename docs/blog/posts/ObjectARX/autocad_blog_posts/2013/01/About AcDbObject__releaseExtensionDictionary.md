---
title: "About AcDbObject::releaseExtensionDictionary"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "What is the difference between calling erase() on the extension dictionary directly and calling releaseExtensionDictionary() on the owning object?"
author: Autodesk
---
# About AcDbObject::releaseExtensionDictionary

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/about-acdbobjectreleaseextensiondictionary.html

## 文章内容

By Augusto Goncalves
What is the difference between calling erase() on the extension dictionary directly and calling releaseExtensionDictionary() on the owning object?
This API was introduced to be able to completely remove an extension dictionary from an object. This member function enables clients to create a brand new extension dictionary in place of an empty extension dictionary within the same drawing session.
The fundamental difference between calling releaseExtensionDictionary() on the parent object and calling erase() on the extension dictionary is most obvious if you look at the return values of other two extensionDictionary manipulation functions extensionDictionary and createExtensionDictionary. Consider the following two call sequences:
(We are given a pointer pO initialized to point to a valid database resident object that is open for write with extension dictionary. We also have a valid pointer pED to the extension dictionary object open for write.)
1.
pO->releaseExtensionDictionary(); // returns Acad::eOk
pO->extensionDictionary(); // returns AcDbObjectId::kNull
pO->createExtensionDictionary(); // succeeds Acad::eOk
2.
pED->erase(); // succeeds with Acad::eOk
pO->extensionDictionary(); // returns a valid object id
pO->createExtensionDictionary(); // fails with eAlreadyInDatabase
In other words, calling erase() on the extension dictionary does not break the link between the object and the extension dictionary. You can access the dictionary at a later stage of you program and unerase it. Note that if you save the database the erased extension dictionary is not saved and the object will return AcDbObject::kNull from a call to extensionDictionary() in the saved database.
releaseExtensionDictionary not only erases the extension dictionary but also breaks the link between the object and the extension dictionary.

