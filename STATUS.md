# DirBridge 当前状态

更新时间：2026-09-18

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

## 审稿补充实验进度（2026-09-18）

| 实验 | 对应意见 | 状态 | 记录 |
|---|---|---|---|
| E1 公平调参 + 异常诊断 | R3-3、R1-D2 | dev 120/120 完成；正式仅 CIFAR-10 CA2FL 5 seed 完成 | `e1-fair-tuning/DESIGN_AND_RESULTS.md` + `REPLY_DRAFT.md` |
| E2 在线初始化 | R3-1 | 完成，60/60 审计通过；code_e2 已合并回主树 | `e2-online-init/DESIGN_AND_RESULTS.md` |
| E4 profile 耦合 | R3-2、R1-D7 | 完成，70/70 审计通过 | `e4-profile-coupling/DESIGN_AND_RESULTS.md` + `RESOURCE_AUDIT_AND_SCOPE.md` |
| E5 (B, K₀, dₛ) 敏感性 | R1-D4/D6、R2-5 | 完成，65/65 审计通过 | `e5-sensitivity/DESIGN_AND_RESULTS.md` |

E1 的关键结论与限制：CA2FL 与 FADAS 的异常都是**配置性**的（server 步长 /
自适应分母失效），调参后 CA2FL 从 5 seed 全 10.00 恢复到均值 49.47；但
DirBridge 的 +22.67 分配对 CI 为 [−4.43, +49.77]，**不显著**，原因是调参后
CA2FL 的 seed 方差（±19.73）是 DirBridge（±3.58）的 5.5 倍。FEMNIST 正式
与 CIFAR-10 的 FedBuff/FADAS 正式跑未完成，不可外推。逃生时间优势已撤回。

原始数据与完整日志在台式机 `/home/jczn2/DirBridge_state/{e2,e4,e5}_{runs,logs}/`（仓库外）。
E1（统一调参 + CA2FL/FADAS 异常诊断）、E3（耦合强度扫描）、E6（内存账本重述）未开始。
E6 的核心证据（CA2FL 缓存在设备内存 0.984/0.916 实测预测比）已由 E4 资源审计提前给出。
