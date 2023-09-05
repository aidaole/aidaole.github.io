# ASM实战注入框架

这篇文章主要介绍通过 `gradle transform` 流程，扫描注解和接口实现类，将实现类和接口自动注入，使得模块间不通过 `module` 依赖实现访问其他模块接口的能力。主要解决组件化项目中，同级模块不能依赖但是想相互调用的问题，避免循环依赖。

也是记录怎么使用 `transform` 和发布插件的完整流程，主要内容如下：

1. 怎么定义注解，在 `transform` 过程中扫描注解，并记录
2. 根据注解内容，通过 `ASM` 插入注册代码
3. 发布插件并使用

## 1. 介绍项目结构

```
app
  |
  +-modules         // 业务层
  |   |
  |   +- module1    // 业务模块1
  |   |
  |   +- module2    // 业务模块2
  |
  +-base
      |
      +-injectservice_plugin  // 插件实现
      |
      +-injectservice_runtime // 插件runtime
```
主要功能就是 `module1` 不通过依赖 `module2` 来实现访问 `mdoule2` 的接口实现


