---
title: "Generate Layer usage data before purge/delete"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Layer
description: "It can sometimes happen that a layer does not get purged and the "IsUsed" property of this layer table record returns true even though the layer is..."
author: Autodesk
---
# Generate Layer usage data before purge/delete

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/generate-layer-usage-data-before-purgedelete.html

## 文章内容

By Balaji Ramamoorthy
It can sometimes happen that a layer does not get purged and the "IsUsed" property of this layer table record returns true even though the layer is not being used. The reason for this is that, AutoCAD maintains a usage data for all the layer table records which is only refreshed when needed. To force an update of the usage data, the "GenerateUsageData" method of the LayerTable is to be used.
Here is a sample code to try and delete layer table records after the call to "GenerateUsageData".
[CommandMethod("Test")]
public void TestMethod()
{
    Document document
            = Application.DocumentManager.MdiActiveDocument;
    Database db = document.Database;
      using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        LayerTable lt = tr.GetObject(
                                        db.LayerTableId,
                                        OpenMode.ForRead
                                    ) as LayerTable;
        lt.GenerateUsageData();
        foreach (ObjectId oid in lt)
        {
            LayerTableRecord ltr = tr.GetObject
                                            (
                                                oid,
                                                OpenMode.ForRead
                                            ) as LayerTableRecord;
            if (ltr.IsUsed == false)
            {
                ltr.UpgradeOpen();
                ltr.Erase();
            }
        }
        tr.Commit();
    }
}

