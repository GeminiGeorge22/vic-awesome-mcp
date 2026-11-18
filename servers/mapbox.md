# Mapbox MCP Server

> 让 AI 查地图：地址转坐标、两点间路线和时间、一次算多点距离、给多个送货点排最优顺序。

| 项 | 内容 |
|---|---|
| 维护方 | Mapbox（官方） |
| 仓库 | https://github.com/mapbox/mcp-server |
| 许可证 | MIT |
| Star | 372（截至 2026-11-18） |
| 类别 | 地图与地理 |
| 鉴权 | Mapbox 访问令牌（免费账号）/ 托管端点支持 OAuth 登录 |
| 亲测 | 2026-11-18，用 npx @mapbox/mcp-server 以 stdio 连接（假令牌）：列出 32 个工具，离线 distance_tool 返回 3.441 公里；联网工具（路线、地理编码）未调用，需要你自己的令牌，配置已逐字核对官方 README |
| Vic 评分 | **86 / 100** |

## 为什么收录

物流线一直缺一个真正的地图类服务。Mapbox 官方这个服务既有联网的路线、等时圈、多点矩阵、路线优化，也有一批不用联网的距离、面积、缓冲区计算工具。所有工具都是查询和计算，不会改你的任何数据。

## Vic 的用法（四条业务线）

- **国际物流**：给一批送货或提货地址排最优顺序（optimization），算仓库到港口、客户的驾车时间和距离（directions、matrix），画某仓库 2 小时车程覆盖范围（isochrone）。
- **外贸**：查海外客户工厂或展会地址的坐标，估算从工厂到港口要多久，安排拜访路线。
- **AI 一人公司**：做带地图的网页或报告时，让 AI 直接生成静态地图图片。
- **全球自媒体**：用处间接，可做探店、旅行类内容的路线图。

## 主要工具

`search_and_geocode_tool` `reverse_geocode_tool` `directions_tool` `matrix_tool` `isochrone_tool` `optimization_tool` `map_matching_tool` `category_search_tool` `static_map_image_tool` `render_map_tool` 以及 `distance_tool` `area_tool` `buffer_tool` 等离线地理计算工具，共 32 个。

## 一行安装

```bash
curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - mapbox --client cursor --write
```

把 `cursor` 换成 `claude-desktop`、`claude-code`、`vscode` 或 `codex`。Cursor、Claude Code、Claude Desktop、VS Code 首次使用会走 OAuth 登录；也可以设环境变量 `MAPBOX_ACCESS_TOKEN`（在 Mapbox 账号后台创建令牌）。Codex 需要先设这个环境变量。

## 手动配置

```json
{
  "mcpServers": {
    "mapbox": {
      "url": "https://mcp.mapbox.com/mcp",
      "headers": { "Authorization": "Bearer <你的 Mapbox 访问令牌>" }
    }
  }
}
```

## 注意事项与风险

- 联网工具按你的 Mapbox 账号用量计费，免费额度用完会收费；建议给令牌只开需要的权限。
- 令牌不要写进仓库或聊天；公开令牌（pk.）被别人拿到会消耗你的额度。
- 地址会发到 Mapbox 服务器，客户隐私地址要留意。
- 仓库 Star 不高（372），但是官方维护，每天都有提交；没有开放的安全相关问题（只有 1 条搜索命中，未发现未修复的严重安全问题）。
- 其中的反馈工具会向 Mapbox 发信息，可用 `--disable-tools feedback_tool` 关掉（本地运行时）。

## 评分明细

| 维度 | 分 |
|---|---|
| 维护方可信度 | 15 / 15 |
| 活跃度 | 15 / 15（最近提交 2026-11-18） |
| 社区认可 | 3 / 10 |
| 对四条业务线的用处 | 15 / 20（物流路线、外贸拜访） |
| 上手难度 | 8 / 10（免费令牌） |
| 安全与权限 | 15 / 15（全部只查询和计算） |
| 文档 | 10 / 10 |
| 许可证 | 5 / 5 |
| **合计** | **86** |
