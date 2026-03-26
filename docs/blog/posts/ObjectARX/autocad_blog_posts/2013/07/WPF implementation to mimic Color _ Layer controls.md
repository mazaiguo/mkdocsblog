---
title: "WPF implementation to mimic Color / Layer controls"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Layer
description: "The ribbon controls such as "Object Color Gallery” and “Layer List Combo Box” ribbon controls are useful for accepting color and layer input and ca..."
author: Autodesk
---
# WPF implementation to mimic Color / Layer controls

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/wpf-implementation-to-mimic-color-layer-controls.html

## 文章内容

By Balaji Ramamoorthy
The ribbon controls such as "Object Color Gallery” and “Layer List Combo Box” ribbon controls are useful for accepting color and layer input and can be placed in ribbon tabs. These controls are data-bound and any user input using these controls also ensures that the entity property gets modified. If you wish to accept color / layer input without such automatic property update to the entity, then you will need your own implementation of the controls.
 Implementing such a control is a programming task involving WPF and with very little use of AutoCAD API. Iam sharing this project to provide a starting point for your own implementation which you can improvise based on your requirements and hopefully saves you some time. 
Here is some relevant portions of the code from the sample project that you can download.
1) ViewModel class and collection classes for the Color control :
// Class that represents the collection of AcadColor
public class AcadColors : ObservableCollection<AcadColor>
{
    public AcadColors()
        : base()
    {
        // List of colors to show in the combo box
        // along with their R,G,B values
        Add(new AcadColor("ByLayer", 255, 255, 255));
        Add(new AcadColor("ByBlock", 255, 255, 255));
        Add(new AcadColor("Red", 255, 0, 0));
        Add(new AcadColor("Yellow", 255, 255, 0));
        Add(new AcadColor("Green", 0, 255, 0));
        Add(new AcadColor("Cyan", 0, 255, 255));
        Add(new AcadColor("Blue", 0, 0, 255));
        Add(new AcadColor("Magenta", 255, 0, 255));
        Add(new AcadColor("White", 255, 255, 255));
        Add(new AcadColor("Select Colors...", 255, 255, 255));
    }
      // To check if a color with a given name
    // exists in this collection
    public bool Contains(String name)
    {
        for(int i = 0; i < Count; i++)
        {
            if(this[i].Name.Equals(name))
                return true;
        }
        return false;
    }
}
  // Class that represents a single color
public class AcadColor
{
    // Color Name
    public String Name
    {
        get;
        set;
    }
      // Brush to bind the label that displays the color
    public System.Windows.Media.SolidColorBrush ColorBrush
    {
        get
        {
            SolidColorBrush brush
                = new SolidColorBrush(
                               Color.FromRgb(Red, Green, Blue));
            return brush; 
        }
    }
      // Red byte
    public byte Red
    {
        get;
        set;
    }
      // Green byte
    public byte Green
    {
        get;
        set;
    }
      // Blue byte
    public byte Blue
    {
        get;
        set;
    }
      // The Color combo displays a "Select color..." option
    // In that case, we do not want to show the color label
    public String IsVisible
    {
        get
        {
            if(Name.Contains("Select"))
                return "Collapsed";
            return "Visible";
        }
    }
      public AcadColor(String name, byte R, byte G, byte B)
    {
        Name = name;
        Red = R;
        Green = G;
        Blue = B;
    }
      public AcadColor()
    {
        Name = String.Empty;
        Red = 255;
        Green = 255;
        Blue = 255;
    }
}
  // View Model for the Color Combo box to bind to
public class ColorViewModel : INotifyPropertyChanged
{
    // collection of colors that we will display
    AcadColors _myAcadColors = new AcadColors();
      // Flag to know if we are displaying the color selection dialog
    bool _showingColorDlg = false;
      public ColorViewModel()
    {
    }
      // Bound to the combo box source
    public AcadColors MyAcadColors
    {
        get
        {
            return _myAcadColors;
        }
    }
      // Default value to show
    private string _colorString = "Red";
      // Bound to the current selection in the combo
    public string ColorString
    {
        get
        {
            return _colorString;
        }
          set
        {
            if (_colorString != value)
            {
                String colorName = value;
                  //The Color combo displays a "Select color..."
                // option. If that is the option chosen,
                // show the color pick dialog
                if (! _showingColorDlg && value.Contains("Select"))
                {// Show the color pick dialog
                    _showingColorDlg = true;
                    colorName = ShowColorDlg();
                }
                _showingColorDlg = false;
                  _colorString = colorName;
                NotifyPropertyChanged("ColorString");
            }
        }
    }
      #region INotifyPropertyChanged Members
      private void NotifyPropertyChanged(string propertyName)
    {
        if (PropertyChanged != null)
        {
            PropertyChanged(this,
                    new PropertyChangedEventArgs(propertyName));
        }
    }
      public event PropertyChangedEventHandler PropertyChanged;
      #endregion
      // Displays the AutoCAD color pick dialog
    // Method returns the name to be displayed in the combo box
    public String ShowColorDlg()
    {
        Document  doc
                = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
          Autodesk.AutoCAD.Windows.ColorDialog dlg
                = new Autodesk.AutoCAD.Windows.ColorDialog();
        if (dlg.ShowDialog() !=  System.Windows.Forms.DialogResult.OK)
        {
            return String.Empty;
        }
          Autodesk.AutoCAD.Colors.Color clr = dlg.Color;
        if (! clr.IsByAci)
        {
            if (clr.IsByLayer)
            {
                return "ByLayer";
            }
            else if (clr.IsByBlock)
            {
                return "ByBlock";
            }
            else
            {
                String colorName
                    = String.Format("{0},{1},{2}",
                                clr.Red, clr.Green, clr.Blue);
                  if(_myAcadColors.Contains(colorName) == false)
                    _myAcadColors.Insert(
                        _myAcadColors.Count - 1,
                        new AcadColor(
                                        colorName,
                                        clr.Red,
                                        clr.Green,
                                        clr.Blue
                                     ));
                  return colorName;
            }
        }
        else
        {
            // Get the AutoCAD color index
            short colIndex = clr.ColorIndex;
              System.Byte byt = System.Convert.ToByte(colIndex);
            int rgb
                = Autodesk.AutoCAD.Colors.EntityColor.LookUpRgb(byt);
            long b = (rgb & 0xffL);
            long g = (rgb & 0xff00L) >> 8;
            long r = rgb >> 16;
              String colorName = String.Format("Color {0}", colIndex);
              if (_myAcadColors.Contains(colorName) == false)
                _myAcadColors.Insert(
                    _myAcadColors.Count - 1,
                    new AcadColor(
                                    colorName,
                                    (byte)r, (byte)g, (byte)b));
              return colorName;
        }
    }
}
2) ViewModel class and collection classes for the Layer control :
// Class that represents the collection of AcadLayer
public class AcadLayers : ObservableCollection<AcadLayer>
{
    public AcadLayers()
        : base()
    {
        // Gather the list of layers to show in the combo box
        // along with their color R,G,B values and layer state information
        Document doc
                = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
        Database db = doc.Database;
        using (Transaction tr
                    = db.TransactionManager.StartTransaction())
        {
            LayerTable lt
                = tr.GetObject  (
                                    db.LayerTableId,
                                    OpenMode.ForRead
                                ) as LayerTable;
              foreach(ObjectId ltrId in lt)
            {
                LayerTableRecord ltr
                        = tr.GetObject(
                                        ltrId,
                                        OpenMode.ForRead
                                       ) as LayerTableRecord;
                Autodesk.AutoCAD.Colors.Color clr = ltr.Color;
                  if (!clr.IsByAci)
                {
                    if (clr.IsByLayer)
                    {
                        Add(new AcadLayer(  ltr.Name,
                                            (byte)255,
                                            (byte)255,
                                            (byte)255,
                                            !ltr.IsOff,
                                            ltr.IsFrozen,
                                            ltr.IsLocked));
                    }
                    else if (clr.IsByBlock)
                    {
                        Add(new AcadLayer(  ltr.Name,
                                            (byte)255,
                                            (byte)255,
                                            (byte)255,
                                            !ltr.IsOff,
                                            ltr.IsFrozen,
                                            ltr.IsLocked));
                    }
                    else
                    {
                        Add(new AcadLayer(  ltr.Name,
                                            clr.Red,
                                            clr.Green,
                                            clr.Blue,
                                            !ltr.IsOff,
                                            ltr.IsFrozen,
                                            ltr.IsLocked));
                    }
                }
                else
                {
                    // Get the AutoCAD color index
                    short colIndex = clr.ColorIndex;
                      System.Byte byt = System.Convert.ToByte(colIndex);
                    int rgb
                        = Autodesk.AutoCAD.Colors.EntityColor.LookUpRgb(byt);
                    long b = (rgb & 0xffL);
                    long g = (rgb & 0xff00L) >> 8;
                    long r = rgb >> 16;
                      if (colIndex == 7)
                    {
                        if (r <= 128 && g <= 128 && b <= 128)
                        {// White
                            Add(new AcadLayer(  ltr.Name,
                                                255,
                                                255,
                                                255,
                                                !ltr.IsOff,
                                                ltr.IsFrozen,
                                                ltr.IsLocked));
                        }
                        else
                        {// Black
                            Add(new AcadLayer(  ltr.Name,
                                                0, 0, 0,
                                                !ltr.IsOff,
                                                ltr.IsFrozen,
                                                ltr.IsLocked));
                        }
                    }
                    else
                    {
                        Add(new AcadLayer(  ltr.Name,
                                            (byte)r,
                                            (byte)g,
                                            (byte)b,
                                            !ltr.IsOff,
                                            ltr.IsFrozen,
                                            ltr.IsLocked));
                    }
                }
            }
            tr.Commit();
        }
    }
}
  // Class that represents a single layer
public class AcadLayer
{
    // Name of the layer
    public String LayerName
    {
        get;
        set;
    }
      // Brush to bind the label that displays the layer color
    public System.Windows.Media.SolidColorBrush LayerColorBrush
    {
        get
        {
            SolidColorBrush brush
                = new SolidColorBrush(Color.FromRgb(Red, Green, Blue));
            return brush;
        }
    }
      // Red byte
    public byte Red
    {
        get;
        set;
    }
      // Green byte
    public byte Green
    {
        get;
        set;
    }
      // Blue byte
    public byte Blue
    {
        get;
        set;
    }
      bool _isOn;
    bool _isFrozen;
    bool _isLocked;
      // Determine if the layer is On
    // and return a string that can be bound to the
    // "Visibility" of an image.
    public String IsOn
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isOn = ! ltr.IsOff;
                tr.Commit();
            }
              if(_isOn)
                return "Visible";
              return "Collapsed";
        }
    }
      // Determine if the layer is Off
    // and return a string that can be bound to the
    // "Visibility" of an image.
    public String IsOff
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isOn = !ltr.IsOff;
                tr.Commit();
            }
              if (! _isOn)
                return "Visible";
              return "Collapsed";
        }
    }
      // Determine if the layer is frozen
    // and return a string that can be bound to the
    // "Visibility" of an image.
    public String IsFrozen
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isFrozen = ltr.IsFrozen;
                tr.Commit();
            }
              if(_isFrozen)
                return "Visible";
              return "Collapsed";
        }
    }
      // Determine if the layer is thawed
    // and return a string that can be bound to
    // the "Visibility" of an image.
    public String IsThawed
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isFrozen = ltr.IsFrozen;
                tr.Commit();
            }
              if (! _isFrozen)
                return "Visible";
              return "Collapsed";
        }
    }
      // Determine if the layer is locked
    // and return a string that can be bound to
    // the "Visibility" of an image.
    public String IsLocked
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isLocked = ltr.IsLocked;
                tr.Commit();
            }
              if (_isLocked)
                return "Visible";
              return "Collapsed";
        }
    }
      // Determine if the layer is unlocked
    // and return a string that can be bound to
    // the "Visibility" of an image.
    public String IsUnLocked
    {
        get
        {
            Document doc
                = Application.DocumentManager.MdiActiveDocument;
            Editor ed = doc.Editor;
            Database db = doc.Database;
            using (Transaction tr
                    = db.TransactionManager.StartTransaction())
            {
                LayerTable lt
                    = tr.GetObject( db.LayerTableId,
                                    OpenMode.ForRead
                                   ) as LayerTable;
                LayerTableRecord ltr
                    = tr.GetObject( lt[LayerName],
                                    OpenMode.ForRead
                                   ) as LayerTableRecord;
                _isLocked = ltr.IsLocked;
                tr.Commit();
            }
              if (! _isLocked)
                return "Visible";
              return "Collapsed";
        }
    }
      public AcadLayer(String layerName,
                     byte R, byte G, byte B,
                     bool isOn, bool isFrozen, bool isLocked)
    {
        LayerName = layerName;
        Red = R;
        Green = G;
        Blue = B;
          _isOn = isOn;
        _isFrozen = isFrozen;
        _isLocked = isLocked;
    }
      public AcadLayer()
    {
        LayerName = "0";
        Red = 255;
        Green = 255;
        Blue = 255;
          _isOn = true;
        _isFrozen = false;
        _isLocked = false;
    }
}
  // View Model for the Color Combo box to bind to
public class LayerViewModel : INotifyPropertyChanged
{
    // collection of layers that we will display
    AcadLayers _layers = new AcadLayers();
      public LayerViewModel()
    {
    }
      // Bound to the combo box source
    // that returns the collection of layers
    public AcadLayers MyAcadLayers
    {
        get
        {
            return _layers;
        }
    }
      // Default value to show
    private string _layerString = "0";
      // Bound to the current selection in the combo
    public string LayerString
    {
        get { return _layerString; }
        set
        {
            if (_layerString != value)
            {
                _layerString = value;
                NotifyPropertyChanged("LayerString");
            }
        }
    }
      #region INotifyPropertyChanged Members
      private void NotifyPropertyChanged(string propertyName)
    {
        if (PropertyChanged != null)
        {
            PropertyChanged(this,
                    new PropertyChangedEventArgs(propertyName));
        }
    }
      public event PropertyChangedEventHandler PropertyChanged;
      #endregion
}
3) Layout of the controls in Xaml :
<ComboBox   DataContext="{Binding ColorDataContext}"
            Name="MyColorCombo"
            Margin="2" Height="30" Width="250"
            ItemsSource="{Binding MyAcadColors}"
            SelectedValuePath="Name"
            SelectedValue="{Binding ColorString}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Margin="2">
                <Label  Visibility="{Binding IsVisible}"
                        Background="{Binding ColorBrush}"
                        Width="15" Height="15"
                        BorderBrush="Black" BorderThickness="1"/>
                <TextBlock  Visibility="{Binding IsVisible}"
                            Text=" " Width="3"/>
                <TextBlock Text="{Binding Name}" Width="100"/>
            </StackPanel>
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
  <ComboBox   Name="MyLayerCombo"
            DataContext="{Binding LayerDataContext}"
            Margin="2" Height="30" Width="250"
            ItemsSource="{Binding MyAcadLayers}"
            SelectedValuePath="Name"
            SelectedValue="{Binding LayerString}">
    <ComboBox.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal" Margin="2">
                <Image  Tag="{Binding LayerName}" 
                        Visibility="{Binding IsOn}"
                        Source="{StaticResource LayerOnImage}"/>
                <Image  Tag="{Binding LayerName}"
                        Visibility="{Binding IsOff}"
                        Source="{StaticResource LayerOffImage}"/>
                <Image  Tag="{Binding LayerName}"
                        Visibility="{Binding IsFrozen}"
                        Source="{StaticResource LayerFreezeImage}"/>
                <Image  Tag="{Binding LayerName}"
                        Visibility="{Binding IsThawed}"
                        Source="{StaticResource LayerThawImage}"/>
                <Image  Tag="{Binding LayerName}"
                        Visibility="{Binding IsLocked}"
                        Source="{StaticResource LayerLockImage}"/>
                <Image  Tag="{Binding LayerName}"
                        Visibility="{Binding IsUnLocked}"
                        Source="{StaticResource LayerUnlockImage}"/>
                <Label  Visibility="{Binding IsVisible}"
                        Background="{Binding LayerColorBrush}"
                        Width="15" Height="15"
                        BorderBrush="Black"
                        BorderThickness="1"/>
                <TextBlock  Visibility="{Binding IsVisible}"
                            Text=" " Width="3"/>
                <TextBlock  Text="{Binding LayerName}"
                            Width="100"/>
            </StackPanel>
        </DataTemplate>
    </ComboBox.ItemTemplate>
</ComboBox>
To try the attached project, build the sample project, netload the dll and run the "Test" command. This command should display a palette with the color and layer controls. The controls display the information based on the active document and if you wish to reload this information, click on the reload button.
Here is the screenshot of the output.
            Download SampleProject

## 评论

**内容**: JoSko said...
How would you add this control to ribbon?
Not in a palette but as a ribbonCombo or something like that?
Reply
11/09/2019 at 09:20 AM

---
