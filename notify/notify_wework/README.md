### 注册企业微信

- 1.点击这里注册：https://work.weixin.qq.com/wework_admin/register_wx?from=myhome 1 分钟时间注册下就行，比较简单。
- 2.注册完成后打开：https://work.weixin.qq.com/wework_admin/frame#profile 复制下网页底部的企业信息中的企业 ID 备用。
- 3.点击微工作台 https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin 看到一个二维码,使用微信扫码关注,这样就可以使企业微信中收到的信息同步到微信上。

### 创建一个应用

- 1.点击这里创建 https://work.weixin.qq.com/wework_admin/frame#apps/createApiApp
  上传一个应用 logo 和自定义应用名字，其他默认。
- 2.创建后打开：https://work.weixin.qq.com/wework_admin/frame#apps 可以看到在 "应用"中的"自建"里有个应用。点进去打开 记录下 AgentId 和 Secret 备用。

### 下载组件放入 custom_components 下

### 配置 configurations.yaml

``` yaml
notify:
  - platform: notify_wework
    name: wework_hahapush
    corpid: !secret notify_wework_HAHALife_corpid # 这个是企业微信的企业 id
    agentId: !secret notify_wework_HAHALife_HahaPush_agentId # 这个是企业微信里面新建应用的应用 id
    secret: !secret notify_wework_HAHALife_HahaPush_secret # 这个是企业微信里面新建应用的应用 secret
    touser: '@all' # 这里是发送个企业应用里面的全部人,当然也可以设置指定的人的 id,具体再企业微信里面设置
```

### 调用服务

``` yaml
service: notify.wework_hahapush
data:
  message: 发送纯文本消息

service: notify.wework_hahapush
data:
  message: 发送带标题和分隔线的纯文本消息
  title: 这是标题

service: notify.wework_hahapush
data:
  message: ' '
  title: 发送带标题的链接卡片
  data:
    type: news
    url: 'http://rangerzhou.top'
    
service: notify.wework_hahapush
data:
  message: 发送带标题和内容的链接卡片
  title: 这是标题
  data:
    type: textcard
    url: 'http://rangerzhou.top'
    
service: notify.wework_hahapush
data:
  message: 发送带标题、内容和头图的链接卡片
  title: 这是标题
  data:
    type: news
    url: 'http://rangerzhou.top'
    picurl: 'https://bbs.hassbian.com/static/image/common/logo.png'

```



此插件和 notify_wechat_qy 区别是 service 调用的参数不同，notify_wechat_qy 把 type, url 等都写在了 message 中，此插件是分开来写。

### References:

https://bbs.hassbian.com/thread-12547-1-1.html



