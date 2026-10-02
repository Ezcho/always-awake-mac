Source: https://no-sleep-pika.online/guide/zh-TW/keep-mac-awake/
Language: zh-TW

MAC GUIDE · 2026-10-02

# 讓 Mac 不進入睡眠的方法：闔蓋模式、caffeinate 與 pika

比較接上電源的闔蓋模式、終端機 caffeinate 指令與 pika 安裝，說明關閉螢幕、鎖定與系統睡眠的差別，以及使用條件和結束方式。

## 先依工作選擇方法

螢幕關閉、畫面鎖定和系統睡眠是不同狀態。鎖定時可能仍在工作；喚醒後視窗存在，也不能證明工作一直執行。外接螢幕工作先考慮闔蓋模式；開蓋的短期工作可用 caffeinate；沒有外接螢幕的闔蓋工作可考慮 pika 與輔助服務。

## 1. 電源與闔蓋模式

開蓋時接上電源、支援的外接顯示器、鍵盤與滑鼠，確認可操作後再闔蓋。能供電的顯示器是否可代替充電器需依規格確認。只插充電器並不是完整的闔蓋配置。顯示器數量與解析度依 Mac 型號而異，配件連接要求應先在開蓋時批准。

[Apple · External displays](https://support.apple.com/en-us/102501)

## 開蓋時檢查 macOS 設定

開蓋並接電時，在系統設定的電池選項尋找顯示器關閉時防止自動睡眠的設定。名稱和位置依 macOS 版本與機種而異。可以保留鎖定密碼，不必一直亮屏。這不是所有闔蓋睡眠的通用解法；記錄原設定以便恢復。

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. 用 caffeinate 暫時防止睡眠

開啟終端機輸入下方指令。macOS 內建 caffeinate，不需 sudo 或額外安裝。它防止閒置造成的系統睡眠，螢幕仍能關閉。保留該程序，在相同終端機按 Control+C 即可停止。沒有輸出而等待是正常狀態；程序結束後要求也會解除。

```
caffeinate -i
```

## 依時間、螢幕與指令設定

第一個例子維持 3,600 秒（一小時）；第二個同時防止螢幕睡眠，持續 1,800 秒（半小時）。不需亮屏可省略 -d。第三個實際執行 make，到該指令結束為止。只在準備編譯的專案中使用；會立即退出的背景啟動器可能比真正工作更早結束。指定工作指令時 -t 不生效。

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## caffeinate 能阻止闔蓋睡眠嗎？

-i 針對系統閒置睡眠，-d 針對螢幕睡眠。闔蓋屬於另一條件，不代表外接螢幕需求已被取代。-s 只在 AC 電源下有效；-u 表示使用者活動，可能喚醒螢幕。不要把任意旗標組合當成所有 Mac 的闔蓋保證。

## 3. 安裝 pika

pika 支援 macOS 13 以上、Apple Silicon 與 Intel。從官方下載完整 PKG，安裝應用程式和管理員輔助服務，由使用者完成 macOS 認證與必要批准。開啟 /Applications/pika.app，確認服務連線，開啟 Session、按需關閉 Monitor，再闔蓋。睡眠防止先準備，畫面策略於闔蓋後套用。開蓋時改 Monitor 只儲存選擇。Session OFF 恢復管理的設定，不會立刻關閉螢幕；關閉視窗不等於結束程式。

[下載 pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[安裝說明](https://no-sleep-pika.online/install/)

## 確認進度並結束

先用短工作記錄開始時間，再測試闔蓋或關屏，之後檢查日誌和進度。這是自行驗證步驟，不代表所有機型都已測試。pmset -g assertions 只讀取當前要求，不能證明網路或闔蓋期間持續運作。man caffeinate 可查看本機說明。

```
pmset -g assertions
```

```
man caffeinate
```

## 鎖定、網路與發熱

鎖定不等於睡眠。Wi-Fi、VPN、API 限額、等待批准或程式錯誤可能中斷工作，pika 不會自動接續 AI 對話或恢復網路。運作中請放在通風的硬質平面，不要放進袋子。電池與熱保護或服務問題可能結束 Session；不能保證防止所有過熱與電力耗盡。

## 資料來源與範圍

本文由 no-sleep-pika 開發者撰寫並介紹自家應用程式，參考 Apple 資料、macOS 的 caffeinate(8) 手冊與 pika 1.0.13 公開實作。並非 Apple 或 AI 供應商背書。選擇適合情境的方法，完成後解除防睡眠。

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

由 no-sleep-pika 開發者撰寫，包含自家產品。

[下載 pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[MacBook 闔蓋指南 →](https://no-sleep-pika.online/guide/zh-TW/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/zh-TW/keep-mac-awake/index.md)
