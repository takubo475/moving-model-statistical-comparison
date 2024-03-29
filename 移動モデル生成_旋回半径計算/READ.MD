・本プログラムは、googleロケーション履歴から得られる緯度経度、日時を元に逆強化学習と呼ばれる対象者の軌道から報酬を算出する手法を用いて計算した結果から、強化学習を行い移動データを再現するプログラムである。
このリポジトリには、以下のフォルダが含まれています。

・事前データの準備-->googleロケーション履歴をjson形式でダウンロードしたものをフォルダ内に配置することで、jsonファイル内から日時,緯度,軽度を抽出しデータベースファイルに変換する。
・移動モデルの逆強化学習-->事前データの準備で作成したデータベースファイルを元に1時間ごと(0時から23時)で逆強化学習を行う
・移動モデルの強化学習-->移動モデルの逆強化学習で計算した結果(excelファイル)を入力として使用しQ学習を用いた強化学習を行う

実験の流れ
目次
・googleロケーション履歴をダウンロード
    https://takeout.google.com/?pli=1
    から、ロケーション履歴をjson形式でダウンロードする。(選択肢に出てこない場合機能を有効にしていない可能性があるため、以下を参考に有効化する)
    https://support.google.com/accounts/answer/3118687?hl=ja#:~:text=%E3%83%AD%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%B1%A5%E6%AD%B4%E3%82%92%E3%82%AA%E3%83%B3%E3%81%BE%E3%81%9F%E3%81%AF%E3%82%AA%E3%83%95%E3%81%AB%E3%81%99%E3%82%8B&text=Google%20%E3%82%A2%E3%82%AB%E3%82%A6%E3%83%B3%E3%83%88%E3%81%AE%20%5B%E3%83%AD%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3%E5%B1%A5%E6%AD%B4,%E3%82%AA%E3%83%B3%E3%81%BE%E3%81%9F%E3%81%AF%E3%82%AA%E3%83%95%E3%81%AB%E3%81%97%E3%81%BE%E3%81%99%E3%80%82

・ダウンロードしたロケーション履歴をデータベースファイルに変換
  ダウンロードしたjsonファイルを、事前データの準備フォルダ内に移動しjson2dbを実行する。
  実行後データベースファイルがが生成または更新される。

・逆強化学習を実行
  jsonから変換したデータベースファイルを、移動モデルの逆強化学習フォルダ内に移動しstart.bat(windows専用)を実行する。この時main.py内の30.31行目の
        state_features = np.vstack([self.state_to_feature2(s)
                                   for s in range(self.n_states)])
  の"self.state_to_feature"が"self.state_to_feature"であれば、報酬=thetaとして計算する。また、self.state_to_feature2"に変更することで、報酬=theta×fs(平均訪問回数)として逆強化学習を実行する。
  
  start.batを起動後は、実験名を入力しEnterを押すことで24個のコマンドプロンプロが起動し各時間に対して逆強化学習が行われる。

  すべての処理が終了すると./移動モデルの逆強化学習/result/実験名 でフォルダが生成されているため、その中から各時間のエクセルファイルを抜き出し１つのフォルダに格納する。

・強化学習を実行
  逆強化学習の結果をまとめたフォルダを./移動モデルの強化学習/input_data内にフォルダを移動させる。
  移動後、main.dbを削除もしくは初期化する。
  #本プログラムでは、移動経路を報酬の値ごとに足切りをし短時間で報酬が一定以上の値間を結ぶ最短経路を結んでいる。この時移動先と出発地点を決定後、各地点から最短経路を計算すると報酬の少ない地点を選択する可能性や斜めに移動せず直線的な移動経路となってしまうため、報酬をネットワークグラフに変換し報酬が基準値より低いノードをネットワークから切り離し最短経路を計算することで最短経路を計算した場合にすべての地点を選択肢に入れた最短経路探索で得られる報酬以上の報酬を獲得することができる。
  以上の処理を実行するために./移動モデルの強化学習/network.pyを実行し各地点間の経路を決定し保存する。
  計算した経路を./移動モデルの強化学習/main.pyを実行し強化学習をする。
  実行後は、./移動モデルの強化学習/main.db内に[id,スタート地点,ゴール地点,報酬,step数,移動ルート]が保存され./移動モデルの強化学習/step_reward.pngには１エピソードを1440(60分*24時間)ステップと仮定した場合の累積報酬が記録される。
  この結果を、./移動モデルの強化学習/visualization.pyを実行しmp4ファイルとして保存することによって可視化する。

以上が本プログラムの実行手順となる。

各プログラムの大まかな働き
./事前データの準備/jspm2db.py-->jsonファイルからデータを抽出しデータベールファイルに保存

./移動モデルの逆強化学習/main.py-->逆強化学習を行うメインプログラム。報酬の計算や状態価値関数を用いて得られたポリシーとエキスパートの方策の差を計算するなどを行っている。
./移動モデルの逆強化学習/db2expart.py-->データベースファイルからエキスパートの軌道をグリッド形式で読み込み値を返す。
./移動モデルの逆強化学習/value_interation.py-->入力された報酬から予測される方策(Policy)を計算する

./移動モデルの強化学習/network.py-->逆強化学習で計算された結果をもとに、訪問地点を決定し各訪問地点間のルートと報酬を記録する。
./移動モデルの強化学習/main.py-->強化学習を実行するためのメインプログラム。
./移動モデルの強化学習/qagent.py-->Qテーブルを更新するためのエージェント。
./移動モデルの強化学習/qtable.py-->各エージェントが共有するQテーブルを設定する。
./移動モデルの強化学習/visualization.py-->強化学習を行った結果を動画に変換するプログラム。
