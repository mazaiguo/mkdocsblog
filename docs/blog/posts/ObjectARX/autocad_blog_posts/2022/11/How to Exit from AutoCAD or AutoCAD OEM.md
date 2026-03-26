---
title: "How to Exit from AutoCAD or AutoCAD OEM"
date: 2022-11-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - OEM
description: "There may be a situation where your Arx application needs to exit AutoCAD if the license check or some other business logic fails"
author: Autodesk
---
# How to Exit from AutoCAD or AutoCAD OEM

发布日期: 2022-11-01

原始链接: https://adndevblog.typepad.com/autocad/2022/11/how-to-exit-from-autocad-or-autocad-oem.html

## 文章内容

By Madhukar Moogala
There may be a situation where your Arx application needs to exit AutoCAD if the license check or some other business logic fails
When aborting, use AcDbHostApplicationServices::fatalError()
Or, acrx_abort() instead of a direct or indirect call to exit().This will allow AutoCAD and other ObjectARX applications to recover as much work as possible. Always use API calls rather than system calls.
It is highly desirable for the RealDWG host application to override this method, and do whatever needs to be done for a clean and graceful shutdown. For example, allowing the user to save some portion of the work in progress, cleaning up memory allocations, and so on are all things that should be done upon a fatal error.
extern "C" AcRx::AppRetCode
acrxEntryPoint(AcRx::AppMsgCode msg, void* pkt)
{
 AcRx::AppRetCode retVal = AcRx::kRetOK;
 switch (msg)
 {
 case AcRx::kInitAppMsg:
  //acrxDynamicLinker->unlockApplication(pkt);
  //acrxRegisterAppMDIAware(pkt);
  //initApp();

  // perform license check
  retVal = checkLicense();
  if (retVal == AcRx::kRetOK)
  {
   acrxDynamicLinker->unlockApplication(pkt);
   acrxRegisterAppMDIAware(pkt);
   initApp();
  }
  else
  {
   MessageBox(adsw_acadMainWnd(),
   L"Application should not be allowed to load.", L"Start-up Error", MB_OK + MB_ICONWARNING);
   acrx_abort(L"Invalid License: Application Quits Now");
   //or
   //acdbHostApplicationServices()->fatalError(_T("Application is Quitting Now"));     
   return AcRx::kRetError;
  }
  break;
 case AcRx::kUnloadAppMsg:
  unloadApp();
  break;
 default:
  break;

 }

 //return AcRx::kRetOK;
 return retVal;

}

## 评论

**内容**: sasuke2690 said...
How do I get back to original view in AutoCAD? spider solitaire 2 suit
Reply
11/20/2022 at 08:25 PM

---
**内容**: Quordle said...
Really helpful post! There's a lot of information here that can help any business start a social networking campaign that works
Reply
11/24/2022 at 06:51 PM

---
**内容**: vex 3 said...
Thanks for this great blog post of yours. I hope you do more.
Reply
02/10/2023 at 01:37 AM

---
**内容**: JamesOneil said...
I have read this article. I think You put how much 24 hour fitness cost
a lot of effort into creating this article. I appreciate your work.
Reply
02/27/2023 at 12:39 PM

---
**内容**: JamesOneil said...
I like this post, And I guess they are https://nail-salonsnearme.com/
to read this post, they will get a good site to generate information, thanks for sharing it with me.
Reply
02/27/2023 at 12:48 PM

---
**内容**: SpankRock said...
You are absolutely right when an error occurs, instead of being confused, you should be calm to handle it. The other day when I was playing basketball stars on my computer, suddenly my screen went black then ran into strange words, I calmly restarted the computer, but in the end I still had to call the mechanic because it doesn't change anything.
Reply
04/02/2023 at 08:18 PM

---
**内容**: usps tracking said...
It goes without saying that the quality of your essay is sufficient; but, I believed that seeing professional images and videos together would be a significant improvement. On usps tracking number, you will find articles and photographs pertaining to these issues; thus, I would appreciate it if you would visit and provide your feedback.
Reply
04/11/2023 at 02:40 AM

---
**内容**: Mario Games said...
In AutoCAD, how can I restore the default perspective?
Reply
05/18/2023 at 08:00 PM

---
**内容**: Quordle said...
Quordle is a unique puzzle game that offers a new challenge every day.
Reply
06/06/2023 at 09:03 PM

---
**内容**: mapquest directions said...
I really like the information you share. I learned a lot of new and useful knowledge from your post.
Reply
07/11/2023 at 02:11 AM

---
**内容**: Caption Aesthetic said...
If you want to explore some crazy aesthetic instagram captions then click here to to visit our site and explore best captions for your posts
Reply
08/10/2023 at 12:28 AM

---
**内容**: Click Here said...
Fabulous information
Reply
08/10/2023 at 12:32 AM

---
**内容**: driving directions said...
The kUnloadAppMsg message is used when unloading the application, and it calls the unloadApp() function to perform any necessary cleanup actions.
Reply
10/17/2023 at 12:07 AM

---
**内容**: quordle said...
You were doing really well. Such a great article with interesting ideas
Reply
10/18/2023 at 06:33 PM

---
**内容**: slope said...
This is an amazing and informative article that covers so much ground.
Reply
11/07/2023 at 11:46 PM

---
**内容**: retro bowl said...
The acrx_abort() function is a safer way to abort AutoCAD than calling the exit() function directly. This is because acrx_abort() allows AutoCAD and other ObjectARX applications to recover as much work as possible before exiting.
Reply
11/12/2023 at 11:17 PM

---
**内容**: mapquest driving directions said...
You do not need to be a savant to be able to move easily. Let us do it for you. Thanks to it, you can freely move anywhere you want
Reply
12/04/2023 at 12:48 AM

---
**内容**: slice master said...
this code snippet demonstrates best practices for handling initialization, cleanup, and error handling within an ObjectARX application for AutoCAD or AutoCAD OEM environments.
Reply
01/28/2024 at 06:15 PM

---
**内容**: slope said...
I am extremely appreciative and would like to extend my sincere gratitude for the provision of this extremely useful information. I am optimistic that your forthcoming pursuits will maintain their capacity to inspire and astonish me.
Reply
05/30/2024 at 03:42 AM

---
