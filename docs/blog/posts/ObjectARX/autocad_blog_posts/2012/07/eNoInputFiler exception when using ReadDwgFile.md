---
title: "eNoInputFiler exception when using ReadDwgFile"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Database
description: "When I run the following code I get an eNoInputFiler exception when calling ReadDwgFile. What could be the problem?"
author: Autodesk
---
# eNoInputFiler exception when using ReadDwgFile

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/enoinputfiler-exception-when-using-readdwgfile.html

## 文章内容

By Adam Nagy
When I run the following code I get an eNoInputFiler exception when calling ReadDwgFile. What could be the problem?
using System;
using System.IO;
  using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.ApplicationServices;
  [assembly: CommandClass(typeof(MyAddIn.Commands))]
  namespace MyAddIn
{
  public class Commands
  {
    [CommandMethod("MyCmd", CommandFlags.Session)]
    public static void MyCmd()
    {
      Document doc = acApp.DocumentManager.MdiActiveDocument;
      using (Database db = new Database(false, false))
      {
        db.ReadDwgFile(
          @"C:\testdwg.dwg", FileShare.Read, false, null);
          // do something with it
      }
    }
  }
}
Solution
The second parameter of the Database constructor (noDocument) controls if the Database should be associated with the current document or not.
Probably the main reason to decide to associate the Database with a document would be to participate in Undo: see ObjectARX Reference > Document-Independent Databases
In this case you would need to do document locking (and since you are in Session context because of CommandFlags.Session, you would need to do it yourself, explicitly, using Document.LockDocument())
However if you do not associate the Database with the current document, then no locking is needed.
So the solution is to either lock the Document when you want to associate your Database with it (noDocument = false):
[CommandMethod("MyCmd", CommandFlags.Session)]
public static void MyCmd()
{
  Document doc = acApp.DocumentManager.MdiActiveDocument;
  using (doc.LockDocument())
  {
    using (Database db = new Database(false, false))
    {
      db.ReadDwgFile(
        @"C:\testdwg.dwg", FileShare.Read, false, null);
        // do something with it
    }
  }
}
... or don’t associate the Database with the current document (noDocument = true, much more common)
[CommandMethod("MyCmd", CommandFlags.Session)]
public static void MyCmd()
{
  using (Database db = new Database(false, true))
  {
    db.ReadDwgFile(
      @"C:\testdwg.dwg", FileShare.Read, false, null);
      // do something with it
  }
}

