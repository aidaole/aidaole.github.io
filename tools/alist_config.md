# Alist 配置阿里云网盘

## 1. 下载alist文件

[https://github.com/alist-org/alist/releases](https://github.com/alist-org/alist/releases)

根据自己电脑类型下载文件, 我的windows 11 64位, 下载 `alist-windows-amd64.zip` 

下载解压, 里面就一个 `alist.exe` 文件

## 2. 首次登录

先重置admin账户密码:

`.\alist.exe admin set 你的密码`

然后启动alist服务

`.\alist.exe server`

获得服务器名称, 默认为 [http://127.0.0.1:5244](http://127.0.0.1:5244), 使用 `admin + 你的密码` 登录即可

## 3. 配置挂载阿里云盘

`设置->存储->添加->阿里云盘Open`

配置项目:

- 驱动: 阿里云盘Open
- 挂在: /阿里云盘Open
- 云盘类型: 资源库/备份盘
- 刷新令牌: [参考](https://alist.nn.ci/zh/guide/drivers/aliyundrive_open.html)
- 秒传: 看你自己勾不勾

然后**保存**即可

回到首页可以看到自己的阿里云盘挂在成功

![](images/alist_config/2024-04-24-00-15-49.png':size=300')

## 4. 添加脚本

每次启动都要在命令行中启动就比较麻烦, 可以在系统中添加默认启动服务

创建 `start_alist.vbs` 文件, 内容如下

```
Set ws = CreateObject("Wscript.Shell")  
ws.run ".\alist.exe server",vbhide
```

然后 `win+R` 输入 `shell:startup` 打开自启动文件夹

将`start_alist.vbs`文件的快捷方式放进去即可

这里也提供关闭alist服务`stop_alist.vbs` 脚本

```
Dim Wsh
Set Wsh = WScript.CreateObject("WScript.Shell")
Wsh.Run "taskkill /f /im alist.exe",0
Set Wsh=NoThing
WScript.quit
```