---
title: "AutoCAD Ribbon runtime API with C++/CLI"
date: 2013-11-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - C++
  - CUI
description: "We already have several examples on our blog illustrating how to use the runtime Ribbon API from .Net, but none using C++/CLI, so I though it would..."
author: Autodesk
---
# AutoCAD Ribbon runtime API with C++/CLI

发布日期: 2013-11-01

原始链接: https://adndevblog.typepad.com/autocad/2013/11/autocad-ribbon-runtime-api-with-ccli.html

## 文章内容

By Philippe Leefsma
We already have several examples on our blog illustrating how to use the runtime Ribbon API from .Net, but none using C++/CLI, so I though it would be useful to place one. Plus this has already been asked by ADN developers in the past, so here it is.
There are several reasons why you would like to invoke that API from mix-managed code, here are the main ones I can think of:
- You just like the syntax (seriously?!)
- You want to directly invoke C++ code from your project
- You have existing MFC dialogs and don’t have the time or resources to migrate them to .Net
- You hate .Net and never want to give it a try, but you need to do some Ribbon customization in AutoCAD
For any of those reasons or even different ones, here is how to invoke the API from managed C++, note that the attached project contains more samples than what I just placed below:
[CommandMethod("AddButtonMixMng")]
void AddButtonMixMng()
{
          Autodesk::Windows::RibbonControl^ ribbonControl =
                   Autodesk::Windows::ComponentManager::Ribbon;
            RibbonTab^ Tab = gcnew RibbonTab();
          Tab->Title = "Test Ribbon";
          Tab->Id = gcnew String("TESTRIBBON_TAB_ID");
            ribbonControl->Tabs->Add(Tab);
            RibbonPanelSource^ srcPanel = gcnew RibbonPanelSource();
          srcPanel->Title = "Panel1";
            RibbonPanel^ panel = gcnew RibbonPanel();
          panel->Source = srcPanel;
          Tab->Panels->Add(panel);
            RibbonButton^ button = gcnew RibbonButton();
          button->Text = "Button Test";
          button->ShowText = true;
          button->ShowImage = true;
          button->Orientation =
              System::Windows::Controls::Orientation::Horizontal;
          button->Size = RibbonItemSize::Large;
          button->Image =
              getBitmapEmbedded(L"Icon16x16.png", 16, 16);
          button->LargeImage =
              getBitmapEmbedded(L"Icon32x32.png", 32, 32);
          button->CommandParameter = "._HelloCmdMng ";
          button->CommandHandler = gcnew ButtonCmdHandler();
            srcPanel->Items->Add(button);
            Tab->IsActive = true;
}
  BitmapImage^ getBitmapEmbedded(LPCTSTR pName, int height, int width)
{
          String^ str=
           System::Runtime::InteropServices::Marshal::PtrToStringUni(
              (IntPtr)(void*)pName);
          Bitmap^ image =
              gcnew Bitmap(Assembly::GetExecutingAssembly()->
                  GetManifestResourceStream(str));
            MemoryStream^ stream = gcnew MemoryStream();
          image->Save(stream,
              System::Drawing::Imaging::ImageFormat::Png);
          BitmapImage^ bmp = gcnew BitmapImage();
            bmp->BeginInit();
          bmp->StreamSource = stream;
          bmp->DecodePixelHeight = height;
          bmp->DecodePixelWidth = width;
          bmp->EndInit();
            return bmp;
}
  ref class ButtonCmdHandler : public System::Windows::Input::ICommand
{
    template < class T, class Cls > bool isInstance(Cls c)
    {
        return dynamic_cast< T >(c) != nullptr;
    }
  public:
                                  virtual bool __clrcall CanExecute(
              System::Object^ parameter) sealed
    {
        return true;
    }
      virtual event EventHandler^ CanExecuteChanged;
      virtual void __clrcall Execute(System::Object^ parameter) sealed
    {
        if (isInstance<RibbonButton^>(parameter))
        {
            RibbonButton^ button =
                dynamic_cast<RibbonButton^>(parameter);
              Document^ doc =
                Application::DocumentManager->MdiActiveDocument;
            doc->SendStringToExecute(
                dynamic_cast<String^>(button->CommandParameter),
                    true, false, false);
        }
    }
};
ArxMngRibbon.zip

## 评论

**内容**: Alexander Rivilis said...
Many thanks Philippe!
Reply
11/22/2013 at 04:32 AM

---
