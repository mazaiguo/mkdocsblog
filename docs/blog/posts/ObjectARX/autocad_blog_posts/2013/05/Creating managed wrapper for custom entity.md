---
title: "Creating managed wrapper for custom entity"
date: 2013-05-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - ObjectARX
description: "ObjectARX 2009 SDK had a nice sample project called "SimpleSquare" that demonstrated the managed wrapper creation that allows access to the custom ..."
author: Autodesk
---
# Creating managed wrapper for custom entity

发布日期: 2013-05-01

原始链接: https://adndevblog.typepad.com/autocad/2013/05/creating-managed-wrapper-for-custom-entity.html

## 文章内容

By Balaji Ramamoorthy
ObjectARX 2009 SDK had a nice sample project called "SimpleSquare" that demonstrated the managed wrapper creation that allows access to the custom entity from a managed code. I have migrated this sample project to work with AutoCAD 2013 and Visual Studio 2010.
The changes are mainly to conform to the new CLR syntax as the original sample used the old CLR syntax.  
Here is the sample project for download.
Download SimpleSquare
To try this, place the "SimpleSquare" folder under "<ObjectARX 2013 SDK folder>\samples\entity" and follow the steps explained in the ReadMe.txt

## 评论

**内容**: Tony Tanzillo said...
Hi Balaji.
Your sample (and the original) are missing some very important things.
You can read more about that in this discussion group post:
http://forums.autodesk.com/t5/Autodesk-ObjectARX/data-extraction-wizzard-custom-entity/m-p/2180119/highlight/true#M24034
Reply
05/04/2013 at 12:57 PM

---
**内容**: Balaji said in reply to Tony Tanzillo...
Hi Tony,
Thanks for that informative link.
It will help developers interested in using Data extraction with custom entity.
Reply
05/06/2013 at 01:22 AM

---
**内容**: Tony Tanzillo said in reply to Balaji...
Hi Balaji.
You're welcome.
However, I think it's important to not marginalize the issue.
Supporting data extraction is not a 'luxury' but rather a necessity, hence the need for a basic example of a managed wrapper for a custom entity to show how to do that.
Reply
05/06/2013 at 12:02 PM

---
**内容**: Balaji said in reply to Tony Tanzillo...
Sorry, My intention was not to marginalize the issue. It is indeed important to have the DX correctly extract data from a custom entity. As you have already provided the link to help developers understand the changes that need to go into this sample project, I did not mention about changing the sample itself.
Regards,
Balaji
Reply
05/07/2013 at 06:43 AM

---
**内容**: Tony Tanzillo said in reply to Balaji...
Balaji, No problem.
It would be nice if the distributed sample, or any sample, showed how to support Data Extraction. I've already come across quite a few cases where custom objects (including some from AutoCAD-based products) do not support Data Extraction, and most-definitely should.
Reply
05/08/2013 at 09:56 PM

---
**内容**: Dale Bartlett said...
Hi Balaji, I am unable to load the solution into VS2010 Express, nor the SimpleSquare.vcproj separately. It attempts to upgrade and then fails. Just curious if this has happened for others.
Reply
05/05/2013 at 05:21 AM

---
**内容**: Balaji said in reply to Dale Bartlett ...
Sorry, I havent tried it with Visual Studio Express edition.
It is not a supported compiler for ObjectARX applications and some restriction do apply when you use it.
http://adndevblog.typepad.com/autocad/2012/05/about-visual-studio-2010-visual-studio-express-platform-toolset-and-autocad-2010-2012.html
Reply
05/06/2013 at 01:25 AM

---
**内容**: Dale Bartlett said...
Thanks Balaji, I'll test on VS Professional version.
Reply
05/06/2013 at 09:53 PM

---
**内容**: Larry Rios said...
Balaji,
Will the new clr syntax work with AutoCAD 2010 SDK?
Thanks,
Larry
Reply
07/15/2013 at 08:18 AM

---
**内容**: Balaji said in reply to Larry Rios...
Hi Larry,
Yes, the sample project in the blog post also works with AutoCAD 2010. The .Net framework version will need to be changed to v3.5 by manually changing the "SimpleSquare.vcxproj" file as explained in this post :
http://stackoverflow.com/questions/2921702/change-c-cli-project-to-another-framework-than-4-0-with-vs2010
The "SimpleSquareUI" project will need to target 3.5 which can be modified using the project properties in Visual Studio IDE.
Regards,
Balaji
Reply
07/15/2013 at 09:50 PM

---
**内容**: Carl said...
Balaji,
Can you point me to any links that pass strings through the managed wrapper? it seems like such a simple thing, but unicode makes it not so ;) Cheers!
Reply
12/02/2013 at 02:11 PM

---
**内容**: Balaji said...
Hi Carl,
Can you please refer to the \Samples\Entity\PolySamp example ?
It uses the "StringToCIF" and "CIFToString" methods to pass strings to and forth.
Regards,
Balaji
Reply
12/03/2013 at 02:08 AM

---
**内容**: Carl said in reply to Balaji...
thanks! I've been digging through that but it's huge - and easy to miss. I'm off and running now.
This is the second time (at least) you bailed me out personally, so thanks again :)
Reply
12/04/2013 at 02:34 PM

---
**内容**: Carl said in reply to Balaji...
A quick clarification on syntax:
SimpleSquare uses
property type name
{
get
set
}
notation, while PolySamp uses
__property void set_Center(Point2d point);
and I originally based mine on SimpleSquare - learning from PolySamp as I go. anyway, my notation pulls an error on String* (no pointers in c++/cli etc) and the __Property notation doesn't work either... Can I use the both property declarations to pass a string or am I missing something here?
Reply
12/04/2013 at 03:59 PM

---
**内容**: Carl said in reply to Carl...
ps, I've started a discussion about this here:
http://forums.autodesk.com/t5/Autodesk-ObjectARX/passing-string-to-custom-objects-through-a-managed-wrapper/m-p/4668155
so as to not derail things here.
Reply
12/04/2013 at 04:20 PM

---
**内容**: Balaji said in reply to Carl...
Hi Carl,
Can you please check if your project is using the old clr syntax or the new one ?
You can find the difference in the syntax here :
http://msdn.microsoft.com/en-us/library/b23b94s7(v=vs.90).aspx
Regards,
Balaji
Reply
12/04/2013 at 09:07 PM

---
**内容**: Account Deleted said...
This is a great example. How would I expose virtual functions such as subWorldDraw() to .NET in the managed wrapper, so that they can be overridden by classes derived from MgSimpleSquare?
Reply
02/20/2015 at 12:43 AM

---
**内容**: Balaji said in reply to Account Deleted...
Hi,
Implementing a custom entity derived from other entity types is not an option that is available with the AutoCAD .Net API. The sample project in this blog post only provides a way to instantiate and set properties of the custom entity through its managed wrapper. I think, you can consider DrawableOverrule and see if that will be of any help in customizing the worldDraw of an entity.
Regards,
Balaji
Reply
02/23/2015 at 02:48 AM

---
**内容**: GlacierXie said...
I want to know how to get/set collection dat？I used List,but not work~
Reply
11/08/2016 at 12:10 AM

---
**内容**: Subir Dutta said...
I got a drawing with Custom Entities and also got the Object Enablers. So now the entities show up in the drawing. Now is it possible to read the properties of the Custom Entities through .Net API ?
My best guess is, the developer of the Custom Entity need to take care about exposing the properties so that those properties can be accessed by .Net API. Am I correct ? Now I don't have anything excepts the object enablers ( dbx ). How to proceed ?
Reply
08/01/2017 at 08:08 PM

---
