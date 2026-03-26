---
title: "Viewing LineType Appearance"
date: 2018-04-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "I have recieved this query, user would like to get appearance of LineTypeRecord or LineTypes through API."
author: Autodesk
---
# Viewing LineType Appearance

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/viewing-linetype-appearance.html

## 文章内容

By Madhukar Moogala
I have recieved this query, user would like to get appearance of LineTypeRecord or LineTypes through API.
We can use Comments API to gets the Linetype appearance in the form of ascii string.
Code:
public static void LineTypeAppearance()
        {
            Database database = HostApplicationServices.WorkingDatabase;
            var ed = AcCore.Application.DocumentManager.MdiActiveDocument.Editor;
            using (Transaction t = database.TransactionManager.StartTransaction())
            {
                var symTable = (SymbolTable)t.GetObject(database.LinetypeTableId,
                                                        OpenMode.ForRead);
                foreach (ObjectId id in symTable)
                {
                    var symbol = (LinetypeTableRecord)t.GetObject(id, OpenMode.ForRead);
                    ed.WriteMessage(string.Format("\nName: {0}\t Appearance: {1}",
                                                    symbol.Name, symbol.Comments));
                }

                t.Commit();
            }
        }
Output
Name: BYBLOCK   Desc:
Name: BYLAYER   Desc:
Name: CONTINUOUS      Desc: Solid line
Name: Wall Base|CENTER     Desc: Center ____ _ ____ _ ____ _ ____ _ ____ _ ____
Name: Wall Base|DASHED     Desc: Dashed __ __ __ __ __ __ __ __ __ __ __ __ __ _

## 评论

**内容**: badziewiak said...
Hello
Thank you for this example.
By the way: Is the line "t.Commit();" necessary in this case? We not making any changes.
Reply
01/11/2020 at 03:41 AM

---
