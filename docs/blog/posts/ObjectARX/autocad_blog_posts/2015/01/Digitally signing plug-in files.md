---
title: "Digitally signing plug-in files"
date: 2015-01-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - Plugin
description: "Digital signature is like an electronic security mark affixed to your plug-in file. The digital signature has the details about the publisher, the ..."
author: Autodesk
---
# Digitally signing plug-in files

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/digitally-signing-plug-in-files.html

## 文章内容

By Virupaksha Aithal
Digital signature is like an electronic security mark affixed to your plug-in file. The digital signature has the details about the publisher, the independent entity who can guarantee the publisher’s identity. It also has the cryptographic checksum which is used to verify that the content has not been tampered after signing or not.
Below are the steps involved in digitally signing your plug-ins
Purchase digital signature
There are different vendors from whom you can purchase the digital signatures.
Example : Verisign, DigiCert, Thawte etc.
 Use signing tool
 Use Signtool.exe (Tool is located with Microsoft SDK toolkit) to sign your C++ or .NET plug-in.
 example : signtool sign /f <PFX file name> /p <Password> FileToSign.dll
 where <PFX file name> is digital signature file (pfx file)
  <Password> - is private key of your digital signature.
  In case of AutoCAD Lisp files, use AcSignApply.exe. You can find this tool with acad.exe 
Other useful links
Code signing http://en.wikipedia.org/wiki/Code_signing
Certificate authority http://en.wikipedia.org/wiki/Certificate_authority

## 评论

**内容**: Tim Stalin said...
Thanks for this.
What's the proper way to sign VLX files? It seems that AcSignApply.exe will sign these files and they seemingly run in AutoCAD 2016, but these signed files will fall into an infinite loop when used in an earlier version of AutoCAD. Is the solution to have a signed VLX for 2016+ and an unsigned for 2015-?
Reply
06/22/2015 at 02:52 PM

---
**内容**: Virupaksha Aithal said...
Hi,
Yes, signed vlx files will not work on AutoCAD 2015 (& earlier versions). You need to have 2 versions vlx file (signed and unsigned)
regards
Viru
Reply
06/22/2015 at 10:07 PM

---
