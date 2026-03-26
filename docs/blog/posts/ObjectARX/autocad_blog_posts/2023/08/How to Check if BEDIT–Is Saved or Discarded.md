---
title: "How to Check if BEDIT–Is Saved or Discarded"
date: 2023-08-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - XREF
description: "This is in continuation to How to Check if XREF Edit In Place Is Saved or Discarded - AutoCAD DevBlog (typepad.com)"
author: Autodesk
---
# How to Check if BEDIT–Is Saved or Discarded

发布日期: 2023-08-01

原始链接: https://adndevblog.typepad.com/autocad/2023/08/how-to-check-if-beditis-saved-or-discarded.html

## 文章内容

By Madhukar Moogala
This is in continuation to How to Check if XREF Edit In Place Is Saved or Discarded - AutoCAD DevBlog (typepad.com)
I have received query how similar thing can be achieved for Block Edit in place.
We can retrieve this information from acedGetBlockEditMode


class XrefCheckEditor : public AcEditorReactor {

virtual void commandEnded(const TCHAR* cmdStr) {
if (wcscmp(cmdStr, L"REFCLOSE") == 0)
{
   
 switch (EditInPlaceXref::XrefState)
 {
 case EditInPlaceXref::Saved:
  acutPrintf(L"\n Modifications To In External Reference Are Saved");
  EditInPlaceXref::Reset();
  break;
 case EditInPlaceXref::Discarded:
  acutPrintf(L"\n Modifications To In External Reference Are Discarded");
  break;
 default:
  break;
 }

}
if (wcscmp(cmdStr, L"BCLOSE") == 0) {
 const bool bSaveHappened = (::acedGetBlockEditMode() & kBlkEditModeBSaved) != 0;
 if (bSaveHappened)
 {
  acutPrintf(L"\n Block Reference is Saved");
 }
 else
 {
  acutPrintf(L"\n Block Reference is Not Saved");
 }
}
}
};

## 评论

**内容**: santiago said...
Muchas gracias!!!
Reply
08/08/2023 at 01:27 AM

---
**内容**: getting over it said...
I appreciate what useful information that you share.
Reply
09/13/2023 at 01:47 AM

---
**内容**: stumble guys said...
Stumble Guys, a Fall Guys ripoff, is currently number one on the free iPhone game charts in both the US and the UK.
Reply
10/01/2023 at 08:06 PM

---
**内容**: driving directions said...

This essay is excellent and really helpful. I've been silently practicing this, and I'm becoming better at it! Enjoy yourself, work harder, and develop your impressiveness
Reply
10/18/2023 at 08:50 PM

---
**内容**: gorilla tag said...
This is an amazing and informative article that covers so much ground.
Reply
11/07/2023 at 11:48 PM

---
**内容**: Bandle said...
Like any skill, regular practice is key to improving your performance in Bandle.
Reply
06/24/2024 at 01:16 AM

---
