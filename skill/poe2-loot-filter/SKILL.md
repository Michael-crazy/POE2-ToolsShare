---
name: poe2-loot-filter
description: Edit local Path of Exile 2 loot filters (.filter), highlight gear for a BD or build, adapt filters to new seasons, retier drops using market prices, or optimize and deploy a filter in the game directory after user approval. Supports 文子过滤 seven tiers and other local PoE2 filters.
---

# PoE2 过滤器

按请求读取对应说明。手动编辑和交付检查见 [editing.md](references/editing.md)，BD 装备高亮另读 [build-gear.md](references/build-gear.md)，赛季升级另读 [season.md](references/season.md)，价格更新另读 [market.md](references/market.md)。可组合执行。先定位用户指定的原文件和档位，多个候选且意图不明确时确认目标。赛季和价格任务确认目标区服、赛季，价格任务还要确认软核或硬核。

保留原文件，交付带清楚名称的候选副本和变更摘要。直接优化游戏目录内的过滤器或准备覆盖时，按 [游戏目录部署](references/game-deploy.md) 执行，覆盖前取得用户对具体候选版和文件清单的同意。通过相对路径定位资源，复用已有规则风格、顺序、编码、换行和中文注释。

更新前按 [七档用途与等级范围](references/filter-tiers.md) 确定目标范围，逐档保留等级门槛和拾取策略。市集调价与赛季升级分别确认范围。用户明确要求整套时，处理全部目标档位。最近加载的文件可用于识别当前档位。

用户本地没有可用过滤器时，按 [下载基础过滤器](references/base-filter.md) 获取文子七档和配套音效，再按用途选择档位并核对目标客户端版本。

运行本 Skill 内的只读检查：

    python scripts/check_filter.py --sound-root "<包含音效子目录的目录>" "<原文件>" "<候选文件>"

脚本路径相对于 Skill 目录。配置和迁移资料只记录相对路径及其根目录角色。实档如存在 UTF-8 之外的编码，先识别并传入 --encoding。脚本检查有限的结构、关键字和音效引用。处理变更涉及的规则顺序、游戏版本支持和物品数据，再按 editing.md 验证。报告实际验证层级和未解决问题。
