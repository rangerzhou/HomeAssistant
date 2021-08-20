### 接入

[**按照官网教程接入**](https://wxpusher.zjiecode.com/docs/#/?id=%e5%bf%ab%e9%80%9f%e6%8e%a5%e5%85%a5)，获取应用 Token 和 用户 UID，用于下方配置。

### 配置

configuration.yaml 配置

``` yaml
notify:
  - platform: wxpusher
    name: wechat_wxpusher
    uids: !secret WxPusher_UID_HahaPush
    apptoken: !secret WxPusher_APP_TOKEN_HahaPush
```



### 调用

``` yaml
service: notify.wechat_wxpusher
data:
  message: I am message
  title: I am title
# 或者
service: notify.wechat_wxpusher
data: {"message":"I am message","title":"I am title"}
```

### shell_command 方式使用 wxpusher

还有另外一种使用方法，因为发送消息其实就是通过 GET 或者 POST 命令进行 [HTTP 调用](https://wxpusher.zjiecode.com/docs/#/?id=http%e8%b0%83%e7%94%a8)，官网中有发送消息的接口，所以可以通过 HA 的 [shell_command](https://www.home-assistant.io/integrations/shell_command) 调用 curl 来发送消息。

#### POST 接口

此接口 type  2 和 type  3 未测试成功，POST 接口是功能完整的接口，推荐使用

``` json
{
  "appToken":"AT_xxx",
  "content":"Wxpusher祝你中秋节快乐!",
  "summary":"消息摘要",//消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度100，可以不传，不传默认截取content前面的内容。
  "contentType":1,//内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown 
  "topicIds":[ //发送目标的topicId，是一个数组！！！，也就是群发，使用uids单发的时候， 可以不传。
      123
  ],
  "uids":[//发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
      "UID_xxxx"
  ],
  "url":"http://wxpusher.zjiecode.com" //原文链接，可选参数
}
```

写成 curl 命令，可以在终端中执行测试是否能成功

``` shell
$ curl -X POST -H "Content-Type: application/json" -d '{"appToken":"你的 TOKEN", "content":"需要发送的内容","contentType":1,"uids":["接收对象的 uid"],"url":"http://wxpusher.zjiecode.com"}' http://wxpusher.zjiecode.com/api/send/message
```

**在 configuration.yaml 中配置，需要替换 your_token 和 your_uid**

``` yaml
shell_command:
  notify_wechat_post: curl -X POST -H "Content-Type:application/json" -d '{"appToken":"your_token", "content":"{{msg}}","contentType":{{type}},"uids":["your_uid"],"url":"http://wxpusher.zjiecode.com"}' http://wxpusher.zjiecode.com/api/send/message
```

**注意：Content-Type 冒号后面不要加空格，在终端中有空格执行没问题，但是在 yaml 配置有空格的话会报错。**

**调用**

``` yaml
# type 为 2 或者 3 没有测试成功
service: shell_command.notify_wechat_post
data:
  msg: who am i
  type: 1

```



#### GET接口

此接口 message 不能有空格，GET 接口是对 POST 接口的阉割，主要是为了某些情况下调用方便，只支持对文字（contentType = 1）的发送，举例：

``` yaml
$ curl -G "http://wxpusher.zjiecode.com/api/send/message/?appToken=your_token&content=your_message&uid=your_uid&url=http%3a%2f%2fwxpusher.zjiecode.com"
# 或者
curl "http://wxpusher.zjiecode.com/api/send/message/?appToken=your_token&content=your_message&uid=your_uid&url=http%3a%2f%2fwxpusher.zjiecode.com"
```



**在  configuration.yaml 中配置，需要替换 your_token 和 your_uid**

``` yaml
# 替换 your_token 和 your_uid 为你的 token 和 uid
shell_command:
  notify_wechat_get: curl -G "http://wxpusher.zjiecode.com/api/send/message/?appToken=your_token&content={{msg}}&uid=your_uid&url=http%3a%2f%2fwxpusher.zjiecode.com"
```

**调用**

``` yaml
service: shell_command.notify_wechat_get
data:
  msg: IamMessage
# 或者
service: shell_command.notify_wechat_get
data: {"msg":"1234567"}

# 经测试传入的消息中不能有空格  
```





官网：https://wxpusher.zjiecode.com
