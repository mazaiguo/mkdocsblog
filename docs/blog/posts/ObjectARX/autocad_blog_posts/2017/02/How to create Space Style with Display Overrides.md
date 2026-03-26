---
title: "How to create Space Style with Display Overrides"
date: 2017-02-01
categories:
  - AutoCAD
tags:
  - API
  - Plot
description: "We have received  this query from one of our ADN publisher, I’m blogging it for benefit every developer."
author: Autodesk
---
# How to create Space Style with Display Overrides

发布日期: 2017-02-01

原始链接: https://adndevblog.typepad.com/autocad/2017/02/how-to-create-space-style-with-display-overrides.html

## 文章内容

By Madhukar Moogala
We have received  this query from one of our ADN publisher, I’m blogging it for benefit every developer.
Thanks to Amod for helping me out. As I’m fairly new to OMF and >NET API for ACA_MEP.
The following code is self explanatory.
public static void PrintToCmdLine(string str)
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    ed.WriteMessage(str);
}
[CommandMethod("createSpaceStyle")]
public static void createSpaceStyle()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
    try
    {
        using (Transaction trans = db.TransactionManager.StartTransaction())
        {
            Autodesk.Aec.Arch.DatabaseServices.DictionarySpaceStyle dict =
             new DictionarySpaceStyle(db);
            // space style
            string stylename = "My_SpaceStyle";
            Autodesk.Aec.Arch.DatabaseServices.SpaceStyle style = 
            new SpaceStyle();
            //Append To DB
            style.SetToStandard(db);
                   
            /*Check*/
            if (dict.Records.IndexOf(style.ObjectId) == -1)
            {
                dict.AddNewRecord(stylename, style);
                trans.AddNewlyCreatedDBObject(style, true);
                /*How to Add overrides to Style */
                DisplayRepresentationManager dispRepMg = 
                 new DisplayRepresentationManager();
                Autodesk.AutoCAD.DatabaseServices.ObjectId dispRepsDictId = 
                  dispRepMg.DisplayRepresentationsDictionaryId;
                DBDictionary dispRepsDict = 
                  (DBDictionary)trans.GetObject(dispRepsDictId, OpenMode.ForWrite, false);
                Autodesk.AutoCAD.DatabaseServices.ObjectId dispRepId = 
                   dispRepsDict.GetAt("AecDbDispRepSpaceModel");
                DisplayRepresentation dispRep = 
                trans.GetObject(dispRepId, OpenMode.ForWrite, false) as DisplayRepresentation;

                Autodesk.AutoCAD.DatabaseServices.ObjectId DispPropId = 
                  dispRep.DefaultDisplayPropertiesId;
                OverrideDisplayProperties ovr = new OverrideDisplayProperties();
                ovr.SubSetDatabaseDefaults(db);
                ovr.SetToStandard(db);
                ovr.DisplayPropertyId = DispPropId;
                ovr.ViewId = dispRepId;
                style.Overrides.Add(ovr);
            }
            /*Access Display Overides*/
            for (int c = 0; c < style.Overrides.Count; c++)
            {
                Override ovr = style.Overrides[c];
                OverrideDisplayProperties odp = 
                            (OverrideDisplayProperties)ovr;
                if (odp != null)
                {
                    string str = "Space style " + 
                                style.Name +
                                " has display overrides\n";
                    PrintToCmdLine(str);
                }
            }                 
                    
            trans.Commit();
        }
    }
    catch (System.Exception ex)
    {
        ed.WriteMessage(ex.ToString());
    }

           
    }
  Please find our style residing STYLEMANAGER:

