---
title: "BlockView Sample Refactored"
date: 2022-11-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - ObjectARX
description: "BlockView is an ObjectARX graphics sample which use to be shipped with ObjectARX in previous year"
author: Autodesk
---
# BlockView Sample Refactored

发布日期: 2022-11-01

原始链接: https://adndevblog.typepad.com/autocad/2022/11/blockview-sample-refactored.html

## 文章内容

By Madhukar Moogala
BlockView is an ObjectARX graphics sample which use to be shipped with ObjectARX in previous year
I've recently recieved a request from an ADN partner
The problem
If we are running in 2022 or 2023 and we have Hardware Acceleration turned ON. We get some graphics not showing up in our CGsPreviewCtrl. Specifically the void CGsPreviewCtrl::RubberRectangle(CPoint startPt, CPoint endPt) will not display on the view. Again, this only occurs in AutoCAD 2022 & 20223, on Windows 11 with Hardware Acceleration turned ON. If we turn OFF hardware acceleration it works, or if we run on Windows 10 or if on AutoCAD 2021 and before it appears to work.
Reason
We start to support DX12 from AutoCAD 2022. DX12 uses flip mode but GDI uses blit mode. The issue happens because the below code attempt to use GDI to draw over a Window used by DX12.
void CGsPreviewCtrl::RubberRectangle(CPoint startPt, CPoint endPt) 
{
  // get the device context for the client area
  CDC *cdc = this->GetDC();
  // if ok
  if (cdc != NULL)
  {
    HDC hdc = cdc->GetSafeHdc();
    // Create a black pen with a dotted style to draw the border of the rectangle.
    HPEN gdiPen = CreatePen(PS_DOT, 1, RGB(0,0,0));
    // Set the ROP cdrawint mode to XOR.
    SetROP2(hdc, R2_XORPEN);

    // Select the pen into the device context.
    HGDIOBJ oldPen = SelectObject(hdc, gdiPen);

    // Create a stock NULL_BRUSH brush and select it into the device
    // context so that the rectangle isn't filled.
    HGDIOBJ oldBrush = SelectObject(hdc, GetStockObject(NULL_BRUSH) );

    // Now XOR the hollow rectangle on the Graphics object with
    // a dotted outline.
    Rectangle(hdc, startPt.x, startPt.y, endPt.x, endPt.y);

    // Put the old stuff back where it was.
    SelectObject(hdc, oldBrush); // no need to delete a stock object
    SelectObject(hdc, oldPen);
    DeleteObject(gdiPen);  // but we do need to delete the pen

    // Return the device context to Windows.
    this->ReleaseDC(cdc);
  }
}
It is highly recommended to move away from GDI API
In case you can't invest in upgrading the code, you can use following workaround to set GFXDX12=0 and close AutoCAD, it will switch to DX11
We updated the old Arx sample to work effectively without switching to DX11 in AutoCAD 2022 and later version.
Github - BlockView

## 评论

**内容**: lolbeans said...
This is a really well-written article. Without a sure, this is among the most outstanding entries I've ever seen. Your work is amazing, and it motivates me to improve. I respect you.
Reply
11/20/2022 at 07:45 PM

---
**内容**: fireboy and watergirl said...
I am really happy to visit your blog. Now I have found what I really want. I check your blog everyday and try to learn something from your blog. Thank you and waiting for your new post.
Reply
02/10/2023 at 01:35 AM

---
**内容**: Bella said...
Writing in college as a foreign student can be a daunting task. However, by taking the time to learn about the resources available to you, you can gain the skills and confidence necessary to succeed. First and foremost, it is important to familiarize yourself with the expectations of your professors. Different cultures and countries can have different expectations when it comes to writing. For example, some professors may prefer essays that are more analytical and argumentative, while others may prefer more descriptive writing. By understanding the expectations of your professor, you can adjust your writing accordingly.
Reply
03/21/2023 at 03:22 PM

---
**内容**: soccer random said...
Finally, I have achieved my goal. The site and the adventurous spots it recommends are both excellent.
Reply
03/30/2023 at 02:15 AM

---
**内容**: Kornel said...
Nice to see this BlockView evolving, however there is still an issue with the OrbitGadget and the ZoomWindowGadget defined in the GsPreviewCtrl.h header file. They are simply not working/showing. No matter wether hw-acceleration is enabled or not, they will never show up in the preview. I had it working in the old days of Acad2009, but with newer versions no luck. Anyone knows how to fix it?
Reply
03/30/2023 at 11:53 PM

---
**内容**: JamesOneil said...
An automatic blog and its production is witnessed for the top questions to ask your video production agency before hiring
of the terms for the citizens. Skills are held for the final report. The term is held for the ultimately followed items for the challenges.
Reply
04/14/2023 at 07:33 AM

---
**内容**: Robert Gottlieb said...
I am very interested in AutoCAD and it is my profession. And I got very good information about AutoCAD from this post of yours. Now let me tell you these Eddie Van Halen Overalls are the best in this winter season.
Reply
01/29/2024 at 03:44 AM

---
**内容**: Jolie Keva said...
I feel very grateful that I read this. It is very helpful [url=https://watermelon-game.io]suika watermelon game[/url] and very informative and I really learned a lot from it.
Reply
02/18/2024 at 11:54 PM

---
