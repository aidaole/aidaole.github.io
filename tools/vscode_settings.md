# vscode 常用配置

```json
{
  "workbench.colorTheme": "Default Dark Modern",
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
  "git.enableSmartCommit": true,
  "git.confirmSync": false,
  "editor.fontSize": 16,
  "dart.flutterSdkPath": "D:\\Greenwares\\flutter",
  "explorer.fileNesting.enabled": true,
  "explorer.fileNesting.patterns": {
    "pubspec.yaml": ".packages, pubspec.lock, .flutter-plugins, .flutter-plugins-dependencies, .metadata, analysis_options.yaml, dartdoc_options.yaml"
  },
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": "explicit"
  },
  "window.openFilesInNewWindow": "on",
  "window.openFoldersInNewWindow": "on",
  "window.zoomLevel": 1
}
```