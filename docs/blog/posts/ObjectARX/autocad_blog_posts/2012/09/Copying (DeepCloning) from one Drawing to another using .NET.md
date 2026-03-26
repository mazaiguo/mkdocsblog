---
title: "Copying (DeepCloning) from one Drawing to another using .NET"
date: 2012-09-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - DWG
  - Database
description: "Here’s how to copy entities from the Model Space of a DWG file hosted inside of AutoCAD to an external DWG file."
author: Autodesk
---
# Copying (DeepCloning) from one Drawing to another using .NET

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/copying-deepcloning-from-one-drawing-to-another-using-net.html

## 文章内容

by Fenton Webb
Here’s how to copy entities from the Model Space of a DWG file hosted inside of AutoCAD to an external DWG file.
  // copy Model Space to external DWG
// by Fenton Webb, DevTech 14/9/2012
[CommandMethod("CopySpaceToExtDWG")]
public static void CopySpaceToExtDWG()
{
 // get the working database (in AutoCAD)
 Database sourceDb = Application.DocumentManager.MdiActiveDocument.Database;
 try
{
  // create a new destination database
  using (Database destDb = new Database(true, true))
  {
   // get the model space object ids for both dbs
   ObjectId sourceMsId = SymbolUtilityServices.GetBlockModelSpaceId(sourceDb);
   ObjectId destDbMsId = SymbolUtilityServices.GetBlockModelSpaceId(destDb);
     // now create an array of object ids to hold the source objects to copy
   ObjectIdCollection sourceIds = new ObjectIdCollection();
     // open the sourceDb ModelSpace (current autocad dwg)
   using (BlockTableRecord ms = sourceMsId.Open(OpenMode.ForRead)
        as BlockTableRecord)
    // loop all the entities and record their ids
    foreach (ObjectId id in ms)
     sourceIds.Add(id);
     // next prepare to deepclone the recorded ids to the destdb
   IdMapping mapping = new IdMapping();
   // now clone the objects into the destdb
   sourceDb.WblockCloneObjects(sourceIds, destDbMsId, mapping, DuplicateRecordCloning.Replace, false);
   destDb.SaveAs("c:\\temp\\dwgs\\CopyTest.dwg", DwgVersion.Current);
  }
}
 catch (System.Exception eXP)
{
  System.Windows.Forms.MessageBox.Show(eXP.ToString());
}
}

## 评论

**内容**: Oleg said...
Hi Fenton,
When I use the code like this where I want to invoke Open method, I usually do "Obsolete" attribute addidtion before of the
CommandMethod, e.g. like this:
[Obsolete]
[CommandMethod("CopySpaceToExtDWG")]
//----rest code here----//
Is this right way?
Thanks for your work for us
Oleg
Reply
09/14/2012 at 11:32 AM

---
**内容**: Fenton Webb said...
Hey Oleg
Open() is not obsolete... Nor is deprecated. I don't use the Obsolete attribute and I don't think it should be used either...
Hope this helps.
Reply
09/14/2012 at 11:56 AM

---
**内容**: Kerry Brown said...
Fenton,
From the 2013 SP1.1 Acdbmgd - Autodesk.AutoCAD.DatabaseServices.ObjectId
[Obsolete("For advanced use only. Use GetObject instead")]
public DBObject Open(OpenMode mode, [MarshalAs(UnmanagedType.U1)] bool openErased, [MarshalAs(UnmanagedType.U1)] bool forceOpenOnLockedLayer)
{
DBObject obj2 = (DBObject) RXObject.Create(this.OpenWorker(mode, openErased, forceOpenOnLockedLayer), true);
GC.SuppressFinalize(obj2);
return obj2;
}
It's easy to think it is obsolete, unless Oleg has read the Forum post that says the Attribute is wrong.
Regards
Kerry
Reply
09/14/2012 at 04:30 PM

---
**内容**: Oleg said in reply to Kerry Brown...
Thank you to both of you,
I'm just using A2010 and I haven't have
an error warning if I've debug the code,
if I'm using this 'obsolete' stuff, otherwise
an error warnig is occurs in the Error window...
Oleg
Reply
09/15/2012 at 03:41 AM

---
**内容**: Andrey Bushman (@AndreyBushman) said...
Hi Fenton,
replace your code row:
BlockTableRecord ms = sourceMsId.Open(OpenMode.ForRead)
by this:
BlockTableRecord ms = sourceMsId.GetObject(OpenMode.ForRead)
In AutoCAD 2013 SP1.1 the ObjectId.GetObject() method not marked like Obsolete.
Regards
Reply
09/15/2012 at 09:24 AM

---
**内容**: Madhukar Moogala said in reply to Andrey Bushman (@AndreyBushman)...
Hi Andrey - ObjectId.GetObject makes use of the topmost open Transaction to open the object. Fenton's code is not using Transactions, and so using that API would crash in this example. You'll find posts elsewhere on this blog discussing Transactions, OpenCloseTransactions and Open/Close.
Reply
09/17/2012 at 03:12 PM

---
**内容**: Fenton Webb said...
Hi guys
I'll try and get this updated so the Obsolete attribute is not longer in the AutoCAD API
Reply
09/17/2012 at 10:17 AM

---
**内容**: Kerry Brown said in reply to Fenton Webb...
Thanks Fenton.
Fenton/Stephen/DevTech,
Can the Help be dated in some way or have a build number ... the downloadable help would be a particularly good candidate for this.
I understood that one of the main arguments for having the help on-line was so that the content could be updated relatively easily .. being able to identify ( and possibly filter ) revised content would be a big help.
Regards
Kerry
Reply
09/17/2012 at 03:56 PM

---
**内容**: Oleg said in reply to Fenton Webb...
Thanks, Fenton!
I will keep it in mind when I could be able to use
next Acad release, now I'm working in 2010,
Regards,
Oleg
Reply
09/18/2012 at 01:21 AM

---
**内容**: dba said...
Hello,
I'm just trying to transfer ent.visible to the new DB. I do "wblockcloneobjects" on a dynamic Blockref and wanted to use the idmapping to transfer the visible property of each subobject (these are nested dynamic blockreferences). Inspecting the idmapping, I found it contains the subblockreferences twice (different Objectids) as idpairs, plus the original Blockref, whose Objectid was passed to the wblockclone... I can't really see the reason for the double entries, and the one "set" has everithing visible, the second features the correct visibility values. Checking by Quickselection in the Blockeditor, there are 7 Blockrefs in the Block :), the idmapping contains 15 idpairs (7*2 + 1 for the cloned blockref).
Any hints were appreciated!
Thank you,
Daniel
Reply
06/30/2014 at 11:35 PM

---
**内容**: Ben said...
Hi there
the title of the post says "deep cloning" but the WblockCloneObjects method is used.
Just want to make sure that the aforementioned method performs a deep clone (i.e. if there is an extension dictionary on the source object to be cloned, will a copy of that extension dictionary be found in the target object?
a pointer in the right direction would be much appreciated.
rgds
Reply
01/07/2019 at 11:09 PM

---
**内容**: Ann said...
Hi,
Has anyone problem while saving database ?
line: destDb.SaveAs("c:\\temp\\dwgs\\CopyTest.dwg", DwgVersion.Current);
I acquired error eCantOpenFile and I have no idea how I can solve it.
Ann
Reply
08/18/2020 at 07:24 AM

---
