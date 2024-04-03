# AndroidMultiLan

android中我们适配多语言是在 `values-xxx` 目录中创建对应语言的 `string.xml`

大公司有自己成熟的多语言适配工具，但是对于小公司可能没有资源来建立一套完整的多语言系统。

下文中提供了一个简洁的多语言适配工具，其功能包括:

1. 将我们项目中的 `string.xml` 整合到一个 `excel` 表格中（此时可以拿表格去给翻译公司翻译）
2. 将 `excel` 文件导出对应国家语言的 `string.xml`

工具的优势:

1. 要适配一个完整国家语言时, 可以非常快捷的知道哪些 `key` 需要翻译, 一键导出列表
2. 翻译完成之后, 不需要手动一个一个根据 `key` 替换到对应的 `string.xml` 中, 避免出错

## 

项目地址: [https://github.com/aidaole/AndroidMultiLan](https://github.com/aidaole/AndroidMultiLan)

## 使用说明

脚本功能主要分为2个部分:

1. `strings.xml` 导出excel: **export_excel.py**
2. excel 导出对应国家语言列表 `strings.xml`: **import_strings.py**