/**
 * 設問データ(正本)
 *
 * 各オブジェクトは以下のフィールドを持つ:
 *  - id            : ユニーク ID。形式 `q-{単元番号}-{連番}`(例: q-04-001)
 *  - unit          : 出題単元(`04-intellectual-property` 等の lecture スラッグ)
 *  - text          : 設問本文。___ で空欄を示す
 *  - choices       : 5 択の配列。順序は何でも良い(生成時にシャッフルされる)
 *  - correctIndex  : choices 内の正答 index(0-based)
 *  - explanation   : 解説文(60〜120 字目安。条文・概念で根拠を示す)
 *  - sourceRef     : 出典(例: `lec07 学習ノート ①` / `_source/...問題Word.docx 1章 p.X 第Y問`)
 *  - origin        : 'existing'(既存問題ベース) | 'original'(lecture 由来オリジナル)
 *
 * 設問の順序がそのままフォームの出題順になる(CONFIG.shuffleQuestions = false の場合)。
 * 単元バランスを保つよう順序を組むこと。
 *
 * --------
 * Phase 1 状況: サンプル 3 問のみ。動作確認用。
 * Phase 2 で 25 問(04: 6 / 05: 6 / 06: 6 / 07: 7)に拡張する。
 */

const QUESTIONS = [
  {
    id: 'q-04-001',
    unit: '04-intellectual-property',
    text: '日本の著作権法において、著作権は ___ に発生する。',
    choices: [
      '文化庁長官が認可した時',
      '創作と同時に',
      '出版社と契約した時',
      '特許庁に登録された時',
      '著作物が公表された時',
    ],
    correctIndex: 1,
    explanation:
      '著作権は「無方式主義」を採り、創作と同時に発生する(著作権法 17 条 2 項)。' +
      '登録や申請は権利発生の要件ではなく、著作物の創作という事実そのものが権利を生む。',
    sourceRef: 'lec04 学習ノート ① 著作権の発生',
    origin: 'original',
  },
  {
    id: 'q-05-001',
    unit: '05-personal-information',
    text:
      '個人情報保護法において、本人の同意なく取得することが原則禁止される、' +
      '人種・信条・病歴等を含む情報を ___ という。',
    choices: [
      '個人識別符号',
      '匿名加工情報',
      '要配慮個人情報',
      '個人関連情報',
      '仮名加工情報',
    ],
    correctIndex: 2,
    explanation:
      '個人情報保護法 2 条 3 項に定める「要配慮個人情報」。人種・信条・病歴・犯罪歴等を含み、' +
      '取得には原則として本人同意が必要(法 17 条 2 項)。',
    sourceRef: 'lec05 学習ノート ② 要配慮個人情報',
    origin: 'original',
  },
  {
    id: 'q-07-001',
    unit: '07-information-security',
    text:
      '情報セキュリティの 3 要素(CIA)のうち、' +
      '認可された者だけが情報にアクセスできることを保証する性質を ___ という。',
    choices: [
      '可用性(Availability)',
      '完全性(Integrity)',
      '真正性(Authenticity)',
      '機密性(Confidentiality)',
      '否認防止(Non-repudiation)',
    ],
    correctIndex: 3,
    explanation:
      'CIA の Confidentiality(機密性)。Integrity(完全性)は情報の改ざん防止、' +
      'Availability(可用性)は必要時のアクセス保証を指し、3 つを区別して扱う。',
    sourceRef: 'lec07 学習ノート ① CIA 三要素',
    origin: 'original',
  },
];
