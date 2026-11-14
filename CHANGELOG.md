# Changelog

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
