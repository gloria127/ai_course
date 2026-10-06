# Установка окружения

Время: ~15 минут. Все лабораторные работают **оффлайн без API-ключей** — вместо реальной модели используется MockLLM, встроенная заглушка с заранее заданными ответами. Ключи понадобятся позже, для проекта.

## Требования

- Python **3.10+** (проверено на 3.10 и 3.12)
- ~1 ГБ диска (пакеты), git

## Вариант A — локально (рекомендуется)

```bash
git clone <репозиторий курса>
cd <репозиторий>/labs
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Вариант B — Google Colab

Загрузите ноутбук лабораторной и в первой ячейке выполните:

```python
!pip -q install mcp openai anthropic
# numpy/matplotlib/pytest в Colab уже есть
```

Файл `course_llm.py` должен лежать рядом с ноутбуком: либо загрузите его в сессию Colab через панель «Файлы» слева, либо склонируйте репозиторий курса прямо в Colab.

## Smoke-test (проверка, что всё работает)

Из каталога `labs/`:

```bash
python3 - <<'EOF'
import numpy, matplotlib, pytest, mcp
from course_llm import MockLLM
llm = MockLLM(scripted=["ok"])
assert llm.chat([{"role": "user", "content": "ping"}]) == "ok"
print("SMOKE TEST OK — окружение готово")
EOF
```

Ожидаемый вывод: `SMOKE TEST OK — окружение готово`. Если падает импорт `course_llm`, скорее всего, вы запустили скрипт не из каталога `labs/`. Интерфейс работы с любой моделью на весь курс один: метод `backend.chat(messages)`, который принимает список сообщений и возвращает строку с ответом (`-> str`, подробности — в docstring `course_llm.py`).

## LLM-бэкенды (понадобятся с недель W4–W5, обязательны к проекту)

- **Без ключей, локально:** установите [Ollama](https://ollama.com), затем `ollama pull <модель из списка курса>`; в коде — `OpenAIBackend(model="...", base_url="http://localhost:11434/v1")`.
- **Облако:** ключ OpenAI-совместимого провайдера или Anthropic. Правила обращения с ключами и бюджет — `../STUDENT-API-RULES.md` (обязательно к прочтению до получения ключа).

## Частые проблемы

| Симптом | Причина/лечение |
|---|---|
| `ModuleNotFoundError: course_llm` | Запуск не из `labs/`; либо добавьте `labs/` в `PYTHONPATH` |
| `command not found: python` | Используйте `python3`; внутри venv доступны оба |
| Jupyter не видит venv | `python3 -m ipykernel install --user --name agents-course` и выберите ядро в ноутбуке |
| Графики не рисуются в терминале | Запускайте через Jupyter/Colab, не `python script.py` |

Проблема не решается за 15 минут — несите её на практикум W1, это нормальный сценарий.
