# Context7

> 让 AI 写代码前先查“最新版”的官方文档，不再照着过时的 API 瞎写。

| 项 | 内容 |
|---|---|
| 维护方 | Upstash |
| 仓库 | https://github.com/upstash/context7 |
| 许可证 | MIT |
| Star | 64,708（截至 2026-11-13） |
| 类别 | 编程文档 |
| 鉴权 | 免密钥可用；免费 API Key 提高调用额度 |
| 亲测 | 2026-11-13，无密钥连接远程地址，tools/list 返回 2 个工具，搜索 “mcp python sdk” 正确返回官方 MCP Python SDK 文档 |
| Vic 评分 | **89 / 100** |

## 为什么收录

AI 模型的知识有截止日期，库一升级它就写错。我们自己做 MCP Server 时就碰到过：MCP Python SDK 2.x 把 `FastMCP` 改名成 `MCPServer`，模型还在写旧写法。Context7 把几千个库的最新文档整理好，AI 写代码前先查一下，错误少很多。

## Vic 的用法（四条业务线）

- **AI 一人公司**：搭 Agent、写 MCP Server、做小工具时，让 AI 先查最新文档再写代码。这是它的主场。
- **全球自媒体**：写技术类教程或视频脚本时，确保代码示例是当前版本。
- **外贸 / 物流**：用处间接，自己写报价、跟单小工具时用得上。

## 主要工具

- `resolve-library-id`：把“mcp python sdk”这种名字转成 Context7 的库 ID。
- `query-docs`：按库 ID 和问题取相关文档和代码示例。

用法小技巧：在提示词里加一句 “use context7”，或在客户端规则里写“需要查库文档时总是用 Context7”。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - context7 --client cursor --write
```

默认不带密钥。有了免费 Key（https://context7.com/dashboard）后加 `--with-key`，并设置环境变量 `CONTEXT7_API_KEY`。官方也提供 `npx ctx7 setup` 一键配置（需 Node.js 22.13+）。

## 手动配置

```json
{
  "mcpServers": {
    "context7": { "url": "https://mcp.context7.com/mcp" }
  }
}
```

Claude Code：`claude mcp add --transport http context7 https://mcp.context7.com/mcp`

## 注意事项与风险

- 你的查询内容会发到 Upstash 的服务器。不要在查询里放客户资料或密钥。
- 只读工具，不会改你的任何东西。
- 文档由社区和厂商提交，冷门库可能缺失或不是最新；关键代码仍要对照官方文档。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 12 / 15（知名公司，非各库官方） |
| 活跃度 | 15 / 15 |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 14 / 20（主要服务一人公司线） |
| 上手难度 | 10 / 10 |
| 安全与权限 | 14 / 15（只读；查询内容发往第三方） |
| 文档 | 9 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **89** |
