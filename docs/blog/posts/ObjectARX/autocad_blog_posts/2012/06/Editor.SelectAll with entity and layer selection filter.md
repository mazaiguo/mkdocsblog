---
title: "Editor.SelectAll with entity and layer selection filter"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - Layer
  - Selection
description: "While using “Editor.SelectAll” API, you can provide “SelectionFilter” to filter out the unwanted entities. Below code shows a simple example which ..."
author: Autodesk
---
# Editor.SelectAll with entity and layer selection filter

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/editorselectall-with-entity-and-layer-selection-filter.html

## 文章内容

By Virupaksha Aithal
While using “Editor.SelectAll” API, you can provide “SelectionFilter” to filter out the unwanted entities. Below code shows a simple example which only gets the Lines and circles from a specified layer only (0, Layer1, Layer2).
[CommandMethod("LayerSelection")]
public void LayerSelection()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      TypedValue[] filterlist = new TypedValue[2];
    //select circle and line
    filterlist[0] = new TypedValue(0, "CIRCLE,LINE");
    //8 = DxfCode.LayerName
    filterlist[1] = new TypedValue(8, "0,Layer1,Layer2");
    SelectionFilter filter =
                            new SelectionFilter(filterlist);
      PromptSelectionResult selRes = ed.SelectAll(filter);
      if (selRes.Status != PromptStatus.OK)
    {
        ed.WriteMessage(
                    "\nerror in getting the selectAll");
        return;
    }
    ObjectId[] ids = selRes.Value.GetObjectIds();
      ed.WriteMessage("No entity found: "
                           + ids.Length.ToString() + "\n");
  }

## 评论

**内容**: Henk said...
I'm using ed.SelectAll and ed.Getselection a lot because of the speed of these methods.
When I debug my app with C# VS 2010 in AutoCAD 2013 the speed has reduced a lot. This is related to the number of objects in the drawing, large drawings will totally freeze my app.
Loading my (Debug as well as Release built) app in AutoCAD without debugging in VS solves it, the speed returned again. So publishing to my customers is no problem.
Did you notice this issue too with AutoCAD 2013?
Greetings,
Reply
07/04/2012 at 06:08 AM

---
**内容**: OCODER said...
I need to select graphical entities (MTexe exactly)inside a blockreference.
can i use the blockreference instead of layer in this example?
if no, can you help me?
thanks
Reply
01/08/2015 at 04:06 AM

---
**内容**: Virupaksha Aithal said in reply to OCODER...
Hi,
Sorry, you cannot use SelectAll API to select the nested (entity inside the block reference). You need to use GetNestedEntity API . refer http://adndevblog.typepad.com/autocad/2012/05/modifying-contents-of-a-picked-cell-inside-a-table.html
Thanks
Viru
Reply
01/08/2015 at 04:55 AM

---
**内容**: Ahmad said...
I need to select polylines which contains some specific name
What is the best way?
Reply
04/26/2015 at 12:15 AM

---
**内容**: kaan said...
Hi
I want to select last 3 entities.
Is it possible using filter?
Reply
06/17/2015 at 02:00 AM

---
**内容**: Jose Antonio mateos said...
Is there any way in selecting Entities by their ObjectId's?
Reply
06/14/2016 at 11:15 AM

---
