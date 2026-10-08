'use strict';
(() => {
  document.querySelectorAll('pre.codeblock').forEach(pre => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'copy-btn';
    button.textContent = 'Másolás';
    button.setAttribute('aria-label', 'A következő szöveg másolása');
    pre.before(button);
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(pre.textContent);
        button.textContent = 'Másolva';
        setTimeout(() => { button.textContent = 'Másolás'; }, 1800);
      } catch {
        const range = document.createRange();
        range.selectNodeContents(pre);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        button.textContent = 'Kijelölve: Ctrl+C';
      }
    });
  });
})();
