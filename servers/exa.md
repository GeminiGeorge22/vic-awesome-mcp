# Exa MCP Server

> 让 AI 用专为 AI 设计的搜索引擎搜全网，并把网页读成干净的 Markdown。

| 项 | 内容 |
|---|---|
| 维护方 | Exa（官方） |
| 仓库 | https://github.com/exa-labs/exa-mcp-server |
| 许可证 | MIT |
| Star | 5,231（截至 2026-11-14） |
| 类别 | 网页搜索 |
| 鉴权 | 免密钥（API Key 可选） |
| 亲测 | 2026-11-14，免密钥连接远程地址，tools/list 返回 2 个工具；web_search_exa 搜“德国 LED 灯具进口商”返回真实的德国进口分销商官网 |
| Vic 评分 | **89 / 100** |

## 为什么收录

搜索类 MCP 里上手最省事的一个：官方托管地址免密钥就能用（有频率限制），搜索结果直接带正文摘要，AI 不用再一个个打开网页。按“意思”搜而不只是按关键词，找公司、找同类网站特别准。需要更多次数时再加免费 Key。

## Vic 的用法（四条业务线）

- **外贸**：“找 10 家德国 LED 灯具进口商的官网”“找做户外家具的美国批发商”，直接拿到公司名、网址和简介，作为开发客户的线索。
- **国际物流**：搜某航线最新的运价新闻、港口拥堵、红海或苏伊士通航消息，汇总给客户。
- **AI 一人公司**：做竞品调研、查新工具和定价，写方案前先让 AI 搜一轮最新资料。
- **全球自媒体**：搜某个话题最近的海外热门文章和讨论，找选题和对标内容；读取文章全文做二次创作的素材。

## 主要工具

`web_search_exa` 搜索并返回干净正文 · `web_fetch_exa` 把一个或多个网址读成 Markdown，共 2 个默认工具。可选：`web_search_advanced_exa`（按域名、日期过滤）、`agent_run`（多步研究，需登录或 Key），用地址参数 `?tools=...` 开启。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - exa --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。默认不带 Key；搜得多了被限流，就设好 `EXA_API_KEY` 环境变量再加 `--with-key`。

## 手动配置

```json
{
  "mcpServers": {
    "exa": { "url": "https://mcp.exa.ai/mcp" }
  }
}
```

Claude Code：`claude mcp add --transport http exa https://mcp.exa.ai/mcp` · Codex：`codex mcp add exa --url https://mcp.exa.ai/mcp`

开启高级搜索：把地址换成 `https://mcp.exa.ai/mcp?tools=web_search_exa,web_fetch_exa,web_search_advanced_exa`（会替换默认工具，要用的都写上）。Key 可以用 `Authorization: Bearer` 请求头传，也支持 OAuth 登录。

## 注意事项与风险

- 搜索词会发到 Exa 的服务器，不要把客户隐私、报价底价写进搜索词。
- 只读工具，不会改你任何东西；但读到的网页内容可能夹带“提示词注入”，AI 照网页指示行事前要留意。
- 免密钥模式有频率限制，批量找客户时建议申请免费 Key。
- 搜到的公司信息要自己核实（官网、海关数据），不要直接当成准客户。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 10 / 15（最近一次提交 2026-11-03） |
| 社区认可 | 8 / 10 |
| 对四条业务线的用处 | 19 / 20 |
| 上手难度 | 10 / 10 |
| 安全与权限 | 13 / 15（只读，但查询会发到第三方） |
| 文档 | 9 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **89** |
