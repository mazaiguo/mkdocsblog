---
title: "Non-COM property with list of possible values"
date: 2012-04-01
categories:
  - AutoCAD COM
tags:
  - COM
  - Palette
description: "In the Property palette you can find properties which only accept values that are listed for the property. If you want to create such a property th..."
author: Autodesk
---
# Non-COM property with list of possible values

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/non-com-property-with-list-of-possible-values.html

## 文章内容

By Adam Nagy
In the Property palette you can find properties which only accept values that are listed for the property. If you want to create such a property then you could do that by creating a new enum type and use that to create a new AcRxValueType that implements IAcRxEnumeration
Header file
/////////////////////////////////////////////////////////////////////
// MyEnumType ///////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////
  typedef enum {} MyEnum;
  template<typename ValueType>
class MyValueTypeTemplate : public AcRxValueType
{
public:
  MyValueTypeTemplate(const ACHAR* name,
    const IAcRxEnumeration& pEnum,
    AcRxMemberCollectionConstructorPtr memberConstruct,
    void* userData = NULL):
  AcRxValueType(name,pEnum, sizeof(ValueType),
    memberConstruct, userData) {}
  virtual int subToString(const void* instance, ACHAR* buffer,
    size_t sizeInACHARs, AcRxValueType::StringFormat format)
    const ADESK_OVERRIDE;
  virtual bool subEqualTo(const void* a, const void* b)
    const ADESK_OVERRIDE;
};
  template<typename ValueType>
class MyEnumTypeTemplate :
  public MyValueTypeTemplate<ValueType>, public IAcRxEnumeration
{
  AcArray<const AcRxEnumTag*> m_tags;
  public:
  MyEnumTypeTemplate(const ACHAR* name,
    AcRxMemberCollectionConstructorPtr memberConstruct,
    void* userData = NULL):
  MyValueTypeTemplate<ValueType>(
    name,*this, memberConstruct, userData) {}
    ~MyEnumTypeTemplate()
  {
    for (int i=m_tags.length()-1;i>=0;i--)
      AcRxMember::deleteMember(m_tags[i]);
  }
    virtual int count() const ADESK_OVERRIDE
  {
    return m_tags.length();
  }
    virtual const AcRxEnumTag& getAt(int i) const ADESK_OVERRIDE
  {
    return *m_tags[i];
  }
    void append(AcRxEnumTag& tag)
  {
    m_tags.append(&tag);
    void acdbImpSetOwnerForEnumTag(
      const AcRxClass*, AcRxEnumTag*);
    acdbImpSetOwnerForEnumTag(this, &tag);
  }
};
  /////////////////////////////////////////////////////////////////////
// MyListProperty ///////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////
  class MyListProperty : public AcRxProperty 
{
public:
  static AcRxObject * makeMyListProperty();
    static const ACHAR * kCategoryName;
  static AcRxCategory * category;
    MyListProperty();
  virtual ~MyListProperty();
    virtual Acad::ErrorStatus subGetValue(
    const AcRxObject* pO, AcRxValue& value) const;
    virtual Acad::ErrorStatus subSetValue(
    AcRxObject* pO, const AcRxValue& value) const;
};
  C++ file
/////////////////////////////////////////////////////////////////////
// MyEnumType ///////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////
  void makeMyEnumTypeTemplateProperties(
  class AcRxMemberCollectionBuilder & collectionBuilder, void*);
  template<>
int MyEnumTypeTemplate<MyEnum>::subToString(
  const void *instance, ACHAR *buffer, size_t sizeInACHARs,
  AcRxValueType::StringFormat format) const
{
  const ACHAR* formatString = L"%d";
  MyEnum & value = *(MyEnum*)instance;
  if (buffer==NULL)
    return _scwprintf(formatString,value);
  return swprintf_s(buffer,sizeInACHARs,formatString,value);
}
  template<>
bool MyEnumTypeTemplate<MyEnum>::subEqualTo(
  const void *a, const void* b) const
{
  MyEnum & v1 = *(MyEnum*)a;
  MyEnum & v2 = *(MyEnum*)b;
  return v1==v2;
}
  template<>
struct AcRxValueType::Desc< MyEnum >
{
  __declspec(dllexport) static const AcRxValueType& value() throw();
  static void del();
};
  MyEnumTypeTemplate<MyEnum>* s_pMyEnumTypeTemplate = NULL;
  const AcRxValueType& AcRxValueType::Desc< MyEnum >::value() throw()
{
  if (s_pMyEnumTypeTemplate==NULL)
  {
    s_pMyEnumTypeTemplate = new MyEnumTypeTemplate<MyEnum>(
      L"MyEnumProperties",&makeMyEnumTypeTemplateProperties);
    AcRxEnumTag* pTag;
    pTag = new  AcRxEnumTag  (L"One", (int)0);
    s_pMyEnumTypeTemplate->append(*pTag);
    pTag = new  AcRxEnumTag  (L"Two", (int)1);
    s_pMyEnumTypeTemplate->append(*pTag);
    pTag = new  AcRxEnumTag  (L"Three", (int)2);
    s_pMyEnumTypeTemplate->append(*pTag);
    pTag = new  AcRxEnumTag  (L"Four", (int)3);
    s_pMyEnumTypeTemplate->append(*pTag);
  }
  return *s_pMyEnumTypeTemplate;
};
  // This should be called when the value type is not needed anymore
// Best call it when the module gets unloaded (On_kUnloadAppMsg)
void AcRxValueType::Desc< MyEnum >::del()
{
  if (s_pMyEnumTypeTemplate)
  {
    const ACHAR * name = s_pMyEnumTypeTemplate->name();
      if (acrxSysRegistry())
      acrxClassDictionary->remove(s_pMyEnumTypeTemplate->name());
      s_pMyEnumTypeTemplate = NULL;
  }
};
  void makeMyEnumTypeTemplateProperties(
  class AcRxMemberCollectionBuilder & collectionBuilder, void*)
{
}
  /////////////////////////////////////////////////////////////////////
// MyListProperty ///////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////
  const ACHAR * MyListProperty::kCategoryName = _T("My Category");
  AcRxCategory * MyListProperty::category = NULL;
  MyListProperty::MyListProperty() :
AcRxProperty(_T("My List Property"),
  AcRxValueType::Desc< MyEnum >::value())
{
  if (category == NULL)
  {
    AcRxCategory * parent =  AcRxCategory::rootCategory();
    category = parent->findDescendant(kCategoryName);
    if (category == NULL)
      category = new AcRxCategory(kCategoryName, parent);
  }
    // OPM = Object Property Manager / Property Palette
    // Add the Placement attribute to set under which category in
  // the OPM the property will be shown
  attributes().add(new AcRxUiPlacementAttribute(kCategoryName, 0));
  // Add this attribute so that AutoCAD will automatically create
  // the COM wrapper for this property, i.e. it will be visible
  // in OPM
  attributes().add(new AcRxGenerateDynamicPropertiesAttribute());
}
  MyListProperty::~MyListProperty()
{
}
  /// <summary>
/// This is called by the system to get the property value for
/// a specific object
/// </summary>
Acad::ErrorStatus MyListProperty::subGetValue(
  const AcRxObject* pO, AcRxValue& value) const
{
  AcDbEntity * ent = AcDbEntity::cast(pO);
  if (ent == NULL)
    return Acad::eNotThatKindOfClass;
    // Get the value from the custom entity
  // or wherever we stored the value
  AEN1MyCircle * pMyCircle = AEN1MyCircle::cast(pO);
  value = AcRxValue(static_cast<MyEnum>(pMyCircle->m_myEnum)); 
    return Acad::eOk;
}
  /// <summary>
/// This is called by the system to retrieve the property value for
/// a specific object
/// </summary>
Acad::ErrorStatus MyListProperty::subSetValue(
  AcRxObject* pO, const AcRxValue& value) const
{
  AcDbEntity * ent = AcDbEntity::cast(pO);
  if (ent == NULL)
    return Acad::eNotThatKindOfClass;
    const MyEnum * val = rxvalue_cast<MyEnum>(&value);
  if (val == NULL)
    return Acad::eInvalidInput;
    // Set the property of the custom entity
  // or store it wherever we want to
  AEN1MyCircle * pMyCircle = AEN1MyCircle::cast(pO);
  pMyCircle->m_myEnum = *val; 
    return Acad::eOk;
}
  /// <summary>
/// This is called to create an instance of our class
/// </summary>
AcRxObject * MyListProperty::makeMyListProperty()
{
  return new MyListProperty();
}

## 评论

**内容**: grx said...
Could you show me the AEN1MyCircle's code? Thanks!
Reply
04/23/2022 at 10:28 PM

---
**内容**: Hanauer said in reply to grx...
I think you find it on DevTV - Ubiquity example.
https://adndevblog.typepad.com/autocad/2012/04/devtv-non-com-property-system.html
Reply
04/25/2022 at 06:25 AM

---
