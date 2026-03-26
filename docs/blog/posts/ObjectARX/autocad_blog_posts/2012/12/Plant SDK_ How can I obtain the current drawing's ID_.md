---
title: "Plant SDK: How can I obtain the current drawing's ID?"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - DWG
description: "I can easily find the filename of the current drawing, but not its ID. Can you help me, please?"
author: Autodesk
---
# Plant SDK: How can I obtain the current drawing's ID?

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/plant-sdk-how-can-i-obtain-the-current-drawings-id.html

## 文章内容

By Marat Mirgaleev
Issue
I can easily find the filename of the current drawing, but not its ID. Can you help me, please?
Solution
You can find the current PnPProjectDrawing object in the list of the current project's drawings, then get the Id property of this PnPProjectDrawing:
    [CommandMethod("FiID")]
    public static void FindTheDwgId()
    {
      Editor ed =Application.DocumentManager.MdiActiveDocument.Editor;
      int foundId = -1;
      Project prj =PnPProjectUtils.GetProjectPartForCurrentDocument();
      System.Collections.Generic.List<PnPProjectDrawing> dwgList =
                                             prj.GetPnPDrawingFiles();
      foreach (PnPProjectDrawing dwg in dwgList)
      {       
        ed.WriteMessage(string.Format("\n--Filename: {0}, Id: {1}",
                                       dwg.AbsoluteFileName, dwg.Id));
        if( String.Equals( Application.DocumentManager.
                                  MdiActiveDocument.Database.Filename,
                        dwg.ResolvedFilePath,
                        StringComparison.InvariantCultureIgnoreCase))
        {
          foundId = dwg.Id;
          break;
        }
      }
      ed.WriteMessage(string.Format(
                 "\nThe Id of the current drawing is: {0}", foundId));
    } // FindTheDwgId()

## 评论

**内容**: dennis said...
I am struggling here with VB.NET and Plant3D. I have downloaded the Plant SDK for 2015Here is what I want to do: Access the Drawing Properties, such as AREA, and make changes to those properties. For example, change a blank entry for AREA to Area51. I am a bit lost now on what References I should load, what namespace I should Import. And then how to call the right Dim pProp ??? to get me going. Please help if you can.
Reply
07/02/2014 at 11:10 AM

---
