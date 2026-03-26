---
title: "DevTV: Non-COM Property System"
date: 2012-04-01
categories:
  - AutoCAD COM
tags:
  - API
  - AutoCAD
  - COM
  - Palette
description: "We've created a DevTV on the Non-COM Property System (codenamed Ubiquity), which got a public API in the latest release of AutoCAD. In the past you..."
author: Autodesk
---
# DevTV: Non-COM Property System

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/devtv-non-com-property-system.html

## 文章内容

By Adam Nagy
We've created a DevTV on the Non-COM Property System (codenamed Ubiquity), which got a public API in the latest release of AutoCAD. In the past you needed to create COM classes to add properties to your custom entities that could be seen in the Properties palette.
Now you can do it without using COM – hence the name 'Non-COM Property System'.
DevTV - Ubiquity

## 评论

**内容**: Alexey Ursegov said...
Hello,
I checked out "DevTV - Ubiquity" and it look great.
The example describes only "double" and "color" property types. How can I create an indexed property (so it looks like combobox)?
I tried to derive from AcRxIndexedProperty class, but I couln't get it to be shown in property palette. Maybe I'm doing something wrong.
Another question is how to make a read-only property?
Reply
05/15/2012 at 04:58 AM

---
**内容**: Adam Nagy said...
Hi Alexey,
There are blog posts here which I think should answer your questions:
http://adndevblog.typepad.com/autocad/2012/04/non-com-property-with-list-of-possible-values.html
and
http://adndevblog.typepad.com/autocad/2012/04/read-only-non-com-property.html
Cheers,
Adam
Reply
05/15/2012 at 05:13 AM

---
**内容**: Kenny said...
Hi Adam,
I am an ADN register member. I looked at your provided demo project DevTV - Ubiquity. It's greate. Now, I can add index property to a line. But I wonder how to exchange indexes of two lines. For example, the original index of line A is 1, and the original index of line B is 2. Now I changed the index of line A into 2. So, what I want see is that if I right click the line B property, its index should be changed into 1. It may be done at the function "subSetValue/subGetValue", but I find the two functions run serval times even I only changed index of line A into 2. So, could you help me? Thanks.
Best Regards
Kenny
Reply
12/11/2012 at 12:59 AM

---
**内容**: Adam Nagy said...
Hi Kenny,
I'm not sure I understand the real issue you are describing. E.g. why is it a problem that those functions are called multiple times? You can check if the assigned property is the same as the current one, in which case you don't have to do anything.
If you could log a case about this with more details on DevHelp Online in case you need more help with this, that would be the best.
Thank you,
Adam
Reply
12/11/2012 at 06:22 AM

---
**内容**: Kenny said...
Hi Adam,
OK. Thanks for your reply. I will summit a case.
Best Regards,
Kenny
Reply
12/12/2012 at 05:24 PM

---
**内容**: Dan said...
Hello,
The new function are great, but unfortunately I can't find a way to change the Properties Window name. Through COM this is changed with the function GetDisplayName
STDMETHODIMP CDHPAVolumeWrapper::GetDisplayName(DISPID dispID,BSTR *pBstr)
{
if (dispID == 0x401)
{ // magic dispID meaning object itself
if (pBstr==NULL)
return E_POINTER;
AcAxObjectRefPtr pDHPACustomEntity(&m_objRef, AcDb::kForRead);
if (pDHPACustomEntity.openStatus() != Acad::eOk)
return E_ACCESSDENIED;
wchar_t szPropertiesDisplayName[MAX_PATH];
pDHPACustomEntity->GetPropertiesDisplayName(szPropertiesDisplayName);
*pBstr = ::SysAllocString(szPropertiesDisplayName);
return S_OK;
}
return IOPMPropertyExtensionImpl::GetDisplayName(dispID, pBstr);
}
How could I do this with the NON-COM functions?
Reply
04/25/2013 at 11:16 PM

---
**内容**: Balaji said...
Hi Dan,
Sorry, this is not possible at present using the Non-COM property system.
We have a request logged with our engineering team for this.
Reply
04/25/2013 at 11:51 PM

---
**内容**: Navneet Tripathi said in reply to Balaji...
Hello,
This thread is from 2013 and it has been a long time. Is there any way now to change the Property Window name using NON-COM properties?
Reply
06/25/2019 at 12:18 AM

---
**内容**: Madhukar Moogala said in reply to Navneet Tripathi...
Hi Navneet,
Changing Properties Display name is not possible yet using Non-Com property system, most of the development on Ubiquity has stalled.
Sorry if it is a bad news.
Reply
06/25/2019 at 02:25 AM

---
**内容**: Dan said...
Hello,
I have another question for you.
With your example I managed to show in the Properties Window for my CustomEntity a new category and new properties. But in the RollOver tooltip I can't see for my CustomEntity the custom category and custom properties.
For doing this I go to to CUI->RollOver Tooltips->I add my CustomEntity to the list but I only see Static Properties there.
In COM I think this is done with
class ATL_NO_VTABLE CSimpleProperty :
public CComObjectRootEx,
public IDynamicProperty,
public IFilterableProperty
{
public:
CSimpleProperty();
BEGIN_COM_MAP(CSimpleProperty)
COM_INTERFACE_ENTRY(IDynamicProperty)
COM_INTERFACE_ENTRY(IFilterableProperty)
END_COM_MAP()
STDMETHOD(ShowFilterableProperty)(THIS_
/*[in]*/DISPID dispID,
/*[in]*/AcFilterablePropertyContext context,
/*[out]*/BOOL* pbShow);
Is there a way to display this also with NON-COM functions?
Reply
07/11/2013 at 11:09 PM

---
**内容**: Balaji said...
Hi Dan,
In AutoCAD 2013, I could see the custom property in the roll-over tooltip. I have shared screenshots to show the steps to enable them using the CUI dialog. I think it is same as what you have already tried.
If that does not help, can you please try with the Ubiquity sample from the DevTV and see if that works for you ?
Here are the screenshots :
https://www.dropbox.com/s/t39wh3ubvnb8i4u/1.png
https://www.dropbox.com/s/f6adq98lz1pas4g/2.png
Regards,
Balaji
Reply
07/12/2013 at 03:14 AM

---
**内容**: Dan said...
Hi Balaji,
I finally figured it out what is the problem with my entity. It seems that if I use the COM wrapper (as in my previous post) for changing dynamically the CustomEntity name, then in the RollOver tooltips I don't see the CustomProperties created with NON-COM functions.
I still don't know how to mix this two things in order to have the name changed and to see the properties in the tooltip. In the normal Properties Window both the name and extra properties are working fine.
I will try this post
http://through-the-interface.typepad.com/through_the_interface/2008/11/adding-custom-p.html
to see if I could add the properties with COM.
If you have any ideas it will be very helpful.
Reply
07/15/2013 at 05:41 AM

---
**内容**: Balaji said in reply to Dan...
Hello Dan,
The blog post that you mentioned about should help resolve this.
If you have a COM wrapper for your custom entity, implementing IFilterableProperty is needed for the properties to appear in the CUI dialog.
When using the Non-COM property system, a COM wrapper is internally created. I am not yet sure how this is supposed to work when there are two wrappers for a custom entity. I will try and reproduce the behavior and will contact our engineering team to get this clarification.
Regards,
Balaji
Reply
07/15/2013 at 10:17 PM

---
**内容**: Dan said in reply to Balaji...
Hi Balaji,
I have one remark to add. The COM Wrraper is implemented on a class derived from AcDbEntity
class DLLEXPORT DHPACustomEntity : public AcDbEntity
The NON-COM one is implemented on class derived from the first one
class DLLIMPEXP DHPAVolume : public DHPACustomEntity
It is done like this because there are several classes derived from the DHPACustomEntity and writing a COM wrapper for all will be a big problem with the only goal of changing the displayed name. By implementing it to the base class and only virtualizing the GetDispalyedName functions it was making our life much easier.
But the NON-COM properties are different between the derived classes so using NON-COM for this ones again will make our life much easier.
Reply
07/16/2013 at 04:18 AM

---
**内容**: Balaji said in reply to Dan...
Hi Dan,
Sorry for the delay in getting back to you.
I could reproduce the behavior in a sample project that implements a COM wrapper for a custom entity while the custom entity also uses the Non-COM property system.
In this case, since the property palette displays both COM / Non-COM properties, I would expect both to appear in the CUI dialog while customizing rollover tool tips. Unfortunately that is not the case.
I have logged this behavior for our engineering team to analyze. Sorry, I did not find a workaround for this.
Regards,
Balaji
Reply
07/23/2013 at 05:49 AM

---
**内容**: Dan said in reply to Balaji...
Thank you very much. Today I've return from holidays and I was about to post this on our new ADN support, but now I will wait.
Reply
08/20/2013 at 03:51 AM

---
**内容**: Balaji said in reply to Dan...
Hi Dan,
I would still suggest logging it as a request. In reply to that, I can send you the details of the engineering request that I have already created. This will help keep track of it and you can also bring out the importance of this fix.
Reply
08/20/2013 at 04:47 AM

---
**内容**: Dan said in reply to Balaji...
Ok I made a support request (Case number 08695619).
Thank you again
Reply
08/22/2013 at 12:55 AM

---
**内容**: Florent said...
Hi,
I'm sorry to come back on old topic. But i don't manage adding an angular property in the OPM.
I think it's like in your example with color :
Constructor's property :
AcRxProperty(_T("My Color Property"), AcRxValueType::Desc::value())
What's class can i use instead of AcCmColor ?
Thank you for your help (and thanks too for this usefull example :)
Florent
Reply
03/20/2016 at 03:04 PM

---
**内容**: Florent said...
Hello,
I founded a solution :
Override AcRxProperty like the example with double value type and add an AcRxUnitTypeAttribute in the constructor like this :

AngleProperty::AngleProperty(const ACHAR *nom, const ACHAR *nomCategorie) :
AcRxProperty(nom, AcRxValueType::Desc::value()),
m_categorie(0)
{

// Add category like Adam's example...
// OPM = Object Property Manager / Property Palette
// Add the Placement attribute to set under which category in the OPM
// the property will be shown
attributes().add(new AcRxUiPlacementAttribute(nomCategorie, 0));
// Add this attribute so that AutoCAD will automatically create the COM
// wrapper for this property, i.e. it will be visible in OPM
attributes().add(new AcRxGenerateDynamicPropertiesAttribute());
// And specialize in angular value
AcRxUnitTypeAttribute *typeDeDonnee = new AcRxUnitTypeAttribute(AcRxUnitTypeAttribute::kAngle);
attributes().add(typeDeDonnee);
}

For methods subSetValue and subGetValue, nothing change, cast with double and use the AcDb::kDxfXdReal type for XData.
Just don't forget the OPM return and use radian values regardless of angle type use.
I hope it's safe and can help someone.
Regards,
Florent
Reply
03/22/2016 at 06:37 AM

---
**内容**: aither said...
Hello, Adam
First, thanks for your list property example, it is great!
But I have a problem: It works as well, when I hover list item after I drop-down the list, subSetValue() is called for every item. When I press a ESC key, or click at ACAD drawing view, the list is closed and the selected item is not changed.
THE PROBLEM: when no selected item of list is hovered, the item index is stored to pent->mNumSides through subSetValue(). But when list is closed by lost-focus, how I restore the pent->mNumSides with current selected item of list?
Sorry for my bad English.
Reply
03/28/2022 at 08:34 PM

---
