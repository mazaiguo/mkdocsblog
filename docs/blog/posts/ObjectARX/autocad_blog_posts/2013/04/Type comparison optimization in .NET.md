---
title: "Type comparison optimization in .NET"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "Although this is not AutoCAD or Autodesk related, I always see developers doing .NET code that can be optimized. Sure in some cases this is not a c..."
author: Autodesk
---
# Type comparison optimization in .NET

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/type-comparison-optimization-in-net.html

## 文章内容

By Augusto Goncalves
Although this is not AutoCAD or Autodesk related, I always see developers doing .NET code that can be optimized. Sure in some cases this is not a concern, or the processing time that will be saved doesn’t worth the trouble. But doing some small good practices can save you big at the end of your project.
So this post is quite simple and about type comparison. The idea came from this interesting post: Drilling into .NET Runtime microbenchmarks: 'typeof' optimizations.
Basically it says that the following type comparison is the faster:
Entity ent = // initialize here
if (ent.GetType() == typeof(Line))
{
}
[Update] Comments:
As well pointed by the comments (see below), the variations of object type comparison shown here (and the linked post) will produce different results. So you need make sure which is one is the correct for each scenario. Once that is decided, I would suggest review the performance trade off of your choice at the linked post.

## 评论

**内容**: Owen Wengerd said...
Do derived types meet that condition? I would expect not, and if they don't, I suspect that your direct type comparison is not appropriate in the majority of cases where an object's type must be checked at runtime.
Reply
04/15/2013 at 12:32 PM

---
**内容**: Augusto Goncalves said in reply to Owen Wengerd...
Hi Owen,
Not sure what you mean by 'derived types', can you clarify?
This quick sample is for runtime check. What type of check are you doing?
Regards,
Augusto Goncalves
Reply
04/15/2013 at 12:43 PM

---
**内容**: Owen Wengerd said in reply to Augusto Goncalves...
By 'derived type' I mean a type that can be cast to a base type that it inherits from. For example, Line is a type derived from Curve. If code is checking for a Curve type at runtime, then Line should be an acceptable type since Line is a type of Curve and a Line can therefore be cast to Curve.
Reply
04/15/2013 at 05:34 PM

---
**内容**: Augusto Goncalves said in reply to Owen Wengerd...
Owen,
Sure, make sense...
(Table is BlockReference)
>> this test is True
(Table.GetType() == typeof(BlockReference))
>> this test is False
So if you are testing against the hierarchy, then the 'is' is the way. Just consider the faster way when hierarchy is relevant.
I see many developers doing type check in even more slower ways, such as comparing by name.
Thanks for pointing it out.
Regards,
Augusto Goncalves
Reply
04/16/2013 at 07:16 AM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
"Just consider the faster way when hierarchy is relevant."
I think you may be missing Owen's point.
How can the programmer possibly know if/when hierarchy is relevant?
If the programmer has specific knowledge of the derived types (as would be the case with Table : BlockReference), that is one thing, and they could eliminate Tables by using your suggested alternative to 'is', but in doing so, they may also be eliminating other custom types that also derive from BlockReference, including ones the programmer has no knowledge of, and therefore, cannot know if they should or should not be treated as BlockReferences by their code.
In OOP school, we are taught to treat instances of derived types as instances of a specific base type that we are dealing with, because way may not know anything about derived types (including ones that may not have existed when our code was written), and shouldn't make assumptions about how they should be dealt with.
Reply
04/16/2013 at 12:13 PM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Hi Tony,
Sorry for this typo... I meant: "Just consider the faster way when hierarchy is NOT relevant"
In some cases we're looking for Line, nothing else, so I'll not worry about hierarchy, nothing other than Line is acceptable.
Thanks for your comments.
Regards,
Augusto Goncalves
Reply
04/16/2013 at 12:19 PM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
Hi Augusto. "In some cases we're looking for Line, nothing else...".
Sorry, one cannot make the assumption that types that may be derived from Line, are not also Lines.
Reply
04/17/2013 at 12:37 PM

---
**内容**: Tony Tanzillo said in reply to Owen Wengerd...
Hi Owen. Since Curve is abstract, there could never be a case where GetType() would return that type, but your point is perfectly valid given the case of two concrete types that have the same relationship.
Reply
04/17/2013 at 12:47 PM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
You seem to be confusing two very different things.
"if( someobject is Line )"
with
if( someobject.GetType() == typeof( Line ) )
Are not the same thing.
If 'someobject' is a type derived from Line, the first test fails and the second succeeds.
Gabeesh ?
Reply
04/16/2013 at 04:47 AM

---
**内容**: Tony Tanzillo said in reply to Tony Tanzillo...
That should have been 'the first test succeeds and the second test fails'
Reply
04/16/2013 at 04:58 AM

---
**内容**: BlackBox said...
As one example of a derived Type, consider Table, which derives from BlockReference.
Reply
04/15/2013 at 02:25 PM

---
**内容**: Augusto Goncalves said in reply to BlackBox...
Yes that is one case where the two can exist on the drawing.
Curve and Line are a little different because there is not 'real' curve on the drawing, only Line, Arc, etc.
Thanks for sharing.
Regards,
Augusto Goncalves
Reply
04/16/2013 at 07:18 AM

---
**内容**: Tony Tanzillo said in reply to Augusto Goncalves...
The fact that Curves is an abstract type shouldn't really have any bearing on that.
I have code that operates on all AcDbText objects in a BlockTableRecord. It will also operate on all AcDbAttributeDefinition instances as well, by virtue of the fact that the latter derives from the former. Neither of the two are abstract types.
And, it is that way by-design.
The point here is not that what you suggest is incorrect, but rather that you presented the two different methods as equivalent, which they are not.
Reply
04/17/2013 at 12:45 PM

---
**内容**: Augusto Goncalves said in reply to Tony Tanzillo...
Hi Tony,
Thanks for the comments, this is correct. So I added a note on it.
Again, thanks for sharing.
Regards,
Augusto Goncalves
Reply
04/17/2013 at 12:48 PM

---
**内容**: Tony Tanzillo said...
Here's a tip: If you have to compare two objects derived from DisposableWrapper, don't use this:
DisposableWrapper a =...
DisposableWrapper b = ...
if( a == b ) {...} // slow
Instead, use this:
if( a.UnmanagedObject == b.UnmanagedObject) {...} // faster
The reason the second one is faster than the first, is because for some un-explainable reason, the == operator for DisposableWrapper leads to a boxing/unboxing operation, which is immensely-slow.
You might want to ask one of your colleagues why it was done that way, because it is totally incorrect, and serves to make all code that uses the operator frequently much slower than it could otherwise be.
To see the more-correct way to implement the == operator, look at the == operator for System.IntPtr.
Reply
04/18/2013 at 06:08 AM

---
**内容**: Fenton Webb said...
Hey Tony!
it's long thread here, so let me ask you - are we talking about simple object comparison now? if not, please ignore this post, if so...
...then you are right, if( a.UnmanagedObject == b.UnmanagedObject) {...} **is** much faster.
However, what is the comparison you are trying to do exactly? You are comparing 2 memory addresses as being the same - Yes, it's the same physical object - but what does that achieve? More likely is that you want to compare the data between 2 objects as being the same, not the address that they reside in memory.
Generally speaking, the Equals operator compares if the 2 objects have the same data, not that they are the same address in memory, testing the UnmanagedObject is of no use. I haven't checked the details of the boxing/unboxing that you talk about but it's probably related to the .NET property handling.
Correct, how the equals operator works is down to the implementer.
Reply
04/18/2013 at 11:29 AM

---
**内容**: Tony Tanzillo said in reply to Fenton Webb...
Hi Fenton, and thanks for replying.
First, I was referring to using the == operator on two variables (reference types) to determine if both of them refer to the same instance, which has nothing to do with value comparisons of fields, properties, and so on. Generally, reference types do not do value comparisons (e.g., compare fields or properties), they compare references to tell if two references are referring to the same instance. Just you might do in C++ when comparing two pointers.
When DisposableWrappers are used as Keys in a System.Collections.Generic.Dictionary, or are stored as elements in a System.Collections.Generic.HashSet (sorry, this lame blogging platform removes the angle braces - those are generic types), there can be a potentially-massive number of equality comparisons. Those two containers are examples, but there are plenty of other scenarios where code needs to know if two references to an object are both references to the same instance. That has nothing to do with comparing members or fields or properties.
The implementation of the DisposableWrapper's == operator is quite definitely incorrect, and you can have a look at System.IntPtr's == operator, which does not delegate to the Equals(Object) override.
Reply
04/19/2013 at 05:20 AM

---
**内容**: BlackBox said in reply to Fenton Webb...
Apologies for jumping backward a bit (I've missed a lot of discussion this week)....
[Fenton] "However, what is the comparison you are trying to do exactly?"
Two specific situations come to mind immediately:
1. I have a Contextual menu who's Popup Event is being used to differentiate between BlockReference, Dimension, MLeader, and Table (given an implied, single selection) whilst also pulling Property data from Entity to be conditionally displayed within my Context Menu.
When dealing with vanilla AutoCAD, this can be simple enough, either test for Type via 'as' operator, pull Type-specific data, or move on... Or... Which I've also done (but see Tony has already touched on) use the Id.ObjectClass.Name to switch between AcDb*'s.
2. Where complexity comes into play, is in dealing with Civil 3D, as d@amn near every AECC* Object is derived from BlockReference... Tin Surfaces, Pipes, Profile Views, heck even Feature Lines... It's quite frustrating.
I'd be very interested to learn a more efficient way of quickly distinguishing Type than what I and others have already outline here (if there is one?), especially so given that I work with Civil 3D, and soon AMEP.
Cheers
Reply
04/19/2013 at 11:47 PM

---
**内容**: Fenton Webb said...
Hey Tony!
appreciate your reply. The thing is, if it's an object in AutoCAD, you normally use ObjectID or Handle to compare if they are the "same object" you see... You can't rely on the memory address, because sometimes the memory manager moves the object, that's one of the reasons why we have an transaction/open close mechanism.
Reply
04/19/2013 at 08:36 AM

---
**内容**: Tony Tanzillo said in reply to Fenton Webb...
"The thing is, if it's an object in AutoCAD, you normally use ObjectID or Handle to compare if they are the "same object" you see..."
Hi Fenton, and thanks again.
AcRxClass (whose managed wrapper is RXClass) doesn't have a handle or an ObjectId.
This isn't really as much of a performance issue in most use cases, but where I noticed a difference was when scanning the model space BlockTableRecord in a very large file to grab all instances of a certain type of DBObject, using the ObjectId's ObjectClass property (and thereby avoiding the need to open each object, get a managed wrapper and test that).
    
 RXClass pointClass = RXClass.GetClass(typeof(DBPoint));
 foreach( ObjectId id in someBlockTableRecord )
 {
   if( id.ObjectClass == pointClass ) 
   {
      // found a DBPoint, proceed.
   }
 }
Reply
04/19/2013 at 10:31 AM

---
**内容**: Fenton Webb said...
OK, got ya.
There's always a Model Space selection filter remember...
http://exchange.autodesk.com/autocadarchitecture/enu/online-help/ARCHDESK/2012/ENU/pages/WS1a9193826455f5ff2566ffd511ff6f8c7ca-4067.htm
Reply
04/19/2013 at 10:51 AM

---
**内容**: Tony Tanzillo said in reply to Fenton Webb...
Hi Fenton.
That would be an option if my code didn't have to work with drawings that aren't open in the editor, and thanks again.
Reply
04/19/2013 at 11:53 AM

---
**内容**: .net runtime optimization service said...
If there is an error in the .net runtime optimization service, then it becomes troublesome to launch apps or play games on your desktop. In case none of the above methods work in fixing the error, you can always temporarily deactivate the .Net optimization service. Doing this will not affect your NET framework but will prompt you to do a few repairs to it.
Reply
09/25/2022 at 10:52 PM

---
