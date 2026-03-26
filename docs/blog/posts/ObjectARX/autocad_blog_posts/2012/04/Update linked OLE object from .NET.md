---
title: "Update linked OLE object from .NET"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Unicode
description: "If you have a linked OLE object (referencing a bitmap, Excel sheet, etc.) inserted in your AutoCAD drawing and you know the object it referencing c..."
author: Autodesk
---
# Update linked OLE object from .NET

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/update-linked-ole-object-from-net.html

## 文章内容

By Adam Nagy
If you have a linked OLE object (referencing a bitmap, Excel sheet, etc.) inserted in your AutoCAD drawing and you know the object it referencing changed, then you may want to get this object updated programmatically.
The Ole2Frame .NET object has an OleObject property which gives back a wrapped pointer to the underlying COleClientItem MFC object. This object has an UpdateLink function. Having not found a .NET equivalent of that I decided to P/Invoke the UpdateLink function of the MFC class, which in case of MFC 9.0 is implemented inside mfc90u.dll
If you check that dll with depends.exe then you’ll see that the signature of that function is not exported. So you can use a utility called dumpbin.exe to find the ordinal number of the function that we could use. Typing this in the Visual Studio Command Prompt you’ll get back a text file that contains information about UpdateLink as well:
c:\Program Files\Microsoft Visual Studio 9.0\VC>dumpbin /exports mfc90u.lib /out:C:\exports.txt
The above text file gives us the ordinal number plus the mangled name of the function:
6766    ?UpdateLink@COleClientItem@@QAEHXZ (public: int __thiscall COleClientItem::UpdateLink(void))
Since Ole2Frame.OleObject gives back a wrapped pointer that you cannot directly pass to UpdateLink, therefore we might as well P/Invoke AcDbOle2Frame::getOleClientItem from acdb18.dll, which provides us with the pointer that we can pass in to UpdateLink. To find out the mangled name of getOleClientItem, you can simply use depends.exe to look into acdb18.dll
Once we have everything we need to P/Invoke those two functions, we can write the following code (this should work for AutoCAD 2010-2012 32 bit):
[DllImport(
    "mfc90u.dll",
    CallingConvention = CallingConvention.ThisCall,
    EntryPoint="#6766")]
public static extern int
  COleClientItem_UpdateLink(IntPtr thisClientItem);
  [DllImport(
    "acdb18.dll",
    CallingConvention = CallingConvention.ThisCall,
    EntryPoint = "?getOleClientItem@AcDbOle2Frame@@QBEPAVCOleClientItem@@XZ")]
public static extern IntPtr
  AcDbOle2Frame_getOleClientItem(IntPtr thisOle2Frame);
  [CommandMethod("UpdateOleClient")]
public void UpdateOleClient()
{
  Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
    PromptEntityResult per =
    ed.GetEntity("Select an OLE object to update");
    if (per.Status != PromptStatus.OK)
    return;
    Database db = HostApplicationServices.WorkingDatabase;
  using (Transaction tr = db.TransactionManager.StartTransaction())
  {
    Ole2Frame o2f =
      (Ole2Frame)tr.GetObject(per.ObjectId, OpenMode.ForWrite);
      IntPtr ptrClientItem =
      AcDbOle2Frame_getOleClientItem(o2f.UnmanagedObject); 
    COleClientItem_UpdateLink(ptrClientItem);
      tr.Commit();
  }
}
Note: the EntryPoint’s inside the DllImport attributes may need to be changed depending on the version of AutoCAD and MFC, plus the OS platform (32 vs. 64 bit) you are using.
The above code does not seem get the OLE object updated if it’s open in another application – e.g. the bitmap is open in Microsoft Paint.

## 评论

**内容**: mehmet.kurt@sampas.com.tr said...
Hi,
How to insert bitmap as embedded OLE OBJECT with c# ? Do you have a sample code? Thank You.
Mehmet Kurt
Reply
08/06/2012 at 06:27 PM

---
**内容**: john said...
Hi
How to get range of embedded ole excel object which one is copy-paste
into modelspace.

john
Reply
10/11/2013 at 12:32 AM

---
