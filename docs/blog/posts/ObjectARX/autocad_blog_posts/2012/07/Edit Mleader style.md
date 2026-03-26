---
title: "Edit Mleader style"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Database
  - Unicode
description: "Mleaderstyle objects are stored in the named object dictionary of the drawing database. Database object exposes an objectId “MLeaderStyleDictionary..."
author: Autodesk
---
# Edit Mleader style

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/edit-mleader-style.html

## 文章内容

By Virupaksha Aithal
Mleaderstyle objects are stored in the named object dictionary of the drawing database. Database object exposes an objectId “MLeaderStyleDictionaryId” to access this dictionary. Below code shows the procedure to edit a Mleader style.   Below code edits only the mleader style’s text height and color, but  Mleaderstyle object exposes many more properties to edit like “ArrowSymbolId”, “ArrowSize” “LandingGap” & etc.
[CommandMethod("EditMleaderStyle")]
static public void EditMleaderStyle()
{
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr =
                       db.TransactionManager.StartTransaction())
    {
        //Name of the mleader Style to edit
        const string styleName = "Standard";
          DBDictionary mlstyles = (DBDictionary)tr.GetObject(
                                        db.MLeaderStyleDictionaryId,
                                        OpenMode.ForRead);
          if (!mlstyles.Contains(styleName))
        {
            return;
        }
        ObjectId id = mlstyles.GetAt(styleName);
          //now get the active mleader style
        MLeaderStyle currentStyle = tr.GetObject(id,   
                                OpenMode.ForWrite) as MLeaderStyle;
          //now edit the style
        currentStyle.TextColor =
                    Autodesk.AutoCAD.Colors.Color.FromRgb(255, 0, 0);
          //just double the text height
        currentStyle.TextHeight = currentStyle.TextHeight * 2;
          tr.Commit();
    }
}

## 评论

**内容**: sybold said...
this works for textheight, color, and most other properties, but setting the scale doesn't work. how can that be done.
the value does not transfer to the mleader when changed in the style.
Reply
07/11/2012 at 01:55 AM

---
**内容**: nav said...
Hi
How we change Style to block and block source to Box.
thanks
Reply
06/03/2014 at 01:57 AM

---
**内容**: TY NGUYEN said...
Hi all guys!
Can we purge MleaderStyle not use in drawing by CAD.net?
Reply
11/09/2016 at 01:02 AM

---
