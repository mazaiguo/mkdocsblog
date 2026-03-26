---
title: "Setting layer transparency"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Forge
  - Layer
description: "Layers can be assigned a transparency value using the AutoCAD's layer dialog."
author: Autodesk
---
# Setting layer transparency

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/setting-layer-transparency.html

## 文章内容

By Balaji Ramamoorthy
Layers can be assigned a transparency value using the AutoCAD's layer dialog.
Here is sample code to show you how a similar result can be achieved using the AutoCAD .Net API.
But before trying this code, dont forget to set the "TRANSPARENCYDISPLAY" system variable to 1.
[CommandMethod("Test")]
public void TestMethod()
{
SetLayerTransparency("Autodesk", 50);
}
  /// sets the layer transparency
// Can range from 0 (opaque) to 90 (almost transparent)
/// returns ObjectId of the layer
private ObjectId SetLayerTransparency
(
string layerName,
Byte layerTransparency
)
{
Document activeDoc
= Application.DocumentManager.MdiActiveDocument;
  Database db = activeDoc.Database;
ObjectId layerId = ObjectId.Null;
bool done = false;
  using (Transaction tr
= db.TransactionManager.StartTransaction())
{
LayerTable lt
= tr.GetObject
(
db.LayerTableId,
OpenMode.ForRead
) as LayerTable;
  if (lt.Has(layerName))
{
layerId = lt[layerName];
LayerTableRecord ltr
= tr.GetObject(
layerId,
OpenMode.ForWrite
) as LayerTableRecord;
  // The color is being set here to ensure that
// a regen will consider redrawing all the entities
// belonging to this layer.
ltr.Color = ltr.Color;
  Byte alpha = (Byte)
(255 * (100 - layerTransparency) / 100);
Transparency trans = new Transparency(alpha);
  ltr.Transparency = trans;
done = true;
}
tr.Commit();
}
  if (done)
{
RefreshEntities(layerId);
// (OR)
//activeDoc.Editor.Regen();
}
  return layerId;
}
  // Marks the entities referencing a
// certain layer as "Modified"
private void RefreshEntities(ObjectId layerId)
{
Document activeDoc =
Application.DocumentManager.MdiActiveDocument;
  Database db = activeDoc.Database;
using (Transaction tr =
db.TransactionManager.StartTransaction())
{
BlockTable bt = tr.GetObject
(
db.BlockTableId,
OpenMode.ForRead
) as BlockTable;
  BlockTableRecord btr =
tr.GetObject
(
bt[BlockTableRecord.ModelSpace],
OpenMode.ForRead
) as BlockTableRecord;
  foreach (ObjectId entityId in btr)
{
Entity ent
= tr.GetObject
(
entityId,
OpenMode.ForRead
) as Entity;
  if (ent.LayerId.Equals(layerId))
{
ent.UpgradeOpen();
ent.RecordGraphicsModified(true);
}
}
tr.Commit();
}

## 评论

**内容**: Tom said...
no TRANSPARENCYDISPLAY variable in autocad 2008
Reply
10/07/2012 at 11:00 PM

---
**内容**: Alexander Rivilis said in reply to Tom...
TRANSPARENCYDISPLAY variable can be using since AutoCAD 2011
Reply
10/07/2012 at 11:45 PM

---
**内容**: Gerrit van Diepen said...
Hi everyone,
From an entity it is possible to read entity.Transparency.IsByLayer
How can I set the value of the Transparency of an entity to Bylayer
I presume it is not the same as:
Dim factor as byte = Cbyte(255 * (100 - 0) / 100)
Dim acTrsprcy as Colors.Transparency = New Colors.transparency(factor)
entity.Transparency = acTrsprcy '' is transparency 0
Reply
03/26/2015 at 07:08 AM

---
