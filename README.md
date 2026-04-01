# 每周教育政策资讯聚合器

一个全自动化的教育政策与资讯聚合平台，聚焦职业教育与本科教育领域。

## 功能特点

- **多源聚合**: 教育部、人社部、各省教育局、主流媒体
- **自动分类**: 基于关键词评分的智能分类（职业教育/本科教育/政策/资讯）
- **实时搜索**: 客户端模糊搜索，无需服务器
- **自动更新**: GitHub Actions 每周定时抓取更新
- **静态部署**: GitHub Pages 免费托管，零服务器成本

## 数据来源

### 国家级政策
- 教育部 (moe.gov.cn)
- 人社部 (mohrss.gov.cn)

### 省级政策
- 各省教育局（陆续接入）

### 媒体资讯
- 新华网教育
- 人民网教育

### EdTech 厂商资讯
- 中教畅享
- 博导前程
- 超星
- 智慧树

## 技术栈

| 层级 | 技术 |
|------|------|
| 爬虫 | Python 3.10 + Playwright |
| 内容提取 | newspaper3k + BeautifulSoup |
| 中文分词 | jieba |
| 前端 | Vanilla JS (ES6+) |
| 搜索 | Fuse.js |
| 调度 | GitHub Actions |
| 托管 | GitHub Pages |

## 项目结构

```
edu-policy-aggregator/
├── .github/workflows/     # GitHub Actions
├── src/scraper/           # Python 爬虫模块
├── frontend/               # 前端页面
├── data/                   # 生成的数据文件
└── requirements.txt        # Python 依赖
```

## 本地开发

### 1. 克隆仓库

```bash
git clone <repo-url>
cd edu-policy-aggregator
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium --with-deps
```

### 4. 运行爬虫

```bash
python -m src.scraper.main
```

### 5. 本地预览前端

使用 VS Code Live Server 或任意 HTTP 服务器：

```bash
cd frontend
python -m http.server 8080
# 访问 http://localhost:8080
```

## 部署

### GitHub Pages + Actions

1. 将仓库推送到 GitHub
2. 在仓库 Settings > Pages 中启用 GitHub Pages
3. 选择 `gh-pages` 分支（或 main 分支）
4. GitHub Actions 将自动每周执行爬虫并部署

### 手动触发更新

在 GitHub 仓库的 Actions 页面，点击 "Weekly Education Policy Scrape" 工作流，然后点击 "Run workflow"。

## 内容分类规则

### 加分关键词
- 职业教育、高职、职业院校: +3
- 本科、高等院校、本科院校: +3
- 高校: +2
- 产教融合、技能人才: +2

### 减分关键词
- 中小学、义务教育、幼儿园: -10
- 学前教育、初中、小学: -5

最终得分 > 0 且不在排除列表 → 收录

## License

MIT
