---
title: "Turn on/off the running osnap"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "To turn on or off the running osnap, simply set the SNAPMODE system variable to 1 or 0."
author: Autodesk
---
# Turn on/off the running osnap

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/turn-onoff-the-running-osnap.html

## 文章内容

By Balaji Ramamoorthy
To turn on or off the running osnap, simply set the SNAPMODE system variable to 1 or 0.
Here is a sample code :
// Turn-off running osnap
Application.SetSystemVariable("SNAPMODE", 0);
  // Turn-on running osnap
Application.SetSystemVariable("SNAPMODE", 1);
The various osnap options are governed by the value of the OSMODE system variable. Here is a post that describes setting of the OSMODE system variable. The values that the OSMODE system variable can take can be found in the AutoCAD documentation.
Prior to AutoCAD 2009, If object snap (Osnap) is turned off, AutoCAD adds 16384, to the current setting for the variable OSMODE. This allows applications to identify the current setting for OSMODE.
For instance, when you activate the "endpoint" object snap and Osnap is enabled, OSMODE contains 1 as its value. If object snap is disabled, OSMODE will contain 16385 as its value (1 + 16384).
Here is a sample code for this :
Int16 osmode = (Int16)Application.GetSystemVariable("OSMODE");
String msg = String.Empty;
if ((osmode & 16384) == 0)
{
    msg = String.Format
            (
                "OSnaps are Disabled. Value of OSMODE = {0}",
                osmode
            );
}
else
{
    msg = String.Format
            (
                "OSnaps are Enabled. Value of OSMODE = {0}",
                osmode
            );
}

## 评论

**内容**: Anonymoose said...
It appears the author is not familiar with the correct way to work with bitwise-encoded values like the OSMODE system variable.
To answer the question of whether OSMODE is enabled or not, this is how it should be done.
short osmode = (short) Application.GetSystemVariable("OSMODE");
string msg = string.Empty;
if( ( osmode & 16384 ) == 0 )
msg = "OSNAPs are enabled";
else
msg = "OSNAPs are disabled";
Reply
05/31/2012 at 09:03 PM

---
**内容**: Balaji said...
It really does not matter in this case because AutoCAD sets the MSB (Most Signifcant Bit).

Consider this, if we are to check for the MSB :
100 in binary = 4 in decimal
101, 111 are both greater than 100 and hence the > check.
If you are using newer versions of AutoCAD, all you have to do is to check for the SNAPMODE system variable.
Thanks for your comments
Reply
06/01/2012 at 03:35 AM

---
**内容**: Owen Wengerd said in reply to Balaji...
The code fails to demonstrate proper programming practice and it will break in the future if new bits are added to OSMODE. It is embarassing code that reflects badly on you and on Autodesk, which should matter.
Reply
06/01/2012 at 08:25 AM

---
**内容**: eura dick said in reply to Owen Wengerd...
well... here we are 4 years later.. and this code is still valid.. way to be a douche
Reply
08/24/2016 at 05:52 AM

---
**内容**: Owen Wengerd said in reply to eura dick...
Notice that Balaji corrected the original post.
Reply
08/24/2016 at 08:54 AM

---
**内容**: Anonymoose said in reply to Balaji...
It really does matter because we are not assuming anything about what other flags AutoCAD may or may not set, now or in the future, and because of the simple fact that testing bits in a byte-encoded value is not supposed to be done using > or other relational operators, because that is what the logical operators &, | and ~ are for.
Reply
06/03/2012 at 01:25 AM

---
**内容**: Balaji said in reply to Anonymoose...
Done
Reply
06/03/2012 at 10:45 PM

---
**内容**: govardhan chindam said in reply to Balaji...
Hello, evryone,
i am an autocad user , we have a customized autoplant , when we are trying to place any "customized autoplant component" osnap tick boxes (center , mid point etc ) are getting off and when ever i come out of the command , and when i using default autoplant components everything is alright .
osmode variabe is 16383
can you please any one you let me know the problem ?
thanks & regards,
Govardhan chindam,
govardhan.chindham@gmail.com,
9560916423
Reply
05/27/2018 at 10:23 PM

---
**内容**: Jeffrey said...
How do I use this code? I'm trying to get AutoCAD to stop snapping to objects when OSNAP is turned off.
Reply
07/27/2016 at 08:39 AM

---
**内容**: govardhan chindam said...
HI balaji,
i am an autocad user , we have a customized autoplant , when we are trying to place any "customized autoplant component" osnap tick boxes (center , mid point etc ) are getting off and when ever i come out of the command , and when i using default autoplant components everything is alright .
osmode variabe is 16383
can you please any one you let me know the problem ?
thanks & regards,
Govardhan chindam,
govardhan.chindham@gmail.com,
Reply
05/27/2018 at 10:23 PM

---
