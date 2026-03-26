---
title: "Retrieving global name of DIMLDRBLK in Localized versions of AutoCAD"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "When using English version of AutoCAD, you can directly retrieve the name of arrow head using DIMLDRBLK system variable. But when using localized v..."
author: Autodesk
---
# Retrieving global name of DIMLDRBLK in Localized versions of AutoCAD

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/retrieving-global-name-of-dimldrblk-in-localized-versions-of-autocad.html

## 文章内容

By Balaji Ramamoorthy
When using English version of AutoCAD, you can directly retrieve the name of arrow head using DIMLDRBLK system variable. But when using localized versions of AutoCAD, this system variable will hold the localized name such as "Punkt" in German for DOT arrow head.
To get the global name even in the localized versions, here is a small code snippet to retrieve it :
 Document doc 
  = Application.DocumentManager.MdiActiveDocument;
 Editor ed = doc.Editor;
   using  (Transaction tr 
  = doc.TransactionManager.StartTransaction())
 {
     DimStyleTableRecord dstr = db.GetDimstyleData();
     ObjectId dimldrblkId = dstr.Dimldrblk;
     if  (!dimldrblkId.IsNull)
     {
         BlockTableRecord btr = tr.GetObject(
    dimldrblkId, 
    OpenMode.ForRead) as BlockTableRecord;
         if  (btr != null)
         {
             ed.WriteMessage(btr.Name);
         }
     }
     tr.Commit();
 }

## 评论

**内容**: Nad said...
Hi,
I thought you might be interested to learn that there’s a first ever AEC application with the Oculus integration in development, and you might want to try it yourself. My team is finalizing the integration now, and we’d be happy to provide you with such an opportunity. The app will allow AEC professionals and their clients to explore building design and construction projects in a truly immersive virtual reality. Please reach me via n.bauman@revizto.com if you’re interested in details.
Cheers!
Reply
01/28/2015 at 08:48 PM

---
**内容**: Andrey Bushman said...
What reason for this language-depending naming of DIMLDRBLK variable?
Reply
02/08/2015 at 11:29 PM

---
**内容**: Balaji said...
Hi Andrey,
Sorry, I am not aware of the reason behind it.
But it could be that the names of the blocks indicate the shape such as DOT, so it might make sense to have them in local language for users to quickly recognize.
Regards,
Balaji
Reply
02/09/2015 at 09:07 PM

---
