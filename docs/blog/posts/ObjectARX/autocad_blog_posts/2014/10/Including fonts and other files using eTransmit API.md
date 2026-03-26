---
title: "Including fonts and other files using eTransmit API"
date: 2014-10-01
categories:
  - AutoCAD
tags:
  - API
  - COM Interop
description: "Recently one of my colleague from Product support enquired if it was possible to find fonts and shape files included in a drawing using the eTransm..."
author: Autodesk
---
# Including fonts and other files using eTransmit API

发布日期: 2014-10-01

原始链接: https://adndevblog.typepad.com/autocad/2014/10/including-fonts-and-other-files-using-etransmit-api-.html

## 文章内容

By Balaji Ramamoorthy
Recently one of my colleague from Product support enquired if it was possible to find fonts and shape files included in a drawing using the eTransmit API. To configure what gets included as dependents when a drawing is added to the TransmittalOperation, it is required to setup the TransmittalInfo.
Here is a sample code that should also fetch the fonts and shape files associated with a drawing using e-Transmit API :
 //AcETransmit19.Interop.dll 
 using  AcETransmit;
   [CommandMethod("DependentFiles" )]
 static  public  void  DependentFilesMethod()
 {
     TransmittalFile tf;
     TransmittalOperation  to 
                 = new  TransmittalOperation();
     TransmittalInfo ti 
                 = to.getTransmittalInfoInterface();
     ti.includeDataLinkFile = 1;
     ti.includeDGNUnderlay = 1;
     ti.includeDWFUnderlay = 1;
     ti.includeFontFile  = 1;
     ti.includeImageFile  = 1;
     ti.includeInventorProjectFile  = 1;
     ti.includeInventorReferences  = 1;
     ti.includeMaterialTextureFile  = 1;
     ti.includeNestedOverlayXrefDwg = 1;
     ti.includePDFUnderlay  = 1;
     ti.includePhotometricWebFile  = 1;
     ti.includePlotFile = 1;
     ti.includeUnloadedXrefDwg  = 1;
     ti.includeXrefDwg = 1;
        string  dwgFile = @"D:\\Temp\\Sample.dwg" ;
     if  (to.addDrawingFile(dwgFile, out  tf) 
                 == AddFileReturnVal.eFileAdded)
     {
           TransmittalFilesGraph tfg 
                 = to.graphInterfacePtr();
           TransmittalFile rootTF = tfg.getRoot();
           DisplayDependent(rootTF);
     }
 }
   static  void  DisplayDependent(TransmittalFile tf)
 {
     int  numberOfDependents = tf.numberOfDependents;
     for  (int  i = 0; i < numberOfDependents; ++i)
     {
         TransmittalFile childTF = tf.getDependent(i);
           FileType ft = childTF.FileType;
           string  sourcePath = childTF.sourcePath;
           Application.DocumentManager.MdiActiveDocument.Editor
                             .WriteMessage(String.Format(
                             "{0} Dependent {1} - {2}" , 
                             Environment.NewLine, 
                                 ft.ToString(), sourcePath));
           DisplayDependent(childTF);
     }
 }

