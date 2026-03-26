---
title: "Registry values for ProductID and LocaleID for AutoCAD and the vertical products"
date: 2013-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "HKEYLOCALMACHINE\Software\Autodesk\AutoCAD\R20.0\ACAD-E001:409 What is ACAD-E001:409?"
author: Autodesk
---
# Registry values for ProductID and LocaleID for AutoCAD and the vertical products

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/registry-values-for-productid-and-localeid-for-autocad.html

## 文章内容

By Virupaksha Aithal
HKEY_LOCAL_MACHINE\Software\Autodesk\AutoCAD\R20.0\ACAD-E001:409 What is ACAD-E001:409?
R20.0 is the release number, the this corresponds to AutoCAD 2015
These digits like E000:409 are a ProductID (E000) and a LocaleID (409).
The ProductID structure is a 4-digit value. However, prior to AutoCAD 2006, the ProductID structure was only 3-digits with a single [p] value. Due to the number of products based on AutoCAD, in AutoCAD 2006 structure was changed to 4-digits.
From AutoCAD 2006 forward, the structure is configured as "[n][r][pp]", where:
[n] = Number representing AutoCAD base release (see below)
[r] = Release number within AutoCAD base, reset to zero for every new n
[pp] = Product based on AutoCAD (see below)
ProductID Assignments (Assigned [n] Values)
F = AutoCAD 2016
E = AutoCAD 2015
D = AutoCAD 2014
B = AutoCAD 2013
A = AutoCAD 2012
9 = AutoCAD 2011
8 = AutoCAD 2010
7 = AutoCAD 2009
6 = AutoCAD 2008
5 = AutoCAD 2007
4 = AutoCAD 2006
3 = AutoCAD 2005
2 = AutoCAD 2004
1 = AutoCAD 2002
The LocaleID structure is a 4-character hex representation of the product's locale / language.
Here is a list of LocaleID - Language Abbreviation - Language
409 ENU English
407 DEU German
040C FRA French
410 ITA Italian
040A ESP Spanish
415 PLK Polish
040E HUN Hungarian
405 CSY Czech
419 RUS Russian
416 PTB Brazilian Portuguese
804 CHS Simplified Chinese
404 CHT Traditional Chinese
412 KOR Korean
411 JPN Japanese
ProductID's for AutoCAD 2016-based products:
F001 AutoCAD 
ProductID's for AutoCAD 2015-based products:
E000 Autodesk Civil 3D
E001 AutoCAD (ACAD)
E00A AutoCAD OEM
E002 Map
E004 AutoCAD Architecture
E005 AutoCAD Mechanical (ACADM)
E006 Building Systems (AutoCAD MEP)
E007 AutoCAD Electrical (ACADE)
E009 AutoCAD LT (ACLT)
E013 Inventor Professional (AIP)
E016 AutoCAD P & ID - 2D
E017 AutoCAD Plant 3D
E022 Autodesk Utility Design
E028 DWG TrueView
E029 AutoCAD ecscad
E030 AutoCAD Structural Detailing
ProductID's for AutoCAD 2014-based products:
D000 Autodesk Civil 3D
D001 AutoCAD (ACAD)
D00A AutoCAD OEM 
D002 Map
D004 AutoCAD Architecture
D005 AutoCAD Mechanical (ACADM)
D006 Building Systems
D007 AutoCAD Electrical (ACADE)
D009 AutoCAD LT (ACLT)
D013 Inventor Professional (AIP)
D016 AutoCAD P & ID - 2D
D017 AutoCAD Plant 3D
D022 Autodesk Utility Design
D028 DWG TrueView
D029 AutoCAD ecscad 
D030 AutoCAD Structural Detailing

ProductID's for AutoCAD 2013-based products:
B000 Autodesk Civil 3D
B001 AutoCAD 
B00A AutoCAD OEM
B002 Map
B004 AutoCAD Architecture
B005 AutoCAD Mechanical (ACADM)
B006 Building Systems
B007 AutoCAD Electrical (ACADE)
B009 AutoCAD LT
B013 Inventor Professional (AIP)
B016 AutoCAD P & ID - 2D
B017 AutoCAD Plant 3D
B022 Autodesk Utility Design
B028 DWG TrueView
B029 AutoCAD ecscad
B030 AutoCAD Structural Detailing
ProductID's for AutoCAD 2012-based products:
A000 Autodesk Civil 3D
A001 AutoCAD 
A001 DwgViewer (DWGVIEWR)
A00A AutoCAD OEM (AOEM)
A002 Map
A003 Inventor Series (AIS)
A004 AutoCAD Architecture
A005 AutoCAD Mechanical (ACADM)
A006 Building Systems
A007 AutoCAD Electrical (ACADE)
A008 Land Desktop
A009 AutoCAD LT (ACLT)
A012 ADT for Raster Design
A013 Inventor Professional (AIP)
A014 Inventor Professional for Routed Systems (AIPRS)
A015 Inventor Professional for Simulation (AIPSIM)
A016 AutoCAD P & ID - 2D
A017 AutoCAD Plant 3D
A018 Civil 3D Land Desktop Companion
A022 Autodesk Utility Design
A023 Autodesk Topobase Client
A024 Autodesk Civil
A028 DWG TrueView
A029 AutoCAD ecscad
A030 AutoCAD Structural Detailing
ProductID's for AutoCAD 2011-based products:
9000 Autodesk Civil 3D
9001 AutoCAD (ACAD)
9001 DwgViewer (DWGVIEWR)
900A AutoCAD OEM (AOEM)
9002 Map
9003 Inventor Series (AIS)
9004 AutoCAD Architecture
9005 AutoCAD Mechanical (ACADM)
9006 Building Systems
9007 AutoCAD Electrical (ACADE)
9008 Land Desktop
9009 AutoCAD LT (ACLT)
9012 ADT for Raster Design
9013 Inventor Professional (AIP)
9014 Inventor Professional for Routed Systems (AIPRS)
9015 Inventor Professional for Simulation (AIPSIM)
9016 AutoCAD P & ID - 2D
9017 AutoCAD Plant 3D
9018 Civil 3D Land Desktop Companion
9022 Autodesk Utility Design
9023 Autodesk Topobase Client
9024 Autodesk Civil
9028 DWG TrueView
9029 AutoCAD ecscad
9030 AutoCAD Structural Detailing

Here is a listing of the LocaleId which indicates the language. The LocaleId starts with the number 4, then it is immediately followed by a hexadecimal number indicating the language.
HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\AutoCAD\R20.0\ACAD-ProductId:LocaleId
FYI: The hex number is defined in winnt.h e.g.
#define LANG_NEUTRAL 0x00
#define LANG_AFRIKAANS 0x36
#define LANG_ALBANIAN 0x1c
#define LANG_ARABIC 0x01
#define LANG_ARMENIAN 0x2b
#define LANG_ASSAMESE 0x4d
#define LANG_AZERI 0x2c
#define LANG_BASQUE 0x2d
#define LANG_BELARUSIAN 0x23
#define LANG_BENGALI 0x45
#define LANG_BULGARIAN 0x02
#define LANG_CATALAN 0x03
#define LANG_CHINESE 0x04
#define LANG_CROATIAN 0x1a
#define LANG_CZECH 0x05
#define LANG_DANISH 0x06
#define LANG_DUTCH 0x13
#define LANG_ENGLISH 0x09
#define LANG_ESTONIAN 0x25
#define LANG_FAEROESE 0x38
#define LANG_FARSI 0x29
#define LANG_FINNISH 0x0b
#define LANG_FRENCH 0x0c
#define LANG_GEORGIAN 0x37
#define LANG_GERMAN 0x07
#define LANG_GREEK 0x08
#define LANG_GUJARATI 0x47
#define LANG_HEBREW 0x0d
#define LANG_HINDI 0x39
#define LANG_HUNGARIAN 0x0e
#define LANG_ICELANDIC 0x0f
#define LANG_INDONESIAN 0x21
#define LANG_ITALIAN 0x10
#define LANG_JAPANESE 0x11
#define LANG_KANNADA 0x4b
#define LANG_KASHMIRI 0x60
#define LANG_KAZAK 0x3f
#define LANG_KONKANI 0x57
#define LANG_KOREAN 0x12
#define LANG_LATVIAN 0x26
#define LANG_LITHUANIAN 0x27
#define LANG_MACEDONIAN 0x2f
#define LANG_MALAY 0x3e
#define LANG_MALAYALAM 0x4c
#define LANG_MANIPURI 0x58
#define LANG_MARATHI 0x4e
#define LANG_NEPALI 0x61
#define LANG_NORWEGIAN 0x14
#define LANG_ORIYA 0x48
#define LANG_POLISH 0x15
#define LANG_PORTUGUESE 0x16
#define LANG_PUNJABI 0x46
#define LANG_ROMANIAN 0x18
#define LANG_RUSSIAN 0x19
#define LANG_SANSKRIT 0x4f
#define LANG_SERBIAN 0x1a
#define LANG_SINDHI 0x59
#define LANG_SLOVAK 0x1b
#define LANG_SLOVENIAN 0x24
#define LANG_SPANISH 0x0a
#define LANG_SWAHILI 0x41
#define LANG_SWEDISH 0x1d
#define LANG_TAMIL 0x49
#define LANG_TATAR 0x44
#define LANG_TELUGU 0x4a
#define LANG_THAI 0x1e
#define LANG_TURKISH 0x1f
#define LANG_UKRAINIAN 0x22
#define LANG_URDU 0x20
#define LANG_UZBEK 0x43
#define LANG_VIETNAMESE 0x2a

## 评论

**内容**: Steve Hill said...
Thanks for the post Virupaksha. So then why did Autodesk skip the letter 'C' when rolling out 2014. 2012 was letter 'A', 2013 was letter 'B' and 2014 is letter 'D'.
I'm sure Autodesk has a good reason for it, and it's not because they don't know the alphabet. ;)
Reply
08/16/2013 at 05:48 AM

---
**内容**: Fenton Webb said...
Hey Steve
yes, there was a reason for it. C was a prototype version of AutoCAD which was released as a preview, but not yet rolled into the main line.
Reply
08/20/2013 at 03:47 PM

---
**内容**: Steve Hill said...
I see. Thanks Fenton.
Reply
09/05/2013 at 03:19 PM

---
**内容**: Will Baron said...
We have found an install on which the French locale ID is not as stated it was in fact not 040C, it was 40C. Which is correct, the one above or what we found after installing the French version? Does this apply to Spanish, and I guess Hungarian too? It is not that we support these languages particularly, just want to be sure the documentation is correct for all who use this.
Reply
06/05/2014 at 03:11 AM

---
**内容**: Amar said...
Hello,
I have a drawing file and it takes about 5 minutes to open. Any drawing file that is generated from a specific Lenovo machine creates this huge delay in opening the file.
It accesses the Registry a lot. I have attached the snapshot of the registry access . This was generated by ProcMon (SysInternals). Please let me know if there is any solution....
Thanks in advance....
1:41:27.2821764 PM acad.exe 4896 RegOpenKey HKLM\Software\Autodesk\AutoCAD\R20.0\ACAD-E001:409 SUCCESS Desired Access: Read
1:41:27.2821933 PM acad.exe 4896 RegQueryValue HKLM\SOFTWARE\Autodesk\AutoCAD\R20.0\ACAD-E001:409\LocaleId SUCCESS Type: REG_SZ, Length: 8, Data: 409
1:41:27.2822090 PM acad.exe 4896 RegQueryValue HKLM\SOFTWARE\Autodesk\AutoCAD\R20.0\ACAD-E001:409\LocaleId SUCCESS Type: REG_SZ, Length: 8, Data: 409
1:41:27.2822256 PM acad.exe 4896 RegCloseKey HKLM\SOFTWARE\Autodesk\AutoCAD\R20.0\ACAD-E001:409 SUCCESS
Reply
03/27/2015 at 11:47 AM

---
**内容**: Andrey Bushman said...
>E002 Map
Is it AutoCAD Map? I am asking because among products also Inventor and DWG TrueView was listed also.
>(Registry Cookie: ACLT-8001)
Does it mean the Registry Cookies is "ACAD" when it is not pointed in your list?
>(Registry Cookies: ACAD-D001; ARD-D001)
Why exist two variants? When am I to expect each of them?
Reply
04/24/2015 at 12:43 AM

---
**内容**: Andrey Bushman said...
What is Registry Cookie for Inventor and DWG Viewer?
Also, can you write the same lists for AutoCAD versions older than AutoCAD 2011? It is necessary for me for testing. Thank you.
Reply
04/24/2015 at 01:23 AM

---
**内容**: Virupaksha Aithal said in reply to Andrey Bushman...
sorry, i do not have information on AutoCAD 2011 and older versions.
Reply
04/29/2015 at 02:45 AM

---
**内容**: Andrey Bushman said...
And for AutoCAD 2016 also. :)
Reply
04/24/2015 at 01:24 AM

---
**内容**: Andrey Bushman said...
Reader of this article be careful, read this: http://www.theswamp.org/index.php?topic=49368.new#new
Reply
04/29/2015 at 02:06 AM

---
**内容**: Virupaksha Aithal said in reply to Andrey Bushman...
sorry, now, i have corrected the examples in blog (for AutoCAD 2013 as mentioned your swamp blog.)
Reply
04/29/2015 at 02:53 AM

---
**内容**: Virupaksha Aithal said...
EO02 is AutoCAD Map. I have removed ARD-D001 from the blog
Reply
04/29/2015 at 02:44 AM

---
**内容**: Andrey Bushman said...
Why you deleted all mentions about the Registry Cookies? It had useful info.
Reply
04/29/2015 at 03:44 AM

---
**内容**: Virupaksha Aithal said...
I am not in position to confirm the Registry Cookies for now. I have Inherited this document. I will update the document once i test the Cookies myself. there are still lot of Cookies which i am not able to confirm like DwgViewer , Autodesk Utility Design, DWG TrueView etc for now. but i have left them in the document.
Thanks
Viru
Reply
04/29/2015 at 08:42 PM

---
**内容**: raghu said...
dear sir when i active autocad .invalid address formatting
so i requested who to file the address line .
Reply
08/26/2015 at 02:40 AM

---
**内容**: peter said...
What is about the LocaleID's from French, Spanish and Hungarian Version?
I will confirm, that the LocaleID from french-Version is not 040C , but "40C".
Did anyone can check the Spanish an Hungarian Version?
Reply
12/14/2015 at 06:51 AM

---
**内容**: peter said in reply to peter...
confirmed: Spanish LocaleID is "40A" !
Reply
12/14/2015 at 07:51 AM

---
**内容**: Herbert said...
Is there an update with registrykeys for the 2017-versions?
Reply
06/15/2016 at 02:51 AM

---
**内容**: sandeep said in reply to Herbert...
Hi,
refer http://jtbworld.com/autocad-information
sandeep
Reply
06/16/2016 at 01:52 AM

---
**内容**: sandeep said...
Hi,
refer http://jtbworld.com/autocad-information
Reply
06/16/2016 at 01:51 AM

---
