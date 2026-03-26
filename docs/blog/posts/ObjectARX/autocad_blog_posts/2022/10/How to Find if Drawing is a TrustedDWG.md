---
title: "How to Find if Drawing is a TrustedDWG"
date: 2022-10-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
description: "TrustedDWG is a key function of AutoCAD and AutoCAD LT that analyses DWG files as they are being opened. The function checks to see if the DWG file..."
author: Autodesk
---
# How to Find if Drawing is a TrustedDWG

发布日期: 2022-10-01

原始链接: https://adndevblog.typepad.com/autocad/2022/10/how-to-find-if-drawing-is-a-trusteddwg.html

## 文章内容

By Madhukar Moogala

TrustedDWG is a key function of AutoCAD and AutoCAD LT that analyses DWG files as they are being opened. The function checks to see if the DWG file was last saved with an Autodesk product or by a software developer who is licensed to use the RealDWG toolkit. If the file does not pass the TrustedDWG analysis, it will inform you in various ways that the DWG file may not be compatible, nor guarantee its integrity when used with AutoCAD or AutoCAD LT.
The visibility of these warnings is controlled by the DWGCHECK system variable. DWGCHECK is an integer variable, and is saved in the registry
When a drawing is not a TrustedDWG, and you open the drawing in AutoCAD or LT, you get this message or pop dialog.

Non Autodesk DWG. This DWG file was saved by a software application that was not developed or licensed by Autodesk. Autodesk cannot guarantee the application compatibility or integrity of this file.

Using API DwgFileWasSavedByAutodeskSoftware

        public void IsTrustedDWG()
        {
            Document doc = CoreApp.DocumentManager.MdiActiveDocument;
            if (doc == null) return;
            Editor ed = doc.Editor;
            var presult = ed.GetString(new PromptStringOptions("Enter Drawing File Path"));
            if (presult.Status != PromptStatus.OK) return;
            var db = HostApplicationServices.WorkingDatabase;
            Database sideDb = new Database(false, true);
            sideDb.ReadDwgFile(presult.StringResult, System.IO.FileShare.Read, true, null);
            HostApplicationServices.WorkingDatabase = sideDb;
            bool isTrustedDWG = sideDb.DwgFileWasSavedByAutodeskSoftware;
            if (isTrustedDWG)
            {
                ed.WriteMessage("Is Trusted DWG\n");
            }
            HostApplicationServices.WorkingDatabase = db;

        }

## 评论

**内容**: lunaterr said...
Thanks for the article on how to find out if a Drawing is TrustedDWG or not
Reply
11/21/2022 at 01:04 AM

---
**内容**: Hanfding said...
This topic is very interesting Sonic exe. It includes functions I'm getting a few minor errors here.
Reply
02/08/2023 at 07:19 PM

---
**内容**: backrooms said...
Pretty good article. I just stumbled across your blog and enjoyed reading your blog posts. I am looking for new articles to get more valuable information. Big thanks for this.
Reply
02/10/2023 at 01:33 AM

---
**内容**: JamesOneil said...
I just stumbled across your blog and enjoyed shell gas station near me
reading your blog posts. I am looking for new articles to ge.
Reply
02/27/2023 at 01:58 AM

---
**内容**: x trench run said...
Excellent article. I recently discovered your blog and have relished reading your blog posts. I'm searching for new articles to increase my knowledge.
Reply
04/09/2023 at 07:45 PM

---
**内容**: gacha life said...
Thank you for providing this information. I am delighted to come on this fantastic article.
Reply
07/25/2023 at 08:30 PM

---
**内容**: Headphoneuk said...
Ensuring the integrity of DWG files is crucial for smooth workflow in AutoCAD and AutoCAD LT. TrustedDWG feature acts as a gatekeeper, verifying if the file meets Autodesk standards. Understanding DWGCHECK and being aware of warnings like "Non Autodesk DWG" can help maintain compatibility and file integrity.
Reply
05/07/2024 at 08:30 AM

---
**内容**: fnaf said...
If it was saved by Autodesk software, it is considered a TrustedDWG, and the function will output "Trusted DWG".
Reply
05/21/2024 at 01:52 AM

---
