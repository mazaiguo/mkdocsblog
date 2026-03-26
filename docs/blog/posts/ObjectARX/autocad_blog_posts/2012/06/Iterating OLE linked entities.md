---
title: "Iterating OLE linked entities"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
description: "Below code shows the procedure to identify the ole linked entity and also shows the procedure to get the linked file name. Note, only linked OLE en..."
author: Autodesk
---
# Iterating OLE linked entities

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/iterating-ole-linked-entities.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to identify the ole linked entity and also shows the procedure to get the linked file name. Note, only linked OLE entities will have link path.
[CommandMethod("oleTest")]
public void oleTest()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectId ModelSpaceId =
               SymbolUtilityServices.GetBlockModelSpaceId(db);
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        BlockTableRecord model = tr.GetObject(ModelSpaceId,
                             OpenMode.ForRead) as BlockTableRecord;
          foreach (ObjectId id in model)
        {
            DBObject obj = tr.GetObject(id, OpenMode.ForRead);
              if (obj is Ole2Frame)
            {
                Ole2Frame oleObj = obj as Ole2Frame;
                  if (oleObj.Type == Ole2Frame.ItemType.Link)
                {
                    ed.WriteMessage(oleObj.LinkPath + "\n");
                }
                else if (oleObj.Type == Ole2Frame.ItemType.Embedded)
                {
                    //Embedded...
                }
              }
        }
          tr.Commit();
    }
  }

## 评论

**内容**: Mehmet Kurt said...
Hi,
How to create OLE object using bitmap file on AutoCAD dwg drawing as programmatically [C#]. I guess OLE2FRAME is using but how ?
Thanks
Reply
08/08/2012 at 09:01 AM

---
**内容**: Greg Hugo said...
Best services!
https://staysuptodate.wordpress.com/rank-1-on-google/?preview=true
Reply
08/13/2018 at 01:52 PM

---
