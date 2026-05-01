/**
 * 小テスト設定
 *
 * createForm.gs / questions.gs と同じ GAS プロジェクト内に置く。
 * GAS は .gs ファイル間で global namespace を共有するため、ここで定義した
 * `CONFIG` は createForm.gs から直接参照できる。
 */

const CONFIG = {
  // フォームのタイトル(Drive 上のファイル名にもなる)
  title: '情報I 小テスト(サンプル)',

  // フォーム冒頭の説明文。受験要領などを書く
  description: [
    '出題範囲: 知的財産権 / 個人情報 / 情報社会の法律 / 情報セキュリティ',
    '問数: 25 問 / 配点: 1 問 4 点 / 計 100 点',
    '回答は 1 回のみ。送信直後に正解・解説・点数が表示されます。',
    '',
    '回答前に氏名と出席番号を入力してください。',
  ].join('\n'),

  // 各設問の配点
  pointsPerQuestion: 4,

  // 出席番号バリデーション(整数 1〜N)
  studentNumberMax: 50,

  // 設問の並び替え。単元バランス維持のため既定 false。
  shuffleQuestions: false,

  // 選択肢のシャッフル。コピペ対策のため既定 true。
  shuffleChoices: true,
};
