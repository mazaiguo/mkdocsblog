---
title: "Using Entitlement API with Lisp"
date: 2022-05-01
categories:
  - AutoCAD .NET
tags:
  - API
  - AutoLISP
  - Entitlement
description: "There is an introductory briefing on Entitlement API by Daniel."
author: Autodesk
---
# Using Entitlement API with Lisp

发布日期: 2022-05-01

原始链接: https://adndevblog.typepad.com/autocad/2022/05/using-entitlement-api-with-lisp.html

## 文章内容

By Madhukar Moogala
There is an introductory briefing on Entitlement API by Daniel.
For reading brevity, I will give simple statement what it brings to the table.
Entitlement API is a rest enabled API, allows you to check if the user is entitled to access your app i.e., user has bought the app from Autodesk App Store
We have examples on .NET, C++ and now on Lisp
.NET
Please check - https://github.com/MadhukarMoogala/Entitlement/blob/9ee757fefa9be4369a0503396b8dc1b774056182/ACAD_EntitilementApi/Plugin.cs#L36
C++
Please check
https://adndevblog.typepad.com/autocad/2020/07/using-entitlement-api-within-objectarx-c.html
Lisp
For lisp we will be using IXMLHTTPRequest which provides client-side protocol support for communication with HTTP servers.
The members of the API can be found here
https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms760305(v=vs.85)

(defun c:IsEntitled (/ http response) 
  (setq appId (getstring "Enter AppId "))
  (setq userId (getvar "ONLINEUSERID"))
  (setq url (strcat "https://apps.autodesk.com/webservices/checkentitlement?userid=" 
                    userId
                    "&appid="
                    appId
            )
  )
  ;https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms759148(v=vs.85)
  (if (setq http (vlax-create-object "MSXML2.XMLHTTP")) 
    (progn 
      (vlax-invoke-method http 'open "get" url :vlax-false)
      (if 
        (not 
          (vl-catch-all-error-p (vl-catch-all-apply 'vlax-invoke (list http 'send)))
        )
        (setq response (vlax-get http 'responseText))
      )
      (vlax-release-object http)
    )
  )
  (cond 
    ((> (vl-string-search "true" response) 0) (princ "\nTrue"))
    (t (princ "\nFalse"))
  )
  (princ)
);defun

## 评论

**内容**: cuphead said...
The information you have posted is very useful.
Reply
08/25/2022 at 02:15 AM

---
**内容**: hurdle said...
I would want to express my gratitude to you for penning such an engaging article on the subject. This has given me a lot to think about, and I am looking forward to reading more.
Reply
10/17/2022 at 07:36 PM

---
**内容**: world of mario said...
That's every detailed and easy for us to understand. Thanks
Reply
11/22/2022 at 08:58 PM

---
**内容**: JamesOneil said...
I have been looking for articles on these topics
for a long time. I don't know how grateful you are for posting on this topic. Thank you for the numerous articles on this site, I will subscribe to those links in my bookmarks and visit them often.
Reply
02/27/2023 at 02:06 AM

---
**内容**: Apkohi said...
Finally I find API. I very much appreciate it. Thank you for this excellent article. Keep posting!
Reply
04/02/2023 at 01:55 AM

---
**内容**: Makayla Florance said...
An automatic use of the tool and technique is filed for the terms for the citizens. The component of the USDOT Permits is done for the joys. The margin is held for the terms. Rank is held for the vital paths for the choices for the ambit for the firm ideals in the team.
Reply
04/10/2023 at 01:39 AM

---
**内容**: LOLbeans io said...
I would like to appreciate the effort you have put into writing this blog. I hope you will have more quality articles in the near future.
Reply
05/03/2023 at 10:05 PM

---
**内容**: Five Nights at Freddy's said...
Thank you a great deal. Your post provided me with an abundance of knowledge, helping me to expand my horizons.
Reply
05/13/2023 at 09:57 AM

---
**内容**: streamzmod said...
I was searching for this API. It can also be used for gaming entertainment.
Reply
06/12/2023 at 12:04 AM

---
**内容**: LOLBEANS said...
I admire this informative article for its well-researched content and excellent wording. I was so engrossed in this material that I couldn't stop reading. I am very impressed with your work and skills. Thank you very much.
Reply
06/15/2023 at 02:09 AM

---
**内容**: oishii said...
Thank you a great deal. Your post provided me with an abundance of knowledge, helping me to expand my horizons.
Reply
06/28/2023 at 04:27 AM

---
**内容**: Robert Arnold said...
As I am a computer science student I enjoyed reading the api topic so I have an advice for you keep this The Righteous Gemstones S3 Jesse Black Suit in your fashion collection if you want to look good.
Reply
07/19/2023 at 06:15 AM

---
**内容**: Irene Torres said...
I got to use this entitlement api through your content which is very amazing. And thats why I am sharing this Destiny 2 Bungie Rewards Vow Of The Disciple Raid Jacket fashion dress with you which will be very helpful for you.
Reply
07/22/2023 at 03:54 AM

---
**内容**: Jennifer Connelly said...
Each jacket in our Heartland Jackets Collection is constructed to last. This collection includes everything you need, whether you're searching for a versatile jacket to finish your regular outfit or a standout item to up your style.
Reply
07/26/2023 at 04:58 AM

---
**内容**: katherine wolf said...
We are provide the best trending attire worldwide with free shipping and we have a vast collection of Barbie 2023 Outfits Collection you can get your favorite Barbie 2023 movie collection in best prices.
Reply
07/31/2023 at 11:34 PM

---
**内容**: christome said...
You have shared a lot of list API's I have read it I like it very much now I will suggest you to use this My Fault 2023 Ronnie Silver Bomber Jacket for this winter season.
Reply
08/03/2023 at 12:36 AM

---
**内容**: Junnas8 said...
I've got it. It's helpful much papa's pizzeria game.
Reply
10/22/2023 at 08:25 PM

---
**内容**: mollyharboe said...
I am a student of programming and I have taken good information about programming from your blog and this information has been very useful for me. Now I will tell you about this summer season, this href="https://www.thejacketspot.com/product/ryan-reynolds-wrexham-canada-goose-hooded-jacket/">Ryan Reynolds Wrexham Canada Goose Hooded Jacket will be the best.
Reply
11/01/2023 at 06:26 AM

---
**内容**: MyWheels said...
IF you looking yamaha ybz dx 125 price in pakistan today you must need to cheak mywheels.
Reply
11/27/2023 at 11:22 AM

---
