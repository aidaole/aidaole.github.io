# 使用VScode打造markdown编辑器

这篇主要介绍怎么用VSCode来写markdown文档，我的主要需求就是用
1. 能本地预览
2. 提供方便的copy图片，自动填图片地址（不需要图床）

## 插件一：Markdown Preview Github Styling

因为我主要是通过GitPage来发布内容，所以这里预览也选择的是Gtihub的格式，安装之后点预览即可看效果，非常方便

## 插件二：Paste Image

这个插件主要实现的功能是，将我内存中的图片，粘贴到文档中，并且自动填好相对路径

比如我使用的截图软件`snipate`选择截图之后，可以到vscode中直接 `ctrl+shift+V` 将图片插入进来，非常方便。 当然也需要一些设置

设置自动填入的相对路径：

![](images/vscode_markdown/2024-04-03-18-48-43.png ':size=300')

这里我的意思是， 在当前目录创建  `images/当前markdown文件名/` 为前缀的目录，并且将图片放进去
