ProxyPool 爬虫代理IP池
=======

爬虫代理IP池,为定时采集网上发布的免费代理验证入库，定时验证入库的代理保证代理的可用性，提供API和CLI两种使用方式。同时你也可以扩展代理源以增加代理池IP的质量和数量。

### 运行项目
##### 下载代码:

```bash
git clone git@github.com:jhao104/proxy_pool.git
```

##### 更新setting.py配置

##### 本地启动项目:

```bash
# 启动调度程序
python3 proxyPool.py schedule

# 启动webApi服务
python3 proxyPool.py server
```

### Docker启动项目

```bash
docker pull jhao104/proxy_pool

docker run --env DB_CONN=redis://:password@ip:port/0 -p 5010:5010 jhao104/proxy_pool:latest
```
### docker-compose

项目目录下运行: 
``` bash
docker-compose up -d
```

### docker安装redis 

```dockerfile
sudo docker pull redis
```

### docker启动redis
```bash
sudo docker run -d --name redis -p 6379:6379 redis --requirepass "password"
-p 端口
-requirepass "密码"
```

### 使用

* Api

启动web服务后, 默认配置下会开启 http://127.0.0.1:5010 的api接口服务:

| api | method | Description | params|
| ----| ---- | ---- | ----|
| / | GET | api介绍 | None |
| /get | GET | 随机获取一个代理| 可选参数: `?type=https` 过滤支持https的代理|
| /pop | GET | 获取并删除一个代理| 可选参数: `?type=https` 过滤支持https的代理|
| /all | GET | 获取所有代理 |可选参数: `?type=https` 过滤支持https的代理|
| /count | GET | 查看代理数量 |None|
| /delete | GET | 删除代理  |`?proxy=host:ip`|


* 爬虫使用

　　如果要在爬虫代码中使用的话， 可以将此api封装成函数直接使用，例如：

```python
import requests

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

def getHtml():
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            html = requests.get('http://www.example.com', proxies={"http": "http://{}".format(proxy)})
            # 使用代理访问
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None
```

### 扩展代理

　　项目默认包含几个免费的代理获取源，但是免费的毕竟质量有限，所以如果直接运行可能拿到的代理质量不理想。所以，提供了代理获取的扩展方法。

　　添加一个新的代理源方法如下:

* 1、首先在[ProxyFetcher](https://github.com/jhao104/proxy_pool/blob/1a3666283806a22ef287fba1a8efab7b94e94bac/fetcher/proxyFetcher.py#L21)类中添加自定义的获取代理的静态方法，
该方法需要以生成器(yield)形式返回`host:ip`格式的代理，例如:

```python

class ProxyFetcher(object):
    # ....

    # 自定义代理源获取方法
    @staticmethod
    def freeProxyCustom1():  # 命名不和已有重复即可

        # 通过某网站或者某接口或某数据库获取代理
        # 假设你已经拿到了一个代理列表
        proxies = ["x.x.x.x:3128", "x.x.x.x:80"]
        for proxy in proxies:
            yield proxy
        # 确保每个proxy都是 host:ip正确的格式返回
```

* 2、添加好方法后，修改[setting.py](https://github.com/jhao104/proxy_pool/blob/1a3666283806a22ef287fba1a8efab7b94e94bac/setting.py#L47)文件中的`PROXY_FETCHER`项：

　　在`PROXY_FETCHER`下添加自定义方法的名字:

```python
PROXY_FETCHER = [
    "freeProxy01",    
    "freeProxy02",
    # ....
    "freeProxyCustom1"  #  # 确保名字和你添加方法名字一致
]
```

　　`schedule` 进程会每隔一段时间抓取一次代理，下次抓取时会自动识别调用你定义的方法。

### 免费代理源

   目前实现的采集免费代理网站有(排名不分先后, 下面仅是对其发布的免费代理情况, 付费代理测评可以参考[这里](https://zhuanlan.zhihu.com/p/33576641)): 
   
  |   代理名称   |  状态  |  更新速度 |  可用率  |  地址 |    代码   |
  | ---------   |  ---- | --------  | ------  | ----- |   ------- |
  | 站大爷     |  ✔    |     ★     |   **     | [地址](https://www.zdaye.com/)    | [`freeProxy01`](/fetcher/proxyFetcher.py#L28) |
  | 66代理     |  ✔    |     ★     |   *     | [地址](http://www.66ip.cn/)         | [`freeProxy02`](/fetcher/proxyFetcher.py#L50) |
  | 开心代理     |   ✔   |     ★     |   *     | [地址](http://www.kxdaili.com/)     | [`freeProxy03`](/fetcher/proxyFetcher.py#L63)  |
  | FreeProxyList |   ✔  |    ★     |   *    | [地址](https://www.freeproxylists.net/zh/) | [`freeProxy04`](/fetcher/proxyFetcher.py#L74) |
  | 快代理       |  ✔    |     ★     |   *     | [地址](https://www.kuaidaili.com/)  | [`freeProxy05`](/fetcher/proxyFetcher.py#L92)  |
  | FateZero    |  ✔    |    ★★    |   *     | [地址](http://proxylist.fatezero.org) | [`freeProxy06`](/fetcher/proxyFetcher.py#L111) |
  | 云代理       |  ✔    |     ★     |   *     | [地址](http://www.ip3366.net/)      | [`freeProxy07`](/fetcher/proxyFetcher.py#L124) |
  | 小幻代理     |  ✔    |     ★★    |    *    | [地址](https://ip.ihuan.me/)        | [`freeProxy08`](/fetcher/proxyFetcher.py#L134) |
  | 免费代理库   |  ✔    |      ☆     |    *    | [地址](http://ip.jiangxianli.com/)   | [`freeProxy09`](/fetcher/proxyFetcher.py#L144) |
  | 89代理      |  ✔    |      ☆     |   *     | [地址](https://www.89ip.cn/)         | [`freeProxy10`](/fetcher/proxyFetcher.py#L155) |
