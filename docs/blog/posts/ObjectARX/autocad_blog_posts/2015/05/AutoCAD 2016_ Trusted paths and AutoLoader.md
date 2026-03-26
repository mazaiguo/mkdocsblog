---
title: "AutoCAD 2016: Trusted paths and AutoLoader"
date: 2015-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - CUI
  - Plugin
description: "In AutoCAD 2014, we introduced Trusted Locations (TRUSTEDPATHS).   “Trusted Paths” are in concept a “white list” of locations that the CAD manager ..."
author: Autodesk
---
# AutoCAD 2016: Trusted paths and AutoLoader

发布日期: 2015-05-01

原始链接: https://adndevblog.typepad.com/autocad/2015/05/autocad-2016-trusted-paths-and-autoloader.html

## 文章内容

By Virupaksha Aithal
In AutoCAD 2014, we introduced Trusted Locations (TRUSTEDPATHS).   “Trusted Paths” are in concept a “white list” of locations that the CAD manager can audit and maintain for add-ins and customizations loaded into AutoCAD.  AutoCAD allows signed files to be loaded from outside of this “whitelist” without SECURELOAD warnings, with the exception that AutoCAD 2016 will check if the publisher of the signed app is in the users trusted publisher certificate store.  The “best practice” is to ensure the “trusted locations” are only writable with Administrator permissions.
Applications utilizing the "autoloader" functionality within AutoCAD have the options to install to the following locations:
%APPDATA%\Autodesk\ApplicationPlugins
%ALLUSERSPROFILE%\Autodesk\ApplicationPlugins
%ProgramFiles%\Autodesk\ApplicationPlugins
%ProgramFiles(x86)%\Autodesk\ApplicationPlugins (In 64-bit OS)
In AutoCAD 2014 & 2015 - %ALLUSERSPROFILE%\Autodesk\ApplicationPlugins and %Appdata%\Autodesk\ApplicationPlugins – are by default trusted paths.
With AutoCAD 2016, only the Program files folder (C:\Program Files\Autodesk\ApplicationPlugins and C:\Program Files (x86)\Autodesk\ApplicationPlugins ) is trusted by default.
This means, when you try to load an unsigned add-in from any location outside of the "trusted locations" you will get a warning message like the one shown below. Note that in AutoCAD 2016 the user can choose to “always trust this app” – if they do, the warning will not be triggered again.
              Signed add-ins with publishers that haven’t been “trusted” by the user will trigger this kind of warning, below.  Note the user can add the publisher to the certificate store by selecting “always trust applications from…” and then they won’t be asked again for that publisher.
                    To avoid warnings, you need to:
Sign all your add-in files with your own digital signature and add your certificate to the local machine’s trusted certificates cache. Attaching a digital signature affords a basic level of security to help designate the publisher of the application and to help guarantee that the application hasn't been tampered with since it was distributed by the signer. We recommend that an app be signed regardless of where it is installed.
OR
Install to a trusted folder (for example C:\Program Files\Autodesk\ApplicationPlugins.) Note that AutoCAD implicitly trusts the AutoCAD install folder and all subfolders under it and C:\Program Files\Autodesk\ApplicationPlugins and all its subfolders. These are considered "trusted locations."
It is strongly recommend to sign your add-in as more and more of AutoCAD customers - particularly larger customers – are requiring any files installed on their networks to be signed.
Related blogs:
Digitally signing plug-in files
Trusted publishers
DevTV AutoCAD 2016
Through the Interface – Security
Autodesk Help:
About Digitally Signing Custom Program Files

## 评论

**内容**: Peter2 said...
Hi Viru
you wrote:
----
To avoid this warning, you need to:
Add the ...,
Sign all ...
----
I suppose it is meant as "OR": "Add... OR Sign ...". Right?
Peter
Reply
05/21/2015 at 03:16 AM

---
**内容**: Virupaksha Aithal said in reply to Peter2...
Thanks for the feedback. I have corrected the post (added OR)
Viru
Reply
05/21/2015 at 04:06 AM

---
**内容**: Steve said...
Is there a way to set add a Trusted Path from the bundle PackageContents.xml?
Reply
07/02/2021 at 09:00 AM

---
