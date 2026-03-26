---
title: "Accessing Drawing Standards File (.dws)"
date: 2017-05-01
categories:
  - AutoCAD
tags:
  - Layer
description: "I had a chance to explore on this, when I came across a query in forum."
author: Autodesk
---
# Accessing Drawing Standards File (.dws)

发布日期: 2017-05-01

原始链接: https://adndevblog.typepad.com/autocad/2017/05/accessing-drawing-standards-file-dws.html

## 文章内容

By Madhukar Moogala
I had a chance to explore on this, when I came across a query in forum.
When user invokes “LAYTRANS”, a layer translator dialog gets popped up and user is allowed to translate the layers from a loaded drawing to current drawing.
layers from loaded drawing are mapped to layers in current drawing or mapping can be set up by an user.
This setup can be saved as standards file (.dws), for future use when user receives a drawing from a customer, user can check if drawing complies with said standards files.
The standards file holds the layer translation mapping information in an extended data of each layers that has been mapped or translated.
For example, the attached file, has a mapping information between layers A,B,C wrt 1,2,3. Where A,B,C layers of standard drawing(source) which will be translated to layers 1,2,3 of current drawing (destination)
Reading dws is same as like reading a drawing file, this is a file with different extension. (Thanks to Lee for the tip).
public static void tstreadDws()
        {
            // save old database
            Database oldDb = HostApplicationServices.WorkingDatabase;
            Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;

            // when using ReadDwgFile, never specify True to buildDefaultDwg
            // also, set noDocument=True because this drawing has no
            // AutoCAD Document associated with it
            using (Database db = new Database(false, true))
            {
                db.ReadDwgFile("D:\\Temp\\MyStandard.dws", FileOpenMode.OpenForReadAndWriteNoShare, true, "");
                // closing the input makes sure the whole dwg is read from disk
                // it also closes the file so you can SaveAs the same name
                db.CloseInput(true);
                string appName = "ACLAYTRANS";               
                string msg = "LAYER TRANSLATION MAPPING:\n";

                // ok time to set the working database

                HostApplicationServices.WorkingDatabase = db;
                using (Transaction t = db.TransactionManager.StartTransaction())
                {
                    LayerTable lt = t.GetObject(db.LayerTableId, OpenMode.ForRead) as LayerTable;
                    foreach(ObjectId oId in lt)
                    {
                        LayerTableRecord ltr = t.GetObject(oId, OpenMode.ForRead) as LayerTableRecord;
                        
                        ResultBuffer rb = ltr.GetXDataForApplication(appName);
                        if (rb != null)
                        {
                            string layerName = ltr.Name;
                            // Get the values in the xdata
                            foreach (TypedValue typeVal in rb)
                            {
                             
                                if(typeVal.TypeCode == 1000)
                                {
                                    msg = msg + layerName + ":" + typeVal.Value +"\n";
                                }
                            }
                        }
                        

                    }
                    t.Commit();
                }
                ed.WriteMessage(msg);
                // reset it back ASAP
              HostApplicationServices.WorkingDatabase = oldDb;
                
            }

        }
  Output:
LAYER TRANSLATION MAPPING:
A:1
B:2
C:3

## 评论

**内容**: BKSpurgeon said...
very interesting! thanks for sharing.
Reply
11/15/2017 at 03:13 PM

---
