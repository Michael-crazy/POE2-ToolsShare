---
name: poe2-loot-filter
description: Edit local Path of Exile 2 loot filters (.filter), highlight gear for a BD or build, adapt filters to new seasons, and retier drops using China or international market prices. Supports 文子过滤 seven tiers and other local PoE2 filters.
---

# PoE2 过滤器

按请求读取对应说明。手动编辑和交付检查见 [editing.md](references/editing.md)，BD 装备高亮另读 [build-gear.md](references/build-gear.md)，赛季升级另读 [season.md](references/season.md)，价格更新另读 [market.md](references/market.md)。可组合执行。先定位用户指定的原文件和档位，多个候选且意图不明确时确认目标。赛季和价格任务确认目标区服、赛季，价格任务还要确认软核或硬核。

保留原文件，交付带清楚名称的候选副本和变更摘要。按请求才安装到游戏目录或覆盖文件。通过同目录相对路径定位资源，音效根目录可单独指定。复用已有规则风格、顺序、编码、换行和中文注释。

运行本 Skill 内的只读检查：

    python scripts/check_filter.py --sound-root "<包含音效子目录的目录>" "<原文件>" "<候选文件>"

脚本路径相对于 Skill 目录，输入可以用绝对路径。实档如存在 UTF-8 之外的编码，先识别并传入 --encoding。脚本检查有限的结构、关键字和音效引用。处理变更涉及的规则顺序、游戏版本支持和物品数据，再按 editing.md 验证。报告实际验证层级和未解决问题。
