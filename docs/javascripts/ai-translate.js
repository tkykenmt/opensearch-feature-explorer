document.addEventListener('DOMContentLoaded', function() {
  const languages = ['Japanese', 'Chinese', 'Korean', 'Spanish', 'French', 'German'];
  const services = {
    'ChatGPT': (text, lang) => `https://chat.openai.com/?q=${encodeURIComponent(`Translate the following to ${lang}:\n\n${text}`)}`,
    'Claude': (text, lang) => `https://claude.ai/new?q=${encodeURIComponent(`Translate the following to ${lang}:\n\n${text}`)}`,
    'Gemini': (text, lang) => `https://gemini.google.com/app?q=${encodeURIComponent(`Translate the following to ${lang}:\n\n${text}`)}`
  };

  // Create UI
  const container = document.createElement('div');
  container.className = 'ai-translate';
  container.innerHTML = `
    <select class="ai-translate-lang">
      ${languages.map(l => `<option value="${l}">${l}</option>`).join('')}
    </select>
    <select class="ai-translate-service">
      ${Object.keys(services).map(s => `<option value="${s}">${s}</option>`).join('')}
    </select>
    <button class="ai-translate-btn">Translate with AI</button>
  `;

  // Insert after article header
  const article = document.querySelector('article');
  if (article) {
    const h1 = article.querySelector('h1');
    if (h1) h1.after(container);
  }

  // Handle click
  container.querySelector('.ai-translate-btn').addEventListener('click', function() {
    const lang = container.querySelector('.ai-translate-lang').value;
    const service = container.querySelector('.ai-translate-service').value;
    const content = article ? article.innerText.substring(0, 8000) : '';
    window.open(services[service](content, lang), '_blank');
  });
});
