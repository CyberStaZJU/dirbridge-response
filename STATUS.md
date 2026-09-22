# DirBridge 当前状态

更新时间：2026-09-22

## 当前结论

已将 `dirbridge-artifact-main.zip` 解压到本目录。压缩包包含 61 个文件，覆盖算法、模型、数据读取、配置、复现实验脚本和结果汇总工具。本地目录此前为空，因此当前代码基线来自该压缩包。

GitHub 公共仓库 `CyberStaZJU/dirbridge-artifact` 的公开结构与压缩包一致：均以 `main_fed.py` 为入口，包含 `algorithm/`、`builders/`、`data_reader/`、`models/`、`utils/`、`ds/`、`scripts/`、`configs/`、`artifacts/` 和数据选择文件。已核对的远端最新提交为 `53027ae`（Add reproducibility environment and table scripts）。

通过 SSH 检查了台式机 `$DIRBRIDGE_ROOT`。该目录不是 Git 仓库；其实际代码在 `$DIRBRIDGE_CODE_ROOT`，共有 67 个文件，并包含额外算法（如 FedAsync、FedAC、SAW、MASFL、OR-MO）、CelebA/GLUE 数据读取器、NPU 运行脚本和已有分析结果。它与 GitHub/压缩包不是同一版本或同一目录布局：台式机版本更大、功能更丰富，GitHub/压缩包则是经过整理的 61 文件 artifact 子集。因此结论是“三方不一致”，不能直接把任一版本当作另一版本的精确副本。

## 项目组成

- 训练入口：`main_fed.py`。
- 算法：`algorithm/` 中实现 DirBridge 及六个对照方法，并由 `dispatcher.py` 调度。
- 数据与模型：`builders/`、`data_reader/`、`models/`；支持 CIFAR、FEMNIST、GSpeech，README 还列出 CIFAR-100 与 TinyImageNet。
- 实验配置：`configs/` 定义 Dir-Skew CIFAR 与 FedScale FEMNIST/GSpeech 的客户端数、并发数、缓冲区、轮数和种子。
- 复现与分析：`scripts/run_quick_smoke.sh`、`run_table1.sh` 至 `run_table6.sh`，以及 `ds/` 汇总脚本。

## 一致性检查

| 项目 | 结果 |
|---|---|
| 本地目录与压缩包 | 一致，已完成解压复制 |
| 当前 Mac 本地目录与 GitHub/压缩包 | 结构和核心文件一致 |
| 台式机 `$DIRBRIDGE_CODE_ROOT` 与 GitHub/压缩包 | 不一致：67 个文件、额外算法/数据集/工具/结果，且没有 Git 元数据 |
| 原始数据 | 未随仓库提供，需按 README 准备 |
| 当前实验结果 | 本地尚未发现可审核的实验输出 |

## 当前限制

共享对话页面标题为“审稿意见回复与实验补充”，但公开抓取没有返回正文内容；本状态基于压缩包、GitHub README 和仓库文件建立。若后续需要把共享对话中的具体审稿要求写入计划，应补充正文或截图。

## 审稿补充实验进度（2026-09-21）

| 实验 | 当前状态 | 记录 |
|---|---|---|
| E1 公平调参与异常诊断 | 早期 E1 记录已提交；后续 CIFAR-10/CIFAR-100 对照已补充；FedBuff mild alpha=0.1 新网格已暂停 | `e1-fair-tuning/` + `SUPPLEMENTAL_RESULTS_20260921.md` |
| E2 在线初始化 | 修复后的 online/full-warm 各 5 个 seed 均完成 500 rounds；accuracy 全部有限，配对差异未显示清晰优势，但两组均有 loss NaN 诊断记录 | `e2-online-init/` + `PUBLIC_ENTRYPOINT_AUDIT_20260922.md` + `CODE_CORRECTIONS_20260921.md` |
| E3 耦合强度扫描 | 暂停；无有效结果 | `e3-profile-coupling/STATUS.md` |
| E4 profile 耦合 | 70/70 审计通过 | `e4-profile-coupling/` |
| E5 (B, K0, ds) 敏感性 | 65/65 审计通过 | `e5-sensitivity/` |
| E6 资源账本 | 没有独立完成矩阵；仅有 E4 资源审计支持证据 | `e6-resource-accounting/STATUS.md` |

后续 CIFAR 对照的主要结论是条件性的：在合适的服务器步长下，FedBuff 与 DirBridge 在若干 CIFAR-10 设置下接近；CIFAR-100 的当前配置下 FedBuff 略高；high-skew CIFAR-10 的 tail-10 基本相同。当前不再声称 DirBridge 普遍提高最终 accuracy。

原始数据和完整日志仍保存在仓库外部；本仓库只保留轻量配置、代码、审计摘要和回复材料。所有未完成、被中止或只通过语法检查的内容都在补充文档中明确标记。
