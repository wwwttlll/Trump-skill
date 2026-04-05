# Trump Skill

与 Trump 对话的 Claude Code 技能。使用 Trump 真实的语录和说话风格进行回复。

## 功能

- **输入**: 用户消息
- **输出**: 以 Trump 风格回复，使用真实语录
- **集成**: Claude Code 斜杠命令 `/trump`
- **数据**: 177 条 Trump 语录，涵盖多个主题

## 安装

```bash
git clone https://github.com/wwwttlll/Trump-skill.git ~/.claude/skills/trump
```

或手动链接:

```bash
ln -s /path/to/Trump-skill ~/.claude/skills/trump
```

## 使用

在 Claude Code 中输入:

```
/trump 你觉得美国经济怎么样？
```

## 话题支持

- China & Trade (中国与贸易)
- Media (媒体与假新闻)
- Biden & Democrats (拜登与民主党)
- Elections (选举)
- Economy & Jobs (经济与就业)
- Immigration (移民)
- Foreign Policy (外交政策)
- MAGA

## 项目结构

```
Trump-skill/
├── SKILL.md              # 技能入口
├── prompts/
│   ├── trump_persona.md  # Trump 人格定义 (5层结构)
│   └── persona_analyzer.md  # 语料分析流程
├── tools/
│   ├── quote_db.py       # 语录数据库
│   └── scraper.py        # 语录收集脚本
└── data/
    └── trump_quotes.db   # SQLite 语录库
```

## 扩展语录

编辑 `tools/scraper.py` 添加更多语录，然后运行:

```bash
python tools/scraper.py
```

## 技术栈

- Python 3
- SQLite

## License

MIT
