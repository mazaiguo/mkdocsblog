---
title: "How to avoid ‘Trust This Publisher’ Dialog"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - API
  - Plugin
description: "From 2016, if modules are signed and the certificate [.cer] file used to sign the modules  is not registered in store, or modules are not located i..."
author: Autodesk
---
# How to avoid ‘Trust This Publisher’ Dialog

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/how-to-avoid-trust-this-publisher-dialog.html

## 文章内容

By Madhukar Moogala
From 2016, if modules are signed and the certificate [.cer] file used to sign the modules  is not registered in store, or modules are not located in any of the trusted location, a window will pop-up asking user to trust the publisher, to avoid this pesky window dialog, you can follow any of these steps.
1. Adding certificate to trusted store during installation:
There is no inherent support in msi to add certificate to the certificate store. This has to be accomplished using a custom action. There are two ways to accomplish it using the custom action.
Use certutil.exe, a command line tool from Microsoft to install the certificate.
Usage: certutil -addstore <storename> <yourcertfile.cer>
Example: certutil.exe -addstore TrustedPublisher mycertfile.cer
Use the Microsoft crypto API to install the certificate to the store.
Sample code is given below, please do the appropriate error checking.
.NET:
X509Certificate2 certificate =
    new X509Certificate2(@"c:\temp\mycertfile.cer");
  /*To load Pfx file to store*/
//  X509Certificate2 certificate = new X509Certificate2(@"C:\temp\mycert.pfx", "pwd123", X509KeyStorageFlags.PersistKeySet);
X509Store store =
    new X509Store(StoreName.TrustedPublisher,
                  StoreLocation.LocalMachine);
store.Open(OpenFlags.ReadWrite);
store.Add(certificate);
store.Close();
  C++:
#include <wincrypt.h>
#include <windows.h>
#include <wintrust.h>
  #pragma comment(lib, "crypt32.lib")
  #define ENCODING (X509_ASN_ENCODING | PKCS_7_ASN_ENCODING)
  typedef struct {
LPWSTR lpszProgramName;
LPWSTR lpszPublisherLink;
LPWSTR lpszMoreInfoLink;
} SPROG_PUBLISHERINFO, *PSPROG_PUBLISHERINFO;
  class X509Certificate
{
public:
X509Certificate();
~X509Certificate(void);
bool initialize(LPCTSTR pszFileName);
bool isCertificateInTrustedPubStore();
bool installCertificateToTrustedPubStore();
private:
HCERTSTORE mhStore;
HCRYPTMSG mhMsg;
CString msFileName;
PCMSG_SIGNER_INFO mpSignerInfo;
SPROG_PUBLISHERINFO mProgPubInfo;
PCCERT_CONTEXT mpCertContext;
};
  X509Certificate::X509Certificate(void)
: mhStore(NULL),
mhMsg(NULL),
mpSignerInfo(NULL),
mpCertContext(NULL)
{
ZeroMemory(&mProgPubInfo, sizeof(mProgPubInfo));
}
  X509Certificate::~X509Certificate(void)
{
if (mProgPubInfo.lpszProgramName != NULL)
free(mProgPubInfo.lpszProgramName);
if (mProgPubInfo.lpszPublisherLink != NULL)
free(mProgPubInfo.lpszPublisherLink);
if (mProgPubInfo.lpszMoreInfoLink != NULL)
free(mProgPubInfo.lpszMoreInfoLink);
if (mpSignerInfo != NULL)
free(mpSignerInfo);
if (mpCertContext != NULL)
CertFreeCertificateContext(mpCertContext);
if (mhStore != NULL)
CertCloseStore(mhStore, 0);
if (mhMsg != NULL)
CryptMsgClose(mhMsg);
}
  bool X509Certificate::initialize(LPCTSTR pszFileName)
{
if (!PathFileExists(pszFileName))
return false;
msFileName = pszFileName;
DWORD dwEncoding, dwContentType, dwFormatType;
DWORD dwSignerInfo;
CERT_INFO CertInfo;
BOOL fResult = CryptQueryObject(CERT_QUERY_OBJECT_FILE,
    pszFileName,
    CERT_QUERY_CONTENT_FLAG_PKCS7_SIGNED_EMBED,
    CERT_QUERY_FORMAT_FLAG_BINARY,
    0,
    &dwEncoding,
    &dwContentType,
    &dwFormatType,
    &mhStore,
    &mhMsg,
    NULL);
fResult = CryptMsgGetParam(mhMsg,
CMSG_SIGNER_INFO_PARAM,
0,
NULL,
&dwSignerInfo);
if (!fResult)
return false;
// Allocate memory for signer information.
mpSignerInfo = (PCMSG_SIGNER_INFO)malloc(dwSignerInfo);
if (!mpSignerInfo)
return false;
// Get Signer Information.
fResult = CryptMsgGetParam(mhMsg,
CMSG_SIGNER_INFO_PARAM,
0,
(PVOID)mpSignerInfo,
&dwSignerInfo);
if (!fResult)
return false;
// Search for the signer certificate in the temporary
// certificate store.
CertInfo.Issuer = mpSignerInfo->Issuer;
CertInfo.SerialNumber = mpSignerInfo->SerialNumber;
mpCertContext = CertFindCertificateInStore(mhStore,
                ENCODING,
                0,
                CERT_FIND_SUBJECT_CERT,
                (PVOID)&CertInfo,
                NULL);
if (!mpCertContext)
{
return false;
}
return true;
}
bool X509Certificate::isCertificateInTrustedPubStore()
{
if (mpCertContext == NULL)
return false;
HCERTSTORE hCertStore = NULL;
PCCERT_CONTEXT  pFoundCertContext = NULL;
__try
{
HCERTSTORE hCertStore = CertOpenStore(
CERT_STORE_PROV_SYSTEM,
0,
0,
CERT_STORE_OPEN_EXISTING_FLAG |
CERT_SYSTEM_STORE_CURRENT_USER,
_T("TrustedPublisher"));
if (hCertStore == NULL)
return false;
pFoundCertContext = CertFindCertificateInStore(hCertStore, ENCODING,
0, CERT_FIND_EXISTING, mpCertContext, NULL);
}
__finally
{
if (pFoundCertContext != NULL)
{
CertFreeCertificateContext(pFoundCertContext);
}
if (hCertStore != NULL)
{
CertCloseStore(hCertStore, 0);
}
}
if (pFoundCertContext == NULL)
return false;
return true;
}
bool X509Certificate::installCertificateToTrustedPubStore()
{
if (mpCertContext == NULL)
return false;
  bool bRet = false;
HCERTSTORE hCertStore = NULL;
__try
{
HCERTSTORE hCertStore = CertOpenStore(
CERT_STORE_PROV_SYSTEM,
0,
0,
CERT_STORE_OPEN_EXISTING_FLAG |
CERT_SYSTEM_STORE_LOCAL_MACHINE,
_T("TrustedPublisher"));
if (hCertStore == NULL)
return false;
if (CertAddCertificateContextToStore(hCertStore, mpCertContext, CERT_STORE_ADD_NEWER, NULL))
{
bRet = true;
}
else
{
if (GetLastError() == CRYPT_E_EXISTS)
{
bRet = true;
}
}
}
__finally
{
if (hCertStore != NULL)
CertCloseStore(hCertStore, 0);
}
return bRet;
}
2. Check the Box
Check the check box in the message which says “always trust the applications from XXXXX”
3. Trusted Location
Install the modules in C:\Program Files\Autodesk\ApplicationPlugins or C:\Program Files (x86)\Autodesk\ApplicationPlugins

## 评论

**内容**: Senthilkumar C K said...
Hi Madhukar,
Thanks for the valuable info.
Is there any way to avoid the pop-up for first time itself?
Thanks,
Senthilkumar C K
Reply
05/04/2015 at 05:13 AM

---
**内容**: Madhukar Moogala said...
Yes, you need to install certificate to store during installation of your plugin, this can be achieved by custom action when your prepare your MSI.
Reply
05/04/2015 at 05:23 AM

---
**内容**: Madhukar Moogala said in reply to Madhukar Moogala...
If you are an ADN partner, Exchange store will help you.
Reply
05/04/2015 at 05:24 AM

---
**内容**: Anshuman Mor said...
Hi Madhukar, I want to use AcSignTool command line tool to sign my lisp files but there doesn't seem to be any documentation available to understand the tool behavior especially how I can supply a certificate to the AcSignTool to sign my files, can you please throw some light.
Reply
07/17/2015 at 06:05 AM

---
**内容**: LarsR said...
Hi Madhukar,
I have added a call to certutil in our installer to register our code signing certificate (.cer file). This works fine, but produces a command window flashing by at install time. To avoid this I am trying to implement the C++ code as custom action. I am having trouble with it - the CryptQueryObject() fails since the .cer file isnt in PKCS7, and not binary either (it's BASE64).
Changing the parameters to the function to CERT_QUERY_CONTENT_FLAG_ALL and CERT_QUERY_FORMAT_FLAG_ALL makes the call pass, but mhMsg is NULL so the rest fails.
Do you have any advice on how to get this to work?
Reply
06/02/2016 at 03:13 AM

---
**内容**: LarsR said in reply to LarsR...
I found the solution. The file passed to the C++ implementation should be a file signed with the certificate to install, i.e. an EXE or DLL file. Then the code works.
Br,
Lars
Reply
06/02/2016 at 07:05 AM

---
**内容**: Harry said...
Does this really work? It doesn't for me.
3. Trusted Location
Install the modules in C:\Program Files\Autodesk\ApplicationPlugins or C:\Program Files (x86)\Autodesk\ApplicationPlugins
Reply
08/21/2017 at 10:50 AM

---
**内容**: Madhukar Moogala said in reply to Harry...
Hi Harry,
Can you please elaborate your question ? checkIf the C:\Program Files\Autodesk\ApplicationPlugins or C:\Program Files (x86)\Autodesk\ApplicationPlugins are in trusted location in your AutoCAD profile ?
May be more generic one's are
%APPDATA%\Autodesk\ApplicationPlugins
%ALLUSERSPROFILE%\Autodesk\ApplicationPlugins
%ProgramFiles%\Autodesk\ApplicationPlugins
%ProgramFiles(x86)%\Autodesk\ApplicationPlugins (In 64-bit OS)
Reply
08/21/2017 at 11:30 PM

---
