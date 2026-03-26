---
title: "What qualifies an ObjectARX class to be an abstract class"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Database
  - Forge
  - ObjectARX
description: "Let's talk about what are abstract classes in C++ to get started."
author: Autodesk
---
# What qualifies an ObjectARX class to be an abstract class

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/what-qualifies-an-objectarx-class-to-be-an-abstract-class.html

## 文章内容

By Gopinath Taget
Let's talk about what are abstract classes in C++ to get started.
According to C++ reference, "Abstract classes act as expressions of general concepts from which more specific classes can be derived. You cannot create an object of an abstract class type; however, you can use pointers and references to abstract class types."
"A class that contains at least one pure virtual function is considered an abstract class. Classes derived from the abstract class must implement the pure virtual function or they, too, are abstract classes."
For an ObjectARX class (still a C++ class), there is no exception from the above. There are some additional database object methods need to be included in a database object derived class. We implemented some macros to take away some of the boiler plate code a developer has to write.
In your class if you forget to use public: and virtual void
PureMethod(...) = 0, your class is useless and does not qualify as an abstract class. You might thing that using the ARX macro ACRX_NO_CONS_DEFINE_MEMBERS will make a class abstract. However, this is not the case. You should indeed use this macro in an abstract ARX class but it does not make a class abstract.
The right way to use this macro is to define it outside the class definition and inside the class definition, ACRX_DECLARE_MEMBERS macro should be used.
ACRX_NO_CONS_DEFINE_MEMBERS calls ACRX_DEFINE_MEMBERS macro to define desc(), isA(), and gpDesc. In addition it also defines: void CLASS_NAME::rxInit(). You should make your default constructor as protected or private, so <ClassName>::desc()->create() returns NULL. This prevents the user from instantiate this base class.
Again, please note that, when you're creating an abstract class, only ACRX_NO_CONS_DEFINE_MEMBERS should be used.
Here is a sample abstract custom object class:
class MyBaseObject : public AcDbObject
{
MyBaseObject() {};
public:
ACRX_DECLARE_MEMBERS(MyBaseObject);
  ~MyBaseObject() {};
 void DoStuff() {ads_printf(L"do something");};
 // to be implemented in derived classes
 virtual void PureMethod(void) = 0;
};
ACRX_NO_CONS_DEFINE_MEMBERS (MyBaseObject, AcDbObject);

