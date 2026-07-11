# 目的
経営者との面談でそのまま見せられる「1枚もの資料」を2種類生成する。いずれも本日（実行当日）の実際のニュース・数値をフックにし、「円建て平準払い終身保険（主軸）×外貨（米ドル）建て平準払い終身保険（補完）」の提案につなげる。

- 資料A（提案プレゼン）: けさのニュース → 会社のお金の課題 → 提案、を1枚で導く
- 資料B（メカニズム図解）: けさの経済の因果関係と、保険がどこで守りになるかを図解

# 表現ルール（必守）
- 経済が苦手な経営者が10秒眺めて分かること。1枚あたりの文字量は最小限。専門用語には短い補足。
- 円建てを「主軸」、米ドル建てを「補完」とする関係。同列に扱う表現（二段構え・並列・2本柱等）は禁止。
- 商品名・利率・返戻率の数値仕様は書かない。
- ニュース・数値はWebSearchで確認済みの当日の事実のみ。作らない。

# 出力形式（厳守）
- 使ってよいタグ: <div> <h2> <h3> <p> <ul> <li> <strong> <span>
- class は以下の指定のものだけを使う。style属性・script・リンクは禁止。
- 前置き・コードフェンスなし。資料Aと資料Bをそれぞれ別ファイルに出力する。

## 資料A（shiryo_presentation.html.tmp）の構造テンプレート
<div class="sheet">
  <p class="sheet-date">〇年〇月〇日（曜）</p>
  <h2 class="sheet-title">（その日のニュースに合わせた平易で刺さるタイトル）</h2>
  <div class="hook">📰 けさのニュース：（1〜2文。数値入り。なぜ社長に関係があるかまで）</div>
  <h3>いま、会社のお金に起きていること</h3>
  <div class="problem-grid">
    <div class="box"><span class="box-title">（課題1見出し）</span>（1文）</div>
    <div class="box"><span class="box-title">（課題2見出し）</span>（1文）</div>
    <div class="box"><span class="box-title">（課題3見出し）</span>（1文）</div>
  </div>
  <h3>ご提案：お金の置き場所の役割分担</h3>
  <div class="plan-main"><span class="plan-label">主軸</span><strong>円建て 平準払い終身保険</strong><p>（役割を2文以内で）</p></div>
  <div class="plan-sub"><span class="plan-label">補完</span><strong>米ドル建て 平準払い終身保険</strong><p>（役割を2文以内で。あくまで円建てを支える位置づけ）</p></div>
  <div class="points"><strong>「平準払い」だからできること</strong>
    <ul>（3点。うち1点は一時払いとの違い、1点は変額保険との違いが伝わる内容に）</ul>
  </div>
  <div class="cta">（次の一歩の提案。例：決算書ベースの金額シミュレーション30分）</div>
</div>

## 資料B（shiryo_mechanism.html.tmp）の構造テンプレート
<div class="sheet">
  <p class="sheet-date">〇年〇月〇日（曜）</p>
  <h2 class="sheet-title">なぜ「今」なのか——けさのニュースが御社に届くまで</h2>
  <div class="flow">
    <div class="flow-step"><strong>世の中：</strong>（けさのニュース・指標。数値入り）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step">（市場の反応。平易な補足つき）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step">（銀行・物価など身近な段階）</div>
    <div class="flow-arrow">▼</div>
    <div class="flow-step highlight"><strong>御社：</strong>（P/L・B/Sへの最終影響。「借りても損、置いても損」等）</div>
  </div>
  <h3>この流れのどこで「保険」が守りになるか</h3>
  <div class="plan-main"><span class="plan-label">主軸</span><strong>円建て 平準払い終身保険</strong><p>（上のフローのどの影響を、どう和らげるか）</p></div>
  <div class="plan-sub"><span class="plan-label">補完</span><strong>米ドル建て 平準払い終身保険</strong><p>（円だけでは守れない部分をどう補うか）</p></div>
  <p class="note">（1文の締め。今動く理由）</p>
</div>
