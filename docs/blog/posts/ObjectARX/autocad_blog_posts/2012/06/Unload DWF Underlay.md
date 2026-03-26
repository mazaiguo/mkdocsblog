---
title: "Unload DWF Underlay"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "To unload a DWF Underlay, you need to unload the “DwfDefinition” using its API “Unload”. Below code shows the procedure to unload a dwf Underlay."
author: Autodesk
---
# Unload DWF Underlay

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/unload-dwf-underlay.html

## 文章内容

By Virupaksha Aithal
To unload a DWF Underlay, you need to unload the “DwfDefinition” using its API “Unload”. Below code shows the procedure to unload a dwf Underlay.
[CommandMethod("DWFUnload")]
static public void DWFUnload()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
               new PromptEntityOptions("\nSelect a Dwf Reference");
    options.SetRejectMessage("\nSelect only Dwf Reference");
    options.AddAllowedClass(typeof(DwfReference), false);
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
      if (acSSPrompt.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        //get the DwfReference
        DwfReference dwfref = Tx.GetObject(acSSPrompt.ObjectId,
                                   OpenMode.ForRead) as DwfReference;
        //get the definiation
        DwfDefinition DwfDef = (DwfDefinition)Tx.GetObject(
                             dwfref.DefinitionId, OpenMode.ForWrite);
          DwfDef.Unload();
          ObjectIdCollection collection =
                                    DwfDef.GetPersistentReactorIds();
        foreach (ObjectId id in collection)
        {
            DBObject temObject = Tx.GetObject(id, OpenMode.ForRead);
              if (temObject is DwfReference)
            {
                DwfReference pdfref = temObject as DwfReference;
                pdfref.UpgradeOpen();
                pdfref.RecordGraphicsModified(true);
            }
        }
        Tx.Commit();
    }
}

## 评论

**内容**: Doublefish said...
How unload xref?
Reply
07/05/2012 at 10:40 PM

---
**内容**: Virupaksha Aithal said...
Hi,
Please take a look at blog post http://adndevblog.typepad.com/autocad/2012/07/unload-external-reference.html
Thanks
Viru
Reply
07/06/2012 at 03:33 AM

---
**内容**: TTaylor said...
Thank you Viru! Now...how do you unload/reload dwf files that are nested within another xref (dwg file). The files appear in the xref manager as subordinates of the xref, can be manually unloaded/reloaded, but are not in the dwf dictionary. Please help!
Reply
03/30/2015 at 11:44 PM

---
