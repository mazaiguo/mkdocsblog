---
title: "Trapping The Output From The AutoCAD Text Screen / Command Prompt"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Unicode
description: "How can I obtain the textual output of commands in AutoCAD, such as MASSPROPS as"
author: Autodesk
---
# Trapping The Output From The AutoCAD Text Screen / Command Prompt

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/trapping-the-output-from-the-autocad-text-screen-command-prompt.html

## 文章内容

By Philippe Leefsma
Q:
How can I obtain the textual output of commands in AutoCAD, such as MASSPROPS as
well as hide the output for certain commands at the command prompt?
A:
You can temporarily replace the AutoCAD host application services object with
your own. The important callback is consoleMessage(), which you can overload to
behave as you require - either to interpret or discard the calls made through
acutPrintf() to display text on the command-line or text screen. There are other
callbacks that require implementing, and these are to be forwarded to the
original host application services object.
It is very important to understand that this mechanism should only be used for
the shortest length of time possible. AutoCAD makes an assumption about its
standard host application services object - it will cast the pointer to a
non-published, derived class. It is therefore a matter of only replacing the
object as long as is absolutely necessary.
This approach has also not been thoroughly tested for all commands; therefore,
it should be used with caution and will need more complete testing on commands
not tested by this sample. Refer to the attached sample.
The key point is to derive a class from AcDbHostApplicationServices and override some necessary methods. The following is some implementation code of the class extracted from the attached project.
class MyHostAppServices : public AcDbHostApplicationServices
{
public:
   MyHostAppServices();
    virtual ~MyHostAppServices();
      virtual Acad::ErrorStatus findFile(
        ACHAR * pcFullPathOut,
        int   nBufferLength,
        const ACHAR * pcFilename,
        AcDbDatabase * pDb = NULL, // When this search
                                   // is related to a db
        AcDbHostApplicationServices::FindFileHint hint = kDefault);
      virtual AcadInternalServices* acadInternalServices();
    virtual const ProdIdCode prodcode();
      virtual void displayChar(ACHAR c) const;
    virtual void displayString(const ACHAR* string, int count) const;
      CString getOutput() const;
  private:
    AcDbHostApplicationServices *m_pOldHostServices;
        };
  CString m_szOutput;
  MyHostAppServices::MyHostAppServices()
{
        m_pOldHostServices = acdbHostApplicationServices();
        m_szOutput = "";
          Acad::ErrorStatus es = acdbSetHostApplicationServices( this );
      setWorkingGlobals( m_pOldHostServices->workingGlobals() );
    setWorkingDatabase( m_pOldHostServices->workingDatabase() );
}
  MyHostAppServices::~MyHostAppServices()
{
        acdbSetHostApplicationServices( m_pOldHostServices );
      setWorkingGlobals( m_pOldHostServices->workingGlobals() );
    setWorkingDatabase( m_pOldHostServices->workingDatabase() );
}
  Acad::ErrorStatus
MyHostAppServices::findFile(
                         ACHAR* pcFullPathOut,
             int   nBufferLength,
             const ACHAR* pcFilename,
             AcDbDatabase * pDb,
             AcDbHostApplicationServices::FindFileHint hint)
{
        return m_pOldHostServices->findFile(
                pcFullPathOut,
                nBufferLength,
                pcFilename,
                pDb,
                hint );
}
  AcadInternalServices*
MyHostAppServices::acadInternalServices()
{
    return m_pOldHostServices->acadInternalServices();
}
  const ProdIdCode
MyHostAppServices::prodcode()
{
    return m_pOldHostServices->prodcode();
}
  void
MyHostAppServices::displayChar( ACHAR c ) const
{
        if(c == 0) return; // To solve an issue in AutoCAD 2004.
          CString tmp;
        tmp.Format(L"%c", c );
        // We unfortunately need to cast away the const from this member
        // as it is required in the callback's header
        m_szOutput += tmp;
}
  void
MyHostAppServices::displayString( const ACHAR *string, int count ) const
{
        CString tmp( string );
        // We unfortunately need to cast away the const from this member
        // as it is required in the callback's header
        m_szOutput += tmp.Left( count );
}
  CString
MyHostAppServices::getOutput() const
{
        return m_szOutput;
}
  TrapOutput 2013.zip

