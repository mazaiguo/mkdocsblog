---
title: "Unload all the PDF underlay"
date: 2016-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Database
  - PDF
description: "Below code shows the procedure to unload all the PDF underlays. It is required to update the corresponding PDF underlay references , so that AutoCA..."
author: Autodesk
---
# Unload all the PDF underlay

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/unload-all-the-pdf-underlay.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to unload all the PDF underlays. It is required to update the corresponding PDF underlay references , so that AutoCAD can update the model space graphics. For this, the “PdfDefinition.GetPersistentReactorIds” API is used to get all the references of the PDF underlay definition.
[CommandMethod("PdfUnload")]
static public void PdfUnload()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;

    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        DBDictionary nod = Tx.GetObject(db.NamedObjectsDictionaryId, 
                                                    OpenMode.ForRead) as DBDictionary;

        string defDictKey = UnderlayDefinition.GetDictionaryKey(typeof(PdfDefinition));

        if (!nod.Contains(defDictKey))
            return;

        DBDictionary pdfDict = Tx.GetObject(nod.GetAt(defDictKey), 
                                                    OpenMode.ForWrite) as DBDictionary;

        foreach (DBDictionaryEntry entry in pdfDict)
        {
            PdfDefinition entryObj = Tx.GetObject(entry.Value, 
                                                    OpenMode.ForWrite) as PdfDefinition;
            entryObj.Unload();

            ObjectIdCollection collection = entryObj.GetPersistentReactorIds();

            foreach (ObjectId id in collection)
            {
                DBObject temObject = Tx.GetObject(id, OpenMode.ForRead);

                if (temObject is PdfReference)
                {
                    PdfReference pdfref = temObject as PdfReference;
                    pdfref.UpgradeOpen();
                    pdfref.RecordGraphicsModified(true);
                }
            }
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Alexander Rivilis said...
Dear Virupaksha Aithal!
You wrote: "It is required to remove corresponding PDF underlay references from the drawing".
But in your's code there are not any removing of PDFReference's (e.g. pdfref.Erase() ). Only "regen" of PDFReference's.
As far as I see it is enough in order to hide it in drawing: http://autode.sk/2axfW7G
Reply
07/21/2016 at 05:47 AM

---
**内容**: viru said in reply to Alexander Rivilis...
Hi Rivilis,
You are correct, now i have updated the text. code need to make sure reference are redraw (not draw) once we remove the definition
thanks again.
regards
Viru
Reply
07/21/2016 at 09:49 PM

---
