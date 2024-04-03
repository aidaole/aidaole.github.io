# 使用VScode打造markdown编辑器

这篇主要介绍怎么用VSCode来写markdown文档，我的主要需求就是用
1. 能本地预览
2. 提供方便的copy图片，自动填图片地址（不需要图床）
3. 有一定的提示，快捷操纵

## 插件一：Markdown Preview Github Styling

因为我主要是通过GitPage来发布内容，所以这里预览也选择的是Gtihub的格式，安装之后点预览即可看效果，非常方便

## 插件二：Paste Image

这个插件主要实现的功能是，将我内存中的图片，粘贴到文档中，并且自动填好相对路径

比如我使用的截图软件`snipate`选择截图之后，可以到vscode中直接 `ctrl+shift+V` 将图片插入进来，非常方便。 当然也需要一些设置

设置自动填入的相对路径：

![](images/vscode_markdown/2024-04-03-18-48-43.png ':size=300')

这里配置意思是， 在当前目录创建  `images/当前markdown文件名/` 为前缀的目录，并且将图片放进去

## 插件三：learn-Markdown

用惯了 `typra` 的同学，肯定对里面的快捷键年年不忘，安装此插件之后，再配置快捷键，可实现类似 `typra` 的功能

```json
{
    "key": "ctrl+b",
    "command": "formatBold",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
  },
  {
    "key": "ctrl+i",
    "command": "formatItalic",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
  },
  {
    "key": "ctrl+shift+`",
    "command": "formatCode",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
  },
  {
    "key": "ctrl+t",
    "command": "insertTable",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
  },
  {
    "key": "ctrl+shift+[",
    "command": "insertNumberedList",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
  },
  {
    "key": "ctrl+shift+]",
    "command": "insertBulletedList",
    "when": "editorTextFocus && !vim.active && editorLangId == 'markdown'"
}
```

vscode 还支持部分代码补全功能，在设置中添加

```json
    "[markdown]": {
        // 快速补全
        "editor.quickSuggestions": {
          "other": true,
          "comments": true,
          "strings": true
        },
        // 显示空格
        "editor.renderWhitespace": "all",
        "editor.snippetSuggestions": "top",
        "editor.tabCompletion": "on",
        // 使用enter 接受提示
        // "editor.acceptSuggestionOnEnter": "on",
    },
```
