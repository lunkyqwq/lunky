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
4. 脚本会先为原客户端 Java 文件创建带时间戳的备份，再复制补丁文件。
5. 此脚本只修改源码；它不会运行 Gradle、编译 JAR 或安装模组。

请确保目标项目与补丁使用的 Minecraft/Fabric API 版本相匹配。不确定时先不要覆盖文件，检查备份与源码路径。

## 自动静态检查

在仓库根目录运行：

```sh
python3 tools/check_save_flow_patch.py
```

当前检查覆盖 16 项静态条件，包括训练世界名称、首次标记写入顺序、取消流程、Java 分隔符平衡、脚本备份行为和测试清单内容。

## 仍需手动验证

静态检查不等于成功编译，也不等于游戏内测试。请参考 [SAVE-FLOW-TEST-PLAN.md](SAVE-FLOW-TEST-PLAN.md)，在独立的备份测试实例中检查首次启动、取消后重试、手动按钮和旧存档保护。

**当前状态：没有经过验证的新版 JAR。** 本仓库目前只保存存档引导补丁及其检查材料，不包含完整模组源码。
