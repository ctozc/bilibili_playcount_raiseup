### 运行项目
1.启动redis

```bash
brew services start redis

redis-server
```

2.启动代理池 

```bash
cd proxy_pool

python3 proxyPool.py schedule

python3 proxyPool.py server
```

3.启动项目

```bash
python3 main.py
```