# lixinger

理杏仁 Python SDK (非官方).

包含以下功能:

- 自动将请求结果转换结果为 Dataframe.
- 根据官方文档中的返回结果定义, 验证请求结果, 对缺少的列进行补齐, 对列类型进行相应转换.
- 支持一次性获取时间范围大于 10 年的数据.
- 适当缓存请求结果, 减少请求 API 次数.
- 遇到网络错误时, 自动重试请求.

## 安装

```bash
pip install lixinger
```

## 用法

### 获取 Token

Token 获取地址为 [https://www.lixinger.com/open/api/token](https://www.lixinger.com/open/api/token).

### 调用 API

使用文档请参考 [理杏仁开放平台](https://www.lixinger.com/open/api/doc).

方法导入路径可以根据文档中的请求 URL 得出, 例如下面代码中对应的请求 URL 为 `/api/cn/company` 则把 `/` 换成 `.` 即可.

```python
from lixinger.utils import set_token
from lixinger.api.cn.company.base import get_company

# 设置 Token
set_token("your_token")

# 获取股票详细信息
company = get_company(stock_codes=["600519"])
print(company)
```

将会看到以下输出内容:

```bash
  stock_code market            ipo_date  ... mutual_markets  name        fs_type
0     600519      a 2001-08-26 16:00:00  ...             ha  贵州茅台  non_financial

[1 rows x 7 columns]
```
