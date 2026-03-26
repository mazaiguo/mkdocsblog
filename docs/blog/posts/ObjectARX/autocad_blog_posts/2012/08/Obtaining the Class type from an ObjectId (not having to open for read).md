---
title: "Obtaining the Class type from an ObjectId (not having to open for read)"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - DWG
  - Database
description: "I’m sure you have all seen code like this before, where you open an entity in the DWG database to find out its type…"
author: Autodesk
---
# Obtaining the Class type from an ObjectId (not having to open for read)

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/obtaining-the-class-type-from-an-objectid-not-having-to-open-for-read.html

## 文章内容

by Fenton Webb
I’m sure you have all seen code like this before, where you open an entity in the DWG database to find out its type…
Database db =
Application.DocumentManager.MdiActiveDocument.Database;
using (Transaction trans = db.TransactionManager.StartTransaction())
{
  // open the entities
  Entity ent1 = (Entity)trans.GetObject(id1, OpenMode.ForRead);
  Entity ent2 = (Entity)trans.GetObject(id2, OpenMode.ForRead);
  // find their type
  Type entType1 = ent1.GetType();
  Type entType2 = ent2.GetType();
  // the two entities should be the same type
  if (!entType1.Equals(entType2))
    return;
  // …
There’s a much more efficient way to obtain the class name/entity type… That’s using ObjectId.ObjectClass property.
Using this property saves you opening an object for read, thus saving valuable CPU cycles.
e.g.
// the two entities should be the same type
if (id1.ObjectClass.Name != id2.ObjectClass.Name))
  return;
Database db =
Application.DocumentManager.MdiActiveDocument.Database;
using (Transaction trans = db.TransactionManager.StartTransaction())
{
// open the entities
Entity ent1 = (Entity)trans.GetObject(id1, OpenMode.ForRead);
Entity ent2 = (Entity)trans.GetObject(id2, OpenMode.ForRead);
// …

## 评论

**内容**: Craig said...
Hi Fenton,
A useful pointer. I was hoping to do this:
if (myObjId.ObjectClass.Name == typeof(BlockReference).Name)
//Do some stuff
but ObjectClass.Name is "AcDbBlockReference", not "BlockReference". Any way I can do this without using literal strings?
Reply
04/24/2013 at 03:58 AM

---
**内容**: Fenton Webb said...
Hey Craig!
the problem with being efficient is that it usually exposes you to the lower level parts of the API. The .NET API wraps the ObjectARX API, and that low level exposure is bringing up ObjectARX class names such as AcDbBlockReference.
You can use the RXClass object to extract the ObjectARX class name of a .NET equivalent so that you bypass this problem - e.g. something like:
RXClass blockRefRX = RXClass.GetClass(typeof(BlockReference));
Reply
04/24/2013 at 09:07 AM

---
**内容**: Craig said...
Thanks Fenton
I went for this :
if (objId.ObjectClass.Name == RXClass.GetClass(typeof(BlockReference)).Name)
Reply
04/26/2013 at 04:21 AM

---
