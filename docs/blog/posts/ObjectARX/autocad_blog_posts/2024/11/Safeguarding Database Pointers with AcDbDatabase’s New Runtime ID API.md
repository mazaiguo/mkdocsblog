---
title: "Safeguarding Database Pointers with AcDbDatabase’s New Runtime ID API"
date: 2024-11-01
categories:
  - AutoCAD
tags:
  - API
  - Database
description: "In Autodesk software, developers sometimes face an issue where a memory address, specifically an AcDbDatabase pointer, may get reused. If a databas..."
author: Autodesk
---
# Safeguarding Database Pointers with AcDbDatabase’s New Runtime ID API

发布日期: 2024-11-01

原始链接: https://adndevblog.typepad.com/autocad/2024/11/safeguarding-database-pointers-with-acdbdatabases-new-runtime-id-api.html

## 文章内容

By Madhukar Moogala
In Autodesk software, developers sometimes face an issue where a memory address, specifically an AcDbDatabase pointer, may get reused. If a database (DB) is deleted and a new one is created at the same memory location, how can we distinguish between the two instances?
This question led us to introduce a new API—runtimeId.
Why the Change?
Our team noticed a pattern in crash reports related to stale AcDbDatabase pointers. Often, these issues stemmed from cached pointers that were no longer valid but hadn’t been refreshed. To help clients validate their pointers, we recommended using acdbActiveDatabaseArray() to search for active database pointers.
While this method allowed clients to identify active pointers, it came with two limitations:
Performance Overhead: As the number of open databases increases, searching through an array can introduce delays.
Ambiguity of Validity: Even if a pointer is valid, it doesn’t guarantee it points to the originally intended database instance.
This is where the runtimeId API comes in.
New API Methods for Safer Database Management
The new runtime ID API allows clients to confirm both the validity and uniqueness of a database pointer:
AcDbDatabase::runtimeId(): Retrieves a unique runtime ID for the current database instance, distinguishing it from any previous instance.
AcDbDatabase::dbIdFromPtr(): A static method that returns the runtime ID from a pointer, if valid.
AcDbDatabase::dbPtrFromId(): A static method that returns the database pointer from an ID, if valid.
By using these methods, developers can cache the runtime ID for long-term usage, ensuring a reliable reference to the database, even if a pointer address is reused.
Future-Proofing with Runtime ID
This approach enables efficient, reliable database pointer management and protects against the issues caused by re-used memory locations. By using runtime IDs, developers can avoid stale pointers and maintain database integrity with minimal performance impact.
        #if DEBUG
    [DllImport("acpal.dll", CallingConvention = CallingConvention.Cdecl,
               CharSet = CharSet.Ansi, EntryPoint = "acutSetAssertDia")]
    static extern bool acutSetAssertDia(bool bSetDia);
      #endif


```csharp
[CommandMethod("TestRunTimeId")]
public static void TestRunTimeId()
{
    var doc = Application.DocumentManager.MdiActiveDocument;
    if (doc == null) return;

    var ed = doc.Editor;

    var firstDb = new Database(true, true);
    var transDb = new Database(true, true);

    // Validate layer table ID
    var id = firstDb.LayerTableId;
    if (!id.IsValid)
    {
        ed.WriteMessage("\nLayer ID is not valid.");
    }
    if (!id.IsWellBehaved)
    {
        ed.WriteMessage("\nLayer ID is not well-behaved.");
    }

    // Attempt to access object in the transaction
    using (Transaction t = transDb.TransactionManager.StartTransaction())
    {
        var obj = t.GetObject(id, OpenMode.ForRead, false);
        if (obj == null)
        {
            ed.WriteMessage("\nCannot open the layer table.");
        }
    }

    // Retrieve and compare runtime IDs
    long rid1 = firstDb.RuntimeId();
    if (rid1 <= 0)
    {
        ed.WriteMessage("\nRuntimeId < 0!");
    }
    if (rid1 != Database.IdFromDb(firstDb))
    {
        ed.WriteMessage("\nDatabase ID from pointer does not match runtime ID!");
    }

    long rid2 = transDb.RuntimeId();
    if (rid2 <= 0)
    {
        ed.WriteMessage("\nRuntimeId < 0!");
    }
    if (rid2 != Database.IdFromDb(transDb))
    {
        ed.WriteMessage("\nTransaction DB ID from pointer does not match runtime ID!");
    }
    if (Database.DbFromId(rid2) != transDb)
    {
        ed.WriteMessage("\nDbPtrFromId returned an incorrect pointer for transDb!");
    }
    if (rid1 == rid2)
    {
        ed.WriteMessage("\nDB and transDb have identical runtime IDs!");
    }

    // Validate null/zero scenarios
    if (Database.DbFromId(0) != null)
    {
        ed.WriteMessage("\nDbFromId(0) returned non-null!");
    }
    if (Database.IdFromDb(null) != 0)
    {
        ed.WriteMessage("\nIdFromDb(null) returned non-zero!");
    }

    // Delete firstDb and check pointer validity
    firstDb.Dispose();
    if (Database.DbFromId(rid1) != null)
    {
        ed.WriteMessage("\nDeleted DB's ID returned a non-null pointer!");
    }
    if (Database.IdFromDb(firstDb) != 0)
    {
        ed.WriteMessage("\nDeleted DB's stale pointer returned non-zero ID!");
    }

    // Check the validity and behavior of stale layer ID
    if (id.IsValid)
    {
        ed.WriteMessage("\nStale layer ID is still valid?");
    }
    if (!id.IsWellBehaved)
    {
        ed.WriteMessage("\nStale layer ID is not well-behaved?");
    }

    // Start a transaction to test stale ID access gracefully
    using (Transaction t = transDb.TransactionManager.StartTransaction())
    {
        acutSetAssertDia(false); // Disable asserts for this test
        try
        {
            var obj = t.GetObject(id, OpenMode.ForRead, false);
            if (obj != null)
            {
                ed.WriteMessage("\nAccess to stale ID succeeded?");
            }
        }
        catch (Autodesk.AutoCAD.Runtime.Exception e)
        {

            ed.WriteMessage($"\nUnexpected GetObject() exception: {e.Message}");
        }
        acutSetAssertDia(true); // Re-enable asserts
    }

    // Clean up transDb
    transDb.Dispose();
    if (Database.DbFromId(rid2) != null)
    {
        ed.WriteMessage("\nDeleted transDb's ID returned a non-null pointer!");
    }
    if (Database.IdFromDb(transDb) != 0)
    {
        ed.WriteMessage("\nDeleted transDb's stale pointer returned non-zero ID!");
    }
}
```

