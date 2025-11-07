---
title: 给PDF添加文字和图片
date: 2025-11-07
categories:
  - windows程序
tags:
  - IMAGE
  - PDF
description: 使用Python给PDF添加文字和图片
author: JerryMa

---

# Python给PDF添加文字和图片

## **依赖库**需要安装三个库：

```bash
pip install pdf2image pillow img2pdf
```

- `pdf2image`：将 PDF 转换为图片（依赖 poppler，Windows 需下载 [poppler-utils](https://blog.alivate.com.au/poppler-windows/) 并添加到环境变量）
- `pillow`：处理图像和绘制文字
- `img2pdf`：将图片重新合并为 PDF

## **关键优势**

- 不依赖 `PyPDF4` 或 `PyPDF2` 的 `add_image` 方法，彻底解决属性缺失问题
- 支持所有系统和 PDF 版本，兼容性极强
- 可以精确控制图章位置和样式

## **注意事项**

- Windows 系统需安装 [poppler](https://blog.alivate.com.au/poppler-windows/) 并配置环境变量（否则 `pdf2image` 会报错）
- 处理大 PDF 时可能占用较多内存（可通过调整分辨率 `300` 降低内存使用）
- 确保图片图章路径正确，文字图章的字体在系统中存在

如果需要在 Linux 或 macOS 上使用，安装 poppler 的命令分别为：

- Ubuntu/Debian：`sudo apt-get install poppler-utils`
- macOS：`brew install poppler`

## 具体的代码

```python
// collapsed
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import img2pdf
import os
import tempfile

def add_stamp_to_pdf(input_pdf, output_pdf, stamp_content, is_image=False, stamp_size=(100, 100)):
    """
    给PDF的左下角添加图章（文字或图片），兼容所有版本
    """
    # 创建临时目录存放中间图片
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. 将PDF每页转换为图片（分辨率300dpi确保清晰）
        pages = convert_from_path(input_pdf, 300)
        processed_pages = []
        
        for page in pages:
            # 2. 准备图章（文字或图片）
            if is_image:
                # 处理图片图章
                with Image.open(stamp_content) as stamp_img:
                    stamp_img = stamp_img.resize(stamp_size, Image.Resampling.LANCZOS)
            else:
                # 处理文字图章
                stamp_img = Image.new('RGBA', stamp_size, (255, 255, 255, 0))  # 透明背景
                draw = ImageDraw.Draw(stamp_img)
                
                # 加载字体（使用系统字体路径）
                try:
                    # 尝试加载Windows系统黑体
                    font = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', 20)
                except:
                    # 尝试加载Linux/macOS系统字体
                    try:
                        font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 20)
                    except:
                        font = ImageFont.load_default()
                
                # 计算文字位置（居中）
                bbox = draw.textbbox((0, 0), stamp_content, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = (stamp_size[0] - text_width) // 2
                text_y = (stamp_size[1] - text_height) // 2
                
                # 绘制文字（红色半透明）
                draw.text((text_x, text_y), stamp_content, font=font, fill=(255, 0, 0, 128))
            
            # 3. 计算图章位置（左下角偏移10px）
            page_width, page_height = page.size
            stamp_x = 10
            stamp_y = page_height - stamp_size[1] - 10  # 左下角（注意图片坐标系y轴向下）
            
            # 4. 将图章粘贴到页面上
            page.paste(stamp_img, (stamp_x, stamp_y), stamp_img)  # 最后一个参数保留透明度
            
            # 5. 保存处理后的页面到临时目录
            temp_path = os.path.join(temp_dir, f"page_{len(processed_pages)}.png")
            page.save(temp_path, 'PNG')
            processed_pages.append(temp_path)
        
        # 6. 将所有处理后的图片重新合并为PDF
        with open(output_pdf, 'wb') as f:
            f.write(img2pdf.convert(processed_pages))

# 示例用法
if __name__ == "__main__":
    # 添加文字图章
    add_stamp_to_pdf(
        input_pdf="input.pdf",
        output_pdf="output_text_stamp.pdf",
        stamp_content="内部文件",
        is_image=False,
        stamp_size=(150, 60)
    )
    
    # 添加图片图章
    add_stamp_to_pdf(
        input_pdf="input.pdf",
        output_pdf="output_image_stamp.pdf",
        stamp_content="stamp.png",  # 图片路径
        is_image=True,
        stamp_size=(120, 120)
    )
```

