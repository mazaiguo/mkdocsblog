---
title: "Accessing And Changing The AutoCAD Preferences"
date: 2013-02-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - COM
  - VBA
description: "This could be done by manipulating the AutoCAD registry directly, or by using the AutoCAD Preferences ActiveX object. Note that if you make a chang..."
author: Autodesk
---
# Accessing And Changing The AutoCAD Preferences

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/accessing-and-changing-the-autocad-preferences.html

## 文章内容

By Augusto Goncalves
This could be done by manipulating the AutoCAD registry directly, or by using the AutoCAD Preferences ActiveX object. Note that if you make a change in the registry directly, those changes will not affect the current running AutoCAD session. However, the ActiveX Preferences object exports all the AutoCAD preferences properties through an interface that you can use in VBA / VB or C++ / MFC applications. Below is sample code snippets (in VB and C++) which appends a new path to the existing AutoCAD support path.
Below you can find a VB and C++ code sample.
Public acadApp As Object ' AcadApplication 
Public acadPrefFiles As Object 'AcadPreferencesFiles

Sub f_preferences()
    On Error Resume Next
    Set acadApp = GetObject(, "AutoCAD.Application")
    If Err Then
       Err.Clear
       Set acadApp = CreateObject("AutoCAD.Application")
       If Err Then
     MsgBox Err.Description & "  " & Err.Number
     Exit Sub
       End If
    End If
    On Error GoTo 0
    acadApp.Visible = True
    Set acadPrefFiles = acadApp.Preferences.Files
   
    Dim strCurrentSuppPath As String
    ' set the current path to temporary variable
    strCurrentSuppPath = acadPrefFiles.SupportPath   
    ' example: You want to add this 
    ' "c:\test" path to the support path
    acadPrefFiles.SupportPath = strCurrentSuppPath & _
        ";" & "c:\test"
End Sub
void fSetSupportPath()
{
  IAcadApplicationPtr pApp = NULL;
  IAcadPreferencesPtr pPref = NULL;
  IAcadPreferencesFilesPtr pPrefFiles = NULL;
    pApp = acedGetAcadWinApp()->GetIDispatch(TRUE);
  pPref = pApp->Preferences;
    pPrefFiles = pPref->Files;
    _bstr_t strOldPath;
  strOldPath = pPrefFiles->GetSupportPath();
    //print old support path
  acutPrintf(_T("\nOld Support path: %s"),
    (ACHAR *)(_bstr_t)pPrefFiles->GetSupportPath());
    //set the new support path
  pPrefFiles->PutSupportPath(strOldPath + _bstr_t(";c:\\temp"));
}
catch(_com_error &es)
{
}

## 评论

**内容**: dario said...
//insert a block, and in the sequel want the data of this block,

//Hello my name is Dario
//'m from Brazil
//I'm still having problem
//need help
//can someone help me?
//insert a block, and in the sequel want the data of this block,
//and then delete this block
//as the example in the main code, just below ..

//I have these questions that are commented no Main method >>???????

//Main method
//===================================================================================================
[CommandMethod("Blockk")]
public void blockk()
{
Document doc = Host.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
string[] data = new string[3];
data[0] = "data 1";
data[1] = "data 2";
data[2] = "data 3";
BlockReference db = InsertBlockFromFile_(doc, @"C:\wbc\orienta.dwg", new Point3d(50, 50, 50), Math.PI * 0.25,
"wbc_insert", data, 30, 30, 1, 7, true, null, "wbcd");
//??????? return..>>> Example
//??????? db.insertionPoint
//??????? db.angle
//??????? db.handle
//??????? db.Xproprierts
//??????? db.Atrib
//??????? db.erase

}

//Complementary methods
//===============================================================================================================================
public static BlockReference InsertBlockFromFile_(Document doc, string DrawingFile, Point3d Pinsert, double Angle,
string Layer, string[] DadosExtendidos = null, double escalax = 1.0, double escalay = 1.0, double escalaz = 1.0, short ColorLayer = 7,
bool ModelSpace = true, string[] Atributos = null, string RegAplicacao = "wbc")
{
if (!System.IO.File.Exists(DrawingFile))
{
MessageBox.Show("Drawing not found\n" + DrawingFile);
return null;
}
string sourceFileName = DrawingFile;
string Blockname = System.IO.Path.GetFileNameWithoutExtension(sourceFileName);
try
{
using (Transaction tr = doc.TransactionManager.StartTransaction())
{
Database db = new Database(false, false);
db.ReadDwgFile(DrawingFile, System.IO.FileShare.Read, true, null);
ObjectId BlkId = doc.Database.Insert(Blockname, db, true); // ISL: Small fix, use correct block name
tr.Commit();
}
}
catch (IOException ioe)
{
MessageBox.Show(ioe.Message);
return null;
}
return AddBlockTest_(doc, Blockname, Pinsert, Angle, Layer, DadosExtendidos, escalax, escalay, escalaz, ColorLayer, Atributos, RegAplicacao);
}
private static BlockReference AddBlockTest_(Document doc, string blockName, Point3d Pinsert, double Angle,
string Layer, string[] DadosExtendidos = null, double escalax = 1.0, double escalay = 1.0, double escalaz = 1.0,
short ColorLayer = 7, string[] Atributos = null, string Regaplicacao = "wbc")
{
Database db = doc.Database;
using (Transaction myT = db.TransactionManager.StartTransaction())
{
//Get the block definition "Check".
BlockTable bt =
db.BlockTableId.GetObject(OpenMode.ForRead) as BlockTable;
BlockTableRecord blockDef =
bt[blockName].GetObject(OpenMode.ForRead) as BlockTableRecord;
BlockTableRecord ms = (BlockTableRecord)myT.GetObject(db.CurrentSpaceId, OpenMode.ForWrite);

//Create new BlockReference, and link it to our block definition
using (BlockReference blockRef =
new BlockReference(Pinsert, blockDef.ObjectId))
{
blockRef.Rotation = Angle;
blockRef.ScaleFactors = new Scale3d(escalax, escalay, escalaz);
//Add the block reference to modelspace
ms.AppendEntity(blockRef);
myT.AddNewlyCreatedDBObject(blockRef, true);
SetXData_(blockRef, Regaplicacao , DadosExtendidos, doc);
CreatLayer_(Layer, doc, ColorLayer);
blockRef.Layer = Layer;
}
//Our work here is done
myT.Commit();
}
return null;
}

static public void SetXData_(Entity bref, string nome, string[] data, Document doc, string VersaoEquipamento = "Without Version")
{
Database db = doc.Database;
using (Transaction tr = doc.TransactionManager.StartTransaction())
{
AddRegAppTableRecord_(nome, doc);
ResultBuffer rb = new ResultBuffer();
rb.Add(new TypedValue(1001, nome));
for (int i = 0; i < data.Length; i++)
{
rb.Add(new TypedValue(1000, data[i]));
}
rb.Add(new TypedValue(1000, VersaoEquipamento));
DateTime Wdata = DateTime.Now;
Wdata.ToShortDateString();
rb.Add(new TypedValue(1000, Wdata.ToString()));
rb.Add(new TypedValue(1000, VariaveisGlobais.Wusuario + "_" + VariaveisGlobais.NumeroSerie));
bref.XData = rb;
tr.Commit();
}
}
public static void CreatLayer_(string sLayerName, Document doc, short CorCamada = 7)
{
Document acDoc = doc;
Database acCurDb = acDoc.Database;
// Start a transaction
using (Transaction acTrans = acCurDb.TransactionManager.StartTransaction())
{
// Open the Layer table for read
LayerTable acLyrTbl;
acLyrTbl = acTrans.GetObject(acCurDb.LayerTableId,
OpenMode.ForRead) as LayerTable;
if (acLyrTbl.Has(sLayerName) == false)
{
Platform.DatabaseServices.LayerTableRecord acLyrTblRec = new LayerTableRecord();
// Assign the layer the ACI color 1 and a name
acLyrTblRec.Color = Platform.Colors.Color.FromColorIndex(Platform.Colors.ColorMethod.ByAci, CorCamada);
acLyrTblRec.Name = sLayerName;
// Upgrade the Layer table for write
acLyrTbl.UpgradeOpen();
// Append the new layer to the Layer table and the transaction
acLyrTbl.Add(acLyrTblRec);
acTrans.AddNewlyCreatedDBObject(acLyrTblRec, true);
}
acTrans.Commit();
}
}

public static void AddRegAppTableRecord_(string regAppName, Document doc)
{
using (Transaction tr = doc.TransactionManager.StartTransaction())
{
RegAppTable rat = (RegAppTable)tr.GetObject(doc.Database.RegAppTableId, OpenMode.ForRead, false);
if (!rat.Has(regAppName))
{
rat.UpgradeOpen();
RegAppTableRecord ratr = new RegAppTableRecord();
ratr.Name = regAppName;
rat.Add(ratr);
tr.AddNewlyCreatedDBObject(ratr, true);
}
tr.Commit();
}
}
Reply
03/26/2014 at 04:47 AM

---
**内容**: Augusto Goncalves said in reply to dario...
Dario,
For a better support, can you please post programing questions at the AutoCAD .NET Forum? See at http://forums.autodesk.com/t5/NET/bd-p/152
Thanks!
Augusto Goncalves
Reply
03/26/2014 at 08:13 AM

---
