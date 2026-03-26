---
title: "AutoCAD P&ID/Plant 3D: Is there any API to recalculate Tags?"
date: 2012-10-01
categories:
  - Plant 3D
tags:
  - API
  - AutoCAD
  - Plant 3D
description: "When a tag format changes, manual update of the respective tags is a very time consuming operation. Can I update the tags with the API?"
author: Autodesk
---
# AutoCAD P&ID/Plant 3D: Is there any API to recalculate Tags?

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/autocad-pidplant-3d-is-there-any-api-to-recalculate-tags.html

## 文章内容

By Marat Mirgaleev
Issue
When a tag format changes, manual update of the respective tags is a very time consuming operation. Can I update the tags with the API?
Solution
To update a tag, you can simply write out a blank tag value with the DataLinksManager.SetProperties() which causes a recalc.
Here is a sample how to do this. It works for Piping and P&ID.
[CommandMethod("PexTagUpdate", CommandFlags.Modal)]
public void PexTagUpdate() // This method can have any name
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
  ed.WriteMessage("\nUpdate tag values");
  string dwgtype = PnPProjectUtils.GetActiveDocumentType();
    if (dwgtype != "PnId" && dwgtype != "Piping")
  {  //"PnId", "Piping", "Ortho", "Iso"
    ed.WriteMessage("\nDrawing must be a PnId or Piping drawing"
                  + " in the current project.\n");
    return;
  }
  Project prj = PnPProjectUtils.GetProjectPartForCurrentDocument();
  DataLinksManager dlm = prj.DataLinksManager;
    PromptSelectionOptions pso = new PromptSelectionOptions();
  pso.MessageForAdding = "\nSelect " + dwgtype
                       + " objects to update <All>: ";
  PromptSelectionResult selResult = ed.GetSelection(pso);
  if (selResult.Status == PromptStatus.Cancel)
    return;
  if (selResult.Status != PromptStatus.OK)
    selResult = ed.SelectAll();
  SelectionSet ss = selResult.Value;
  ObjectId[] objIds = ss.GetObjectIds();
  int nTags = 0, nTagsModified = 0;
    foreach (ObjectId objId in objIds)
  {
    Database oDB =
               Application.DocumentManager.MdiActiveDocument.Database;
    Autodesk.AutoCAD.DatabaseServices.TransactionManager tmgr
      = oDB.TransactionManager;
    using (Transaction t = tmgr.StartTransaction())
    {
      StringCollection strNames = new StringCollection();
      StringCollection strNewValues = new StringCollection();
      strNames.Add("Tag");
      strNewValues.Add("");  // A blank value causes a recalc.
                  // A tag that is currently blank will remain blank.
      try
      {
        DBObject obj = t.GetObject(objId, OpenMode.ForRead);
        if (!dlm.HasLinks(objId))
          continue; // Not a Plant object
        nTags++;
        StringCollection strOldValues =
            dlm.GetProperties(objId, strNames, true);
          //----- HERE IT IS. UPDATE OF THE TAG ------------------------
        dlm.SetProperties(objId, strNames, strNewValues);
        //------------------------------------------------------------
          t.Commit();
          // Get new values
        StringCollection strRecalcValues =
            dlm.GetProperties(objId, strNames, true);
        if (strRecalcValues[0] == "")
          continue;
        nTagsModified++;
        // Report changes
        ed.WriteMessage("\n   tag=" + strRecalcValues[0]);
        if (strOldValues[0] != strRecalcValues[0])
          ed.WriteMessage("  oldtag=" + strOldValues[0]);
      }
      catch (System.Exception e)
      {
        if (t != null)
        {
          t.Abort();
          t.Dispose();
        }
        ed.WriteMessage("\nCould not update tag: "
                      + e.Message.ToString());
      }
    }
  }
  ed.WriteMessage("\nDone (" + nTagsModified + " of " + nTags
                + " modified).");
}

## 评论

**内容**: Marat Mirgaleev said...
Surely, it will be better to move StartTransaction() out of the foreach cycle.
Reply
12/03/2012 at 07:50 AM

---
**内容**: Klaus Schachinger said...
is there a way which normal user can do?
Reply
06/26/2015 at 07:48 AM

---
**内容**: Artem said...
It's very useful code! I can't understand why Plant 3D developers don't realize this command as standart.
Thank you!
Reply
10/07/2016 at 05:58 AM

---
**内容**: Klaus Schachinger said...
Hi, I am still waiting for that command!
Reply
07/24/2017 at 03:45 PM

---
