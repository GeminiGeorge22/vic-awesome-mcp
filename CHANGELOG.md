# Changelog

## 2026-11-15

- 新增 Filesystem MCP Server（90）：协议官方，让 AI 读你指定文件夹里的单据，默认只读。
- 新增 Memory MCP Server（88）：协议官方，本地知识图谱，让 AI 跨对话记住客户和习惯。
- 新增 Stripe MCP Server（86）：Stripe 官方托管，查收款和账务，关键动作需人工批准；未连接实测。
- install.py：新增 `--dir`（指定文件夹）、本地服务器的固定环境变量、`--full-access` 对本地服务器生效；validate.py 的 smoke 测试同步支持。

## 2026-11-14

- 新增 Time MCP Server（90）：协议官方参考实现，本地跨时区换算，约客户、算截关时间不再出错。
- 新增 Exa MCP Server（89）：Exa 官方 AI 搜索，免密钥可用，找海外客户和选题。
- 新增 Apify MCP Server（89）：Apify 官方，几千个现成爬虫（Google 地图、Instagram、TikTok、亚马逊），默认关闭数据上报。
- install.py：OAuth 提示改为通用说法；validate.py：smoke 测试只对 npx 加 -y（支持 uvx）。

## 2026-11-13

- 新增 Playwright MCP（92）：微软官方浏览器自动化，默认隔离模式。
- 新增 GitHub MCP Server（92）：GitHub 官方，默认只读地址。
- 新增 Context7（89）：最新库文档，免密钥可用。
- 首发：精选标准、一行安装脚本 install.py（5 个客户端）、目录 catalog.json、校验脚本 tools/validate.py。
