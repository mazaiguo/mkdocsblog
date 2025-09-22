---
title: WPF里引用SVG图标
date: 2024-06-05
categories:
  - windows程序
tags:
  - WPF
  - SVG
  - SharpVectors
description: 在WPF应用程序中引用和显示SVG格式图标的多种实现方法
author: JerryMa
---



# WPF里引用svg图标

## 第一种方式

引入`xmlns:svgc="http://sharpvectors.codeplex.com/svgc/"`
https://elinamllc.github.io/SharpVectors/articles/index.html

下载`sharpvectors`

```csharp
<Image Source="{svgc:SvgImage Source=/Images/SVG/email 33.svg}" />
```



## 第二种方式

将Path路径提出来，设置key值，放置在资源里

```csharp
<Window.Resources>
    <!--Close Image-->
    <PathFigureCollection x:Key="ClosePathData">
        M482.048 0h64v533.333h-64V0z
        M695.381 132.864v54.187c128 69.845 225.494 208.618 225.494 368.469 0 230.08-184.939 416.64-415.019 416.64-230.123 0-406.016-186.56-406.016-416.64 0-159.85 83.541-298.624 232.875-368.47v-54.186C162.048 206.528 52.075 368 52.075 555.52c0 256.96 203.37 465.259 460.33 465.259 256.939 0 459.52-208.299 459.52-465.259 0-187.52-105.877-348.992-276.544-422.656z
    </PathFigureCollection>
    <DrawingImage x:Key="CloseImage">
        <DrawingImage.Drawing>
            <GeometryDrawing>
                <GeometryDrawing.Brush>
                    <SolidColorBrush  Color="#666D73"/>
                </GeometryDrawing.Brush>
                <GeometryDrawing.Geometry>
                    <PathGeometry FillRule="Nonzero"  Figures="{StaticResource ClosePathData}" />
                </GeometryDrawing.Geometry>
            </GeometryDrawing>
        </DrawingImage.Drawing>
    </DrawingImage>
</Window.Resources>
```

多条Path就放多个PathFigureCollection里，使用时，直接调用

```csharp
<Image Source="{StaticResource CloseImage}" />
```

显示图标

使用[SvgToXaml](https://github.com/BerndK/SvgToXaml)工具

`资源文件`

```csharp
 <!--  Close Image  -->
        <PathFigureCollection x:Key="ClosePathData">
            M482.048 0h64v533.333h-64V0z
            M695.381 132.864v54.187c128 69.845 225.494 208.618 225.494 368.469 0 230.08-184.939 416.64-415.019 416.64-230.123 0-406.016-186.56-406.016-416.64 0-159.85 83.541-298.624 232.875-368.47v-54.186C162.048 206.528 52.075 368 52.075 555.52c0 256.96 203.37 465.259 460.33 465.259 256.939 0 459.52-208.299 459.52-465.259 0-187.52-105.877-348.992-276.544-422.656z
        </PathFigureCollection>
        <DrawingImage x:Key="CloseImage">
            <DrawingImage.Drawing>
                <GeometryDrawing>
                    <GeometryDrawing.Brush>
                        <SolidColorBrush Color="Gray" />
                    </GeometryDrawing.Brush>
                    <GeometryDrawing.Geometry>
                        <PathGeometry Figures="{StaticResource ClosePathData}" FillRule="Nonzero" />
                    </GeometryDrawing.Geometry>
                </GeometryDrawing>
            </DrawingImage.Drawing>
        </DrawingImage>

        <!--BoxIcons_LogosBlenderGeometryKey-->
        <Geometry x:Key="BoxIcons_LogosBlenderGeometryKey">F1 M48,48z M0,0z M530.219,404.864C531.798,433.323 545.707,458.368 566.742,476.16 587.693,493.682 614.924,504.322 644.639,504.322 644.913,504.322 645.187,504.321 645.461,504.319L645.419,504.319C675.712,504.319 703.446,493.652 724.139,476.159 745.131,458.367 759.083,433.279 760.662,404.863 762.283,375.594 750.55,348.415 729.899,328.276 708.276,307.619 678.912,294.906 646.578,294.906 646.185,294.906 645.793,294.908 645.401,294.912L645.461,294.912C645.109,294.908 644.693,294.906 644.277,294.906 611.938,294.906 582.567,307.62 560.892,328.321L560.939,328.277C540.331,348.416,528.555,375.594,530.219,404.864z M346.624,347.264C346.837,336.171 350.421,314.539 355.712,297.6 367.982,259.513 387.391,226.735 412.548,199.316L412.373,199.509C439.559,169.668,472.554,145.638,509.633,129.121L511.487,128.383C549.32,111.262 593.517,101.286 640.045,101.286 640.599,101.286 641.153,101.287 641.706,101.29L641.62,101.29C641.736,101.29 641.874,101.29 642.012,101.29 688.999,101.29 733.619,111.424 773.807,129.625L771.796,128.81C810.672,146.268,843.623,170.392,870.613,200.04L870.826,200.277C895.749,227.577,915.125,260.406,926.878,296.668L927.402,298.538C932.668,314.564,936.452,333.214,938.012,352.493L938.069,353.365C938.518,359.018 938.773,365.605 938.773,372.251 938.773,422.081 924.397,468.553 899.566,507.747L900.18,506.709C882.233,535.122,860.325,559.175,834.892,578.899L834.26,579.37 834.303,579.413 566.996,784.768C549.46,798.165 520.02,798.123 500.82,784.683 481.321,771.072 479.145,748.587 496.383,734.336L496.34,734.293 607.529,643.797 268.116,643.413C240.127,643.413 213.204,624.981 207.871,601.77 202.41,578.09 221.439,558.463 250.58,558.378L250.537,558.25 422.356,558.591 114.516,322.346C85.6310000000001,300.202 76.2870000000001,263.381 94.4630000000001,240.042 112.98,216.319 152.234,216.319 181.503,239.957L348.842,376.874C348.885,376.874,346.453,358.399,346.623,347.263z M776.619,285.397C742.144,250.24 693.931,230.314 641.664,230.229 589.355,230.144 541.141,249.898 506.624,284.97 490.736,300.874 478.188,320.117 470.123,341.556L469.76,342.656C464.013,357.906 460.687,375.534 460.687,393.939 460.687,398.581 460.899,403.174 461.313,407.708L461.27,407.125C463.147,428.672 469.505,449.237 479.787,467.797 489.856,486.101 503.766,502.57 520.832,516.608 553.277,542.868 595.049,558.766 640.534,558.766 640.931,558.766 641.328,558.765 641.725,558.762L641.664,558.762C642.121,558.766 642.661,558.768 643.201,558.768 688.501,558.768 730.118,543.003 762.866,516.66L762.496,516.948C779.52,503.039 793.429,486.612 803.499,468.351 813.739,449.748 820.139,429.268 822.016,407.722 822.385,403.772 822.596,399.18 822.596,394.538 822.596,376.136 819.286,358.507 813.23,342.214L813.568,343.252C805.052,320.672,792.485,301.385,776.609,285.386L776.619,285.396z</Geometry>
        <DrawingGroup x:Key="BoxIcons_LogosBlenderDrawingGroupKey" ClipGeometry="M0,0 V48 H48 V0 H0 Z">
            <DrawingGroup Transform="0.0562308674397924,0,0,-0.0562308674397924,-4.78802069564223,49.1935494114674">
                <GeometryDrawing Brush="#FFD3D3D3" Geometry="{StaticResource BoxIcons_LogosBlenderGeometryKey}">
                    <GeometryDrawing.Pen>
                        <Pen
                            Brush="#FF000000"
                            EndLineCap="Flat"
                            LineJoin="Miter"
                            StartLineCap="Flat"
                            Thickness="1" />
                    </GeometryDrawing.Pen>
                </GeometryDrawing>
            </DrawingGroup>
        </DrawingGroup>
        <DrawingImage x:Key="BoxIcons_LogosBlenderDrawingImageKey" Drawing="{StaticResource BoxIcons_LogosBlenderDrawingGroupKey}" />
```

![image-20240907113623699](http://image.jerryma.xyz//images/20240907-image-20240907113623699.png)





```csharp
 <WrapPanel>
                <Image Margin="0,0,10,0" Source="{StaticResource BoxIcons_LogosBlenderDrawingImageKey}" />
                <Viewbox
                    Grid.Row="1"
                    Grid.Column="2"
                    Margin="0,0,10,0">
                    <Path
                        Data="M839.040 242.731c-13.009-30.022-27.582-55.778-44.492-79.769l0.93 1.39c-22.912-32.725-41.728-55.339-56.149-67.925-22.4-20.565-46.464-31.147-72.192-31.744-18.432 0-40.704 5.248-66.645 15.915-26.027 10.624-49.92 15.829-71.808 15.829-22.912 0-47.488-5.205-73.813-15.829-26.283-10.667-47.531-16.256-63.787-16.768-24.619-1.067-49.237 9.771-73.771 32.597-15.659 13.653-35.243 37.12-58.752 70.315-25.173 35.371-45.867 76.544-62.080 123.349-17.365 50.645-26.069 99.627-26.069 147.072 0 54.315 11.733 101.205 35.243 140.459 18.116 31.030 43.055 56.256 72.877 74.187l0.936 0.522c28.511 17.374 62.912 27.821 99.722 28.244l0.118 0.001c19.627 0 45.355-6.059 77.227-18.005s52.352-18.005 61.269-18.005c6.741 0 29.397 7.125 67.968 21.248 36.395 13.099 67.115 18.517 92.288 16.384 68.267-5.504 119.509-32.384 153.6-80.853-61.013-36.992-91.179-88.747-90.581-155.179 0.512-51.755 19.328-94.805 56.192-128.981 15.812-15.151 34.402-27.559 54.904-36.362l1.202-0.459c-4.523-13.099-9.301-25.6-14.336-37.632zM682.581 858.453c0-40.533-14.848-78.421-44.331-113.451-35.669-41.643-78.763-65.749-125.483-61.952-0.571 4.506-0.896 9.719-0.896 15.009 0 0.124 0 0.247 0.001 0.371v-0.019c0 38.955 16.896 80.597 47.061 114.688 15.019 17.237 34.133 31.616 57.301 43.051 23.125 11.264 44.971 17.493 65.536 18.56 0.555-5.461 0.811-10.88 0.811-16.256z"
                        Fill="Gray"
                        StrokeThickness="1" />
                </Viewbox>
                <Image Margin="0,0,10,0" Source="{StaticResource CloseImage}" />
                <Image Margin="0,0,10,0" Source="{svgc:SvgImage Source=/Images/SVG/email 33.svg}" />
            </WrapPanel>
```



在Button中使用

```csharp
 <local:ImageButton
            x:Name="btn_Image"
            Grid.Row="3"
            HorizontalContentAlignment="Center"
            VerticalContentAlignment="Center"
            Background="White"
            Content="播放"
            FontSize="16"
            Foreground="Gray"
            Icon="{StaticResource edit_13DrawingImage}"
            IconContentMargin="10,0,0,0"
            IconHeight="32"
            IconMouseOver="{StaticResource discount_21DrawingImage}"
            IconWidth="32"
            MouseDownForeground="Blue"
            MouseOverForeground="#FFFFFF"
            ToolTip="播放" />
        <local:ButtonEx
            Grid.Row="4"
            HorizontalAlignment="Center"
            VerticalAlignment="Center"
            ButtonType="IconText"
            Content="11122"
            Icon="{StaticResource discount_21DrawingImage}" />
```

