// Keep the embedded example in sync with the documentation's native theme.
(() => {
  const root = document.documentElement;
  const names = {
    '--demo-bg': '--md-default-bg-color', '--demo-fg': '--md-default-fg-color',
    '--demo-surface': '--doc-surface', '--demo-border': '--doc-border',
    '--demo-primary': '--doc-primary', '--demo-accent': '--md-typeset-a-color',
    '--demo-code': '--md-code-bg-color'
  };
  let observer;
  function apply() {
    try {
      if (parent === window) throw new Error('standalone');
      const host = parent.document.body;
      root.dataset.theme = host.dataset.mdColorScheme === 'slate' ? 'dark' : 'light';
      const styles = parent.getComputedStyle(host);
      Object.entries(names).forEach(([target, source]) => {
        const value = styles.getPropertyValue(source).trim();
        if (value) root.style.setProperty(target, value);
      });
      if (!observer) {
        observer = new MutationObserver(apply);
        observer.observe(host, {attributes: true, attributeFilter: ['data-md-color-scheme']});
      }
    } catch (_) {
      root.dataset.theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
  }
  apply();
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', apply);
  addEventListener('pagehide', () => observer && observer.disconnect());
})();
