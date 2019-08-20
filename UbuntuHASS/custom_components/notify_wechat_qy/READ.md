wechatnotify:
  description: 企业微信通知
  fields:
    title:
      description: 消息标题
      example: "今日头条"
    message:
      description: 消息内容, 类型可以是“text, news, textcard, video, image"，当类型为text，只需要内容1；当类型为news，需要内容1和内容2和内容3，其中内容1为显示的文字，内容2为点开的连接，内容3为推送图片的连接；当类型为textcard，需要内容1和内容2，其中内容1为显示的文字，内容2为点开的连接；当类型为video，需要内容1和内容2，其中内容1为显示的文字，内容2为MP4文件的路径，比如 ，，{"title":"Homeassistant","message":"video|内容|/home/test/.homeassistant/1.mp4"}
      example: 格式："类型|内容1|内容2|内容3" 比如："video|内容|/home/test/.homeassistant/1.mp4", "image|内容|/home/test/.homeassistant/1.jpg"

