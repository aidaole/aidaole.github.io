# JitPack 发布的坑

这里记录一下在github上项目, 从 JitPack 产物遇到的一些坑

# JDK版本

JitPack默认还是使用的 java 1.8 版本进行编译, 所以如果你的项目比较新, 使用 gradle wrapper 比较高, JitPack在编译时就会报错

解决方法:

在项目根目录下添加: `jitpack.yml` 文件, 添加需要的jdk版本. 可以指定jdk版本: openjdk17, openjdk11 等

```
jdk:
  - openjdk17
```

# 多项目结构, 发布子项目

比如说我的项目中有一个 app, 一个lib1. 我要发布的内容是 lib1 的产物, app只是我用来验证代码的

这个时候需要告诉 JitPack 你的产物的位置, 以及要发布的产物的坐标, 在lib1的build.gradle中添加配置:

```
plugins {
    // ...
    id 'maven-publish'
}

afterEvaluate {
    publishing {
        publications {
            release(MavenPublication) {
                from components.release
                groupId = 'com.github.aidaole' // com.github.[username]
                artifactId = 'lib1' // lib的名字
                version = 'undefined' // version不重要,会根据tag生成
            }
        }
    }
}
```

# 发布

其他的就按照 JitPack 官网的指导文档, 到github上创建一个tag, 并且在 Jitpack 上发布即可, 如果顺利就可以看到 `com.github.aidaole:lib1:xxx` 这样一个依赖, 就是你的产物地址, 可以愉快的玩耍了


# 其他

app中最好是不要应用具体的插件版本, 英文jitpack编译的时候大概率会报错

创建tag的时候, 可以从本地push tag到远端, 但是最后还是要自己创建Release版本. 所以还不如直接在github中直接创建Release自带tag