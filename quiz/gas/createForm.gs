/**
 * createQuiz: questions.gs と config.gs を読み込み、Google フォーム小テストを生成する。
 *
 * 使い方(README.md §B 参照):
 *   1. GAS エディタで「実行する関数」を `createQuiz` にして実行
 *   2. 実行ログに表示される Edit URL をブラウザで開く
 *   3. フォーム編集画面で「成績を送信直後に表示」と「正解 / 不正解 / 点数を表示」を手動 ON
 *      (GAS の API では切り替えられないため)
 *
 * config.gs の `CONFIG` と questions.gs の `QUESTIONS` を参照する。
 */

function createQuiz() {
  validateQuestions_(QUESTIONS, CONFIG);

  const form = FormApp.create(CONFIG.title);
  form.setDescription(CONFIG.description);
  form.setIsQuiz(true);

  // メール収集 (Verified 優先): サインイン済み Google アカウントから
  // 自動取得し、回答者の手入力を不要にする。古い GAS 環境では setCollectEmail(true)
  // にフォールバック(この場合は手入力欄になる)。
  if (typeof FormApp.EmailCollectionType !== 'undefined') {
    form.setEmailCollectionType(FormApp.EmailCollectionType.VERIFIED);
  } else {
    form.setCollectEmail(true);
  }

  form.setLimitOneResponsePerUser(true);
  form.setShowLinkToRespondAgain(false);
  form.setAllowResponseEdits(false);
  form.setShuffleQuestions(CONFIG.shuffleQuestions);

  addNameAndStudentNumber_(form, CONFIG);

  QUESTIONS.forEach((q, i) => {
    addMultipleChoiceQuestion_(form, q, i + 1, CONFIG);
  });

  Logger.log('=========================================');
  Logger.log('フォームを作成しました。');
  Logger.log('Edit URL    : ' + form.getEditUrl());
  Logger.log('Public URL  : ' + form.getPublishedUrl());
  Logger.log('=========================================');
  Logger.log('⚠ フォーム編集画面で以下を手動で ON にしてください:');
  Logger.log('  - 設定 > テスト > 「成績の表示」 → 送信直後');
  Logger.log('  - 設定 > テスト > 回答者が見る項目 → 間違えた質問 / 正解 / 点数 すべて ON');
  Logger.log('=========================================');
}

/* ============ 補助関数 ============ */

function addNameAndStudentNumber_(form, config) {
  form.addTextItem()
    .setTitle('氏名')
    .setHelpText('姓名をフルネームで入力してください。')
    .setRequired(true);

  form.addTextItem()
    .setTitle('出席番号')
    .setHelpText('1 〜 ' + config.studentNumberMax + ' の整数で入力してください。')
    .setValidation(
      FormApp.createTextValidation()
        .setHelpText('1 〜 ' + config.studentNumberMax + ' の整数で入力してください。')
        .requireNumberBetween(1, config.studentNumberMax)
        .build()
    )
    .setRequired(true);
}

function addMultipleChoiceQuestion_(form, q, displayNumber, config) {
  const item = form.addMultipleChoiceItem();
  item.setTitle('Q' + displayNumber + '. ' + q.text);
  item.setPoints(config.pointsPerQuestion);
  item.setRequired(true);

  // choices をシャッフル(または固定)し、正答フラグを保ったまま渡す
  const indexed = q.choices.map((text, idx) => ({
    text: text,
    isCorrect: idx === q.correctIndex,
  }));
  const ordered = config.shuffleChoices ? shuffle_(indexed) : indexed;

  item.setChoices(
    ordered.map(c => item.createChoice(c.text, c.isCorrect))
  );

  const feedbackText =
    '正解: ' + q.choices[q.correctIndex] + '\n\n' + q.explanation;

  const feedback = FormApp.createFeedback().setText(feedbackText).build();
  item.setFeedbackForCorrect(feedback);
  item.setFeedbackForIncorrect(feedback);
}

function shuffle_(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const tmp = a[i];
    a[i] = a[j];
    a[j] = tmp;
  }
  return a;
}

/**
 * 設問データの妥当性を実行前にチェック。問題があれば例外を投げる。
 * フォームを作ってしまってから「壊れた設問」に気付くと修復が面倒なので前段で止める。
 */
function validateQuestions_(questions, config) {
  if (!Array.isArray(questions) || questions.length === 0) {
    throw new Error('QUESTIONS が空です。questions.gs に設問を定義してください。');
  }
  questions.forEach((q, i) => {
    const tag = '[Q' + (i + 1) + ' id=' + (q.id || '?') + ']';
    if (typeof q.text !== 'string' || q.text.length === 0) {
      throw new Error(tag + ' text が空です。');
    }
    if (!Array.isArray(q.choices) || q.choices.length !== 5) {
      throw new Error(tag + ' choices は 5 要素必須(現状: ' + (q.choices ? q.choices.length : '無し') + ')');
    }
    const uniq = new Set(q.choices);
    if (uniq.size !== q.choices.length) {
      throw new Error(tag + ' choices に重複があります。');
    }
    if (
      typeof q.correctIndex !== 'number' ||
      q.correctIndex < 0 ||
      q.correctIndex >= q.choices.length
    ) {
      throw new Error(tag + ' correctIndex が choices の範囲外です。');
    }
    if (typeof q.explanation !== 'string' || q.explanation.length === 0) {
      throw new Error(tag + ' explanation が空です。');
    }
  });

  const expectedTotal = questions.length * config.pointsPerQuestion;
  Logger.log(
    '設問チェック OK: ' + questions.length + ' 問 × ' +
    config.pointsPerQuestion + ' 点 = ' + expectedTotal + ' 点'
  );
}
