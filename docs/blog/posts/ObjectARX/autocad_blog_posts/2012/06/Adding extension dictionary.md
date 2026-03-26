---
title: "Adding extension dictionary"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Plugin
description: "Each AutoCAD object can store a custom data with it. Normally this functionality is used by AutoCAD graphical entities to store non graphical data...."
author: Autodesk
---
# Adding extension dictionary

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/adding-extension-dictionary.html

## 文章内容

By Virupaksha Aithal
Each AutoCAD object can store a custom data with it. Normally this functionality is used by AutoCAD graphical entities to store non graphical data. For example, an AutoCAD line can store a string or/and a double with it (in its extension dictionary). Below code shows the procedure to add an extension dictionary strong a double and a string
[CommandMethod("AddExtensionDictionary")]
public void AddExtensionDictionary()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityResult ers = ed.GetEntity("Select entity to add" +
                                           " extension dictionary ");
    if (ers.Status != PromptStatus.OK)
        return;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        DBObject dbObj = tr.GetObject(ers.ObjectId,
                                                   OpenMode.ForRead);
          ObjectId extId = dbObj.ExtensionDictionary;
          if (extId == ObjectId.Null)
        {
            dbObj.UpgradeOpen();
            dbObj.CreateExtensionDictionary();
            extId = dbObj.ExtensionDictionary;
        }
          //now we will have extId...
        DBDictionary dbExt =
                (DBDictionary)tr.GetObject(extId, OpenMode.ForRead);
          //if not present add the data
        if (!dbExt.Contains("TEST"))
        {
            dbExt.UpgradeOpen();
            Xrecord xRec = new Xrecord();
            ResultBuffer rb = new ResultBuffer();
            rb.Add(new TypedValue(
                      (int)DxfCode.ExtendedDataAsciiString, "Data"));
            rb.Add(new TypedValue((int)DxfCode.ExtendedDataReal,
                                                              10.2));
              //set the data
            xRec.Data = rb;
              dbExt.SetAt("TEST", xRec);
            tr.AddNewlyCreatedDBObject(xRec, true);
        }
        else
        {
            ed.WriteMessage("entity contains the TEST data\n");
        }
            tr.Commit();
    }
  }

## 评论

**内容**: Bruno S said...
Hello,
Thanks for the post. Very helpful. However, I have a question. Is there a way to get/edit those values in the editor? If so, where?
Thanks.
Regards,
Bruno
Reply
01/10/2013 at 01:22 PM

---
