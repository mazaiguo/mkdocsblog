---
title: "Setting pick first selection set from using AutoCAD.NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Selection
description: "You can use “Editor. SetImpliedSelection” API to set the pick first (selection with grips) selection set. The code below is a code for sample comma..."
author: Autodesk
---
# Setting pick first selection set from using AutoCAD.NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/setting-pick-first-selection-set-from-using-autocadnet.html

## 文章内容

By Virupaksha Aithal
You can use “Editor. SetImpliedSelection” API to set the pick first (selection with grips) selection set. The code below is a code for sample command, which prompts for entity selection and places it to pick first selection set. Please note it's necessary to specify command flags for commands, which access pick first selection set.
[CommandMethod("SelectTest", CommandFlags.UsePickSet |
                        CommandFlags.Redraw | CommandFlags.Modal)]
static public void SelectTest()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      try
    {
        PromptSelectionResult result = ed.GetSelection();
        if (result.Status != PromptStatus.OK)
            return;
          ed.SetImpliedSelection(result.Value.GetObjectIds());
    }
    catch(System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

## 评论

**内容**: BKSpurgeon said...
Hi thx for the above. It is a little unclear to me what what setimpliedselection does? I've looked in the ObjectARX developers and reference guides and have not got a clear answer from them. any ideas on: (i) what it does, (ii) methods and (iii) parameters which it is capable fo holding.
Moreoever - where can I myself find out what it does?
your assistance is much appreciated.
Reply
04/20/2015 at 05:05 PM

---
**内容**: Virupaksha Aithal said...
Hi,
Please refer AutoCAD.NET documentation of setimpliedselection. http://docs.autodesk.com/ACD/2010/ENU/AutoCAD%20.NET%20Developer%27s%20Guide/index.html?url=WS1a9193826455f5ff2566ffd511ff6f8c7ca-4098.htm,topicNumber=d0e17281. Also, refer Kean's blog http://through-the-interface.typepad.com/through_the_interface/2006/09/using_the_pickf.html which few more details on setimpliedselection.
Reply
04/20/2015 at 10:24 PM

---
