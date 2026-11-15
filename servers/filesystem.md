# Filesystem MCP Server

> 让 AI 读取你指定文件夹里的文件：报价单、合同、素材、日志。默认只读，只能碰你划定的那个文件夹。

| 项 | 内容 |
|---|---|
| 维护方 | Model Context Protocol 官方（参考实现） |
| 仓库 | https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem |
| 许可证 | MIT / Apache-2.0（官方仓库正从 MIT 迁移到 Apache-2.0） |
| Star | 92,002（整个 modelcontextprotocol/servers 仓库，截至 2026-11-15） |
| 类别 | 本地文件 |
| 鉴权 | 免密钥 |
| 亲测 | 2026-11-15，npx 本地 stdio 启动（--read-only），tools/list 返回 10 个工具，且不含任何写入工具；read_text_file 成功读出测试文件。去掉 --read-only 时为 14 个工具 |
| Vic 评分 | **90 / 100** |

## 为什么收录

AI 想看你电脑上的文件，最稳的办法就是这个官方服务器：你在启动命令里写明允许的文件夹，它就只能在里面操作，越界一律拒绝。2.3.0 版加了 `--read-only`，写入类工具根本不会出现在列表里，由服务器强制，不靠客户端自觉。装法也简单：一个 npx 命令。

## Vic 的用法（四条业务线）

- **外贸**：把客户询盘、历史报价单、产品目录放进一个文件夹，让 AI 翻出“去年给这位客户的报价”，照着生成新报价。
- **国际物流**：让 AI 读一批提单、装箱单、发票的文本或 CSV，核对件数、重量是否对得上。
- **AI 一人公司**：让 AI 读项目目录、日志、笔记，回答“这个脚本昨天为什么失败”。需要它写文件时再加 `--full-access`。
- **全球自媒体**：让 AI 浏览选题库、脚本草稿、素材文件夹，找出还没用过的选题。

## 主要工具

只读模式 10 个：`read_text_file` `read_media_file` `read_multiple_files` `list_directory` `list_directory_with_sizes` `directory_tree` `search_files` `get_file_info` `list_allowed_directories`（外加兼容旧名的 `read_file`）。加 `--full-access` 后多出 `write_file` `edit_file` `create_directory` `move_file` 等写入类，共 14 个。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - filesystem --client cursor --write --dir ~/Documents/vic-work
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。不加 `--write` 只打印配置。`--dir` 是必填的：你想让 AI 看哪个文件夹就写哪个。想让 AI 也能改文件，再加 `--full-access`。

## 手动配置

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem@2.3.0", "--read-only", "/Users/你/Documents/vic-work"]
    }
  }
}
```

Claude Code：`claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem@2.3.0 --read-only /你的/文件夹` · Codex：`codex mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem@2.3.0 --read-only /你的/文件夹`

需要 Node.js。版本号固定在 2.3.0，因为 `--read-only` 是新版才有的参数；旧版会把它当成文件夹名忽略，反而变成可写，所以请保持 2.3.0 或更新的版本。想只保护其中一个文件夹，可用 `--read-only-dir <路径>`。

## 注意事项与风险

- 文件夹别选太大。不要把整个用户目录或放密钥的目录交给它。
- 不加 `--read-only` 时 AI 能覆盖、移动文件，且 `write_file` 是直接覆盖。重要文件先备份。
- 文件内容会被送进模型，里面若有别人写的指令（提示词注入），模型可能照做；读不可信文件时别同时开启写权限。
- 路径检查按路径名进行，硬链接指向允许目录外时，改文件会改到所有名字（官方文档明确提醒）。
- 官方仓库同期有若干开放 Issue，未见公开的严重未修复安全问题。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15（最近提交 2026-11-11） |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 13 / 20（读本地单据、素材很实用，但不产生新数据） |
| 上手难度 | 9 / 10（免密钥，但要指定文件夹） |
| 安全与权限 | 15 / 15（`--read-only` 由服务器强制，只能访问指定目录） |
| 文档 | 8 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **90** |
