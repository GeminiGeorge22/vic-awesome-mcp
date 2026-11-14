# Apify MCP Server

> 让 AI 调用 Apify 商店里几千个现成爬虫：Google 地图、Instagram、TikTok、亚马逊……要数据直接说，拿到结构化结果。

| 项 | 内容 |
|---|---|
| 维护方 | Apify（官方） |
| 仓库 | https://github.com/apify/apify-mcp-server |
| 许可证 | MIT |
| Star | 16,162（截至 2026-11-14） |
| 类别 | 网页抓取与数据采集 |
| 鉴权 | OAuth（大多数客户端首次使用时登录）/ API Token |
| 亲测 | 2026-11-14，核对官方 README；未登录时用 `?tools=search-actors,fetch-actor-details` 连上远程地址（2 个工具），search-actors 搜“instagram scraper”返回真实结果。完整工具需要你的账号，未连接 |
| Vic 评分 | **89 / 100** |

## 为什么收录

Playwright 是让 AI 一步步点浏览器；Apify 是直接调用别人做好的“专用爬虫”（叫 Actor），它们已经处理好登录墙、代理和反爬，返回干净的表格数据。一个 MCP 就能用上几千个网站的采集能力，不用每个网站装一个。官方维护，几乎每天发版。

## Vic 的用法（四条业务线）

- **外贸**：用 Google Maps Scraper 批量抓“迪拜 建材批发商”的公司名、电话、网站、评分，做客户名单；抓亚马逊同类产品价格和评论，做选品和报价参考。
- **国际物流**：抓 Google 地图上目的港附近的货代、仓库、清关行；整理成合作方名单。
- **AI 一人公司**：把重复的数据采集做成 Apify 定时任务，AI 只负责发起和读结果。
- **全球自媒体**：抓对标账号在 Instagram、TikTok、YouTube 的最近帖子、播放量和评论，分析爆款规律；监控品牌关键词。

## 主要工具

`search-actors` 在商店里找合适的爬虫 · `fetch-actor-details` 看输入参数和价格 · `call-actor` 运行爬虫 · 读取运行结果的存储工具 · `search-apify-docs` 查文档。默认还带 Web Search 和 Web Fetch 两个爬虫。用地址参数 `?tools=apify/instagram-scraper` 可以只开某一个爬虫。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - apify --client cursor --write
```

Cursor、VS Code、Claude Code、Claude Desktop 首次使用时会弹出 Apify 登录页（OAuth），不用填 Token。Codex 需要先设 `APIFY_TOKEN` 环境变量（获取方法见 https://docs.apify.com/integrations/api#api-token ）。

## 手动配置

```json
{
  "mcpServers": {
    "apify": { "url": "https://mcp.apify.com?telemetry-enabled=false" }
  }
}
```

Claude Code：`claude mcp add apify "https://mcp.apify.com?telemetry-enabled=false" -t http`

本仓库默认加了 `telemetry-enabled=false`（关闭 Apify 的使用数据上报，官方 README 写明这样可以关）。本地版：`npx -y @apify/actors-mcp-server`（需要 Node.js 22+ 和 `APIFY_TOKEN`）。

## 注意事项与风险

- **会花钱**：运行爬虫消耗 Apify 账户额度，按各爬虫自己的价格计费。让 AI 调用 `call-actor` 时在 `callOptions` 里加 `maxTotalChargeUsd` 或 `maxItems` 限制花费。
- 有些爬虫需要“完全权限”，首次运行会要求你点链接批准，看清再批。删除爬虫等危险工具默认不加载。
- 抓社交平台、地图数据要遵守平台条款和当地隐私法规，抓来的个人联系方式不要直接群发。
- 爬虫来自不同作者，质量和价格差别大，优先选 Apify 官方或高评分的。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15 |
| 社区认可 | 8 / 10 |
| 对四条业务线的用处 | 19 / 20 |
| 上手难度 | 7 / 10（OAuth 登录；爬虫按量付费） |
| 安全与权限 | 10 / 15（能运行付费爬虫；危险工具默认不加载、可设花费上限） |
| 文档 | 10 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **89** |
