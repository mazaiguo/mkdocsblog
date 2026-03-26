---
title: "Obtaining the Layer States “Detailed Data” from an External DWG File"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - DWG
  - Layer
description: "Leading on from this post Obtaining the Layer States from an External DWG file I had the question to list out the internal data from the LayerState..."
author: Autodesk
---
# Obtaining the Layer States “Detailed Data” from an External DWG File

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/obtaining-the-layer-states-detailed-data-from-an-external-dwg-file.html

## 文章内容

Leading on from this post Obtaining the Layer States from an External DWG file I had the question to list out the internal data from the LayerStatesManager dictionary Xrecords…
So here you go…
// list the layer states detailed data
// by Fenton Webb, DevTech, 07/08/2012
[CommandMethod("ListLayerStates")]
public void ListLayerStates()
{
  Document doc = Application.DocumentManager.MdiActiveDocument;
  Editor ed = doc.Editor;
    // select a dwg file
  OpenFileDialog openFileDlg = default(OpenFileDialog);
  openFileDlg = new OpenFileDialog("Select DWG File", "fenton.dwg", "dwg", "Select DWG file", 0);
  // if something was selected
    if (openFileDlg.ShowModal() == true)
  {
    // extract the file path
    string dwgPath = openFileDlg.Filename;
      // now open the dwg in a side database
    using (Database sideDb = new Database(false, true))
    {
      // read the dwg file
      sideDb.ReadDwgFile(dwgPath, System.IO.FileShare.Read, false, null);
      // close the file and make sure we have read everything in
      sideDb.CloseInput(true);
        // get the layer state manager
      LayerStateManager lsManager = sideDb.LayerStateManager;
      //get the layer states dict
      using (DBDictionary layerStatesDict =
        lsManager.LayerStatesDictionaryId(true).Open(OpenMode.ForRead)
                                  as DBDictionary)
      {
        string sLayerStateName = "";
        // now loop each layer state
        foreach (DBDictionaryEntry layerStateDict in layerStatesDict)
        {
          // get the layer state name
          sLayerStateName = layerStateDict.Key;
          ed.WriteMessage("\nData for Later State " + sLayerStateName);
          // now cast to an XRecord
          using (Xrecord layerStateXRec =
            layerStateDict.Value.Open(OpenMode.ForRead) as Xrecord)
          {
            // extract the data from the result buffer
            ResultBuffer layerStateResbuf = layerStateXRec.Data;
            // now loop each entry
            foreach (TypedValue dxfEntry in layerStateResbuf)
            {
              switch (dxfEntry.TypeCode)
              {
                // mask
                case (int)DxfCode.Int32 + 1:
                {
                  ed.WriteMessage("\nMask = " + dxfEntry.Value.ToString());
                }break;
                  // has viewport data
                case (int)DxfCode.Bool:
                {
                  ed.WriteMessage("\nHas Viewport Data = " +
                      dxfEntry.Value.ToString());
                } break;
                  // Layer description
                case (int)DxfCode.XTextString + 1:
                  {
                    ed.WriteMessage("\nLayer Description = " +
                      dxfEntry.Value.ToString());
                  } break;
                  // current Layer
                case (int)DxfCode.XTextString + 2:
                  {
                    ed.WriteMessage("\nCurrent Layer = " +
                      dxfEntry.Value.ToString());
                  } break;
                  // layer name
                case (int)DxfCode.LayerName:
                {
                  ed.WriteMessage("\nLayer Name= " +
                    dxfEntry.Value.ToString());
                } break;
                  // layer object id
                case (int)DxfCode.SoftPointerId:
                {
                  ObjectId id = (ObjectId)(dxfEntry.Value);
                  using (LayerTableRecord ltr =
                    id.Open(OpenMode.ForRead) as LayerTableRecord)
                    ed.WriteMessage("\nLayer Name = " + ltr.Name);
                } break;
                  // restore options
                case (int)DxfCode.Int32:
                {
                  ed.WriteMessage("\nRestore Options= " +
                      dxfEntry.Value.ToString());
                  } break;
                  // layer color
                case (int)DxfCode.Color:
                {
                  ed.WriteMessage("\nColor= " + dxfEntry.Value.ToString());
                  } break;
                  // layer true color
                case (int)DxfCode.Int32 + 2:
                {
                  ed.WriteMessage("\nTrue Color= " +
                    dxfEntry.Value.ToString());
                } break;
                  // color book
                case (int)DxfCode.XTextString:
                {
                  ed.WriteMessage("\nColorBook Name = " +
                    dxfEntry.Value.ToString());
                } break;
                  // lineweight
                case (int)DxfCode.LineWeight:
                {
                  ed.WriteMessage("\nLineWeight = " +
                    dxfEntry.Value.ToString());
                } break;
                  // linetype name
                case (int)DxfCode.LinetypeName:
                {
                  ed.WriteMessage("\nLinetype Name = " +
                    dxfEntry.Value.ToString());
                } break;
                  // linetype object id
                case (int)DxfCode.SoftPointerId + 1:
                {
                  ObjectId id = (ObjectId)(dxfEntry.Value);
                  using (LinetypeTableRecord ltr =
                    id.Open(OpenMode.ForRead) as LinetypeTableRecord)
                    ed.WriteMessage("\nLinetype Name = " + ltr.Name);
                } break;
                  // plotstyle object id
                case (int)DxfCode.PlotStyleNameId:
                {
                  ed.WriteMessage("\nPlotStyle Id = " +
                    dxfEntry.Value.ToString());
                } break;
                  // plotstyle name
                case (int)DxfCode.Text:
                {
                  ed.WriteMessage("\nPlotStyle Name = " +
                    dxfEntry.Value.ToString());
                } break;
                  // Transparency
                case (int)DxfCode.Alpha:
                {
                  ed.WriteMessage("\nTransparency Alpha Channel = " +
                    dxfEntry.Value.ToString());
                } break;
                  // Transparency
                case (int)DxfCode.XDataStart:
                  {
                    ed.WriteMessage
                      ("\n*******************************************");
                  } break;
                  default:
                  {
                    ed.WriteMessage("\nID " +
                      dxfEntry.TypeCode.ToString() +
                      " has data " +
                      dxfEntry.Value.ToString() +
                      " is not yet handled...");
                  }break;
              }
            }
          }
        }
      }
    }
  }
}

## 评论

**内容**: cesar said...
Hi,
what is the code to read, if the layer is frozen?
Reply
02/19/2021 at 07:51 AM

---
