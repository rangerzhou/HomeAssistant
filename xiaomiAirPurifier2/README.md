

1. 下载组件放入 HA 对应目录

2. 配置 configurations.yaml:

``` yaml
homeassistant:
  ...
  # 包含 packages
  packages: !include_dir_named packages
```

3. 安装 home-assistant-custom-ui

``` shell
# 在 ~/home/homeassistant/ 下载 update.sh
$ curl -o update.sh "https://raw.githubusercontent.com/andrey-git/home-assistant-custom-ui/master/update.sh?raw=true"
$ chmod a+x update.sh
$ ./update.sh
```

4. 激活 home-assistant-custom-ui, 配置 configurations.yaml:

``` shell
homeassistant:
  ...
  # Activating home-assistant-custom-ui
  customize_glob:
  "*.*":
    custom_ui_state_card: state-card-custom-ui
frontend:
  extra_html_url:
    - /local/custom_ui/state-card-custom-ui.html
  extra_html_url_es5:
    - /local/custom_ui/state-card-custom-ui-es5.html
```

