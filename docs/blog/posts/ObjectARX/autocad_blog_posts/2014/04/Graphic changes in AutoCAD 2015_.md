---
title: "Graphic changes in AutoCAD 2015:"
date: 2014-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Below are some of the important Graphic changes with respect to AutoCAD 2015."
author: Autodesk
---
# Graphic changes in AutoCAD 2015:

发布日期: 2014-04-01

原始链接: https://adndevblog.typepad.com/autocad/2014/04/graphic-changes-in-autocad-2015.html

## 文章内容

By Virupaksha Aithal
Below are some of the important Graphic changes with respect to AutoCAD 2015.
To create “CreateAutoCADOffScreenDevice”
.NET
KernelDescriptor descriptor  = new KernelDescriptor();
descriptor.addRequirement(Autodesk.AutoCAD.UniqueString.Intern("3D Drawing"));
GraphicsKernel kernal = Manager.AcquireGraphicsKernel(descriptor);
Device dev = gsm.CreateAutoCADOffScreenDevice(kernal);
ObjectARX:
descriptor.addRequirement(AcGsKernelDescriptor::k3DDrawing);
AcGsGraphicsKernel *pGraphicsKernel =
AcGsManager::acquireGraphicsKernel(descriptor);
AcGsDevice *offDevice = pGraphicsKernel->createOffScreenDevice();
To create “CreateAutoCADModel”
.NET
Model model = gsm.CreateAutoCADModel(kernal);
ObjectARX:
AcGsModel *pModel = gsManager->createAutoCADModel(*pGraphicsKernel);
Regarding Autodesk.AutoCAD.GraphicsSystem.RenderMode:
RenderMode is retried now. Use visual style in View.
.NET
view.VisualStyle = new VisualStyle(VisualStyleType.Realistic);
ObjectARX:
pView->setVisualStyle(AcGiVisualStyle::kGouraud);
Download ObjectARX and .NET  Block View sample for AutoCAD 2015.

## 评论

**内容**: Loic Jourdan said...
Hi,
Thank you for the update.
What are the corresponding modifications in the native c++ API?
Thanks
Reply
04/08/2014 at 03:41 AM

---
**内容**: Virupaksha Aithal said in reply to Loic Jourdan...
Hi Loic,
I have updated the blog with ObjectARX code
Thanks
Viru
Reply
04/09/2014 at 04:34 AM

---
**内容**: Loic Jourdan said...
Sorry, I haven't seen the reference to ObjectArx block view sample.
Reply
04/09/2014 at 03:13 AM

---
**内容**: Virupaksha Aithal said...
Hi Loic,
Please refer final line of blog, which contains the hyperlinks to sample.
Thanks
Viru
Reply
04/09/2014 at 04:37 AM

---
**内容**: Loic Jourdan said...
Excellent, thanks a lot!
I have some issues building (x64) block view sample arx sample with visual studio 2012 update 4.
It builds correctly (only a warning below) but it results in a curiously small AsdkBlockView.arx (21KB) which is not loadable within acad.
I've tried loaded it into depenency walker to see what dependency is eventually missing and it gave me a strange result: I see no dependencies to acad or one of its libraries, only dependencies to mfc, crt and kernel (?!)
BTW, can you confirm (or invalidate) that passing false as last argument of CreateAtilImage call at the end of AsdkRenderOffScreen fails to render image using pView->getSnapShot ?
Thanks a lot.
The warning I got (looks ok, similar to those I got with former versions)
rxapi.lib(nullobid.obj) : warning LNK4254: section 'rxapi' (C0000040) merged into '.rdata' (40000040) with different attributes
Reply
04/09/2014 at 07:38 AM

---
**内容**: Kedar said...
Hi Virupaksha,
How do you create a Acgsview?
Do I have to create the Graphics Kernel, etc.? In old code, I am simply using acgsGetGsView. But that seems like deprecated.
Thanks,
K
Reply
07/11/2014 at 01:38 PM

---
**内容**: JeanPierre said...
I am using GsPreviewCtrl (from an earlier ARX example) and I followed the methods above. However, when trying to compile, I get the following:
GsPreviewCtrl.obj : error LNK2001: unresolved external symbol "__declspec(dllimport) public: static class AcUniqueString const * const AcGsKernelDescriptor::k3DDrawing"
GsPreviewCtrl.obj : error LNK2001: unresolved external symbol "__declspec(dllimport) public: static class AcGsGraphicsKernel * __cdecl AcGsManager::acquireGraphicsKernel
When I look into gs.h, I see "DRAWBRIDGE_API" being defined. What is this? What reference am I missing. Please help - very frustrated, cannot get this nice preview class to work anymore!
Regards,
JP
Reply
07/19/2014 at 01:51 PM

---
**内容**: Virupaksha Aithal said in reply to JeanPierre...
Hi,
Please add reference to AcDrawBridge.lib.
Thanks
Viru
Reply
07/21/2014 at 02:18 AM

---
**内容**: Volodymyr said...
Is it possible to run this sample on AutoCAD 2014?
Reply
10/23/2015 at 10:50 AM

---
**内容**: dba said...
Hello,
is there a (simple) way to show the ViewCube in the View, or at least mimic it in some manner?
Thanks,
Daniel
Reply
01/25/2016 at 03:57 AM

---
