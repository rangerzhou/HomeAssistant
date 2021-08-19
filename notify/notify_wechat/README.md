

Server 酱介绍：http://sc.ftqq.com/3.version

### 使用方法

- 申请 sckey：http://sc.ftqq.com/?c=code

- 绑定微信：http://sc.ftqq.com/?c=wechat&a=bind

- 下载 `__init__.py` 和 `notify.py` ，放入 `homeassistant/custom_components/notify_wechat` 目录下

- 配置 configurations.yaml

  ``` yaml
  notify:
    - platform: notify_wechat
      name: weixin
      sc_key: !secret notify_serverchan_sc_key
  ```

### HA 使用

调用服务 notify.weixin

``` shell
{"title":"Homeassistant","message":"来自HA的测试"}
```



此文使用组件参考：

[解决Server酱微信推送功能](https://bbs.hassbian.com/forum.php?mod=viewthread&tid=3936&extra=&highlight=server%2B%E9%85%B1&page=1)



其他参考：

[Pushbear【微信推送消息】【推送图片】【www文件夹的用处】](https://bbs.hassbian.com/thread-2766-1-1.html)

[使用PushBear一对多的微信推送](https://bbs.hassbian.com/thread-1650-1-1.html)

[通过serverchan推送微信消息的简陋插件](https://bbs.hassbian.com/thread-1099-1-1.html)

