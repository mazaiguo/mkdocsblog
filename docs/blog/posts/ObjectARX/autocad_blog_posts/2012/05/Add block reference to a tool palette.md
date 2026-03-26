---
title: "Add block reference to a tool palette"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
  - Palette
description: "In the user interface you can select a block reference in the drawing and simply drag & drop it onto a tool palette. I would like to do the same pr..."
author: Autodesk
---
# Add block reference to a tool palette

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/add-block-reference-to-a-tool-palette.html

## 文章内容

By Adam Nagy
In the user interface you can select a block reference in the drawing and simply drag & drop it onto a tool palette. I would like to do the same programmatically: add a new item to the tool palette that references a given block and create a preview image for it.
Solution
You can not only drag & drop a block reference onto a tool palette, but you can also copy-paste it onto the tool palette. And this is what the following solution takes advantage of. We COPYCLIP the block reference and then call the Paste() function of the tool palette.
Here is the ObjectARX solution:
static void BlockRefToToolPalette(void)
{
  // select block reference
  ads_name name;
  ads_point pt;
  if (acedEntSel(L"Select block reference", name, pt) != RTNORM)
    return;
    // get the tool palette where we want to add an item
  CAcTcUiToolPaletteSet* ps = AcTcUiGetToolPaletteWindow();
  CAcTcUiToolPalette* pal =
    ps->FindPalette(L"Architectural", NULL, FALSE);
  if (pal == NULL)
    return;
    // copyclip the block reference
  if (acedCommand(
        RTSTR, L"_COPYCLIP", RTENAME,
        name, RTSTR, L"", RTNONE) != RTNORM)
    return;
    // paste the clipboard onto the palette
  IDataObject* pdo;
  if (SUCCEEDED(::OleGetClipboard(&pdo)))
  {
    if (pal->Paste(pdo, 0, NULL))
    {
      // success
    }
  }
}
Since the above ARX functions do not have corresponding .NET wrappers, we need to P/Invoke those functions.
Note that the DllImport.EntryPoints are specific to AutoCAD 2010. In case of other AutoCAD versions you would need to use a tool like e.g. Dependency Walker (depends.exe) to check the correct entry point.
[DllImport(
  "acad.exe",
  CallingConvention = CallingConvention.Cdecl,
  CharSet = CharSet.Unicode,
  EntryPoint = "acedCmd")]
public static extern int acedCmd(System.IntPtr resBuf);
  [DllImport(
  "AcTcUi.dll",
  CallingConvention = CallingConvention.Cdecl,
  CharSet = CharSet.Unicode,
  EntryPoint =
  "?AcTcUiGetToolPaletteWindow@@YAPAVCAcTcUiToolPaletteSet@@XZ")]
public static extern System.IntPtr AcTcUiGetToolPaletteWindow();
  [DllImport(
  "AcTcUi.dll",
  CallingConvention = CallingConvention.ThisCall,
  CharSet = CharSet.Unicode,
  EntryPoint =
  "?FindPalette@CAcTcUiToolPaletteSet@@QBEPAVCAcTcUiToolPalette" +
  "@@PB_WPAPAVCAcTcUiToolPaletteGroup@@H@Z")]
public static extern System.IntPtr CAcTcUiToolPaletteSet_FindPalette( 
  System.IntPtr paletteSet, string name, System.IntPtr group,  
  bool searchOnlyCurrentGroup);
  [DllImport(
  "AcTcUi.dll",
  CallingConvention = CallingConvention.ThisCall,
  CharSet = CharSet.Unicode,
  EntryPoint =
  "?Paste@CAcTcUiToolPalette@@UAEHPAUIDataObject@@HPAV?$" +
  "CTypedPtrArray@VCPtrArray@@PAVAcTcCatalogItem@@@@@Z")]
public static extern bool CAcTcUiToolPalette_Paste(
  System.IntPtr palette,
  System.Runtime.InteropServices.ComTypes.IDataObject data,  
  int index, System.IntPtr resultList);
  [CommandMethod("BlockRefToToolPalette")]
public void BlockRefToToolPalette()
{
  Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    PromptEntityResult per =
    ed.GetEntity("Select block reference to add to tool palette");
    if (per.Status == PromptStatus.OK)
  {
    // find tool palette you need
    System.IntPtr ps = AcTcUiGetToolPaletteWindow();
      System.IntPtr pal =
      CAcTcUiToolPaletteSet_FindPalette(
        ps, "Architectural", System.IntPtr.Zero, false);
      if (pal != System.IntPtr.Zero)
    {
      // copyclip the block reference
      ResultBuffer rb = new ResultBuffer();
      rb.Add(new TypedValue((int)LispDataType.Text, "_COPYCLIP"));
      rb.Add(
        new TypedValue((int)LispDataType.ObjectId, per.ObjectId));
      rb.Add(new TypedValue((int)LispDataType.Text));
        // if copyclip was OK
      if (acedCmd(rb.UnmanagedObject) == 5100/*RTNORM*/)
      {
        System.Runtime.InteropServices.ComTypes.IDataObject
          comDataObject =
            (System.Runtime.InteropServices.ComTypes.IDataObject)
            System.Windows.Forms.Clipboard.GetDataObject();
          CAcTcUiToolPalette_Paste(
          pal, comDataObject, 0, System.IntPtr.Zero);
      }
    }
  }
}

