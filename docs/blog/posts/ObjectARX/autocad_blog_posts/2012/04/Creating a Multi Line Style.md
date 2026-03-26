---
title: "Creating a Multi Line Style"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - Database
  - Plugin
description: "Multi line style is stored in the named object Dictionary. You can get the Multi line named object Dictionary id using “Database::MLStyleDictionary..."
author: Autodesk
---
# Creating a Multi Line Style

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/creating-a-multi-line-style.html

## 文章内容

By Virupaksha Aithal
Multi line style is stored in the named object Dictionary. You can get the Multi line named object Dictionary id using “Database::MLStyleDictionaryId” property.
Below codes demonstrates the adding a new Multi line style to the Multi line Style dictionary.
[CommandMethod("createmlinestyle")]
public void createmlinestyle()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor editor = doc.Editor;
    Database db = doc.Database;
    using (Transaction Tx =
        db.TransactionManager.StartTransaction())
    {
          DBDictionary mlineDic =
            (DBDictionary)Tx.GetObject(db.MLStyleDictionaryId,
                                              OpenMode.ForRead);
        if (!mlineDic.Contains("TEST"))
        {
            mlineDic.UpgradeOpen();
            MlineStyle mlineStyle = new MlineStyle();
            mlineDic.SetAt("TEST", mlineStyle);
            Tx.AddNewlyCreatedDBObject(mlineStyle, true);
              mlineStyle.EndAngle = 3.14159 * 0.5;
            mlineStyle.StartAngle = 3.14159 * 0.5;
            mlineStyle.Name = "TEST";
            Autodesk.AutoCAD.Colors.Color Color;
            Color =
                Autodesk.AutoCAD.Colors.Color.FromRgb(255, 0, 0);
              MlineStyleElement element =
                    new MlineStyleElement(0.25,
                                        Color,
                                         db.Celtype);
            mlineStyle.Elements.Add(element, true);
            element =
                    new MlineStyleElement(-0.25,
                                        Color,
                                        db.Celtype);
              mlineStyle.Elements.Add(element, false);
        }
          Tx.Commit();
    }
}

