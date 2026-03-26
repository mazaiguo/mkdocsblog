---
title: "Quick way to find number of entities in modelspace"
date: 2014-12-01
categories:
  - AutoCAD
tags:
  - Block
  - Database
description: "LINQ provides an easy way to find the number of entities in modelspace without having to iterate on our own. The IEnumerator exposed by BlockTableR..."
author: Autodesk
---
# Quick way to find number of entities in modelspace

发布日期: 2014-12-01

原始链接: https://adndevblog.typepad.com/autocad/2014/12/quick-way-to-find-number-of-entities-in-modelspace.html

## 文章内容

By Balaji Ramamoorthy
LINQ provides an easy way to find the number of entities in modelspace without having to iterate on our own. The IEnumerator exposed by BlockTableRecord can be cast as IEnumerable<ObjectId> to find the count. Here is a code snippet :
 using  System.Linq;
   Document doc 
  = Application.DocumentManager.MdiActiveDocument;
 Database db = doc.Database;
   using  (Transaction tr 
  = db.TransactionManager.StartTransaction())
 {
     BlockTable bt = tr.GetObject(
    db.BlockTableId, 
    OpenMode.ForRead) as BlockTable;
       ObjectId modelSpaceId 
   = SymbolUtilityServices.GetBlockModelSpaceId(db);
       BlockTableRecord btr = tr.GetObject(
    modelSpaceId, 
    OpenMode.ForRead) as BlockTableRecord;
       System.Collections.Generic.IEnumerable<ObjectId> 
   idCollection = btr.Cast<ObjectId>();
       doc.Editor.WriteMessage(
   String.Format("{0} Model space count : {1}" , 
   Environment.NewLine, idCollection.Count<ObjectId>()));
       tr.Commit();
 }

## 评论

**内容**: Ric said...
I tried to adapt this for counting lines, or circle and so on.
but using
idCollection = btr.Cast();
idCollection.Count();
resulted in an error
thank you
Reply
01/06/2015 at 06:14 AM

---
**内容**: Ric said...
edit:
but using
idCollection = btr.Cast;
idCollection.Count();
resulted in an error
thank you
Reply
01/06/2015 at 06:16 AM

---
**内容**: Ric said...
can't show "less then" and "greater then" symbols
after "Cast" and "Count", please imagine there's "Line" within those two symbols
Reply
01/06/2015 at 06:20 AM

---
**内容**: Balaji said...
With this code, you can only cast it as a collection of ObjectId, because that is the one the block table record enumerator lets you iterate.
You can try using Editor.SelectAll with appropriate filter to identify the number of lines or circles.
Regards,
Balaji
Reply
01/07/2015 at 02:47 AM

---
**内容**: steeloncall said...
Steeloncall offering a wide range of steel materials online with the best prices in India. https://steeloncall.com/ms-unequal-angles https://steeloncall.com/brands/jsw-neo https://steeloncall.com/brands/KAY2
Reply
05/10/2020 at 11:21 PM

---
