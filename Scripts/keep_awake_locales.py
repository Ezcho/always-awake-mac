"""Editorial copy for the keep-awake comparison, published 2026-10-02."""
COPY = {}
def add(locale, title, intro, headings, paragraphs, ui):
    COPY[locale] = dict(title=title, intro=intro, headings=headings.split('|'), paragraphs=[p.strip().split('\n\n') for p in paragraphs.strip().split('\n---\n')], download=ui[0], install=ui[1], related=ui[2], disclosure=ui[3])

add('ko', 'Mac에서 맥을 잠들지 않게 하는 방법: 클램쉘·터미널·pika 비교',
'맥 잠자기 방지 방법을 전원 연결과 클램쉘 모드, caffeinate 터미널 명령어, pika 설치 순서로 비교합니다. 화면 끄기와 잠금의 차이, 덮개를 닫을 때의 조건과 작업 확인 방법까지 정리했습니다.',
'먼저 목적에 맞는 방법 고르기|1. 전원 연결 + 클램쉘 모드로 덮고 사용하기|덮개를 열어 둔다면 macOS 전원 설정도 확인|2. 터미널 caffeinate로 잠자기 잠시 막기|시간 제한·화면 유지·작업 종료에 맞춘 명령어|caffeinate로 덮개 닫힘까지 막을 수 있을까?|3. pika 설치 후 Session과 Monitor로 제어하기|작업이 계속되는지 확인하고 정상 종료하기|자주 묻는 질문: 잠금·네트워크·발열|공식 자료와 이 글의 범위',
'''
큰 파일을 받거나 코드를 빌드하고 AI 에이전트 작업을 맡겼는데, 잠깐 자리를 비운 뒤 돌아오니 진행이 멈춰 있는 경우가 있습니다. Mac 화면이 어두워진 것만으로는 원인을 알 수 없습니다. 화면 잠자기, 화면 잠금, 시스템 잠자기는 서로 다른 상태이기 때문입니다. 화면과 로그인 화면이 꺼져 있어도 시스템은 작업을 계속할 수 있고, 반대로 앱 창이 다시 나타난다고 자리를 비운 동안 계속 실행됐다는 뜻은 아닙니다.

외장 모니터로 계속 일하려면 전원과 주변기기를 갖춘 클램쉘 구성을 먼저 확인하세요. 덮개를 열어 둔 상태에서 특정 작업만 끝내려면 macOS 기본 명령어 caffeinate가 간단합니다. 외장 화면 없이 덮개를 닫고 백그라운드 작업을 유지하고 싶다면 pika의 설치형 보조 서비스와 Session 기능을 사용할 수 있습니다. 세 가지를 한꺼번에 켜기보다 자신의 목적에 맞는 방법 하나부터 확인하는 편이 문제 원인을 찾기 쉽습니다.
---
클램쉘 모드는 맥북을 닫고 외장 모니터·키보드·마우스로 사용하는 구성입니다. 먼저 덮개를 연 채 전원 어댑터, 지원되는 외장 디스플레이, 입력 장치를 연결합니다. 외장 화면이 정상 출력되고 키보드와 마우스가 반응하는지 확인한 다음 덮개를 닫습니다. 전원을 공급하는 호환 USB-C 디스플레이를 쓰는 경우 별도 충전기 필요 여부는 해당 기기의 사양에 따릅니다.

충전기만 연결한다고 클램쉘 구성이 완성되는 것은 아닙니다. Apple은 덮개를 닫은 Mac의 외장 화면 문제를 확인할 때 전원과 외장 키보드·마우스 연결을 점검하도록 안내합니다. 디스플레이 지원 대수·해상도는 Mac 모델과 칩에 따라 다릅니다. Apple Silicon에서 액세서리 연결 허용을 요청하면 덮개를 연 상태에서 승인하세요. 화면이 검게 나오면 먼저 케이블·허브·전원·디스플레이 지원 조건부터 확인하고 앱 설치를 만능 해결책으로 생각하지 않는 것이 좋습니다.
---
덮개를 열어 두고 충전 중인 Mac이라면 시스템 설정의 배터리 → 옵션에서 ‘전원 어댑터 사용 시 디스플레이가 꺼져 있을 때 자동으로 잠자지 않게 하기’에 해당하는 항목을 확인할 수 있습니다. 메뉴 이름과 제공 위치는 macOS 버전과 기종에 따라 달라질 수 있으므로 시스템 설정 검색과 Apple 안내를 함께 확인하세요. 데스크톱 Mac은 에너지 관련 메뉴 구성이 다를 수 있습니다.

이 설정은 화면을 계속 밝게 켜 두는 것과 다릅니다. 화면 끄기 시간과 잠금 시 암호 요구는 그대로 두면서 전원 연결 중 자동 잠자기만 조정할 수 있습니다. 또한 덮개 닫힘에 의한 잠자기까지 항상 막아 주는 설정으로 이해하면 안 됩니다. 작업이 끝난 뒤 기존 값을 돌려놓고 싶다면 변경 전 설정을 기록해 두세요. 회사 관리 장비에서는 관리 정책으로 설정이 제한될 수도 있습니다.
---
터미널은 응용 프로그램의 유틸리티 폴더나 Spotlight에서 열 수 있습니다. macOS에 기본 포함된 caffeinate는 실행 중에 잠자기 방지 요청(assertion)을 유지하는 도구입니다. 아래 명령은 사용자 입력이 없어서 발생하는 시스템의 유휴 잠자기를 막습니다. 별도 프로그램 설치나 sudo 관리자 권한은 필요하지 않습니다.

명령을 실행한 터미널을 그대로 두고 다른 앱에서 다운로드나 작업을 진행하면 됩니다. 아무 메시지 없이 커서가 대기하는 것은 정상입니다. 화면 잠자기 방지 옵션은 넣지 않았으므로 디스플레이는 설정에 따라 꺼질 수 있습니다. 중지하려면 해당 터미널에서 Control+C를 누릅니다. caffeinate가 종료되면 자신이 만든 요청도 해제됩니다. 컴퓨터를 종료하거나 터미널 프로세스를 끊은 뒤에도 영구 유지되는 설정이 아닙니다.
---
아래 첫 명령은 3,600초, 즉 1시간 동안 유휴 잠자기를 막습니다. 두 번째 명령은 1,800초, 즉 30분 동안 유휴 잠자기와 디스플레이 잠자기를 함께 막습니다. 화면이 필요하지 않으면 -d를 빼는 편이 목적에 맞습니다. -t의 단위는 분이 아니라 초입니다.

세 번째 명령은 make를 실행하고 그 작업이 끝날 때까지 유휴 잠자기를 막는 예시입니다. make를 쓰는 프로젝트 디렉터리에서 실행하며, 실제로 빌드를 수행하는 명령이므로 테스트용으로 무작정 붙여 넣지는 마세요. 자신의 작업 명령으로 바꿀 수 있습니다. 별도 프로세스를 백그라운드로 보내고 바로 끝나는 실행 프로그램을 감싼 경우에는 진짜 작업보다 caffeinate가 먼저 끝날 수 있습니다. 명령을 직접 실행하는 방식에서는 -t가 사용되지 않는다는 점도 macOS 매뉴얼에 명시되어 있습니다.
---
흔한 오해는 caffeinate -i나 -d를 실행하면 맥북 덮개를 닫아도 무조건 계속 돌아간다는 것입니다. -i는 유휴 시스템 잠자기, -d는 디스플레이 잠자기를 대상으로 합니다. 덮개 닫힘은 별도의 조건이므로 이 명령을 클램쉘 조건을 대체하는 수단으로 안내할 수는 없습니다. 덮개를 열어 두고 일시적으로 작업을 유지하는 용도로 먼저 사용하세요.

매뉴얼의 -s 옵션은 시스템 잠자기 방지 요청을 만들지만 AC 전원에서만 유효합니다. 이것도 모든 Mac과 macOS에서 외장 화면 없이 덮개 닫힘을 우회한다는 보장은 아닙니다. -u는 사용자 활동을 알리는 옵션으로 화면을 깨울 수 있어, 화면을 끄고 두려는 목적에는 맞지 않을 수 있습니다. 인터넷의 여러 옵션을 의미 없이 묶기보다 필요한 동작만 선택하는 것이 낫습니다.
---
pika는 Session과 Monitor를 메뉴 막대에서 제어하는 macOS 13 이상용 앱으로, Apple Silicon과 Intel을 지원합니다. 공식 다운로드 페이지에서 통합 PKG를 받고 설치 프로그램을 엽니다. PKG는 앱과 덮개 기능에 필요한 관리자 보조 서비스를 함께 설치합니다. macOS 인증·보안 승인이 표시되면 설치 도움말을 따라 사용자가 직접 완료합니다. macOS 보안을 전체 비활성화할 필요는 없습니다.

설치 후 /Applications/pika.app을 실행하고 보조 서비스가 연결됐는지 확인합니다. Session ON으로 준비한 다음, 화면 유지가 필요하지 않다면 Monitor OFF를 선택하고 맥북 덮개를 닫습니다. 덮개 모드에서 ON을 누르거나 열린 덮개 상태에서 Monitor를 바꾼 순간 화면을 즉시 끄도록 설계된 앱은 아닙니다. 시스템 잠자기 방지는 덮개를 닫기 전에 준비하고 화면 정책은 덮개 닫힘 뒤 적용합니다.

덮개를 다시 열면 화면 제어가 대기 상태로 돌아갑니다. Session OFF를 누르면 pika가 관리한 잠자기 설정을 복구하며 Monitor도 OFF로 표시되지만 화면을 즉시 끄지는 않습니다. 창의 X 버튼은 앱 종료가 아니며 메뉴 막대에 남습니다. 완전히 끝낼 때는 Session OFF 또는 앱의 종료 메뉴를 사용하세요. 보조 서비스 오류가 보이면 정상 실행으로 간주하지 말고 설치·연결 문제부터 해결해야 합니다.
---
어떤 방법을 선택하든 첫 실행은 짧게 확인하세요. 작은 다운로드나 테스트 작업을 시작하고 시작 시각·진행률을 기록한 다음, 원하는 화면·덮개 상태로 몇 분 두었다가 돌아와 작업 로그의 시각이 이어지는지 확인합니다. 여기서 제안한 확인 절차는 독자가 자신의 장비에서 수행할 절차이며, 모든 모델에서 검증을 마쳤다는 뜻이 아닙니다.

터미널의 pmset -g assertions는 현재 잠자기 방지 요청을 읽기만 하는 진단 명령입니다. 다른 앱이 유지한 요청이 함께 보일 수 있으며, 이 출력만으로 덮개 닫힘이나 네트워크의 연속 동작까지 입증할 수는 없습니다. 명령 옵션은 man caffeinate로 해당 Mac에 설치된 설명서를 볼 수 있습니다. 이 글을 작성하면서 매뉴얼을 확인했으며 전원 설정을 바꾸는 명령을 실행하지는 않았습니다.
---
‘화면이 잠겼는데 작업이 멈춘 건가요?’ 잠금만으로 시스템 잠자기라고 판단할 수 없습니다. 비밀번호 요구를 끄기보다 작업 로그를 확인하세요. ‘AI 작업은 무조건 끝까지 되나요?’ 그렇지 않습니다. Wi-Fi·VPN·API 장애, 사용량 제한, 권한 승인 대기, 앱 자체 오류는 잠자기 방지와 별개입니다. pika는 AI의 대화를 대신 진행하거나 끊긴 네트워크를 자동 복구하지 않습니다.

‘가방 안에서 켜 두어도 되나요?’ 실행 중인 맥북은 통풍되는 단단한 곳에 두세요. 덮개를 닫았다는 이유로 발열이 사라지지 않으며, pika의 배터리·열 상태 보호가 모든 과열이나 방전을 막는 보장은 아닙니다. 배터리·열 보호, 보조 서비스 연결 문제 등에 따라 세션이 종료될 수 있습니다. 장시간 작업 전에는 전원·환기·작업 저장 및 재시도 방법을 함께 확인하세요.
---
이 글은 no-sleep-pika 제작자가 작성한 자사 앱을 포함한 방법 비교입니다. 외장 화면 사용 조건과 설정 위치는 Apple 공식 자료를, 터미널 옵션은 macOS의 caffeinate(8) 매뉴얼을 근거로 설명했습니다. pika 동작은 공개 1.0.13 문서와 구현을 기준으로 하며 Apple이나 AI 서비스 제공자의 공식 추천을 의미하지 않습니다.

외장 화면으로 일할 때는 클램쉘 구성을, 덮개를 열고 일회성 작업을 할 때는 caffeinate를, 외장 화면 없이 덮고 작업을 유지할 때는 pika 설치와 보조 서비스 상태를 확인하세요. 작업을 계속하는 데 필요한 조건은 화면을 켜 두는 조건과 같지 않습니다. 자신의 환경에서 짧게 확인한 뒤 필요한 시간만 유지하는 것이 이 가이드의 핵심입니다.
''', ['pika 다운로드','설치 도움말','맥북 덮개 닫기 가이드','no-sleep-pika 제작자가 작성한 자사 앱 포함 비교 안내입니다.'])

add('en', 'How to keep your Mac awake: clamshell mode, caffeinate and pika',
'Compare three ways to prevent Mac sleep: power and clamshell mode, the built-in caffeinate command, and pika. Learn which method fits a closed lid, a dark display, or a temporary background job.',
'Choose the method for your job|1. Power and closed-display clamshell mode|Check macOS settings with the lid open|2. Keep a Mac awake temporarily with caffeinate|Timed sessions, display sleep and individual commands|Does caffeinate keep a closed MacBook awake?|3. Install pika and use Session and Monitor|Verify your job and end the session|Questions about locking, networks and heat|Sources and scope',
'''
A download, build or AI-agent job may stop progressing while you are away. A dark display does not tell you why. Display sleep, a locked screen and system sleep are different states: a locked Mac can still be running, while seeing the same windows after waking does not establish that work continued throughout the break.

For an external-monitor desk setup, check clamshell requirements first. For a temporary task with the lid open, caffeinate needs no additional app. For closed-lid background work without an external monitor, pika provides Session controls with an installed administrator helper. Start with one method so that failures and cleanup are easier to understand.
---
Clamshell mode means using a MacBook with its lid closed and external display and input devices connected. With the lid open, connect power, a supported monitor, keyboard and mouse or trackpad; confirm they work before closing it. A compatible display that supplies power may replace a separate charger depending on its specifications.

Connecting only a charger does not establish this setup. Apple’s external-display troubleshooting specifies power and external input devices for a closed laptop. Supported display counts and resolutions depend on your Mac. Approve accessory connection prompts with the lid open. If the external screen is black, check cables, docks, power and model limits before assuming an app will fix it.
---
For a plugged-in laptop with the lid open, look in System Settings → Battery → Options for the option preventing automatic sleep on the power adapter when the display is off. Labels and availability vary by macOS version and model; desktop Macs use different energy settings. The Apple guide below describes the setting.

This can allow the display to turn off without automatically putting the whole computer to sleep. You can keep password-on-lock enabled. It is not a universal override for lid-triggered sleep. Record your original choice if you want to restore it afterward, and remember that managed Macs may restrict these settings.
---
Open Terminal from Utilities or Spotlight. macOS includes caffeinate, which holds a sleep-prevention request while it runs. The command below prevents idle system sleep without requiring sudo or a separate installation. Leave its Terminal session running while you work in another app.

No message and a waiting cursor are normal. Without the display option, your screen can still sleep. Press Control+C in that Terminal to stop it and release its request. This is a temporary process, not a permanent power preference that survives termination or shutdown.
---
The first command below prevents idle sleep for 3,600 seconds (one hour). The second prevents both idle system sleep and display sleep for 1,800 seconds (30 minutes). Omit -d when the display does not need to remain lit. The -t duration is in seconds.

The third runs make and keeps its assertion for that command’s lifetime. Run it only in a project where you intend to build; it really executes make. You can substitute your own job. A launcher that exits after starting background work can finish before the actual job does. The installed manual says that -t is not used when a utility is invoked with caffeinate.
---
The -i option concerns idle system sleep and -d concerns display sleep. Closing a laptop lid is a separate condition. These options should not be presented as a replacement for clamshell requirements or a guarantee of closed-lid operation without a monitor.

The -s assertion is valid only on AC power; it is not evidence of a universal lid-sleep override. The -u option declares user activity and can wake the display, which may conflict with wanting a dark screen. Choose options for their documented purpose rather than copying a long flag combination blindly.
---
pika is a menu-bar utility for macOS 13 or later, supporting Apple Silicon and Intel. Download the full PKG from the official site. The installer includes the app and administrator helper needed for closed-lid functionality. Complete macOS authorization and any required security approval yourself using the installation guide; do not disable system-wide security protections.

Open /Applications/pika.app and confirm helper connectivity. Turn Session ON, choose Monitor OFF if you do not need display wakefulness, then close the lid. Sleep prevention is prepared before closure; the display policy engages after lid closure. Changing Monitor while the lid is open saves a preference rather than immediately blanking the screen.

Reopening the lid returns display control to waiting. Session OFF restores pika’s managed sleep setting and shows Monitor OFF without immediately blanking the screen. Closing the window leaves the menu-bar app running. Use Session OFF or Quit to finish. A helper error means the operation has not succeeded and must be resolved first.
---
Test a short download or build, note its starting time, leave the Mac in your intended state, and inspect timestamps and progress afterward. This is a suggested verification procedure, not a claim that every Mac model has been tested. Check the job itself, not just whether the screen lights up again.

The read-only pmset command below shows current power assertions, including requests from other apps. It does not alone prove closed-lid continuity or network availability. Read the installed caffeinate manual for your Mac’s options. Preparing this article involved reading the manual, not changing the machine’s power settings.
---
A lock screen does not by itself mean that the system slept. Keep authentication enabled and inspect your job log. Sleep prevention cannot fix Wi-Fi, VPN or API outages, service limits, permission prompts or app crashes. pika neither drives AI conversations nor reconnects a failed network.

Keep a running Mac on a firm, ventilated surface, not in a bag. A closed lid does not remove heat production. Battery and thermal protection may end a pika session and cannot guarantee protection against all overheating or depletion. For long jobs, plan power, ventilation, saved progress and recovery as well as sleep prevention.
---
This comparison is written by the maker of no-sleep-pika and includes our own app. Apple documentation supports external-display and settings guidance; command options were checked against the installed caffeinate(8) manual. pika behavior refers to the public 1.0.13 documentation and implementation. This is not an endorsement by Apple or any AI provider.

Use clamshell mode for an external-screen workstation, caffeinate for temporary lid-open tasks, or pika with a working helper for closed-lid background work. A screen staying on and a job continuing are different goals. Verify your environment and keep the session active only as long as needed.
''', ['Download pika','Installation help','Closed-lid MacBook guide','Written by the maker of no-sleep-pika; this comparison includes our own app.'])

add('ja', 'Macをスリープさせない方法：クラムシェル・caffeinate・pika',
'電源と外部ディスプレイ、ターミナルのcaffeinate、pikaの3つの方法を比較。画面ロックとスリープの違い、ふたを閉じる条件、作業の確認方法を説明します。',
'目的に合う方法を選ぶ|1. 電源接続とクラムシェルモード|ふたを開けて使う場合の設定|2. caffeinateで一時的にスリープを防ぐ|時間・画面・コマンドに合わせた使い方|ふたを閉じても動く？|3. pikaをインストールする|動作確認と終了|ロック・通信・発熱の注意点|参考資料と対象範囲',
'''
画面の消灯、画面ロック、システムのスリープは別の状態です。ロック中でも処理は動くことがあります。外部画面で作業するならクラムシェル、一時的な開いた状態の処理ならcaffeinate、外部画面なしで閉じて動かすならpikaの補助サービスを検討します。
---
ふたを開けた状態で電源、対応する外部ディスプレイ、キーボードとマウスを接続し、動作を確認してから閉じます。給電対応のディスプレイでは仕様により充電器を兼ねられます。充電器だけではこの構成になりません。画面数や解像度はMacのモデルによって異なり、アクセサリの許可も必要な場合があります。
---
電源接続中でふたを開けている場合は、システム設定のバッテリーのオプションで、画面がオフのときの自動スリープを防ぐ設定を確認します。名称や場所はOSと機種によります。パスワード要求は維持できます。この設定がふたを閉じたときのスリープも必ず防ぐわけではありません。
---
ターミナルを開いて次のコマンドを実行します。caffeinateはmacOSに含まれ、sudoは不要です。入力がないために起きるシステムのスリープを防ぎます。ターミナルを動かしたままにし、終了はその画面でControl+C。画面自体は消灯できます。永続設定ではなく、プロセス終了で要求も解除されます。
---
最初の例は3,600秒（1時間）、次は画面のスリープも含めて1,800秒（30分）です。画面が不要なら-dを省きます。最後の例はmakeを実際に起動し、その終了まで維持します。ビルドするつもりのプロジェクトでのみ実行してください。別プロセスを起動してすぐ終了するランチャーでは、実作業より先に解除される場合があります。コマンドを指定した場合-tは使われません。
---
-iはアイドル時のシステムスリープ、-dは画面のスリープが対象です。ふたを閉じる動作は別条件で、外部画面なしの動作保証ではありません。-sはAC電源でのみ有効です。-uはユーザー操作を通知して画面を点灯させる場合があり、消灯させたい目的には合わないことがあります。
---
pikaはmacOS 13以降のApple SiliconとIntelに対応します。公式サイトの統合PKGでアプリと管理者補助サービスをインストールし、macOSの認証や必要な承認を完了します。/Applications/pika.appを開き、補助サービス接続を確認。Session ON、必要ならMonitor OFFを選び、ふたを閉じます。スリープ防止は事前に準備され、画面制御は閉じてから適用されます。開いた状態でMonitorを変更しても即座に消灯しません。Session OFFで管理した設定を復元します。ウィンドウを閉じてもアプリは終了しません。
---
短い処理で開始時刻を記録し、閉じた状態を試してからログと進行状況を確認します。全モデルでの動作確認済みという意味ではありません。pmset -g assertionsは現在の要求を読むだけで、通信やふたを閉じた状態の継続を証明するものではありません。詳細はman caffeinateで確認できます。
---
ロックだけで処理停止とは判断できません。通信障害、VPN、API制限、承認待ち、アプリの停止は別問題で、pikaはAI会話や通信の復旧を代行しません。動作中は通気のよい硬い面に置き、バッグに入れないでください。電池・熱の保護や補助サービス障害でSessionが終了する場合があり、すべての過熱や放電を防げる保証はありません。
---
no-sleep-pikaの開発者による自社製品を含む比較です。Appleの資料とMacに付属するcaffeinate(8)マニュアルを参考にし、pikaは公開版1.0.13の仕様を説明しています。AppleやAI提供企業による推薦ではありません。必要な時間だけ使い、終了後は通常の状態に戻しましょう。
''', ['pikaをダウンロード','インストール案内','ふたを閉じたMacBookのガイド','pika開発者による、自社アプリを含む比較です。'])

add('zh-CN', '让 Mac 不进入睡眠的方法：合盖模式、caffeinate 与 pika',
'比较接通电源的合盖模式、终端 caffeinate 命令和 pika 安装。说明屏幕关闭、锁屏与系统睡眠的区别，以及各方法的条件和退出步骤。',
'先选择适合任务的方法|1. 接通电源并使用合盖模式|开盖时检查 macOS 电源设置|2. 使用 caffeinate 临时防止睡眠|按时间、屏幕和任务选择命令|caffeinate 能阻止合盖睡眠吗？|3. 安装 pika 并控制 Session|确认任务继续并结束会话|锁屏、网络和发热问题|资料来源与范围',
'''
屏幕关闭、锁屏和系统睡眠并不相同。锁屏时任务可能仍在运行，唤醒后窗口仍在也不能证明任务一直在执行。外接显示器办公可先用合盖模式；开盖的临时任务可用 caffeinate；不接外屏的合盖后台工作可考虑带辅助服务的 pika。
---
先在开盖状态连接电源、受支持的外接显示器、键盘和鼠标，确认能正常使用后再合盖。支持供电的显示器可能代替单独充电器，需查看规格。只接充电器并不构成这一配置。外屏数量和分辨率取决于 Mac 型号；出现配件连接请求时应先在开盖状态批准。
---
开盖并连接电源时，可在系统设置的电池选项中寻找显示器关闭时防止自动睡眠的设置。名称和位置随系统及型号变化。可以保留锁屏密码要求，而不必一直亮屏。此设置并非合盖睡眠的通用覆盖。记录原设置以便完成后恢复。
---
打开终端运行下面命令。macOS 自带 caffeinate，无需额外安装或 sudo。它阻止因空闲导致的系统睡眠；屏幕仍可关闭。保持该终端进程运行，在同一终端按 Control+C 结束。没有输出而等待是正常现象，这不是重启后仍保留的永久设置。
---
第一个例子维持 3,600 秒，即一小时；第二个同时防止屏幕睡眠，持续 1,800 秒，即半小时。不需要亮屏就省略 -d。第三个会实际运行 make，并在该命令结束时释放请求，只在确实准备编译的项目中使用。立即退出的后台任务启动器可能比真实任务先结束。指定运行命令时 -t 不生效。
---
-i 针对系统空闲睡眠，-d 针对屏幕睡眠。合盖是另一种条件，不能把这些选项当成无需外屏就能合盖运行的保证。-s 仅在交流电源下有效；-u 表示用户活动，可能唤醒屏幕。应理解选项含义，不要盲目组合参数。
---
pika 支持 macOS 13 及以上、Apple Silicon 和 Intel。下载官方完整 PKG，安装应用和管理员辅助服务，并由用户完成 macOS 身份认证与必要的安全批准。打开 /Applications/pika.app，确认服务连接，开启 Session，按需关闭 Monitor，然后合盖。系统防睡眠会提前准备，屏幕策略在合盖后应用。开盖时切换 Monitor 只保存选择。关闭 Session 会恢复 pika 管理的设置，但不会立即熄屏；关闭窗口也不会退出应用。
---
先用短任务记录开始时间，按实际需求合盖或熄屏，之后检查日志时间和进度。这是建议的自测步骤，并非声称已测试所有型号。pmset -g assertions 只读取当前防睡眠请求，不能证明网络或合盖连续性。man caffeinate 可查看本机说明。
---
锁屏不等于任务停止。网络、VPN、API 限额、等待批准或应用崩溃都可能单独中断任务，pika 不会代替 AI 继续对话或恢复连接。运行中的 Mac 应放在通风的硬质表面，不要装进包里。电池或热保护、辅助服务故障可能结束会话；保护功能不能保证防止所有过热或耗尽。
---
本文由 no-sleep-pika 开发者撰写，包含自家应用。依据 Apple 官方资料、本机 caffeinate(8) 手册及 pika 公开版 1.0.13 的文档与实现，不代表 Apple 或 AI 服务提供商推荐。按使用场景选择方法，并仅在需要期间保持运行。
''', ['下载 pika','安装帮助','MacBook 合盖指南','由 no-sleep-pika 开发者撰写，包含自家应用的比较。'])

add('zh-TW', '讓 Mac 不進入睡眠的方法：闔蓋模式、caffeinate 與 pika',
'比較接上電源的闔蓋模式、終端機 caffeinate 指令與 pika 安裝，說明關閉螢幕、鎖定與系統睡眠的差別，以及使用條件和結束方式。',
'先依工作選擇方法|1. 電源與闔蓋模式|開蓋時檢查 macOS 設定|2. 用 caffeinate 暫時防止睡眠|依時間、螢幕與指令設定|caffeinate 能阻止闔蓋睡眠嗎？|3. 安裝 pika|確認進度並結束|鎖定、網路與發熱|資料來源與範圍',
'''
螢幕關閉、畫面鎖定和系統睡眠是不同狀態。鎖定時可能仍在工作；喚醒後視窗存在，也不能證明工作一直執行。外接螢幕工作先考慮闔蓋模式；開蓋的短期工作可用 caffeinate；沒有外接螢幕的闔蓋工作可考慮 pika 與輔助服務。
---
開蓋時接上電源、支援的外接顯示器、鍵盤與滑鼠，確認可操作後再闔蓋。能供電的顯示器是否可代替充電器需依規格確認。只插充電器並不是完整的闔蓋配置。顯示器數量與解析度依 Mac 型號而異，配件連接要求應先在開蓋時批准。
---
開蓋並接電時，在系統設定的電池選項尋找顯示器關閉時防止自動睡眠的設定。名稱和位置依 macOS 版本與機種而異。可以保留鎖定密碼，不必一直亮屏。這不是所有闔蓋睡眠的通用解法；記錄原設定以便恢復。
---
開啟終端機輸入下方指令。macOS 內建 caffeinate，不需 sudo 或額外安裝。它防止閒置造成的系統睡眠，螢幕仍能關閉。保留該程序，在相同終端機按 Control+C 即可停止。沒有輸出而等待是正常狀態；程序結束後要求也會解除。
---
第一個例子維持 3,600 秒（一小時）；第二個同時防止螢幕睡眠，持續 1,800 秒（半小時）。不需亮屏可省略 -d。第三個實際執行 make，到該指令結束為止。只在準備編譯的專案中使用；會立即退出的背景啟動器可能比真正工作更早結束。指定工作指令時 -t 不生效。
---
-i 針對系統閒置睡眠，-d 針對螢幕睡眠。闔蓋屬於另一條件，不代表外接螢幕需求已被取代。-s 只在 AC 電源下有效；-u 表示使用者活動，可能喚醒螢幕。不要把任意旗標組合當成所有 Mac 的闔蓋保證。
---
pika 支援 macOS 13 以上、Apple Silicon 與 Intel。從官方下載完整 PKG，安裝應用程式和管理員輔助服務，由使用者完成 macOS 認證與必要批准。開啟 /Applications/pika.app，確認服務連線，開啟 Session、按需關閉 Monitor，再闔蓋。睡眠防止先準備，畫面策略於闔蓋後套用。開蓋時改 Monitor 只儲存選擇。Session OFF 恢復管理的設定，不會立刻關閉螢幕；關閉視窗不等於結束程式。
---
先用短工作記錄開始時間，再測試闔蓋或關屏，之後檢查日誌和進度。這是自行驗證步驟，不代表所有機型都已測試。pmset -g assertions 只讀取當前要求，不能證明網路或闔蓋期間持續運作。man caffeinate 可查看本機說明。
---
鎖定不等於睡眠。Wi-Fi、VPN、API 限額、等待批准或程式錯誤可能中斷工作，pika 不會自動接續 AI 對話或恢復網路。運作中請放在通風的硬質平面，不要放進袋子。電池與熱保護或服務問題可能結束 Session；不能保證防止所有過熱與電力耗盡。
---
本文由 no-sleep-pika 開發者撰寫並介紹自家應用程式，參考 Apple 資料、macOS 的 caffeinate(8) 手冊與 pika 1.0.13 公開實作。並非 Apple 或 AI 供應商背書。選擇適合情境的方法，完成後解除防睡眠。
''', ['下載 pika','安裝說明','MacBook 闔蓋指南','由 no-sleep-pika 開發者撰寫，包含自家產品。'])

add('es', 'Cómo evitar que tu Mac se duerma: modo cerrado, caffeinate y pika',
'Compara la alimentación y el modo clamshell, los comandos de Terminal y pika. Aprende cuándo sirve cada método, qué ocurre al cerrar la tapa y cómo terminar la sesión.',
'Elige según tu tarea|1. Alimentación y modo clamshell|Ajustes con la tapa abierta|2. Evitar reposo con caffeinate|Duración, pantalla y comandos|¿Funciona con la tapa cerrada?|3. Instalar pika|Comprobar y finalizar|Bloqueo, red y temperatura|Fuentes y alcance',
'''
Apagar la pantalla, bloquearla y suspender el sistema son estados distintos. Un Mac bloqueado puede seguir trabajando. Para usar monitor externo, empieza por clamshell; para tareas temporales con tapa abierta, caffeinate; para trabajar cerrado sin monitor externo, considera pika con su servicio auxiliar.
---
Con la tapa abierta, conecta alimentación, monitor compatible, teclado y ratón; comprueba su funcionamiento antes de cerrarla. Una pantalla que suministra energía puede sustituir al cargador según sus especificaciones. Conectar solamente el cargador no basta. El número y resolución de pantallas dependen del modelo; acepta los permisos de accesorios con la tapa abierta.
---
En un portátil enchufado, busca en Ajustes del Sistema → Batería → Opciones la prevención de reposo automático cuando la pantalla está apagada. La ubicación varía según macOS y modelo. Puedes conservar la contraseña de bloqueo. No es una anulación universal del reposo al cerrar la tapa. Anota los ajustes originales.
---
Abre Terminal y ejecuta el comando siguiente. caffeinate viene con macOS y no necesita sudo. Evita el reposo por inactividad, aunque la pantalla puede apagarse. Mantén el proceso activo y pulsa Control+C en ese Terminal para terminar. Que no muestre mensajes es normal; la solicitud desaparece al finalizar el proceso.
---
El primer ejemplo dura 3.600 segundos, una hora; el segundo mantiene también la pantalla durante 1.800 segundos, media hora. Omite -d si no necesitas imagen. El tercero ejecuta realmente make y dura hasta que ese comando termina: úsalo solo en un proyecto que quieras compilar. Un lanzador que sale enseguida puede terminar antes que el trabajo real. Al ejecutar una utilidad, -t no se utiliza.
---
-i afecta al reposo del sistema por inactividad; -d al de la pantalla. Cerrar la tapa es otra condición: no son una garantía de funcionamiento cerrado sin monitor. -s solo es válido con alimentación de corriente; -u señala actividad y puede encender la pantalla. Selecciona las opciones por su función documentada.
---
pika admite macOS 13 o posterior, Apple Silicon e Intel. Instala el PKG completo de la web oficial: contiene la app y el servicio auxiliar con privilegios. Completa personalmente la autenticación y aprobación necesarias en macOS. Abre /Applications/pika.app, confirma la conexión del servicio, activa Session, elige Monitor OFF si procede y cierra la tapa. La prevención se prepara antes; la política de pantalla se aplica después de cerrarla. Cambiar Monitor con la tapa abierta guarda la elección. Session OFF restaura el ajuste gestionado sin apagar inmediatamente la pantalla; cerrar la ventana no cierra la app.
---
Prueba primero una tarea corta, registra la hora y revisa el progreso y los registros después. Es una prueba propuesta, no una certificación de todos los modelos. pmset -g assertions consulta solicitudes actuales sin modificarlas; no demuestra continuidad de red ni de funcionamiento cerrado. man caffeinate muestra el manual instalado.
---
Bloqueo no significa necesariamente reposo. Wi-Fi, VPN, límites de API, permisos pendientes y errores pueden detener tareas: pika no continúa conversaciones ni reconecta la red. Mantén el Mac funcionando sobre una superficie firme y ventilada, no dentro de una bolsa. La protección térmica, la batería o un fallo del servicio pueden finalizar la sesión; no se garantiza evitar todo sobrecalentamiento o descarga.
---
Comparación del creador de no-sleep-pika que incluye su propia app. Las fuentes son Apple, el manual caffeinate(8) de macOS y la documentación e implementación pública de pika 1.0.13. No implica recomendación de Apple ni de proveedores de IA. Mantén el equipo despierto solo durante el tiempo necesario.
''', ['Descargar pika','Ayuda de instalación','Guía de MacBook cerrado','Escrito por el creador de no-sleep-pika; incluye nuestra app.'])

add('fr', 'Empêcher un Mac de se mettre en veille : écran fermé, caffeinate et pika',
'Comparez le mode capot fermé avec alimentation, les commandes Terminal et pika. Découvrez les conditions, les limites et la manière de terminer chaque session.',
'Choisir selon le besoin|1. Alimentation et mode capot fermé|Réglages avec le capot ouvert|2. Utiliser caffeinate temporairement|Durée, écran et commande|Et lorsque le capot est fermé ?|3. Installer pika|Vérifier puis arrêter|Verrouillage, réseau et chaleur|Sources et portée',
'''
Écran éteint, verrouillage et veille du système sont différents. Un Mac verrouillé peut continuer à travailler. Utilisez le mode capot fermé pour un écran externe, caffeinate pour une tâche temporaire capot ouvert, ou pika avec son service auxiliaire pour travailler fermé sans écran externe.
---
Capot ouvert, branchez l’alimentation, un écran compatible, le clavier et la souris, puis vérifiez leur fonctionnement avant de fermer. Un écran fournissant du courant peut remplacer le chargeur selon ses caractéristiques. Le chargeur seul ne suffit pas. Le nombre d’écrans et leur résolution dépendent du modèle. Autorisez les accessoires avant de fermer.
---
Sur un portable branché, cherchez dans Réglages Système → Batterie → Options le réglage empêchant la veille automatique lorsque l’écran est éteint. Son emplacement varie selon macOS et le modèle. Conservez le mot de passe au verrouillage. Cela ne garantit pas d’empêcher la veille déclenchée par la fermeture du capot. Notez les anciens réglages.
---
Ouvrez Terminal et lancez la commande ci-dessous. caffeinate est intégré à macOS et ne demande pas sudo. Il empêche la veille d’inactivité, mais l’écran peut s’éteindre. Gardez le processus actif et utilisez Contrôle+C dans ce Terminal pour l’arrêter. L’absence de message est normale. La demande disparaît quand le processus se termine.
---
Le premier exemple dure 3 600 secondes, soit une heure. Le deuxième maintient aussi l’écran pendant 1 800 secondes, soit trente minutes ; retirez -d si inutile. Le troisième exécute réellement make et accompagne sa durée : utilisez-le seulement pour compiler le projet voulu. Un lanceur quittant immédiatement peut finir avant la tâche réelle. L’option -t n’est pas utilisée lorsqu’une commande est lancée.
---
-i concerne la veille d’inactivité du système et -d celle de l’écran. Fermer le capot est une autre condition : ces options ne garantissent pas le fonctionnement fermé sans écran externe. -s ne vaut que sur secteur ; -u signale une activité et peut rallumer l’écran. Choisissez les options selon leur fonction.
---
pika prend en charge macOS 13 et versions ultérieures, Apple Silicon et Intel. Son PKG officiel complet installe l’app et le service auxiliaire administrateur. Effectuez vous-même l’authentification et les autorisations nécessaires. Ouvrez /Applications/pika.app, vérifiez le service, activez Session, choisissez Monitor OFF si nécessaire, puis fermez le capot. La prévention est préparée avant ; la politique d’affichage est appliquée après fermeture. Capot ouvert, Monitor enregistre seulement le choix. Session OFF restaure le réglage géré sans éteindre immédiatement l’écran. Fermer la fenêtre ne quitte pas l’app.
---
Testez une courte tâche en notant l’heure et vérifiez ses journaux après l’attente. Cette procédure ne signifie pas que tous les modèles ont été testés. pmset -g assertions lit les demandes existantes sans les modifier ; il ne prouve pas la continuité réseau ni le fonctionnement capot fermé. man caffeinate ouvre le manuel local.
---
Un verrouillage n’est pas forcément une veille. Wi-Fi, VPN, limites d’API, autorisations en attente et erreurs peuvent interrompre le travail. pika ne poursuit pas les conversations IA et ne rétablit pas le réseau. Utilisez une surface ferme et ventilée, jamais un sac. Batterie, protection thermique ou panne du service peuvent arrêter la session ; aucune garantie contre toute surchauffe ou décharge n’est donnée.
---
Comparaison rédigée par le créateur de no-sleep-pika, incluant sa propre app. Sources : Apple, manuel macOS caffeinate(8), documentation et code de pika 1.0.13. Il ne s’agit pas d’une recommandation d’Apple ou d’un fournisseur d’IA. Limitez la session à la durée nécessaire.
''', ['Télécharger pika','Aide à l’installation','Guide du MacBook fermé','Rédigé par le créateur de no-sleep-pika ; présente notre app.'])

add('de', 'Mac wach halten: Clamshell-Modus, caffeinate und pika im Vergleich',
'Netzteil und geschlossener Bildschirm, Terminal-Befehle oder pika: Voraussetzungen, Grenzen und das sichere Beenden einer Sitzung verständlich erklärt.',
'Die passende Methode wählen|1. Stromversorgung und Clamshell-Modus|Einstellungen bei geöffnetem Deckel|2. Mit caffeinate vorübergehend wach bleiben|Zeitlimit, Display und einzelne Befehle|Was passiert beim Zuklappen?|3. pika installieren|Fortschritt prüfen und beenden|Sperre, Netzwerk und Wärme|Quellen und Geltungsbereich',
'''
Ein dunkles Display, eine Bildschirmsperre und Systemruhezustand sind unterschiedliche Zustände. Ein gesperrter Mac kann weiterarbeiten. Für externe Bildschirme eignet sich Clamshell, für kurze Aufgaben mit offenem Deckel caffeinate und für Arbeit ohne externen Bildschirm bei geschlossenem Deckel pika mit Hilfsdienst.
---
Verbinde bei offenem Deckel Strom, einen unterstützten Monitor, Tastatur und Maus. Prüfe alles vor dem Zuklappen. Ein stromliefernder Monitor kann je nach Spezifikation das Netzteil ersetzen. Ein Ladegerät allein ergibt diese Konfiguration nicht. Monitoranzahl und Auflösung hängen vom Mac ab. Zubehörfreigaben bei offenem Deckel bestätigen.
---
Suche am angeschlossenen Notebook unter Systemeinstellungen → Batterie → Optionen nach der Verhinderung automatischen Ruhezustands bei ausgeschaltetem Display. Namen und Orte unterscheiden sich je nach macOS und Modell. Das Sperrpasswort kann aktiv bleiben. Diese Option ist keine allgemeine Umgehung des Ruhezustands beim Zuklappen. Notiere den ursprünglichen Wert.
---
Öffne Terminal und starte den folgenden Befehl. caffeinate gehört zu macOS und benötigt kein sudo. Er verhindert inaktivitätsbedingten Systemruhezustand, während das Display ausgehen darf. Lass den Prozess laufen und beende ihn dort mit Control+C. Eine wartende Eingabe ohne Ausgabe ist normal. Die Anforderung endet mit dem Prozess.
---
Der erste Befehl gilt 3.600 Sekunden, also eine Stunde. Der zweite hält auch das Display für 1.800 Sekunden, also 30 Minuten wach; ohne Bedarf -d weglassen. Der dritte führt make tatsächlich aus und begleitet diesen Prozess. Nur im gewünschten Build-Projekt starten. Ein sofort endender Starter kann die Anforderung vor der eigentlichen Hintergrundarbeit verlieren. Mit einem ausgeführten Programm wird -t nicht verwendet.
---
-i betrifft Systemleerlauf, -d das Display. Deckelschließen ist eine andere Bedingung, deshalb garantieren diese Optionen keinen Betrieb ohne externen Monitor. -s gilt nur bei Netzstrom; -u meldet Benutzeraktivität und kann das Display einschalten. Flags nach ihrem dokumentierten Zweck auswählen.
---
pika unterstützt macOS 13 oder neuer, Apple Silicon und Intel. Das vollständige offizielle PKG installiert App und Administrator-Hilfsdienst. macOS-Authentifizierung und erforderliche Freigaben selbst abschließen. /Applications/pika.app öffnen, Dienstverbindung prüfen, Session einschalten, bei Bedarf Monitor OFF wählen und Deckel schließen. Schlafverhinderung wird vorher vorbereitet, Displaysteuerung danach angewendet. Bei offenem Deckel speichert Monitor nur die Wahl. Session OFF stellt die verwaltete Einstellung wieder her, ohne sofort das Display auszuschalten. Das Schließen des Fensters beendet die App nicht.
---
Notiere bei einem kurzen Test Startzeit und Fortschritt, und kontrolliere danach das Aufgabenprotokoll. Dies ist ein Prüfverfahren, keine Aussage über Tests aller Modelle. pmset -g assertions liest aktuelle Anforderungen, beweist aber weder Netzwerk- noch Deckelkontinuität. man caffeinate zeigt die lokal installierte Anleitung.
---
Eine Sperre ist nicht zwingend Schlaf. WLAN, VPN, API-Limits, wartende Freigaben oder App-Fehler können Arbeit unterbrechen. pika führt KI-Gespräche nicht weiter und repariert keine Verbindung. Ein laufender Mac gehört auf eine feste, belüftete Fläche, nicht in eine Tasche. Akku- oder Wärmeschutz sowie Dienstfehler können die Sitzung beenden; vollständiger Schutz vor Überhitzung oder Entladung wird nicht garantiert.
---
Vergleich vom Entwickler von no-sleep-pika mit eigener App. Grundlage sind Apple-Dokumente, das macOS-Handbuch caffeinate(8) und pika 1.0.13. Keine Empfehlung durch Apple oder KI-Anbieter. Nur so lange wach halten, wie die Aufgabe es benötigt.
''', ['pika herunterladen','Installationshilfe','MacBook mit geschlossenem Deckel','Vom no-sleep-pika-Entwickler verfasst; enthält unsere eigene App.'])

add('pt-BR', 'Como manter o Mac acordado: modo clamshell, caffeinate e pika',
'Compare alimentação e tampa fechada, comandos do Terminal e pika. Veja condições, limitações, bloqueio de tela e como finalizar cada método.',
'Escolha conforme a tarefa|1. Alimentação e modo clamshell|Ajustes com a tampa aberta|2. Usar caffeinate temporariamente|Tempo, tela e comandos|E com a tampa fechada?|3. Instalar pika|Verificar e encerrar|Bloqueio, rede e calor|Fontes e escopo',
'''
Tela apagada, bloqueio e repouso do sistema são estados diferentes. Um Mac bloqueado pode continuar trabalhando. Para monitor externo, considere clamshell; para uma tarefa temporária com a tampa aberta, caffeinate; para trabalhar fechado sem monitor externo, pika com seu serviço auxiliar.
---
Com a tampa aberta, conecte energia, monitor compatível, teclado e mouse e teste antes de fechar. Uma tela que fornece energia pode substituir o carregador conforme suas especificações. Só conectar o carregador não basta. A quantidade de monitores e a resolução dependem do modelo; autorize acessórios com a tampa aberta.
---
No notebook ligado à energia, procure em Ajustes do Sistema → Bateria → Opções a prevenção de repouso automático com a tela apagada. Nomes e localização variam por sistema e modelo. Preserve a senha de bloqueio. Esse ajuste não garante impedir o repouso provocado ao fechar a tampa. Anote o valor anterior.
---
Abra o Terminal e execute abaixo. caffeinate já vem no macOS, sem sudo. Impede repouso por inatividade, mas permite apagar a tela. Deixe o processo ativo e use Control+C nesse Terminal para terminar. Não exibir mensagens é normal. A solicitação é liberada quando o processo acaba; não é um ajuste permanente.
---
O primeiro exemplo dura 3.600 segundos, uma hora; o segundo também mantém a tela por 1.800 segundos, meia hora. Omita -d se não precisar da tela. O terceiro executa make de verdade até sua conclusão; use somente no projeto que pretende compilar. Um iniciador que sai imediatamente pode terminar antes da tarefa em segundo plano. Ao executar um programa, -t não é usado.
---
-i corresponde ao repouso ocioso do sistema, -d ao da tela. Fechar a tampa é outra condição e não há garantia de funcionamento fechado sem monitor. -s só vale com energia da tomada. -u informa atividade e pode acender a tela. Escolha opções pelo efeito documentado.
---
pika funciona no macOS 13 ou posterior, Apple Silicon e Intel. O PKG oficial completo instala app e serviço auxiliar administrador. Faça a autenticação e as aprovações do macOS pessoalmente. Abra /Applications/pika.app, confirme o serviço, ligue Session, escolha Monitor OFF se necessário e feche a tampa. A prevenção é preparada antes; a política de tela entra após fechar. Com a tampa aberta, Monitor só salva a preferência. Session OFF restaura o ajuste sem apagar imediatamente a tela. Fechar a janela não encerra o app.
---
Teste uma tarefa curta, registre a hora e confira os registros e o progresso depois. É um procedimento sugerido, não comprovação de todos os modelos. pmset -g assertions apenas consulta solicitações e não comprova continuidade da rede ou com a tampa fechada. man caffeinate mostra o manual local.
---
Bloqueio não significa necessariamente repouso. Wi-Fi, VPN, limites de API, aprovações e falhas de apps podem interromper tarefas; pika não continua conversas nem reconecta a rede. Use uma superfície firme e ventilada, nunca uma bolsa. Proteção térmica, bateria ou falha do serviço podem finalizar a sessão; não há garantia contra todo superaquecimento ou descarga.
---
Comparação escrita pelo criador de no-sleep-pika, incluindo seu próprio app. Baseada em Apple, manual macOS caffeinate(8) e documentação e implementação de pika 1.0.13. Não implica endosso da Apple ou de fornecedores de IA. Mantenha a sessão apenas pelo tempo necessário.
''', ['Baixar pika','Ajuda de instalação','Guia do MacBook fechado','Escrito pelo criador de no-sleep-pika; inclui nosso app.'])

add('ru', 'Как не дать Mac уснуть: закрытая крышка, caffeinate и pika',
'Сравниваем питание и режим clamshell, команды Терминала и pika. Условия работы, блокировка экрана, ограничения и завершение сеанса.',
'Выбор способа|1. Питание и режим clamshell|Настройки при открытой крышке|2. Временно использовать caffeinate|Время, экран и отдельная команда|А если закрыть крышку?|3. Установка pika|Проверка и завершение|Блокировка, сеть и нагрев|Источники и границы',
'''
Выключенный экран, блокировка и сон системы — разные состояния. Заблокированный Mac может продолжать работу. Для внешнего монитора сначала проверьте clamshell; для временной задачи с открытой крышкой — caffeinate; для закрытого ноутбука без монитора — pika со вспомогательной службой.
---
При открытой крышке подключите питание, совместимый монитор, клавиатуру и мышь, проверьте работу и затем закройте крышку. Монитор с питанием может заменить зарядное устройство согласно его характеристикам. Одного зарядного устройства недостаточно. Число дисплеев и разрешение зависят от модели. Разрешите подключение аксессуаров до закрытия крышки.
---
На подключённом к питанию ноутбуке найдите в системных настройках аккумулятора параметр предотвращения автоматического сна при выключенном экране. Названия зависят от версии macOS и модели. Пароль блокировки можно оставить. Это не универсальный запрет сна при закрытии крышки. Запишите прежнее значение.
---
Откройте Терминал и выполните команду ниже. caffeinate входит в macOS и не требует sudo. Он препятствует сну из-за бездействия, но экран может погаснуть. Оставьте процесс запущенным; для остановки нажмите Control+C в том же Терминале. Отсутствие вывода нормально. После завершения процесса запрос снимается.
---
Первый пример действует 3600 секунд, то есть час; второй также удерживает экран 1800 секунд, полчаса. Без необходимости уберите -d. Третий действительно запускает make и действует до его завершения: используйте только в проекте, который собираетесь собирать. Быстро завершающийся запускатель может закончить раньше фоновой задачи. При запуске команды параметр -t не используется.
---
-i относится к сну системы при бездействии, -d — к дисплею. Закрытие крышки является отдельным условием: эти параметры не гарантируют работу без внешнего монитора. -s действует только от сети питания; -u обозначает активность пользователя и может включить экран. Не копируйте комбинации флагов без понимания.
---
pika поддерживает macOS 13 и новее, Apple Silicon и Intel. Полный официальный PKG устанавливает приложение и административную вспомогательную службу. Подтверждения macOS выполните самостоятельно. Откройте /Applications/pika.app, проверьте соединение службы, включите Session, при необходимости выберите Monitor OFF и закройте крышку. Предотвращение сна готовится заранее, управление экраном применяется после закрытия. При открытой крышке Monitor только сохраняет выбор. Session OFF восстанавливает управляемую настройку без немедленного выключения экрана. Закрытие окна не завершает приложение.
---
Сначала запустите короткую задачу, отметьте время и затем проверьте журнал и прогресс. Это рекомендация для собственной проверки, а не заявление о тестировании всех моделей. pmset -g assertions только читает запросы и не доказывает непрерывность сети или работы с закрытой крышкой. man caffeinate открывает локальное руководство.
---
Блокировка сама по себе не доказывает сон. Wi-Fi, VPN, ограничения API, ожидание разрешений и ошибки приложений могут прервать работу. pika не продолжает разговоры ИИ и не восстанавливает сеть. Работающий Mac размещайте на твёрдой проветриваемой поверхности, не в сумке. Защита батареи и температуры или сбой службы могут завершить сеанс; полной гарантии от перегрева и разряда нет.
---
Сравнение подготовил разработчик no-sleep-pika, включая собственное приложение. Источники — Apple, руководство macOS caffeinate(8), документация и реализация pika 1.0.13. Это не рекомендация Apple или поставщиков ИИ. Завершайте сеанс после нужной задачи.
''', ['Скачать pika','Помощь с установкой','MacBook с закрытой крышкой','Материал разработчика no-sleep-pika с описанием собственного приложения.'])

add('id', 'Cara menjaga Mac tetap aktif: clamshell, caffeinate, dan pika',
'Bandingkan daya dan mode clamshell, perintah Terminal, serta pika. Pahami syarat tutup layar, penguncian, batasan, dan cara mengakhiri sesi.',
'Pilih sesuai tugas|1. Daya dan mode clamshell|Pengaturan saat tutup terbuka|2. Gunakan caffeinate sementara|Durasi, layar, dan perintah|Bagaimana saat tutup ditutup?|3. Instal pika|Periksa lalu akhiri|Kunci layar, jaringan, panas|Sumber dan cakupan',
'''
Layar mati, layar terkunci, dan sistem tidur berbeda. Mac terkunci masih dapat bekerja. Untuk monitor eksternal periksa clamshell; untuk tugas sementara dengan tutup terbuka gunakan caffeinate; untuk pekerjaan tertutup tanpa monitor eksternal pertimbangkan pika dengan layanan pembantunya.
---
Saat tutup terbuka, hubungkan daya, monitor yang didukung, keyboard dan mouse. Pastikan semuanya bekerja sebelum menutup. Monitor yang memasok daya mungkin menggantikan pengisi daya sesuai spesifikasi. Pengisi daya saja tidak membentuk konfigurasi ini. Jumlah dan resolusi layar bergantung pada model; setujui aksesori sebelum menutup.
---
Pada laptop tersambung daya, cari pengaturan pencegahan tidur otomatis saat layar mati di Pengaturan Sistem → Baterai → Opsi. Nama dan lokasinya berbeda menurut macOS dan model. Tetap aktifkan kata sandi penguncian. Pengaturan ini bukan jaminan mencegah tidur akibat menutup layar. Catat pilihan sebelumnya.
---
Buka Terminal dan jalankan perintah berikut. caffeinate sudah ada di macOS dan tidak memerlukan sudo. Ini mencegah tidur karena tidak ada aktivitas, tetapi layar boleh mati. Biarkan proses berjalan dan tekan Control+C pada Terminal tersebut untuk berhenti. Tidak ada keluaran adalah normal. Permintaan dilepas saat proses selesai.
---
Contoh pertama berlaku 3.600 detik atau satu jam. Contoh kedua juga menjaga layar selama 1.800 detik atau setengah jam; hapus -d jika tidak perlu. Contoh ketiga benar-benar menjalankan make sampai selesai, jadi gunakan hanya pada proyek yang hendak dibangun. Peluncur yang segera keluar dapat selesai sebelum tugas latar belakang. Jika menjalankan utilitas, -t tidak digunakan.
---
-i berlaku untuk tidur sistem karena tidak aktif, -d untuk layar. Menutup tutup merupakan kondisi berbeda, bukan jaminan operasi tanpa monitor. -s hanya berlaku pada daya AC; -u menyatakan aktivitas pengguna dan dapat menyalakan layar. Pilih opsi sesuai fungsi yang didokumentasikan.
---
pika mendukung macOS 13 ke atas, Apple Silicon dan Intel. PKG resmi lengkap memasang aplikasi dan layanan pembantu administrator. Selesaikan autentikasi dan persetujuan macOS sendiri. Buka /Applications/pika.app, periksa layanan, aktifkan Session, pilih Monitor OFF jika perlu, lalu tutup layar. Pencegahan tidur disiapkan sebelumnya; kebijakan layar diterapkan setelah ditutup. Saat terbuka, Monitor hanya menyimpan pilihan. Session OFF memulihkan pengaturan tanpa langsung mematikan layar. Menutup jendela tidak keluar dari aplikasi.
---
Uji tugas singkat, catat waktu, kemudian periksa log dan kemajuannya. Ini prosedur uji yang disarankan, bukan klaim semua model telah diuji. pmset -g assertions hanya membaca permintaan saat ini dan tidak membuktikan koneksi jaringan atau kesinambungan saat ditutup. man caffeinate membuka manual lokal.
---
Terkunci tidak selalu berarti tidur. Wi-Fi, VPN, batas API, persetujuan tertunda, atau kesalahan aplikasi dapat menghentikan pekerjaan; pika tidak melanjutkan percakapan AI atau memperbaiki jaringan. Gunakan permukaan keras dan berventilasi, bukan tas. Proteksi baterai, suhu atau gangguan layanan dapat mengakhiri sesi dan tidak menjamin semua panas berlebih atau kehabisan daya dapat dicegah.
---
Ditulis oleh pembuat no-sleep-pika dan mencakup aplikasi sendiri. Berdasarkan dokumen Apple, manual caffeinate(8) macOS, serta dokumentasi dan implementasi pika 1.0.13. Bukan dukungan resmi Apple atau penyedia AI. Jalankan hanya selama diperlukan.
''', ['Unduh pika','Bantuan instalasi','Panduan MacBook tertutup','Ditulis oleh pembuat no-sleep-pika; mencakup aplikasi kami.'])

add('hi', 'Mac को स्लीप में जाने से कैसे रोकें: क्लैमशेल, caffeinate और pika',
'पावर और क्लैमशेल मोड, Terminal कमांड और pika की तुलना। ढक्कन बंद करने की शर्तें, स्क्रीन लॉक, सीमाएँ और सत्र समाप्त करने का तरीका जानें।',
'काम के अनुसार तरीका चुनें|1. पावर और क्लैमशेल मोड|ढक्कन खुला हो तो सेटिंग देखें|2. caffeinate से अस्थायी रोक|समय, स्क्रीन और कमांड|क्या बंद ढक्कन पर भी काम होगा?|3. pika इंस्टॉल करें|जाँचें और समाप्त करें|लॉक, नेटवर्क और गर्मी|स्रोत और दायरा',
'''
स्क्रीन बंद होना, लॉक होना और सिस्टम स्लीप अलग स्थितियाँ हैं। लॉक Mac काम जारी रख सकता है। बाहरी मॉनिटर के लिए क्लैमशेल, खुले ढक्कन के अस्थायी काम के लिए caffeinate और बाहरी मॉनिटर के बिना बंद ढक्कन के काम के लिए सहायक सेवा सहित pika पर विचार करें।
---
ढक्कन खोलकर पावर, समर्थित मॉनिटर, कीबोर्ड और माउस जोड़ें और चलना जाँचकर ढक्कन बंद करें। पावर देने वाला मॉनिटर अपनी क्षमता के अनुसार चार्जर की जगह ले सकता है। सिर्फ चार्जर पर्याप्त नहीं। स्क्रीन की संख्या और रिजॉल्यूशन Mac मॉडल पर निर्भर हैं। एक्सेसरी की अनुमति पहले दें।
---
पावर से जुड़े लैपटॉप में System Settings → Battery → Options में स्क्रीन बंद होने पर अपने आप स्लीप रोकने का विकल्प देखें। नाम और स्थान संस्करण व मॉडल के अनुसार बदलते हैं। लॉक का पासवर्ड चालू रख सकते हैं। यह ढक्कन बंद करने से होने वाली स्लीप को हर स्थिति में नहीं रोकता। पुरानी सेटिंग लिख लें।
---
Terminal खोलकर नीचे का कमांड चलाएँ। caffeinate macOS में शामिल है; sudo की जरूरत नहीं। यह निष्क्रियता के कारण सिस्टम स्लीप रोकता है, स्क्रीन बंद हो सकती है। प्रक्रिया चलती रहने दें; उसी Terminal में Control+C से रोकें। कोई संदेश न दिखना सामान्य है। प्रक्रिया समाप्त होने पर उसका अनुरोध हट जाता है।
---
पहला उदाहरण 3,600 सेकंड यानी एक घंटा है। दूसरा 1,800 सेकंड यानी आधे घंटे तक स्क्रीन भी चालू रखता है; जरूरत न हो तो -d हटाएँ। तीसरा वास्तव में make चलाता है और उसके समाप्त होने तक रहता है। केवल जिस प्रोजेक्ट को बिल्ड करना है उसमें चलाएँ। तुरंत बंद होने वाला लॉन्चर असली बैकग्राउंड काम से पहले समाप्त हो सकता है। कमांड चलाने वाले रूप में -t लागू नहीं होता।
---
-i सिस्टम की निष्क्रियता वाली स्लीप के लिए है और -d स्क्रीन के लिए। ढक्कन बंद करना अलग शर्त है; बाहरी मॉनिटर के बिना चलने की गारंटी नहीं। -s केवल AC पावर पर लागू है। -u उपयोगकर्ता गतिविधि दर्शाता है और स्क्रीन जगा सकता है। विकल्प का अर्थ समझकर चुनें।
---
pika macOS 13 या नया, Apple Silicon और Intel पर काम करता है। आधिकारिक पूर्ण PKG ऐप और एडमिन सहायक सेवा इंस्टॉल करता है। macOS प्रमाणीकरण और आवश्यक अनुमति खुद पूरी करें। /Applications/pika.app खोलें, सेवा कनेक्शन जाँचें, Session ON करें, जरूरत हो तो Monitor OFF चुनें और ढक्कन बंद करें। स्लीप रोकने की तैयारी पहले होती है; स्क्रीन नीति बंद होने के बाद लागू होती है। खुले ढक्कन में Monitor सिर्फ चयन बचाता है। Session OFF प्रबंधित सेटिंग वापस करता है, स्क्रीन तुरंत बंद नहीं करता। विंडो बंद करने से ऐप बंद नहीं होता।
---
छोटा काम चलाकर समय लिखें और बाद में लॉग व प्रगति देखें। यह जाँच का सुझाव है, सभी मॉडल पर परीक्षण का दावा नहीं। pmset -g assertions वर्तमान अनुरोध केवल पढ़ता है; इससे नेटवर्क या बंद ढक्कन की निरंतरता सिद्ध नहीं होती। man caffeinate से स्थानीय मैनुअल पढ़ें।
---
लॉक का मतलब हमेशा स्लीप नहीं। Wi-Fi, VPN, API सीमा, अनुमति की प्रतीक्षा या ऐप की त्रुटि काम रोक सकती है। pika AI बातचीत आगे नहीं चलाता और नेटवर्क नहीं सुधारता। चलते Mac को हवादार ठोस सतह पर रखें, बैग में नहीं। बैटरी, ताप सुरक्षा या सेवा की समस्या सत्र समाप्त कर सकती है; हर ओवरहीटिंग या डिस्चार्ज रोकने की गारंटी नहीं।
---
यह तुलना no-sleep-pika के निर्माता ने अपनी ऐप सहित लिखी है। स्रोत Apple दस्तावेज, macOS का caffeinate(8) मैनुअल और pika 1.0.13 का सार्वजनिक दस्तावेज व कार्यान्वयन हैं। यह Apple या AI प्रदाता का समर्थन नहीं है। जरूरत खत्म हो तो सत्र बंद करें।
''', ['pika डाउनलोड करें','इंस्टॉलेशन सहायता','बंद MacBook की गाइड','no-sleep-pika निर्माता की अपनी ऐप सहित तुलना।'])

add('ar', 'كيف تمنع Mac من السكون: وضع الغطاء المغلق وcaffeinate وpika',
'مقارنة بين توصيل الطاقة ووضع الشاشة الخارجية وأوامر الطرفية وتطبيق pika، مع شروط إغلاق الغطاء وحدود كل طريقة وكيفية إنهائها.',
'اختر الطريقة المناسبة|1. الطاقة ووضع الغطاء المغلق|الإعدادات والغطاء مفتوح|2. منع السكون مؤقتًا باستخدام caffeinate|المدة والشاشة والأوامر|ماذا يحدث عند إغلاق الغطاء؟|3. تثبيت pika|التحقق وإنهاء الجلسة|القفل والشبكة والحرارة|المصادر والنطاق',
'''
إطفاء الشاشة وقفلها وسكون النظام حالات مختلفة. قد يستمر Mac المقفل بالعمل. للشاشة الخارجية تحقق من وضع الغطاء المغلق، وللمهام المؤقتة مع الغطاء المفتوح استخدم caffeinate، وللعمل المغلق دون شاشة خارجية يمكن استخدام pika مع خدمته المساعدة.
---
والغطاء مفتوح، صِل الطاقة وشاشة مدعومة ولوحة مفاتيح وفأرة وتحقق منها قبل الإغلاق. قد تغني الشاشة المزودة بالطاقة عن الشاحن وفق مواصفاتها. الشاحن وحده لا يكفي لهذا التكوين. عدد الشاشات ودقتها يعتمدان على طراز Mac، ووافق على توصيل الملحقات قبل إغلاق الغطاء.
---
على المحمول الموصول بالطاقة ابحث في إعدادات النظام والبطارية والخيارات عن منع السكون التلقائي عند إطفاء الشاشة. الأسماء والمواقع تختلف حسب النظام والطراز. يمكنك إبقاء كلمة مرور القفل. هذا ليس تجاوزًا شاملًا للسكون الناتج عن إغلاق الغطاء. سجّل الإعداد السابق لاستعادته.
---
افتح الطرفية وشغّل الأمر التالي. caffeinate مضمن في macOS ولا يحتاج sudo. يمنع سكون النظام بسبب الخمول، مع إمكانية إطفاء الشاشة. اترك العملية تعمل واضغط Control+C في الطرفية نفسها لإيقافها. عدم ظهور رسائل طبيعي، وينتهي طلب المنع بانتهاء العملية.
---
المثال الأول لمدة 3600 ثانية، أي ساعة. الثاني يمنع سكون الشاشة أيضًا لمدة 1800 ثانية، أي نصف ساعة؛ احذف -d إن لم تحتاجها. الثالث يشغّل make فعلًا ويستمر حتى نهايته، فاستخدمه فقط في مشروع تريد بناءه. المشغّل الذي يخرج فورًا قد ينتهي قبل المهمة الخلفية. عند تشغيل أمر لا يُستخدم -t.
---
الخيار -i يخص خمول النظام و-d يخص الشاشة. إغلاق الغطاء شرط مختلف، ولا تضمن هذه الخيارات العمل دون شاشة خارجية. يعمل -s فقط على طاقة AC، وقد يوقظ -u الشاشة لأنه يعلن نشاط المستخدم. اختر الخيارات حسب معناها الموثق.
---
يدعم pika نظام macOS 13 والأحدث وApple Silicon وIntel. ثبّت حزمة PKG الرسمية الكاملة التي تشمل التطبيق والخدمة المساعدة بصلاحيات المسؤول. أكمل المصادقة والموافقات بنفسك. افتح /Applications/pika.app وتحقق من الخدمة، ثم فعّل Session واختر Monitor OFF عند الحاجة وأغلق الغطاء. يُجهّز منع السكون مسبقًا وتُطبق سياسة الشاشة بعد الإغلاق. مع الغطاء المفتوح يُحفظ اختيار Monitor فقط. يعيد Session OFF الإعداد المُدار دون إطفاء الشاشة فورًا. إغلاق النافذة لا يُنهي التطبيق.
---
ابدأ بمهمة قصيرة وسجّل الوقت، ثم افحص السجل والتقدم بعد التجربة. هذه طريقة تحقق مقترحة وليست ادعاء اختبار جميع الطرازات. يقرأ pmset -g assertions الطلبات الحالية فقط ولا يثبت استمرار الشبكة أو العمل المغلق. يعرض man caffeinate الدليل المحلي.
---
القفل وحده لا يعني السكون. قد توقف المهمة مشكلات Wi-Fi وVPN وحدود API وانتظار الموافقات وأخطاء التطبيق. لا يكمل pika محادثات الذكاء الاصطناعي ولا يصلح الشبكة. ضع Mac العامل على سطح صلب وجيد التهوية، لا داخل حقيبة. قد تنهي حماية البطارية والحرارة أو أعطال الخدمة الجلسة، ولا تضمن منع كل سخونة أو نفاد للطاقة.
---
كتب مطور no-sleep-pika هذه المقارنة التي تتضمن تطبيقه. تستند إلى Apple ودليل macOS caffeinate(8) ووثائق وتنفيذ pika 1.0.13. لا تعني توصية من Apple أو مزودي الذكاء الاصطناعي. أبقِ الجلسة فقط للوقت اللازم.
''', ['تنزيل pika','مساعدة التثبيت','دليل MacBook بالغطاء المغلق','مقارنة كتبها مطور no-sleep-pika وتشمل تطبيقه.'])

add('vi', 'Cách giữ Mac không ngủ: clamshell, caffeinate và pika',
'So sánh nguồn điện và chế độ gập máy, lệnh Terminal và pika. Tìm hiểu điều kiện, giới hạn, khóa màn hình và cách kết thúc phiên.',
'Chọn theo công việc|1. Nguồn điện và chế độ clamshell|Cài đặt khi mở nắp|2. Dùng caffeinate tạm thời|Thời gian, màn hình và lệnh|Khi gập nắp thì sao?|3. Cài đặt pika|Kiểm tra rồi kết thúc|Khóa, mạng và nhiệt|Nguồn và phạm vi',
'''
Tắt màn hình, khóa màn hình và ngủ hệ thống khác nhau. Mac bị khóa vẫn có thể làm việc. Với màn hình ngoài hãy kiểm tra clamshell; với việc tạm thời khi mở nắp dùng caffeinate; với việc gập máy không có màn hình ngoài có thể dùng pika và dịch vụ trợ giúp.
---
Khi mở nắp, kết nối nguồn, màn hình hỗ trợ, bàn phím và chuột; kiểm tra rồi mới gập. Màn hình cấp nguồn có thể thay sạc theo thông số. Chỉ cắm sạc chưa đủ. Số màn hình và độ phân giải tùy model Mac. Chấp thuận phụ kiện trước khi gập nắp.
---
Trên laptop cắm nguồn, tìm tùy chọn ngăn tự động ngủ khi màn hình tắt trong Cài đặt hệ thống → Pin → Tùy chọn. Tên và vị trí tùy phiên bản và model. Có thể giữ mật khẩu khóa. Đây không phải cách đảm bảo chặn mọi giấc ngủ do gập nắp. Ghi lại cài đặt cũ.
---
Mở Terminal và chạy lệnh dưới. caffeinate có sẵn trong macOS, không cần sudo. Nó ngăn ngủ do không hoạt động, màn hình vẫn có thể tắt. Giữ tiến trình chạy và nhấn Control+C trong cùng Terminal để dừng. Không có thông báo là bình thường; yêu cầu kết thúc khi tiến trình thoát.
---
Ví dụ đầu kéo dài 3.600 giây, một giờ. Ví dụ thứ hai giữ cả màn hình trong 1.800 giây, nửa giờ; bỏ -d nếu không cần. Ví dụ cuối thực sự chạy make đến khi hoàn tất: chỉ dùng trong dự án định biên dịch. Trình khởi chạy thoát ngay có thể kết thúc trước công việc nền thật. Khi chạy một lệnh, -t không được sử dụng.
---
-i dành cho ngủ hệ thống do nhàn rỗi, -d dành cho màn hình. Gập nắp là điều kiện khác, không bảo đảm chạy khi không có màn hình ngoài. -s chỉ có hiệu lực với nguồn AC; -u báo hoạt động người dùng và có thể bật màn hình. Chọn tùy chọn theo chức năng được mô tả.
---
pika hỗ trợ macOS 13 trở lên, Apple Silicon và Intel. PKG chính thức đầy đủ cài ứng dụng và dịch vụ trợ giúp quản trị. Tự hoàn tất xác thực và phê duyệt macOS. Mở /Applications/pika.app, kiểm tra kết nối dịch vụ, bật Session, chọn Monitor OFF nếu cần rồi gập nắp. Ngăn ngủ được chuẩn bị trước, chính sách màn hình áp dụng sau khi gập. Khi mở nắp, Monitor chỉ lưu lựa chọn. Session OFF khôi phục cài đặt đã quản lý mà không tắt màn hình ngay. Đóng cửa sổ không thoát ứng dụng.
---
Thử việc ngắn, ghi giờ rồi kiểm tra nhật ký và tiến độ sau đó. Đây là quy trình đề xuất, không phải tuyên bố đã thử mọi model. pmset -g assertions chỉ đọc yêu cầu hiện tại, không chứng minh mạng hoặc hoạt động khi gập liên tục. man caffeinate hiển thị hướng dẫn trên máy.
---
Khóa không nhất thiết là ngủ. Wi-Fi, VPN, giới hạn API, chờ phê duyệt hay lỗi ứng dụng vẫn có thể ngắt việc. pika không tiếp tục hội thoại AI hoặc sửa mạng. Đặt Mac đang chạy trên mặt cứng thoáng khí, không trong túi. Bảo vệ pin, nhiệt hoặc lỗi dịch vụ có thể kết thúc phiên; không bảo đảm ngăn mọi quá nhiệt hay cạn pin.
---
Bài so sánh do nhà phát triển no-sleep-pika viết, gồm ứng dụng của chính mình. Dựa trên Apple, hướng dẫn macOS caffeinate(8), tài liệu và mã pika 1.0.13. Không phải sự bảo chứng của Apple hay nhà cung cấp AI. Chỉ duy trì phiên trong thời gian cần thiết.
''', ['Tải pika','Trợ giúp cài đặt','Hướng dẫn gập MacBook','Do nhà phát triển no-sleep-pika viết, có giới thiệu ứng dụng của mình.'])

add('th', 'วิธีทำให้ Mac ไม่พักเครื่อง: clamshell, caffeinate และ pika',
'เปรียบเทียบการต่อไฟและปิดฝา คำสั่ง Terminal และ pika พร้อมเงื่อนไข ข้อจำกัด การล็อกหน้าจอ และวิธีหยุดใช้งาน',
'เลือกวิธีตามงาน|1. ต่อไฟและใช้โหมด clamshell|ตั้งค่าเมื่อเปิดฝา|2. ใช้ caffeinate ชั่วคราว|ระยะเวลา หน้าจอ และคำสั่ง|ปิดฝาแล้วยังทำงานหรือไม่?|3. ติดตั้ง pika|ตรวจสอบและจบการทำงาน|การล็อก เครือข่าย และความร้อน|แหล่งข้อมูลและขอบเขต',
'''
หน้าจอดับ หน้าจอล็อก และระบบพักเครื่องเป็นคนละสถานะ Mac ที่ล็อกอาจยังทำงานได้ หากใช้จอนอกให้ตรวจสอบ clamshell หากเปิดฝาทำงานชั่วคราวใช้ caffeinate และหากปิดฝาโดยไม่มีจอนอกให้พิจารณา pika กับบริการช่วยเหลือ
---
เปิดฝาแล้วต่อไฟ จอที่รองรับ คีย์บอร์ดและเมาส์ ตรวจสอบก่อนปิดฝา จอที่จ่ายไฟได้อาจแทนที่ชาร์จตามสเปก การต่อที่ชาร์จอย่างเดียวไม่ครบเงื่อนไข จำนวนจอและความละเอียดขึ้นอยู่กับรุ่น Mac ควรอนุญาตอุปกรณ์เสริมก่อนปิดฝา
---
เมื่อเสียบไฟและเปิดฝา ให้หาตัวเลือกป้องกันพักเครื่องอัตโนมัติเมื่อหน้าจอดับใน System Settings → Battery → Options ชื่อและตำแหน่งต่างกันตามระบบและรุ่น เก็บรหัสผ่านหน้าจอล็อกไว้ได้ นี่ไม่ใช่การรับประกันว่าจะหยุดการพักเครื่องจากการปิดฝาทุกกรณี จดค่าเดิมก่อนเปลี่ยน
---
เปิด Terminal และรันคำสั่งด้านล่าง caffeinate มีใน macOS ไม่ต้องใช้ sudo ป้องกันระบบพักจากการไม่มีการใช้งาน แต่หน้าจอยังดับได้ ปล่อยกระบวนการทำงานไว้และกด Control+C ใน Terminal เดิมเพื่อหยุด ไม่มีข้อความแสดงถือว่าปกติ คำขอจะสิ้นสุดเมื่อกระบวนการจบ
---
ตัวอย่างแรกทำงาน 3,600 วินาทีหรือหนึ่งชั่วโมง ตัวอย่างที่สองรักษาหน้าจอด้วยเป็นเวลา 1,800 วินาทีหรือครึ่งชั่วโมง เอา -d ออกหากไม่ต้องการหน้าจอ ตัวอย่างสุดท้ายรัน make จริงจนจบ ใช้เฉพาะโปรเจกต์ที่ตั้งใจจะบิลด์ ตัวเรียกงานที่ออกทันทีอาจจบก่อนงานเบื้องหลังจริง เมื่อระบุคำสั่งให้รันจะไม่ใช้ -t
---
-i เกี่ยวกับระบบพักจากการว่าง ส่วน -d เกี่ยวกับหน้าจอ การปิดฝาเป็นอีกเงื่อนไข จึงไม่รับประกันการทำงานโดยไม่มีจอนอก -s มีผลเฉพาะไฟ AC และ -u แจ้งกิจกรรมผู้ใช้อาจทำให้หน้าจอติด เลือกตัวเลือกตามหน้าที่ที่อธิบายไว้
---
pika รองรับ macOS 13 ขึ้นไป Apple Silicon และ Intel PKG ทางการแบบเต็มติดตั้งแอปและบริการช่วยเหลือระดับผู้ดูแล ยืนยันตัวตนและอนุญาตใน macOS ด้วยตนเอง เปิด /Applications/pika.app ตรวจสอบบริการ เปิด Session เลือก Monitor OFF หากต้องการแล้วปิดฝา ระบบเตรียมป้องกันพักก่อนปิดฝา และใช้การควบคุมหน้าจอหลังปิด ขณะเปิดฝา Monitor แค่บันทึกตัวเลือก Session OFF คืนค่าที่จัดการโดยไม่ดับหน้าจอทันที การปิดหน้าต่างไม่ใช่การออกจากแอป
---
ลองงานสั้น จดเวลาแล้วดูบันทึกและความคืบหน้าหลังทดสอบ นี่เป็นขั้นตอนแนะนำ ไม่ใช่คำอ้างว่าทดสอบทุกรุ่นแล้ว pmset -g assertions อ่านคำขอปัจจุบันเท่านั้น ไม่ยืนยันความต่อเนื่องของเครือข่ายหรือการปิดฝา man caffeinate เปิดคู่มือในเครื่อง
---
การล็อกไม่ได้แปลว่าพักเสมอ ปัญหา Wi-Fi, VPN, ขีดจำกัด API, รออนุมัติหรือแอปผิดพลาดยังหยุดงานได้ pika ไม่สนทนา AI ต่อหรือซ่อมเครือข่าย วาง Mac ที่ทำงานบนพื้นแข็งอากาศถ่ายเท ไม่ใส่กระเป๋า การป้องกันแบตเตอรี่ ความร้อนหรือบริการขัดข้องอาจจบเซสชัน และไม่รับประกันป้องกันความร้อนหรือแบตหมดทุกกรณี
---
เขียนโดยผู้พัฒนา no-sleep-pika และรวมแอปของตนเอง อ้างอิง Apple คู่มือ macOS caffeinate(8) และเอกสารกับการทำงานของ pika 1.0.13 ไม่ใช่การรับรองจาก Apple หรือผู้ให้บริการ AI เปิดใช้งานเฉพาะช่วงที่จำเป็น
''', ['ดาวน์โหลด pika','ช่วยเหลือติดตั้ง','คู่มือปิดฝา MacBook','เขียนโดยผู้พัฒนา no-sleep-pika และแนะนำแอปของตนเอง'])
