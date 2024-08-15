# Author: Yinyuwiey
# 首先需要确保已经通过pip安装了 requests 、 plyer库
import requests
import sys
import subprocess
from plyer import notification

# 校园网登录所使用的URL请求参数
sign_parameter = '将此处引号里面的文本改为你的校园网登录URL请求参数'
# 校园网的名称
# 查询校园网WIFI名称可以打开cmd，输入这个命令netsh wlan show interfaces然后回车，在输出的信息找到SSID，SSID后的值即为校园网WIFI名称。
wlan_name = '将此处引号里面的文本改为里的校园网名称'


# 运行CMD脚本，获取当前WiFi名称
cmd = ['D:\\存放本项目文件的文件夹\\get_wifi_name.bat']
# 使用Popen以便手动处理编码问题，防止因为当前WiFi名称中含有中文导致报错。并设置creationflags参数，以隐藏命令行执行窗口，实现静默运行
# 也可使用 creationflags = subprocess.CREATE_NO_WINDOW, 实现进程不显示窗口，和0x08000000效果一致
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)
# 获取输出并指定使用UTF-8解码
stdout, stderr = process.communicate()
result = stdout.decode('utf-8', errors='ignore')  # 使用UTF-8解码，忽略不能解码的字符
# 输出当前WiFi名称
'''print(result)'''

# 判断当前WiFi名称是否与校园网名称匹配，匹配则进一步检查能否联网，不匹配则退出程序
if wlan_name in result:
    # 检查当前能否联网
    def connect_web():
        # requests 是一个常用的 HTTP 请求库，我们可以使用它来判断网络连接状态
        try:
            response = requests.get("http://connectivitycheck.platform.hicloud.com/generate_204")
            if response.status_code == 204:
                return True
            else:
                return False
        except requests.ConnectionError:
            return False
        # 上述代码中，我们使用 requests.get() 方法发送一个 GET 请求到华为延迟测速地址，并判断响应状态码。
        # 如果请求成功，status_code 属性将返回 204，表示连接成功。否则会抛出 ConnectionError 异常。我们通过捕获异常，来判断连接是否成功
    # 如果当前无网络，则执行登录指令，否则退出程序
    if connect_web() is False:
        try:
            requests.get(sign_parameter, timeout=20)
            notification.notify(
                title='校园网自动登录指令执行完成',
                message='请检查网络是否已经可用',
                app_icon='D:\\存放本项目文件的文件夹\\Check.ico',
                timeout=8,
            )
            # notify的timeout表示消息在屏幕上显示的时长
        finally:
            sys.exit(0)
    else:
        '''notification.notify(
            title='当前校园网已连接，无需执行自动登录',
            message='登录指令不会执行',
            app_icon='D:\\电脑自动登录校园网py文件\\logo_net.ico',
            timeout=8,
        )'''
        sys.exit(0)
else:
    '''notification.notify(
        title='当前网络非校园网，无需执行自动登录',
        message='登录指令不会执行',
        app_icon='D:\\电脑自动登录校园网py文件\\logo_net.ico',
        timeout=8,
    )'''
    sys.exit(0)
