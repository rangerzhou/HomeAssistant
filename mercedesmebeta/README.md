## HomeAssistant mercedesme 组件集成

### 1. 下载 `device_tracker.py`, ` __init__.py`, `sensor.py` 到 *homeassistant/custom_components/mercedesmebeta* 下；

### 2. 配置 configuration.yaml

``` yaml
mercedesmebeta:
  client_id: !secret mercedesmebeta_client_id
  client_secret: !secret mercedesmebeta_client_secret
  cache_path: ~/homeassistant
```



重启 HA，之后会在 *~/homeassistant/deps/lib/python3.7/site-packages/* 下生成一个 *mercedesmejsonpy* 目录，也可以在通过命令 `sudo pip install mercedesmejsonpy` （https://pypi.org/project/mercedesmejsonpy/）安装。

HA 启动后会弹出通知提示设置，点击设置若出现 Faulty query：
``` Error
Reason: invalid_redirect_uri
Description: Mismatching redirect_uri.

API-0000016c19aa1fe0-1069bd7c
```
则尝试在 https://developer.mercedes-benz.com/console 中 Regenerate key，
并在 Configuration.yaml 中配置 http：
```
http:
  base_url: 'http://raspberrypi.local:8123'
```

注意树莓派时间是否正确，如果不正确可能会报错，修改时间：`sudo date -s "2019-12-16 14:40:50"`

Simulator：https://car-simulator.developer.mercedes-benz.com/

CONSOLE：https://developer.mercedes-benz.com/console

API 文档：https://developer.mercedes-benz.com/apis/connected_vehicle_experimental_api/docs

