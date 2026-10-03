#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量创建 widework-v2 任务池 Issue。"""
import subprocess, json, sys

REPO = "a3230038469/widework-v2"

def issue(title, labels, body):
    args = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body", body]
    for l in labels:
        args += ["--label", l]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("FAIL", title, r.stderr.strip()[:200], flush=True)
        return None
    url = r.stdout.strip().splitlines()[-1]
    print("OK", url, title, flush=True)
    return url

T = []

# ============ F0 地基 ============
T.append(("[F0-01] 仓库骨架与目录边界说明", ["F0地基","P0","难度/易"], """
## 任务说明
把仓库目录骨架补齐并写清"哪个目录归哪个板块"，让所有人一眼知道自己的活该放哪。

## 交付物
- 根目录 `STRUCTURE.md`（每行：目录 → 归属板块 → 谁可写）
- 若发现骨架缺目录，在 Issue 里说明，由集成负责人补

## 验收标准（3 例）
1. `STRUCTURE.md` 覆盖 frontend/backend/content/deploy/stats/docs 六目录
2. 每个目录写明"可写角色"，与 CONTRIBUTING.md 第五节红线一致
3. 新人只读这一份就能判断某文件该放哪

## 接口依赖
无（本任务只出文档）

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F0-02] CI 守门：提交规范 + 目录边界 + 契约收口三项检查", ["F0地基","P0","难度/中"], """
## 任务说明
写 GitHub Actions workflow，在每次 PR 上自动检查三件事，不合规就标红。

## 交付物
- `.github/workflows/guard.yml`
- 检查项 ①：提交信息必须含 `#数字`（任务号）
- 检查项 ②：不得提交 `node_modules/` `dist/` `.env` `.env.*`
- 检查项 ③：`backend/` 中 `weknora` 字样只允许出现在 `app/rag_proxy.py`
- 检查项 ④：`frontend/` 中不得出现内网地址（`127.0.0.1` `localhost` `内网 IP` 形式）

## 验收标准（3 例）
1. 故意用一个不带任务号的提交发 PR → CI 报红，且报错信息说明原因
2. 故意提交一个 `.env` 文件 → CI 报红
3. 正常 PR（提交带 #号、只动自己目录）→ CI 绿灯

## 接口依赖
读 `CONTRIBUTING.md` 第三节、第五节

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F0-03] Mock Server：让前后端并行开工不等彼此", ["F0地基","P0","难度/中"], """
## 任务说明
按 C3 契约做一个假后端（Mock Server），返回结构正确的假数据，让前端不等后端就能开工。

## 交付物
- `backend/mock/server.py`（或 Node 版，任选其一，说明选型理由）
- `backend/mock/README.md`：怎么启动、覆盖了哪些接口

## 覆盖接口（按 C3 契约返回结构）
- `GET /api/documents`（返回 8 条假文档，字段照 C2）
- `GET /api/documents/{doc_id}`
- `POST /api/documents/{doc_id}/download`
- `POST /api/ask`（返回假 answer + 2 条 citations）

## 验收标准（3 例）
1. 启动后 `curl /api/documents` 返回 `{code:0, data:{total, items[...]}}`，items 里字段与 C2 完全一致
2. 假数据覆盖三种 category（研究报告/政策法规/案例工具）便于前端测筛选
3. README 里三步能跑起来（装依赖 → 启动 → 访问）

## 接口依赖
严格按 `docs/contracts/C2-字段映射表.md`、`docs/contracts/C3-API协议.md` 实现

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F0-04] 前端工程脚手架（Vue3 + Vite + Element Plus）", ["F0地基","P0","难度/中"], """
## 任务说明
搭好前端工程，让领页面任务的人 clone 下来就能直接写页面。

## 交付物
- `frontend/package.json`、`vite.config.js`、`index.html`
- `frontend/src/main.js`、`frontend/src/App.vue`、`frontend/src/router/index.js`
- `frontend/src/api/request.js`：统一请求封装，baseURL 从环境变量读（默认指向 Mock）
- `frontend/README.md`：装依赖 → 启动 → 切 Mock/真后端 的方法

## 验收标准（3 例）
1. `npm install && npm run dev` 能起本地服务，浏览器打开不报错
2. 路由已配好占位页（首页/检索/文档详情/登录），访问路径能切换
3. `request.js` 里 baseURL 改一处即可切 Mock / 真后端

## 接口依赖
C3 契约（统一响应 `{code,message,data}`，code=0 成功）

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F0-05] 后端工程脚手架（FastAPI + 统一响应包裹）", ["F0地基","P0","难度/中"], """
## 任务说明
搭好后端工程骨架，让领接口任务的人直接往里加路由。

## 交付物
- `backend/app/main.py`、`backend/requirements.txt`
- `backend/app/core/response.py`：统一 `{code,message,data}` 包裹 + 错误码常量
- `backend/app/core/errors.py`：1001/2001/2002/2004/5000 五个错误码的抛出方式
- `backend/app/routers/__init__.py`（占位）
- `backend/README.md`：启动命令（uvicorn）、自带 /docs 说明

## 验收标准（3 例）
1. `uvicorn app.main:app` 起得来，访问 `/docs` 能看到接口文档页
2. 造一个 400 响应，返回体是 `{code:1001, message:"参数错误", data:null}`
3. 抛异常时返回 `{code:5000, ...}` 而不是裸 500 堆栈

## 接口依赖
C3 契约统一约定与错误码段

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F0-06] rag_proxy 粘合层：全仓库唯一对接 WeKnora 的文件", ["F0地基","P0","难度/难"], """
## 任务说明
写 `backend/app/rag_proxy.py`——门户后端唯一允许出现 WeKnora 地址的地方，把 C3 的 `/api/ask` 映射到引擎接口。

## 交付物
- `backend/app/rag_proxy.py`
- 引擎地址从环境变量读（`WEKNORA_BASE_URL`），不硬编码
- 出参严格映射为 `{answer, citations[{doc_id,title,snippet}]}`

## 验收标准（3 例）
1. 引擎不可用时返回 `{code:5000,...}` + 明确 message，前端能展示"AI 暂时不可用"
2. 出参 citations 字段名与 C3 完全一致（doc_id/title/snippet）
3. 用 grep 确认全仓库 `weknora` 字样只出现在本文件（大小写不敏感）

## 接口依赖
C3 契约 `/api/ask`；上游为 F3 引擎任务

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))

# ============ F1 前端 ============
F1 = [
 ("F1-01","首页","R01 R02","易","""
## 任务说明
做首页：产品一句话介绍 + 搜索框（最显眼）+ 四大分类入口 + 登录/注册按钮 + 底部免责声明。

## 交付物
- `frontend/src/pages/home/` 目录下全部文件（含路由注册）

## 验收标准（3 例）
1. 375px 宽度下搜索框完整可见、不被遮挡（PRD 4.1 硬标准）
2. 点分类卡片跳到检索结果页并带上 category 参数
3. 未登录时右上角显示"登录/注册"，登录后显示昵称

## 接口依赖
C3：`GET /api/documents?category=` ；埋点 C4：`page_view_home`
Mock 已就绪，无需等待
"""),
 ("F1-02","登录与注册页","R01","中","""
## 任务说明
做登录/注册页：注册表单含 5 类信息（手机号、昵称、身份类型、所属机构、使用目的）+ 隐私提示。

## 交付物
- `frontend/src/pages/login/` 目录下全部文件

## 验收标准（3 例）
1. 正确信息注册 → 成功跳首页并显示昵称
2. 缺必填项 → 前端提示且不发请求
3. 手机号重复注册 → 显示后端返回的错误提示（不裸奔错误码）

## 接口依赖
C3：`POST /api/auth/register`（phone, nickname, user_type, org, reason）、`POST /api/auth/login`（phone, code）
埋点 C4：`login_success`
"""),
 ("F1-03","书架式分类展示页","R02","中","""
## 任务说明
做书架页：按四大分类（研究报告/政策法规/案例工具/各类标准）分区展示文档卡片，卡片显示标题/来源/年份。

## 交付物
- `frontend/src/pages/kb/` 目录下全部文件

## 验收标准（3 例）
1. 覆盖 400+ 文档时列表能分页加载，不一次性全渲染
2. 分类为空时显示 Empty 态（不是白屏）
3. 点卡片进入文档详情页，带对 doc_id

## 接口依赖
C3：`GET /api/documents?category=&page=`；C2 字段 doc_id/title/category/source/year
"""),
 ("F1-04","检索与结果页","R03","中","""
## 任务说明
做检索页：输入关键词 → 只按**文件名**匹配（PRD 明确不做全文检索）→ 结果列表带高亮。

## 交付物
- `frontend/src/pages/search/` 目录下全部文件

## 验收标准（3 例）
1. 输入关键词回车 → 列表显示匹配结果，命中词高亮
2. 零结果 → 显示兜底提示并引导去 AI 问答（PRD 4.1：零结果兜底触发率 100%）
3. 关键词为空提交 → 不发请求，给提示

## 接口依赖
C3：`GET /api/documents?q=`；埋点 C4：`search_submit`、`search_zero_result`
"""),
 ("F1-05","分类筛选与排序","R07","中","""
## 任务说明
在检索/书架页加筛选器：按 category、topic、year 筛选，按年份排序。

## 交付物
- `frontend/src/pages/search/` 下的筛选组件（或独立组件目录）

## 验收标准（3 例）
1. 选多个筛选条件 → 结果同时满足，条件回显在页面上
2. 点"清空筛选" → 恢复全量列表
3. 筛选无结果 → 显示 Empty 态并提示清空条件

## 接口依赖
C3：`GET /api/documents?category=&year=`；C2 字段 category/topic/year
"""),
 ("F1-06","文档详情页","R08","中","""
## 任务说明
做文档详情页：展示元数据（C2 字段）+ 在线预览 PDF + 下载按钮 + 相关推荐。

## 交付物
- `frontend/src/pages/doc/` 目录下全部文件

## 验收标准（3 例）
1. PDF 能在线预览不下载（PDF.js）
2. 下载按钮点击后触发下载并计数（走 C3 download 接口）
3. 元数据缺失字段（如 year 为空）显示"—"而不是 undefined

## 接口依赖
C3：`GET /api/documents/{doc_id}`、`POST /api/documents/{doc_id}/download`
埋点 C4：`doc_preview`、`doc_download`
"""),
 ("F1-07","AI 问答页","R05 R06","难","""
## 任务说明
做 AI 问答页：提问框、答案区（带引用来源可点开原文）、多轮对话、等待态。

## 交付物
- `frontend/src/pages/ask/` 目录下全部文件

## 验收标准（3 例）
1. 提问后显示 answer + 引用列表，点引用能跳到对应文档
2. 题目模糊时（如"这个怎么办"）不报错，走正常问答流程（R06 模糊提问）
3. 无来源的答案不输出到界面（PRD 4.1：答案来源标注率 100%）

## 接口依赖
C3：`POST /api/ask`（question, session_id）→ answer, citations[{doc_id,title,snippet}]
埋点 C4：`ai_ask`、`ai_answer_view`
"""),
 ("F1-08","图书馆员登录界面（平台原生 R05-A）","R01 R05-A","易","""
## 任务说明
为 R10 双平台对比准备一个"平台原生方案"的入口页（用 WorkBuddy 原生能力问答），与自研 RAG 形成对比。

## 交付物
- `frontend/src/pages/librarian/` 目录下全部文件
- 页面上要有明显说明："本页为双平台对比验证用"

## 验收标准（3 例）
1. 页面能正常渲染并提交问题
2. 与 AI 问答页在视觉上可区分（避免用户混淆）
3. 页面文案说明这是实验性入口

## 接口依赖
R10 相关；具体对接方式如不确定，在 Issue 里提问
"""),
 ("F1-09","用户反馈区","R12","易","""
## 任务说明
做反馈表单：反馈内容 + 联系方式（选填），提交后给成功提示。

## 交付物
- `frontend/src/pages/feedback/` 目录下全部文件（或作为组件嵌入详情页）

## 验收标准（3 例）
1. 内容为空提交 → 前端提示不发请求
2. 提交成功 → 显示成功提示并清空表单
3. 提交失败 → 显示可重试提示，不丢用户已填内容

## 接口依赖
C3：`POST /api/feedback`（content, contact）
"""),
 ("F1-10","全局组件：导航栏 / 页脚 / 免责声明 / 三态组件","R08","中","""
## 任务说明
把全站共用的组件抽出来：顶部导航、页脚、常驻免责声明条、Loading/Empty/Error 三态占位组件。

## 交付物
- `frontend/src/components/` 目录下全部文件 + 使用说明

## 验收标准（3 例）
1. 三态组件各有默认文案，页面可直接 `<Loading/><Empty/><Error/>` 使用
2. 免责声明文案与 PRD 一致（"答案由 AI 依据库内资料生成，仅供参考，不构成法律或政策意见；请以原文为准"）
3. 导航栏在 375px 下不横向溢出

## 接口依赖
无接口；文案取自 PRD
"""),
 ("F1-11","移动端适配与首屏体检","R08","中","""
## 任务说明
全站移动端走查：375px 宽度下逐页检查、修复溢出与遮挡，输出体检报告。

## 交付物
- `docs/移动端体检报告.md`（逐页：问题 + 修复前后）
- 对应的样式修复代码（改动落在各页面目录内）

## 验收标准（3 例）
1. 首页/检索/详情/问答四页在 375px 下无横向滚动条
2. 搜索框与主按钮在首屏完整可见
3. 报告里每页至少给出 1 条具体发现（含修复说明）

## 接口依赖
无
"""),
]
for code, name, reqs, diff, body in F1:
    T.append((f"[{code}] {name}开发", ["F1前端","P0" if code in ("F1-01","F1-02","F1-03","F1-04","F1-06","F1-07") else "P1", f"难度/{diff}"],
              body + f"\n\n## 对应需求\nPRD {reqs}\n\n## 领取方式\nassign 自己 + 标签改「状态/进行中」+ 评论\"我认领\"\n"))

# ============ F2 后端 ============
F2 = [
 ("F2-01","auth 接口组：注册与登录","R01","中","""
## 任务说明
实现 `POST /api/auth/register` 与 `POST /api/auth/login`。

## 交付物
- `backend/app/routers/auth.py` + 单元测试

## 验收标准（3 例）
1. 正确注册返回 `{code:0, data:{token, user}}`
2. 缺参数返回 `code:1001`
3. 手机号已存在返回明确业务错误（不泄露是否为已注册用户以外信息）

## 接口依赖
C3 契约 auth 两接口；C2 字段
"""),
 ("F2-02","documents 接口组：列表/详情/下载计数","R02 R03 R07 R08 R09","中","""
## 任务说明
实现文档三接口：列表（含文件名检索与筛选）、详情、下载（计数）。

## 交付物
- `backend/app/routers/documents.py` + 单元测试

## 验收标准（3 例）
1. `?q=xx` 只按 title 模糊匹配（不做全文检索），返回 `total + items[]`
2. `?category=&year=` 组合筛选结果正确
3. 下载接口返回 `file_url` 并把计数 +1（可通过再次查询统计验证）

## 接口依赖
C3 契约；C2 字段（items 里字段名必须完全一致）
"""),
 ("F2-03","events 接口组：埋点接收与落库","R04","易","""
## 任务说明
实现 `POST /api/events`，接收前端埋点并落库，供看板聚合。

## 交付物
- `backend/app/routers/events.py` + 单元测试 + 表结构说明

## 验收标准（3 例）
1. 上报合法事件返回 `{code:0}`
2. 事件名不在 C4 表里 → 返回 `code:1001` 并说明原因
3. 落库字段能支撑"按事件名 + 日期聚合"查询

## 接口依赖
C4 契约 8 个事件名；C3 契约
"""),
 ("F2-04","stats 接口组：看板聚合","R04","中","""
## 任务说明
实现 `GET /api/stats/summary`，按 C4 事件聚合出看板指标。

## 交付物
- `backend/app/routers/stats.py` + 单元测试

## 验收标准（3 例）
1. 支持 `date_range` 参数，返回该区间各指标
2. 指标口径与 PRD §8.2 一致（零结果率、下载转化率等）
3. 区间内无数据时返回 0 而不是 null/报错

## 接口依赖
C3 /api/stats/summary；C4 事件表
"""),
 ("F2-05","upload 接口组：用户提交文件进审核队列","R11","中","""
## 任务说明
实现 `POST /api/upload`：接收用户提交的文件 + 元数据，写入待审队列，返回工单号。

## 交付物
- `backend/app/routers/upload.py` + 单元测试

## 验收标准（3 例）
1. 合法文件 + 元数据 → 返回 `ticket_id`，状态为待审
2. 超出大小/格式限制 → `code:1001` 并说明限制
3. 元数据缺必填字段（按 C2）→ 拒绝并指出缺哪个

## 接口依赖
C3 /api/upload；C2 字段（提交的元数据需满足必填项）
"""),
 ("F2-06","feedback 接口组：反馈提交与查询","R12","易","""
## 任务说明
实现 `POST /api/feedback`：接收反馈内容与联系方式并落库。

## 交付物
- `backend/app/routers/feedback.py` + 单元测试

## 验收标准（3 例）
1. 内容非空 → 返回 `{code:0}`
2. 内容为空 → `code:1001`
3. 联系方式选填，不传也能成功

## 接口依赖
C3 /api/feedback
"""),
]
for code, name, reqs, diff, body in F2:
    T.append((f"[{code}] {name}", ["F2后端","P0" if code in ("F2-01","F2-02","F2-03") else "P1", f"难度/{diff}"],
              body + f"\n\n## 对应需求\nPRD {reqs}\n\n## 领取方式\nassign 自己 + 标签改「状态/进行中」+ 评论\"我认领\"\n"))

# ============ F3 引擎 ============
F3 = [
 ("F3-01","部署 WeKnora（锁定 v0.8.2）","R05","中","""
## 任务说明
照官方文档用 Docker 把 WeKnora 跑起来，锁定版本号。

## 交付物
- `deploy/weknora/docker-compose.yml`（锁定 v0.8.2）
- `deploy/weknora/部署记录.md`：步骤、踩坑、截图位置

## 验收标准（3 例）
1. 一台干净机器照文档能跑起来（30 分钟内）
2. 管理界面能登录进去
3. 引擎只监听内网，不直接暴露公网

## 接口依赖
无（上游无依赖，是 F3 其他任务的前置）
"""),
 ("F3-02","引擎接入百炼 Qwen 与 Embedding","R05","易","""
## 任务说明
在 WeKnora 里配置大模型走阿里云百炼（Qwen 对话 + Embedding），不在本地跑模型。

## 交付物
- `deploy/weknora/模型配置说明.md`（含字段含义，**不要写具体密钥**）

## 验收标准（3 例）
1. 问答能走通并返回答案
2. 文档向量化用的是百炼 Embedding（不是本地）
3. 说明文档里用占位符代替密钥，不出现真实 key

## 接口依赖
依赖 F3-01 完成
"""),
 ("F3-03","知识库建立与 400+ 文档批量导入","R05","中","""
## 任务说明
建知识库，把 400+ 份资料批量导入，验证解析效果。

## 交付物
- `deploy/weknora/导入记录.md`（导入数量、失败清单、原因）
- 批量导入脚本（若用到）

## 验收标准（3 例）
1. 导入成功率记录清楚，失败文件列出并说明原因
2. PDF/Word 两类格式都能被解析出正文（抽 5 份人工看）
3. 导入后管理界面能按文件名搜到

## 接口依赖
依赖 F3-01、F4 的元数据清单
"""),
 ("F3-04","问答质量调参（切片/检索配比）","R05 R06","中","""
## 任务说明
调切片大小与混合检索配比，让答案质量达标。

## 交付物
- `deploy/weknora/调参记录.md`（每次调整 + 对比结果）

## 验收标准（3 例）
1. 10 个典型问题测试：答案有引用、可点开原文
2. 零结果有兜底提示
3. 记录里能看出"改了什么 → 结果怎么变"

## 接口依赖
依赖 F3-03
"""),
 ("F3-05","生成 scoped API Key 供后端调用","R05","易","""
## 任务说明
给 F2 的 rag_proxy 发一个作用域受限的 API Key，说明怎么配置到门户后端。

## 交付物
- `deploy/weknora/API对接说明.md`（Key 怎么配到环境变量 `WEKNORA_BASE_URL` 与密钥变量）

## 验收标准（3 例）
1. 说明里明确指出 Key 只能通过环境变量注入，不能进代码仓库
2. F2 的 rag_proxy 能按此说明调通
3. 说明里给出撤销/轮换 Key 的步骤

## 接口依赖
依赖 F3-01；被 F0-06 依赖
"""),
]
for code, name, reqs, diff, body in F3:
    T.append((f"[{code}] {name}", ["F3引擎","P0" if code in ("F3-01","F3-02") else "P1", f"难度/{diff}"],
              body + f"\n\n## 对应需求\nPRD {reqs}\n\n## 领取方式\nassign 自己 + 标签改「状态/进行中」+ 评论\"我认领\"\n"))

# ============ F4 内容 ============
T.append(("[F4-01] 内容元数据清洗脚本", ["F4内容","P1","难度/中"], """
## 任务说明
写脚本：把基金会导出的 Excel/CSV 清洗成符合 C2 字段规范的标准数据。

## 交付物
- `content/scripts/clean_metadata.py`
- `content/README.md`：输入输出格式说明

## 验收标准（3 例）
1. 400+ 份全量跑通，输出字段与 C2 一字不差
2. 抽样 20 份人工核对无误
3. 异常数据（缺必填项）不静默丢弃，输出到待处理清单

## 接口依赖
C2 字段映射表（输出格式的唯一依据）

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F4-02] 字段映射核对：基金会分类 → C2 四分类", ["F4内容","P1","难度/中"], """
## 任务说明
把基金会 Excel 里现有的分类，映射到 C2 的四大类（研究报告/政策法规/案例工具/各类标准）。

## 交付物
- `content/字段映射核对表.md`（原分类 → 目标分类 → 待人工确认项）

## 验收标准（3 例）
1. Excel 里出现过的每个分类都有归处
2. 无法自动归类的列出并标"待确认"
3. 结论反馈到 C2 的「待确认」清单，供 10/4 冻结

## 接口依赖
C2 字段映射表（含待确认项）

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F4-03] 文件命名规范与内容缺口清单模板", ["F4内容","P2","难度/易"], """
## 任务说明
定文件命名规范（去公文外壳、保留原文件名用于检索），并做《内容缺口清单》模板。

## 交付物
- `content/命名规范.md`
- `content/内容缺口清单-模板.md`

## 验收标准（3 例）
1. 命名规范给出 before/after 例子（至少 3 个）
2. 规范与 C2 的 title 字段定义一致（title 是检索匹配的唯一对象）
3. 缺口清单模板可按月填写（PRD 4.1：每月一份）

## 接口依赖
C2 字段映射表

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))

# ============ F5 看板 ============
T.append(("[F5-01] Umami 自托管部署", ["F5看板","P1","难度/中"], """
## 任务说明
用 Docker 把 Umami 跑起来（无 Cookie、隐私友好），接入站点。

## 交付物
- `stats/umami/docker-compose.yml`
- `stats/umami/部署说明.md`

## 验收标准（3 例）
1. Umami 后台能登录并看到站点统计
2. 站点脚本已接入（页面能上报 page_view）
3. 说明写清"无 Cookie"配置项在哪

## 接口依赖
无

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F5-02] 数据看板页（消费 stats 接口）", ["F5看板","P1","难度/中"], """
## 任务说明
做 `/admin/dashboard` 看板页，展示 C4 八事件聚合出的指标。

## 交付物
- `stats/dashboard/` 前端页面代码

## 验收标准（3 例）
1. 8 个事件在页面上都能看到对应数字
2. 支持日期区间切换
3. 无数据时显示 0 与空态提示，不是报错

## 接口依赖
C3：`GET /api/stats/summary`；C4：8 个事件名

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))

# ============ F6 部署 ============
T.append(("[F6-01] 根目录 docker-compose 一键编排", ["F6部署","P1","难度/中"], """
## 任务说明
写根目录 `docker-compose.yml`：门户 + 引擎 + 统计一次起。

## 交付物
- `docker-compose.yml`
- `deploy/README.md`

## 验收标准（3 例）
1. 一台干净服务器 `docker compose up -d` 全起
2. 各服务依赖顺序正确（引擎先于门户）
3. 端口不冲突，只暴露必要端口

## 接口依赖
依赖 F1/F2/F3/F5 的产物

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F6-02] Nginx 反代与 HTTPS", ["F6部署","P1","难度/中"], """
## 任务说明
配 Nginx 反代 + Let's Encrypt 证书，实现 HTTPS。

## 交付物
- `deploy/nginx/` 配置
- `deploy/https说明.md`

## 验收标准（3 例）
1. 域名访问自动跳 HTTPS
2. 证书能自动续期
3. 门户与引擎的路由分离正确（引擎不暴露公网）

## 接口依赖
依赖 F6-01

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F6-03] 备份脚本", ["F6部署","P2","难度/易"], """
## 任务说明
写数据库与文档的定时备份脚本。

## 交付物
- `deploy/backup.sh` + 说明

## 验收标准（3 例）
1. 脚本能手动跑通并产出备份文件
2. 支持保留最近 N 份、自动清理旧备份
3. 说明里写清怎么恢复

## 接口依赖
无

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))
T.append(("[F6-04] 上线手册（30 分钟从零到可访问）", ["F6部署","P1","难度/中"], """
## 任务说明
写《上线手册》：新机器 → 可访问站点，全程照手册无口头补充。

## 交付物
- `deploy/上线手册.md`

## 验收标准（3 例）
1. 演练一次：照手册走完能访问站点
2. 手册里每条命令可直接复制执行
3. 列出常见失败与排查方法（至少 3 条）

## 接口依赖
依赖 F6-01、F6-02

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))

# ============ F7 ============
T.append(("[F7-01] 双平台并行验证对比报告（R10）", ["F0地基","P0","难度/中"], """
## 任务说明
用 WorkBuddy 平台原生方案与自研 WeKnora 方案跑同一批问题，产出对比报告。

## 交付物
- `docs/双平台对比报告.md`（同一批问题两边的答案质量、引用能力、延迟、成本）

## 验收标准（3 例）
1. 同一批问题（≥10 个）在两边都跑过
2. 对比维度至少含：答案准确度、是否有引用、响应延迟
3. 结论明确说明自研方案是否达标、遗留问题

## 接口依赖
依赖 F1-08（平台原生入口页）、F3 引擎可用

## 领取方式
assign 自己 + 标签改「状态/进行中」+ 评论"我认领"
"""))

print(f"\n共 {len(T)} 个任务待创建", file=sys.stderr)
ok = 0
for title, labels, body in T:
    if issue(title, labels, body.strip()):
        ok += 1
print(f"\n创建完成：{ok}/{len(T)}", file=sys.stderr)
