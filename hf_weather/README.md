使用方法：

下载组件放入对应目录，配置 configuration.yaml:

``` yaml
# 配置 configuration.yaml
weather:
  - platform: hf_weather
    name: test                  # entity_id，自定义
    city: {{YOUR_CITY_CODE}}    # 城市代码，api平台有查询接口查询
    appkey: {{YOUR_API_KEY}}    # api平台申请的key
```

启用 sun 组件：

``` yaml
# 配置 configuration.yaml
sun:
```

lovelace 启用天气卡片（首页右上角“配置 UI - 原始配置编辑器”）：

``` yaml
# 配置lovelace（使用UI的原始编辑器编辑即可）
# 引入自定义卡片hf_weather-card
resources:
  - type: module
    url: /local/custom-lovelace/hf_weather-card/hf_weather-card.js
  - type: module
    url: /local/custom-lovelace/hf_weather-card/hf_weather-more-info.js
# 在view里面的cards节点，增加天气卡片类型
views:
    path: default_view
    title: Home
    cards:
      - type: 'custom:hf_weather-card'                                # card类型
        entity: weather.test                                         # entityid
        mode: daily                                                   # hourly按小时天气预报、daily按天天气预报，不设置则同时显示
        title: 天气                                                   # 标题，不设置则使用entity的friendly_name
        icons: /local/custom-lovelace/hf_weather-card/icons/animated/  # 图标路径，不设置则采用cdn，结尾要有"/"
```





参考：

https://ljr.im/articles/plugin-%C2%B7-change-lovelace-weather-card-based-on-windy/

https://bbs.hassbian.com/thread-7054-1-1.html