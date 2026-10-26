# Reflex AI 独立训练存档补丁（中文说明）

> 这是一个 **Java 源码补丁**，不是完整 Fabric 模组，也不是可放入 `mods` 文件夹的 JAR。

## 功能范围

- 首次启动时打开 Minecraft 自带的“创建世界”界面。
- 预填世界名称 `Reflex AI Training`。
- 主菜单提供“Reflex AI 训练存档”按钮，可再次打开创建界面。
- 只有实际进入通过该流程创建的世界后，才写入首次引导标记。
- 不会静默创建世界，也不会主动删除、重命名或覆盖其他存档。

## 应用补丁

1. 先备份你的测试实例中的 `.minecraft/saves` 和 `.minecraft/config`。
2. 将本补丁文件夹中的 `ReflexAiClient.java` 与 `apply-save-flow-patch.ps1` 放在同一目录。
3. 在 PowerShell 中运行：
   `./apply-save-flow-patch.ps1 -ProjectRoot "D:\你的完整源码项目路径"`
4. 脚本会先检查目标路径，并拒绝把补丁覆盖到自身。
5. 如果目标文件与补丁一致，脚本会直接结束，不创建多余备份；否则会创建带毫秒时间戳的备份，暂存新文件并校验 SHA-256，再替换目标。
6. 此脚本只修改源码；它不会运行 Gradle、编译 JAR 或安装模组。

请确保目标项目与补丁使用的 Minecraft/Fabric API 版本相匹配。不确定时先不要覆盖文件，检查备份与源码路径。

## 自动静态检查

在仓库根目录运行：

```sh
python3 tools/check_save_flow_patch.py
```

当前检查覆盖 21 项静态条件，包括训练世界名称、首次标记写入顺序、取消流程、Java 分隔符平衡、脚本自覆盖保护、重复应用检查、暂存文件校验和备份行为。

## 仍需手动验证

静态检查不等于成功编译，也不等于游戏内测试。请参考 [SAVE-FLOW-TEST-PLAN.md](SAVE-FLOW-TEST-PLAN.md)，在独立的备份测试实例中检查首次启动、取消后重试、手动按钮和旧存档保护。

**当前状态：没有经过验证的新版 JAR。** 本仓库目前只保存存档引导补丁及其检查材料，不包含完整模组源码。


## 完整源码与归档来源审计

解压目录中的客户端入口与本补丁逐字节一致，但同名 `ReflexAI-Fabric-3.4.0-source.zip` 内的客户端文件不同，不能视为同一快照。请查看 [SOURCE-INTEGRATION-AUDIT.md](SOURCE-INTEGRATION-AUDIT.md) 和 [BUILD-READINESS-REPORT.md](BUILD-READINESS-REPORT.md)，并运行 `python3 tools/audit_source_provenance.py /path/to/ReflexAI-Fabric-3.4.0 /path/to/ReflexAI-Fabric-3.4.0-source.zip` 做只读比对。该工具不会编译或测试模组。

来源审计回归测试：`python3 tools/test_source_provenance_audit.py`。

## 补丁包完整性校验

`PATCH-BUNDLE-MANIFEST.sha256` 记录纯源码补丁包内文件的哈希。运行 `python3 tools/verify_patch_bundle.py` 校验清单中的文件，运行 `python3 tools/test_verify_patch_bundle.py` 检查篡改是否会被发现。哈希校验不代表模组已编译或通过游戏测试。
