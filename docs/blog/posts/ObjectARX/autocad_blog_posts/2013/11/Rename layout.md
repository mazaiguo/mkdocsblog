---
title: "Rename layout"
date: 2013-11-01
categories:
  - AutoCAD
tags:
  - Database
description: "You can use LayoutManager class function RenameLayout to rename the layouts. Below code shows simple example showing the renaming of the layout."
author: Autodesk
---
# Rename layout

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/rename-layout.html

## 文章内容

By Virupaksha Aithal
You can use LayoutManager class function RenameLayout to rename the layouts. Below code shows simple example showing the renaming of the layout.
[CommandMethod("RenameLayout")]
static public void renamelayoutName()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      //get the Layout name
    PromptStringOptions opts =
       new PromptStringOptions("Enter Layout name to change");
    opts.AllowSpaces = true;
      PromptResult layoutName = ed.GetString(opts);
      if (layoutName.Status != PromptStatus.OK)
        return;
      bool bUpdate = false;
    using (Transaction tr =
                    db.TransactionManager.StartTransaction())
    {
        DBDictionary dLayouts = tr.GetObject(db.LayoutDictionaryId,
                          OpenMode.ForRead) as DBDictionary;
          if (dLayouts.Contains(layoutName.StringResult))
        {
            bUpdate = true;
        }
          tr.Commit();
      }
      if (bUpdate)
    {
        LayoutManager acLayoutMgr = LayoutManager.Current;
        acLayoutMgr.RenameLayout(layoutName.StringResult,
                    layoutName.StringResult + " - modified");
          doc.Editor.Regen();
    }
    else
    {
        ed.WriteMessage("No Layout with name "
                + layoutName.StringResult);
    }
}

## 评论

**内容**: JamesOneil said...
An automatic skill is firm and approached for the citizens. The effective use of the game grid 2
for thk offers. Method is inclined for the team work. Value is done for the reformed tip by all issues for the certificate options by all major s signs for the team.
Reply
08/07/2023 at 02:01 AM

---
**内容**: tiny games said...
Thanks for this article! I read it and try
Reply
08/09/2023 at 08:05 PM

---
