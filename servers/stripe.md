# Stripe MCP Server

> 让 AI 查你的 Stripe：收款、客户、发票、退款、余额，还能直接查 Stripe 文档。

| 项 | 内容 |
|---|---|
| 维护方 | Stripe（官方托管） |
| 仓库 | https://github.com/stripe/ai |
| 许可证 | MIT（stripe/ai 仓库）；服务本身是 Stripe 官方托管的远程服务 |
| Star | 2,063（stripe/ai 仓库，截至 2026-11-15） |
| 类别 | 支付与收款 |
| 鉴权 | OAuth（首次使用时登录授权）/ 代理 API 密钥（Agent API key） |
| 亲测 | 2026-11-15，逐字核对官方文档 docs.stripe.com/mcp；未连接（需要你自己的 Stripe 账号） |
| Vic 评分 | **86 / 100** |

## 为什么收录

做外贸或一人公司收款，Stripe 是最常用的渠道之一。官方托管的远程 MCP 让 AI 直接查流水、客户、订阅和发票，不用你在 Dashboard 里翻页。权限是它的亮点：OAuth 授权时可以按沙盒或正式环境分别设置权限；涉及转账、退款这类动作要你在 Dashboard 点“批准”才会执行（官方标为 Human confirmation）。

## Vic 的用法（四条业务线）

- **外贸**：问“这个月美元收款有几笔、哪个客户还没付尾款”，或让 AI 起草并核对给海外客户的发票。
- **国际物流**：如果你向客户收物流服务费，可以让 AI 汇总已付、未付、退款情况，对账更快。
- **AI 一人公司**：看订阅、MRR、客户流失；查某笔扣款为什么失败。
- **全球自媒体**：如果你卖课程、会员或周边，可以查各产品的销量。

## 主要工具

`stripe_api_search` `stripe_api_details` `stripe_api_read`（读取任意 GET 接口） `stripe_api_write`（写入） `get_stripe_account_info` `stripe_analytics`（预览） `search_stripe_documentation` `stripe_implementation_planner` `get_balance_summary` `send_money` `transfer_money` `convert_currency` `setup_recipient` `atlas_company_formation` `send_stripe_feedback`。具体可用的取决于你的账号和授权。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - stripe --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。不加 `--write` 只打印配置。Cursor、Claude Code、Claude Desktop、VS Code 首次使用时会打开 Stripe 登录页。Codex 需要先设环境变量 `STRIPE_AGENT_API_KEY`（在 Stripe Dashboard 里创建带 Agent 标记的密钥，只勾需要的只读权限）。

## 手动配置

```json
{
  "mcpServers": {
    "stripe": {
      "url": "https://mcp.stripe.com"
    }
  }
}
```

用密钥的客户端把 `Authorization: Bearer <agent API key>` 放进请求头。官方说明：2026 年 12 月起，Stripe MCP 不再接受完整密钥和不带 Agent 标记的受限密钥，请改用新建的 Agent API 密钥或 OAuth。需要给你的网络放行 `mcp.stripe.com`。

## 注意事项与风险

- 这是真钱账号。**先连沙盒（Sandbox）**，确认好用再授权正式环境，并只给需要的权限。
- 打开客户端的“工具调用前确认”，不要让 AI 自动执行写入类工具。
- 退款、转账、创建发票等写入动作能改变真实账务；官方建议不要和其他不可信的 MCP 一起用，以防提示词注入。
- 官方标注为公开预览（Public preview），工具和行为可能变化。
- 我们没有连接实测，卡片内容均来自官方文档；`stripe/ai` 仓库本身没有开放的安全相关 Issue。
- 授权可以随时在 Stripe 用户设置的 OAuth sessions 里撤销。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15（仓库最近提交 2026-11-15） |
| 社区认可 | 6 / 10（约 2k Star） |
| 对四条业务线的用处 | 16 / 20（外贸收款、一人公司对账） |
| 上手难度 | 7 / 10（OAuth，需要 Stripe 账号） |
| 安全与权限 | 12 / 15（可按环境分权限、关键动作需人工确认；但能写） |
| 文档 | 10 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **86** |
