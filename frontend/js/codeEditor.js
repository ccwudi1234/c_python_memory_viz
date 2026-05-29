let editor = null;

export function initEditor(initialCode, mode) {
  const textarea = document.getElementById('codeEditor');
  editor = CodeMirror.fromTextArea(textarea, {
    value: initialCode,
    mode,
    theme: 'dracula',
    lineNumbers: true,
    indentUnit: 2,
    tabSize: 2,
    indentWithTabs: false,
    autofocus: true,
    styleActiveLine: true,
    lineWrapping: true,
    extraKeys: {
      'Ctrl-Space': 'autocomplete',
      'Ctrl-/': 'toggleComment'
    }
  });
  editor.setValue(initialCode);
}

export function getCode() {
  return editor ? editor.getValue() : document.getElementById('codeEditor').value;
}

export function setCode(code) {
  if (editor) {
    editor.setValue(code);
    editor.refresh();
  } else {
    document.getElementById('codeEditor').value = code;
  }
}

export function setMode(mode) {
  if (!editor) return;
  editor.setOption('mode', mode);
}
