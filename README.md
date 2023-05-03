# lixinger

理杏仁 Python SDK (非官方).

## 安装

```bash
pip install lixinger
```

## 用法

设置自己的 Token (配置文件路径: ~/.config/lixinger/settings.toml)

```toml
[default]
token = "your token"
```

使用文档请参考 [理杏仁开放平台](https://www.lixinger.com/open/api/doc)

```python
from lixinger.api.cn.company.base import get_company

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
