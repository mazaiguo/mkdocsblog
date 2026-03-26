---
title: "How to create your own AutoCAD OEM Help CHM from the 2012/2013 HTML source"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
  - Unicode
description: "New in AutoCAD 2012 is the HTML help system (no more CHM). That said, contrary to what the OEM Developers Guide implies, in AutoCAD OEM, CHM’s are ..."
author: Autodesk
---
# How to create your own AutoCAD OEM Help CHM from the 2012/2013 HTML source

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-create-your-own-autocad-oem-help-chm-from-the-2013-html-source.html

## 文章内容

by Fenton Webb
New in AutoCAD 2012 is the HTML help system (no more CHM). That said, contrary to what the OEM Developers Guide implies, in AutoCAD OEM, CHM’s are still required.
Here’s how to build your AutoCAD OEM 2012/2013 CHM from the supplied HTML source files.
You will first need to download and install Microsoft HTML Help 
I’m going to use my OEM2013 install, but it should be the same in OEM 2012 also.
Where I mention OEM2013, I mean C:\Program Files\Autodesk\OEM2013
Step 1: Create default .hhp file
Using a text editor, create a new  .hhp file called MyOEMProduct.hhp and save it to the OEM2013\Help folder. The contents of this file should be as follows, edit the fields in the text file as you need:
[OPTIONS]
Auto TOC=9
Compatibility=1.1 or later
Compiled file=aoem.chm
Default Window=TriPane
Default topic=files\homepage.htm
Display compile progress=Yes Error log file=log.log
Full-text search=Yes
Language=0x409 English (United States)
[WINDOWS]
TriPane="AutoCAD Whatever",,,,"files\homepage.htm",,,,,0xe3520,255,0x304e,[0,0,800,600],,,,,,,0
[FILES]
index.html
Step 2: Copy the context help .htm files to the OEM2013\Help folder
Move or copy all the files from the OEM2013\Help\ConextHelp subfolder to the OEM2013\Help folder.
Step 3: Repair the relative paths in the htm files
Next, recursively replace all *.htm files which have the text
.replace(‘../files
with
.replace(‘./files
Step 4: Update the Java Script so it does nothing
Edit common-processing.js so that the initFrame() just returns or comment out the entire function…
e.g.
function initFrame(url,topicNumber,index,hash)
{
return; // just return and do nothing

    if (top == self) {
        var hashWithoutSharp;
        if (hash !== undefined) {
            hashWithoutSharp = hash.substring(1);
        }
        window.location.replace('../' + index + '?url=' + url + ',topicNumber=' + topicNumber + ((hashWithoutSharp) ? ',hash=' + hashWithoutSharp : ''));
    }
}
Step 5: Load your .hhc into HTML Help
Using HTML Help, load your MyOEMProduct.hhc into HTML Help. Be careful about permissions to the OEM2013\Help folder, if needed, change the owner of Program Files to be yourself (with full permissions) otherwise HTML Help may not be able to save.
Step 6: Add all help files to the HTML Help Project
In DOS, create an hhp file by redirecting the file listing from DIR to a hhp file… e.g.
dir *.htm /B /S /R >> MyOEMProduct.hhp
dir style /B /S /R >> MyOEMProduct.hhp
dir scripts /B /S /R >> MyOEMProduct.hhp
dir images /B /S /R >> MyOEMProduct.hhp
dir html /B /S /R >> MyOEMProduct.hhp
dir files /B /S /R >> MyOEMProduct.hhp
Step 7: Save the HTML Project and quit HTML Help.
Step 8: Edit style\acad.css to remove broken banners
To get rid of the broken buttons in the banner, in style\acad.css make the following changes.
Change
.headNavLinkShare {
margin: 35px -18px 0 -18px;
position:absolute;
}
To
.headNavLinkShare {
                display: none;
}

Change
.headNavLinkAddToFav {
margin: 35px -47px 0 -47px;
position:absolute;
}
To
.headNavLinkAddToFav {
                display: none;
}
Change
.headNavLinkHome {
margin: 35px -76px 0 -76px;
position:absolute;
}
To
.headNavLinkHome {
                display: none;
}
Step 9: Create the Table of Contents (Optional)
Normal AutoCAD does not have a Table Of Contents, but you can create your own if you want. Doing this will require substantial work to implement it correctly, so this is optional.
In HTML Help, simply click on the ‘Contents’ tab to create a TOC.
Step 10: Build the CHM using HTML Help 
Reload your MyOEMProduct.hhc into HTML Help and then hit the Generate button
Step 11: Sit back
…watch as HTML Help generates the CHM file you!
If you have any high quality cigars to hand, you may want to use this time to select one from the box, clip the end off using your favourite cigar clipper, light up then place your alligator skin boots on the table in front of you to enjoy.

## 评论

**内容**: Don said...
Hi Fenton,
Can you send me a CHM from the AutoCAD 2013 HTML source?
Thanks.
Don
Reply
02/11/2013 at 01:11 PM

---
**内容**: Don said...
If you can just send me a OEM2013 CHM, I can create the content from that. If you can that would help me out a great deal. Please contect me via email if you prefer.
Thanks Fenton.
Don
Reply
02/11/2013 at 01:21 PM

---
**内容**: Fenton Webb said...
Hey Don!
Sorry, but AutoCAD Help is HTML form now. Hence why I describe how to build it above.
Reply
02/11/2013 at 03:57 PM

---
**内容**: Don said...
Yes, I understand that. I thought maybe you had already created a CHM based on your procedure in this post. I was asking for a copy of the CHM (if you have one available).
Reply
02/14/2013 at 01:30 PM

---
**内容**: Fenton Webb said...
Sorry Don, don't have - I actually had to wipe my machine shortly after
Reply
02/14/2013 at 02:31 PM

---
**内容**: Stefan said...
Hi Fenton.
I have tried to build a chm file for our OEM product.
It works fine, but is it possible to get the search window on default topic (like the index.html)? I only get the right side of the "index.html" window (homepage.htm).
Thank you,
Stefan
Reply
02/26/2013 at 01:18 AM

---
**内容**: Craig said...
Hi Fenton,
I was interested to try this. I think I must have missed something because I get compilation errors i.e.
HHC5003: Error: Compilation failed while compiling scripts\ACD.
Also with scripts\ACG, scripts\ACR, scripts\AUG and scripts\DPG.
I also get script errors when viewing the chm file which may be as a result.
Any thoughts?
Thanks.
Craig
Reply
08/27/2013 at 08:48 AM

---
**内容**: Balaji said in reply to Craig...
Hi Craig,
Sorry, this is too late to be of any help to you. But just wanted to share in case anyone else has the same issue.
I was following the steps from this blog post and had similar issues as you reported. You may be replacing
"../files" with "./files" in step 3.
It is important to find and replace ".replace('../files" with ".replace('./files" as mentioned in the blog post. Also, please ensure that when you first create the .hhp file, the cursor at the end is at an empty line. When files are added in Step 6, it will append it to the end of the .hhp file, so without the additional line, it can end up appending incorrectly.
Following the steps in this blog post line-by-line, the chm built just fine.
Fenton's blog posts are so full of details, cant afford to miss a step. So I followed even step 11 :)
Regards,
Balaji
Reply
07/08/2014 at 03:29 AM

---
