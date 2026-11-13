# Playwright MCP

> 让 AI 像人一样打开网页、点击、填表、截图、抓数据，不需要视觉模型。

| 项 | 内容 |
|---|---|
| 维护方 | Microsoft（官方） |
| 仓库 | https://github.com/microsoft/playwright-mcp |
| 许可证 | Apache-2.0 |
| Star | 39,571（截至 2026-11-13） |
| 类别 | 浏览器自动化 |
| 鉴权 | 免密钥 |
| 亲测 | 2026-11-13，npx 本地 stdio 启动，tools/list 返回 25 个工具 |
| Vic 评分 | **92 / 100** |

## 为什么收录

浏览器自动化 MCP 里最权威的一个：微软官方维护、几乎每天更新。它读的是网页的“无障碍树”（结构化文字），不是截图，所以又快又准，普通文字模型就能用。很多网站没有 API，有了它，AI 就能替你操作这些网站。

## Vic 的用法（四条业务线）

- **外贸**：打开 B2B 平台或竞品官网，抓同类产品的价格、MOQ、卖点，整理成对比表。
- **国际物流**：在船公司或货代网站查船期、查柜号轨迹，把结果汇总给客户。
- **AI 一人公司**：自动填写重复的后台表单，给自己的落地页做上线前检查（链接、表单、手机端截图）。
- **全球自媒体**：批量打开对标账号主页，记录最近发帖主题和互动数据。

## 主要工具

`browser_navigate` 打开网页 · `browser_snapshot` 读取页面结构 · `browser_click` / `browser_type` / `browser_fill_form` 点击和填表 · `browser_take_screenshot` 截图 · `browser_tabs` 多标签 · `browser_wait_for` 等待加载，共 25 个。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - playwright --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。不加 `--write` 只打印配置，不改文件。

## 手动配置

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest", "--isolated"]
    }
  }
}
```

本仓库默认加了 `--isolated`（浏览器资料只存内存，关掉即清空）。需要保持登录状态时去掉它。

Claude Code：`claude mcp add playwright -- npx @playwright/mcp@latest --isolated` · Codex：`codex mcp add playwright -- npx @playwright/mcp@latest --isolated`

需要 Node.js 18+。

## 注意事项与风险

- AI 能访问任何网站；如果去掉隔离模式，还能用到你已登录的账号。本仓库的配置默认加了 `--isolated`（浏览器资料只存在内存里，关掉就清空），不要让它碰网银和支付页面。
- 有一个 `browser_run_code_unsafe` 工具可以在页面里执行任意代码，名字已经写明不安全；让 AI 用之前先看清它要跑什么。
- `--allowed-origins` 可以限定能访问的网站，但官方说明它**不是**安全边界。
- 官方也提供 Playwright CLI + Skills 版本，写代码场景更省上下文；需要长时间连续操作浏览器时用 MCP 更合适。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15 |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 19 / 20 |
| 上手难度 | 10 / 10 |
| 安全与权限 | 8 / 15（可执行任意页面代码、默认可访问所有网站） |
| 文档 | 10 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **92** |
