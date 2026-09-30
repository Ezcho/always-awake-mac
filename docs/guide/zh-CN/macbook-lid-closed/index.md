Source: https://no-sleep-pika.online/guide/zh-CN/macbook-lid-closed/
Language: zh-CN

[← 使用指南](https://no-sleep-pika.online/guide/)

no-sleep-pika

# 如何让 MacBook 合上盖子后继续运行

合上屏幕，继续工作。先区分外接显示器办公与只保留后台任务这两种需求。

no-sleep-pika · 2026-10-01

只保留后台任务**打开 pika → Session ON → Monitor OFF → 合上盖子**

盖子打开时，切换 Session 或 Monitor 不会立即关闭或锁定屏幕。

## 合盖是关机还是睡眠？

MacBook 合盖通常会进入睡眠，而不是完全关机。重新打开后应用还在，不代表下载、构建或 AI 任务在此期间持续运行。屏幕关闭、屏幕锁定和系统睡眠是不同状态。

[Apple 官方说明](https://support.apple.com/en-gb/guide/mac-help/mh10330/mac)

## 是否使用外接显示器？

如果要在外接屏幕上继续工作，请先检查 Mac 支持的合盖模式，连接显示器、键盘和鼠标。这种用途可能不需要额外的防睡眠应用。Apple Silicon Mac 如提示批准配件连接，请在合盖前完成；电源及显示器配置要求请查阅对应机型说明。

[Apple 官方说明](https://support.apple.com/en-us/102282)

## 使用 pika 保持后台任务运行

- 从首页下载完整 PKG，安装后在“应用程序”中打开 pika，确认辅助服务已连接。

- 启动需要运行的任务，然后将 Session 切换为 ON。

- 不需要显示器时，将 Monitor 保持为 OFF。只有 Session 开启时才能选择 Monitor。

- 合上盖子后，pika 才应用合盖后的屏幕设置。请放在通风良好的桌面上使用。

- 任务结束后将 Session 切换为 OFF，恢复 pika 管理的睡眠设置。Monitor 也显示 OFF，但不会立即关闭屏幕。

## 如何确认任务没有暂停

先做一次短测试：记录任务进度或日志时间，开启 Session 后合盖，稍后打开并查看合盖期间是否有进展。出现锁屏不等于任务停止。若应用正在等待输入或登录，pika 无法代替操作。关闭控制窗口只会隐藏窗口；菜单栏图标被遮挡时，可从“应用程序”重新打开控制窗口。

## 电池、温度与网络限制

电量不足或 macOS 热状态达到保护阈值时，pika 可能结束会话。合盖且未连接外接显示器时使用更保守的阈值，但这不代表可以安全地放在密闭包内运行。防睡眠不能保证 Wi-Fi、VPN 或远程 API 连接；长任务应使用工具自身的重试和检查点功能。当前下载没有 Developer ID 签名或公证，macOS 可能阻止安装。请在自己的系统和设备上验证。

[更多安装、连接和排障步骤 · English →](https://no-sleep-pika.online/guide/)

## 如何让 MacBook 合上盖子后继续运行

pika 是一款 macOS 菜单栏应用，通过 Session 和 Monitor 两个开关控制。支持 macOS 13 及以上版本、Apple Silicon 和 Intel。

[下载 pika →](https://no-sleep-pika.online/zh-CN/)[安装帮助（英语）](https://no-sleep-pika.online/install/)[MCP 连接指南（英语）](https://no-sleep-pika.online/guide/#mcp)
