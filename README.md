# Trump Skill

与 Trump 对话的 Claude Code 技能。使用 Trump 真实的语录和说话风格进行回复。

## 安装

```bash
ln -s /path/to/trump-skill ~/.claude/skills/trump
```

## 使用

```
/trump [消息]
```

例如：
```
/trump 你觉得美国经济怎么样？
/trump 谈谈中国
/trump 媒体都是假新闻
```

## 项目结构

```
trump-skill/
├── SKILL.md              # 技能入口
├── prompts/
│   ├── trump_persona.md  # Trump 人格定义
│   └── persona_analyzer.md  # 语料分析流程
├── tools/
│   ├── quote_db.py       # 语录数据库
│   └── scraper.py        # 语录收集脚本
├── data/
│   └── trump_quotes.db   # 语录数据库 (177条)
└── requirements.txt
```

## 语录来源

语录来自 Trump 的公开演讲、采访、Twitter/Truth Social、辩论等，按主题分类：
- china, trade, media, biden, election
- immigration, economy, energy, healthcare
- foreign, politics, maga, self, famous

## 扩展语录

```bash
# 编辑 scraper.py 添加更多语录
# 然后重新运行
python tools/scraper.py
```

## 技术栈

- Python 3
- SQLite
