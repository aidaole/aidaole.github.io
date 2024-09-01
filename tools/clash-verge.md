# clash-verge

新一代替代clash的工具, clash-verge更加简便使用, 设置项也更加简单, 这里放一些常用的设置

## 下载地址

[https://github.com/clash-verge-rev/clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev)

## 设置

### 内核设置

选择Meta内核,并重启内核

![](images/clash-verge/2024-09-01-16-07-28.png ':size=300')

### 导入订阅

导入订阅

![](images/clash-verge/2024-09-01-16-10-01.png ':size=300')

### 配置自定义规则

这里主要是配置一些指定域名或者网址走什么代理

比如: 

steam 在国内直接走直连速度就是最快的

chatgpt 和 claude需要代理, 但是香港又不能使用, 所以这里直接指向台湾

```yaml
prepend-rules: 
  - DOMAIN,steamcdn-a.akamaihd.net,🎯 全球直连
  - DOMAIN-SUFFIX,cm.steampowered.com,🎯 全球直连
  - DOMAIN-SUFFIX,steamserver.net,🎯 全球直连
  - DOMAIN-KEYWORD,chatgpt,🇹🇼 台湾
  - DOMAIN-KEYWORD,openai,🇹🇼 台湾
  - DOMAIN-SUFFIX,anthropic.com,🇹🇼 台湾
  - DOMAIN-SUFFIX,claude.ai,🇹🇼 台湾
  - IP-CIDR,45.121.184.0/24,🎯 全球直连
  - IP-CIDR,103.10.124.0/23,🎯 全球直连
  - IP-CIDR,103.28.54.0/24,🎯 全球直连
  - IP-CIDR,146.66.152.0/24,🎯 全球直连
  - IP-CIDR,146.66.155.0/24,🎯 全球直连
  - IP-CIDR,153.254.86.0/24,🎯 全球直连
  - IP-CIDR,155.133.224.0/22,🎯 全球直连
  - IP-CIDR,155.133.230.0/24,🎯 全球直连
  - IP-CIDR,155.133.232.0/23,🎯 全球直连
  - IP-CIDR,155.133.234.0/24,🎯 全球直连
  - IP-CIDR,155.133.236.0/22,🎯 全球直连
  - IP-CIDR,155.133.240.0/23,🎯 全球直连
  - IP-CIDR,155.133.244.0/23,🎯 全球直连
  - IP-CIDR,155.133.246.0/24,🎯 全球直连
  - IP-CIDR,155.133.248.0/21,🎯 全球直连
  - IP-CIDR,162.254.192.0/21,🎯 全球直连
  - IP-CIDR,185.25.182.0/23,🎯 全球直连
  - IP-CIDR,190.217.32.0/22,🎯 全球直连
  - IP-CIDR,192.69.96.0/22,🎯 全球直连
  - IP-CIDR,205.196.6.0/24,🎯 全球直连
  - IP-CIDR,208.64.200.0/22,🎯 全球直连
  - IP-CIDR,208.78.164.0/22,🎯 全球直连
  - IP-CIDR,205.185.194.0/24,🎯 全球直连
```

### 配置bypass

有些网址比如bugly, 和一些公司网址, 走代理是不能访问的, 这些就需要配置到 bypass里面直接忽略

找到: 设置->系统代理->设置bypass (注意: 多个域名以`;`隔开)

![](images/clash-verge/2024-09-01-16-16-39.png ':size=300')


## 总结

其他的就可以自己摸索了, clash-verge相对于clash其实简化了一些设置, 使用起来更加简单, 各平台都支持. 对于学计算机开发的同学, 有一个梯子学习最新的技术是更加方便的. 希望大家好好利用