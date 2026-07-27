# Cloud Glyph Skills

## 职责

严格遵循该SKILL定义的工作流，产出符合规范的Wiki文档

## 变量约定

> CloudGlyph_Git:[https://github.com/Axvser/CloudGlyph][ReadOnly][Template Repository] - Cloud Glyph 仓库地址

> CloudGlyph_Child_Git:[request] - 本地Wiki仓库根目录，该Wiki仓库是基于Cloud Glyph:[Template Repository]创建的独立仓库，自身不计入Wiki分析或编写

> Project_Root:[request] - 待文档化的项目的根目录

> MainSKILL_Path:[CloudGlyph_Child_Git/skills/SKILL.md] - 当前技能所在路径

> Wiki_Root:[CloudGlyph_Child_Git/src/CloudGlyph/Assets/Docs/content/{languages}/] - 产出文档的根目录，按language划分的动态变量，例如编写英语时，它就是CloudGlyph_Child_Git/src/CloudGlyph/Assets/Docs/content/en/，Agent仅允许在Wiki_Root下编辑文档内容

> LanguageMap_List:[CloudGlyph_Child_Git/src/CloudGlyph/Assets/Docs/config/languages.json] - Wiki支持语言的范围

> LanguageTargets_List:[request] - 用户希望Wiki支持的语言范围

## 结构约定

⚙ {ID}_{PageName}/ - 产出Markdown时采取的文件夹命名规则，文件夹构成的树结构就是最终App渲染Wiki时看到的目录结构

⚙ index.md - 每个{ID}_{PageName}/下都必须有且仅有一个固定名称的index.md文件，否则将导致目录结构不完整，md文件可留白，可以加更多子目录表示子项

⚙ 输出路径下的**每一个**目录都必须包含 index.md——包括中间父目录，不仅限于叶子目录。创建新的子目录后，立即确认该路径的每一级祖先目录都有 index.md。常见错误是创建了例如 `2_设计模式/0_工作流/index.md` 但遗忘了 `2_设计模式/index.md`。

最终，目录会呈现下述结构，这是四个固定的维度，而/.../意味着允许你在遵循规范的前提下，基于具体功能划分，自行延展子项并添加内容，无深度限制

> Wiki_Root/0_欢迎/

> Wiki_Root/1_快速开始/.../

> Wiki_Root/2_API/.../

> Wiki_Root/3_SE分析/.../

> Wiki_Root/4_版权/.../

## 编码风格约定

⚙ 在编写 Wiki 代码块前，扫描【Project_Root】下的源文件检测项目的主导缩进风格（TAB 或 空格+宽度），生成的代码块缩进必须与其匹配。检测有歧义时 .NET/C# 项目默认使用 **4 空格**。

⚙ 从源文件（Demo / Test / 源码）提取代码片段时，保留其原有的空白风格，不要做 TAB 与空格之间的转换。

## 可访问性约定

⚙ 尊重源代码中明确标记为非public的内容，避免在Wiki中暴露这些内容

⚙ 避免在Wiki中暴露敏感信息，如密码、密钥、个人信息等

## 工作流

> 0.开始

> 1.变量确认

> 2.功能发现

> 3.编写【快速入门】

> 4.编写【API参考】

> 5.编写【SE分析】

> 6.编写【版权】

> 7.编写【欢迎页】

> 8.审批

> 9.结束

## 技能索引

<!-- SKILL_INDEX -->
