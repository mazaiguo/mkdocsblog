---
title: "Remove vertices from 3d Polyline"
date: 2013-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Database
  - Polyline
description: "Below code shows the procedure to remove the user specified vertex of AutoCAD 3d Polyline. Code, first traverse through the vertices of the user se..."
author: Autodesk
---
# Remove vertices from 3d Polyline

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/remove-vertexes-from-3d-polyline.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to remove the user specified vertex of AutoCAD 3d Polyline. Code, first traverse through the vertices of the user selected 3d Polyline and prepares a list of vertexes to be erased.
[CommandMethod("Remove3DVertex")]
static public void RemoveVertex()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction oTr =
                        db.TransactionManager.StartTransaction())
    {
        ObjectIdCollection ids = new ObjectIdCollection();
          PromptEntityOptions options =
                   new PromptEntityOptions("\nPick a 3DPolyline:");
        options.SetRejectMessage("Select 3DPolyline only" + "\n");
        options.AddAllowedClass(typeof(Polyline3d), true);
        PromptEntityResult result = ed.GetEntity(options);
          if (result.Status != PromptStatus.OK)
            return;
          Polyline3d oEnt = oTr.GetObject(result.ObjectId,
                                    OpenMode.ForRead) as Polyline3d;
            foreach (ObjectId oVtId in  oEnt)
        {
            PolylineVertex3d oVt = oTr.GetObject(oVtId,
                            OpenMode.ForRead) as PolylineVertex3d;
            PromptKeywordOptions oPko =
             new PromptKeywordOptions("\nWant to remove vertex at "
                                 + oVt.Position.ToString() + "?");
              oPko.AllowNone = false;
            oPko.Keywords.Add("Yes");
            oPko.Keywords.Add("No");
            oPko.Keywords.Default = "No";
            PromptResult oPkr = ed.GetKeywords(oPko);
              if (oPkr.Status == PromptStatus.OK
                                && oPkr.StringResult == "Yes")
            {
                ids.Add(oVtId);
            }
        }
          foreach (ObjectId oVtId in ids)
        {
            PolylineVertex3d oVt = oTr.GetObject(oVtId,
                        OpenMode.ForWrite) as PolylineVertex3d;
            oVt.Erase();
        }
          if (ids.Count != 0)
        {
            oEnt.UpgradeOpen();
            oEnt.RecordGraphicsModified(true);
        }
          oTr.Commit();
    }
}

