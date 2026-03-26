---
title: "Serialize a .NET class into an AutoCAD drawing database"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Database
description: "I would like to serialize my .NET class into an AutoCAD drawing database, so it is saved into the drawing, and I can recreate my class again (deser..."
author: Autodesk
---
# Serialize a .NET class into an AutoCAD drawing database

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/serialize-a-net-class-into-an-autocad-drawing-database.html

## 文章内容

By Adam Nagy
I would like to serialize my .NET class into an AutoCAD drawing database, so it is saved into the drawing, and I can recreate my class again (deserialize it), when the drawing is reopened. How could I do it?
Solution
You could use the .NET serialization technique to serialize your class into a binary stream and then you can save it in the drawing as a bunch of binary chunks. You could save the ResultBuffer to an object's XData or into an Xrecord.Data of an entity or an item in the Named Objects Dictionary (NOD). DevNote TS2563 tells you what the difference is between using XData and Xrecord. If you are saving it into an XData, then the ResultBuffer needs to start with a registered application name. Here is a sample which shows this:
using System;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;
using System.Security.Permissions;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.EditorInput;
  [assembly: CommandClass(typeof(MyClassSerializer.Commands))]
  namespace MyClassSerializer
{
  // We need it to help with deserialization
    public sealed class MyBinder : SerializationBinder
  {
    public override System.Type BindToType(
      string assemblyName,
      string typeName)
    {
      return Type.GetType(string.Format("{0}, {1}",
        typeName, assemblyName));
    }
  }
    // Helper class to write to and from ResultBuffer
    public class MyUtil
  {
    const int kMaxChunkSize = 127;
      public static ResultBuffer StreamToResBuf(
      MemoryStream ms, string appName)
    {
      ResultBuffer resBuf =
        new ResultBuffer(
          new TypedValue(
            (int)DxfCode.ExtendedDataRegAppName, appName));
        for (int i = 0; i < ms.Length; i += kMaxChunkSize)
      {
        int length = (int)Math.Min(ms.Length - i, kMaxChunkSize);
        byte[] datachunk = new byte[length];
        ms.Read(datachunk, 0, length);
        resBuf.Add(
          new TypedValue(
            (int)DxfCode.ExtendedDataBinaryChunk, datachunk));
      }
        return resBuf;
    }
      public static MemoryStream ResBufToStream(ResultBuffer resBuf)
    {
      MemoryStream ms = new MemoryStream();
      TypedValue[] values = resBuf.AsArray();
        // Start from 1 to skip application name
        for (int i = 1; i < values.Length; i++)
      {
        byte[] datachunk = (byte[])values[i].Value;
        ms.Write(datachunk, 0, datachunk.Length);
      }
      ms.Position = 0;
        return ms;
    }
  }
    [Serializable]
  public abstract class MyBaseClass : ISerializable
  {
    public const string appName = "MyApp";
      public MyBaseClass()
    {
    }
      public static object NewFromResBuf(ResultBuffer resBuf)
    {
      BinaryFormatter bf = new BinaryFormatter();
      bf.Binder = new MyBinder();
        MemoryStream ms = MyUtil.ResBufToStream(resBuf);
        MyBaseClass mbc = (MyBaseClass)bf.Deserialize(ms);
        return mbc;
    }
      public static object NewFromEntity(Entity ent)
    {
      using (
        ResultBuffer resBuf = ent.GetXDataForApplication(appName))
      {
        return NewFromResBuf(resBuf);
      }
    }
      public ResultBuffer SaveToResBuf()
    {
      BinaryFormatter bf = new BinaryFormatter();
      MemoryStream ms = new MemoryStream();
      bf.Serialize(ms, this);
      ms.Position = 0;
        ResultBuffer resBuf = MyUtil.StreamToResBuf(ms, appName);
        return resBuf;
    }
      public void SaveToEntity(Entity ent)
    {
      // Make sure application name is registered
      // If we were to save the ResultBuffer to an Xrecord.Data,
      // then we would not need to have a registered application name
        Transaction tr =
        ent.Database.TransactionManager.TopTransaction;
        RegAppTable regTable =
        (RegAppTable)tr.GetObject(
          ent.Database.RegAppTableId, OpenMode.ForWrite);
      if (!regTable.Has(MyClass.appName))
      {
        RegAppTableRecord app = new RegAppTableRecord();
        app.Name = MyClass.appName;
        regTable.Add(app);
        tr.AddNewlyCreatedDBObject(app, true);
      }
        using (ResultBuffer resBuf = SaveToResBuf())
      {
        ent.XData = resBuf;
      }
    }
      [SecurityPermission(SecurityAction.LinkDemand,
       Flags = SecurityPermissionFlag.SerializationFormatter)]
    public abstract void GetObjectData(
      SerializationInfo info, StreamingContext context);
  }
    [Serializable]
  public class MyClass : MyBaseClass
  {
    public string myString;
    public double myDouble;
      public MyClass()
    {
    }
      protected MyClass(
      SerializationInfo info, StreamingContext context)
    {
      if (info == null)
        throw new System.ArgumentNullException("info");
        myString = (string)info.GetValue("MyString", typeof(string));
      myDouble = (double)info.GetValue("MyDouble", typeof(double));
    }
      [SecurityPermission(SecurityAction.LinkDemand,
       Flags = SecurityPermissionFlag.SerializationFormatter)]
    public override void GetObjectData(
      SerializationInfo info, StreamingContext context)
    {
      info.AddValue("MyString", myString);
      info.AddValue("MyDouble", myDouble);
    }
      // Just for testing purposes
      public override string ToString()
    {
      return base.ToString() + "," +
        myString + "," + myDouble.ToString();
    }
  }
    public class Commands
  {
    [CommandMethod("SaveClassToEntityXData")]
    static public void SaveClassToEntityXData()
    {
      Database db = acApp.DocumentManager.MdiActiveDocument.Database;
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        PromptEntityResult per =
        ed.GetEntity("Select entity to save class to:\n");
      if (per.Status != PromptStatus.OK)
        return;
        // Create an object
        MyClass mc = new MyClass();
      mc.myDouble = 1.2345;
      mc.myString = "Some text";
        // Save it to the document
        using (
        Transaction tr = db.TransactionManager.StartTransaction())
      {
        Entity ent =
          (Entity)tr.GetObject(per.ObjectId, OpenMode.ForWrite);
          mc.SaveToEntity(ent);
          tr.Commit();
      }
        // Write some info about the results
        ed.WriteMessage(
        "Content of MyClass we serialized:\n {0} \n", mc.ToString());
    }
      [CommandMethod("GetClassFromEntityXData")]
    static public void GetClassFromEntityXData()
    {
      Database db = acApp.DocumentManager.MdiActiveDocument.Database;
      Editor ed = acApp.DocumentManager.MdiActiveDocument.Editor;
        PromptEntityResult per =
        ed.GetEntity("Select entity to get class from:\n");
      if (per.Status != PromptStatus.OK)
        return;
        // Get back the class
        using (
        Transaction tr = db.TransactionManager.StartTransaction())
      {
        Entity ent =
          (Entity)tr.GetObject(per.ObjectId, OpenMode.ForRead);
          MyClass mc = (MyClass)MyClass.NewFromEntity(ent);
          // Write some info about the results
          ed.WriteMessage(
          "Content of MyClass we deserialized:\n {0} \n",
          mc.ToString());
          tr.Commit();
      }
    }
  }
}

## 评论

**内容**: petcon said...
old code but cool
Reply
06/04/2012 at 03:36 AM

---
**内容**: Gdiael said...
Hi Adam, nice post!
Is it possible to serialize a class using the object xmlserializer and save the information in resulbuffer as text, and reverse the process to deserialize?
In the case of a class with a large number of properties, which are instances of other classes, there is a problem? All classes must be serializable?
Reply
01/14/2013 at 05:38 PM

---
**内容**: Adam Nagy said...
Hi,
Yes, you should be able to use the XmlSerializer instead of implementing your own serialization. In that case you will also have to save the type name of the object you are serializing because XmlSerializer seems to require them.
Also the data limit for XData is 16 KB, so if you want to serialize big objects you should probably go with extension dictionary instead: http://adndevblog.typepad.com/autocad/2012/06/adding-extension-dictionary.html
Cheers,
Adam
Reply
01/15/2013 at 07:04 AM

---
**内容**: Keith Brown said...
I thought that I would add that the StreamToResBuf method requires the memorystream.position to be at 0.
I created the memory stream and then immediately passed it to this method and it was making a result buffer full of 0's because the position was at the end of the stream. Adding the following line to the beginning of the method will insure that the pointer is always at the beginning of the stream.
ms.Seek(0, SeekOrigin.Begin)
Reply
01/27/2016 at 12:31 PM

---
**内容**: Keith Brown said in reply to Keith Brown...
Or you could use ms.Position = 0 as was done in the ResBufToStream method
Reply
01/27/2016 at 12:48 PM

---
**内容**: Adam Nagy said in reply to Keith Brown...
Hi Keith,
Yes, and I do set the position of the MemoryStream to 0 in the SaveToResBuf() function before calling MyUtil.StreamToResBuf().
I cannot remember now why I did it like that instead of doing inside the MyUtil.StreamToResBuf() function :)
Cheers,
Adam
Reply
01/27/2016 at 12:51 PM

---
**内容**: Jared Rodrigues said...
I used this method to save a class to a drawing in AutoCAD 2016. Now we are trying to upgrade to AutoCAD 2019 but in 2019 it doesn't deserialize the class correctly in old drawings originally created in 2016. Has anyone else experienced this?
Reply
10/24/2019 at 11:07 PM

---
**内容**: Jared Rodrigues said in reply to Jared Rodrigues...
I found a solution to my problem.
For some reason you need to change this:
public static object NewFromResBuf(ResultBuffer resBuf) {
BinaryFormatter bf = new BinaryFormatter();
bf.Binder = new MyBinder();
MemoryStream ms = MyUtil.ResBufToStream(resBuf);
MyBaseClass mbc = (MyBaseClass)bf.Deserialize(ms);
return mbc;
}
to this in AutoCAD 2019:
public static object NewFromResBuf(ResultBuffer resBuf) {
BinaryFormatter bf = new BinaryFormatter();
bf.Binder = new MyBinder();
MemoryStream ms = MyUtil.ResBufToStream(resBuf);
object mbc = bf.Deserialize(ms);
return mbc;
}
Reply
10/25/2019 at 08:56 AM

---
**内容**: Jared Rodrigues said in reply to Jared Rodrigues...
Never mind my solution doesn't actually fix the problem.
Reply
10/25/2019 at 09:06 AM

---
**内容**: Madhukar Moogala said in reply to Jared Rodrigues...
Can you please ask this in forum with providing a sample project. Other experts or I can take a look at it this.
https://forums.autodesk.com/t5/net/bd-p/152
Reply
10/28/2019 at 11:06 PM

---
