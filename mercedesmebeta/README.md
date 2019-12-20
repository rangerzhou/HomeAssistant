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

注意树莓派时间是否正确，如果不正确可能会报错:
```
2019-12-19 11:59:27 ERROR (SyncWorker_11) [mercedesmejsonpy.controller] Connection failed with http code 401
NoneType: None
... ...
2019-12-19 11:59:31 ERROR (MainThread) [homeassistant.setup] Error during setup of component mercedesmebeta
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/dist-packages/homeassistant/setup.py", line 156, in _async_setup_component
    component.setup, hass, processed_config)  # type: ignore
  File "/usr/lib/python3.7/concurrent/futures/thread.py", line 57, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/home/pi/.homeassistant/custom_components/mercedesmebeta/__init__.py", line 165, in setup
    mercedesme_api = Controller(auth_handler, scan_interval)
  File "/home/pi/.homeassistant/deps/lib/python3.7/site-packages/mercedesmejsonpy/controller.py", line 156, in __init__
    self.load_cars()
  File "/home/pi/.homeassistant/deps/lib/python3.7/site-packages/mercedesmejsonpy/controller.py", line 183, in load_cars
    for current_car in cars:
TypeError: 'NoneType' object is not iterable

```
修改时间即可解决：`sudo date -s "2019-12-16 14:40:50"`

Simulator：https://car-simulator.developer.mercedes-benz.com/

CONSOLE：https://developer.mercedes-benz.com/console

API 文档：https://developer.mercedes-benz.com/apis/connected_vehicle_experimental_api/docs

