---
title: "Using e-Transmit API in .Net to find external references in a drawing"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - COM
  - XREF
description: "The e-Trasmit API is exposed using COM (AcETransmit18.tlb) and so, you will first need to create an inter-op assembly for use in your .Net project...."
author: Autodesk
---
# Using e-Transmit API in .Net to find external references in a drawing

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/using-e-transmit-api-in-net-to-find-external-references-in-a-drawing.html

## 文章内容

By Balaji Ramamoorthy
The e-Trasmit API is exposed using COM (AcETransmit18.tlb) and so, you will first need to create an inter-op assembly for use in your .Net project. You can add reference from the COM tab and select "Transmittal 18.0 Type Library" in which case Visual Studio will create the inter-op assembly. The other way is to create it yourself using the type library importer tool and add reference to the generated inter-op assembly. Now, you are all set to use the e-Transmit API.
Here is a sample code :
using TRANSMITTALLib;
  [CommandMethod("eTransmitRef")]
static public void TestMethod()
{
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      TransmittalFile tf;
    TransmittalOperation  to = new TransmittalOperation();
      // Path of the drawing file for which we need
    // the external references
    string dwgFile = @"C:\Temp\Test2013.dwg";
    if (to.addDrawingFile(dwgFile, out tf)
                                == AddFileReturnVal.eFileAdded)
    {
        TransmittalFilesGraph tfg = to.graphInterfacePtr();
        TransmittalFile rootTF = tfg.getRoot();
          List<TransmittalFile> tfList = new List<TransmittalFile>();
        tfList.Add(rootTF);
          while (tfList.Count > 0)
        {
            tf = tfList[0];
            tfList.RemoveAt(0);
              int numberOfDependents = tf.numberOfDependents;
            for (int i = 0; i < numberOfDependents; ++i)
            {
                TransmittalFile childTF = tf.getDependent(i);
                tfList.Add(childTF);
                  string sourcePath = childTF.sourcePath;
                  ed.WriteMessage(Environment.NewLine + sourcePath);
            }
        }
    }
}

## 评论

**内容**: wuquan said...
HELLO,
Transmittal 18.0 Type Library; in which version of AUTO CAD?
I install the AutoCad 2010 LT, but I can't find the Transmittal 18.0 Type Library.
Reply
05/17/2015 at 11:33 PM

---
**内容**: Balaji said in reply to wuquan...
Hi,
You should find under "C:\Program Files\Common Files\Autodesk Shared"
18.0 should be for AutoCAD 2010. You can find the list here :
http://www.cadforum.cz/cadforum_en/products.asp
But, the above code snippet cannot work in AutoCAD LT as customizing it is not supported. Please try it in full version of AutoCAD.
Regards,
Balaji
Reply
05/17/2015 at 11:47 PM

---
**内容**: wuquan said in reply to Balaji...
Thanks!
Reply
05/18/2015 at 12:17 AM

---
**内容**: Sam Shen said...
Hi Balaji, nice to see you had made it work before, can you help to have a look this:
I tried to do samething on my laptop , as below:
(1)Installed a AutoCAD 2010
(2)Create a new C# project
(3)Added a reference of "Transmittal 18.0 Type Library“ to the project
(4)Tried to compile and run the example source code
and I met an exception says "Retrieving COM factory CLSID {2A45DA6A-F580-4F3F-81D3-F263C4F5C44B} component failed due to the error: 80040154"
The component if we check "inproc" is another dll : eTransmit.dll
looks like the interop dll used an external reference dll, I am now confused.

Reply
01/27/2018 at 09:47 PM

---
