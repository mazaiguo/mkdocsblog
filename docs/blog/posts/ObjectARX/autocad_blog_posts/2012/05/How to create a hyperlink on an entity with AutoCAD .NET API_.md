---
title: "How to create a hyperlink on an entity with AutoCAD .NET API?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
description: "Entities in AutoCAD can be associated with hyperlinks. Users can visit the referenced locations from the hyperlink on an entity. There are three ty..."
author: Autodesk
---
# How to create a hyperlink on an entity with AutoCAD .NET API?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-create-a-hyperlink-on-an-entity.html

## 文章内容

By Augusto Goncalves
Entities in AutoCAD can be associated with hyperlinks. Users can visit the referenced locations from the hyperlink on an entity. There are three types of hyperlink locations on AutoCAD entities. They are URLs, files, and DWG file targets (model, layout1, and so on). This article shows how to use .NET API to create a URL hyperlink on an entity. The code is in C#.
[CommandMethod("createHLink")]
static public void CmdCreateHyperLink()
{
  Editor ed = Application.DocumentManager.
    MdiActiveDocument.Editor;
  Database db = Application.DocumentManager.
    MdiActiveDocument.Database;
  PromptEntityResult selectedEntity =
    ed.GetEntity("Please Select an Entity: ");
  ObjectId objectId = selectedEntity.ObjectId;
  try
  {
    using (Transaction trans =
      db.TransactionManager.StartTransaction())
    {
      //Get the entity
      Entity ent = trans.GetObject(objectId,
        OpenMode.ForWrite) as Entity;
        //Get the hyperlink collection from the entity
      HyperLinkCollection linkCollection = ent.Hyperlinks;
        //Create a new hyperlink
      HyperLink hyperLink = new HyperLink();
      hyperLink.Description = "ADN DevBlog";
      hyperLink.Name = "ADN DevBlog";
      hyperLink.SubLocation =
        "http://adndevblog.typepad.com/autocad/";
        //Add the hyperlink to the collection
      linkCollection.Add(hyperLink);
      trans.Commit();
    }
  }
  catch (System.Exception ex)
  {
    ed.WriteMessage(ex.Message);
  }
}

## 评论

**内容**: Luigi71 said...
Hello Mr. Goncalves.
I'm trying to change a hyperlink description using VB.NET, here's the code:

Using acLockCurrDoc As DocumentLock = acDoc.LockDocument()
Using acTrans As Transaction = acCurDb.TransactionManager.StartTransaction()

Dim MyEntity As Entity = CType(acTrans.GetObject(MyObjID, OpenMode.ForWrite), Entity)
Dim hyperlinkColl As HyperLinkCollection = MyEntity.Hyperlinks
Dim hyperL As HyperLink = hyperlinkColl.Item(0)
hyperL.Description ="Some description"

acTrans.Commit()

End Using
End Using

Step through the code in debug mode, after passing hyperL.Description ="Some description" row, the Description property of the hyperlink is
effectively modified as I can see from the variable window of VisualStudio, but when I go to the drawing in order to verify if the modification have taken place, the hyperlink description was not modified.
Any suggestion?
Thanks alot in advance.
Luigi
Reply
11/12/2013 at 02:15 AM

---
**内容**: Augusto Goncalves said in reply to Luigi71...
Luigi,
Can you try set it back?
Read with
Dim hyperL As HyperLink = hyperlinkColl.Item(0)
Change the description...
Then write back
hyperlinkColl.Item(0) = hyperL
Hope this helps.
Regards,
Augusto Goncalves
Reply
11/19/2013 at 07:29 PM

---
**内容**: Luigi said...
Hello Augusto, thankyou for the answer.
Tried out the suggestion but getting an 'AccessViolationException, Attempted to read or write protected memory. This is often an indication that other memory is corrupt'.
If I do the following:
hyperlinkColl.RemoveAt(0)
hyperlinkColl.Add(hyperL)
I'm getting the same exception.
The only way to solve the issue seems to create another Hyperlink instance, such as
Dim hyperL2 = New HyperLink
then
hyperL2.Description = hyperL.Description
hyperL2.Description "New description"
hyperlinkColl.RemoveAt(0)
hyperlinkColl.Add(hyperL2)
In this case all works fine.
It would be interesting to investigate...
Thankyou
Best regards.
Luigi
Reply
11/20/2013 at 01:29 PM

---
**内容**: Aleksey said...
Hello Augusto,
There is mistake:
You shouldn't use hyperLink.SubLocation. Instead use
hyperLink.Name = "http://adndevblog.typepad.com/autocad/";
Otherwise you will have incorrect link like "ADN DevBlog#http://adndevblog.typepad.com/autocad/"
Reply
02/11/2014 at 04:15 AM

---
**内容**: Wilco said...
Aleksey is right, don't use hyperLink.SubLocation it is for bookmarks. hyperLink.Name did the trick for me.
Reply
12/03/2014 at 01:55 AM

---
**内容**: Wess Wesselink said...
And how can I create a hyperlink to an image on the network?
I've created a tool that lets the user select a folder with photo's and the tool reads the GPS location and puts a triangle at this location with a hyperlink attached to it.
The idea is that when the user clicks on the triangle the picture taken at this location is automatically opened.
Reply
09/10/2022 at 11:04 AM

---
