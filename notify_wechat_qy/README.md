

### 下载组件放入 custom_components 下

### 配置 configurations.yaml

``` yaml
  - platform: notify_wechat_qy
    name: weixin_qiye 			# 用于生成服务实体 ID, 比如这个出来就是 notify.weixin_qiye
    corpid: !secret notify_qiyewechat_corpid 	# 这个是企业微信的企业 id
    agentId: !secret notify_qiyewechat_agentId 	# 这个是企业微信里面新建应用的应用 id
    secret: !secret notify_qiyewechat_secret 	# 这个是企业微信里面新建应用的应用 secret
    touser: '@all' # 这里是发送个企业应用里面的全部人,当然也可以设置指定的人的 id,具体再企业微信里面设置
```

### 调用服务

``` yaml
- service: notify.weixin_qiye
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