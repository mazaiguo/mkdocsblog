---
title: "ADN AutoCAD Utilities"
date: 2012-08-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
description: "The ADN AutoCAD Utilities are a set of ActiveX® controls and utilities developed by the ADN Developer Technical Services team to expose functionali..."
author: Autodesk
---
# ADN AutoCAD Utilities

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/adn-autocad-utilities.html

## 文章内容

By Balaji Ramamoorthy
The ADN AutoCAD Utilities are a set of ActiveX® controls and utilities developed by the ADN Developer Technical Services team to expose functionality that is not easily implemented using the existing official AutoCAD APIs. The controls may be used free of charge for application development and deployment, subject to the terms and conditions defined in the License Agreement.
These are controls that were previously posted to the ADN website that we’re now posting in public.
 
The controls are covered by a license agreement – which must be accepted as part of the installation process. It is important to read the license agreement before using the controls in your own applications.
What you get with this install:
1) The utilities and controls
2) Help document and samples
3) Merge Modules for the utilities and controls. These are installer modules that you can merge into the MSI installer for your own application, allowing you to distribute the utilities with your applications that use them. Please look up the documentation in the Merge Modules section for more information.
Note: Some of these utilities are OCX controls while the others are provided as ObjectARX® applications. For consistency, none of the utilities are registered during installation of this package. Therefore, please ensure you register these utilities before use. All the ActiveX controls (*.OCX and *.DLL) can be registered by simple running the "regsvr32" command (e.g. regsvr32 AcadLayer.ocx) in the command line. The ObjectARX applications are self registering and would register themselves the first time they are loaded into AutoCAD.
Download ADNUtilities2013_X64
Download ADNUtilities2013_Win32

## 评论

**内容**: Jimmy Bergmark - JTB World said...
Thanks for posting but it would be better I think to just have the files zipped because now I need to install them on two separate machines to get the files for both 32-bit and 64-bit.
Reply
08/12/2012 at 11:09 PM

---
**内容**: Balaji said in reply to Jimmy Bergmark - JTB World...
Hi Jimmy,
Thanks for pointing it out.
If you are trying to install it on a 32 bit system, the 64 bit installer wouldnt work. But, on a 64 bit system, you can run the 32/64 bit installers to get the contents.
You are right, It would be much easier if we packaged it as a zip, but it is easier to include the EULA in an installer. I am discussing this with my colleagues, to see if it can be provided as a zip.
Thank you.
Reply
08/13/2012 at 10:40 PM

---
**内容**: Gopinath Tage said in reply to Jimmy Bergmark - JTB World...
Hi Jimmy,
Can you clarify a little? Do you need the 64 bit controls on a 32 bit machine? If so, can you explain why? If you need to install the 64 bit controls on a 32 bit machine I suspect it is only because you want to access the 64 bit merge modules. In that case, it would just be easier for us to package the merge modules separately and distribute them. Having the actual 32 and 64 bit controls on the same machine could lead to unnecessary headaches.
Reply
08/14/2012 at 11:12 PM

---
**内容**: Jimmy Bergmark - JTB World said in reply to Gopinath Tage...
My build machine is 32-bit where I build for both 32-bit and 64-bit. But it is not a big deal, I just installed on the 64-bit machine and copied the 64-bit files I needed. I don't use the merge modules though.
Reply
08/14/2012 at 11:29 PM

---
**内容**: User48 said...
These are simply not worth the hassle you will experience with registration issues. These types of controls and functions need to be built into AutoCAD and exposed in a ManagedFormCtrls.dll for .NET use.
Using an OCX today to put it mildly "antiquated".
Reply
08/13/2012 at 07:18 AM

---
**内容**: Balaji said in reply to User48...
Hello,
Thanks for your comments.
I agree that the use of OCX is outdated. But there are many developers who have applications built using it and we need to support them.
Using WPF, it is now much easier to create controls such as the AcadColor or AcadLineType etc.
So in my opinion, applications being written ground-up might use the OCX controls to quickly get the functionality and then move to a custom control implemented using WPF if they prefer to avoid the hassles with ActiveX controls.
Regarding having such controls built into AutoCAD, I am not sure if that can happen anytime soon because they will need to be prioritized against other tasks by the engineering team.
Reply
08/13/2012 at 10:51 PM

---
**内容**: Maksim Sestic said...
Thanks for posting updated controls. I presume that .arx is R19 compatible?
Reply
10/09/2012 at 01:56 AM

---
**内容**: Balaji said in reply to Maksim Sestic...
Hi Maksim,
Yes. That's right.
Reply
10/10/2012 at 01:34 AM

---
**内容**: Paolo said...
Many thanks....
Reply
01/12/2014 at 04:08 PM

---
**内容**: rplees@hotmail.com said...
I tested DwgThumbnail.ocx and this version works to 2007.
With dwg version 2010 and higher there is runtime error 321: Invalid file format!
Is there a newer DwgThumbnail.ocx or something for dwg version 2013 or 2014?
mvg
Rene Plees
Belgium
Reply
02/04/2014 at 03:53 AM

---
**内容**: Balaji said in reply to rplees@hotmail.com...
Hi Rene,
This is the latest version of the DwgThumbnail. This should work ok for 2013 drawings as well.
Have you tried the sample project that is bundled with the utilities ? Does it also crash ?
Can you please provide a buildable sample project to demonstrate the crash ? You can email it to me at "balaji dot ramamoorthy at autodesk dot com"
Regards,
Balaji
Reply
02/05/2014 at 02:17 AM

---
**内容**: rplees@hotmail.com said in reply to Balaji...
Hallo Balaji,
Thanks for you answer,
I have tested DwgThumbnail.ocx on a VBA form (DwgThumbnail1.DwgFileName = Testfilename) with AutoCad Electrical 2013. (where Testfilename is a path to a valid dwg file) With Testfilename saved as 2013 there comes an error msg: Invalid file format! When saving Testfilename back to version 2010 or 2007 all works fine. When saving again the same Testfilename to version 2013 the error comes back.
Therefore i think the problem is not in the vba programcode. Probably there is an other problem, the preview in the project explorer from Electrical also does not work with 2013 drawings. (windows register to an older version ??) In the windows explorer preview pane all versions works normal up to 2013.
Thanks
Rene
Reply
02/07/2014 at 06:11 AM

---
