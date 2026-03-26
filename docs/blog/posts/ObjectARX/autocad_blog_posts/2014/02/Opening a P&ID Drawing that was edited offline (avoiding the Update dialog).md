---
title: "Opening a P&ID Drawing that was edited offline (avoiding the Update dialog)"
date: 2014-02-01
categories:
  - AutoCAD .NET
tags:
  - API
  - C#
  - DWG
  - Database
  - SQL
description: "A drawing that was edited offline has to be re-inserted (merged) into the project. Plant drawings contain subset of project database (BLOB as SQL d..."
author: Autodesk
---
# Opening a P&ID Drawing that was edited offline (avoiding the Update dialog)

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/opening-a-pid-drawing-that-was-edited-offline-avoiding-the-update-dialog.html

## 文章内容

By Wayne Brill
A drawing that was edited offline has to be re-inserted (merged) into the project. Plant drawings contain subset of project database (BLOB as SQL database). Plant also a knows whether the drawing was saved in the current project or not. If drawing was not saved in the current project, the BLOB has to be merged into the project.
There are several API to handle this situation:
Project.IsDrawingOutOfSync(string dwgname, Database db) – tells whether AcDbDatabase is in sync with project database
Project.UpdatePnPDrawing(Database db, string dwgname, ref PnPSyncConflicts conflicts) – merge blob into project database.
C# example:
[CommandMethod("testOpen", CommandFlags.Session)]
public void testOpen()
{
    string strDwgPath;
    Database db = new Database(false, true);
      Project currentProject =
        PlantApp.CurrentProject.ProjectParts["PnId"];
    DataLinksManager dlm =
                     currentProject.DataLinksManager;
      // get project drawing 
    PnPProjectDrawing pnp_dwg =
        currentProject.GetDwgFileByName
        ("C:\\MyProject\\PID DWG\\PumpAnlage.dwg");
      // use resolved path
    strDwgPath = pnp_dwg.ResolvedFilePath;
        db.ReadDwgFile(strDwgPath,
                FileShare.ReadWrite, false, null);
    // tell DLM to manage drawing database.
    //(Documents are automatically enlisted
    //when they are opened in editor)
    dlm.EnlistDrawing(db);
    // dispose will unelist it
      if (currentProject.IsDrawingOutOfSync
                              (strDwgPath, db))
    {
          PnPSyncConflicts conflicts = null;
        currentProject.UpdatePnPDrawing
                (db, strDwgPath, ref conflicts);
        // tell DLM that drawing related data has to
        // be saved in the project database.
        // otherwise, DLM will not save drawing sync
        // timestamp causing out-of-sync
        // situation on drawing open
      DataLinksManager.DatabaseToForceSaveComplete
                                             = db;
        try
        {
            db.SaveAs(strDwgPath, DwgVersion.Current);
        }
        catch (System.Exception ex)
        {
          }
        finally
        {
          DataLinksManager.DatabaseToForceSaveComplete
                                               = null;
          }
    }
        db.CloseInput(true);
    db.Dispose();
      DocumentCollection acDocMgr =
                         Application.DocumentManager;
      Document acDoc = acDocMgr.Open(strDwgPath, false);
      AcadDocument anAcadDoc =
               (AcadDocument)acDoc.GetAcadDocument();
    // if(!anAcadDoc.Saved)
        anAcadDoc.Save();
  }

## 评论

**内容**: dario said...
hello Augusto
My name is Dario (Brazil)
I need help please

insert a block and catch sequence data of this block
how to get the data inserted block properties, insertion point, extended data layer, rotation, color etc. ..
and then delete this block

[CommandMethod("Block")]
public void block()
{
doc = Host.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
string[] Dados = new string[3];
Dados[0] = "dado 1";
Dados[1] = "dado 2";
Dados[2] = "dado 3";
BlockReference br = CadGlobal.InsertBlockFromFile(doc, @"C:\wbc\orienta.dwg", new Point3d(50, 50, 50), Math.PI * 0.25,
"wbc_insert" , Dados, 30, 30, 1, 7, true, null, "wbcd");
help example:????
???? br.insertioPoint
???? br.rotation
???? br.layerName
???? br.Xpropierts[0]

???? br.Erase();
}
-------------------------------------------------
Augusto .. favor enviar para dariowbc@terra.com.br
Muito grato
Reply
03/06/2014 at 06:31 AM

---
**内容**: Wayne Brill said...
Hello Dario,
You may want to post this question in the Discussion group. (It does not seem related to this post regarding P&ID)
http://forums.autodesk.com/t5/NET/bd-p/152
The AutoCAD .NET training (Lab 4) covers events. (ObjectAppended) This event would fire when a BlockReference is added to the drawing.
http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=1911627
This site also has several posts about BlockReferences.
Thanks,
Wayne
Reply
03/06/2014 at 09:01 AM

---
**内容**: Martin Buss said...
Hi Wayne,
why do you open and save the document finally?
I tried without and the database got updated.
And when opening the file by project manager Plant doesn't ask for updating the data.
Everything nice..
Thank you
Martin
Reply
04/07/2017 at 02:58 AM

---
**内容**: Martin Buss said...
ok, I can answer myself.. It looks everything nice in the database, but it is not saved in the drawing. When we open the project again, all synchronization work got lost. Thank you anyway for the article.
Reply
04/07/2017 at 06:26 AM

---
**内容**: Divz said...
Hi, I have almost tried the se but I am getting same message as edited offline please update project data or review changes please let me know
Reply
03/04/2020 at 12:03 PM

---
