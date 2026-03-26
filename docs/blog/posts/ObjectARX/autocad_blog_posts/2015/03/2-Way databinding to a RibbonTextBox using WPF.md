---
title: "2-Way databinding to a RibbonTextBox using WPF"
date: 2015-03-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "To have a RibbonTextBox automatically update your data when the user updates the ribbon textbox and vice-versa, you can use the RibbonTextBox.TextV..."
author: Autodesk
---
# 2-Way databinding to a RibbonTextBox using WPF

发布日期: 2015-03-01

原始链接: https://adndevblog.typepad.com/autocad/2015/03/2-way-databinding-to-a-ribbontextbox-using-wpf.html

## 文章内容

By Balaji Ramamoorthy
To have a RibbonTextBox automatically update your data when the user updates the ribbon textbox and vice-versa, you can use the RibbonTextBox.TextValueBinding to establish a 2-way databinding. Here is a sample code :
 public  class  ManufacturerData 
  : System.ComponentModel.INotifyPropertyChanged
 {
     private  string manufacturerName;
       public  ManufacturerData() { }
       public  ManufacturerData(String manufacturer)
     {
         manufacturerName = manufacturer;
     }
       public  String ManufacturerProperty
     {
         get { return  manufacturerName; }
         set
         {
             manufacturerName = value;
             OnPropertyChanged("ManufacturerProperty" );
         }
     }
       public  event  
   System.ComponentModel.
   PropertyChangedEventHandler PropertyChanged;
       private  void  OnPropertyChanged(string info)
     {
         System.ComponentModel.PropertyChangedEventHandler 
    handler = PropertyChanged;
         if  (handler != null)
         {
             handler(this , new  System.ComponentModel.
     PropertyChangedEventArgs(info));
         }
     }
 }
   public  class  Commands 
 {
     public  static  ManufacturerData _data 
   = new  ManufacturerData("Autodesk" );
     public  static  bool  _added = false ;
       [CommandMethod("RTB" )]
     static  public  void  RibbonTextBoxMethod()
     {
         if  (!_added)
         {
             Autodesk.Windows.RibbonControl rc 
     = Autodesk.Windows.ComponentManager.Ribbon;
             Autodesk.Windows.RibbonTab rt = null;
             foreach (Autodesk.Windows.RibbonTab tab 
             in rc.Tabs)
             {
                 if  (tab.AutomationName.Equals("Add-ins" ))
                 {
                     rt = tab;
                     break ;
                 }
             }
             if  (rt == null)
                 return ;
               Autodesk.Windows.RibbonPanelSource rps 
     = new  Autodesk.Windows.RibbonPanelSource();
             rps.Title = "MyPanel" ;
             Autodesk.Windows.RibbonPanel rp 
     = new  Autodesk.Windows.RibbonPanel();
             rp.Source = rps;
             rt.Panels.Add(rp);
               Autodesk.Windows.RibbonTextBox rtb 
     = new  Autodesk.Windows.RibbonTextBox();
             rtb.Id = "MyRTB" ;
             rtb.Text = "Manufacturer" ;
             rtb.ShowText = true ;
             rps.Items.Add(rtb);
             rt.IsActive = true ;
               System.Windows.Data.Binding myBinding 
     = new  System.Windows.Data.Binding
     ("ManufacturerProperty" );
             myBinding.Source = _data;
             myBinding.Mode 
     = System.Windows.Data.BindingMode.TwoWay;
             rtb.TextValueBinding = myBinding;
               _added = true ;
         }
     }
 }

## 评论

**内容**: Craig said...
Hi Balaji,
Thanks for the post.
I want to evolve this example to use an ObservableCollection and bind it to a RibbonCombo.
I've got as far as the combo does contain objects but does not display a single property for example the name. I've tried setting the path nut the binding fails completely; no objects appear in the combo.
Is there another example elsewhere that demonstrates this?
Thanks
Reply
07/29/2016 at 04:42 AM

---
