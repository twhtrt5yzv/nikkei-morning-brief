# 目的
経営者との面談でそのまま見せられる「1枚もの資料」を2種類生成する。いずれも本日（実行当日）の実際のニュース・数値をフックにし、「円建て平準払い終身保険（主軸）×米ドル建て平準払い終身保険（補完）」の提案につなげる。

- 資料A（提案プレゼン）: けさのニュース → 課題 → 提案 → 反論封じ、を1枚で完結させる
- 資料B（メカニズム図解）: けさの経済の因果関係と、保険がどこで守りになるかを図解

# 設計思想（最重要）
1. **図解優先・文字最少。** 経営者が10秒眺めて構造が分かること。文は各要素の文字数上限を厳守。数字は本文でなく「数字バン（kpi）」で大きく見せる。
2. **論理を緻密に。** すべての主張は当日の検索済み事実に接続する。「事実→影響→対策」の因果に飛躍を作らない。誇張・断定しすぎ（「必ず増える」等）は禁止。「〜しやすい」「〜の局面」と正確に書く。
3. **反論を先回りして封じる。** 資料Aには経営者が必ず口にする疑問トップ3とその切り返しをQ&Aで載せる。切り返しは感情論でなく、事実か構造（平準払いの仕組み・リスクの所在）で返す。
   よくある反論の例: 「資金が長く拘束されるのでは」「投資信託や一時払いの方が増えるのでは」「今決める必要はないのでは（様子見したい）」「保険料が負担になるのでは」——この中からその日のニュースに最も関係する3つを選ぶ。

# 表現ルール（必守）
- 平易な言葉。専門用語には短い補足。
- 円建てを「主軸」、米ドル建てを「補完」とする関係。同列に扱う表現（二段構え・並列・2本柱等）は禁止。
- 商品名・利率・返戻率の数値仕様は書かない。
- ニュース・数値はWebSearchで確認済みの当日の事実のみ。作らない。取得できなかった指標はkpiに入れない。

# 出力形式（厳守）
- 使ってよいタグ: <div> <h2> <h3> <p> <ul> <li> <strong> <span>
- class は以下のテンプレートにあるものだけ。style属性・script・リンク禁止。前置き・コードフェンスなし。

## 資料A（shiryo_presentation.html.tmp）
<div class="sheet">
  <p class="sheet-date">〇年〇月〇日（曜）</p>
  <h2 class="sheet-title">（20字以内。その日のニュースに合わせ、経営者の損得に直結する言葉で）</h2>
  <div class="kpi-grid">
    <div class="kpi"><span class="kpi-num">（数値。例: 2.88%）</span><span class="kpi-label">（指標名6字以内）</span><span class="kpi-sub">（意味づけ8字以内。例: 30年ぶり高水準）</span></div>
    （×3個。その日最も物語る数字を選ぶ）
  </div>
  <div class="hook">📰 （けさのニュース1文・50字以内＋「つまり御社にとって〜」の1文・40字以内）</div>
  <h3>いま、会社のお金に起きていること</h3>
  <div class="problem-grid">
    <div class="box"><span class="box-title">（課題を8字以内）</span>（補足20字以内）</div>
    （×3個）
  </div>
  <h3>ご提案：お金の置き場所の役割分担</h3>
  <div class="plan-duo">
    <div class="plan-main"><span class="plan-label">主軸</span><strong>円建て 平準払い終身保険</strong><p>（役割。60字以内）</p></div>
    <div class="plan-sub"><span class="plan-label">補完</span><strong>米ドル建て 平準払い終身保険</strong><p>（役割。50字以内。円建てを支える位置づけを明確に）</p></div>
  </div>
  <div class="points"><strong>「平準払い」だからできること</strong>
    <ul>（3点・各30字以内。一時払いとの違い1点、変額保険との違い1点を必ず含む）</ul>
  </div>
  <h3>社長がよく口にされる疑問に、先にお答えします</h3>
  <div class="qa">
    <div class="qa-item"><span class="q">（想定反論。20字以内）</span><span class="a">（事実か構造で切り返す。50字以内）</span></div>
    （×3個。その日のニュースに最も関係する反論を選ぶ）
  </div>
  <div class="cta">（次の一歩。30字以内。例: まずは決算書ベースの30分シミュレーションを）</div>
</div>

## 資料B（shiryo_mechanism.html.tmp）
<div class="sheet">
  <p class="sheet-date">〇年〇月〇日（曜）</p>
  <h2 class="sheet-title">なぜ「今」なのか——けさのニュースが御社に届くまで</h2>
  <div class="kpi-grid">（資料Aと同じ形式で3個。同じ数字でよい）</div>
  <div class="flow">
    <div class="flow-step"><strong>世の中：</strong>（40字以内）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step"><strong>市場：</strong>（40字以内。平易な補足つき）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step"><strong>銀行・物価：</strong>（40字以内）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step highlight"><strong>御社：</strong>（P/L・B/Sへの最終影響。50字以内）</div>
  </div>
  <h3>この流れのどこで「保険」が守りになるか</h3>
  <div class="plan-duo">
    <div class="plan-main"><span class="plan-label">主軸</span><strong>円建て 平準払い終身保険</strong><p>（フローのどの影響をどう和らげるか。60字以内）</p></div>
    <div class="plan-sub"><span class="plan-label">補完</span><strong>米ドル建て 平準払い終身保険</strong><p>（円だけでは守れない部分。50字以内）</p></div>
  </div>
  <p class="note">（締め1文・40字以内。今動く理由）</p>
</div>
