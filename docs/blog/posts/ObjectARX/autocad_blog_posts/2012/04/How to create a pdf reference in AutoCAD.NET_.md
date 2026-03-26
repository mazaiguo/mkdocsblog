---
title: "How to create a pdf reference in AutoCAD.NET?"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
  - PDF
description: "PDF underlay’s are represented by the PdfDefinition and PdfReference classes in the AutoCAD .NET API. An Underlay (in this case PDF) Reference must..."
author: Autodesk
---
# How to create a pdf reference in AutoCAD.NET?

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-create-a-pdf-reference-in-autocadnet.html

## 文章内容

By Virupaksha Aithal
PDF underlay’s are represented by the PdfDefinition and PdfReference classes in the AutoCAD .NET API. An Underlay (in this case PDF) Reference must reference compatible an underlay definition. The Underlay reference is responsible for the placement of the content within the drawing while Underlay Definition handles the linkage to the underlay content.
Note: The path for the PDF is hard coded and needs to be edited to reflect the path on your system.
[CommandMethod("pdfInsert")]
static public void DoPdfInsert()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      using (Transaction t =
        doc.TransactionManager.StartTransaction())
    {
        DBDictionary nod =
            (DBDictionary)t.GetObject(db.NamedObjectsDictionaryId,
                                                OpenMode.ForWrite);
        string defDictKey =
          UnderlayDefinition.GetDictionaryKey(typeof(PdfDefinition));
          if (!nod.Contains(defDictKey))
        {
            using (DBDictionary dict = new DBDictionary())
            {
                nod.SetAt(defDictKey, dict);
                t.AddNewlyCreatedDBObject(dict, true);
            }
        }
        ObjectId idPdfDef;
        DBDictionary pdfDict =
            (DBDictionary)t.GetObject(nod.GetAt(defDictKey),
                                        OpenMode.ForWrite);
          using (PdfDefinition pdfDef = new PdfDefinition())
        {
            pdfDef.SourceFileName = @"C:\temp\test.pdf";
            idPdfDef = pdfDict.SetAt("TEST", pdfDef);
            t.AddNewlyCreatedDBObject(pdfDef, true);
        }
        BlockTable bt =
            (BlockTable)t.GetObject(db.BlockTableId,
                                    OpenMode.ForRead);
        BlockTableRecord btr =
            (BlockTableRecord)t.GetObjec(
                            bt[BlockTableRecord.ModelSpace],
                           OpenMode.ForWrite);
          using (PdfReference pdf = new PdfReference())
        {
            pdf.DefinitionId = idPdfDef;
              btr.AppendEntity(pdf);
            t.AddNewlyCreatedDBObject(pdf, true);
        }
        t.Commit();
    }
}

## 评论

**内容**: Christos Zambas said...
Hello,
Thank you for the code above. I'm working on an AutoCAD plugin and I need to implement -PDFATTACH, which I believe is what this does. Would you by any chance also know how to choose which PDF page to display? I don't see any relevant functions/properties in the PdfDefinition and PdfReference variables.
Thank you in advance,
Christos Zambas
Reply
06/15/2018 at 10:34 AM

---
**内容**: Josh said...
I have basically the same question as the above..
Also, does anyone know where these show up in AutoCad? They don't appear in the underlay
Reply
06/12/2022 at 08:42 PM

---
