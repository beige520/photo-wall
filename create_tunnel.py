import subprocess
import re
import time
import sys

print("正在启动本地服务器...")
server = subprocess.Popen(
    ['python', '-m', 'http.server', '8888'],
    cwd=r'C:\Users\zhj08\Desktop\红梅与贝',
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)
time.sleep(2)

print("正在创建公开链接...")
print("使用 localhost.run 服务...")
print("请在手机上访问以下链接：")
print()
print("="*60)

# 使用SSH命令创建隧道
try:
    ssh_process = subprocess.Popen(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-R', '80:localhost:8888', 'localhost.run'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 读取输出
    for line in iter(ssh_process.stdout.readline, ''):
        if line:
            print(line.rstrip())
            # 查找URL
            if 'localhost.run' in line or '.trycloudflare.com' in line:
                match = re.search(r'(https?://[^\s]+)', line)
                if match:
                    url = match.group(1)
                    print()
                    print("="*60)
                    print(f"🎉 公开链接已创建！")
                    print(f"📱 手机访问: {url}")
                    print("="*60)
                    print()
                    print("按 Ctrl+C 停止服务")
                    break
    
except KeyboardInterrupt:
    print("\n正在停止服务...")
    ssh_process.terminate()
    server.terminate()
except Exception as e:
    print(f"错误: {e}")
    print("请确保已安装SSH客户端")
