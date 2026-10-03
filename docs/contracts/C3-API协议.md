# C3 API 契约 · 门户后端接口协议

> 状态：草案 → **2026-10-04 冻结**
> 统一约定：所有接口返回 `{code, message, data}` 包裹；`code=0` 成功
> 错误码段：1001 参数错误 / 2001 未登录 / 2002 无权限 / 2004 资源不存在 / 5000 服务端错误

| 方法 | 路径 | 用途 | 关键入参 | 关键出参 | 对应需求 |
|---|---|---|---|---|---|
| POST | /api/auth/register | 注册（5 类信息 + 隐私提示） | phone, nickname, user_type, org, reason | token, user | R01 |
| POST | /api/auth/login | 登录 | phone, code | token, user | R01 |
| GET | /api/documents | 列表 + 文件名检索 | q, category, year, page, page_size | total, items[Document] | R02 R03 R07 |
| GET | /api/documents/{doc_id} | 文档详情 | - | Document + related[] | R08 |
| POST | /api/documents/{doc_id}/download | 下载（并计数） | - | file_url | R09 |
| POST | /api/ask | **AI 问答（代理 WeKnora，唯一 AI 入口）** | question, session_id | answer, citations[{doc_id, title, snippet}] | R05 R06 |
| POST | /api/events | 埋点上报 | event, props | ok | R04 |
| GET | /api/stats/summary | 看板聚合数据 | date_range | 按 C4 事件聚合的指标 | R04 |
| POST | /api/upload | 用户提交文件（进审核队列） | file, meta | ticket_id | R11 |
| POST | /api/feedback | 反馈提交 | content, contact | ok | R12 |

## 关键约束

- `/api/ask` 是门户**唯一**暴露的 AI 入口；前端永远不直连 WeKnora
- 引擎变更只改 `backend/app/rag_proxy.py` 一处
- Document 结构以 C2 字段映射表为准
- 接口负责人：待按任务领取情况补充
