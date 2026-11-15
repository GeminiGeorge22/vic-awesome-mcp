# Memory MCP Server

> 给 AI 一本跨对话的记事本：客户偏好、报价规则、你的习惯，下次还记得。

| 项 | 内容 |
|---|---|
| 维护方 | Model Context Protocol 官方（参考实现） |
| 仓库 | https://github.com/modelcontextprotocol/servers/tree/main/src/memory |
| 许可证 | MIT / Apache-2.0（官方仓库正从 MIT 迁移到 Apache-2.0） |
| Star | 92,002（整个 modelcontextprotocol/servers 仓库，截至 2026-11-15） |
| 类别 | 持久记忆 |
| 鉴权 | 免密钥 |
| 亲测 | 2026-11-15，npx 本地 stdio 启动，tools/list 返回 9 个工具；create_entities 写入一个实体后，read_graph 能读回来 |
| Vic 评分 | **88 / 100** |

## 为什么收录

大模型每次新对话都从零开始。这个服务器把“谁、是什么、有什么特点、和谁什么关系”存成一个本地知识图谱文件，AI 可以随时写入、搜索、修改。全部在本机，不联网，不需要账号。官方 README 提醒默认存储位置在 node_modules 里，更新或清缓存可能丢文件，所以我们的安装脚本直接把存储路径设到你的家目录 `~/vic-memory.jsonl`。

## Vic 的用法（四条业务线）

- **外贸**：记下每个客户的币种、付款方式、常订型号、喜欢的沟通口吻，下次起草报价或邮件自动照做。
- **国际物流**：记下常用货代、航线的报价区间和截关习惯，让 AI 比价时有历史可参考。
- **AI 一人公司**：记下产品决策、命名规则、踩过的坑，换个对话窗口也不用重讲。
- **全球自媒体**：记下各账号的人设、禁用词、爆款结构，让 AI 写稿保持一致。

## 主要工具

`create_entities` `create_relations` `add_observations` `delete_entities` `delete_observations` `delete_relations` `read_graph` `search_nodes` `open_nodes`，共 9 个。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - memory --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。不加 `--write` 只打印配置。安装脚本会把记忆文件设到 `~/vic-memory.jsonl`，多个客户端装了同一个就共用同一份记忆（官方用文件锁保证不互相覆盖）。

## 手动配置

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory@2.1.1"],
      "env": { "MEMORY_FILE_PATH": "/Users/你/vic-memory.jsonl" }
    }
  }
}
```

Claude Code：`claude mcp add memory -e MEMORY_FILE_PATH=/Users/你/vic-memory.jsonl -- npx -y @modelcontextprotocol/server-memory@2.1.1`

`MEMORY_FILE_PATH` 要写绝对路径，且所在文件夹必须已存在。需要 Node.js。

## 注意事项与风险

- 记忆文件是明文 JSONL，别让 AI 存密码、银行卡、客户证件号。
- AI 写什么就存什么，没有确认步骤。偶尔打开文件看看，删掉不对的内容。
- 记忆会被带进之后的对话，写错了会一直影响后面的回答。
- 文件不加密、不自动备份。想保留就自己拷贝。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15（最近提交 2026-11-11） |
| 社区认可 | 10 / 10 |
| 对四条业务线的用处 | 12 / 20（四条线都用得上，但效果取决于你怎么用） |
| 上手难度 | 10 / 10 |
| 安全与权限 | 12 / 15（纯本地，但写入无确认、明文存储） |
| 文档 | 9 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **88** |
