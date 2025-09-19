---
title: SVG2Image
date: 2024-08-28
categories:
  - Python
  - 图像处理
  - SVG
tags:
  - Python
  - SVG
  - 图像转换
  - cairosvg
description: SVG图像转换为其他格式图像的Python实现方法，使用cairosvg库
author: JerryMa
---

# SVG2Image

## 安装gmk+，[github] ([https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2Ftschoonj%2FGTK-for-Windows-Runtime-Environment-Installer))

## 安装需要的库

```bash
pip install cairosvg
```

https://www.gtk.org/docs/installations/windows/

https://github.com/wingtk/gvsbuild

### 安装[gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe)

### 安装python3.12

### 将`C:\Program Files\GTK3-Runtime Win64\bin`添加到PATH中

`svg2bmp`

```python
"""
SVG文件转换为BMP格式。
"""
from PIL import Image
import cairosvg
import os
from io import BytesIO
import sys


# 获取同一目录下的所有svg文件的绝对路径
def getFileName(filedir):
    """
    获取指定目录下所有以"dwg"为后缀的文件的绝对路径列表。

    参数:
    filedir: str - 文件目录的路径。

    返回:
    List[str] - 包含所有符合条件的文件的绝对路径的列表，如果没有找到任何文件，则返回空列表。
    """
    # 使用列表推导式和os.walk遍历指定目录及其子目录，查找所有以"svg"结尾的文件
    # os.path.join用于拼接文件的绝对路径
    file_list = [
        os.path.join(root, filespath)
        for root, dirs, files in os.walk(filedir)
        for filespath in files
        if str(filespath).endswith("svg")
    ]
    # 如果file_list不为空，则返回file_list，否则返回空列表
    return file_list if file_list else []


# 获取当前脚本目录
def get_current_file_path():
    # 通过命令行参数获取当前脚本的绝对路径
    abs_file = sys.argv[0]
    # 将路径中的斜杠替换为反斜杠，以适应Windows系统
    windows_path = abs_file.replace("/", "\\")
    # 去除路径中的脚本文件名，仅保留目录部分
    windows_path = windows_path[: windows_path.rfind("\\")]
    # 返回脚本所在的目录路径
    return windows_path


if __name__ == "__main__":
    currentPath = get_current_file_path()
    print(currentPath)
    file_list = getFileName(currentPath)
    print(file_list)
    for file in file_list:
        # 假设你有一个SVG文件名为'example.svg'
        png_file = file.replace(".svg", ".png")
        cairosvg.svg2png(url=file, write_to=png_file, output_width=64, output_height=64)

        # 打开 PNG 文件
        png_image = Image.open(png_file)

        bmp_file = file.replace(".svg", ".bmp")
        # 将 PNG 文件保存为 BMP
        png_image.save(bmp_file, 'BMP')

        # 使用svglib将SVG文件转换为报告实验室图形对象
        os.remove(png_file)
```



## svgToIcon

在Windows上，你需要安装ImageMagick和Wand库。以下是详细的安装步骤：

### 安装ImageMagick

1. **下载ImageMagick**：

   - 访问 [ImageMagick官方下载页面](https://imagemagick.org/script/download.php)。
   - 点击 "Binary releases" 下的 "Windows"。
   - 下载适用于你的Windows版本的预编译二进制包（例如，`ImageMagick-7.0.10-Q16-HDRI-x64-dll.exe`）。

2. **安装ImageMagick**：

   - 运行下载的安装程序。
   - 按照安装向导的指示完成安装。
   - 在安装过程中，确保选中 "Add application directory to your system path" 选项，这样ImageMagick的路径会被添加到系统环境变量中。

3. 安装Wand库

4. **安装Python环境**：

   - 如果你还没有安装Python，请从 [Python官方下载页面](https://www.python.org/downloads/) 下载并安装适用于Windows的Python版本。

5. **使用pip安装Wand**：

   - 打开命令提示符（CMD）。

   - 输入以下命令来安装Wand库：

     ```bash
     pip install Wand
     ```

   - 如果提示权限问题，请以管理员身份运行命令提示符，并重复上述命令。

## 完整代码

`svgtoimage.py`

```python
"""
SVG文件转换为BMP格式。
"""
from PIL import Image
import cairosvg
import os
from io import BytesIO
import sys
from wand.image import Image as wimg
from wand.color import Color
# 获取同一目录下的所有svg文件的绝对路径
def getFileName(filedir):
    """
    获取指定目录下所有以"dwg"为后缀的文件的绝对路径列表。

    参数:
    filedir: str - 文件目录的路径。

    返回:
    List[str] - 包含所有符合条件的文件的绝对路径的列表，如果没有找到任何文件，则返回空列表。
    """
    # 使用列表推导式和os.walk遍历指定目录及其子目录，查找所有以"svg"结尾的文件
    # os.path.join用于拼接文件的绝对路径
    file_list = [
        os.path.join(root, filespath)
        for root, dirs, files in os.walk(filedir)
        for filespath in files
        if str(filespath).endswith("svg")
    ]
    # 如果file_list不为空，则返回file_list，否则返回空列表
    return file_list if file_list else []


# 获取当前脚本目录
def get_current_file_path():
    # 通过命令行参数获取当前脚本的绝对路径
    abs_file = sys.argv[0]
    # 将路径中的斜杠替换为反斜杠，以适应Windows系统
    windows_path = abs_file.replace("/", "\\")
    # 去除路径中的脚本文件名，仅保留目录部分
    windows_path = windows_path[: windows_path.rfind("\\")]
    # 返回脚本所在的目录路径
    return windows_path

# svg转ico
def svgtoico(input_file):
    """
    将SVG文件转换为ICO格式。

    参数:
    svg_file: str - SVG文件的路径。

    返回:
    无返回值，直接生成同名的ICO文件。
    """
    # # 保存为ICO文件
    ico_file = input_file.replace(".svg", ".ico")
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]

    with wimg(filename=input_file, background=Color("transparent")) as img:
        img.background_color = Color('transparent')  # 设置背景颜色为透明
        img.alpha_channel = 'set'  # 确保图像有透明通道

        with wimg() as ico:
            for size in sizes:
                with img.clone() as icon:
                    icon.resize(size[0], size[1])
                    ico.sequence.append(icon)
            ico.save(filename=ico_file)
# ... existing imports ...
import json

def load_config():
    """
    加载配置文件，如果不存在则创建默认配置。

    返回:
    dict - 包含配置信息的字典
    """
    config_path = os.path.join(get_current_file_path(), 'config.json')
    default_config = {
        "image_size": {
            "width": 64,
            "height": 64
        },
        "image_type": {
            "type": "BMP"
        }
    }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 确保所有必需的配置项都存在
            if 'image_size' not in config:
                config['image_size'] = default_config['image_size']
            if 'width' not in config['image_size']:
                config['image_size']['width'] = default_config['image_size']['width']
            if 'height' not in config['image_size']:
                config['image_size']['height'] = default_config['image_size']['height']
            if 'image_type' not in config:
                config['image_type'] = default_config['image_type']
            if 'type' not in config['image_type']:
                config['image_type']['type'] = default_config['image_type']['type']
            return config
    except FileNotFoundError:
        # 如果配置文件不存在，创建默认配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def svgtoimage(svg_file, config=None):
    """
    将SVG文件转换为指定格式的图像文件。

    参数:
    svg_file: str - SVG文件的路径
    config: dict - 配置信息，包含图像尺寸等参数

    返回:
    str - 生成的图像文件路径
    """
    if config is None:
        config = load_config()
    
    size = (
        config['image_size']['width'],
        config['image_size']['height']
    )
    
    format = config['image_type']['type']
    # 生成输出文件路径
    output_file = svg_file.replace(".svg", f".{format.lower()}")
    
    # 如果是ICO格式，创建多个尺寸的图标
    if format.upper() == 'ICO':
        # 创建不同尺寸的图标
        png_data = cairosvg.svg2png(
        url=svg_file, 
        output_width=max(size[0], 256),  # 使用较大的尺寸以保持质量
        output_height=max(size[1], 256)
        )

        # 从字节流创建PIL Image对象
        img = Image.open(BytesIO(png_data))
        svgtoico(svg_file)
    else:
        # 其他格式直接保存
        png_data = cairosvg.svg2png(
        url=svg_file, 
        output_width=size[0],  # 使用较大的尺寸以保持质量
        output_height=size[1]
        )
    
        # 从字节流创建PIL Image对象
        img = Image.open(BytesIO(png_data))
        img.save(output_file, format=format)
    
    print(f"输出文件为: {output_file}")
    return output_file

if __name__ == "__main__":
    currentPath = get_current_file_path()
    print(currentPath)
    file_list = getFileName(currentPath)
    print(file_list)
    
    # 加载配置
    config = load_config()
    
    for file in file_list:
        # 使用配置信息进行转换
        svgtoimage(file, config=config)
```

`config.json`

```json
{
    "image_size": {
        "width": 16,
        "height": 16
    },
    "image_type": {
        "type": "ico"
    }
}
```

