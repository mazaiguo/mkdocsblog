---
title: "Can I get the list of entities which were selected before the current command started (in .NET)?"
date: 2012-10-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Plot
description: "If the user had selected some entities and then started my command, can I find out which entities were selected?"
author: Autodesk
---
# Can I get the list of entities which were selected before the current command started (in .NET)?

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/can-i-get-the-list-of-entities-which-were-selected-before-the-current-command-started-in-net.html

## 文章内容

By Marat Mirgaleev
Issue
If the user had selected some entities and then started my command, can I find out which entities were selected?
Solution
Yes, it is possible, if the PICKFIRST system variable is set to 1 and your command has the UsePickSet flag set.
The sample below shows a command that prints out the list of selected entities.
  [CommandMethod("LiPS", CommandFlags.UsePickSet)]
  public static void ListPreSelected()
  {
    Document doc = Application.DocumentManager.MdiActiveDocument;
    PromptSelectionResult selectionResult =
                                          doc.Editor.SelectImplied();
    if (selectionResult.Status == PromptStatus.OK)
    {
      using (Transaction tr =
                  doc.Database.TransactionManager.StartTransaction())
      {
        SelectionSet currentlySelectedEntities =
                                               selectionResult.Value;
        foreach (ObjectId id
                 in currentlySelectedEntities.GetObjectIds())
        {
          Entity ent = tr.GetObject(id, OpenMode.ForRead) as Entity;
          doc.Editor.WriteMessage("\n..." + ent.ToString());
        }
      }
    }
    else
      doc.Editor.WriteMessage("\n...SelectionResult.Status="
                                + selectionResult.Status.ToString());
  } // ListPreSelected()

## 评论

**内容**: dba said...
Hi, I see, this is an older post, but maybe it's still active. Is there a way to find out, which object is involved in a certain command execution?
Especially if the command "GRIP_POPUP" starts on a dynamic block, the current selection does not seem to help, since I can start the command even if multiple obejcts are currently selected and the command affects one Blockref only.
Any hints are appreciated.
Thanks,
Daniel
Reply
07/07/2014 at 04:10 AM

---
