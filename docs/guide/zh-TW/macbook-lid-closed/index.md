Source: https://no-sleep-pika.online/guide/zh-TW/macbook-lid-closed/
Language: zh-TW

[← 使用指南](https://no-sleep-pika.online/guide/)

no-sleep-pika

# 如何讓 MacBook 闔上蓋子後繼續執行

闔上螢幕，工作繼續。先區分外接顯示器操作與只保留背景工作這兩種需求。

no-sleep-pika · 2026-10-01

只保留背景工作**開啟 pika → Session ON → Monitor OFF → 闔上蓋子**

蓋子開啟時，切換 Session 或 Monitor 不會立即關閉或鎖定螢幕。

## 闔蓋是關機還是睡眠？

MacBook 闔蓋通常會進入睡眠，而不是完全關機。重新打開後 App 還在，不代表下載、建置或 AI 工作在此期間持續進行。螢幕關閉、螢幕鎖定與系統睡眠是不同狀態。

[Apple 官方說明](https://support.apple.com/en-gb/guide/mac-help/mh10330/mac)

## 有使用外接顯示器嗎？

若要在外接螢幕繼續操作，請先確認 Mac 支援的闔蓋模式，連接顯示器、鍵盤和滑鼠。這種用途可能不需要額外的防睡眠 App。Apple Silicon Mac 若要求允許配件連接，請在闔蓋前完成；電源與顯示器配置要求請查看對應機型說明。

[Apple 官方說明](https://support.apple.com/en-us/102282)

## 以 pika 維持背景工作

- 從首頁下載完整 PKG，安裝後從「應用程式」開啟 pika，確認輔助服務已連線。

- 啟動要執行的工作，將 Session 切換為 ON。

- 不需要顯示器時，讓 Monitor 保持 OFF。只有 Session 開啟時才能選擇 Monitor。

- 闔上蓋子後，pika 才套用闔蓋後的螢幕設定。請在通風良好的桌面使用。

- 工作結束後關閉 Session，還原 pika 管理的睡眠設定。Monitor 也會顯示 OFF，但不會立即關閉螢幕。

## 如何確認工作沒有暫停

先做短時間測試：記下進度或紀錄時間，開啟 Session 後闔蓋，稍後打開並查看闔蓋期間是否有進展。出現鎖定畫面不等於工作停止。若 App 等待輸入或登入，pika 無法代替操作。關閉控制視窗只會隱藏視窗；選單列圖示被擋住時，可從「應用程式」重新開啟控制視窗。

## 電池、溫度與網路限制

電量不足或 macOS 熱狀態達到保護門檻時，pika 可能結束階段。闔蓋且未連接外接顯示器時採用較保守的門檻，但這不代表能安全地在密閉包包中執行。防睡眠無法保證 Wi-Fi、VPN 或遠端 API 連線；長時間工作請搭配工具的重試與檢查點功能。目前下載沒有 Developer ID 簽章或公證，macOS 可能阻擋安裝。請在自己的系統與設備上確認。

[更多安裝、連線與疑難排解步驟 · English →](https://no-sleep-pika.online/guide/)

## 如何讓 MacBook 闔上蓋子後繼續執行

pika 是 macOS 選單列 App，以 Session 和 Monitor 兩個開關控制。支援 macOS 13 以上、Apple Silicon 與 Intel。

[下載 pika →](https://no-sleep-pika.online/zh-TW/)[安裝說明（英文）](https://no-sleep-pika.online/install/)[MCP 連線指南（英文）](https://no-sleep-pika.online/guide/#mcp)
