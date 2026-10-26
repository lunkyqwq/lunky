# 本地完整源码对接审计

## 发现

本次工作区中找到 `ReflexAI-Fabric-3.4.0-source.zip` 和解压后的 `ReflexAI-Fabric-3.4.0/`。归档 ZIP 完整性检查通过，包含 29 个文件。

完整项目中的客户端入口：

`src/main/java/com/example/reflexai/client/ReflexAiClient.java`

与本补丁中的 `patches/save-flow-3.4.1/ReflexAiClient.java` 逐字节一致，SHA-256 均为：

`1a4fbbcb6f927f7ad1d4d40b4379996cfeb3686ca56c112ac71e25121ab555dd`

因此，这份 3.4.0 完整源码**已经包含**本补丁的训练存档引导代码，不应再次覆盖或重复应用。

## 如何复查

在 Python 3 环境下，从补丁仓库根目录运行：

```sh
python3 tools/audit_local_source.py /path/to/ReflexAI-Fabric-3.4.0
```

脚本会检查关键项目文件、比较两个客户端源码的 SHA-256，并报告是否完全一致。脚本只读，不会修改源码，也不会运行 Gradle。

## 重要限制

- 源码文件一致只证明存档引导代码已存在，不证明项目能成功编译。
- 本轮没有运行 Gradle 构建，也没有启动 Minecraft 1.21.11 进行游戏内测试。
- 本仓库仍是独立补丁与审计工具仓库，不是完整模组源码仓库，也不包含可安装 JAR。
