---
title: "List DWF underlay definitions in the drawing"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - Database
description: "Each DWF underlay definitions are stored in the named object Dictionary under Dictionary name "ACADDWFDEFINITIONS". Below code shows the procedure ..."
author: Autodesk
---
# List DWF underlay definitions in the drawing

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/list-dwf-underlay-definitions-in-the-drawing.html

## 文章内容

By Virupaksha Aithal
Each DWF underlay definitions are stored in the named object Dictionary under Dictionary name "ACAD_DWFDEFINITIONS". Below code shows the procedure to go through the "ACAD_DWFDEFINITIONS" Dictionary and listing all the DWF definitions.
[CommandMethod("DWFUnderlayList")]
static public void DWFUnderlayList()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr =
                    db.TransactionManager.StartTransaction())
    {
        DBDictionary nod = (DBDictionary)tr.GetObject(
                db.NamedObjectsDictionaryId, OpenMode.ForRead);
          string defDictKey = UnderlayDefinition.GetDictionaryKey(
                                            typeof(DwfDefinition));
          if (nod.Contains(defDictKey))
        {
            DBDictionary dwfDict =
                        (DBDictionary)tr.GetObject(
                           nod.GetAt(defDictKey), OpenMode.ForRead);
              foreach (DBDictionaryEntry entry in dwfDict)
            {
                DwfDefinition dwfDef = (DwfDefinition)tr.GetObject(
                                    entry.Value, OpenMode.ForRead);
                  ed.WriteMessage(dwfDef.ActiveFileName + "\n");
            }
        }
        else
        {
            ed.WriteMessage("No DWF underlay in the drawing file\n");
        }
          tr.Commit();
    }
}

## 评论

**内容**: LM said...
Is there a .NET API to implement the same funtion as "ULAYERS" in command line? or how to access layer information from a DGNDefinition?
Reply
03/27/2013 at 07:51 AM

---
