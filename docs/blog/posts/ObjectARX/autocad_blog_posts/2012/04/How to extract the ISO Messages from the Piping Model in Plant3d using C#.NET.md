---
title: "How to extract the ISO Messages from the Piping Model in Plant3d using C#.NET"
date: 2012-04-01
categories:
  - Plant 3D
tags:
  - .NET
  - C#
  - Plant 3D
description: "Extracting the ISO Messages from the Plant3d Piping model is fairly straight forward to do. I think probably the best (easiest) way to do it is to ..."
author: Autodesk
---
# How to extract the ISO Messages from the Piping Model in Plant3d using C#.NET

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/how-to-extract-the-iso-messages-from-the-piping-model-in-plant3d-using-cnet.html

## 文章内容

By Fenton Webb
Extracting the ISO Messages from the Plant3d Piping model is fairly straight forward to do. I think probably the best (easiest) way to do it is to use a SS Selection Filter to select only those objects that are DXF Code ACPPDB3DISOSPHERESYMBOL then extract the ISO Message from the Extension Dictionary entry PnP3dMsg.
Here’s the code
// list Iso Messages in model space, by Fenton Webb, DevTech, Autodesk, 16/4/2012
[CommandMethod("listIsosMS", CommandFlags.NoPaperSpace)]
public void listIsosMS()
{
  // get the AutoCAD Editor object
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    // create a ss get filter
  TypedValue[] filter = new TypedValue[] { new TypedValue((int)DxfCode.Start, "ACPPDB3DISOSPHERESYMBOL") };
  // now select them from model space
  SelectionFilter sf = new SelectionFilter(filter);
  PromptSelectionResult psr = ed.SelectAll(sf);
  // if success
  if (psr.Status == PromptStatus.OK)
  {
    ed.WriteMessage("\nFound {0} Iso Message entit{1}.", psr.Value.Count, (psr.Value.Count == 1 ? "y" : "ies"));
    foreach (ObjectId id in psr.Value.GetObjectIds())
    {
      // open the entity for read
      using (Entity ent = id.Open(OpenMode.ForRead) as Entity)
      {
        // see if the extensiuon dictionary is valid
        if (ent.ExtensionDictionary.IsValid == true)
        {
          // open the extension dict
          using (DBDictionary extDict = ent.ExtensionDictionary.Open(OpenMode.ForRead) as DBDictionary)
          {
            // see if the PnP3dMsg is there
            if (extDict.Contains("PnP3dMsg") == true)
            {
              // get at the PnP3dMsg entry
              using (Xrecord xrec = extDict.GetAt("PnP3dMsg").Open(OpenMode.ForRead) as Xrecord)
              {
                // now find the text
                foreach (TypedValue val in xrec.Data)
                {
                  if (val.TypeCode == 1)
                  {
                    ed.WriteMessage("\nISO Message Text=" + val.Value.ToString());
                    break;
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
  However, in the ISOMetric drawings, those ISO messages are just raw AutoCAD Blocks. Therefore, you will need to search all BlockReferences for an Attribute name of 'XX', from the 'XX' attribute property you can extract the ISO message text.

## 评论

**内容**: matin said...
Dear Fenton
I want to get nozzle attribute of created equipment in autocad plant 3d.
I want to get X coordinate (Port 1) of nozzle. Please Help!
public static void Test()
{
Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
using (EquipmentHelper eqHelper = new EquipmentHelper())
{
PromptEntityResult res = ed.GetEntity("\nSelect equipment entity: ");
ObjectId eqId = res.ObjectId;
EquipmentType eq = eqHelper.RetrieveEquipmentFromInstance(eqId);
foreach (CategoryInfo categoryInfo in eq.Categories)
{
ed.WriteMessage("\n" + categoryInfo.DisplayName);
foreach (ParameterInfo parameterInfo in categoryInfo.Parameters)
{
ed.WriteMessage("\n\t" + parameterInfo.Name + ";" + parameterInfo.Value);
}
}

foreach (NozzleInfo nozzleInfo in eq.Nozzles)
{
ed.WriteMessage("\n\n"
+ "Display Name:" + nozzleInfo.DisplayName + ";\n"
+ "End Type:" + nozzleInfo.EndType + ";\n"
+ "Facing:" + nozzleInfo.Facing + ";\n"
+ "Long Desc.:" + nozzleInfo.LongDescription + ";\n"
+ "Name:" + nozzleInfo.Name + ";\n"
+ "Nozzle End Type:" + nozzleInfo.NozzleEndType + ";\n"
+ "Nozzle Size:" + nozzleInfo.NozzleSize + ";\n"
+ "Pressure Class:" + nozzleInfo.PressureClass + ";\n"
+ "Port Name:" + nozzleInfo.PortName + ";\n"
+ "Port Index:" + nozzleInfo.PortIndex + ";\n"
+ "nozzle Tag:" + nozzleInfo.NozzleTag + ";\n"
+ "Object:" + nozzleInfo + ";\n"
+ "Part Size Record ID:" + nozzleInfo.PartSizeRecordId + ";\n"
+ "Part Sub Type:" + nozzleInfo.PartSubType);
}

}

}
Best Regards
Reply
01/03/2017 at 12:19 AM

---
