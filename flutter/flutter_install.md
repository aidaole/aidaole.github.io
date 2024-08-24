# 国内环境安装flutter

参考文档 [https://flutter.cn/community/china](https://flutter.cn/community/china)

1. 首先官网下载最新版本的flutter sdk，解压到自己的目录，并将 `flutter home/bin` 配置到环境变量中。但是不要走默认的 [https://storage.googleapis.com](https://storage.googleapis.com) 去下载， 要使用国内的镜像下载地址 [https://flutter.cn/docs/release/archive?tab=windows](https://flutter.cn/docs/release/archive?tab=windows)，否则后期可能依赖拉不下来
2. Android环境下，打开Android Studio的 sdkmanager， 安装 sdk tools->command line tools，并将 `android sdk home\cmdline-tools\latest` 配置到环境变量中
3. 打开命令行，运行 `flutter doctor` 发现有错误
```bash
PS D:\> flutter doctor
Doctor summary (to see all details, run flutter doctor -v):
[✓] Flutter (Channel stable, 3.19.5, on Microsoft Windows [版本 10.0.22631.3296], locale zh-CN)
[✓] Windows Version (Installed version of Windows is version 10 or higher)
[!] Android toolchain - develop for Android devices (Android SDK version 34.0.0)
    ! Some Android licenses not accepted. To resolve this, run: flutter doctor --android-licenses
[✓] Chrome - develop for the web
[✗] Visual Studio - develop Windows apps
    ✗ Visual Studio not installed; this is necessary to develop Windows apps.
      Download at https://visualstudio.microsoft.com/downloads/.
      Please install the "Desktop development with C++" workload, including all of its default components
[✓] Android Studio (version 2023.2)
[✓] Connected device (3 available)
[!] Network resources
    ✗ A cryptographic error occurred while checking "https://storage.googleapis.com/": Connection terminated during
      handshake
      You may be experiencing a man-in-the-middle attack, your network may be compromised, or you may have malware
      installed on your computer.
    ✗ A network error occurred while checking "https://maven.google.com/": 信号灯超时时间已到
```
需要配置一下国内的flutter 网络环境, 主要是执行。最好是自己在环境变量中手动添加，下面命令只能当此生效
```shell
$env:PUB_HOSTED_URL="https://pub.flutter-io.cn"
$env:FLUTTER_STORAGE_BASE_URL="https://storage.flutter-io.cn"
```
4. 执行完之后， 发现网络环境已经OK了，下一步同意开发者协议 `flutter doctor --android-licenses`
5. OK 最后一个错误是 `visualstudio` 没有安装， 这个不用管，要开发windows应用才需要安装
6. 这个时候创建flutter项目，然后运行，可能遇到下面的错误，是因为下载不到对应的gradle wrapper版本。可以手动下载对应的版本之后，放到 `./gradle/wrapper/xxx` 版本中即可
```bash
Exception in thread "main" java.net.ConnectException: Connection timed out: connect
	at java.base/sun.nio.ch.Net.connect0(Native Method)
	at java.base/sun.nio.ch.Net.connect(Net.java:579)
	at java.base/sun.nio.ch.Net.connect(Net.java:568)
	at java.base/sun.nio.ch.NioSocketImpl.connect(NioSocketImpl.java:593)
  // ...
	at org.gradle.wrapper.Download.downloadInternal(Download.java:58)
```

