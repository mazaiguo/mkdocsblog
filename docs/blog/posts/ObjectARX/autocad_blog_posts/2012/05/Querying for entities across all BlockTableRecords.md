---
title: "Querying for entities across all BlockTableRecords"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Block
  - C#
description: "In a comment to a previous post of mine, Viktor K asked:"
author: Autodesk
---
# Querying for entities across all BlockTableRecords

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/querying-for-entities-across-all-blocktablerecords.html

## 文章内容

By Stephen Preston
In a comment to a previous post of mine, Viktor K asked:
Is there a method in .net api to search for a text string in the entire file and return values from dbtext, mtext, attributes, cells, etc... Basically how "find" command searches. I would imagine that you'd get objectids back of all the entities found with that text string. Or even better a find/replace functionality?
Doing that isn’t particularly easy, because the text entity could be in any BlockTableRecord in the drawing. Whatever approach you use, it ultimately results in AutoCAD iterating through every entity in every BlockTableRecord in the BlockTable. This will always be a slow process, which is why the AutoCAD Content Explorer feature (for example) indexes drawings in the background for speedy searching.
Last night, I took Viktor’s question as an excuse to go back and play with some of my experimental LINQ samples that Kean posted on his blog. As a result, here is a simple C# routine that returns all the DBText, Mtext, and AttributeDefinitions in a drawing that contain a particular string. This is only a partial answer to Viktor’s question, but a nice start:
    [CommandMethod("FINDTEXT")]
    public void FindText()
    {
      Database db = Application.DocumentManager.MdiActiveDocument.Database;
      Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      dynamic bt = db.BlockTableId;
      string str = "ABC";
        var textEnts = from btrs in (IEnumerable<dynamic>)bt
                      from ent in (IEnumerable<dynamic>)btrs
                      where
                      ((ent.IsKindOf(typeof(DBText)) &&
                        (ent.TextString.Contains(str))) ||
                      (ent.IsKindOf(typeof(MText)) &&
                        (ent.Contents.Contains(str))))
                      select ent;
        foreach (ObjectId qEnt in textEnts)
      {
        ed.WriteMessage("\n" + qEnt.ToString());
      }
    }
And now I’ve shown you the code, here are some health warnings:
This code uses Dynamic .NET – new in AutoCAD 2013. Don’t waste your time trying it if you’re using an earlier AutoCAD version.
A significant omission is that the above LINQ query doesn’t return AttributeReferences, even though they are derived from DbText. That is because AttributeReferences are accessed through the BlockReference.AttributeCollection property.
I’m a LINQ newbie, so I make no claims that the above query is optimized in any way. I’d be very happy to receive comments with suggestions for improvements to make this post more complete.

## 评论

**内容**: Viktor K said...
Thanks Stephen, at least I know it won't be easy :)
I should be able to use LINQ in 2010-2012 anyway, so I'll give it a shot (although as you've mentioned this is still doing the same thing as iterating through in a loop) of course without the dynamic portion of it.
Thanks again for your answer.
Reply
05/09/2012 at 12:13 PM

---
**内容**: Rik De Peuter said...
Here is an extension method for Database, for those who could use it:
public static List GetAll(this Database db, Func predicate = null) where T : DBObject
{
using(var tr = db.TransactionManager.StartTransaction())
{
dynamic bt = db.BlockTableId;
var q = ((IEnumerable) bt).SelectMany(x => (IEnumerable) x)
.Select(x => tr.GetObject(x, OpenMode.ForRead)).OfType();
if (predicate != null)
{
q = q.Where(predicate);
}
return q.ToList();
}
}
Reply
03/26/2014 at 12:24 AM

---
