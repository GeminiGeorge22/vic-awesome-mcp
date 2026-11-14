# Time MCP Server

> 让 AI 准确知道“现在几点”，并在全球时区之间换算时间（自动处理夏令时）。

| 项 | 内容 |
|---|---|
| 维护方 | Model Context Protocol 官方（参考实现） |
| 仓库 | https://github.com/modelcontextprotocol/servers/tree/main/src/time |
| 许可证 | MIT / Apache-2.0（官方仓库正从 MIT 迁移到 Apache-2.0） |
| Star | 91,976（整个 modelcontextprotocol/servers 仓库，截至 2026-11-14） |
| 类别 | 时间与时区 |
| 鉴权 | 免密钥 |
| 亲测 | 2026-11-14，uvx 本地 stdio 启动，tools/list 返回 3 个工具；convert_time 把上海 21:00 换算到洛杉矶，返回相差 -16 小时（正确） |
| Vic 评分 | **90 / 100** |

## 为什么收录

大模型本身不知道“现在”，算时差也常出错，尤其碰到夏令时切换。这个 MCP 是协议官方维护的参考实现，只做一件事：读系统时钟、按 IANA 时区（如 `America/New_York`）换算，结果可靠。完全本地运行，不联网、不读文件、不需要任何账号，是最安全的一类 MCP。

## Vic 的用法（四条业务线）

- **外贸**：约欧美客户开会时，让 AI 直接给出“对方当地上午 10 点 = 北京时间几点”，并提醒对方是否刚进入或结束夏令时；写开发信时注明对方工作时间再发。
- **国际物流**：把船公司给的截关、截单时间（常是港口当地时间）统一换成北京时间，避免错过 cut-off；算“到港后已过去多少小时”。
- **AI 一人公司**：跨时区排日程、写自动化脚本时让 AI 拿到准确的当前时间，不再靠猜。
- **全球自媒体**：按目标受众所在时区（如美西晚 8 点）推算北京时间的发帖时刻，排期更准。

## 主要工具

`get_current_time` 查任意时区当前时间 · `convert_time` 两个时区之间换算 · `get_time_ago` 算“N 天 / 小时前”是什么时候，共 3 个。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - time --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。不加 `--write` 只打印配置。

## 手动配置

```json
{
  "mcpServers": {
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time"]
    }
  }
}
```

Claude Code：`claude mcp add time -- uvx mcp-server-time` · Codex：`codex mcp add time -- uvx mcp-server-time`

需要先装 [uv](https://docs.astral.sh/uv/)（提供 `uvx` 命令）。也可以 `pip install mcp-server-time` 后用 `python -m mcp_server_time`，或用 Docker 镜像 `mcp/time`。默认用电脑的系统时区，想固定可加 `--local-timezone Asia/Shanghai`。

## 注意事项与风险

- 纯本地计算，不联网、不写文件，几乎没有风险。
- 时区名要写准确的 IANA 名字，大小写也要对（`Asia/Shanghai` 可以，`asia/shanghai` 会报错）。
- 夏令时回拨那天同一时刻会出现两次，它会把两次都告诉你，不会替你乱猜。
- 用处单一：只管时间，不查航班、船期等实时数据。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15 |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 12 / 20（四条线都用得上，但只解决时间换算这一件事） |
| 上手难度 | 9 / 10（免密钥，但要先装 uv） |
| 安全与权限 | 15 / 15 |
| 文档 | 9 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **90** |
