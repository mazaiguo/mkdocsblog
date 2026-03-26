---
title: "Docking toolbars in rows using CUI API"
date: 2015-10-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
  - CUI
description: "The toolbar creation and docking in AutoCAD API is exposed via the COM API. Although the toolbars can be docked using the COM API, it does not prov..."
author: Autodesk
---
# Docking toolbars in rows using CUI API

发布日期: 2015-10-01

原始链接: https://adndevblog.typepad.com/autocad/2015/10/docking-toolbars-in-rows-using-cui-api.html

## 文章内容

By Balaji Ramamoorthy
The toolbar creation and docking in AutoCAD API is exposed via the COM API. Although the toolbars can be docked using the COM API, it does not provide a way to arrange the docked toolbars as in multiple rows. AutoCAD internally uses a method that can dock toolbars to the desired location in rows, which is not exposed via the COM API.
A way to workaround it is to configure the workspace toolbars and set their arrangement using CUI API. Here is a sample code snippet that arranges the toolbars in the current workspace as shown in the following screenshot. All other toolbars in the current workspace are hidden. You can modify the code to show other toolbars if required.
Here is the toolbar arrangement that we seek :
Row : 0 Column : 0 - Smooth Mesh toolbar
Row : 1 Column : 0 - Smooth Mesh Primitives toolbar
Row : 0 Column : 1 - Draw toolbar
Row : 1 Column : 1 - Draw order toolbar
Row : 0 Column : 2 - Standard toolbar
Row : 1 Column : 2 - CAD Standard toolbar
 using  Autodesk.AutoCAD.Customization;
   [DllImport("accore.dll" , CharSet = CharSet.Ansi, 
 CallingConvention = CallingConvention.Cdecl, 
 EntryPoint = "acedCmdS" )]
 private  static  extern  int  acedCmdS(System.IntPtr vlist);
   [CommandMethod("SetDockedToolbars" )]
 public  void  SetDockedToolbarsMethod()
 {
     Document activeDoc 
   = Application.DocumentManager.MdiActiveDocument;
     Database db = activeDoc.Database;
     Editor ed = activeDoc.Editor;
       string mainCuiFile = 
   (string)Application.GetSystemVariable("MENUNAME" );
     mainCuiFile += ".cuix" ;
     CustomizationSection cs 
   = new  CustomizationSection(mainCuiFile);
       string curWorkspace = 
   (string)Application.GetSystemVariable("WSCURRENT" );
     Workspace ws = cs.getWorkspace(curWorkspace);  
     // Turn off all the workspace toolbars. 
     // We will later turn on the ones that we need and  
     // dock them as we desire 
     foreach (WorkspaceToolbar wsTb in ws.WorkspaceToolbars)
     {
         wsTb.Display = 0;
     }
       // Smooth Mesh toolbar 
     Toolbar tbSmoothMesh = 
   cs.MenuGroup.Toolbars.
   FindToolbarWithName("Smooth Mesh" );
     WorkspaceToolbar wsTbSmoothMesh = 
   ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbSmoothMesh.ElementID, cs.MenuGroup.Name);
       if (wsTbSmoothMesh == null)
     {
         wsTbSmoothMesh = new  WorkspaceToolbar(ws, tbSmoothMesh);
         ws.WorkspaceToolbars.Add(wsTbSmoothMesh);
     }
     wsTbSmoothMesh.Display = 1;
     wsTbSmoothMesh.ToolbarOrient = ToolbarOrient.left;
     wsTbSmoothMesh.DockRow = 0;
     wsTbSmoothMesh.DockColumn = 0;
       // Smooth Mesh Primitives toolbar 
     Toolbar tbSmoothMeshPrimitives 
   = cs.MenuGroup.Toolbars.FindToolbarWithName
   ("Smooth Mesh Primitives" );
     WorkspaceToolbar wsTbSmoothMeshPrimitives 
   = ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbSmoothMeshPrimitives.ElementID, cs.MenuGroup.Name);
     if (wsTbSmoothMeshPrimitives == null)
     {
         wsTbSmoothMeshPrimitives = 
    new  WorkspaceToolbar(ws, tbSmoothMeshPrimitives);
         ws.WorkspaceToolbars.Add(wsTbSmoothMeshPrimitives);
     }
     wsTbSmoothMeshPrimitives.Display = 1;
     wsTbSmoothMeshPrimitives.ToolbarOrient = ToolbarOrient.left;
     wsTbSmoothMeshPrimitives.DockRow = 1;
     wsTbSmoothMeshPrimitives.DockColumn = 0;
       // Draw toolbar 
     Toolbar tbDraw = 
   cs.MenuGroup.Toolbars.FindToolbarWithName("Draw" );
     WorkspaceToolbar wsTbDraw = 
   ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbDraw.ElementID, cs.MenuGroup.Name);
     if (wsTbDraw == null)
     {
         wsTbDraw = new  WorkspaceToolbar(ws, tbDraw);
         ws.WorkspaceToolbars.Add(wsTbDraw);
     }
     wsTbDraw.Display = 1;
     wsTbDraw.ToolbarOrient = ToolbarOrient.left;
     wsTbDraw.DockRow = 0;
     wsTbDraw.DockColumn = 1;
       // Draw order toolbar 
     Toolbar tbDrawOrder = 
   cs.MenuGroup.Toolbars.FindToolbarWithName("Draw Order" );
     WorkspaceToolbar wsTbDrawOrder = 
   ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbDrawOrder.ElementID, cs.MenuGroup.Name);
     if (wsTbDrawOrder == null)
     {
         wsTbDrawOrder = new  WorkspaceToolbar(ws, tbDrawOrder);
         ws.WorkspaceToolbars.Add(wsTbDrawOrder);
     }
     wsTbDrawOrder.Display = 1;
     wsTbDrawOrder.ToolbarOrient = ToolbarOrient.left;
     wsTbDrawOrder.DockRow = 1;
     wsTbDrawOrder.DockColumn = 1;
       // Standard toolbar 
     Toolbar tbStandard = 
   cs.MenuGroup.Toolbars.FindToolbarWithName("Standard" );
     WorkspaceToolbar wsTbStandard = 
   ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbStandard.ElementID, cs.MenuGroup.Name);
     if (wsTbStandard == null)
     {
         wsTbStandard = new  WorkspaceToolbar(ws, tbStandard);
         ws.WorkspaceToolbars.Add(wsTbStandard);
     }
     wsTbStandard.Display = 1;
     wsTbStandard.ToolbarOrient = ToolbarOrient.left;
     wsTbStandard.DockRow = 0;
     wsTbStandard.DockColumn = 2;
       // CAD Standard toolbar 
     Toolbar tbCADStandards = 
   cs.MenuGroup.Toolbars.FindToolbarWithName
   ("CAD Standards" );
     WorkspaceToolbar wsTbCADStandards 
   = ws.WorkspaceToolbars.FindWorkspaceToolbar
   (tbCADStandards.ElementID, cs.MenuGroup.Name);
     if (wsTbCADStandards == null)
     {
         wsTbCADStandards = 
    new  WorkspaceToolbar(ws, tbCADStandards);
         ws.WorkspaceToolbars.Add(wsTbCADStandards);
     }
     wsTbCADStandards.Display = 1;
     wsTbCADStandards.ToolbarOrient = ToolbarOrient.left;
     wsTbCADStandards.DockRow = 1;
     wsTbCADStandards.DockColumn = 2;
       saveCui(cs);
 }
   public  static  void  saveCui(CustomizationSection cs)
 {
     if  (cs.IsModified)
         cs.Save();
       ResultBuffer rb = new  ResultBuffer();
     rb.Add(new  TypedValue(5005, "FILEDIA" ));
     rb.Add(new  TypedValue(5005, "0" ));
     acedCmdS(rb.UnmanagedObject);
       string cuiMenuGroup = cs.MenuGroup.Name;
     rb = new  ResultBuffer();
     rb.Add(new  TypedValue(5005, "_CUIUNLOAD" ));
     rb.Add(new  TypedValue(5005, cuiMenuGroup));
     acedCmdS(rb.UnmanagedObject);
       string cuiFileName = cs.CUIFileName;
     rb = new  ResultBuffer();
     rb.Add(new  TypedValue(5005, "_CUILOAD" ));
     rb.Add(new  TypedValue(5005, cuiFileName));
     acedCmdS(rb.UnmanagedObject);
 }

