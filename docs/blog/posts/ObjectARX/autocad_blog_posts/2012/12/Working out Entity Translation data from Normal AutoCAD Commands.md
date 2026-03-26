---
title: "Working out Entity Translation data from Normal AutoCAD Commands"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "How do I get the arguments to the AutoCAD-commands COPY, MOVE, MIRROR, and so on, via ObjectARX. With an editor-reactor we have been able to contro..."
author: Autodesk
---
# Working out Entity Translation data from Normal AutoCAD Commands

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/working-out-entity-translation-data-from-normal-autocad-commands.html

## 文章内容

by Fenton Webb
Issue
How do I get the arguments to the AutoCAD-commands COPY, MOVE, MIRROR, and so on, via ObjectARX. With an editor-reactor we have been able to control the events "commandWillStart" and "commandEnded", but how can I get the translation-vector of the MOVE- or COPY-command at the "commandEnded"-event?
Solution
If your own custom entities are being translated, you will receive the
transformation matrix in their overloaded transformBy().
If they are not your entities, you can use one of these three methods:
Method #1
Attach an object reactor - either transient or persistent - to all of the
entities in the drawing.
Method #2
Use a database reactor to find out when an entity is opened for modify, and when
the modifications have actually been performed.
Method #3
Check the extended entity-data that is attached to the entities in order to see
how they have been transformed.
The first method is laborious, and is functionally equivalent to the second.
The second method is much cleaner. You could initially set a flag in your
COPY/MOVE commandWillStart method, indicating that a command you want to react to is current.
You should overload the following virtual functions in your database reactor:

virtual void AcDbDatabaseReactor::objectOpenedForModify ( const AcDbDatabase*
dwg, const AcDbObject* dbObj )
virtual void AcDbDatabaseReactor::objectModified ( const AcDbDatabase* dwg,
const AcDbObject* dbObj )
In the objectOpenedForModify() you would check whether a COPY or MOVE is active, by testing the flag I mentioned and also whether the entity being modified is one you want. Then, you would query its location and cache this in memory. On the second notification, objectModified, you would check its location, and from here you can calculate the translation.
In the case of a COPY, you will get an objectModified() notification when the
copy is initially appended to the database (with the original's position) and
then receive objectOpenedForModify() (again with the original position) and a
further objectModified() with the new position.
With the third method, you would attach XData to the entities you want to watch as certain XData point codes get transformed along with the parent entity.
e.g.
- a world space position (group code 1011) for simple translations.
- up to three world directions (group code 1013) for more complex
transformations. The world directions should correspond to the three axes, and
allow you to find more detailed information about the exact transformation.
Then on the commandEnded() notification you would check to see how this data has
been transformed. This approach is complimentary to the second: you can use the
database reactor to find the entities being modified and then query their XData
to discover the precise changes.

