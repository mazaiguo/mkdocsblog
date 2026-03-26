---
title: "Converting C# to Java – An Experiment (Part 6)"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - AutoCAD
  - C#
  - Plugin
description: "(Links to previous installments: Part 1; Part 2; Part 3; Part 4; Part 5)."
author: Autodesk
---
# Converting C# to Java – An Experiment (Part 6)

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/converting-c-to-java-an-experiment-part-6.html

## 文章内容

By Stephen Preston
(Links to previous installments: Part 1; Part 2; Part 3; Part 4; Part 5).
I left this series hanging because I was busy with our ADN DevCamps for a while, and then I had some frustration finishing off my app. I had intended to add functionality to allow the user to save/load as many prioritization lists as they wanted (as I did for my AutoCAD version), but after much searching I discovered that the Android SDK doesn't include a file picker (open/save) activity or dialog. This seems to be a fairly common question among new Android developers, and it took me a long time to find out because I refused to believe it was true :-). (Please let me know if I overlooked something in a newer Android SDK. Its always a problem googling for information on an SDK that has been around for a while - you find lots of old comments and samples that no longer apply to the latest SDK version).
The options to use a file picker in your app seem to be either to rely on one already being installed on the device that will respond to an intent you broadcast, or to 'roll your own'. I found a promising looking project on GitHub for the 'roll your own' option, and another one on code.google.com.
To avoid going off on a tangent, I decided to abandon the multiple file option, and instead use the serialization interfaces I'd already implemented to persist the same list between application sessions, and also to handle the Android OS destroying and later restoring my App Activities in the background if it needed to free up resources. Handling your Activities being destroyed and restored is a very important aspect of Android app development.
To cut a long story short, I've posted a new version of the Prioritizer app for you to download here. It extends the previous version I walked through by adding:
A new Activity to perform the binary comparison between activities.
A button to sort Items by priority.
A button to clear the list.
The ability to delete an Item (from the edit activity).
Persistence of the list between states and also better handling of the Activity lifecycle. 
Use of string resources in layouts instead of hardcoded strings.
The app is far from optimized - saving the entire Item list every time anything is updated is particularly klunky - but it works. Hopefully the comments in the code are self-explanatory. The additions are really more of the same, which is why I've not documented the changes step-by-step.
To summarize what we've found during this exercise:
Converting C# to Java is pretty straightforward. Their syntax is very similar, as are the class libraries they provide. This syntax comparison sheet is a great help when you're trying your first few migrations.
The big differences when porting between platforms are the interfaces to the specific platforms - for example, the UI and the file system. This is why its important to separate your business logic from platform specific code whenever you write an app you plan to port between platforms. This was the reason for the AutoCAD Big Split project (which Kean has described on his blog).
Android apps consist of Activities. Information is passed between Activities using an Intent. Once you know how to do that you're up and running.
Android programming is much easier to setup on MacOS than on Windows or Linux ;-), with the added advantage that you can learn iOS programming as well if you buy a Mac :-).
I'm off to play around with Windows Azure now to see what all the fuss is about. Some of the guys on our C&M DevBlog are well ahead of me there, so I may not get to blog about it. I'm also looking forward to coming back to Android and trying the Rajawali SDK that Kean told me about.

## 评论

**内容**: Anonymoose said...
Convert C# to Java ???
Why?
http://www.xamarian.com
Reply
06/29/2012 at 03:38 PM

---
**内容**: Anonymoose said in reply to Anonymoose...
Sorry, the correct link is:
http://www.xamarin.com
Reply
06/29/2012 at 03:45 PM

---
**内容**: Madhukar Moogala said in reply to Anonymoose...
I'm aware of Xamarin, Tony, but I've not bought a license to try it. Its one of several cross-platform SDKs available for mobile devices. It seems you're a fan, because you made a very similar post to Kean's blog. My reply is the same as Kean's. Personally, I prefer to learn a new platform via the native tools, and this series is documenting my experiences doing that for anyone who is interested. If you're not, then no need read it :-).
Reply
06/30/2012 at 05:43 PM

---
**内容**: Anonymoose said...
Your and my personal preferences aside, I think any discussion about converting C# to Java merits at least brief mention of alternatives to conversion, using tools like Mono for Android and MonoTouch for iOs, because they can eliminate the need for conversion and dramatically reduce the cost of targeting multiple platforms insofar as non platform-dependent code goes. Making readers aware of those tools is just a professional courtesy, irrespective of one's own personal preference.
While Android itself is largely written in Java, the native tool on Android is actually C++, not Java. It may also be worth mentioning that because Mono For Android bypasses Java and the Dalvik runtime for many things it does and instead uses P/Invoke directly call native code, C# applications on Mono For Android consistently outperform equivalent or similar Java applications, and have far less battery consumption.
Reply
07/05/2012 at 03:28 PM

---
**内容**: Madhukar Moogala said in reply to Anonymoose...
I suggest you keep your eye on our Cloud and Mobile DevBlog. I know Gopinath already has plans for looking at the available cross-platform development technologies in due course.
And sorry if I caused confusion with my use of the phrase 'native tools'. My intended meaning was 'tools provided/recommended by the vendor', which I think was evident from the context in which I used it. Gopinath has already mentioned on C&M DevBlog that Google discourage the use of NDK unless its strictly necessary - http://adndevblog.typepad.com/cloud_and_mobile/2012/06/native-programming-on-android.html.
Reply
07/05/2012 at 04:30 PM

---
