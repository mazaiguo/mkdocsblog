---
title: "Clear pick first selection set"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - API
  - Selection
description: "You can use “Editor.SetImpliedSelection” API to clear the pick first (selection with grips) selection set. The code below first gets the list of ob..."
author: Autodesk
---
# Clear pick first selection set

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/clear-pick-first-selection-set-.html

## 文章内容

By Virupaksha Aithal
You can use “Editor.SetImpliedSelection” API to clear the pick first (selection with grips) selection set. The code below first gets the list of objects in pick first selection set and clear the selection set later by passing empty ObjectId array to SetImpliedSelection.
[CommandMethod("ClearPickFirst", CommandFlags.UsePickSet |
                CommandFlags.Redraw | CommandFlags.Modal)]
static public void ClearPickFirst()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      try
    {
        PromptSelectionResult result = ed.SelectImplied();
          if (result.Status != PromptStatus.OK)
            return;
          SelectionSet ss = result.Value;
        ObjectId[] ids = ss.GetObjectIds();
          ed.WriteMessage("Pick first has " +
                    ids.Length.ToString() + " entities");
          ObjectId[] newIds = new ObjectId[0];
          ed.SetImpliedSelection(newIds);
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.Message);
    }
}

## 评论

**内容**: Veli V. said...
Hi,
how this can be done in ObjectARX?
I have a problem to release dwg´s active pickfirst selectionset.
Cheers Veli V.
Reply
05/09/2012 at 05:53 AM

---
**内容**: Account Deleted said...
>>how this can be done in ObjectARX?
With help of acedSSSetFirst function.
Reply
05/09/2012 at 10:19 PM

---
**内容**: Domi said...
Hi Mr,
I am Vietnammese. Sorry for my English.
I have just been beginning with objectARX. I have some issues. Could you help me?
They are,
1. I have some polygons. when I click on an area, how can I know the area belongs to polygons? Which polygon?
2. How can I save a list of selected lines to be able to delete some lines in the list from a chose polygon? How about property ObjectId?
3. Can I detect all derived cycles with lines?
Thank you very much!
Best regards.
Reply
04/03/2015 at 09:00 PM

---
**内容**: Ajay said...
I've created an autocad plugin in .net. I've added one panel in autocad with the Commands called "Add Balloon".
I want the functionality like , when we select any dimension of drawing , and click on "Add Balloon" command button, it should do numbering of the dimensions in Multileader, like 1,2,3 ... in continuous ascending order and should do grouping of the dimension and its multileader numbering balloon.
Reply
06/11/2015 at 02:09 AM

---
