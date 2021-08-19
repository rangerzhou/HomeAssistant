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
  - platform: notify_wechat_qy
    name: wework_hahapush # 用于生成服务实体 ID, 比如这个就是 notify.wework_hahapush
    corpid: !secret notify_wework_HahaLife_corpid # 这个是企业微信的企业 id
    agentId: !secret notify_wework_HahaLife_HahaPush_agentId # 这个是企业微信里面新建应用的应用 id
    secret: !secret notify_wework_HahaLife_HahaPush_secret # 这个是企业微信里面新建应用的应用 secret
    touser: '@all' # 这里是发送个企业应用里面的全部人,当然也可以设置指定的人的 id,具体再企业微信里面设置
```

### 调用服务

``` yaml
- service: notify.wework_hahalife
  data:
    title: "标题"
    message: "类型|内容1|内容2|内容3"   

```

类型可以是 **text, news, textcard, video, image**
- text：只需要内容 1  
- news：需要内容 1 和内容 2 和内容 3，其中内容 1 为显示的文字，内容 2 为点开的连接，内容 3 为推送图片的连接
- textcard： 需要内容 1 和内容 2 其中内容 1 为显示的文字，内容 2 为点开的连接
- image：例如：image|内容|/home/ranger/Pictures/dog.jpeg
- video ：需要内容 1 和内容 2 其中内容 1 为显示的文字，内容 2 为 MP4 文件的路径  比如 {"title":"HomeAssistant","message":"video|内容|/home/pi/.homeassistant/test.mp4"}



### References:

https://bbs.hassbian.com/thread-7128-1-1.html

https://bbs.hassbian.com/thread-7585-1-1.html