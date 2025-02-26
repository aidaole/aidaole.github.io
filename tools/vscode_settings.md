# vscode 常用配置

```json
{
    "window.commandCenter": 1,
    "workbench.activityBar.orientation": "vertical",
    "window.zoomLevel": -1,
    "[dart]": {
        "editor.formatOnSave": true,
        "editor.formatOnType": true,
        "editor.rulers": [
            80
        ],
        "editor.selectionHighlight": false,
        "editor.tabCompletion": "onlySnippets",
        "editor.wordBasedSuggestions": "off",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "always",
            "source.fixAll": "always"
        },
        "editor.guides.bracketPairs": true,
    },
    
    "editor.fontSize": 14,
    "git.enableSmartCommit": true,
    "git.confirmSync": false,
    "workbench.colorTheme": "Atom One Light",
    "pasteImage.path": "images/${currentFileNameWithoutExt}",
    "pasteImage.suffix": "':size=300'",
    "[markdown]": {
    // 快速补全
    "editor.quickSuggestions": {
      "other": true,
      "comments": true,
      "strings": true
    },
    // 显示空格
    "editor.renderWhitespace": "all",
    // snippet 提示优先（看个人喜欢）
    "editor.snippetSuggestions": "top",
    "editor.tabCompletion": "on",
    // 使用enter 接受提示
    // "editor.acceptSuggestionOnEnter": "on",
  },
}
```
