# Finance Project Agent Instructions

本项目是本地优先的个人宏观数据监控系统。

- Python 代码遵循 PEP 8，使用类型注解；公开 API 写 docstring。
- 注释使用中文，解释业务原因，不重复代码字面意思。
- 公用常量放在 `backend/constant.py`。
- 本地路径、API Key、数据库路径通过环境变量或配置传入，不写死绝对路径。
- 新增环境变量时同步更新 `env.example` 和 `README.md`。
- 数据源适配器要实现 `backend.domain.providers.MacroDataProvider`。
- 有测试时先写 pytest，再实现。
- 进展、教训、提交记录、后续事项写入 `PREGRESS.md`。
- 图表布局必须按用户指定的业务行对齐；同类指标放在同一行，不同子类不要混排。
- 不同类型图表必须使用不同绘制风格，通过 `chart_style` 等显式字段区分，避免只靠频率自动猜。
