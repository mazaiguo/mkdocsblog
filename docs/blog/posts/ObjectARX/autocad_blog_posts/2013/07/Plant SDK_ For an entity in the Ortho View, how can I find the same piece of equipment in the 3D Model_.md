---
title: "Plant SDK: For an entity in the Ortho View, how can I find the same piece of equipment in the 3D Model?"
date: 2013-07-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
description: "I would like to let my users to select an entity in the Ortho view in AutoCAD Plant 3D and find some properties of this selected equipment:"
author: Autodesk
---
# Plant SDK: For an entity in the Ortho View, how can I find the same piece of equipment in the 3D Model?

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/plant-sdk-for-an-entity-in-the-ortho-view-how-can-i-find-the-same-piece-of-equipment-in-the-3d-model.html

## 文章内容

By Marat Mirgaleev
Issue
I would like to let my users to select an entity in the Ortho view in AutoCAD Plant 3D and find some properties of this selected equipment:
But it seems that to do this I need to find the corresponding object in the 3D model first:
How can I do this?
Solution
Unfortunately, the current Plant SDK does not provide this functionality. But a good news is that there is an undocumented class that is safe to use for this purpose.
Before we start coding, we need to find some sample drawings which we can use for testing. Let it be the out-of-the-box SampleProject with its Area1_Plan drawing:
and the 3D model in 1-PE-001 drawing:
Screenshots from these files can be found at the top of this post.
Let’s start from selecting an entity in the Ortho view. When you test the code, do not forget to switch from PAPER space to MODEL using the button shown on the first screenshot (or you just can’t select anything).
As soon as we have the selected entity’s ObjectId, we can call the undocumented method
     Autodesk.ProcessPower.Drawings2d.PnPDwg2dUtil.GetModelObjectId().
It is located in an assembly called C:\Program Files\Autodesk\AutoCAD 2014\PLNT3D\PnPDwg2dUtil.dll and, obviously, we need to add a reference to it from our Visual Studio project.
This is a code snippet which demonstrates usage of the GetModelObjectId() method. It defines a new command called “FOTM” (From Ortho To Model):
    // From an entity in Ortho, looking for this entity in the Model.
    // Using the out-of-the-box SampleProject for tests:
    //   Ortho: Area1_Plan
    //   Model: 1-PE-001
    // In Area1_Plan, you need to switch from Paper to Model,
    //   otherwise you can't select anything in it.
    //===============================================================
    [CommandMethod("FOTM")]
    public void FromOrthoToModel()
    {
      // To test, select an entity in an Ortho drawing
      Document doc = Application.DocumentManager.MdiActiveDocument;
      PromptEntityResult selectedEntity = doc.Editor.GetEntity(
                                  "\nSelect an entity to annotate:");
      if (selectedEntity.Status != PromptStatus.OK)
        return;
        // GetModelObjectId() is an undocumented method to find
      //   the corresponding entity in the Piping Model
      //=============================================================
      Autodesk.ProcessPower.Drawings2d.MdObjectId orthoId =
            Autodesk.ProcessPower.Drawings2d.PnPDwg2dUtil.
                  GetModelObjectId(selectedEntity.ObjectId,
                                   selectedEntity.ObjectId.Database);
        // In this orthoId we have a drawing GUID and PpObjectId:
      Autodesk.ProcessPower.DataLinks.PpObjectId ppId =
                                                 orthoId.PrjObjectId;
      string dwgGUID = orthoId.DwgGUID;
        // Find the entity's ObjectId in the Model drawing.
      // Note: To do this you have to have the Model drawing open.
      Autodesk.ProcessPower.DataLinks.DataLinksManager dlm =
                         PlantApplication.CurrentProject.
                            ProjectParts["Piping"].DataLinksManager; 
      ObjectId oid = dlm.MakeAcDbObjectId(ppId);
        // THAT'S IT:
      doc.Editor.WriteMessage("\n oid=" + oid.ToString());
      } // FromOrthoToModel()

## 评论

**内容**: Louis Jacobs said...
Marat,
What I want to do is the reverse in a way.
I have the PnPID of a pump in a P&ID drawing.
I show a list of possible values for the pump, allowing engineers to edit the data externally in an Access database.
What I'd like to do is, to select the datarow and then to navigate to the P&ID and zoom into that pump.
Is this possible?
Reply
01/29/2014 at 04:23 AM

---
**内容**: ced44 said in reply to Louis Jacobs...
Hi Louis,
Did you had the solution of your question?
I'm very interested about it !!
Regards
Reply
07/17/2014 at 12:18 AM

---
**内容**: Jhaze said...
Does the api have the functionality to create an orthographic drawing of a lets say a "pipe support component" in a drawing? assuming that I have drawn a whole Plant?
Reply
02/20/2020 at 07:29 PM

---
