---
title: "Adding a new layer and making it current layer"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - Database
  - Layer
  - Plugin
description: "Below sample code shows the procedure to add a new layer. All layers are stored in a symbol table called layer table. To make any layer as current ..."
author: Autodesk
---
# Adding a new layer and making it current layer

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/adding-a-new-layer-and-making-it-current-layer.html

## 文章内容

By Virupaksha Aithal
Below sample code shows the procedure to add a new layer. All layers are stored in a symbol table called layer table. To make any layer as current layer, set the Database property Clayer with the object id of the layer.
[CommandMethod("AddLayer")]
public void AddLayer()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        LayerTable ltb = (LayerTable)tr.GetObject(db.LayerTableId,
                                                  OpenMode.ForRead);
        //create a new layout.
        if (!ltb.Has("NewLayer"))
        {
            ltb.UpgradeOpen();
            LayerTableRecord newLayer = new LayerTableRecord();
            newLayer.Name = "NewLayer";
              newLayer.LineWeight = LineWeight.LineWeight005;
            newLayer.Description = "This is new layer";
              //red color
            newLayer.Color =
                    Autodesk.AutoCAD.Colors.Color.FromRgb(255, 0, 0);
              ltb.Add(newLayer);
            tr.AddNewlyCreatedDBObject(newLayer, true);
        }
          tr.Commit();
        //make it as current
        db.Clayer = ltb["NewLayer"];
    }
  }

## 评论

**内容**: Matus Brlit said...
Just a note:
When I don't need the editor object, like in this case, I obtain the Database object from HostApplicationServices.WorkingDatabase because it's thread-safe.
Obtaining it this way is not.
Reply
06/22/2012 at 04:48 AM

---
**内容**: Owen Wengerd said in reply to Matus Brlit...
When a user runs a command, they expect it to use the database for the document running the command, which is not necessarily the working database.
Reply
06/22/2012 at 10:16 AM

---
**内容**: Artvegas said...
The layer Description property doesn't seem to get set to. Didn't work in either 2012 or 2013. Reading user-defined layer description worked ok.
What's up with that?
Reply
08/03/2012 at 09:31 AM

---
**内容**: Nikhil Ruikar said...
The above written code works fine when I am creating a single layer. It fails when creating multiple layers.
Here's my code which fails at,
LayerTable layerTable = (LayerTable)this.transaction.GetObject(this.database.LayerTableId, OpenMode.ForRead);
Code:
/////////////////////////////////////////////////////////////////////////////////////////////
foreach (LayerAttributeColor item in layerColorAttributeValues)
{
LayerTable layerTable = (LayerTable)this.transaction.GetObject(this.database.LayerTableId, OpenMode.ForRead);
if (!layerTable.Has(item.LayerName))
{
LayerTableRecord ltr = new LayerTableRecord();
// ... and set its properties
ltr.Name = item.LayerName;
ltr.Color = Autodesk.AutoCAD.Colors.Color.FromRgb(255, 0, 0);
// Add the new layer to the layer table
layerTable.UpgradeOpen();
ObjectId ltId = layerTable.Add(ltr);
layerTable.DowngradeOpen();
this.transaction.AddNewlyCreatedDBObject(ltr, true);
// Set the layer to be current for this drawing
//this.database.Clayer = ltId;
// Commit the transaction
this.transaction.Commit();
ltr.Dispose();
}
}
/////////////////////////////////////////////////////////////////////////////////////////////
The exception message reads as,
"Operation is not valid due to the current state of the object".
Please advise.
Reply
02/01/2018 at 12:03 AM

---
**内容**: Deepika said...

Use TrueCAD-intellicad Software.One of the best AutoCAD alternative cad software at affordable price. here is reference link "https://actcad.com/download-actcad-intellicad-software.php"
Reply
05/05/2021 at 03:16 AM

---
**内容**: Eva said...
The best part of using CMS IntelliCAD was finding out it has all the CAD features I’d already worked with. I was pretty worried about finding a good fit for me, but CMS IntelliCAD is definitely unbeatable. Registered for free and had a free trial before payment, I'm glad I could test it out before any payment. CMS IntelliCAD is definitely worth the hype.
Reply
03/25/2022 at 08:31 AM

---
**内容**: Sona said...
Was a bit hesitant to try at first but CMS IntelliCAD turned out to be a good alternative for me. The free trial worked immediately, which was good to try it out before paying for it. All the features it offers are user-friendly and easy to work with, which was another win for me. Good job.
Reply
03/28/2022 at 08:50 AM

---
**内容**: Nataly said...
I've been using CADHOBBY IntelliCAD for my personal projects for a few months now, and I can say that it's one of the best CAD software for hobbyists. It's user-friendly, and the learning curve is not steep.
Reply
04/08/2023 at 10:21 AM

---
