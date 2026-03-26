---
title: "Plant SDK: How to programmatically change the “Status” property of a Butt Weld?"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I managed to find all the butt welds in the drawing, they are kept inside the Autodesk.ProcessPower.PnP3dObjects.Connector class. But I can’t find ..."
author: Autodesk
---
# Plant SDK: How to programmatically change the “Status” property of a Butt Weld?

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/plant-sdk-how-to-programmatically-change-the-status-property-of-a-butt-weld.html

## 文章内容

By Marat Mirgaleev
Issue
I managed to find all the butt welds in the drawing, they are kept inside the Autodesk.ProcessPower.PnP3dObjects.Connector class. But I can’t find the “Status” property in these objects. How can I access this property and change its value?
Solution
The “Status” property and many others are stored in a SubPart of the Connector object. So, what we need to do is to iterate through these SubParts and find one of the WeldSubPart type. Here is a sample (some error checking is omitted for brevity):
[CommandMethod("UpSt", CommandFlags.UsePickSet)]
public void UpdateStatus_ShortVersion()
{
  try
  {
    // Make sure you pre-selected a Connector of Weld type!
    PromptSelectionResult selResult = acApp.DocumentManager.
                          MdiActiveDocument.Editor.SelectImplied();
    SelectionSet selSet = selResult.Value;
    ObjectId[] objIds = selSet.GetObjectIds();
    ObjectId weldObjID = objIds[0];
      Database db =acApp.DocumentManager.MdiActiveDocument.Database;
    using (Transaction tr =
                          db.TransactionManager.StartTransaction())
    {
      PnP3D.Connector wld = tr.GetObject( weldObjID,
                OpenMode.ForRead, false, true) as PnP3D.Connector;
        DataLinksManager dlm = PlantApplication.CurrentProject.
                          ProjectParts["Piping"].DataLinksManager;
      PartsRepository projectParts = DataLinksManager3d.
                          Get3dManager(dlm).ProjectPartsRepository;
        PnP3D.SubPartCollection subPartColl = wld.AllSubParts;
      int index = 1; // NOTE: We start from 1, not from 0!
      foreach (PnP3D.SubPart sp in subPartColl)
      {
        if (sp is PnP3D.WeldSubPart)
        {
          int rowId = dlm.FindAcPpRowId( dlm.MakeAcPpObjectId(
                                              weldObjID, index ));
          Autodesk.ProcessPower.PartsRepository.Part partWld =
                                      projectParts.FindPart(rowId);
            // To set properties we need to call BeginEdit()
          //   and EndEdit()
          partWld.BeginEdit();
          partWld["Status"] = "Existing";
          partWld.EndEdit();
        }
        index++;
      } // foreach subpart
      dlm.AcceptChanges();
      tr.Commit();
    } // using
  }
  catch (System.Exception e)
  {
    acApp.DocumentManager.MdiActiveDocument.Editor.WriteMessage(
                                                    e.ToString());
  }
} // UpdateStatus_ShortVersion()

## 评论

**内容**: rflin@ctcim.com.tw said...
Hi,
could you send the Visual studio project for this subject to me?
Thanks'
Reply
08/26/2015 at 10:27 PM

---
**内容**: divya said in reply to rflin@ctcim.com.tw...
Did you got the code?
Reply
02/20/2020 at 05:34 AM

---
**内容**: RF Lin said...
Hi,
How to assign the weld number to properties by Plant SDK?
Reply
08/26/2015 at 10:30 PM

---
**内容**: divya said in reply to RF Lin...
Autodesk.ProcessPower.PnP3dObjects.Connector class i am unable to find this class
Reply
02/20/2020 at 05:47 AM

---
**内容**: RF Lin said...
How to get all of the weld object of one Line?
Reply
08/27/2015 at 07:49 PM

---
