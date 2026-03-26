---
title: "Accessing visible entities in a dynamic block"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Block
  - C++
  - ObjectARX
description: "Here is a question once posted by an ADN member:"
author: Autodesk
---
# Accessing visible entities in a dynamic block

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/accessing-visible-entities-in-a-dynamic-block.html

## 文章内容

By Philippe Leefsma
  Here is a question once posted by an ADN member:
How do I access the list of visible entities for a specific visibility state in a dynamic block that contains a visibility parameter?
The following solution is a code sample based on a suggestion proposed by Tony Tanzillo in this forum post.
Solution
Unfortunately, as the dynamic block API is a bit limited, there is no direct way to access this information. This is actually buried in the dynamic block definition's extension dictionary, and the object you need to look for is an instance of an "AcDbBlockVisibilityParameter" (that's the native ObjectARX class and the runtime class name, but it isn’t exposed to the public API, neither in C++ nor .Net).
So a bit of extra work is needed in order to obtain it, here are the steps:
1. Get the BlockTableRecord for the dynamic block definition.
2. Get the extension dictionary for the BlockTableRecord.
3. Get ObjectId of the "ACAD_ENHANCEDBLOCK" entry in the extension dictionary.
4. call acdbEntGet() on ObjectId obtained in step 3, which returns a ResultBuffer containing TypedValues.
5. Iterate over the TypedValues looking for an item whose group code is 360, and get the ObjectId stored in the
TypedValue's Value property, then get value of the 'Name' property of the ObjectId's ObjectClass property,
and see if it equals the string "AcDbBlockVisibilityParameter".
6. Once you've found the AcDbBlockVisibilityParameter object's ObjectId, call acdbEntGet() on it.
7. Iterate over the TypedValues in the ResultBuffer returned by acdbEntGet(), looking for an item whose group code is 303.

8. Get the next element from the ResultBuffer, which is a 94 group code whose value is the number of ObjectIds that follow, and then read that many subsequent items and collect the ObjectIds in each into a list, and you then have finally the ObjectIds of the block entities that are explicitly visible in the visiblity state.
Here is the complete C# code:
[CommandMethod("DynablockVisibilityStates")]
public void DynablockVisibilityStates()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptResult pr = ed.GetString("\nEnter block name: ");
      if (pr.Status != PromptStatus.OK)
        return;
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockTable bt = Tx.GetObject(
            db.BlockTableId,
            OpenMode.ForRead)
                as BlockTable;
          if (!bt.Has(pr.StringResult))
        {
            ed.WriteMessage("\nBlock doesn't exist :(");
            return;
        }
          BlockTableRecord btr = Tx.GetObject(
            bt[pr.StringResult],
            OpenMode.ForRead)
                as BlockTableRecord;
                if (!btr.IsDynamicBlock)
        {
            ed.WriteMessage("\nNot a dynamic block :(");
            return;
        }
          if (btr.ExtensionDictionary == null)
        {
            ed.WriteMessage("\nNo ExtensionDictionary :(");
            return;
        }
          DBDictionary dico = Tx.GetObject(
            btr.ExtensionDictionary,
            OpenMode.ForRead)
                as DBDictionary;
          if (!dico.Contains("ACAD_ENHANCEDBLOCK"))
        {
            ed.WriteMessage(
                "\nACAD_ENHANCEDBLOCK Entry not found :(");
              return;
        }
          ObjectId graphId = dico.GetAt("ACAD_ENHANCEDBLOCK");
          System.Collections.Generic.List<object> parameterIds =
            acdbEntGetObjects(graphId, 360);
          foreach (object parameterId in parameterIds)
        {
            ObjectId id = (ObjectId)parameterId;
              if (id.ObjectClass.Name ==
                "AcDbBlockVisibilityParameter")
            {
                System.Collections.Generic.List<TypedValue>
                    visibilityParam = acdbEntGetTypedVals(id);
                  System.Collections.Generic.
                    List<TypedValue>.Enumerator enumerator =
                    visibilityParam.GetEnumerator();
                  while (enumerator.MoveNext())
                {
                    if (enumerator.Current.TypeCode == 303)
                    {
                        string group =
                            (string)enumerator.Current.Value;
                          enumerator.MoveNext();
                          int nbEntitiesInGroup =
                            (int)enumerator.Current.Value;
                          ed.WriteMessage(
                           "\n . Visibility Group: " + group +
                           " Nb Entities in group: " +
                           nbEntitiesInGroup);
                          for (int i = 0; i < nbEntitiesInGroup; ++i)
                        {
                            enumerator.MoveNext();
                            ObjectId entityId =
                                (ObjectId)enumerator.Current.Value;
                              Entity entity = Tx.GetObject(
                                entityId,
                                OpenMode.ForRead)
                                    as Entity;
                              ed.WriteMessage("\n    - " +
                                entity.ToString() + " " +
                                entityId.ToString());
                        }
                    }
                }
                break;
            }
        }
          Tx.Commit();
    }
}
  public struct ads_name
{
    IntPtr a;
    IntPtr b;
};
  [DllImport("acdb18.dll",
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "?acdbGetAdsName@@YA?AW4ErrorStatus@Acad@@AAY01JVAcDbObjectId@@@Z")]
public static extern int acdbGetAdsName(
    ref ads_name name, ObjectId objId);
  [DllImport("acad.exe",
    CharSet = CharSet.Ansi,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acdbEntGet")]
public static extern System.IntPtr acdbEntGet(ref ads_name ename);
  private System.Collections.Generic.List<object>
    acdbEntGetObjects(ObjectId id, short dxfcode)
{
    System.Collections.Generic.List<object> result =
        new System.Collections.Generic.List<object>();
      ads_name name = new ads_name();
      int res = acdbGetAdsName(ref name, id);
      ResultBuffer rb = new ResultBuffer();
      Autodesk.AutoCAD.Runtime.Interop.AttachUnmanagedObject(
        rb, acdbEntGet(ref name), true);
      ResultBufferEnumerator iter = rb.GetEnumerator();
      while (iter.MoveNext())
    {
        TypedValue typedValue = (TypedValue)iter.Current;
          if (typedValue.TypeCode == dxfcode)
        {
            result.Add(typedValue.Value);
        }
    }
      return result;
}
  private System.Collections.Generic.List<TypedValue>
    acdbEntGetTypedVals(ObjectId id)
{
    System.Collections.Generic.List<TypedValue> result =
        new System.Collections.Generic.List<TypedValue>();
      ads_name name = new ads_name();
        int res = acdbGetAdsName(ref name, id);
      ResultBuffer rb = new ResultBuffer();
      Autodesk.AutoCAD.Runtime.Interop.AttachUnmanagedObject(
        rb, acdbEntGet(ref name), true);
      ResultBufferEnumerator iter = rb.GetEnumerator();
      while (iter.MoveNext())
    {
        result.Add((TypedValue)iter.Current);
    }
      return result;
}

## 评论

**内容**: Jason Booth said...
Two questions:
It looks like AcDbBlockVisibilityParameter contains only entities visible under the default lookup parameters. What if the block definition has a combination of visibility and lookup parameters?
and
This appears to only check the visibility state on the original block definition, instead of a specific reference. Does this mean that to look up the state of a specific reference, the extension dictionary on "BlockRef.DynamicBlockTableRecord" should be used instead?
Reply
07/18/2012 at 04:30 PM

---
**内容**: Philippe Leefsma said...
To answer question two, yes the code checks the entities visible inside each visibility state of the block record. For a block reference you would check in which visibility state it is through its dynamic parameters and deduce from that which entities are visible for that specific reference.
I’m not sure about the first question, did you test on an actual drawing?
Keep in mind that this approach should be considered as a "hack". This information is not exposed through any public API, so some data might not be accessible at all and if you need to further dig it out, you would need to investigate that on your own.
Reply
07/19/2012 at 12:28 AM

---
**内容**: Jason Booth said in reply to Philippe Leefsma...
Yes, I tested a pre-made dynamic block reference of a "wood screw" that I found online. It used a visibility parameter to select the screw type, and a lookup parameter to select the screw length.
What I didn't know at the time was that the lookup table was controlling a stretch action and an array action. Therefore I doubt it's possible to get find the entities of a dynamic block reference in their current state using this approach.
I'm going to set the block to "explodable" and try using acedCmd() to run the Explode command and see if that works for me.
Thanks.
Reply
07/19/2012 at 07:46 AM

---
**内容**: JeffH said...
I know a little late but if wanting to know what is visible for a BlockReference iterate its Blocktablerecord and check each entities IsVisible property.
Reply
02/18/2014 at 11:27 PM

---
**内容**: Philippe Leefsma said...
Hi Jeff,
Thanks for the feedback. Here the approach allows to know which entities are visible without instantiating the block in advance ...
Reply
02/19/2014 at 12:05 AM

---
**内容**: Tony M said...
Hi I converted the code to vb.net and I am having trouble with these statements.
the example has acdb18.dll But the program couldn't find it so I used acdb19.dll
When the code hits this statement it throws an error something about a Entry point "?"
Can you tell me what I need to do to get it running?
Dim res As Integer = acdbGetAdsName(name, id)
_
Public Shared Function acdbGetAdsName(ByRef name As ads_name, objId As ObjectId) As Integer
End Function

_
Public Shared Function acdbEntGet(ByRef ename As ads_name) As System.IntPtr
End Function
Thanks,
Tony
Reply
06/07/2016 at 02:17 PM

---
**内容**: James said...
Has there been a cleaner way exposed in the API to get the visible entities in the later versions?
Reply
10/04/2016 at 06:09 AM

---
**内容**: Philippe Leefsma said...
Not as far as I know... this method is quite reliable, although a bit verbose.
Reply
10/04/2016 at 06:19 AM

---
**内容**: Jürgen Becker said...
Hi Philippe,
can you tell me the Entry Point for AutoCAD 2017 and 2018?
Thanks for your answer.
BTW: How it goes?
Cheers Jürgen
Reply
02/20/2018 at 08:11 AM

---
