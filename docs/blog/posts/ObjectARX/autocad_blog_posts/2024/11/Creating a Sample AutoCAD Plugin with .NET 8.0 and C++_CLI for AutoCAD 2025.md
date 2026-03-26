---
title: "Creating a Sample AutoCAD Plugin with .NET 8.0 and C++/CLI for AutoCAD 2025"
date: 2024-11-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Plugin
description: "In this article, will walk through the development of a simple AutoCAD plugin using C++/CLI. The plugin will add a feature to draw circles dynamica..."
author: Autodesk
---
# Creating a Sample AutoCAD Plugin with .NET 8.0 and C++/CLI for AutoCAD 2025

发布日期: 2024-11-01

原始链接: https://adndevblog.typepad.com/autocad/2024/11/creating-a-sample-autocad-plugin-with-net-80-and-ccli-for-autocad-2025.html

## 文章内容

By Madhukar Moogala
In this article, will walk through the development of a simple AutoCAD plugin using C++/CLI. The plugin will add a feature to draw circles dynamically, where users can specify the radius and the plugin will generate a random color for each circle.
We will break the plugin down into three major parts:
AutoCAD Database Helper Class
UI Form Implementation
ObjectARX Entry Point
Part 1: AutoCAD Database Helper Class
In AutoCAD, entities such as circles, lines, and other objects are stored in the AutoCAD database. The AcDbHelper class in our plugin facilitates the creation and manipulation of AutoCAD entities.
Smart Pointer for AutoCAD Database Objects
We start by creating a unique_db_ptr template class to manage AutoCAD objects with a smart pointer. This ensures that AutoCAD objects are correctly cleaned up after use.
      
```cpp
    template  struct unique_db_ptr : public std::unique_ptr
      {
          unique_db_ptr(T* t) : std::unique_ptr(t, closeOrDeleteDbObj) { }
      
          static unique_db_ptr create()
          {
              T* newObj = new T();
              return unique_db_ptr(newObj);
          }
      
          // Helper function for smart pointer cleanup
          static void closeOrDeleteDbObj(AcDbObject* pObj)
          {
              if (pObj->objectId().isNull())
                  delete pObj;
              else
                  pObj->close();
          }
      };
```


​      
​    
Adding Entities to the Database
We also define a method to add entities like circles to AutoCAD's model space, ensuring they are correctly appended to the database.
​    
```cpp
static bool addToDb(AcDbEntity* pEnt, AcDbDatabase* pDb = nullptr)
{
if (!pDb)
    pDb = acdbHostApplicationServices()->workingDatabase();

unique_db_ptr ent(pEnt);
AcDbBlockTable* pBt;
if (Acad::eOk != pDb->getBlockTable(pBt, AcDb::kForRead))
    return false;

unique_db_ptr bt(pBt);
AcDbBlockTableRecord* pMs;
if (Acad::eOk != pBt->getAt(ACDB_MODEL_SPACE, pMs, AcDb::kForWrite))
    return false;

return Acad::eOk == unique_db_ptr(pMs)->appendAcDbEntity(ent.get());
}
```

  

Creating and Adding Circles
The createCircle method creates a circle with a specified radius and color index, then adds it to the database:

```cpp
static bool createCircle(const AcGePoint3d& center, double radius, int colorIndex = 1)
  {
      auto circlePtr = unique_db_ptr::create();
      if (!circlePtr)
          return false;

      AcDbCircle* circle = circlePtr.get();
      circle->setDatabaseDefaults();
      circle->setRadius(radius);
      circle->setColorIndex(colorIndex);
      circle->setCenter(center);
      return addToDb(circle);
  }
```

  

Part 2: UI Form Implementation
Now, let’s move on to creating the user interface (UI) that interacts with the AutoCAD database. We’ll use Windows Forms in C++/CLI for this purpose.
MainForm Class
The MainForm class represents the UI, containing a button to draw a circle and a numeric input for the circle radius. It uses a task-based asynchronous method to perform the drawing operation on the main AutoCAD thread.
    
```cpp
  public ref class MainForm : public Form
  {
  private:
      Button^ drawButton;
      NumericUpDown^ radiusInput;
      Label^ radiusLabel;

      void InitializeComponent()
      {
          //adding controls to the form and initialising properties
      }

      Task^ DrawCircleAsync(System::Object^ data)
      {
          //draw the circle
      }

      void DrawButton_Click(System::Object^ sender, System::EventArgs^ e)
      {
          // Handle click event
          auto dm = Autodesk::AutoCAD::ApplicationServices::Core::Application::DocumentManager;

          // Create the delegate with the correct syntax
          auto callback = gcnew Func(this, &MainForm::DrawCircleAsync);
         
          // Execute the callback in the command context
          auto task = dm->ExecuteInCommandContextAsync(callback, nullptr);
           task->GetResult();
          // Enable the button
           drawButton->Enabled = true;
          // Set focus to the drawing area and zoom extents
           AcadUtils::Utils::SetFocusToDwgView();
           AcadUtils::Utils::CancelAndRunCmds("_.zoom\n_extents\n");
      }

  public:
      MainForm()
      {
          InitializeComponent();
      }
  };
```

  

ExecuteInCommandContextAsync Method
In this code, the ExecuteInCommandContextAsync method is used to execute a callback (in this case, the DrawCircleAsync method) within AutoCAD's command context. The primary reason for using this API is to ensure that any interactions with AutoCAD, especially those that modify the drawing or perform operations on the AutoCAD database, are executed on the correct thread, which is the AutoCAD main thread.
Why Use ExecuteInCommandContextAsync?
AutoCAD, being a single-threaded application, has strict rules about how commands and modifications to the AutoCAD database should be performed. Interacting with AutoCAD from another thread, such as a UI thread, can cause problems because it bypasses AutoCAD's synchronization mechanisms, leading to potential crashes, invalid operations, or unexpected behavior.
SynchronizationContext Issue
When you display a WinForm dialog (like MainForm in your code), it restores the 'previous' SynchronizationContext, which in this case is the default context. This default context attempts to execute continuations using the thread pool, not the main AutoCAD thread. Since AutoCAD requires that commands (such as modifying the database or interacting with the drawing) be run on its main thread, executing on a background thread (via the thread pool) can cause synchronization issues.
AutoCAD doesn't like this because it expects all UI operations and database modifications to occur on the main AutoCAD thread. If you try to execute these operations on a different thread (e.g., using the thread pool), AutoCAD's internal threading model will not handle it correctly.
How ExecuteInCommandContextAsync Solves This
By using ExecuteInCommandContextAsync, the callback (i.e., the DrawCircleAsync method) is explicitly executed within AutoCAD's command context. This method ensures that the operation is correctly scheduled on the AutoCAD thread, which means:
Correct Threading: It guarantees that the AutoCAD API calls are made on the main AutoCAD thread, which is crucial for thread safety.
Synchronization Context: It sets up the correct synchronization context for the operation, so any continuation (like UI updates or database operations) that happens after this method call will respect AutoCAD's threading model and ensure that UI updates (like enabling buttons) are done on the UI thread without causing conflicts.
Asynchronous Execution: It allows the asynchronous execution of AutoCAD commands without blocking the UI thread or causing AutoCAD to freeze while waiting for the operation to complete. The GetResult() method ensures that the UI thread waits for the task to finish before proceeding.
Part 3: ObjectARX Entry Point
The CArxNetCoreApp class represents the entry point of our AutoCAD plugin. It registers the application and launches the UI dialog.
    
      class CArxNetCoreApp : public AcRxArxApp
      {
      public:
          virtual AcRx::AppRetCode On_kInitAppMsg(void* pkt) { 
            return AcRxArxApp::On_kInitAppMsg(pkt); }
          virtual AcRx::AppRetCode On_kUnloadAppMsg(void* pkt) { 
            return AcRxArxApp::On_kUnloadAppMsg(pkt); }
          virtual void RegisterServerComponents() {}
    
          static void MADGUIToolLaunch()
          {
              try
              {
                  auto form = gcnew UIForms::MainForm();
                  Autodesk::AutoCAD::ApplicationServices::Application::ShowModelessDialog(form);
              }
              catch (System::Exception^ ex)
              {
                  acutPrintf(L"\nException occurred: %s", ex->Message);
              }
          }
      };

  

Conclusion
This plugin demonstrates how to integrate AutoCAD with C++/CLI, offering a simple yet powerful tool to interact with AutoCAD's database, create entities, and provide a user-friendly interface for drawing circles. The use of smart pointers, task-based asynchronous methods, and Windows Forms for UI design highlights the flexibility and power of combining C++/CLI with AutoCAD's ObjectARX SDK.
By following the steps outlined in this tutorial, you can build and expand upon this basic plugin to add more features and functionality to AutoCAD.
View on GitHub


//-----------------------------------------------------------------------------
//----- acrxEntryPoint.cpp
//-----------------------------------------------------------------------------
#include "StdAfx.h"
#include "resource.h"
//-----------------------------------------------------------------------------
#define szRDS _RXST("MAD")
using namespace System;
using namespace System::Windows::Forms;
using namespace System::Threading::Tasks;
using namespace System::Drawing;
using namespace Autodesk::AutoCAD::ApplicationServices::Core;
using namespace Autodesk::AutoCAD::Internal;
// Part 1: AutoCAD Database Helper Class
//----------------------------------------
class AcDbHelper
{
public:
    // Smart pointer for AutoCAD database objects
    template <class T> struct unique_db_ptr : public std::unique_ptr<T, void(*)(AcDbObject*)>
    {
        unique_db_ptr<T>(T* t) : std::unique_ptr<T, void(*)(AcDbObject*)>(t, closeOrDeleteDbObj) { }
        static unique_db_ptr<T> create()
        {
            T* newObj = new T();
            return unique_db_ptr<T>(newObj);
        }
    };
    // Add entity to model space
    static bool addToDb(AcDbEntity* pEnt, AcDbDatabase* pDb = nullptr)
    {
        if (!pDb)
            pDb = acdbHostApplicationServices()->workingDatabase();
        unique_db_ptr<AcDbEntity> ent(pEnt);
        AcDbBlockTable* pBt;
        if (Acad::eOk != pDb->getBlockTable(pBt, AcDb::kForRead))
            return false;
        unique_db_ptr<AcDbBlockTable> bt(pBt);
        AcDbBlockTableRecord* pMs;
        if (Acad::eOk != pBt->getAt(ACDB_MODEL_SPACE, pMs, AcDb::kForWrite))
            return false;
        return Acad::eOk == unique_db_ptr<AcDbBlockTableRecord>(pMs)->appendAcDbEntity(ent.get());
    }
    // Create and add circle to database
    static bool createCircle(const AcGePoint3d& center, double radius, int colorIndex = 1)
    {
        auto circlePtr = unique_db_ptr<AcDbCircle>::create();
        if (!circlePtr)
            return false;
        AcDbCircle* circle = circlePtr.get();
        circle->setDatabaseDefaults();
        circle->setRadius(radius);
        circle->setColorIndex(colorIndex);
        circle->setCenter(center);
        return addToDb(circle);
    }
    // Generate a random color index
    static int getRandomColorIndex()
    {
        int colorArray[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int index = rand() % 10;
        return (colorArray[index]);
    }
private:
    // Helper function for smart pointer cleanup
    static void closeOrDeleteDbObj(AcDbObject* pObj)
    {
        if (pObj->objectId().isNull())
            delete pObj;
        else
            pObj->close();
    }
};
// Part 2: UI Form Implementation with Clean Design
//----------------------------------------
namespace UIForms {
    namespace AcadApp = Autodesk::AutoCAD::ApplicationServices::Core;
    namespace AcadUtils = Autodesk::AutoCAD::Internal;
    public ref class MainForm : public Form
    {
    private:
                 // UI Controls
        Button^ drawButton;
        NumericUpDown^ radiusInput;
        Label^ radiusLabel;
        // Initialize the form controls
        void InitializeComponent()
        {
            this->Text = "Advanced AutoCAD Drawing Tool";
            this->Width = 400;
            this->Height = 200;
            this->FormBorderStyle = System::Windows::Forms::FormBorderStyle::FixedDialog;
            this->StartPosition = FormStartPosition::CenterScreen;
            // Radius input setup
            radiusLabel = gcnew Label();
            radiusLabel->Text = "Circle Radius:";
            radiusLabel->Location = Point(50, 40);
            radiusLabel->AutoSize = true;
            radiusInput = gcnew NumericUpDown();
            radiusInput->Location = Point(150, 38);
            radiusInput->Minimum = 1;
            radiusInput->Maximum = 10000;
            radiusInput->Value = 10;
            radiusInput->DecimalPlaces = 2;
            // Draw button setup
            drawButton = gcnew Button();
            drawButton->Text = "Draw Circle";
            drawButton->Location = Point(150, 80);
            drawButton->Width = 100;
            drawButton->Click += gcnew EventHandler(this, &MainForm::DrawButton_Click);
            // Add controls to form
            this->Controls->Add(radiusLabel);
            this->Controls->Add(radiusInput);
            this->Controls->Add(drawButton);
        }
        // Helper method that performs the drawing operation on the main thread
        Task^ DrawCircleAsync(System::Object^ data)
        {
            // Create a TaskCompletionSource to manage the task lifecycle
            auto tcs = gcnew TaskCompletionSource();
            try
            {
                double radius = Convert::ToDouble(radiusInput->Value);
                int colorIndex = AcDbHelper::getRandomColorIndex();
                if (AcDbHelper::createCircle(AcGePoint3d::kOrigin, radius, colorIndex))
                {
                    //Marks the task as successfully completed
                    tcs->SetResult();
                }
                else
                {
                    throw gcnew Exception("Failed to create circle");
                }
            }
            catch (System::Exception^ ex)
            {
                // Marks the task as completed with an exception
                tcs->SetException(ex);
            }
            return tcs->Task;
        }
        /// <summary
        /// Handles the "Draw Circle" button click, initiates the async drawing operation, and handles task completion or errors.
        ///</summary>
        void DrawButton_Click(System::Object^ sender, System::EventArgs^ e)
        {
            // Disable the button to prevent multiple clicks
            drawButton->Enabled = false;
            try
            {
                // Retrieve the DocumentManager to interact with AutoCAD's document system.
                auto dm = Autodesk::AutoCAD::ApplicationServices::Core::Application::DocumentManager;
                // Create a delegate for the DrawCircleAsync method, which returns a Task.
                auto callback = gcnew Func<Object^, Task^>(this, &MainForm::DrawCircleAsync);
                //  Execute the delegate asynchronously within AutoCAD's command context.
                //  This ensures that the drawing operation happens in the correct environment.
                auto task = dm->ExecuteInCommandContextAsync(callback, nullptr);
               //Attach a completion handler(OnCompleted) to the task to handle post - operation actions.
                task->OnCompleted(gcnew Action(this, &MainForm::OnDrawCompleted));
            }
            catch (System::Exception^ ex)
            {
                MessageBox::Show("Error: " + ex->Message, "Error",
                MessageBoxButtons::OK, MessageBoxIcon::Error);
            }
        }
        void OnDrawCompleted()
        {
            try
            { 
                // Enable the button
                drawButton->Enabled = true;
                // Set focus to the drawing area and zoom extents
                AcadUtils::Utils::SetFocusToDwgView();
                AcadUtils::Utils::CancelAndRunCmds("_.zoom\n_extents\n");
            }
            catch (System::Exception^ ex)
            {
                MessageBox::Show("Error: " + ex->Message, "Error",
                MessageBoxButtons::OK, MessageBoxIcon::Error);
            }
        }  
    public:
        MainForm() {
            InitializeComponent();
        }
    };
}
// Part 3: ObjectARX Entry Point
//----------------------------------------
class CArxNetCoreApp : public AcRxArxApp {
public:
    CArxNetCoreApp() : AcRxArxApp() {}
    virtual AcRx::AppRetCode On_kInitAppMsg(void* pkt) {
        return AcRxArxApp::On_kInitAppMsg(pkt);
    }
    virtual AcRx::AppRetCode On_kUnloadAppMsg(void* pkt) {
        return AcRxArxApp::On_kUnloadAppMsg(pkt);
    }
    virtual void RegisterServerComponents() {
    }
    static void MADGUIToolLaunch() {
        UIForms::MainForm^ form = gcnew UIForms::MainForm();
        try
        {
            Autodesk::AutoCAD::ApplicationServices::Application::ShowModelessDialog(form);
        }
        catch (System::Exception^ ex)
        {
            acutPrintf(L"\nException occurred: %s", ex->Message);
        }       
    }   
    };
IMPLEMENT_ARX_ENTRYPOINT(CArxNetCoreApp)
ACED_ARXCOMMAND_ENTRY_AUTO(CArxNetCoreApp, MADGUI, ToolLaunch, ToolLaunch, ACRX_CMD_MODAL, NULL)
view raw
AutoCADPlugin.cpp hosted with ❤ by GitHub

## 评论

**内容**: happy wheels said...
I am typically the one to blog, and we truly value your posts. This article has piqued my curiosity about the topic. Please allow me to bookmark your blog and continue to check the selection details.
Reply
12/12/2024 at 12:34 AM

---
**内容**: slope said...
Slope brings a sense of conquest, making players always want to try again to get a higher score.
Reply
12/22/2024 at 06:32 PM

---
