---
title: "Exploding AEC entities using RealDWG"
date: 2015-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Block
  - C#
  - C++
description: "Exploding an AEC entity such as a Wall in AutoCAD results in a block reference and the block table record that it refers to contains faces. But whe..."
author: Autodesk
---
# Exploding AEC entities using RealDWG

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/exploding-aec-entities-using-realdwg.html

## 文章内容

By Balaji Ramamoorthy
Exploding an AEC entity such as a Wall in AutoCAD results in a block reference and the block table record that it refers to contains faces. But when exploding the Wall entity in a RealDWG application results in a block reference and the block table record that it refers to contains lines. 
In this blog post we will look into the reason for this difference and a way to workaround it. The workaround was provided by my colleagues Mikako Harada and Tony Zou. Many thanks to them.
While RealDWG can read a drawing created by any of the AutoCAD verticals, the object enablers specific to the verticals will still be needed for the host application to recognize the entities in that drawing. The object enabler defines the resulting entity set when the entity is exploded. As object enabler provides the explode functionality for its custom entities, they may also have other considerations.
For example, when an AEC drawing has its viewing direction set as Top View, a wall appears as a rectangle. When the viewing direction is any other view, the wall appears as a collection of faces. 
Also, AEC drawings do not fully load into a side database when using the readDwgFile. This is a known behavior in AutoCAD Architecture and here is a blog post by my colleague Adam Nagy. For the database to get fully loaded in a side database it is required to call AecAppDbx::drawingPromoterAndIniter method.
Considering the above reasons, here are the C++ and .Net sample codes to explode a wall entity in a RealDWg application. The methods to have the database initialized and to set its viewing direction are invoked by accessing the exported methods from AecBase.dbx using their ordinal numbers. Please note that the ordinal numbers can change and are version specific. In the below code, the ordinal numbers for 2015 and 2016 releases are provided. For any other version, you may need to find them out using dumpbin on AecBase.lib from the \Lib-x64 folder.
Here is the C# code snippet :
 using  System.Runtime.InteropServices;
 using  Autodesk.AutoCAD.Runtime;
   internal  static  class  Workaround 
 {
     [StructLayout (LayoutKind .Sequential)]
     private  struct  AcGeVector3d 
     {
         public  double  x;
         public  double  y;
         public  double  z;
     }
       // for 2016 
     //[DllImport(@"C:\\Program Files\\Autodesk\\RealDWG 2015\\AecBase.dbx",  
     //        CallingConvention = CallingConvention.Cdecl,  
     //        EntryPoint = "#1202")] 
          // for 2015 
     [DllImport (@"C:\\Program Files\\Autodesk\\RealDWG 2015\\AecBase.dbx" , 
         CallingConvention = CallingConvention .Cdecl, 
         EntryPoint = "#1204" )]   
       private  extern  static  void  setLastViewDir(ref  AcGeVector3d  vDir);
       public  static  void  SetLastViewDirection(Vector3d direction)
     {
         if  (! SystemObjects.ServiceDictionary.Contains(
             "AecBaseServices" ))
             return ;
         AcGeVector3d  vec;
         vec.x = direction.X;
         vec.y = direction.Y;
         vec.z = direction.Z;
         setLastViewDir(ref  vec);
     }
 }
   // No change in ordinals 
 // For 2015 and 2016 
 [DllImport (@"C:\\Program Files\\Autodesk\\RealDWG 2015\\AecBase.dbx" , 
     CallingConvention = CallingConvention .Cdecl, 
     CharSet = CharSet .Unicode, EntryPoint = "#897" )] 
 public  extern  static  void  drawingPromoterAndIniter
 (IntPtr db, bool  sideDb);
     Database db = new  Database(false , true );
   db.ReadDwgFile(
     @"D:\\Temp\\wall.dwg" , 
     System.IO.FileShare.None, 
     false , 
     "" );
   HostApplicationServices.WorkingDatabase = db;
   drawingPromoterAndIniter(db.UnmanagedObject, true );
 Workaround.SetLastViewDirection(Vector3d.XAxis);
   //... Usual Explode of the entity
  Here is the C++ code snippet :
 typedef void  (*drawingPromoterAndIniter)
     (AcDbDatabase* pDb, bool  bUseCurrentViewInfo);
 typedef void  (*setLastViewDir)(AcGeVector3d direction);
     acdbSetHostApplicationServices(&gDumpDwgHostApp);
    CString testFilePath = "D:\\\\Temp\\\\wall.dwg" ;
   long  lcid = 0x00000409;  // English 
 acdbValidateSetup(lcid);
   bool  isLoaded = acrxLoadModule(
     _T("C:\\\\Program Files\\\\Autodesk\\\\RealDWG 2016\\\\AecBase.dbx" ), 0);
   HMODULE hModule=GetModuleHandle(_T("AecBase.dbx" ));
 int  ordinal = 897;
 auto drawingPromoterFunc = 
     (drawingPromoterAndIniter)GetProcAddress(hModule, (LPCSTR) ordinal);
 if  (drawingPromoterFunc == nullptr) 
 {
  AfxMessageBox(_T("Error ! function not in AecBase.dbx !!" ));
  return  1;
 }
   ordinal = 1202; // 2016 
 //ordinal = 1204; //2015 
 auto setLastViewDirFunc = 
     (setLastViewDir)GetProcAddress(hModule, (LPCSTR) ordinal);
 if  (setLastViewDirFunc == nullptr) 
 {
  AfxMessageBox(_T("Error ! function not in AecBase.dbx !!" ));
  return  1;
 }
    AcDbDatabase *pDb = new  AcDbDatabase(Adesk::kFalse);
 if  (pDb == NULL)
     return  1;
   Acad::ErrorStatus es = Acad::eOk;
 es = pDb->readDwgFile(testFilePath);
   acdbHostApplicationServices()->setWorkingDatabase(pDb);
 acdbResolveCurrentXRefs(pDb);
 drawingPromoterFunc(pDb, false );
   setLastViewDirFunc(AcGeVector3d::kXAxis);
   //... Usual Explode of the entity

## 评论

**内容**: Wbmk said...
Hi, thanx for this example, but i am fairly new to this and i am having trouble using your example to extract values from a propertyset wich is attached to a solid3D.
When i try to Pinvoke the loading of side databases, my application crashes. Is the correct ordinal used in the example? When i generate a list of exports using dumpbin the only readable function name that resembles the function you are using is:
106 7 00177990 drawingPromoterAndInitialize
When i run my code from whitin ACA, it run's fine and values are extracted; but using RealDWG i keep getting a ProxyObject instead of a PropertySet.
Any hint's a to what i a doing wrong?
Reply
12/10/2015 at 06:13 AM

---
**内容**: Balaji said in reply to Wbmk...
Sorry for the delay. I hadn't noticed your comment to this post.
I have posted a reply to your discussion forum post on the same topic
http://forums.autodesk.com/t5/net/use-objectdbx-realdwg-to-read-propertysetdef-from-solid3d/m-p/5955500#M46959
Thanks
Balaji
Reply
12/17/2015 at 01:07 AM

---
**内容**: Artur said...
What are ordinal numbers for RealDWG 2017?
Reply
04/21/2016 at 07:43 AM

---
