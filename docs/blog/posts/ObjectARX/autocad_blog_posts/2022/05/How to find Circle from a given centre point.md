---
title: "How to find Circle from a given centre point"
date: 2022-05-01
categories:
  - AutoCAD
tags:
  - Selection
  - Unicode
description: "Selection filters are very powerful device yet most of the times it is overlooked, using selection filters you can achieve many regular tasks of co..."
author: Autodesk
---
# How to find Circle from a given centre point

发布日期: 2022-05-01

原始链接: https://adndevblog.typepad.com/autocad/2022/05/how-to-find-circle-from-a-given-centre-point.html

## 文章内容

By Madhukar Moogala
Selection filters are very powerful device yet most of the times it is overlooked, using selection filters you can achieve many regular tasks of conditional selections.
In this snippet we will see, how you can leverage the selection filters to get a circle(s) from a given a centre point!
Do let me know if you have used conditional filters in any interesting scenario.
How do I prepare a conditional filter sequence ?
For example, we have a task to find all the MTEXT entities with particular background mask color fill
From the above picture, we have few MText entities with different colors, suppose if I want to get a MText with green background color fill ?
First, I would check the entity information, I can use this entity information in building a selection filter, (entget (car (entsel)))
Applying this code and pick MTEXT entity with green background mask would give me
((-1 . ) (0 . "MTEXT") (330 . ) (5 . "299") (100 . "AcDbEntity") (67 . 0) (410 . "Model") (8 . "0") (100 . "AcDbMText") (10 1495.9 1933.67 0.0) (40 . 2.5) (41 . 17.7906) (46 . 0.0) (71 . 1) (72 . 5) (1 . "AUTOCAD") (7 . "Standard") (210 0.0 0.0 1.0) (11 1.0 0.0 0.0) (42 . 16.8895) (43 . 2.58697) (50 . 0.0) (73 . 1) (44 . 1.0) (90 . 1) (63 . 3) (45 . 1.0) (441 . 0))
Now referring to MTEXT DXF reference, it is clear that DXF Code 90 is background mask on and 63 is the color when Background mask is enabled
DXF Reference
Now, to pick all MTEXT entities with background color Green
The conditional filter would be (90 . 1) (63 . 3)
This give length of entities respecting our filter
(sslength  (ssget "X"  (list  (cons 0 "MTEXT")(cons 90 1)(cons 63 3))))
Back to our topic, applying similar logic we can construct a code to filter circle based on given center point
AcDbObjectIdArray getCirclesFromAGivenPoint(AcGePoint3d centerPoint) {

    AcDbObjectIdArray idArray;
    ads_name ss, entName;
    /*Construct a filter list*/
    resbuf* filterRb = acutBuildList(RTDXF0, L"CIRCLE",
        10, asDblArray(centerPoint),
        RTNONE);    bool hasSS = false;

    /*Make selection based on filtered list*/
    if (acedSSGet(_T("_X"), NULL, NULL, filterRb, ss) == RTNORM) {
        Adesk::Int32 len;
        acedSSLength(ss, &len);
        if (len > 0) {
            hasSS = true;
            /*Collect and append the objectId to an array*/
                    for (int nEnt = 0; nEnt < len; nEnt++)
                    {
                           if (acedSSName(ss, nEnt,entName) == RTNORM)
                           {
                                 AcDbObjectId selId;
                                 if (acdbGetObjectId(selId, entName) == Acad::eOk)
                                        idArray.append(selId);
                           }
                    }
        }
        freeResbuf(&filterRb);

        if (hasSS)
            acedSSFree(ss);
    }
    return idArray;
}

## 评论

**内容**: cladder said...
I can see a lot of interesting information!
Reply
08/25/2022 at 02:14 AM

---
**内容**: cookie clicker said...
I was looking for a way to use dxf codes to modify some of the settings for my MTEXT object. It was harder than I anticipated, but with other people's assistance, I finally have code that accomplishes my goals. I'm aware that this might be written in simpler code, but it fits the way my mind works.
Reply
10/03/2022 at 02:53 AM

---
**内容**: Orborneny said...
Bloxorz want to say thank you for your information
Reply
11/22/2022 at 07:51 AM

---
**内容**: JamesOneil said...
Thanks for taking the time to discuss that Barclays Bank Near Me - Branch / ATM Locations
I'd love to learn more about this area. Would you mind updating your blog post with additional insights? It will be really helpful for all of us.
Reply
02/27/2023 at 02:03 AM

---
**内容**: Charles Kraus said...
All the shapes of the success and team are fit for the working. Yes, the range of the best crypto ATM is signed for the contract. Agreement is done for the typical chain of the events for the turns for the semi-final matter for all people.
Reply
04/01/2023 at 02:18 AM

---
**内容**: GraceKelly said...
Interesting situations occur when manipulating the filter amuses the user. These filters work very well in conjunction with the cuphead as it is responsive.
Reply
04/03/2023 at 12:53 AM

---
**内容**: Five Nights at Freddy's Security Breach said...
Good post! This is a great blog that I'll be sure to visit many more times this year. We appreciate the article.
Reply
05/03/2023 at 10:04 PM

---
**内容**: Ramselton23 said...
get post
Reply
05/04/2023 at 11:02 PM

---
**内容**: retro bowl said...
The knowledge you share is excellent. It greatly aids in my comprehension of this subject.
Reply
06/17/2023 at 02:09 AM

---
**内容**: slope said...
I appreciate your post because it has a lot of good information that I can absorb and learn.
Reply
07/11/2023 at 02:12 AM

---
**内容**: amanda the adventurer said...
Conditional filters can be very useful in automating tasks and selecting specific entities based on certain criteria.
Reply
08/03/2023 at 12:58 AM

---
