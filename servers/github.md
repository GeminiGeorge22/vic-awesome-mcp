# GitHub MCP Server

> 让 AI 直接管理你的 GitHub：看代码、提 Issue、审 PR、查 Actions 构建结果。

| 项 | 内容 |
|---|---|
| 维护方 | GitHub（官方） |
| 仓库 | https://github.com/github/github-mcp-server |
| 许可证 | MIT |
| Star | 34,419（截至 2026-11-13） |
| 类别 | 开发者工具 |
| 鉴权 | OAuth（VS Code 一键登录）或 Personal Access Token |
| 亲测 | 2026-11-13，逐字核对官方 README 与远程服务器文档；仓库当天有提交。需要个人 Token，未实际连接 |
| Vic 评分 | **92 / 100** |

## 为什么收录

GitHub 官方出品，提供托管好的远程地址，不用自己部署。它最大的优点是权限可以收得很紧：每个地址后面加 `/readonly` 就只能读，还能按功能（仓库、Issue、Actions 等）拆开只开需要的部分。

## Vic 的用法（四条业务线）

- **AI 一人公司**：管理你自己的开源仓库（vic-mcp-servers、vic-awesome-mcp 等）：让 AI 汇总新 Issue、回答用户提问的草稿、检查 Actions 有没有失败。
- **全球自媒体**：把 GitHub 当内容素材库，让 AI 统计各仓库 Star 增长，写进周报或推文。
- **外贸 / 物流**：用处间接。团队用 GitHub 管内部工具或文档时可以用。

## 本仓库的默认：只读

一行安装默认用 `https://api.githubcopilot.com/mcp/readonly`，AI 只能看、不能改。确实需要让它提 Issue、合并 PR 时，加 `--full-access`。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - github --client vscode --write    # VS Code：首次使用会弹出 GitHub 登录
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - github --client cursor --write    # 其他客户端：需要设置环境变量 GITHUB_PAT
```

Token 在 https://github.com/settings/personal-access-tokens/new 创建，建议用 fine-grained token，只勾需要的仓库和权限。

## 手动配置

VS Code（`.vscode/mcp.json`，OAuth）：

```json
{
  "servers": {
    "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/readonly" }
  }
}
```

Cursor（`~/.cursor/mcp.json`，Token）：

```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/readonly",
      "headers": { "Authorization": "Bearer ${env:GITHUB_PAT}" }
    }
  }
}
```

Claude Code：`claude mcp add --transport http github https://api.githubcopilot.com/mcp/readonly --header "Authorization: Bearer $GITHUB_PAT"`

本地 Docker 版（`ghcr.io/github/github-mcp-server`）支持 `--read-only` 和 `--lockdown-mode`，见官方 README。

## 注意事项与风险

- 公开仓库里的 Issue、评论可能藏着“提示词注入”。官方的 lockdown 模式能过滤无推送权限作者的内容，但官方说明它不是权限边界。
- Token 权限给多少，AI 就能做多少。只读地址 + 最小权限 Token 最稳。
- GitHub Enterprise Server 不支持远程地址，需要本地部署。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15 |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 15 / 20（主要服务一人公司线） |
| 上手难度 | 7 / 10（需要 OAuth 或 Token） |
| 安全与权限 | 15 / 15（只读地址、分功能地址、lockdown 模式） |
| 文档 | 10 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **92** |
