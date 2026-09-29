#!/usr/bin/env python3
"""Build the dependency-free, localized GitHub Pages site. Run from any directory."""
from pathlib import Path
import html
import json
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs'
BASE = 'https://no-sleep-pika.online'
REPO = 'https://github.com/Ezcho/always-awake-mac'
# Keep this aligned with the published release, not the unreleased source version.
RELEASE = 'v1.0.3-mvp'
DOWNLOAD = f'{REPO}/releases/download/{RELEASE}/Always-Awake-1.0.3.dmg'
LANGUAGES = [('en','English'),('ko','한국어'),('zh-CN','简体中文'),('zh-TW','繁體中文'),('ja','日本語'),('hi','हिन्दी'),('id','Bahasa Indonesia'),('es','Español'),('fr','Français'),('de','Deutsch'),('pt-BR','Português'),('ru','Русский'),('ar','العربية'),('vi','Tiếng Việt'),('th','ไทย')]
KEYS = '''title description skip features connect download eyebrow headline intro source release compatibility scroll feature1 body1 feature2 body2 feature3 body3 controls controlstitle controlsbody window mcp mcptitle mcpbody buildstep addstep toolstep copy copied copyfail installation installtitle install1 install2 install3 limitation safety faq q1 a1 q2 a2 q3 a3 footer language screenshot buildlabel configlabel'''.split()
TEXT = {}
def add(locale, values):
    values = [line.strip() for line in values.strip().splitlines()]
    assert len(values) == len(KEYS), (locale, len(values), len(KEYS))
    TEXT[locale] = dict(zip(KEYS, values))

add('en', '''
no-sleep-pika — Mac sleep & display controls
Meet no-sleep-pika: a lightweight macOS menu bar app for session and display controls, with battery and thermal monitoring and an MCP interface for AI agents.
Skip to content
The app
Connect MCP
Download for Mac
A SMALL APP FOR LONGER SESSIONS
A little pika.<br>A longer session.
Session and display controls, right in your Mac’s menu bar. A quiet companion for work that takes a little longer.
View source
Public release 1.0.3 · macOS 13+ · Apple Silicon & Intel
Check installation requirements
Meet your night-shift companion
One session switch.
Start or stop a keep-awake session from the menu bar. Your work stays front and center.
Your screen, your choice.
Control the display while a session is active. Session OFF also resets and disables the Monitor switch; it does not immediately turn the screen off.
Mindful of your Mac.
Battery and macOS thermal-state monitoring can end a session at protective thresholds. Limits adapt to closed-lid, portable and desktop use.
SMALL BY DESIGN
Two switches.<br>Room to focus.
Open the controls when you need them. Close the window and pika stays in the menu bar.
Session · Monitor · That’s it.
READY FOR YOUR AGENT
Let your agent<br>flip the switch.
The MCP interface is in the source build. The public 1.0.3 download does not include it yet.
On a Mac with Xcode Command Line Tools, build the source, move dist/pika.app to /Applications, then open it. Standard mode does not require helper approval.
In Codex, open Settings → MCP servers. Add a STDIO server named pika with the command below. No arguments are needed.
After restarting the MCP server, your agent can check status and change Session or Monitor. Monitor requires an active session. Check sessionMode and lidClosedSupported with pika_status; standard mode keeps the Mac awake only with its lid open.
Copy
Copied
Select and copy the command
INSTALL & GET STARTED
A home in your menu bar.
Download the DMG and move the app to Applications. The current download may still be named Always Awake.
Open the app and follow the helper-service setup. Controls appear at launch; closing the window keeps the app running.
Turn Session on, then choose Monitor on or off. Remove the helper from the app’s settings before uninstalling.
The current download is not Developer ID signed or notarized. Depending on your system, macOS may block the app or its privileged helper. If installation or Session startup fails, follow the installation guidance on GitHub.
Closed-lid behavior depends on your Mac and macOS configuration. Thermal monitoring is not a temperature guarantee, and this app cannot guarantee safe operation inside a bag. Keep ventilation clear.
A few useful details
Does Monitor OFF stop my work?
During an active session, Monitor controls the display. Turning Session off also resets the Monitor switch to off and disables it, without immediately sleeping the display.
Which language does the website use?
On your first visit, we use your browser’s preferred language, with English as the fallback. Your choice is saved on this device. No IP-location lookup is used.
Is the source available?
Yes. Explore the code, installation requirements and MCP setup on GitHub. The website and app can evolve at different speeds; check the release notes before installing.
Small app. Longer sessions.
Choose language
The pika Mac app with Session and Monitor switches
Build from source
MCP command
''')
add('ko', '''
no-sleep-pika — Mac 잠자기·화면 제어
no-sleep-pika는 메뉴 막대에서 세션과 화면을 제어하는 가벼운 macOS 앱입니다. 배터리·열 상태 모니터링과 AI 에이전트용 MCP 인터페이스를 제공합니다.
본문으로 이동
앱 소개
MCP 연결
Mac용 다운로드
작은 앱, 더 긴 작업 시간
작은 피카.<br>조금 더 긴 작업.
Mac 메뉴 막대에서 세션과 화면을 간편하게 제어하세요. 시간이 더 필요한 작업 곁에 조용히 머뭅니다.
소스코드 보기
공개 버전 1.0.3 · macOS 13+ · Apple Silicon 및 Intel
설치 요구사항 확인
야근을 함께할 작은 친구
세션은 스위치 하나로.
메뉴 막대에서 잠자기 방지 세션을 시작하고 종료하세요. 하던 작업에 집중할 수 있습니다.
화면은 원하는 대로.
세션이 켜져 있을 때 화면을 제어하세요. Session을 끄면 Monitor 스위치도 꺼지고 비활성화됩니다. 실제 화면을 즉시 끄지는 않습니다.
Mac의 상태도 살피며.
배터리와 macOS 열 상태가 보호 기준에 도달하면 세션을 종료할 수 있습니다. 덮개 닫힘·휴대·데스크톱 사용 상태에 따라 기준이 달라집니다.
처음부터 가볍게
두 개의 스위치.<br>집중할 여유.
필요할 때만 제어창을 여세요. 창을 닫아도 피카는 메뉴 막대에 남아 있습니다.
Session · Monitor · 이것만 있으면 됩니다.
에이전트와 함께
스위치는<br>에이전트에게.
MCP 인터페이스는 소스 빌드에 포함되어 있습니다. 현재 공개된 1.0.3 다운로드에는 아직 포함되지 않았습니다.
Xcode Command Line Tools가 있는 Mac에서 소스를 빌드하고 dist/pika.app을 /Applications로 옮긴 뒤 실행하세요. 일반 모드에는 보조 서비스 승인이 필요 없습니다.
Codex의 설정 → MCP servers에서 pika라는 STDIO 서버를 추가하고 아래 명령어를 입력하세요. 별도 인수는 필요 없습니다.
MCP 서버를 다시 시작하면 에이전트가 상태를 확인하고 Session·Monitor를 제어할 수 있습니다. Monitor에는 활성 세션이 필요합니다. pika_status의 sessionMode와 lidClosedSupported를 확인하세요. 일반 모드는 덮개를 연 상태에서만 잠자기를 방지합니다.
복사
복사됨
명령어를 선택해 복사하세요
설치하고 시작하기
메뉴 막대가 피카의 집.
DMG를 다운로드하고 앱을 응용 프로그램으로 옮기세요. 현재 다운로드의 이름은 Always Awake로 표시될 수 있습니다.
앱을 열고 보조 서비스 설정을 진행하세요. 실행하면 제어창이 나타나며, 창을 닫아도 앱은 계속 실행됩니다.
Session을 켜고 Monitor를 선택하세요. 앱을 삭제하기 전에는 설정에서 보조 서비스를 제거하세요.
현재 다운로드는 Developer ID 서명·공증 전입니다. 시스템에 따라 macOS가 앱이나 권한이 필요한 보조 서비스를 차단할 수 있습니다. 설치 또는 Session 시작에 문제가 있으면 GitHub의 설치 안내를 확인하세요.
덮개를 닫았을 때의 동작은 Mac과 macOS 설정에 따라 다릅니다. 열 상태 감시는 특정 온도나 가방 안 사용의 안전을 보장하지 않습니다. 통풍을 확보하세요.
알아두면 좋은 것들
Monitor를 끄면 작업도 멈추나요?
활성 세션에서 Monitor는 화면을 제어합니다. Session을 끄면 Monitor 스위치도 꺼지고 비활성화되지만 실제 화면을 즉시 잠재우지는 않습니다.
웹사이트 언어는 어떻게 정하나요?
첫 방문 시 브라우저 선호 언어를 사용하고, 지원하지 않으면 영어로 표시합니다. 선택한 언어는 이 기기에 저장됩니다. IP로 위치를 조회하지 않습니다.
소스코드를 볼 수 있나요?
네. GitHub에서 코드·설치 요구사항·MCP 설정을 확인하세요. 웹사이트와 앱의 업데이트 시점이 다를 수 있으니 설치 전 릴리스 안내를 확인하세요.
작은 앱. 더 긴 작업 시간.
언어 선택
Session과 Monitor 스위치가 있는 pika Mac 앱
소스에서 빌드
MCP 명령어
''')
add('zh-CN', '''
no-sleep-pika — Mac 睡眠与显示控制
no-sleep-pika 是轻量级 macOS 菜单栏应用，提供会话与显示控制、电池和热状态监测，以及面向 AI 智能体的 MCP 接口。
跳转到正文
应用介绍
连接 MCP
下载 Mac 版
小巧应用，更长的工作时光
小小鼠兔。<br>陪你多做一会儿。
在 Mac 菜单栏轻松控制会话和屏幕。为需要更多时间的工作，留一个安静的伙伴。
查看源代码
公开版本 1.0.3 · macOS 13+ · Apple Silicon 与 Intel
查看安装要求
认识你的夜班伙伴
一个开关，管理会话。
在菜单栏启动或结束保持唤醒的会话，让注意力留在工作上。
屏幕，由你决定。
会话开启时可以控制屏幕。关闭 Session 会同时关闭并禁用 Monitor 开关，但不会立即关闭实际屏幕。
也关心 Mac 的状态。
电池和 macOS 热状态达到保护阈值时，可结束会话。阈值随合盖、便携和桌面使用状态调整。
从设计开始轻巧
两个开关。<br>更多专注空间。
需要时打开控制窗口。关闭窗口后，pika 仍在菜单栏待命。
Session · Monitor · 就这么简单。
为你的智能体准备好
让智能体<br>来拨动开关。
MCP 接口已包含在源码构建中。目前公开的 1.0.3 下载版尚未包含此功能。
在装有 Xcode Command Line Tools 的 Mac 上构建源码，将 dist/pika.app 移至 /Applications 后打开。标准模式无需批准辅助服务。
在 Codex 的 Settings → MCP servers 中添加名为 pika 的 STDIO 服务器，使用下方命令，无需参数。
重启 MCP 服务器后，智能体可查询状态并控制 Session 或 Monitor。Monitor 需要先开启会话。使用 pika_status 查看 sessionMode 和 lidClosedSupported；标准模式仅在盖子打开时保持 Mac 唤醒。
复制
已复制
请选择并复制命令
安装并开始
菜单栏里的小伙伴。
下载 DMG 并将应用移至“应用程序”。当前下载的名称可能仍为 Always Awake。
打开应用并完成辅助服务设置。启动时显示控制窗口；关闭窗口后应用继续运行。
开启 Session，再选择 Monitor 开或关。卸载前请在应用设置中移除辅助服务。
当前下载尚未使用 Developer ID 签名或公证。根据系统配置，macOS 可能拦截应用或特权辅助服务。如果安装或 Session 启动失败，请查看 GitHub 上的安装指南。
合盖后的行为取决于 Mac 和 macOS 配置。热状态监测不能保证特定温度，也不能保证放在包内运行的安全。请保持通风。
你可能想了解
关闭 Monitor 会停止工作吗？
会话开启时，Monitor 控制屏幕。关闭 Session 会将 Monitor 开关关闭并禁用，但不会立即让屏幕进入睡眠。
网站如何选择语言？
首次访问时采用浏览器偏好语言，不支持时显示英语。你的选择保存在此设备上，不通过 IP 查询位置。
源代码开放吗？
是的。可在 GitHub 查看代码、安装要求和 MCP 设置。网站和应用更新节奏可能不同，安装前请查看发布说明。
小巧应用，更长的工作时光。
选择语言
带有 Session 和 Monitor 开关的 pika Mac 应用
从源码构建
MCP 命令
''')
add('zh-TW', '''
no-sleep-pika — Mac 睡眠與螢幕控制
no-sleep-pika 是輕量 macOS 選單列應用程式，提供工作階段與螢幕控制、電池及熱狀態監測，以及 AI 代理用的 MCP 介面。
跳至主要內容
應用程式
連接 MCP
下載 Mac 版
小巧程式，更長的工作時光
小小鼠兔。<br>陪你多做一會兒。
在 Mac 選單列輕鬆控制工作階段與螢幕。為需要更多時間的工作，留一位安靜的夥伴。
查看原始碼
公開版本 1.0.3 · macOS 13+ · Apple Silicon 與 Intel
查看安裝需求
認識你的夜班夥伴
一個開關，管理工作階段。
從選單列啟動或結束保持喚醒的工作階段，把注意力留給工作。
螢幕，由你決定。
工作階段開啟時可控制螢幕。關閉 Session 也會關閉並停用 Monitor 開關，但不會立即關閉實際螢幕。
也關心 Mac 的狀態。
電池和 macOS 熱狀態達到保護門檻時，可結束工作階段。門檻會隨闔蓋、行動和桌面使用狀態調整。
從設計開始輕巧
兩個開關。<br>更多專注空間。
需要時打開控制視窗。關閉視窗後，pika 依然留在選單列。
Session · Monitor · 就這麼簡單。
為你的代理準備好
讓代理<br>來切換開關。
MCP 介面已包含在原始碼建置中。目前公開的 1.0.3 下載版尚未包含此功能。
在已安裝 Xcode Command Line Tools 的 Mac 上建置原始碼，將 dist/pika.app 移至 /Applications 後開啟。標準模式不需要核准輔助服務。
在 Codex 的 Settings → MCP servers 新增名為 pika 的 STDIO 伺服器，使用下方指令，無須引數。
重新啟動 MCP 伺服器後，代理可查詢狀態並控制 Session 或 Monitor。Monitor 需要先開啟工作階段。使用 pika_status 查看 sessionMode 和 lidClosedSupported；標準模式僅在上蓋開啟時保持 Mac 喚醒。
複製
已複製
請選取並複製指令
安裝並開始
選單列裡的小夥伴。
下載 DMG 並將程式移至「應用程式」。目前下載的名稱可能仍為 Always Awake。
開啟程式並完成輔助服務設定。啟動時顯示控制視窗；關閉視窗後程式會繼續執行。
開啟 Session，再選擇 Monitor 開或關。移除程式前，請先在設定中移除輔助服務。
目前下載尚未使用 Developer ID 簽署或公證。依系統設定，macOS 可能阻擋程式或特權輔助服務。如果安裝或 Session 啟動失敗，請參考 GitHub 的安裝指南。
闔蓋後的行為取決於 Mac 和 macOS 設定。熱狀態監測無法保證特定溫度，也無法保證放在包內執行的安全。請保持通風。
你可能想知道
關閉 Monitor 會停止工作嗎？
工作階段開啟時，Monitor 控制螢幕。關閉 Session 會關閉並停用 Monitor 開關，但不會立即讓螢幕進入睡眠。
網站如何選擇語言？
首次造訪時使用瀏覽器偏好語言，不支援時顯示英文。你的選擇保存在此裝置上，不會透過 IP 查詢位置。
原始碼公開嗎？
是的。可在 GitHub 查看程式碼、安裝需求和 MCP 設定。網站與程式更新步調可能不同，安裝前請查看版本說明。
小巧程式，更長的工作時光。
選擇語言
具有 Session 和 Monitor 開關的 pika Mac 應用程式
從原始碼建置
MCP 指令
''')
add('ja', '''
no-sleep-pika — Mac のスリープと画面をコントロール
no-sleep-pika は、セッションと画面の操作、バッテリーと熱状態の監視、AI エージェント向け MCP を備えた軽量 macOS メニューバーアプリです。
本文へ移動
アプリ
MCP 接続
Mac 版をダウンロード
小さなアプリで、もう少し長く
小さなナキウサギ。<br>もう少し、作業のそばに。
Mac のメニューバーからセッションと画面を操作。時間のかかる作業に、静かな相棒を。
ソースを見る
公開版 1.0.3 · macOS 13+ · Apple Silicon / Intel
インストール要件を見る
夜の作業の小さな相棒
セッションはスイッチひとつ。
メニューバーからスリープ防止セッションを開始・終了。目の前の作業に集中できます。
画面は、思いどおりに。
セッション中は画面を操作できます。Session をオフにすると Monitor もオフになり操作不可になりますが、画面がすぐに消えるわけではありません。
Mac の状態にも気を配る。
バッテリーと macOS の熱状態が保護しきい値に達すると、セッションを終了できます。しきい値は蓋を閉じた状態・携帯・デスクトップ利用に応じて変わります。
小ささを大切に
スイッチふたつ。<br>集中するための余白。
必要なときだけ操作ウィンドウを開く。閉じても pika はメニューバーに残ります。
Session · Monitor · それだけ。
エージェントとつながる
スイッチ操作は、<br>エージェントへ。
MCP はソースからのビルドで利用できます。現在公開中の 1.0.3 にはまだ含まれていません。
Xcode Command Line Tools を入れた Mac でソースをビルドし、dist/pika.app を /Applications へ移動して起動します。標準モードにヘルパーの承認は不要です。
Codex の Settings → MCP servers で、pika という STDIO サーバーを追加し、下のコマンドを入力します。引数は不要です。
MCP サーバーを再起動すると、エージェントが状態を確認し Session と Monitor を操作できます。Monitor には有効なセッションが必要です。pika_status の sessionMode と lidClosedSupported を確認してください。標準モードは蓋を開けた状態でのみスリープを防ぎます。
コピー
コピーしました
コマンドを選択してコピー
インストールして始める
メニューバーが、居場所です。
DMG をダウンロードし、アプリを「アプリケーション」へ移動。現在のダウンロードは Always Awake という名前の場合があります。
アプリを開いてヘルパーを設定します。起動時に操作ウィンドウが表示され、閉じてもアプリは動作を続けます。
Session をオンにしてから Monitor を選びます。アンインストール前に設定からヘルパーを削除してください。
現在のダウンロードは Developer ID 署名・公証前です。環境によって macOS がアプリや特権ヘルパーをブロックする場合があります。インストールや Session の開始に問題があれば、GitHub のインストール案内をご確認ください。
蓋を閉じたときの動作は Mac と macOS の設定によります。熱状態の監視は温度やバッグの中での安全な動作を保証しません。通気を確保してください。
知っておきたいこと
Monitor をオフにすると作業も止まりますか？
有効なセッションでは Monitor が画面を制御します。Session をオフにすると Monitor もオフになり操作不可になりますが、画面がすぐにスリープするわけではありません。
サイトの言語はどう決まりますか？
初回はブラウザの優先言語を使用し、非対応の場合は英語を表示します。選択はこの端末に保存されます。IP による位置検索は行いません。
ソースコードは公開されていますか？
はい。コード・インストール要件・MCP 設定は GitHub で確認できます。サイトとアプリの更新時期は異なる場合があります。インストール前にリリースノートをご確認ください。
小さなアプリ。もう少し長く。
言語を選択
Session と Monitor スイッチを備えた pika Mac アプリ
ソースからビルド
MCP コマンド
''')
add('hi', '''
no-sleep-pika — Mac की नींद और स्क्रीन का नियंत्रण
no-sleep-pika एक हल्का macOS मेनू बार ऐप है। सेशन और स्क्रीन नियंत्रण, बैटरी व तापीय स्थिति की निगरानी और AI एजेंट के लिए MCP इंटरफ़ेस।
मुख्य सामग्री पर जाएँ
ऐप
MCP जोड़ें
Mac के लिए डाउनलोड
छोटा ऐप, लंबे सेशन
नन्हा पिका।<br>काम के लिए थोड़ा और समय।
Mac के मेनू बार से सेशन और स्क्रीन नियंत्रित करें। समय लेने वाले काम के लिए एक शांत साथी।
सोर्स कोड देखें
सार्वजनिक संस्करण 1.0.3 · macOS 13+ · Apple Silicon और Intel
इंस्टॉल करने की ज़रूरतें देखें
रात के काम का छोटा साथी
सेशन के लिए एक स्विच।
मेनू बार से Mac को जागृत रखने वाला सेशन शुरू या बंद करें। ध्यान अपने काम पर रखें।
स्क्रीन पर आपका नियंत्रण।
सेशन चालू होने पर स्क्रीन नियंत्रित करें। Session बंद करने से Monitor स्विच भी बंद और निष्क्रिय हो जाता है, लेकिन असली स्क्रीन तुरंत बंद नहीं होती।
Mac की स्थिति का भी ख़याल।
बैटरी और macOS की तापीय स्थिति तय सुरक्षा सीमा तक पहुँचने पर सेशन समाप्त हो सकता है। सीमाएँ ढक्कन बंद होने, पोर्टेबल और डेस्कटॉप उपयोग के अनुसार बदलती हैं।
शुरू से हल्का
दो स्विच।<br>ध्यान लगाने की जगह।
ज़रूरत पर नियंत्रण विंडो खोलें। उसे बंद करने पर भी pika मेनू बार में रहता है।
Session · Monitor · बस इतना ही।
आपके एजेंट के लिए तैयार
स्विच का काम<br>एजेंट को दें।
MCP इंटरफ़ेस सोर्स से बने ऐप में उपलब्ध है। सार्वजनिक 1.0.3 डाउनलोड में यह अभी शामिल नहीं है।
Xcode Command Line Tools वाले Mac पर सोर्स बनाएँ, dist/pika.app को /Applications में ले जाएँ और खोलें। सामान्य मोड में सहायक सेवा की मंज़ूरी ज़रूरी नहीं है।
Codex में Settings → MCP servers खोलें। pika नाम का STDIO सर्वर जोड़कर नीचे दिया कमांड डालें। किसी आर्ग्युमेंट की ज़रूरत नहीं है।
MCP सर्वर दोबारा शुरू करने के बाद एजेंट स्थिति देख सकता है और Session या Monitor बदल सकता है। Monitor के लिए चालू सेशन ज़रूरी है। pika_status से sessionMode और lidClosedSupported देखें; सामान्य मोड केवल ढक्कन खुला होने पर Mac को जागृत रखता है।
कॉपी करें
कॉपी हो गया
कमांड चुनकर कॉपी करें
इंस्टॉल करें और शुरू करें
मेनू बार में एक घर।
DMG डाउनलोड करके ऐप को Applications में ले जाएँ। मौजूदा डाउनलोड का नाम अभी Always Awake हो सकता है।
ऐप खोलकर सहायक सेवा सेट करें। शुरू होने पर नियंत्रण विंडो दिखती है; विंडो बंद करने पर ऐप चलता रहता है।
Session चालू करें, फिर Monitor चुनें। ऐप हटाने से पहले उसकी सेटिंग से सहायक सेवा हटाएँ।
मौजूदा डाउनलोड Developer ID से हस्ताक्षरित या नोटराइज़्ड नहीं है। सिस्टम के अनुसार macOS ऐप या विशेषाधिकार वाली सहायक सेवा रोक सकता है। इंस्टॉल करने या Session शुरू करने में समस्या हो तो GitHub की इंस्टॉलेशन गाइड देखें।
ढक्कन बंद होने पर व्यवहार Mac और macOS की सेटिंग पर निर्भर है। तापीय निगरानी निश्चित तापमान या बैग के भीतर सुरक्षित उपयोग की गारंटी नहीं देती। हवा का रास्ता खुला रखें।
कुछ उपयोगी बातें
क्या Monitor बंद करने से काम रुक जाएगा?
चालू सेशन में Monitor स्क्रीन नियंत्रित करता है। Session बंद होने पर Monitor स्विच भी बंद और निष्क्रिय हो जाता है, लेकिन स्क्रीन तुरंत नहीं सोती।
वेबसाइट कौन-सी भाषा चुनती है?
पहली बार ब्राउज़र की पसंदीदा भाषा इस्तेमाल होती है। असमर्थित भाषा के लिए अंग्रेज़ी दिखाई जाती है। आपकी पसंद इसी डिवाइस पर सेव होती है। IP से स्थान नहीं खोजा जाता।
क्या सोर्स कोड उपलब्ध है?
हाँ। GitHub पर कोड, इंस्टॉल करने की ज़रूरतें और MCP सेटअप देखें। वेबसाइट और ऐप अलग समय पर अपडेट हो सकते हैं; इंस्टॉल करने से पहले रिलीज़ नोट पढ़ें।
छोटा ऐप। लंबे सेशन।
भाषा चुनें
Session और Monitor स्विच वाला pika Mac ऐप
सोर्स से बनाएँ
MCP कमांड
''')
add('id', '''
no-sleep-pika — Kontrol tidur dan layar Mac
no-sleep-pika adalah aplikasi bilah menu macOS ringan untuk mengontrol sesi dan layar, memantau baterai serta kondisi termal, dan menghubungkan agen AI melalui MCP.
Lewati ke konten
Aplikasi
Hubungkan MCP
Unduh untuk Mac
APLIKASI KECIL, SESI LEBIH PANJANG
Pika kecil.<br>Waktu kerja lebih panjang.
Kontrol sesi dan layar langsung dari bilah menu Mac. Teman tenang untuk pekerjaan yang butuh sedikit waktu lagi.
Lihat kode sumber
Rilis publik 1.0.3 · macOS 13+ · Apple Silicon & Intel
Lihat persyaratan instalasi
Kenali teman kerja malam Anda
Satu sakelar untuk sesi.
Mulai atau akhiri sesi pencegah tidur dari bilah menu. Tetap fokus pada pekerjaan Anda.
Layar sesuai keinginan.
Kontrol layar selama sesi aktif. Mematikan Session juga mematikan dan menonaktifkan sakelar Monitor, tetapi tidak langsung mematikan layar.
Memperhatikan kondisi Mac.
Pemantauan baterai dan kondisi termal macOS dapat mengakhiri sesi saat batas perlindungan tercapai. Batas menyesuaikan penggunaan dengan penutup tertutup, portabel, dan desktop.
DIRANCANG RINGAN
Dua sakelar.<br>Ruang untuk fokus.
Buka kontrol saat diperlukan. Tutup jendelanya, dan pika tetap ada di bilah menu.
Session · Monitor · Cukup itu.
SIAP UNTUK AGEN ANDA
Biarkan agen<br>mengatur sakelar.
Antarmuka MCP tersedia dalam build dari kode sumber. Unduhan publik 1.0.3 belum menyertakannya.
Di Mac dengan Xcode Command Line Tools, bangun kode sumber, pindahkan dist/pika.app ke /Applications, lalu buka. Mode standar tidak memerlukan persetujuan layanan pembantu.
Di Codex, buka Settings → MCP servers. Tambahkan server STDIO bernama pika dengan perintah di bawah. Tidak diperlukan argumen.
Setelah memulai ulang server MCP, agen dapat memeriksa status dan mengubah Session atau Monitor. Monitor memerlukan sesi aktif. Periksa sessionMode dan lidClosedSupported melalui pika_status; mode standar hanya menjaga Mac tetap terjaga saat penutup terbuka.
Salin
Tersalin
Pilih dan salin perintah
INSTAL DAN MULAI
Rumah di bilah menu.
Unduh DMG dan pindahkan aplikasi ke Applications. Unduhan saat ini mungkin masih bernama Always Awake.
Buka aplikasi dan ikuti pengaturan layanan pembantu. Kontrol muncul saat dibuka; menutup jendela tidak menghentikan aplikasi.
Aktifkan Session, lalu pilih Monitor aktif atau mati. Hapus layanan pembantu dari pengaturan sebelum menghapus aplikasi.
Unduhan saat ini belum ditandatangani Developer ID atau dinotarisasi. Bergantung pada sistem, macOS dapat memblokir aplikasi atau layanan pembantu berhak istimewa. Jika instalasi atau Session gagal dimulai, lihat panduan instalasi di GitHub.
Perilaku saat penutup ditutup bergantung pada Mac dan konfigurasi macOS. Pemantauan termal tidak menjamin suhu tertentu maupun keamanan penggunaan di dalam tas. Pastikan ventilasi tidak terhalang.
Beberapa hal penting
Apakah Monitor OFF menghentikan pekerjaan?
Selama sesi aktif, Monitor mengontrol layar. Mematikan Session juga mematikan dan menonaktifkan sakelar Monitor, tanpa langsung menidurkan layar.
Bagaimana bahasa situs dipilih?
Pada kunjungan pertama, bahasa pilihan browser digunakan, dengan bahasa Inggris sebagai cadangan. Pilihan disimpan di perangkat ini. Tidak ada pencarian lokasi IP.
Apakah kode sumber tersedia?
Ya. Lihat kode, persyaratan instalasi, dan pengaturan MCP di GitHub. Situs dan aplikasi dapat diperbarui pada waktu berbeda; periksa catatan rilis sebelum menginstal.
Aplikasi kecil. Sesi lebih panjang.
Pilih bahasa
Aplikasi pika untuk Mac dengan sakelar Session dan Monitor
Bangun dari kode sumber
Perintah MCP
''')
add('es', '''
no-sleep-pika — Control del reposo y la pantalla del Mac
no-sleep-pika es una app ligera para la barra de menús de macOS, con control de sesiones y pantalla, supervisión de batería y estado térmico e interfaz MCP para agentes de IA.
Saltar al contenido
La app
Conectar MCP
Descargar para Mac
UNA PEQUEÑA APP PARA SESIONES MÁS LARGAS
Una pequeña pika.<br>Un poco más de tiempo.
Controla las sesiones y la pantalla desde la barra de menús del Mac. Una compañía discreta para el trabajo que necesita un poco más de tiempo.
Ver código fuente
Versión pública 1.0.3 · macOS 13+ · Apple Silicon e Intel
Consultar requisitos de instalación
Tu compañía para el turno de noche
Un interruptor para la sesión.
Inicia o termina una sesión que mantiene el Mac despierto desde la barra de menús. Concéntrate en tu trabajo.
Tu pantalla, tú decides.
Controla la pantalla durante una sesión activa. Desactivar Session también apaga e inhabilita el interruptor Monitor, sin apagar la pantalla de inmediato.
Pendiente de tu Mac.
La supervisión de batería y estado térmico de macOS puede terminar la sesión al alcanzar los umbrales de protección. Los límites se adaptan al uso con tapa cerrada, portátil o de escritorio.
PEQUEÑA POR DISEÑO
Dos interruptores.<br>Espacio para concentrarte.
Abre los controles cuando los necesites. Cierra la ventana y pika seguirá en la barra de menús.
Session · Monitor · Nada más.
LISTA PARA TU AGENTE
Deja que tu agente<br>mueva el interruptor.
La interfaz MCP está en la compilación desde el código fuente. La descarga pública 1.0.3 todavía no la incluye.
En un Mac con Xcode Command Line Tools, compila el código, mueve dist/pika.app a /Applications y ábrela. El modo estándar no requiere autorizar el servicio auxiliar.
En Codex, abre Settings → MCP servers. Añade un servidor STDIO llamado pika con el comando de abajo. No necesita argumentos.
Tras reiniciar el servidor MCP, tu agente puede consultar el estado y cambiar Session o Monitor. Monitor requiere una sesión activa. Consulta sessionMode y lidClosedSupported con pika_status; el modo estándar mantiene el Mac despierto solo con la tapa abierta.
Copiar
Copiado
Selecciona y copia el comando
INSTALA Y EMPIEZA
Un hogar en tu barra de menús.
Descarga el DMG y mueve la app a Aplicaciones. La descarga actual puede seguir llamándose Always Awake.
Abre la app y configura el servicio auxiliar. Los controles aparecen al iniciarla; cerrar la ventana deja la app funcionando.
Activa Session y elige Monitor encendido o apagado. Elimina el servicio auxiliar desde los ajustes antes de desinstalar.
La descarga actual no tiene firma Developer ID ni notarización. Según tu sistema, macOS puede bloquear la app o su servicio auxiliar privilegiado. Si falla la instalación o el inicio de Session, consulta la guía de instalación en GitHub.
El comportamiento con la tapa cerrada depende del Mac y de la configuración de macOS. La supervisión térmica no garantiza una temperatura ni el uso seguro dentro de una bolsa. Mantén libre la ventilación.
Algunos detalles útiles
¿Desactivar Monitor detiene el trabajo?
Durante una sesión activa, Monitor controla la pantalla. Desactivar Session también apaga e inhabilita Monitor, sin poner la pantalla en reposo inmediatamente.
¿Cómo se elige el idioma del sitio?
En la primera visita usamos el idioma preferido del navegador, con inglés como alternativa. Tu elección se guarda en este dispositivo. No consultamos tu ubicación por IP.
¿Está disponible el código fuente?
Sí. Consulta el código, los requisitos de instalación y la configuración MCP en GitHub. La web y la app pueden actualizarse en momentos distintos; revisa las notas de la versión antes de instalar.
Pequeña app. Sesiones más largas.
Elegir idioma
La app pika para Mac con los interruptores Session y Monitor
Compilar desde el código fuente
Comando MCP
''')
add('fr', '''
no-sleep-pika — Contrôle de la veille et de l’écran du Mac
no-sleep-pika est une app légère pour la barre des menus de macOS : contrôle des sessions et de l’écran, suivi de la batterie et de l’état thermique, et interface MCP pour agents IA.
Aller au contenu
L’app
Connecter MCP
Télécharger pour Mac
UNE PETITE APP POUR PRENDRE SON TEMPS
Un petit pika.<br>Un peu plus de temps.
Contrôlez les sessions et l’écran depuis la barre des menus du Mac. Un compagnon discret pour les tâches qui demandent un peu plus de temps.
Voir le code source
Version publique 1.0.3 · macOS 13+ · Apple Silicon et Intel
Consulter les prérequis
Votre compagnon de nuit
Un seul interrupteur pour la session.
Lancez ou arrêtez une session de maintien en éveil depuis la barre des menus. Restez concentré sur votre travail.
Votre écran, votre choix.
Contrôlez l’écran pendant une session active. Désactiver Session désactive aussi Monitor, sans éteindre immédiatement l’écran.
À l’écoute de votre Mac.
Le suivi de la batterie et de l’état thermique de macOS peut arrêter une session aux seuils de protection. Les limites s’adaptent au capot fermé, au mode portable et au mode bureau.
PETITE PAR NATURE
Deux interrupteurs.<br>De la place pour se concentrer.
Ouvrez les commandes au besoin. Fermez la fenêtre : pika reste dans la barre des menus.
Session · Monitor · C’est tout.
PRÊTE POUR VOTRE AGENT
Laissez votre agent<br>actionner l’interrupteur.
L’interface MCP est disponible dans la version compilée depuis les sources. Le téléchargement public 1.0.3 ne l’inclut pas encore.
Sur un Mac avec Xcode Command Line Tools, compilez les sources, déplacez dist/pika.app dans /Applications, puis ouvrez l’app. Le mode standard ne nécessite pas d’autoriser le service auxiliaire.
Dans Codex, ouvrez Settings → MCP servers. Ajoutez un serveur STDIO nommé pika avec la commande ci-dessous. Aucun argument n’est nécessaire.
Après le redémarrage du serveur MCP, votre agent peut consulter l’état et modifier Session ou Monitor. Monitor nécessite une session active. Consultez sessionMode et lidClosedSupported avec pika_status ; le mode standard maintient le Mac éveillé uniquement avec le capot ouvert.
Copier
Copié
Sélectionnez et copiez la commande
INSTALLEZ ET COMMENCEZ
Une place dans votre barre des menus.
Téléchargez le DMG et déplacez l’app dans Applications. Le téléchargement actuel peut encore porter le nom Always Awake.
Ouvrez l’app et configurez le service auxiliaire. Les commandes apparaissent au lancement ; fermer la fenêtre laisse l’app fonctionner.
Activez Session, puis choisissez l’état de Monitor. Supprimez le service auxiliaire dans les réglages avant de désinstaller l’app.
Le téléchargement actuel n’est ni signé avec Developer ID ni notarié. Selon votre système, macOS peut bloquer l’app ou son service auxiliaire privilégié. En cas de problème d’installation ou de démarrage de Session, consultez le guide sur GitHub.
Le comportement capot fermé dépend du Mac et de la configuration macOS. Le suivi thermique ne garantit ni une température précise ni une utilisation sûre dans un sac. Dégagez la ventilation.
Quelques détails utiles
Désactiver Monitor arrête-t-il mon travail ?
Pendant une session active, Monitor contrôle l’écran. Désactiver Session désactive aussi Monitor, sans mettre immédiatement l’écran en veille.
Comment la langue du site est-elle choisie ?
À la première visite, nous utilisons la langue préférée du navigateur, ou l’anglais à défaut. Votre choix est enregistré sur cet appareil. Aucune recherche de localisation par IP.
Le code source est-il disponible ?
Oui. Consultez le code, les prérequis et la configuration MCP sur GitHub. Le site et l’app peuvent évoluer à des rythmes différents ; lisez les notes de version avant l’installation.
Petite app. Sessions plus longues.
Choisir la langue
L’app pika pour Mac avec les interrupteurs Session et Monitor
Compiler depuis les sources
Commande MCP
''')
add('de', '''
no-sleep-pika — Ruhezustand und Display am Mac steuern
no-sleep-pika ist eine schlanke macOS-Menüleisten-App für Sitzungen und Displaysteuerung, mit Überwachung von Akku und thermischem Zustand sowie MCP für KI-Agenten.
Zum Inhalt springen
Die App
MCP verbinden
Für Mac laden
KLEINE APP, LÄNGERE SITZUNGEN
Ein kleiner Pfeifhase.<br>Ein bisschen mehr Zeit.
Sitzungen und Display direkt über die Menüleiste steuern. Ein stiller Begleiter für Arbeit, die etwas länger dauert.
Quellcode ansehen
Öffentliche Version 1.0.3 · macOS 13+ · Apple Silicon & Intel
Installationsvoraussetzungen
Dein Begleiter für die Nachtschicht
Ein Schalter für die Sitzung.
Starte oder beende eine Sitzung zum Wachhalten über die Menüleiste. Dein Fokus bleibt bei der Arbeit.
Dein Display, deine Wahl.
Steuere das Display während einer aktiven Sitzung. Session AUS schaltet auch Monitor aus und deaktiviert den Schalter, ohne das Display sofort auszuschalten.
Behält deinen Mac im Blick.
Die Überwachung von Akku und thermischem macOS-Zustand kann Sitzungen an Schutzgrenzen beenden. Die Grenzen passen sich an zugeklappten, mobilen und Desktop-Betrieb an.
BEWUSST KLEIN
Zwei Schalter.<br>Platz zum Konzentrieren.
Öffne die Steuerung bei Bedarf. Schließe das Fenster, und pika bleibt in der Menüleiste.
Session · Monitor · Das ist alles.
BEREIT FÜR DEINEN AGENTEN
Lass deinen Agenten<br>den Schalter umlegen.
Die MCP-Schnittstelle ist im Build aus dem Quellcode enthalten. Der öffentliche Download 1.0.3 enthält sie noch nicht.
Erstelle die App auf einem Mac mit Xcode Command Line Tools aus dem Quellcode, verschiebe dist/pika.app nach /Applications und öffne sie. Der Standardmodus benötigt keine Genehmigung für den Hilfsdienst.
Öffne in Codex Settings → MCP servers. Füge einen STDIO-Server namens pika mit dem folgenden Befehl hinzu. Argumente sind nicht nötig.
Nach dem Neustart des MCP-Servers kann dein Agent den Status prüfen und Session oder Monitor ändern. Monitor benötigt eine aktive Sitzung. Prüfe sessionMode und lidClosedSupported mit pika_status; der Standardmodus hält den Mac nur bei geöffnetem Deckel wach.
Kopieren
Kopiert
Befehl markieren und kopieren
INSTALLIEREN UND LOSLEGEN
Ein Zuhause in deiner Menüleiste.
Lade die DMG und verschiebe die App nach Programme. Der aktuelle Download heißt möglicherweise noch Always Awake.
Öffne die App und richte den Hilfsdienst ein. Die Steuerung erscheint beim Start; beim Schließen des Fensters läuft die App weiter.
Schalte Session ein und wähle den Monitor-Zustand. Entferne vor der Deinstallation den Hilfsdienst in den Einstellungen.
Der aktuelle Download ist weder mit Developer ID signiert noch notarisiert. Je nach System kann macOS die App oder ihren privilegierten Hilfsdienst blockieren. Bei Problemen mit der Installation oder dem Start von Session beachte die Installationsanleitung auf GitHub.
Das Verhalten bei geschlossenem Deckel hängt von Mac und macOS-Konfiguration ab. Thermische Überwachung garantiert weder eine bestimmte Temperatur noch sicheren Betrieb in einer Tasche. Halte die Lüftung frei.
Gut zu wissen
Stoppt Monitor AUS meine Arbeit?
Während einer aktiven Sitzung steuert Monitor das Display. Session AUS setzt Monitor ebenfalls auf AUS und deaktiviert den Schalter, ohne das Display sofort in den Ruhezustand zu versetzen.
Wie wird die Sprache ausgewählt?
Beim ersten Besuch gilt die bevorzugte Browsersprache, sonst Englisch. Deine Auswahl wird auf diesem Gerät gespeichert. Es gibt keine IP-Standortabfrage.
Ist der Quellcode verfügbar?
Ja. Code, Installationsvoraussetzungen und MCP-Einrichtung stehen auf GitHub. Website und App können unterschiedlich schnell aktualisiert werden; prüfe vor der Installation die Versionshinweise.
Kleine App. Längere Sitzungen.
Sprache wählen
Die pika Mac-App mit Session- und Monitor-Schaltern
Aus Quellcode erstellen
MCP-Befehl
''')
add('pt-BR', '''
no-sleep-pika — Controle de repouso e tela do Mac
no-sleep-pika é um app leve para a barra de menus do macOS, com controle de sessão e tela, monitoramento de bateria e estado térmico e interface MCP para agentes de IA.
Pular para o conteúdo
O app
Conectar MCP
Baixar para Mac
UM APP PEQUENO PARA SESSÕES MAIS LONGAS
Uma pequena pika.<br>Um pouco mais de tempo.
Controle a sessão e a tela direto da barra de menus do Mac. Uma companhia discreta para o trabalho que precisa de mais um tempinho.
Ver código-fonte
Versão pública 1.0.3 · macOS 13+ · Apple Silicon e Intel
Conferir requisitos de instalação
Sua companhia no turno da noite
Um interruptor para a sessão.
Inicie ou encerre uma sessão que mantém o Mac acordado pela barra de menus. Seu foco continua no trabalho.
Sua tela, sua escolha.
Controle a tela durante uma sessão ativa. Desligar Session também desliga e desativa o interruptor Monitor, sem apagar a tela imediatamente.
De olho no seu Mac.
O monitoramento da bateria e do estado térmico do macOS pode encerrar a sessão nos limites de proteção. Os limites se adaptam ao uso com tampa fechada, portátil e desktop.
PEQUENO POR NATUREZA
Dois interruptores.<br>Espaço para focar.
Abra os controles quando precisar. Feche a janela e pika continua na barra de menus.
Session · Monitor · Só isso.
PRONTO PARA SEU AGENTE
Deixe seu agente<br>acionar o interruptor.
A interface MCP está disponível na compilação do código-fonte. O download público 1.0.3 ainda não a inclui.
Em um Mac com Xcode Command Line Tools, compile o código, mova dist/pika.app para /Applications e abra o app. O modo padrão não exige autorização do serviço auxiliar.
No Codex, abra Settings → MCP servers. Adicione um servidor STDIO chamado pika com o comando abaixo. Não são necessários argumentos.
Após reiniciar o servidor MCP, seu agente pode consultar o estado e alterar Session ou Monitor. Monitor exige uma sessão ativa. Confira sessionMode e lidClosedSupported com pika_status; o modo padrão mantém o Mac acordado apenas com a tampa aberta.
Copiar
Copiado
Selecione e copie o comando
INSTALE E COMECE
Um lar na sua barra de menus.
Baixe o DMG e mova o app para Aplicativos. O download atual ainda pode se chamar Always Awake.
Abra o app e configure o serviço auxiliar. Os controles aparecem ao iniciar; fechar a janela mantém o app em execução.
Ligue Session e escolha o estado de Monitor. Antes de desinstalar, remova o serviço auxiliar nos ajustes do app.
O download atual não tem assinatura Developer ID nem notarização. Dependendo do sistema, o macOS pode bloquear o app ou seu serviço auxiliar privilegiado. Se a instalação ou o início de Session falhar, consulte o guia de instalação no GitHub.
O comportamento com a tampa fechada depende do Mac e da configuração do macOS. O monitoramento térmico não garante uma temperatura específica nem o uso seguro dentro de uma bolsa. Mantenha a ventilação livre.
Alguns detalhes úteis
Desligar Monitor interrompe meu trabalho?
Durante uma sessão ativa, Monitor controla a tela. Desligar Session também desliga e desativa Monitor, sem colocar a tela em repouso imediatamente.
Como o idioma do site é escolhido?
Na primeira visita, usamos o idioma preferido do navegador, com inglês como alternativa. Sua escolha fica salva neste dispositivo. Não consultamos localização por IP.
O código-fonte está disponível?
Sim. Consulte o código, os requisitos de instalação e a configuração MCP no GitHub. Site e app podem ter ritmos de atualização diferentes; leia as notas da versão antes de instalar.
App pequeno. Sessões mais longas.
Escolher idioma
O app pika para Mac com os interruptores Session e Monitor
Compilar a partir do código-fonte
Comando MCP
''')
add('ru', '''
no-sleep-pika — Управление сном и экраном Mac
no-sleep-pika — лёгкое приложение для строки меню macOS: управление сеансами и экраном, отслеживание батареи и теплового состояния, MCP для ИИ-агентов.
Перейти к содержимому
Приложение
Подключить MCP
Скачать для Mac
МАЛЕНЬКОЕ ПРИЛОЖЕНИЕ ДЛЯ ДОЛГИХ СЕАНСОВ
Маленькая пищуха.<br>Чуть больше времени.
Управляйте сеансом и экраном из строки меню Mac. Тихий спутник для работы, которой нужно немного больше времени.
Исходный код
Публичная версия 1.0.3 · macOS 13+ · Apple Silicon и Intel
Требования к установке
Ваш спутник в ночную смену
Один переключатель сеанса.
Начинайте и завершайте сеанс бодрствования из строки меню. Сосредоточьтесь на своей работе.
Ваш экран — ваш выбор.
Управляйте экраном во время активного сеанса. Выключение Session также выключает и блокирует Monitor, но не гасит экран немедленно.
Внимание к состоянию Mac.
Отслеживание батареи и теплового состояния macOS позволяет завершать сеанс при достижении защитных порогов. Пороги зависят от закрытой крышки, переносного и настольного режима.
НИЧЕГО ЛИШНЕГО
Два переключателя.<br>Больше места для работы.
Открывайте панель, когда она нужна. Закройте окно — pika останется в строке меню.
Session · Monitor · Вот и всё.
ДЛЯ ВАШЕГО АГЕНТА
Пусть переключает<br>ваш агент.
Интерфейс MCP включён в сборку из исходного кода. Публичная версия 1.0.3 пока его не содержит.
На Mac с Xcode Command Line Tools соберите приложение из исходного кода, перенесите dist/pika.app в /Applications и откройте его. Стандартный режим не требует одобрения вспомогательной службы.
В Codex откройте Settings → MCP servers. Добавьте STDIO-сервер с именем pika и командой ниже. Аргументы не нужны.
После перезапуска MCP-сервера агент сможет проверять состояние и менять Session или Monitor. Для Monitor нужен активный сеанс. Проверьте sessionMode и lidClosedSupported через pika_status; стандартный режим поддерживает бодрствование Mac только при открытой крышке.
Копировать
Скопировано
Выделите и скопируйте команду
УСТАНОВКА И ЗАПУСК
Место в вашей строке меню.
Скачайте DMG и перенесите приложение в «Программы». Текущая версия может всё ещё называться Always Awake.
Откройте приложение и настройте вспомогательную службу. Панель появляется при запуске; закрытие окна не завершает приложение.
Включите Session и выберите состояние Monitor. Перед удалением приложения удалите вспомогательную службу в настройках.
Текущая версия не подписана Developer ID и не нотарифицирована. В зависимости от системы macOS может заблокировать приложение или привилегированную вспомогательную службу. При проблемах с установкой или запуском Session обратитесь к руководству на GitHub.
Поведение при закрытой крышке зависит от Mac и настроек macOS. Тепловой мониторинг не гарантирует определённую температуру или безопасность работы в сумке. Не перекрывайте вентиляцию.
Полезные подробности
Остановка Monitor прервёт работу?
В активном сеансе Monitor управляет экраном. Выключение Session также выключает и блокирует Monitor, но не переводит экран в сон немедленно.
Как выбирается язык сайта?
При первом посещении используется предпочитаемый язык браузера, иначе — английский. Ваш выбор сохраняется на этом устройстве. Геолокация по IP не используется.
Доступен ли исходный код?
Да. Код, требования к установке и настройка MCP доступны на GitHub. Сайт и приложение могут обновляться в разное время; перед установкой прочитайте примечания к выпуску.
Маленькое приложение. Долгие сеансы.
Выбрать язык
Приложение pika для Mac с переключателями Session и Monitor
Собрать из исходного кода
Команда MCP
''')
add('ar', '''
no-sleep-pika — التحكم في سكون Mac وشاشته
no-sleep-pika تطبيق خفيف لشريط قوائم macOS للتحكم في الجلسة والشاشة، مع مراقبة البطارية والحالة الحرارية وواجهة MCP لوكلاء الذكاء الاصطناعي.
انتقل إلى المحتوى
التطبيق
ربط MCP
تنزيل لنظام Mac
تطبيق صغير لجلسات أطول
بيكا صغير.<br>وقت أطول للعمل.
تحكّم في الجلسة والشاشة مباشرة من شريط قوائم Mac. رفيق هادئ للعمل الذي يحتاج إلى مزيد من الوقت.
عرض الشيفرة المصدرية
الإصدار العام 1.0.3 · macOS 13+ · Apple Silicon وIntel
متطلبات التثبيت
تعرّف إلى رفيق العمل الليلي
مفتاح واحد للجلسة.
ابدأ أو أنهِ جلسة إبقاء الجهاز مستيقظًا من شريط القوائم. حافظ على تركيزك في العمل.
شاشتك، خيارك.
تحكّم في الشاشة أثناء الجلسة النشطة. إيقاف Session يوقف مفتاح Monitor ويعطّله أيضًا، لكنه لا يطفئ الشاشة فورًا.
مع الاهتمام بحالة Mac.
قد تنهي مراقبة البطارية والحالة الحرارية في macOS الجلسة عند حدود الحماية. تتكيف الحدود مع إغلاق الغطاء والاستخدام المحمول أو المكتبي.
صغير بتصميمه
مفتاحان.<br>مساحة للتركيز.
افتح عناصر التحكم عند الحاجة. أغلق النافذة وسيبقى pika في شريط القوائم.
Session · Monitor · هذا كل شيء.
جاهز لوكيلك
دع وكيلك<br>يحرّك المفتاح.
واجهة MCP متوفرة في النسخة المبنية من المصدر. التنزيل العام 1.0.3 لا يتضمنها بعد.
على Mac مزوّد بـ Xcode Command Line Tools، ابنِ التطبيق من المصدر وانقل dist/pika.app إلى /Applications ثم افتحه. الوضع القياسي لا يحتاج إلى الموافقة على الخدمة المساعدة.
في Codex افتح Settings → MCP servers. أضف خادم STDIO باسم pika باستخدام الأمر أدناه. لا حاجة إلى معاملات.
بعد إعادة تشغيل خادم MCP يمكن لوكيلك فحص الحالة وتغيير Session أو Monitor. يتطلب Monitor جلسة نشطة. افحص sessionMode وlidClosedSupported باستخدام pika_status؛ الوضع القياسي يبقي Mac مستيقظًا فقط عندما يكون الغطاء مفتوحًا.
نسخ
تم النسخ
حدّد الأمر وانسخه
ثبّت وابدأ
منزل في شريط القوائم.
نزّل DMG وانقل التطبيق إلى Applications. قد يظل اسم التنزيل الحالي Always Awake.
افتح التطبيق وأكمل إعداد الخدمة المساعدة. تظهر عناصر التحكم عند التشغيل؛ إغلاق النافذة لا يوقف التطبيق.
شغّل Session ثم اختر حالة Monitor. احذف الخدمة المساعدة من إعدادات التطبيق قبل إلغاء تثبيته.
التنزيل الحالي غير موقّع بـ Developer ID ولم يخضع للتوثيق. بحسب نظامك قد يحظر macOS التطبيق أو الخدمة المساعدة ذات الامتيازات. إذا تعثر التثبيت أو بدء Session، راجع دليل التثبيت على GitHub.
السلوك مع الغطاء المغلق يعتمد على Mac وإعدادات macOS. المراقبة الحرارية لا تضمن درجة حرارة محددة أو سلامة التشغيل داخل حقيبة. اترك التهوية مفتوحة.
تفاصيل مفيدة
هل إيقاف Monitor يوقف عملي؟
أثناء الجلسة النشطة يتحكم Monitor في الشاشة. إيقاف Session يوقف مفتاح Monitor ويعطّله دون إدخال الشاشة في السكون فورًا.
كيف تُختار لغة الموقع؟
في الزيارة الأولى نستخدم لغة المتصفح المفضلة، والإنجليزية عند عدم دعمها. يُحفظ اختيارك على هذا الجهاز. لا نبحث عن موقعك عبر عنوان IP.
هل الشيفرة المصدرية متاحة؟
نعم. اطّلع على الشيفرة ومتطلبات التثبيت وإعداد MCP على GitHub. قد يتطور الموقع والتطبيق بسرعات مختلفة؛ راجع ملاحظات الإصدار قبل التثبيت.
تطبيق صغير. جلسات أطول.
اختر اللغة
تطبيق pika لنظام Mac بمفتاحي Session وMonitor
البناء من المصدر
أمر MCP
''')
add('vi', '''
no-sleep-pika — Điều khiển chế độ ngủ và màn hình Mac
no-sleep-pika là ứng dụng thanh menu macOS gọn nhẹ, điều khiển phiên và màn hình, theo dõi pin và trạng thái nhiệt, cùng giao diện MCP cho tác nhân AI.
Đến nội dung
Ứng dụng
Kết nối MCP
Tải cho Mac
ỨNG DỤNG NHỎ, PHIÊN LÀM VIỆC DÀI HƠN
Pika bé nhỏ.<br>Thêm thời gian làm việc.
Điều khiển phiên và màn hình ngay trên thanh menu Mac. Người bạn yên lặng cho những công việc cần thêm chút thời gian.
Xem mã nguồn
Bản công khai 1.0.3 · macOS 13+ · Apple Silicon & Intel
Xem yêu cầu cài đặt
Người bạn đồng hành ca đêm
Một công tắc cho phiên.
Bắt đầu hoặc kết thúc phiên giữ máy thức từ thanh menu. Tập trung vào công việc trước mắt.
Màn hình theo ý bạn.
Điều khiển màn hình khi phiên đang hoạt động. Tắt Session cũng tắt và vô hiệu hóa công tắc Monitor nhưng không tắt màn hình ngay lập tức.
Quan tâm đến chiếc Mac.
Theo dõi pin và trạng thái nhiệt macOS có thể kết thúc phiên khi chạm ngưỡng bảo vệ. Ngưỡng thay đổi theo chế độ đóng nắp, di động và máy bàn.
GỌN NHẸ TỪ THIẾT KẾ
Hai công tắc.<br>Không gian để tập trung.
Mở bảng điều khiển khi cần. Đóng cửa sổ, pika vẫn ở lại trên thanh menu.
Session · Monitor · Chỉ vậy thôi.
SẴN SÀNG CHO TÁC NHÂN CỦA BẠN
Để tác nhân<br>bật tắt giúp bạn.
Giao diện MCP có trong bản dựng từ mã nguồn. Bản tải công khai 1.0.3 chưa bao gồm tính năng này.
Trên Mac có Xcode Command Line Tools, dựng mã nguồn, chuyển dist/pika.app vào /Applications rồi mở. Chế độ tiêu chuẩn không yêu cầu phê duyệt dịch vụ trợ giúp.
Trong Codex, mở Settings → MCP servers. Thêm máy chủ STDIO tên pika với lệnh bên dưới. Không cần đối số.
Sau khi khởi động lại máy chủ MCP, tác nhân có thể kiểm tra trạng thái và thay đổi Session hoặc Monitor. Monitor yêu cầu phiên đang hoạt động. Kiểm tra sessionMode và lidClosedSupported bằng pika_status; chế độ tiêu chuẩn chỉ giữ Mac thức khi mở nắp.
Sao chép
Đã sao chép
Chọn và sao chép lệnh
CÀI ĐẶT VÀ BẮT ĐẦU
Một ngôi nhà trên thanh menu.
Tải DMG và chuyển ứng dụng vào Applications. Bản tải hiện tại có thể vẫn mang tên Always Awake.
Mở ứng dụng và thiết lập dịch vụ trợ giúp. Bảng điều khiển xuất hiện khi khởi chạy; đóng cửa sổ vẫn giữ ứng dụng chạy.
Bật Session rồi chọn trạng thái Monitor. Gỡ dịch vụ trợ giúp trong cài đặt trước khi xóa ứng dụng.
Bản tải hiện tại chưa được ký Developer ID hoặc công chứng. Tùy hệ thống, macOS có thể chặn ứng dụng hoặc dịch vụ trợ giúp đặc quyền. Nếu gặp lỗi cài đặt hoặc khởi động Session, hãy xem hướng dẫn trên GitHub.
Hành vi khi đóng nắp phụ thuộc vào Mac và cấu hình macOS. Theo dõi nhiệt không đảm bảo nhiệt độ cụ thể hay an toàn khi chạy trong túi. Giữ thông thoáng các khe tản nhiệt.
Một vài điều hữu ích
Tắt Monitor có dừng công việc không?
Trong phiên đang hoạt động, Monitor điều khiển màn hình. Tắt Session cũng tắt và vô hiệu hóa Monitor mà không lập tức đưa màn hình vào chế độ ngủ.
Trang web chọn ngôn ngữ thế nào?
Lần đầu truy cập, chúng tôi dùng ngôn ngữ ưu tiên của trình duyệt, mặc định tiếng Anh nếu không hỗ trợ. Lựa chọn được lưu trên thiết bị này. Không tra cứu vị trí qua IP.
Mã nguồn có công khai không?
Có. Xem mã, yêu cầu cài đặt và thiết lập MCP trên GitHub. Trang web và ứng dụng có thể cập nhật khác thời điểm; hãy xem ghi chú phát hành trước khi cài.
Ứng dụng nhỏ. Phiên dài hơn.
Chọn ngôn ngữ
Ứng dụng pika cho Mac với công tắc Session và Monitor
Dựng từ mã nguồn
Lệnh MCP
''')
add('th', '''
no-sleep-pika — ควบคุมการพักเครื่องและหน้าจอ Mac
no-sleep-pika เป็นแอปแถบเมนู macOS ขนาดเล็กสำหรับควบคุมเซสชันและหน้าจอ พร้อมติดตามแบตเตอรี่และสถานะความร้อน และอินเทอร์เฟซ MCP สำหรับเอเจนต์ AI
ข้ามไปยังเนื้อหา
แอป
เชื่อมต่อ MCP
ดาวน์โหลดสำหรับ Mac
แอปเล็ก เพื่อเซสชันที่ยาวขึ้น
พิกาตัวน้อย<br>เพิ่มเวลาทำงานอีกนิด
ควบคุมเซสชันและหน้าจอจากแถบเมนู Mac เพื่อนเงียบ ๆ สำหรับงานที่ต้องการเวลาเพิ่มอีกหน่อย
ดูซอร์สโค้ด
รุ่นสาธารณะ 1.0.3 · macOS 13+ · Apple Silicon และ Intel
ดูข้อกำหนดการติดตั้ง
เพื่อนร่วมงานยามค่ำคืน
สวิตช์เดียวสำหรับเซสชัน
เริ่มหรือหยุดเซสชันที่ทำให้เครื่องตื่นจากแถบเมนู ให้คุณจดจ่อกับงานตรงหน้า
หน้าจอในแบบที่คุณเลือก
ควบคุมหน้าจอขณะเซสชันทำงาน การปิด Session จะปิดและล็อกสวิตช์ Monitor ด้วย แต่จะไม่ดับหน้าจอทันที
ใส่ใจสถานะของ Mac
การติดตามแบตเตอรี่และสถานะความร้อนของ macOS อาจยุติเซสชันเมื่อถึงเกณฑ์ป้องกัน เกณฑ์ปรับตามการปิดฝา การใช้งานแบบพกพา และแบบเดสก์ท็อป
เล็กตั้งแต่การออกแบบ
สองสวิตช์<br>พื้นที่สำหรับสมาธิ
เปิดส่วนควบคุมเมื่อต้องการ ปิดหน้าต่างแล้ว pika ยังอยู่บนแถบเมนู
Session · Monitor · เท่านี้เอง
พร้อมสำหรับเอเจนต์ของคุณ
ให้เอเจนต์ช่วย<br>เปิดปิดสวิตช์
อินเทอร์เฟซ MCP อยู่ในรุ่นที่สร้างจากซอร์สโค้ด รุ่นสาธารณะ 1.0.3 ที่ดาวน์โหลดได้ยังไม่มีฟีเจอร์นี้
บน Mac ที่มี Xcode Command Line Tools ให้สร้างแอปจากซอร์สโค้ด ย้าย dist/pika.app ไปที่ /Applications แล้วเปิดแอป โหมดมาตรฐานไม่ต้องอนุมัติบริการตัวช่วย
ใน Codex เปิด Settings → MCP servers เพิ่มเซิร์ฟเวอร์ STDIO ชื่อ pika ด้วยคำสั่งด้านล่าง ไม่ต้องใส่อาร์กิวเมนต์
หลังเริ่มเซิร์ฟเวอร์ MCP ใหม่ เอเจนต์จะตรวจสอบสถานะและเปลี่ยน Session หรือ Monitor ได้ Monitor ต้องมีเซสชันที่ทำงานอยู่ ตรวจสอบ sessionMode และ lidClosedSupported ด้วย pika_status โหมดมาตรฐานทำให้ Mac ตื่นได้เฉพาะเมื่อเปิดฝาอยู่
คัดลอก
คัดลอกแล้ว
เลือกและคัดลอกคำสั่ง
ติดตั้งและเริ่มต้น
บ้านเล็ก ๆ บนแถบเมนู
ดาวน์โหลด DMG และย้ายแอปไปที่ Applications รุ่นดาวน์โหลดปัจจุบันอาจยังใช้ชื่อ Always Awake
เปิดแอปและตั้งค่าบริการตัวช่วย ส่วนควบคุมจะแสดงเมื่อเปิดแอป การปิดหน้าต่างจะไม่หยุดแอป
เปิด Session แล้วเลือกสถานะ Monitor ก่อนถอนการติดตั้ง ให้ลบบริการตัวช่วยจากการตั้งค่าของแอป
รุ่นดาวน์โหลดปัจจุบันยังไม่ได้ลงนาม Developer ID หรือรับการรับรอง macOS อาจบล็อกแอปหรือบริการตัวช่วยที่มีสิทธิ์พิเศษ ทั้งนี้ขึ้นอยู่กับระบบ หากติดตั้งหรือเริ่ม Session ไม่ได้ โปรดดูคู่มือการติดตั้งบน GitHub
การทำงานเมื่อปิดฝาขึ้นอยู่กับ Mac และการตั้งค่า macOS การติดตามความร้อนไม่รับประกันอุณหภูมิหรือความปลอดภัยเมื่อใช้งานในกระเป๋า ควรเปิดทางระบายอากาศไว้
รายละเอียดที่ควรรู้
ปิด Monitor แล้วงานจะหยุดไหม?
ระหว่างเซสชันที่ทำงาน Monitor ควบคุมหน้าจอ การปิด Session จะปิดและล็อก Monitor ด้วย โดยไม่ทำให้หน้าจอพักทันที
เว็บไซต์เลือกภาษาอย่างไร?
ครั้งแรกจะใช้ภาษาที่ต้องการของเบราว์เซอร์ หากไม่รองรับจะใช้ภาษาอังกฤษ ตัวเลือกของคุณบันทึกไว้ในอุปกรณ์นี้ ไม่มีการค้นหาตำแหน่งจาก IP
ซอร์สโค้ดเปิดเผยหรือไม่?
ใช่ ดูโค้ด ข้อกำหนดการติดตั้ง และการตั้งค่า MCP ได้ที่ GitHub เว็บไซต์และแอปอาจอัปเดตต่างเวลากัน โปรดอ่านบันทึกรุ่นก่อนติดตั้ง
แอปเล็ก เซสชันยาวขึ้น
เลือกภาษา
แอป pika สำหรับ Mac พร้อมสวิตช์ Session และ Monitor
สร้างจากซอร์สโค้ด
คำสั่ง MCP
''')


def page_path(locale):
    return '/' if locale == 'en' else '/' + locale + '/'


def page_url(locale):
    return BASE + page_path(locale)


def render(locale):
    t = TEXT[locale]
    esc = html.escape
    h = lambda key: esc(t[key]).replace('&lt;br&gt;', '<br>')
    alternate = '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{page_url(code)}">' for code, _ in LANGUAGES)
    options = '\n'.join(f'<option value="{code}" lang="{code}"{(" selected" if code == locale else "")}>{name}</option>' for code, name in LANGUAGES)
    language_links = ' '.join(f'<a href="{page_path(code)}" hreflang="{code}" lang="{code}">{name}</a>' for code, name in LANGUAGES)
    cards = ''.join(f'<article class="feature"><span class="pixel-icon icon-{n}" aria-hidden="true">{["↗", "◐", "+"][n-1]}</span><h3>{h("feature"+str(n))}</h3><p>{h("body"+str(n))}</p></article>' for n in range(1,4))
    faq = ''.join(f'<details><summary>{h("q"+str(n))}<span aria-hidden="true">+</span></summary><p>{h("a"+str(n))}</p></details>' for n in range(1,4))
    schema = {'@context':'https://schema.org','@type':'SoftwareApplication','name':'no-sleep-pika','alternateName':'pika','url':BASE,'applicationCategory':'UtilitiesApplication','operatingSystem':'macOS 13 or later','description':t['description'],'softwareVersion':'1.0.3','downloadUrl':DOWNLOAD,'image':BASE+'/assets/pika-pixel.png','codeRepository':REPO,'inLanguage':locale}
    return f'''<!doctype html>
<html lang="{locale}" dir="{'rtl' if locale == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{h('title')}</title><meta name="description" content="{esc(t['description'], quote=True)}">
<meta name="theme-color" content="#f6f4eb"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{page_url(locale)}">
{alternate}
<link rel="alternate" hreflang="x-default" href="{BASE}/">
<meta property="og:type" content="website"><meta property="og:site_name" content="no-sleep-pika">
<meta property="og:title" content="{h('title')}"><meta property="og:description" content="{esc(t['description'], quote=True)}">
<meta property="og:url" content="{page_url(locale)}"><meta property="og:image" content="{BASE}/assets/pika-pixel.png">
<meta property="og:image:alt" content="A pixel-art pika animal">
<meta property="og:locale" content="{locale.replace('-', '_')}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{h('title')}"><meta name="twitter:description" content="{esc(t['description'], quote=True)}"><meta name="twitter:image" content="{BASE}/assets/pika-pixel.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body data-locale="{locale}">
<a class="skip" href="#main">{h('skip')}</a>
<div class="shell">
<header class="header">
<a href="{page_path(locale)}" class="brand" aria-label="no-sleep-pika"><img src="/assets/favicon.svg" alt="" width="30" height="30"><span>no-sleep-pika<span class="brand-dot">.</span></span></a>
<nav aria-label="{h('features')}"><a href="#features">{h('features')}</a><a href="#mcp">MCP <span aria-hidden="true">↗</span></a></nav>
<div class="language"><span aria-hidden="true">◎</span><label class="sr-only" for="language">{h('language')}</label><select id="language">{options}</select></div>
</header>
<main id="main">
<section class="hero" aria-labelledby="hero-title">
<div class="hero-copy"><p class="eyebrow"><span class="status-dot" aria-hidden="true"></span>{h('eyebrow')}</p><h1 id="hero-title">{h('headline')}</h1><p class="intro">{h('intro')}</p>
<div class="actions"><a class="button primary" href="{DOWNLOAD}"><svg width="17" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 2v11m-4-4 4 4 4-4M3 13v5h14v-5" stroke="currentColor" stroke-width="1.8"/></svg>{h('download')}</a><a class="text-link" href="{REPO}">{h('source')} <span aria-hidden="true">↗</span></a></div>
<p class="release">{h('release')}</p><a class="requirement" href="#installation">{h('compatibility')} <span aria-hidden="true">↘</span></a>
</div>
<div class="hero-art"><span class="moon" aria-hidden="true"></span><span class="star star-a" aria-hidden="true">✦</span><span class="star star-b" aria-hidden="true">+</span><span class="star star-c" aria-hidden="true">✦</span><div class="orbit" aria-hidden="true"></div><img class="mascot" src="/assets/pika-pixel.png" alt="" width="1239" height="1270" fetchpriority="high"><span class="art-name" aria-hidden="true">no sleep, pika.</span><span class="art-coordinates" aria-hidden="true">☾ 00:01 — ∞</span></div>
</section>
<div class="divider"><span>{h('scroll')}</span><span aria-hidden="true">↓</span></div>
<section id="features" class="features" aria-label="{h('features')}">{cards}</section>
<section class="controls-panel" aria-labelledby="controls-title"><div><p class="eyebrow">{h('controls')}</p><h2 id="controls-title">{h('controlstitle')}</h2><p>{h('controlsbody')}</p></div><div class="app-preview"><div class="preview-menubar" aria-hidden="true"><span>pika</span><span>◉ &nbsp; ▰ &nbsp; 00:01</span></div><img src="/app.png" width="232" height="80" alt="{h('screenshot')}" loading="lazy"><p>{h('window')}</p></div></section>
<section id="mcp" class="mcp-section" aria-labelledby="mcp-title"><div class="section-heading"><div><p class="eyebrow">{h('mcp')}</p><h2 id="mcp-title">{h('mcptitle')}</h2></div><p>{h('mcpbody')}</p></div>
<div class="mcp-grid"><ol class="steps"><li><span>01</span><p>{h('buildstep')} <a href="{REPO}#mcp">{h('source')} ↗</a></p></li><li><span>02</span><p>{h('addstep')}</p></li><li><span>03</span><p>{h('toolstep')}</p></li></ol>
<div class="terminal" dir="ltr"><div class="terminal-bar"><span class="terminal-dots" aria-hidden="true">● ● ●</span><span>pika / MCP</span><span>STDIO</span></div><div class="terminal-body"><p class="code-label">{h('buildlabel')}</p><pre><code>git clone https://github.com/Ezcho/always-awake-mac.git
cd always-awake-mac
./Scripts/build.sh</code></pre><div class="code-heading"><p class="code-label">{h('configlabel')}</p><button class="copy" data-copy="mcp-command" data-copied="{h('copied')}" data-failed="{h('copyfail')}">{h('copy')} <span aria-hidden="true">⧉</span></button></div><pre class="command"><code id="mcp-command">/Applications/pika.app/Contents/MacOS/pika-mcp</code></pre><div class="tool-list"><code>pika_status</code><code>pika_set_session(enabled)</code><code>pika_set_monitor(enabled)</code></div><span class="copy-status sr-only" role="status" aria-live="polite"></span></div></div></div></section>
<section id="installation" class="installation" aria-labelledby="install-title"><p class="eyebrow">{h('installation')}</p><h2 id="install-title">{h('installtitle')}</h2><ol class="install-steps">{''.join(f'<li><span>0{n}</span><p>{h("install"+str(n))}</p></li>' for n in range(1,4))}</ol><div class="install-note"><span aria-hidden="true">ⓘ</span><div><p>{h('limitation')} <a href="{REPO}#readme">GitHub ↗</a></p><p>{h('safety')}</p></div></div></section>
<section class="faq" aria-labelledby="faq-title"><h2 id="faq-title">{h('faq')}</h2><div>{faq}</div></section>
</main>
<footer><div><a class="brand" href="{page_path(locale)}">no-sleep-pika<span class="brand-dot">.</span></a><p>{h('footer')}</p></div><div class="footer-links"><a href="{REPO}">GitHub ↗</a><a href="{REPO}/releases/tag/{RELEASE}">1.0.3 ↗</a><a href="#mcp">MCP ↗</a></div></footer>
<noscript><nav class="language-fallback" aria-label="{h('language')}">{language_links}</nav></noscript>
</div></body></html>'''


def main():
    assert set(TEXT) == {code for code, _ in LANGUAGES}
    for locale, _ in LANGUAGES:
        dest = OUT if locale == 'en' else OUT / locale
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(render(locale), encoding='utf-8')
    alternatives = ''.join(f'<xhtml:link rel="alternate" hreflang="{code}" href="{page_url(code)}"/>' for code, _ in LANGUAGES)
    alternatives += f'<xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>'
    # No fabricated lastmod date: source changes determine deploy dates.
    entries = ''.join(f'<url><loc>{page_url(code)}</loc>{alternatives}</url>' for code, _ in LANGUAGES)
    (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">' + entries + '</urlset>\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n', encoding='utf-8')
    (OUT / '.nojekyll').touch()
    print(f'Built {len(LANGUAGES)} localized pages, sitemap.xml and robots.txt.')

if __name__ == '__main__':
    main()
