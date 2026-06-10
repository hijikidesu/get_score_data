# get_score_data
SDVX譜面保管所(https://sdvx.in/ )にある譜面画像を譜面データに変換するツールです。

# 作成経緯
研究でSOUND VOLTEXの譜面データが必要だったのですが、インターネット上には画像形式の譜面データしか存在しなかったため、このツールを作成しました。

# 使い方
1."Download ZIP"や "git clone"でコードをダウンロード

2.`python get_score.py`を実行

3.https://sdvx.in/ にアクセスして、譜面データが欲しい楽曲の譜面画像htmlのURLをコピーします

4.コピーしたURLと曲名を入力して「譜面データ取得」を押す

<img width="843" height="220" alt="Image" src="https://github.com/user-attachments/assets/d2d44f46-3144-4b8f-89e3-2a0707864e4a" />

5.「譜面データ読み取り完了!」というポップアップがでれば成功

# 動作確認環境
・conda 24.11.3

・python 3.14.3

・opencv 4.12.0 

・numpy 2.4.2

・pandas 3.0.0

・pillow 12.0.0

・tk 8.6.15 

・customtkinter 5.2.2 

・selenium 4.41.0 

・requests 2.32.5 

# 注意点
`get_score.py` と `get_score_method.py` は、必ず同じディレクトリ内に配置してください。

# 認知しているバグ
・SOUND VOLTEX∇で初登場した楽曲の譜面画像が上手く読み込めない

・ロングノーツを上手く読み取れないときがある

・つまみも上手く読み取れないときがある

# 困ってること
・48分など細かすぎる譜面間隔のノーツに対応できない

・普通じゃない変拍子(ex:8/11拍子)の楽曲に対応できない
