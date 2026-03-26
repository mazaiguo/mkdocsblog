---
title: "Inserting a DWF Underlay reference"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - Database
description: "DWF underlay’s are represented by the DwfDefinition and DwfReference classes in the AutoCAD .NET API. An Underlay Reference must reference compatib..."
author: Autodesk
---
# Inserting a DWF Underlay reference

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/inserting-a-dwf-underlay-reference.html

## 文章内容

By Virupaksha Aithal
DWF underlay’s are represented by the DwfDefinition and DwfReference classes in the AutoCAD .NET API. An Underlay Reference must reference compatible an underlay definition. The Underlay reference is responsible for the placement of the content within the drawing while Underlay Definition handles the linkage to the underlay content.
[CommandMethod("DWFInsert")]
static public void DWFInsert()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (Transaction tr =
                    db.TransactionManager.StartTransaction())
    {
          //first check for the required Layout
        UnderlayFile layouts = UnderlayHost.DwfHost.GetFile(
                                        "C:\\temp\\test.DWF", "");
        UnderlayItem selectedItem = null;
        foreach (UnderlayItem item in layouts.Items)
        {
            if (String.Compare(item.Name, "Model", true) == 0)
            {
                selectedItem = item;
                break;
            }
        }
         // if not found return;
        if(selectedItem == null)
        {
            ed.WriteMessage("error, No page with name Model");
            return;
        }
          DBDictionary nod = (DBDictionary)tr.GetObject(
                db.NamedObjectsDictionaryId, OpenMode.ForRead);
        string defDictKey = UnderlayDefinition.GetDictionaryKey(
                                            typeof(DwfDefinition));
          ObjectId defId = ObjectId.Null;
        if (!nod.Contains(defDictKey))
        {
            using (DBDictionary dict = new DBDictionary())
            {
                nod.UpgradeOpen();
                  defId = nod.SetAt(defDictKey, dict);
                tr.AddNewlyCreatedDBObject(dict, true);
            }
        }
        else
        {
            defId = nod.GetAt(defDictKey);
        }
          ObjectId idDef = ObjectId.Null;
        DBDictionary dwfDict = (DBDictionary)tr.GetObject(defId,
                                                 OpenMode.ForRead);
          if (dwfDict.Contains("Model"))
        {
            idDef = dwfDict.GetAt("Model");
        }
        else
        {
            using (DwfDefinition dwfDef = new DwfDefinition())
            {
                dwfDict.UpgradeOpen();
                dwfDef.SourceFileName = "C:\\temp\\test.DWF";
                dwfDef.SetUnderlayItem("C:\\temp\\test.DWF",
                                          "C:\\temp\\test.DWF",
                                               selectedItem);
                  idDef = dwfDict.SetAt("Model", dwfDef);
                tr.AddNewlyCreatedDBObject(dwfDef, true);
              }
        }
          using (DwfReference dwf = new DwfReference())
        {
            //add a reference
            dwf.DefinitionId = idDef;
            dwf.Position = new Point3d(10, 10, 0);
              ObjectId ModelSpaceId =
                SymbolUtilityServices.GetBlockModelSpaceId(db);
              BlockTableRecord model = tr.GetObject(ModelSpaceId,
                             OpenMode.ForWrite) as BlockTableRecord;
            model.AppendEntity(dwf);
            tr.AddNewlyCreatedDBObject(dwf, true);
        }
        tr.Commit();
      }
}

