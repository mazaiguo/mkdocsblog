---
title: "How to find all fields in a drawing?"
date: 2014-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
  - DXF
  - Database
description: "The Named Object Dictionary (NOD) in a database contains an “ACADFIELDLIST” entry if your drawing contains any field. This entry holds a record of ..."
author: Autodesk
---
# How to find all fields in a drawing?

发布日期: 2014-07-01

原始链接: https://adndevblog.typepad.com/autocad/2014/07/how-to-find-all-fields-in-a-drawing.html

## 文章内容

By Philippe Leefsma
The Named Object Dictionary (NOD) in a database contains an “ACAD_FIELDLIST” entry if your drawing contains any field. This entry holds a record of type “AcDbFieldList” which is unfortunately an object type that isn’t exposed to the ARX or .Net API.
Each AcDbField object is typically accessible from an entity Extension Dictionary, for example if I you create a MText that contains a field, you can access that specific MText and look for the AcDbField in the ExtensionDictionary.
In order to access all fields directly, one way to get the job done is to grab all TypedValue (DxfCode – Value pairs) of our AcDbFieldList, iterate through them and grab the one that have dxf code = 330 and are of type AcDbField.
We need to rely on some good old P/Invoked arx methods, hence that code is version dependent, here is an example for R19:
class ImportsR19
{
    public struct ads_name
    {
        public IntPtr a;
        public IntPtr b;
    };
      [DllImport("acdb19.dll",
        CallingConvention = CallingConvention.Cdecl,
        EntryPoint = "?acdbGetAdsName@@YA?AW4ErrorStatus@Acad@@AAY01JVAcDbObjectId@@@Z")]
    public static extern int acdbGetAdsName32(
        ref ads_name name,
        ObjectId objId);
      [DllImport("acdb19.dll",
        CallingConvention = CallingConvention.Cdecl,
        EntryPoint = "?acdbGetAdsName@@YA?AW4ErrorStatus@Acad@@AEAY01_JVAcDbObjectId@@@Z")]
    public static extern int acdbGetAdsName64(
        ref ads_name name,
        ObjectId objId);
      public static int acdbGetAdsName(
        ref ads_name name,
        ObjectId objId)
    {
        if (Marshal.SizeOf(IntPtr.Zero) > 4)
            return acdbGetAdsName64(ref name, objId);
          return acdbGetAdsName32(ref name, objId);
    }
      [DllImport("accore.dll",
        CharSet = CharSet.Unicode,
        CallingConvention = CallingConvention.Cdecl,
        EntryPoint = "acdbEntGet")]
    public static extern System.IntPtr acdbEntGet(
        ref ads_name ename);
      public static System.Collections.Generic.List<TypedValue>
        acdbEntGetTypedValues(ObjectId id)
    {
        System.Collections.Generic.List<TypedValue> result =
            new System.Collections.Generic.List<TypedValue>();
          ads_name name = new ads_name();
          int res = acdbGetAdsName(ref name, id);
          ResultBuffer rb = new ResultBuffer();
        Autodesk.AutoCAD.Runtime.Interop.AttachUnmanagedObject(
            rb,
            acdbEntGet(ref name),
            true);
          ResultBufferEnumerator iter = rb.GetEnumerator();
          while (iter.MoveNext())
        {
            result.Add((TypedValue)iter.Current);
        }
          return result;
    }
}
        [CommandMethod("FieldList")]
public void FieldList()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      using (var tx = db.TransactionManager.StartTransaction())
    {
        var nod = tx.GetObject(
            db.NamedObjectsDictionaryId,
            OpenMode.ForRead) as DBDictionary;
          if (!nod.Contains("ACAD_FIELDLIST"))
        {
            ed.WriteMessage("\nDrawing has no field...");
            return;
        }
          var id = nod.GetAt("ACAD_FIELDLIST");
          List<TypedValue> dxf = ImportsR19.acdbEntGetTypedValues(id);
          foreach (var entry in dxf)
        {
            if (entry.TypeCode == 330)
            {
                ObjectId objId = (ObjectId)entry.Value;
                  if (objId.ObjectClass.Name == "AcDbField")
                {
                    Field field = tx.GetObject(
                        objId,
                        OpenMode.ForWrite) as Field;
                      field.Evaluate();
                      ed.WriteMessage(
                     "\n - Format: " + field.Format +
                     " Value: " +
                     field.GetStringValue());                        
                }
            }
        }
    }
}

## 评论

**内容**: dennis said...
Hi Philippe: I am trying to do this in VB.NET. I first tried taking your code above and converting it on the Telerik website from C# to VB.NET. It left me with errors on the DLLIMPORT call and the setting for the "var" from the line: using (var tx = db.TransactionManager.StartTransaction()) . Could you give me some direction on what I should have in my Reference list and the Import for VB.NET, and how to resolve the two errors mentioned above. I admit I am new at this, and do appreciate your direction.
Reply
07/08/2014 at 07:18 AM

---
**内容**: Philippe said...
The minimum references are: AcMgd.dll, AcDbMgd.dll and AcCoreMgd.dll from the ARX/inc of your SDK. Make sure to set the "Copy Local=False" for the 3 of them.
VB.Net doesn't support the "var" keyword, that's an implicit type declaration in C#, you need to use either late binding or the explicit type, i.e. Transaction. If you are also new to .Net, I suggest you first take a look at some beginner, general purpose tutorials on the topic.
Here is are some Vb.Net samples with P/Invoke that may help you getting started on that:
Private Structure ads_name
Private a As IntPtr
Private b As IntPtr
End Structure
_
Private Shared Function acdbEntGet(ByRef ename As ads_name) As System.IntPtr
End Function
_
Private Shared Function acdbEntLast(ByRef result As ads_name) As Integer
End Function
_
Private Shared Function acdbEntNext(ByRef ent As ads_name, ByRef result As ads_name) As Integer
End Function
_
Private Shared Function acdbGetObjectId(ByRef id As ObjectId, ByRef name As ads_name) As ErrorStatus
End Function
_
Public Sub GetAllBlocks()
Dim doc As Document = Application.DocumentManager.MdiActiveDocument
Dim db As Database = doc.Database
Dim ed As Editor = doc.Editor
Using Tx As Transaction = db.TransactionManager.StartTransaction()
Dim tbl As BlockTable = Tx.GetObject(db.BlockTableId(), OpenMode.ForRead, False, True)
For Each id As ObjectId In tbl
Dim btr As BlockTableRecord = Tx.GetObject(id, OpenMode.ForRead, False, True)
ed.WriteMessage("- Block: " + btr.Name + vbCrLf)
Next
End Using
End Sub
You can also find several Vb.Net samples on that same blog, although we usually prefer to write with C#.
Hope that helps.

Reply
07/08/2014 at 09:15 AM

---
**内容**: Philippe said...
Ha... the VB.Net tags for dllimport do not along very well with html markups... Take a look on the web if you don't know how to do a dllimport:
http://stackoverflow.com/questions/2229793/how-to-use-dllimport-in-vb-net
Philippe.
Reply
07/08/2014 at 09:18 AM

---
**内容**: dennis said...
Thanks for the extra help. I will keep digging.
Reply
07/09/2014 at 08:46 AM

---
**内容**: dennis said...
Update for you Philippe, I figured the "var" thing out. Thanks to the link you provided for the dllimport, I found a bit on the converting the "var" call.
http://stackoverflow.com/questions/2478552/vb-net-equivalent-to-c-sharp-var-keyword
Reply
07/23/2014 at 08:10 AM

---
