# fucking-school-gate

这是一个绕过学校进出扫码认证的中间人代理程序。

## 安装
`pip3 install mitmproxy lxml beautifulsoup4` 

## 启动
`mitmdump -p "your-port" -s fucking_school_gate.py --set block_global=false`

## 使用
安卓手机可连接WiFi，在所连接WiFi的高级设置里设置手动代理，填写部署程序的服务器ip和程序启动端口即可；也可使用流量，可以在APN接入点中选择当前接入点，在代理和端口位置填写服务器ip和程序启动端口，保存即可。
