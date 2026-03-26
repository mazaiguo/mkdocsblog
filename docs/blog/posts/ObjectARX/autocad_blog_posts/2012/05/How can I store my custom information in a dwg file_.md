---
title: "How can I store my custom information in a dwg file?"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "Q: I need to store some information in a dwg file, which would describe this drawing and let to integrate it with another software system. Can I wr..."
author: Autodesk
---
# How can I store my custom information in a dwg file?

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-can-i-store-my-custom-information-in-a-dwg-file.html

## 文章内容

By Marat Mirgaleev
Q: I need to store some information in a dwg file, which would describe this drawing and let to integrate it with another software system. Can I write such custom information into a drawing and read it later? Can it be done without opening the drawing in AutoCAD?

A: You may use so called Named Object Dictionary (NOD) to store custom data in a drawing. NOD is an essential part of an AutoCAD drawing database and it is created automatically when the drawing is created.
As always with database operations, your program may open a dwg file invisibly to the user via Database.ReadDwgFile() method, i.e. it does not have to be the drawing in the active AutoCAD window.
Here is an example:
// Write some data to the NOD
//============================
[CommandMethod("WNOD")]
public void WriteToNOD()
{
  Database db = new Database();
  try
  {
    // We will write to C:\Temp\Test.dwg. Make sure it exists!
    // Load it into AutoCAD
    db.ReadDwgFile(@"C:\Temp\Test.dwg",
                    System.IO.FileShare.ReadWrite, false, null);
      using( Transaction trans =
                      db.TransactionManager.StartTransaction() )
    {
      // Find the NOD in the database
      DBDictionary nod = (DBDictionary)trans.GetObject(
                  db.NamedObjectsDictionaryId, OpenMode.ForWrite);
        // We use Xrecord class to store data in Dictionaries
      Xrecord myXrecord = new Xrecord();
      myXrecord.Data = new ResultBuffer(
              new TypedValue((int)DxfCode.Int16, 1234),
              new TypedValue((int)DxfCode.Text,
                              "This drawing has been processed"));
        // Create the entry in the Named Object Dictionary
      nod.SetAt("MyData", myXrecord);
      trans.AddNewlyCreatedDBObject(myXrecord, true);
        // Now let's read the data back and print them out
      //  to the Visual Studio's Output window
      ObjectId myDataId = nod.GetAt("MyData");
      Xrecord readBack = (Xrecord)trans.GetObject(
                                    myDataId, OpenMode.ForRead);
      foreach (TypedValue value in readBack.Data)
        System.Diagnostics.Debug.Print(
                  "===== OUR DATA: " + value.TypeCode.ToString()
                  + ". " + value.Value.ToString());
        trans.Commit();
      } // using
      db.SaveAs(@"C:\Temp\Test.dwg", DwgVersion.Current);
    }
  catch( Exception e )
  {
    System.Diagnostics.Debug.Print(e.ToString());
  }
  finally
  {
    db.Dispose();
  }
  } // End of WriteToNOD()
  You can treat the NOD as a place to keep "document-level" data.
If you need to store some data related to particular objects in the drawing, consider using their Extension Dictionaries.

## 评论

**内容**: hm said...
is it slow? still need to load the dwg to autocad, even if it is invisible,
if I need 100 dwg info like this , can I do it this way
Reply
05/17/2012 at 01:51 PM

---
**内容**: Marat Mirgaleev said in reply to hm...
Thanks for your question. I was curious to benchmark it myself and the results are as follows:
I used AutoCAD 2013 on my laptop with Windows 7 32 bit.
I found the biggest dwg file on my computer - 4771 KB.
I simply put the code above into a cycle with 100 iterations.
1st test: AutoCAD + Debug dll: 3 min 21 sec.
2nd test: accoreconsole.exe + Release dll: 3 min 06 sec.
So, approximately 2 seconds for an iteration.
Of course, your results may differ - you may have bigger dwg files, also, the dwg file in my test was, obviously, completely cashed by Windows.
Reply
05/18/2012 at 05:49 AM

---
**内容**: hm said in reply to Marat Mirgaleev...
Thank you Very much,
In my case I can't wait so long, I need to find some other ways to get the info
Reply
05/18/2012 at 06:30 AM

---
**内容**: petcon said...
i think the easyest way is use serialize,and store in the binary in xrecord.
Reply
05/17/2012 at 10:14 PM

---
**内容**: Andrey said...
Thank you, Marat. It is simple and clear example.
Reply
08/29/2012 at 01:03 PM

---
**内容**: Indrawan Adi wicaksono said...
Hi, is the data stored in NOD can be read directly by navisworks?
What if the CAD drawing convert to NWD file? is the data stored in NOD still available in NWD file?
Reply
12/24/2012 at 11:34 PM

---
**内容**: Matheus said...
I'm trying to save a large string in Xrecord date. In my case I want to save a json serialization. But from what I noticed Xrecord Data has a string size limitation. My question is is there any way to save a large string in NOD? Or a way to save a file.json in NOD dictionary?
Reply
03/09/2019 at 02:51 AM

---
**内容**: Ann said...
Hi,
Has anyone problem while saving database ?
line: destDb.SaveAs("c:\\temp\\dwgs\\CopyTest.dwg", DwgVersion.Current);
I acquired error eCantOpenFile and I have no idea how I can solve it.
Ann
Reply
09/16/2020 at 12:12 AM

---
