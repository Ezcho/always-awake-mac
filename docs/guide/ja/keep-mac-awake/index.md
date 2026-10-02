Source: https://no-sleep-pika.online/guide/ja/keep-mac-awake/
Language: ja

MAC GUIDE · 2026-10-02

# Macをスリープさせない方法：クラムシェル・caffeinate・pika

電源と外部ディスプレイ、ターミナルのcaffeinate、pikaの3つの方法を比較。画面ロックとスリープの違い、ふたを閉じる条件、作業の確認方法を説明します。

## 目的に合う方法を選ぶ

画面の消灯、画面ロック、システムのスリープは別の状態です。ロック中でも処理は動くことがあります。外部画面で作業するならクラムシェル、一時的な開いた状態の処理ならcaffeinate、外部画面なしで閉じて動かすならpikaの補助サービスを検討します。

## 1. 電源接続とクラムシェルモード

ふたを開けた状態で電源、対応する外部ディスプレイ、キーボードとマウスを接続し、動作を確認してから閉じます。給電対応のディスプレイでは仕様により充電器を兼ねられます。充電器だけではこの構成になりません。画面数や解像度はMacのモデルによって異なり、アクセサリの許可も必要な場合があります。

[Apple · External displays](https://support.apple.com/en-us/102501)

## ふたを開けて使う場合の設定

電源接続中でふたを開けている場合は、システム設定のバッテリーのオプションで、画面がオフのときの自動スリープを防ぐ設定を確認します。名称や場所はOSと機種によります。パスワード要求は維持できます。この設定がふたを閉じたときのスリープも必ず防ぐわけではありません。

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. caffeinateで一時的にスリープを防ぐ

ターミナルを開いて次のコマンドを実行します。caffeinateはmacOSに含まれ、sudoは不要です。入力がないために起きるシステムのスリープを防ぎます。ターミナルを動かしたままにし、終了はその画面でControl+C。画面自体は消灯できます。永続設定ではなく、プロセス終了で要求も解除されます。

```
caffeinate -i
```

## 時間・画面・コマンドに合わせた使い方

最初の例は3,600秒（1時間）、次は画面のスリープも含めて1,800秒（30分）です。画面が不要なら-dを省きます。最後の例はmakeを実際に起動し、その終了まで維持します。ビルドするつもりのプロジェクトでのみ実行してください。別プロセスを起動してすぐ終了するランチャーでは、実作業より先に解除される場合があります。コマンドを指定した場合-tは使われません。

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## ふたを閉じても動く？

-iはアイドル時のシステムスリープ、-dは画面のスリープが対象です。ふたを閉じる動作は別条件で、外部画面なしの動作保証ではありません。-sはAC電源でのみ有効です。-uはユーザー操作を通知して画面を点灯させる場合があり、消灯させたい目的には合わないことがあります。

## 3. pikaをインストールする

pikaはmacOS 13以降のApple SiliconとIntelに対応します。公式サイトの統合PKGでアプリと管理者補助サービスをインストールし、macOSの認証や必要な承認を完了します。/Applications/pika.appを開き、補助サービス接続を確認。Session ON、必要ならMonitor OFFを選び、ふたを閉じます。スリープ防止は事前に準備され、画面制御は閉じてから適用されます。開いた状態でMonitorを変更しても即座に消灯しません。Session OFFで管理した設定を復元します。ウィンドウを閉じてもアプリは終了しません。

[pikaをダウンロード · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[インストール案内](https://no-sleep-pika.online/install/)

## 動作確認と終了

短い処理で開始時刻を記録し、閉じた状態を試してからログと進行状況を確認します。全モデルでの動作確認済みという意味ではありません。pmset -g assertionsは現在の要求を読むだけで、通信やふたを閉じた状態の継続を証明するものではありません。詳細はman caffeinateで確認できます。

```
pmset -g assertions
```

```
man caffeinate
```

## ロック・通信・発熱の注意点

ロックだけで処理停止とは判断できません。通信障害、VPN、API制限、承認待ち、アプリの停止は別問題で、pikaはAI会話や通信の復旧を代行しません。動作中は通気のよい硬い面に置き、バッグに入れないでください。電池・熱の保護や補助サービス障害でSessionが終了する場合があり、すべての過熱や放電を防げる保証はありません。

## 参考資料と対象範囲

no-sleep-pikaの開発者による自社製品を含む比較です。Appleの資料とMacに付属するcaffeinate(8)マニュアルを参考にし、pikaは公開版1.0.13の仕様を説明しています。AppleやAI提供企業による推薦ではありません。必要な時間だけ使い、終了後は通常の状態に戻しましょう。

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

pika開発者による、自社アプリを含む比較です。

[pikaをダウンロード](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[ふたを閉じたMacBookのガイド →](https://no-sleep-pika.online/guide/ja/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/ja/keep-mac-awake/index.md)
