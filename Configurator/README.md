### Github 源码

https://github.com/danielperna84/hass-configurator

### 安装

https://github.com/danielperna84/hass-configurator/wiki/Installation

在树莓派直接执行 `pip install hass-configurator` 即可安装，安装后执行 `hass-configurator -l 192.168.53.188`  即可启动 configurator ，使用 `hass-configurator -h` 查看更多命令。

### 配置开机启动

https://github.com/danielperna84/hass-configurator/wiki/Daemonizing

``` shell
$ sudo vim /etc/systemd/system/hass-configurator.service
[Unit]
Description=HASS-Configurator
After=network.target

[Service]
Type=simple
User=pi
Group=pi
# Some security related options.
# See https://www.freedesktop.org/software/systemd/man/systemd.exec.html for details.
# NoNewPrivileges=true
# ProtectSystem=true
# InaccessiblePaths=-/mnt -/media
# ReadOnlyPaths=/bin -/lib -/lib64 -/sbin
# PrivateTmp=true
# ProtectKernelTunables=true
# ProtectKernelModules=true
# ProtectControlGroups=true
# RestrictRealtime=true

# Set configuration options by specifying environment variables
# Environment=HC_LISTENIP=0.0.0.0
# Environment=HC_PORT=3218
# Environment=HC_GIT=false
# Environment=HC_ALLOWED_NETWORKS=192.168.1.0/24,127.0.0.1
# ...
# Set the path to your configurator.py location
# WorkingDirectory=/etc/homeassistant
# You can also save your static options in a JSON formatted conf-file
ExecStart=sudo /usr/local/bin/hass-configurator -l 192.168.53.188
Restart=always

[Install]
WantedBy=multi-user.target
```

随后配置：

``` shell
$ sudo systemctl --system daemon-reload
$ sudo systemctl enable hass-configurator.service
$ sudo systemctl start hass-configurator.service
$ sudo systemctl status hass-configurator.service
```

配置 configuration.yaml

``` yaml
panel_iframe:
  configurator:
    title: Configurator
    icon: mdi:wrench
    url: http://192.168.53.188:3218
```



