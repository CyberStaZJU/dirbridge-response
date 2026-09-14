# DirBridge 当前状态

更新时间：2026-09-14

## 当前结论

已将 `/Users/yibo/Downloads/dirbridge-artifact-main.zip` 解压到本目录。压缩包包含 61 个文件，覆盖算法、模型、数据读取、配置、复现实验脚本和结果汇总工具。本地目录此前为空，因此当前代码基线来自该压缩包。

GitHub 公共仓库 `CyberStaZJU/dirbridge-artifact` 的公开结构与压缩包一致：均以 `main_fed.py` 为入口，包含 `algorithm/`、`builders/`、`data_reader/`、`models/`、`utils/`、`ds/`、`scripts/`、`configs/`、`artifacts/` 和数据选择文件。已核对的远端最新提交为 `53027ae`（Add reproducibility environment and table scripts）。

通过 SSH 检查了台式机 `/home/jczn2/DirBridge`。该目录不是 Git 仓库；其实际代码在 `/home/jczn2/DirBridge/code`，共有 67 个文件，并包含额外算法（如 FedAsync、FedAC、SAW、MASFL、OR-MO）、CelebA/GLUE 数据读取器、NPU 运行脚本和已有分析结果。它与 GitHub/压缩包不是同一版本或同一目录布局：台式机版本更大、功能更丰富，GitHub/压缩包则是经过整理的 61 文件 artifact 子集。因此结论是“三方不一致”，不能直接把任一版本当作另一版本的精确副本。

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
| 台式机 `/home/jczn2/DirBridge/code` 与 GitHub/压缩包 | 不一致：67 个文件、额外算法/数据集/工具/结果，且没有 Git 元数据 |
| 原始数据 | 未随仓库提供，需按 README 准备 |
| 当前实验结果 | 本地尚未发现可审核的实验输出 |

## 当前限制

共享对话页面标题为“审稿意见回复与实验补充”，但公开抓取没有返回正文内容；本状态基于压缩包、GitHub README 和仓库文件建立。若后续需要把共享对话中的具体审稿要求写入计划，应补充正文或截图。
