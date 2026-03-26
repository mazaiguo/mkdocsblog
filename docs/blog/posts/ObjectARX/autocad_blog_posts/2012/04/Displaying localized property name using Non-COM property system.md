---
title: "Displaying localized property name using Non-COM property system"
date: 2012-04-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
description: "If you are getting started with the Non-COM property system in AutoCAD, please refer to this DevTV by my colleague, Adam Nagy. In this post, we wil..."
author: Autodesk
---
# Displaying localized property name using Non-COM property system

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/displaying-localized-property-name-using-non-com-property-system.html

## 文章内容

By Balaji Ramamoorthy
If you are getting started with the Non-COM property system in AutoCAD, please refer to this DevTV by my colleague, Adam Nagy. In this post, we will look at the changes required for displaying a localized property name using the Non-COM property system.
1) The first step is to ensure that strings are fetched from the string table. To associate the ID of the string with the property, instantiate the "AcRxLocalizedNameAttribute" class and add it to the attributes collection of the property. This can be done in the property constructor.
MyDoubleProperty::MyDoubleProperty() :
    AcRxProperty(_T("My Double Property"),
    AcRxValueType::Desc<double>::value())
{
    // ...
      AcRxLocalizedNameAttribute *pAttrib
            = new AcRxLocalizedNameAttribute(IDS_MYDOUBLE_PROPERTY);
    attributes().add(pAttrib);
}
2) Implement a class derived from "AcRxResourceLoader" and override the "subLoadString" method. Ensure that your implementation in this method returns the localized string corresponding to the ID passed in as a parameter.
// Our resource loader class
class MyResourceLoader : public AcRxResourceLoader
{
    // Return the string fetched from the string table
    virtual Acad::ErrorStatus subLoadString
                                (
                                    unsigned int id,
                                    unsigned int sourceHint,
                                    AcString& result
                                )
    {
        if (sourceHint)
            return AcRxResourceLoader::loadString
                                    (
                                        AcRxObject::desc(),
                                        id,
                                        sourceHint,
                                        result
                                    );
        const int size = 1024;
        ACHAR buf[size];
        int ret = ::LoadString(_hdllInstance, id, buf, size);
          if (ret==0)
            return Acad::eKeyNotFound;
          ASSERT(ret!=size-1);
        result = buf;
        return Acad::eOk;
    }
};
3) Create a global instance of the resource loader class that we created in Step 2.
// Create a global instance of our resource loader
MyResourceLoader _mrl;
4) Add the global instance of the resouce loader class that we created in Step 3 as a protocol extension object to the AcRxClass of the property. A suitable place to do this is the "On_kInitAppMsg" method of your application.
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
{
    AcRx::AppRetCode retCode
                = AcRxArxApp::On_kInitAppMsg (pkt);
      // Add the global instance of our resouce loader
    // as a protocol extension object to the AcRxClass
    // of the property.
    MyDoubleProperty::desc()->addX
                                (
                                    AcRxResourceLoader::desc(),
                                    &_mrl
                                );
      return (retCode) ;
}
We now have everything in place to display the localized name for our property.
Here is a sample project with these changes. This project does not implement resource dlls and so if you need help with it, you may refer to this documentation :
http://support.microsoft.com/kb/198846

## 评论

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
Thank you very much.
Reply
04/25/2013 at 11:19 PM

---
**内容**: Balaji said in reply to Dan...
Hi Dan,
Sorry, this is not possible at present using the Non-COM property system.
We have a request logged with our engineering team for this.
Reply
04/26/2013 at 12:00 AM

---
