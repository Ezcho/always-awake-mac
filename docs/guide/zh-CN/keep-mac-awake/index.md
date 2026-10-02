Source: https://no-sleep-pika.online/guide/zh-CN/keep-mac-awake/
Language: zh-CN

MAC GUIDE · 2026-10-02

# 让 Mac 不进入睡眠的方法：合盖模式、caffeinate 与 pika

比较接通电源的合盖模式、终端 caffeinate 命令和 pika 安装。说明屏幕关闭、锁屏与系统睡眠的区别，以及各方法的条件和退出步骤。

## 先选择适合任务的方法

屏幕关闭、锁屏和系统睡眠并不相同。锁屏时任务可能仍在运行，唤醒后窗口仍在也不能证明任务一直在执行。外接显示器办公可先用合盖模式；开盖的临时任务可用 caffeinate；不接外屏的合盖后台工作可考虑带辅助服务的 pika。

## 1. 接通电源并使用合盖模式

先在开盖状态连接电源、受支持的外接显示器、键盘和鼠标，确认能正常使用后再合盖。支持供电的显示器可能代替单独充电器，需查看规格。只接充电器并不构成这一配置。外屏数量和分辨率取决于 Mac 型号；出现配件连接请求时应先在开盖状态批准。

[Apple · External displays](https://support.apple.com/en-us/102501)

## 开盖时检查 macOS 电源设置

开盖并连接电源时，可在系统设置的电池选项中寻找显示器关闭时防止自动睡眠的设置。名称和位置随系统及型号变化。可以保留锁屏密码要求，而不必一直亮屏。此设置并非合盖睡眠的通用覆盖。记录原设置以便完成后恢复。

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. 使用 caffeinate 临时防止睡眠

打开终端运行下面命令。macOS 自带 caffeinate，无需额外安装或 sudo。它阻止因空闲导致的系统睡眠；屏幕仍可关闭。保持该终端进程运行，在同一终端按 Control+C 结束。没有输出而等待是正常现象，这不是重启后仍保留的永久设置。

```
caffeinate -i
```

## 按时间、屏幕和任务选择命令

第一个例子维持 3,600 秒，即一小时；第二个同时防止屏幕睡眠，持续 1,800 秒，即半小时。不需要亮屏就省略 -d。第三个会实际运行 make，并在该命令结束时释放请求，只在确实准备编译的项目中使用。立即退出的后台任务启动器可能比真实任务先结束。指定运行命令时 -t 不生效。

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## caffeinate 能阻止合盖睡眠吗？

-i 针对系统空闲睡眠，-d 针对屏幕睡眠。合盖是另一种条件，不能把这些选项当成无需外屏就能合盖运行的保证。-s 仅在交流电源下有效；-u 表示用户活动，可能唤醒屏幕。应理解选项含义，不要盲目组合参数。

## 3. 安装 pika 并控制 Session

pika 支持 macOS 13 及以上、Apple Silicon 和 Intel。下载官方完整 PKG，安装应用和管理员辅助服务，并由用户完成 macOS 身份认证与必要的安全批准。打开 /Applications/pika.app，确认服务连接，开启 Session，按需关闭 Monitor，然后合盖。系统防睡眠会提前准备，屏幕策略在合盖后应用。开盖时切换 Monitor 只保存选择。关闭 Session 会恢复 pika 管理的设置，但不会立即熄屏；关闭窗口也不会退出应用。

[下载 pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[安装帮助](https://no-sleep-pika.online/install/)

## 确认任务继续并结束会话

先用短任务记录开始时间，按实际需求合盖或熄屏，之后检查日志时间和进度。这是建议的自测步骤，并非声称已测试所有型号。pmset -g assertions 只读取当前防睡眠请求，不能证明网络或合盖连续性。man caffeinate 可查看本机说明。

```
pmset -g assertions
```

```
man caffeinate
```

## 锁屏、网络和发热问题

锁屏不等于任务停止。网络、VPN、API 限额、等待批准或应用崩溃都可能单独中断任务，pika 不会代替 AI 继续对话或恢复连接。运行中的 Mac 应放在通风的硬质表面，不要装进包里。电池或热保护、辅助服务故障可能结束会话；保护功能不能保证防止所有过热或耗尽。

## 资料来源与范围

本文由 no-sleep-pika 开发者撰写，包含自家应用。依据 Apple 官方资料、本机 caffeinate(8) 手册及 pika 公开版 1.0.13 的文档与实现，不代表 Apple 或 AI 服务提供商推荐。按使用场景选择方法，并仅在需要期间保持运行。

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

由 no-sleep-pika 开发者撰写，包含自家应用的比较。

[下载 pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[MacBook 合盖指南 →](https://no-sleep-pika.online/guide/zh-CN/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/zh-CN/keep-mac-awake/index.md)
