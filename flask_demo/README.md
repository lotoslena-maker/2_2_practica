# МетІАЗ ОВУ — групове заняття 2.2

Основна теоретична вебсторінка знаходиться у кореневому файлі \`index.html\` (працює через GitHub Pages). **Міні Flask-застосунок** знаходиться в окремій папці \`flask_demo/\`.

## Запуск у VS Code

1. Скачайте цей репозиторій через **Code → Download ZIP** та розпакуйте його, або виконайте:
   \`\`\`powershell
   git clone https://github.com/lotoslena-maker/2_2_practica.git
   cd 2_2_practica/flask_demo
   \`\`\`
2. Відкрийте папку **flask_demo** у VS Code (**File → Open Folder**).
3. Відкрийте термінал (**Terminal → New Terminal**).
4. Створіть ізольоване середовище:
   \`\`\`powershell
   python -m venv .venv
   \`\`\`
5. Для Windows PowerShell запустіть Python без активації:
   \`\`\`powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe app.py
   \`\`\`
   Для Ubuntu/Linux:
   \`\`\`bash
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python app.py
   \`\`\`
6. Відкрийте http://127.0.0.1:5000 у браузері. Зупинити сервер: **Ctrl+C**.

## Для чого кожний файл?

- \`app.py\` — Flask-сервер. Віддає сторінку та два API: \`/api/demo\`, \`/api/live\`. Використовує requests для HTTP і BeautifulSoup для розбору HTML.
- \`requirements.txt\` — залежності Python: Flask, requests, beautifulsoup4.
- \`templates/index.html\` — HTML-каркас інтерфейсу та три вкладки.
- \`static/style.css\` — кольори, сітка, оформлення.
- \`static/app.js\` — перемикання вкладок, запит до Flask API, вивід таблиці та експорт CSV.
- \`sample_news.html\` — локальний навчальний HTML для гарантованої демонстрації парсингу.
- \`.gitignore\` — заборона додавання в Git локального середовища Python і кешів.

## Принцип роботи

Браузер → Flask (\`/\`) → HTML/CSS/JS.
Кнопка «Навчальний запуск» → JS \`fetch('/api/demo')\` → Flask → локальний HTML → BeautifulSoup → JSON → таблиця.
Кнопка «Живий запит» → JS \`fetch('/api/live')\` → Flask → robots.txt → requests → АрміяInform → BeautifulSoup → JSON → таблиця.

**Важливо:** живий режим залежить від доступності ресурсу, правил robots.txt та поточної HTML-структури. Якщо ресурс забороняє або блокує автоматичний доступ, використовуйте навчальний режим. Запуск GitHub Pages НЕ запускає Flask: Python-сервер потрібно запускати локально або розгортати окремо.
