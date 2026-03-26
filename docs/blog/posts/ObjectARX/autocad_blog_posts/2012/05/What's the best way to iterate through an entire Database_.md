---
title: "What's the best way to iterate through an entire Database?"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Database
description: "The objects stored in the database get an handle value that gets incremented sequentially, so the fastest approach if one wants to iterate through ..."
author: Autodesk
---
# What's the best way to iterate through an entire Database?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/whats-the-best-way-to-iterate-through-an-entire-database.html

## 文章内容

By Philippe Leefsma
The objects stored in the database get an handle value that gets incremented sequentially, so the fastest approach if one wants to iterate through the whole content of a Database, is to start from handle = 1 to the max handle existing in the Database. P/Invoking "acdbHandEnt" can then help to retrieve the ObjectId from an handle.
The following C# code illustrates how to do that:
public struct ads_name
{
    public IntPtr a;
    public IntPtr b;
};
  [DllImport("acdb19.dll",
CharSet = CharSet.Unicode,
CallingConvention = CallingConvention.Cdecl,
EntryPoint = "acdbHandEnt")]
public static extern int acdbHandEnt(
    string handle, ref ads_name name);
  [CommandMethod("IterateDb")]
static public void IterateDb()
{
    ads_name ename = new ads_name();
      Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      ObjectIdCollection validIds = new ObjectIdCollection();
      // now get the last handle in the db
    Handle handseed = db.Handseed;
      // copy the handseed total into an efficient raw datatype
    long handseedTotal = handseed.Value;
      // loop from 0 to the last handle (this could be a big loop)
    for (long i = 1; i < handseedTotal; ++i)
    {
        string handle = Convert.ToString(i, 16);
          // get the ename by converting
        // the long to a hex value string
        int res = acdbHandEnt(handle, ref ename);
          if (res != 5100) // RTNORM
            continue;
          // convert the ename to an objectid
        ObjectId id = new ObjectId(ename.a);
          // check if it's a valid objectId
        if (!id.IsValid)
            continue;
          try
        {
            // open if not erased
            using (DBObject obj =
                id.Open(OpenMode.ForRead, false))
            {
                validIds.Add(id);
            }
        }
        catch
        {
          }
    }
      ed.WriteMessage("\nNumber of retrieved valid ObjectIds: "
        + validIds.Count.ToString());
      validIds.Clear();
}

## 评论

**内容**: Account Deleted said...
Hi, Philippe!
I think you should start not with the handle == 1, but with a handle db.BlockTable.Handle, which is usually equal to 1.
However, I often had to deal with the dwg-files, which have the first real handle very large, such as 0xffffffe.
Reply
05/07/2012 at 01:31 AM

---
**内容**: Account Deleted said...
Also this topic may be interesting: http://www.theswamp.org/index.php?topic=39272.0
Reply
05/07/2012 at 01:39 AM

---
**内容**: Maxence DELANNOY said...
You can use Database.TryGetObjectId to convert the handle to an ObjectId.
Reply
05/30/2012 at 03:25 AM

---
