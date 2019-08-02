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



Simulator：https://car-simulator.developer.mercedes-benz.com/

CONSOLE：https://developer.mercedes-benz.com/console

API 文档：https://developer.mercedes-benz.com/apis/connected_vehicle_experimental_api/docs

