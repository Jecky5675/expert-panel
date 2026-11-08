# Публикация Expert Panel: GitHub, npm и PyPI/pipx

Эта инструкция описывает подготовку и публикацию релиза. Сборки и тесты локально не публикуют пакет и не создают GitHub-репозиторий.

## Статус разрешения на публикацию

**Авторские материалы Expert Panel лицензированы под MIT** — см. корневой `LICENSE`; package metadata указывает MIT. Эта лицензия не переоформляет донорские материалы. `docs/NOTICE.md` фиксирует два новых источника без лицензии (Vibe Security MCP/skill и ub-mode) и набор проектных правил без лицензии. Из них не копировались исходники, policy JSON или substantial text. Встроенные правила сформулированы независимо как общие инженерные практики.

Перед публичным выпуском проверьте происхождение каждого уже включённого vendor-файла и подтвердите, что владелец проекта имеет право распространять его. Донорские лицензии и атрибуции находятся в `docs/NOTICE.md` и `docs/licenses/`. Если право на конкретный файл не подтверждается, исключите его из публикуемого payload либо замените независимой реализацией. MIT для файлов Expert Panel не является лицензией на donor-works и не устраняет этот release review.

## Требования к среде

- Git и учётная запись GitHub с правом создавать репозиторий.
- Node.js 18+ и npm для npm-пакета.
- Python 3.10+ и pipx для потребительской установки; для сборки wheel — современный `build`/`wheel`.
- Учётные записи npm и PyPI с настроенной двухфакторной защитой. Предпочтительны Trusted Publishing с GitHub Actions или токены с минимальными правами; не храните токены в репозитории.
- Имя npm-пакета `expert-panel-installer` и имя PyPI-дистрибутива `expert-panel-installer` должны быть свободны либо контролироваться владельцем проекта.

## 1. Подготовка GitHub-репозитория

Работайте из каталога `expert-panel/` — в корне должны находиться `skills/`, `docs/`, `scripts/`, `README.md` и `README_RU.md`. Не добавляйте в публикацию соседнюю папку с исходными скиллами-донорскими материалами.

1. После решения по лицензии создайте публичный GitHub-репозиторий, выберите имя и добавьте описание, topics и default branch.
2. Проверьте `git status`, затем просмотрите весь `git diff` и список файлов. Убедитесь, что нет токенов, локальных данных, build outputs, архивов и случайно скопированных donor-репозиториев.
3. Из корня проекта прогоните проверки:

```bash
python scripts/validate_skill.py skills/expert-panel
python scripts/tests/run_evals.py skills/expert-panel
python scripts/role_orchestrator.py --check-cases
python scripts/tests/self_test.py skills/expert-panel
python scripts/audit_release.py .
python scripts/tests/audit_readme.py README.md --root . --strict
python scripts/tests/audit_readme.py README_RU.md --root . --strict
python -m compileall -q scripts
node --check scripts/node/cli.mjs
python scripts/python/build_publishable.py --target both --output ./dist-check
```

4. Workflow сейчас лежит в неподдерживаемой папке `scripts/.github/workflows/validate.yml`. До публикации переместите его в корневой `.github/workflows/` и обновите команды под текущую структуру проекта; GitHub Actions не запускает workflow из `scripts/.github/`. Затем дождитесь зелёного CI.
5. После review создайте тег версии, совпадающий с package manifests (например `v27.3.0`), и опубликуйте GitHub Release с changelog, инструкциями установки и фактическими результатами тестов.

## 2. npm: пакет для `npx`

Публиковать нужно из `scripts/node/`, а не из корня репозитория. Имя и версия берутся из `scripts/node/package.json`.

1. После утверждения лицензии проверьте `scripts/node/package.json` и убедитесь, что поле `files` включает CLI и `package-payload/**`.
2. Соберите и проверьте содержимое tarball без публикации:

```bash
node scripts/node/stage-package.mjs
cd scripts/node
npm pack --dry-run
npm pack
```

Проверьте, что архив содержит `cli.mjs`, `package-payload/skills/expert-panel/SKILL.md`, зависимости/плагины, нужные для обещанных команд экспорта, и notices. Не публикуйте, если любой файл отсутствует или `npx` не запускается из временной чистой папки.

3. Войдите в npm (с 2FA):

```bash
npm login
npm whoami
```

4. Проверьте уникальность имени, затем опубликуйте:

```bash
npm view expert-panel-installer name
npm publish --access public
```

Если включён Trusted Publishing, выполняйте публикацию только из проверенного GitHub Actions workflow. После публикации проверьте `npm view expert-panel-installer version` и запуск `npx expert-panel-installer@27.3.0` в чистом каталоге.

## 3. PyPI и `pipx`

Для pipx пакет должен быть wheel или sdist с entry point `expert-panel` и с полным скиллом внутри пакета. Установка `pipx` у потребителя не исправит отсутствующий payload.

1. Соберите wheel и sdist в отдельную временную папку, используя изолированное окружение с актуальными build tools:

```bash
python -m venv .venv-build
# Windows: .venv-build\\Scripts\\activate
# macOS/Linux: source .venv-build/bin/activate
python -m pip install --upgrade build
python scripts/python/build_publishable.py --target python --output ./dist-check
```

2. Проверьте, что сборка выдала wheel и sdist, а внутри обоих есть `expert_panel_installer/cli.py`, `expert_panel_installer/export_formats.py`, `expert_panel_installer/skills/expert-panel/SKILL.md` и `expert_panel_installer/licenses/`. Установите артефакт локально в чистое окружение и проверьте `expert-panel --help`, импорт пакета, установку скилла в временный каталог и все четыре формата экспорта. Не используйте для проверки опубликованный пакет.
3. Получите имя/доступ к проекту PyPI, настройте 2FA и Trusted Publishing или короткоживущий токен через защищённое хранилище секретов. Проверяйте наличие имени через официальный PyPI; не пытайтесь перехватить чужой проект.
4. Перед настоящей публикацией можно проверить TestPyPI с отдельной настройкой учётной записи:

```bash
python -m pip install --upgrade twine
python -m twine check dist-check/python/*
python -m twine upload --repository testpypi dist-check/python/*
```

5. Для публичного PyPI используйте Trusted Publishing или токен, ограниченный нужным проектом:

```bash
python -m twine upload dist-check/python/*
```

После публикации проверьте установку в чистом окружении:

```bash
pipx install expert-panel-installer==27.3.0
pipx run expert-panel-installer --help
```

При необходимости обновления:

```bash
pipx upgrade expert-panel-installer
```

## Запреты и контроль

- Не выполнять `npm publish`, `twine upload`, создание публичного GitHub-репозитория или GitHub Release без прямого запроса владельца и подтверждённого решения о правах/лицензиях.
- Не коммитить `.npmrc`, `.pypirc`, токены, recovery codes или секреты CI.
- Не переиспользовать номер уже опубликованной версии: npm/PyPI обычно не позволяют перезаписать релиз; повышайте версии во всех manifests согласованно.
- Перед публикацией каждого артефакта сохраняйте список файлов и SHA-256 для аудита, а после публикации проверяйте именно установленный опубликованный пакет.
