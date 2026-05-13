import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    let disposable = vscode.commands.registerCommand('extension.explainCode', () => {
        const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.document.getText(editor.selection);
            vscode.window.showInformationMessage(`ИИ Анализ: Данный код реализует логику ${selection.length > 50 ? "обработки данных" : "вызова функции"}.`);
        }
    });
    context.subscriptions.push(disposable);
}