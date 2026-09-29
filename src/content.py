"""Site content: everything that ends up on the pages, in English and Russian.

Every fact here is taken from the project READMEs (and the GitHub profile README);
see the comment above each project. Paths to images are relative to REPOS_ROOT and are
read on every build, so new screenshots in a repository get picked up by a rebuild.
"""

REPOS_ROOT = "~/Projects/2027"

SITE = {
    "name": {"en": "Vitaliy Alexeyev", "ru": "Виталий Алексеев"},
    "handle": "VitaminDB",
    "role": {
        "en": "Systems engineer — Rust, GPU/CUDA, ML inference, Linux desktop software",
        "ru": "Системный инженер — Rust, GPU/CUDA, инференс нейросетей, десктопный софт для Linux",
    },
    "location": {"en": "Kostanay, Kazakhstan", "ru": "Костанай, Казахстан"},
    "availability": {"en": "Open to remote work", "ru": "Открыт к удалённой работе"},
    "contacts": {
        "github": "https://github.com/VitaminDB",
        "x": "https://x.com/alexeyev_vitaly",
        "email": "vitamindbnfkz@gmail.com",
        "paypal": "https://paypal.me/vitamindbnfkz",
        "youtube": "",   # channel URL; hidden while empty
        "discord": "",   # invite URL; hidden while empty
    },
    "hub": {
        "title": {
            "en": "Vitaliy Alexeyev — Rust, CUDA and Linux desktop projects",
            "ru": "Виталий Алексеев — проекты на Rust, CUDA и для Linux",
        },
        "description": {
            "en": "Systems engineer from Kazakhstan: a local AI studio, a CUDA inference engine, "
                  "a Rust GUI framework, a Wayland desktop and Linux hardware tools.",
            "ru": "Системный инженер из Костаная: локальная AI-студия, движок инференса на CUDA, "
                  "GUI-фреймворк для Rust, рабочий стол Wayland и утилиты для железа в Linux.",
        },
        "intro": {
            "en": "I build software that runs close to the hardware: a local AI studio and the CUDA "
                  "engine under it, the GUI framework they are drawn with, a Wayland desktop, and "
                  "Linux tools for a laptop and a mouse whose vendors ship Windows-only software. "
                  "Six open-source projects, all written in Rust, all running on my own machine.",
            "ru": "Я пишу софт, который работает близко к железу: локальную AI-студию и CUDA-движок "
                  "под ней, GUI-фреймворк, на котором они нарисованы, рабочий стол для Wayland и "
                  "утилиты для Linux к ноутбуку и мыши, производители которых делают программы "
                  "только под Windows. Шесть открытых проектов, все на Rust, все работают на моей машине.",
        },
        "stats": [
            {"value": "125B", "label": {"en": "MoE model on a 24 GB laptop GPU",
                                         "ru": "MoE-модель на ноутбучной карте 24 ГБ"}},
            {"value": "210", "unit": "tok/s", "label": {"en": "Gemma-4 26B A4B decode",
                                                        "ru": "декод Gemma-4 26B A4B"}},
            {"value": "110+", "label": {"en": "widgets in the GUI framework",
                                         "ru": "виджетов в GUI-фреймворке"}},
            {"value": "6", "label": {"en": "open-source projects, MIT / Apache-2.0",
                                      "ru": "открытых проектов, MIT / Apache-2.0"}},
        ],
        # From github-profile/README.md, "Background".
        "background": {
            "en": [
                "Fifteen years close to the metal before this — repairing electronics, bare-metal "
                "firmware, PCB design. Earlier commercial work: a central-heating controller with a "
                "GSM-OTA bootloader (in production for years) and a Qt/C++ SPI-flash recovery tool "
                "used daily in a repair shop.",
            ],
            "ru": [
                "До этого — пятнадцать лет рядом с железом: ремонт электроники, прошивки без ОС, "
                "разводка плат. Из коммерческих работ — контроллер системы отопления с загрузчиком "
                "обновлений по GSM (годами работает в серии) и программа на Qt/C++ для "
                "восстановления SPI-флешек, которой каждый день пользуются в сервисном центре.",
            ],
        },
        "skills": ["Rust", "CUDA · NVRTC", "GEMM / GEMV", "FP4 / FP8 quantization", "Nsight",
                   "C++", "wgpu / WGSL", "Wayland", "STM32 · AVR · PIC", "Arch Linux", "KiCad"],
    },
    # The vibe-coding statement. EN is verbatim from the brief.
    "vibe": {
        "en": "Everything here is vibe-coded. Since spring 2026 I write all of my projects with "
              "Claude Code: I decide what to build and how it fits together, describe each task, "
              "and review, run and measure the result on my own hardware — the model writes the "
              "code. That is how one person ends up with a CUDA inference engine, a GUI framework, "
              "an AI studio and a Wayland desktop in half a year. The numbers on these pages are "
              "measured on my machine, not taken on the model's word.",
        "ru": "Всё здесь написано вайбкодингом. С весны 2026 года я пишу все свои проекты в "
              "Claude Code: сам решаю, что строить и как части складываются в целое, описываю "
              "каждую задачу, а потом проверяю, запускаю и замеряю результат на своём железе — "
              "код пишет модель. Так один человек за полгода и приходит к CUDA-движку инференса, "
              "GUI-фреймворку, AI-студии и рабочему столу для Wayland. Цифры на этих страницах "
              "измерены на моей машине, а не взяты на слово у модели.",
    },
    "hardware": {
        "en": "Measured on an RTX 5090 Laptop GPU (24 GB) with 93 GB of system RAM, Arch Linux.",
        "ru": "Замерено на ноутбучной RTX 5090 (24 ГБ) с 93 ГБ оперативной памяти, Arch Linux.",
    },
}

# Interface strings.
UI = {
    "en": {
        "skip": "Skip to content",
        "nav_projects": "Projects",
        "nav_vibe": "How it is built",
        "nav_contact": "Contact",
        "lang_other": "Русский",
        "lang_other_short": "RU",
        "home": "Home",
        "projects_h": "Projects",
        "projects_sub": "Six repositories, one stack: every app below is drawn with syngui, and the AI ones run on synaptix.",
        "vibe_h": "How it is built",
        "vibe_label": "Vibe-coded with Claude Code",
        "background_h": "Background",
        "contact_h": "Contact",
        "contact_sub": "Questions, bug reports, work offers — any of these reaches me.",
        "read_more": "Details",
        "on_github": "Source on GitHub",
        "on_aur": "AUR package",
        "what_h": "What it is",
        "features_h": "Key features",
        "install_h": "Install",
        "install_readme": "Full instructions in the README",
        "req_h": "Requirements and limitations",
        "gallery_h": "Screenshots",
        "gallery_open": "open full size",
        "perf_h": "Measured performance",
        "video_h": "Watch it run",
        "video_youtube": "Watch on YouTube",
        "video_file": "Download the video (MP4)",
        "built_h": "How it is built",
        "others_h": "Other projects",
        "licence": "Licence",
        "platform": "Platform",
        "language": "Language",
        "packages": "Packages",
        "status": "Status",
        "support": "Support the work via PayPal",
        "footer_note": "Static site, no trackers, no cookies. Built with a Python script.",
        "nf_title": "Page not found",
        "nf_text": "There is nothing at this address. The projects are one click away.",
        "nf_back": "Back to the home page",
        "email": "Email",
        "screenshot": "Screenshot",
        "stack": "Built on",
        "col_model": "Model",
        "col_prefill": "Prefill",
        "col_decode": "Decode",
        "col_notes": "Notes",
        "breadcrumb": "Breadcrumb",
        "other_nav": "Other projects",
        "vibe_more": "Why that matters: every speed figure is measured on real hardware, and every README lists what does not work yet next to what does.",
    },
    "ru": {
        "skip": "К содержимому",
        "nav_projects": "Проекты",
        "nav_vibe": "Как сделано",
        "nav_contact": "Контакты",
        "lang_other": "English",
        "lang_other_short": "EN",
        "home": "Главная",
        "projects_h": "Проекты",
        "projects_sub": "Шесть репозиториев, один стек: все программы ниже нарисованы на syngui, а те, что с нейросетями, работают на synaptix.",
        "vibe_h": "Как сделано",
        "vibe_label": "Вайбкодинг в Claude Code",
        "background_h": "Опыт",
        "contact_h": "Контакты",
        "contact_sub": "Вопросы, баг-репорты, предложения о работе — пишите куда удобнее.",
        "read_more": "Подробнее",
        "on_github": "Исходники на GitHub",
        "on_aur": "Пакет в AUR",
        "what_h": "Что это",
        "features_h": "Возможности",
        "install_h": "Установка",
        "install_readme": "Полная инструкция — в README",
        "req_h": "Требования и ограничения",
        "gallery_h": "Скриншоты",
        "gallery_open": "открыть в полном размере",
        "perf_h": "Замеры скорости",
        "video_h": "Как это работает",
        "video_youtube": "Смотреть на YouTube",
        "video_file": "Скачать видео (MP4)",
        "built_h": "Как сделано",
        "others_h": "Другие проекты",
        "licence": "Лицензия",
        "platform": "Платформа",
        "language": "Язык",
        "packages": "Пакеты",
        "status": "Статус",
        "support": "Поддержать через PayPal",
        "footer_note": "Статический сайт без трекеров и cookies. Собран скриптом на Python.",
        "nf_title": "Страница не найдена",
        "nf_text": "По этому адресу ничего нет. Проекты — в один клик отсюда.",
        "nf_back": "На главную",
        "email": "Почта",
        "screenshot": "Скриншот",
        "stack": "Основа",
        "col_model": "Модель",
        "col_prefill": "Префилл",
        "col_decode": "Декод",
        "col_notes": "Примечание",
        "breadcrumb": "Навигационная цепочка",
        "other_nav": "Другие проекты",
        "vibe_more": "Что это значит на деле: каждая цифра скорости измерена на реальном железе, а в каждом README рядом с тем, что работает, перечислено то, что пока не работает.",
    },
}


def img(path, alt_en, alt_ru, cap_en=None, cap_ru=None):
    return {"src": path, "alt": {"en": alt_en, "ru": alt_ru},
            "caption": {"en": cap_en or alt_en, "ru": cap_ru or alt_ru}}


PROJECTS = [
    # ------------------------------------------------------------------ synthos
    # Source: synthos/README.md, synthos_public/07-facts.md
    {
        "slug": "synthos",
        "name": "synthos",
        "repo": "https://github.com/VitaminDB/synthos",
        "readme": "https://github.com/VitaminDB/synthos#readme",
        "aur": ["synthos-bin", "synthos-git"],
        "licence": "MIT OR Apache-2.0",
        "platform": {"en": "Linux x86_64 · NVIDIA sm_80+", "ru": "Linux x86_64 · NVIDIA sm_80+"},
        "stack": ["Rust", "CUDA", "synaptix", "syngui"],
        "category": "MultimediaApplication",
        "status": {"en": "Early, single developer", "ru": "Ранняя стадия, один разработчик"},
        "title": {
            "en": "synthos — local AI studio for Linux, no Python",
            "ru": "synthos — локальная AI-студия для Linux без Python",
        },
        "description": {
            "en": "Run LLMs locally on Linux and NVIDIA: agentic chat, notes, image, video, music "
                  "and speech generation. 27B–125B models on one GPU. Rust, no Python, no cloud.",
            "ru": "Запуск LLM локально на Linux и NVIDIA: чат с агентом, заметки, генерация "
                  "картинок, видео, музыки и речи. Модели 27B–125B на одной видеокарте, без Python.",
        },
        "tagline": {
            "en": "A local AI desktop studio: agentic chat, notes and a node editor for images, "
                  "video, music and speech — on one NVIDIA GPU, with no Python and no cloud.",
            "ru": "Локальная нейросетевая студия для рабочего стола: чат с агентом, заметки и "
                  "нодовый редактор для картинок, видео, музыки и речи — на одной видеокарте "
                  "NVIDIA, без Python и облака.",
        },
        "card": {
            "en": "Local AI studio: agentic chat, notes with boards and a calendar, a node editor for "
                  "image, video, music and speech generation. 27B–125B models on one GPU.",
            "ru": "Локальная AI-студия: чат с агентом, заметки с досками и календарём, нодовый "
                  "редактор для генерации картинок, видео, музыки и речи. Модели 27B–125B на одной карте.",
        },
        "stats": [
            {"value": "125B", "label": {"en": "MoE chat model on a 24 GB laptop card", "ru": "MoE-модель для чата на ноутбучной карте 24 ГБ"}},
            {"value": "262k", "label": {"en": "tokens of context on that card", "ru": "токенов контекста на той же карте"}},
            {"value": "210", "unit": "tok/s", "label": {"en": "Gemma-4 26B A4B decode", "ru": "декод Gemma-4 26B A4B"}},
            {"value": "7 GB", "label": {"en": "of VRAM runs every model family", "ru": "VRAM хватает любой модели"}},
        ],
        "what": {
            "en": [
                "synthos is one desktop app around a local GPU. A chat client runs 27B–125B models "
                "from single-file .syn bundles or GGUF files and drives the rest of the app through "
                "tools; a notes mode holds your documents, kanban boards, mind maps and calendar in "
                "a single project file; a node editor wires generative models into runnable graphs — "
                "prompt → image, image + instruction → edited image, text or image → video with "
                "sound, lyrics → music, script → multi-voice dialogue, audio → transcript.",
                "The agent can build and run those graphs itself, write into your notes, search your "
                "knowledge base and read the web. Everything runs on the device on the native "
                "synaptix engine — no Python, no torch, no cloud. Nothing leaves the machine.",
            ],
            "ru": [
                "synthos — одна программа для рабочего стола вокруг локальной видеокарты. Чат "
                "запускает модели от 27B до 125B из однофайловых бандлов .syn или из GGUF и через "
                "инструменты управляет всем остальным; режим заметок держит документы, канбан-доски, "
                "майнд-карты и календарь в одном файле проекта; нодовый редактор собирает "
                "генеративные модели в графы, которые можно запустить: промпт → картинка, картинка "
                "с инструкцией → отредактированная картинка, текст или картинка → видео со звуком, "
                "текст песни → музыка, сценарий → диалог на несколько голосов, звук → расшифровка.",
                "Агент умеет сам собрать и запустить такой граф, писать в заметки, искать по базе "
                "знаний и читать веб. Всё считается на месте, на собственном движке synaptix — без "
                "Python, без torch и без облака. Данные не покидают машину.",
            ],
        },
        "features": {
            "en": [
                "Chat with Qwen3, the Qwen3.6 / 3.8 hybrids, Qwen3.8-Flash-Next (a 125B MoE that runs on a 24 GB card), Gemma-3, Gemma-4 26B A4B, Muse Glimmer 30B and Llama — with vision where the model has it.",
                "Native inference: NVFP4, MXFP8, SQ1…SQ8 and all ggml quantization types, CUDA-graph decode, MTP and DFlash speculative decoding, prefix-KV reuse across turns and partial offload of layers to host RAM.",
                "An agent with tools: web search and reading, knowledge-base retrieval, building and running node graphs, full access to notes, a view_media tool, a wizard that asks you a question mid-turn, subagents and your own skills.",
                "Notes where a whole project is one .syn file: a WYSIWYG block editor over Markdown, flow or free-canvas pages, kanban boards, Gantt charts, mind maps and a calendar with reminders.",
                "Images: FLUX.1, FLUX.2 (dev, klein 4B / 9B), Qwen-Image 2.1, Qwen-Image-Edit 2509 / 2511 and SDXL.",
                "Video: LTX-2.3 (text, image or audio to video, IC-LoRA control) and MiniMax-H3 with synchronized stereo audio and image / video / audio references.",
                "Music and speech: YuE2 songs through an editable ABC score and covers of a recording, ACE-Step, VoxCPM2 and OmniVoice voice cloning, VibeVoice multi-speaker dialogue, GigaAM transcription, Sortformer diarization.",
                "A local knowledge base (RAG): files, folders, PDF and URLs, hybrid BM25 + vector search with an optional rerank, stored in bundled SQLite.",
                "A code editor with git-status decorations and integrated terminals that run full-screen TUIs.",
                "A Hugging Face browser with a download dock, in-app packing of models into .syn with per-layer-group quantization, and an interface in 14 languages.",
            ],
            "ru": [
                "Чат с Qwen3, гибридами Qwen3.6 / 3.8, Qwen3.8-Flash-Next (MoE на 125B, которая работает на карте 24 ГБ), Gemma-3, Gemma-4 26B A4B, Muse Glimmer 30B и Llama — со зрением, если оно есть у модели.",
                "Собственный инференс: NVFP4, MXFP8, SQ1…SQ8 и все типы квантования ggml, декод через CUDA-граф, спекулятивное декодирование MTP и DFlash, переиспользование префикс-KV между ходами и частичная выгрузка слоёв в оперативную память.",
                "Агент с инструментами: поиск и чтение веба, поиск по базе знаний, сборка и запуск нодовых графов, полный доступ к заметкам, просмотр файлов своим зрением (view_media), вопрос пользователю посреди хода, субагенты и свои навыки.",
                "Заметки, где весь проект — один файл .syn: визуальный блочный редактор поверх Markdown, страницы потоком или свободным холстом, канбан-доски, диаграммы Ганта, майнд-карты и календарь с напоминаниями.",
                "Картинки: FLUX.1, FLUX.2 (dev, klein 4B / 9B), Qwen-Image 2.1, Qwen-Image-Edit 2509 / 2511 и SDXL.",
                "Видео: LTX-2.3 (из текста, картинки или звука, управление через IC-LoRA) и MiniMax-H3 с синхронным стереозвуком и референсами — картинками, видео и звуком.",
                "Музыка и речь: песни YuE2 через редактируемую партитуру ABC и каверы на запись, ACE-Step, клонирование голоса в VoxCPM2 и OmniVoice, диалог на несколько голосов в VibeVoice, распознавание речи GigaAM и разметка спикеров Sortformer.",
                "Локальная база знаний (RAG): файлы, папки, PDF и ссылки, гибридный поиск BM25 + векторы с необязательным реранком, всё хранится во встроенном SQLite.",
                "Редактор кода с подсветкой статуса git и встроенными терминалами, в которых работают полноэкранные TUI.",
                "Браузер Hugging Face с панелью загрузок, упаковка моделей в .syn прямо в программе с квантованием по группам слоёв и интерфейс на 14 языках.",
            ],
        },
        "install": {
            "code": "paru -S synthos-bin   # prebuilt binary — recommended\nparu -S synthos-git   # build from source (CUDA toolkit, ~2 h, ~15 GB disk)",
            "note": {
                "en": "Other distributions: download the tarball from Releases or build from source — the binary is built against Arch library versions. Models downloaded from Hugging Face are packed once into a single .syn file (Syn packages → Build a .syn); GGUF chat models open directly.",
                "ru": "Другие дистрибутивы: архив со страницы Releases или сборка из исходников — бинарник собран под версии библиотек Arch. Модели, скачанные с Hugging Face, один раз упаковываются в файл .syn (Syn packages → Build a .syn); чат-модели в GGUF открываются напрямую.",
            },
        },
        "requirements": {
            "en": [
                "Linux x86_64 only. Runtime: gtk3, wayland, libxkbcommon, fontconfig, a Vulkan driver, alsa, ffmpeg.",
                "An NVIDIA GPU from sm_80 (Ampere) up. Native NVFP4 / MXFP8 tensor-core paths need Blackwell (sm_120+); older cards run through portable kernels.",
                "7 GB of VRAM is enough to run everything, 24 GB to run it quickly: on 7 GB a 27B hybrid answers at 1–2 tok/s.",
                "No AMD (ROCm) or Apple (Metal) support. A Windows build is planned but does not exist yet.",
                "No model weights are shipped: you download them yourself and accept each model's licence — some are non-commercial.",
                "Early stage: one developer, one machine (RTX 5090 Laptop, 24 GB, Arch Linux). How it behaves on other GPUs and distributions is not known yet — bug reports with hardware details help most.",
            ],
            "ru": [
                "Только Linux x86_64. Нужны gtk3, wayland, libxkbcommon, fontconfig, драйвер Vulkan, alsa, ffmpeg.",
                "Видеокарта NVIDIA от sm_80 (Ampere) и новее. Родные тензорные пути NVFP4 / MXFP8 — только на Blackwell (sm_120+), старые карты работают через переносимые ядра.",
                "Чтобы запустить всё, хватает 7 ГБ видеопамяти, чтобы работало быстро — нужно 24 ГБ: на 7 ГБ гибрид 27B отвечает со скоростью 1–2 ток/с.",
                "AMD (ROCm) и Apple (Metal) не поддерживаются. Сборка под Windows в планах, но её пока нет.",
                "Веса моделей в комплект не входят: их скачиваете вы и принимаете лицензию каждой модели — некоторые только для некоммерческого использования.",
                "Ранняя стадия: один разработчик, одна машина (ноутбучная RTX 5090, 24 ГБ, Arch Linux). Как программа поведёт себя на других картах и дистрибутивах, пока неизвестно — больше всего помогают баг-репорты с описанием железа.",
            ],
        },
        "perf": {
            "rows": [
                ["Gemma-4 26B A4B", "10 100 tok/s (4k)", "210 tok/s", ""],
                ["Qwen3.8-27B hybrid", "1 450 tok/s (3.3k)", "47 tok/s", "MTP + CUDA graph"],
                ["Qwen3.8-Flash-Next 125B MoE", "1 650 tok/s @ 260k", "17–22 tok/s", "262k context on 24 GB"],
            ],
            "note": {
                "en": "A 3k-token follow-up turn on top of an 80k history takes 3.3 s thanks to prefix-KV reuse. Images at 1024²: SDXL 30 steps in 6.5 s, Qwen-Image 2.1 40 steps in 30 s (MXFP8) or 23 s (NVFP4).",
                "ru": "Ход на 3k токенов поверх истории в 80k занимает 3,3 с благодаря префикс-KV. Картинки 1024²: SDXL за 30 шагов — 6,5 с, Qwen-Image 2.1 за 40 шагов — 30 с (MXFP8) или 23 с (NVFP4).",
            },
        },
        "video": {
            "file": "~/Projects/synthos_public/video/synthos-125b.mp4",
            "poster_at": 3.0,
            "youtube_id": "",
            "caption": {
                "en": "Qwen3.8-Flash-Next, a 125B MoE, answering in real time on a laptop RTX 5090 with 24 GB — no speed-up. Decode 21–23 tok/s; a 6.4k-token prompt prefilled in 4.5 s; the repeated prompt served from the prefix-KV cache in 1.1 s; about 21 of 24 GB of VRAM in use.",
                "ru": "Qwen3.8-Flash-Next, MoE на 125B, отвечает в реальном времени на ноутбучной RTX 5090 с 24 ГБ — без ускорения записи. Декод 21–23 ток/с; префилл промпта на 6,4k токенов — 4,5 с; повтор того же промпта из кэша префикс-KV — 1,1 с; занято около 21 из 24 ГБ видеопамяти.",
            },
            "title": {"en": "synthos: a 125B MoE model on a 24 GB laptop GPU",
                      "ru": "synthos: MoE-модель на 125B на ноутбучной карте 24 ГБ"},
            "duration": "PT56S",
        },
        "built": {
            "en": "The model writes the code, the tests and most of the documentation; I decide what to build, review it and measure it. Every number in the README was measured on my machine, with the losses reported next to the wins. synthos is my own daily code editor and chat.",
            "ru": "Модель пишет код, тесты и большую часть документации; я решаю, что делать, проверяю и замеряю. Каждая цифра в README измерена на моей машине, и рядом с выигрышами записаны потери. synthos — мой собственный ежедневный редактор кода и чат.",
        },
        "hero": img("synthos/docs/screenshots/notes-dashboard-floating-chat.png",
                    "synthos: a notes workspace built by the agent, with the chat torn off into a floating window",
                    "synthos: рабочее пространство заметок, собранное агентом, и чат, вынесенный в плавающее окно"),
        "gallery": [
            img("synthos/docs/screenshots/agent-pipeline-self-correct.png",
                "The agent runs a MiniMax-H3 video pipeline, hits a latent-shape error and fixes the resolution itself",
                "Агент запускает видеопайплайн MiniMax-H3, получает ошибку формы латента и сам исправляет разрешение"),
            img("synthos/docs/screenshots/nodes-menu-models.png",
                "The node editor: the Neuro node menu, a running graph and the models-in-memory panel",
                "Нодовый редактор: меню нод Neuro, работающий граф и панель загруженных моделей"),
            img("synthos/docs/screenshots/chat-details.png",
                "Chat details: tok/s, prefill time and how much of the prompt came from the prefix-KV cache",
                "Подробности чата: ток/с, время префилла и доля промпта из кэша префикс-KV"),
            img("synthos/docs/screenshots/notes-kanban-drag.png",
                "Kanban boards with labels, priorities and checklists — a card mid-drag",
                "Канбан-доски с метками, приоритетами и чек-листами — карточку перетаскивают"),
            img("synthos/docs/screenshots/chat-tools-autotools-skills.png",
                "Tools, the autotools pool and skills, toggled per chat",
                "Инструменты, пул autotools и навыки включаются для каждого чата отдельно"),
            img("synthos/docs/screenshots/pack-build-syn.png",
                "Build a .syn: the model is recognised by itself; pick where to save and, optionally, a quantization",
                "Сборка .syn: модель распознаётся сама, остаётся выбрать, куда сохранить, и при желании квантование"),
            img("synthos/docs/screenshots/notes-calendar-month.png",
                "Calendar, month view — events, board deadlines and Gantt bars",
                "Календарь на месяц — события, сроки с досок и полосы из диаграммы Ганта"),
            img("synthos/docs/screenshots/notes-mindmap.png", "Mind map in notes", "Майнд-карта в заметках"),
            img("synthos/docs/screenshots/code-editor-terminal.png",
                "Code editor with the integrated terminal", "Редактор кода со встроенным терминалом"),
        ],
    },
    # ------------------------------------------------------------------ synaptix
    # Source: synaptix/README.md (the README has no images; screenshots are synthos UI
    # showing the engine's numbers).
    {
        "slug": "synaptix",
        "name": "synaptix",
        "repo": "https://github.com/VitaminDB/synaptix",
        "readme": "https://github.com/VitaminDB/synaptix#readme",
        "aur": [],
        "licence": "MIT OR Apache-2.0",
        "platform": {"en": "CUDA sm_80+ · CPU fallback", "ru": "CUDA sm_80+ · запасной путь на CPU"},
        "stack": ["Rust", "CUDA", "NVRTC"],
        "category": "DeveloperApplication",
        "status": {"en": "Young, API not stable", "ru": "Молодой, API нестабилен"},
        "title": {
            "en": "synaptix — Rust CUDA inference engine, no PyTorch",
            "ru": "synaptix — движок инференса на Rust и CUDA без PyTorch",
        },
        "description": {
            "en": "Native Rust engine for LLM, image, video, speech and music models: hand-written "
                  "CUDA kernels via NVRTC, NVFP4 / MXFP8 / SQ quantization, GGUF. No PyTorch.",
            "ru": "Нативный движок на Rust для LLM, картинок, видео, речи и музыки: свои CUDA-ядра "
                  "через NVRTC, квантование NVFP4 / MXFP8 / SQ, GGUF напрямую. Без PyTorch.",
        },
        "tagline": {
            "en": "A native Rust engine for running and training neural networks — hand-written CUDA kernels compiled at runtime through NVRTC, with no PyTorch, no libtorch and no Python runtime.",
            "ru": "Нативный движок на Rust для запуска и обучения нейросетей — написанные вручную CUDA-ядра, которые компилируются на лету через NVRTC. Без PyTorch, без libtorch и без Python.",
        },
        "card": {
            "en": "The engine under synthos: LLM, diffusion, video, speech and music models on hand-written CUDA kernels. NVFP4 / MXFP8 / SQ quantization, GGUF loads directly.",
            "ru": "Движок под synthos: LLM, диффузия, видео, речь и музыка на своих CUDA-ядрах. Квантование NVFP4 / MXFP8 / SQ, GGUF загружается напрямую.",
        },
        "stats": [
            {"value": "~245k", "label": {"en": "lines of Rust", "ru": "строк на Rust"}},
            {"value": "73", "label": {"en": ".cu kernel files, JIT-compiled", "ru": "файла CUDA-ядер, компиляция на лету"}},
            {"value": "2 000+", "label": {"en": "tests", "ru": "тестов"}},
            {"value": "27", "label": {"en": "ggml block types executed as they are", "ru": "типов блоков ggml работают как есть"}},
        ],
        "what": {
            "en": [
                "An alternative to the Python ML stack. Everything from the tensor API and CUDA kernels up to full model ports, a tokenizer, an inference engine with paged KV caches and a training stack is written in Rust.",
                "It runs on any NVIDIA GPU from sm_80 (Ampere) up: kernels are JIT-compiled for the card, with native NVFP4 / MXFP8 block-scale tensor-core paths on Blackwell and portable kernels everywhere else. Models load from single-file .syn bundles or directly from GGUF. Correctness is held to bit-exact parity with PyTorch and NeMo reference implementations — per row, not by a global cosine similarity that hides local errors.",
            ],
            "ru": [
                "Альтернатива Python-стеку для машинного обучения. Всё — от API тензоров и CUDA-ядер до полных портов моделей, токенизатора, движка инференса со страничным KV-кэшем и стека обучения — написано на Rust.",
                "Работает на любой видеокарте NVIDIA от sm_80 (Ampere): ядра компилируются на лету под конкретную карту, на Blackwell есть родные тензорные пути NVFP4 / MXFP8, на остальных — переносимые ядра. Модели загружаются из однофайловых бандлов .syn или прямо из GGUF. Корректность проверяется побитовым совпадением с эталонами PyTorch и NeMo — построчно, а не по общему косинусному сходству, за которым прячутся локальные ошибки.",
            ],
        },
        "features": {
            "en": [
                "Hand-written CUDA kernels, JIT-compiled through NVRTC for the card's compute capability; any sm_80+ GPU, native block-scale mma.sync on Blackwell (sm_120+).",
                "Model ports checked against upstream: Qwen3 (dense and MoE), the Qwen3-Next hybrids, Qwen4Exp 125B MoE, Llama, Gemma-3, Gemma-4, Muse Glimmer; FLUX.1, FLUX.2, Qwen-Image 2.1, Qwen-Image-Edit, SDXL; LTX-2.3 and MiniMax-H3 video.",
                "Speech and music: Whisper, GigaAM, Sortformer; VoxCPM, OmniVoice, VibeVoice; YuE2, SheetSage2, ACE-Step; BGE-M3 embeddings and reranker.",
                "Single-file .syn bundles: mmapped zero-copy, quantized while packing, precision chosen per layer group.",
                "SQ1…SQ8, a portable block format with a GPU encoder; GGUF runs directly with all 27 ggml block types; quantized bundles can be transcoded on load for older cards.",
                "MXFP8 KV cache by default, paged KV, CUDA-graph decode and speculative decoding.",
                "MoE experts in pinned host RAM streaming at ~39 GB/s, plus partial block offload: a 125B MoE runs on a 24 GB card and every model family was measured on 7 GB.",
                "Prefix-KV sessions that survive between turns for every architecture, including prompts with images.",
                "A CLI for everything: inspect, convert, quantize, run, chat, bench, imagine, video, music, speak, podcast, transcribe.",
            ],
            "ru": [
                "CUDA-ядра, написанные вручную и компилируемые через NVRTC под compute capability конкретной карты; любая карта от sm_80, родной block-scale mma.sync на Blackwell (sm_120+).",
                "Порты моделей, сверенные с оригиналами: Qwen3 (плотные и MoE), гибриды Qwen3-Next, Qwen4Exp на 125B MoE, Llama, Gemma-3, Gemma-4, Muse Glimmer; FLUX.1, FLUX.2, Qwen-Image 2.1, Qwen-Image-Edit, SDXL; видео LTX-2.3 и MiniMax-H3.",
                "Речь и музыка: Whisper, GigaAM, Sortformer; VoxCPM, OmniVoice, VibeVoice; YuE2, SheetSage2, ACE-Step; эмбеддинги BGE-M3 и реранкер.",
                "Однофайловые бандлы .syn: читаются через mmap без копирования, квантуются при упаковке, точность выбирается для каждой группы слоёв.",
                "SQ1…SQ8 — переносимый блочный формат с энкодером на GPU; GGUF работает напрямую со всеми 27 типами блоков ggml; квантованный бандл можно перекодировать при загрузке под старую карту.",
                "KV-кэш в MXFP8 по умолчанию, страничный KV, декод через CUDA-граф и спекулятивное декодирование.",
                "Эксперты MoE живут в закреплённой памяти хоста и подкачиваются со скоростью ~39 ГБ/с, плюс частичная выгрузка блоков: MoE на 125B работает на карте 24 ГБ, а все семейства моделей проверены на 7 ГБ.",
                "Сессии префикс-KV переживают смену хода у всех архитектур, включая промпты с картинками.",
                "CLI на всё: inspect, convert, quantize, run, chat, bench, imagine, video, music, speak, podcast, transcribe.",
            ],
        },
        "install": {
            "code": "cargo build --release -p synaptix-cli\nsynaptix convert model.gguf model.syn\nsynaptix run model.gguf \"Explain NVFP4\" --max-tokens 256\nsynaptix bench model.syn --n-tokens 128",
            "note": {
                "en": "Needs the CUDA toolkit at build time (nvcc pins the CUDA version); the driver is loaded dynamically at runtime. The reference tensors for the bit-exact tests are not committed — regenerate them with scripts/reference/.",
                "ru": "Для сборки нужен CUDA toolkit (по nvcc фиксируется версия CUDA); драйвер подгружается динамически при запуске. Эталонные тензоры для побитовых тестов в репозиторий не входят — их генерируют скрипты из scripts/reference/.",
            },
        },
        "requirements": {
            "en": [
                "CUDA (primary) and CPU. Any sm_80+ card; native NVFP4 / MXFP8 block-scale MMA needs Blackwell (sm_120+), older cards run the same weights through dequantizing kernels.",
                "Young and single-author: the API is not stable, expect breaking changes.",
                "Inference is what is production-ready — it powers synthos daily. Training has working autograd, optimizers and checkpointing, but the RLHF, distillation and self-play modules are scaffolding.",
                "Some model directories are stubs; only the models listed in the README actually run.",
                "Weaker paths are documented, not hidden: bf16 GEMM lands at 0.82–1.16× of cuBLAS depending on shape, behind on large-M tails.",
            ],
            "ru": [
                "CUDA (основной путь) и CPU. Любая карта от sm_80; родной block-scale MMA для NVFP4 / MXFP8 требует Blackwell (sm_120+), на старых картах те же веса идут через ядра с деквантованием.",
                "Проект молодой, автор один: API нестабилен, ломающие изменения будут.",
                "Готов к работе инференс — на нём каждый день работает synthos. В обучении есть рабочий autograd, оптимизаторы и чекпойнты, но модули RLHF, дистилляции и self-play — пока каркас.",
                "Часть каталогов моделей — заглушки; реально работают только модели из списка в README.",
                "Слабые места описаны, а не спрятаны: bf16 GEMM даёт 0,82–1,16× от cuBLAS в зависимости от формы и отстаёт на больших M.",
            ],
        },
        "perf": {
            "rows": [
                ["Gemma-4 26B A4B", "10 100 tok/s @ 4k", "210 tok/s", "CUDA-graph decode captures the MoE"],
                ["Qwen3.8-27B hybrid", "1 450 tok/s @ 3.3k", "47 tok/s", "MTP speculative decode"],
                ["Qwen3.8-Flash-Next 125B MoE", "1 650 tok/s @ 260k", "17–22 tok/s", "262k context on 24 GB"],
            ],
            "note": {
                "en": "Gemma-4 decode went 35 → 210 tok/s and prefill 957 → 10 100 tok/s over a week of kernel work. Diffusion at 1024²: SDXL 30 steps in 6.5 s (8.8 GB peak), Qwen-Image-Edit-2511 40 steps in 155 s with NVFP4 (13.2 GB peak).",
                "ru": "Декод Gemma-4 вырос с 35 до 210 ток/с, а префилл — с 957 до 10 100 ток/с за неделю работы над ядрами. Диффузия 1024²: SDXL за 30 шагов — 6,5 с (пик 8,8 ГБ), Qwen-Image-Edit-2511 за 40 шагов — 155 с в NVFP4 (пик 13,2 ГБ).",
            },
        },
        "built": {
            "en": "The model writes the code, the tests and most of the documentation. Every number in the README was measured on my machine, and correctness is checked against reference implementations layer by layer rather than taken on the model's word.",
            "ru": "Модель пишет код, тесты и большую часть документации. Каждая цифра в README измерена на моей машине, а корректность проверяется по эталонным реализациям слой за слоем, а не принимается на слово у модели.",
        },
        "hero": img("synthos/docs/screenshots/chat-details.png",
                    "synaptix at work inside synthos: tok/s, prefill time and the prefix-KV share of a chat turn",
                    "synaptix в работе внутри synthos: ток/с, время префилла и доля промпта из префикс-KV"),
        "gallery": [
            img("synthos/docs/screenshots/pack-wizard-layers.png",
                "Packing a .syn bundle: components, auxiliary files and precision per layer group (synthos UI)",
                "Упаковка бандла .syn: компоненты, вспомогательные файлы и точность для каждой группы слоёв (интерфейс synthos)"),
            img("synthos/docs/screenshots/nodes-acestep.png",
                "ACE-Step text → music graph running on synaptix (synthos node editor)",
                "Граф ACE-Step «текст → музыка» на synaptix (нодовый редактор synthos)"),
            img("synthos/docs/screenshots/agent-pipeline-run.png",
                "The agent checks VRAM, frees it and starts a video run (synthos)",
                "Агент проверяет видеопамять, освобождает её и запускает генерацию видео (synthos)"),
        ],
    },
    # ------------------------------------------------------------------ syngui
    # Source: syngui/README.md
    {
        "slug": "syngui",
        "name": "syngui",
        "repo": "https://github.com/VitaminDB/syngui",
        "readme": "https://github.com/VitaminDB/syngui#readme",
        "aur": [],
        "licence": "MIT OR Apache-2.0",
        "platform": {"en": "Linux · Windows · macOS · Android · Web", "ru": "Linux · Windows · macOS · Android · Web"},
        "stack": ["Rust", "wgpu 28", "WGSL"],
        "category": "DeveloperApplication",
        "status": {"en": "Young, API not stable", "ru": "Молодой, API нестабилен"},
        "title": {
            "en": "syngui — GPU GUI framework for Rust with CSS-like styles",
            "ru": "syngui — GUI-фреймворк для Rust на wgpu со стилями как CSS",
        },
        "description": {
            "en": "Retained-mode GUI framework for Rust: wgpu rendering, real stylesheets with a "
                  "cascade, reactive signals, 110+ widgets — terminal, code and block editors, video.",
            "ru": "GUI-фреймворк для Rust: рендер на wgpu, таблицы стилей с каскадом, реактивные "
                  "сигналы, 110+ виджетов — терминал, редактор кода, блочный редактор, видео.",
        },
        "tagline": {
            "en": "A retained-mode GUI framework for Rust — GPU-rendered through wgpu, styled with CSS-like stylesheets, wired with reactive signals.",
            "ru": "Retained-mode GUI-фреймворк для Rust: рисует на GPU через wgpu, оформляется таблицами стилей в духе CSS, связывается реактивными сигналами.",
        },
        "card": {
            "en": "Retained-mode GUI framework for Rust: wgpu rendering, CSS-like stylesheets, reactive signals, 110+ widgets. Every app here is built on it.",
            "ru": "Retained-mode GUI-фреймворк для Rust: рендер на wgpu, стили как в CSS, реактивные сигналы, 110+ виджетов. На нём построены все программы отсюда.",
        },
        "stats": [
            {"value": "110+", "label": {"en": "widgets in 10 categories", "ru": "виджетов в 10 категориях"}},
            {"value": "1 400+", "label": {"en": "tests", "ru": "тестов"}},
            {"value": "5.8", "unit": "ms", "label": {"en": "per frame for a long chat feed (was 3.4 s)", "ru": "на кадр длинной ленты чата (было 3,4 с)"}},
            {"value": "5", "label": {"en": "platforms: Linux, Windows, macOS, Android, Web", "ru": "платформ: Linux, Windows, macOS, Android, Web"}},
        ],
        "what": {
            "en": [
                "Most Rust GUI libraries make you choose: immediate-mode simplicity (egui) or a retained tree with typed styling (iced), a custom DSL (Slint) or web tech (Tauri, Dioxus). syngui takes a different combination — real stylesheets with a cascade, SolidJS-style fine-grained reactivity, a retained widget tree, and a large set of widgets you would normally have to vendor yourself.",
                "It is used in production by its author: synthos, syndesktop, linux-legion and ardor-mouse all run on it, so its bugs get found by real use.",
            ],
            "ru": [
                "Большинство GUI-библиотек для Rust заставляют выбирать: простота immediate mode (egui) или retained-дерево с типизированными стилями (iced), собственный DSL (Slint) или веб-технологии (Tauri, Dioxus). syngui собирает другую комбинацию — настоящие таблицы стилей с каскадом, точечную реактивность в духе SolidJS, retained-дерево виджетов и большой набор виджетов, которые обычно приходится тащить в проект самому.",
                "Автор пользуется им в продакшене: на нём работают synthos, syndesktop, linux-legion и ardor-mouse, так что баги находятся в реальной работе.",
            ],
        },
        "features": {
            "en": [
                "MSS stylesheets: variables and var(), type / class / compound / descendant selectors, :hover, :active, :focus, :checked, :disabled, nesting, transitions, @keyframes, inheritance, plus window-state pseudo-classes.",
                "Fine-grained reactivity: use_signal, use_effect, create_memo and use_context with automatic dependency tracking; subtrees rebuild granularly.",
                "Retained-mode architecture: immutable Widget → stateful Element, diffed via can_update(), with dirty-flag propagation.",
                "110+ widgets: line / bar / pie / radar / gauge charts, a tile map, an embedded terminal (PTY + VT100), Markdown with syntax highlighting, a rope-backed code editor, an audio-clocked video player with hardware decode, a devtools inspector.",
                "DocumentEditor: a Notion-style block editor where Markdown is both the model and the file format, with flow or free-canvas layout, vector shapes and live embeds of your own widgets.",
                "3D transforms from stylesheets, particle emitters with 15 presets and a macOS-dock-style fisheye row.",
                "Measured hot paths: VirtualList, keyed children, a cached cascade and rendering batched into a handful of draw calls in one pass.",
                "wgpu 28 (Vulkan / Metal / DX12 / GL / WebGPU) with hand-written WGSL shaders.",
                "Linux on X11 and Wayland (with its own drag-and-drop), Windows, macOS, Android and Android TV, WebAssembly.",
            ],
            "ru": [
                "Таблицы стилей MSS: переменные и var(), селекторы по типу, классу, составные и по потомкам, :hover, :active, :focus, :checked, :disabled, вложенность, переходы, @keyframes, наследование и псевдоклассы состояния окна.",
                "Точечная реактивность: use_signal, use_effect, create_memo и use_context с автоматическим отслеживанием зависимостей; поддеревья перестраиваются по частям.",
                "Retained-архитектура: неизменяемый Widget → Element с состоянием, сравнение через can_update() и распространение флагов грязности.",
                "Больше 110 виджетов: графики (линии, столбцы, круговые, радар, шкалы), тайловая карта, встроенный терминал (PTY + VT100), Markdown с подсветкой синтаксиса, редактор кода на rope, видеоплеер с синхронизацией по звуку и аппаратным декодированием, инспектор.",
                "DocumentEditor — блочный редактор в духе Notion, где Markdown и модель, и формат файла: поток или свободный холст, векторные фигуры и живые встраивания своих виджетов.",
                "3D-трансформации прямо из стилей, эмиттеры частиц с 15 пресетами и ряд с увеличением под курсором, как в доке macOS.",
                "Горячие пути измерены: VirtualList, ключи у детей, кэш каскада и отрисовка, собранная в несколько вызовов за один проход.",
                "wgpu 28 (Vulkan / Metal / DX12 / GL / WebGPU) и шейдеры на WGSL, написанные вручную.",
                "Linux на X11 и Wayland (со своим drag-and-drop), Windows, macOS, Android и Android TV, WebAssembly.",
            ],
        },
        "install": {
            "code": "cargo build -p syngui\ncargo test -p syngui\ncargo run -p widget_gallery_mss   # every widget + MSS styling",
            "note": {
                "en": "Video playback sits behind the optional ffmpeg feature and needs FFmpeg 7+ development libraries; without it nothing links against FFmpeg. The widget gallery also builds to WebAssembly.",
                "ru": "Видео — за необязательной фичей ffmpeg, для неё нужны dev-библиотеки FFmpeg 7+; без неё с FFmpeg ничего не линкуется. Галерея виджетов собирается и в WebAssembly.",
            },
        },
        "requirements": {
            "en": [
                "Text shaping is simple: Latin, Cyrillic and CJK render correctly, but there is no kerning, no ligatures, no GSUB/GPOS, no bidirectional text and no complex scripts (Arabic, Devanagari).",
                "Colour emoji are drawn without a shaper: ZWJ sequences and VS16 can render as separate glyphs.",
                "Accessibility (AccessKit) exists behind a non-default feature and is not continuously tested.",
                "No CI yet: Windows, macOS and Android builds are verified by hand.",
                "The API is not stable; expect breaking changes.",
            ],
            "ru": [
                "Шейпинг текста простой: латиница, кириллица и CJK рисуются правильно, но нет кернинга, лигатур, GSUB/GPOS, двунаправленного текста и сложных письменностей (арабской, деванагари).",
                "Цветные эмодзи рисуются без шейпера: последовательности ZWJ и VS16 могут распасться на отдельные глифы.",
                "Доступность (AccessKit) есть за необязательной фичей и не проверяется постоянно.",
                "CI пока нет: сборки под Windows, macOS и Android проверяются вручную.",
                "API нестабилен, ломающие изменения будут.",
            ],
        },
        "built": {
            "en": "The model writes the code, the tests and most of the documentation. The performance numbers were measured on my machine, and every app I have built since — synthos, syndesktop, linux-legion, ardor-mouse — runs on this framework, so its bugs get found by real use.",
            "ru": "Модель пишет код, тесты и большую часть документации. Цифры производительности измерены на моей машине, а все программы, которые я сделал после, — synthos, syndesktop, linux-legion, ardor-mouse — работают на этом фреймворке, так что его баги находятся в настоящей работе.",
        },
        "hero": img("syngui/docs/widget-gallery.png",
                    "The widget_gallery_mss example running natively — MarkdownView with syntax highlighting",
                    "Пример widget_gallery_mss в нативном окне — MarkdownView с подсветкой синтаксиса"),
        "gallery": [
            img("synthos/docs/screenshots/notes-kanban-drag.png",
                "Built on syngui: DocumentEditor pages and kanban boards in synthos",
                "На syngui: страницы DocumentEditor и канбан-доски в synthos"),
            img("synthos/docs/screenshots/code-terminal-btop.png",
                "Built on syngui: the embedded terminal running btop inside synthos",
                "На syngui: встроенный терминал с btop внутри synthos"),
            img("synthos/docs/screenshots/notes-charts.png",
                "Built on syngui: line, bar, pie and radar charts",
                "На syngui: графики — линии, столбцы, круговая диаграмма, радар"),
            img("linux_legion/screenshots/lighting.png",
                "Built on syngui: the live keyboard map in linux-legion",
                "На syngui: живая карта клавиатуры в linux-legion"),
        ],
    },
    # ------------------------------------------------------------------ syndesktop
    # Source: syndesktop/README.md (Russian at the time of writing), github-profile.
    {
        "slug": "syndesktop",
        "name": "syndesktop",
        "repo": "https://github.com/VitaminDB/syndesktop",
        "readme": "https://github.com/VitaminDB/syndesktop#readme",
        "aur": [],
        "licence": "MIT OR Apache-2.0",
        "platform": {"en": "Linux · Wayland", "ru": "Linux · Wayland"},
        "stack": ["Rust", "smithay 0.7", "syngui"],
        "category": "DesktopEnhancementApplication",
        "status": {"en": "Early, build from source", "ru": "Ранняя стадия, сборка из исходников"},
        "title": {
            "en": "syndesktop — Wayland desktop environment written in Rust",
            "ru": "syndesktop — окружение рабочего стола Wayland на Rust",
        },
        "description": {
            "en": "Wayland desktop environment in Rust: a smithay compositor, a shell with a "
                  "macOS-style dock and panels, system settings, a file manager, a screenshot tool.",
            "ru": "Окружение рабочего стола Wayland на Rust: композитор на smithay, оболочка с доком "
                  "в стиле macOS и панелями, параметры системы, проводник и снимок экрана.",
        },
        "tagline": {
            "en": "A Wayland desktop environment in Rust, laid out like Plasma: a compositor, a shell and system settings as separate programs, configured through one file with changes applied live.",
            "ru": "Окружение рабочего стола для Wayland на Rust, устроенное как Plasma: композитор, оболочка и «Параметры системы» — отдельные программы, всё настраивается одним файлом, и изменения применяются на лету.",
        },
        "card": {
            "en": "Wayland desktop environment: a smithay compositor, a shell with a macOS-style dock and panels, system settings, a file manager and a screenshot tool.",
            "ru": "Рабочий стол для Wayland: композитор на smithay, оболочка с доком в стиле macOS и панелями, параметры системы, проводник и снимок экрана.",
        },
        "stats": [
            {"value": "5", "label": {"en": "programs: compositor, shell, settings, files, screenshot", "ru": "программ: композитор, оболочка, параметры, проводник, снимок"}},
            {"value": "14", "label": {"en": "built-in themes, plus your own in MSS", "ru": "встроенных тем и свои на MSS"}},
            {"value": "18", "label": {"en": "pages in system settings", "ru": "страниц в параметрах системы"}},
            {"value": "0.7", "label": {"en": "smithay under the compositor", "ru": "версия smithay в композиторе"}},
        ],
        "what": {
            "en": [
                "syndesktop is a desktop environment for Wayland, written in Rust, with its interface drawn by syngui. It is split the way Plasma is: a compositor, a shell and a system-settings app are separate programs.",
                "Almost everything is configured through ~/.config/syndesktop/config.toml, and changes apply on the fly. The settings app edits that file with toml_edit, so your comments survive.",
            ],
            "ru": [
                "syndesktop — окружение рабочего стола для Wayland на Rust, интерфейс нарисован на syngui. Устроено как Plasma: композитор, оболочка и «Параметры системы» — отдельные программы.",
                "Почти всё настраивается через ~/.config/syndesktop/config.toml, изменения применяются на лету. «Параметры системы» правят этот файл через toml_edit, так что комментарии в нём сохраняются.",
            ],
        },
        "features": {
            "en": [
                "Compositor on smithay 0.7: DRM/KMS with several GPUs, hotplug and DPMS, or a nested window; server-side decorations, workspaces, floating / tile / columns / grid / monocle layouts, snapping to screen halves, window overview, Alt+Tab, window rules, Xwayland and IPC.",
                "Shell on syngui (layer-shell): wallpaper, panels with applets, a launcher, D-Bus notifications, OSD, a power menu, a window switcher and a lock screen (ext-session-lock + PAM).",
                "A dock in the spirit of macOS and Latte Dock: icons grow under the pointer, window indicators, bounces and particles on launch, 3D tilt and a 3D shelf with reflections, stacks and folders, autohide and smart hide.",
                "An adaptive panel that stretches to the screen edge when a window is maximized or touches it, as in Plasma 6 — and a panel that becomes the title bar, with window title, window buttons and a global menu for Qt/KDE and GTK apps.",
                "System settings with 18 pages that edit config.toml in place.",
                "A file manager in the spirit of Windows 11: tabs in the title bar, two panes, icon / tile / list / table views, thumbnails, background operations with pause and cancel, Ctrl+Z, trash, search and a built-in image viewer (EXIF rotation, HEIC).",
                "A screenshot tool: the screen freezes, you drag a region with handles and a magnifier or click a window or monitor, then copy, save, copy the path or open.",
                "14 built-in themes — Nord, Catppuccin, Tokyo Night, Gruvbox, Rosé Pine, Everforest, Dracula, Kanagawa, Solarized and more — plus your own in MSS.",
                "Scriptable over IPC: syndesktop msg windows, action \"workspace 2\", restart-shell and more.",
            ],
            "ru": [
                "Композитор на smithay 0.7: DRM/KMS с несколькими GPU, горячим подключением и DPMS или вложенное окно; серверные рамки, рабочие столы, раскладки floating / tile / columns / grid / monocle, прилипание к половинам экрана, обзор окон, Alt+Tab, правила окон, Xwayland и IPC.",
                "Оболочка на syngui (layer-shell): обои, панели с апплетами, меню запуска, уведомления по D-Bus, OSD, меню питания, переключатель окон и экран блокировки (ext-session-lock + PAM).",
                "Док в духе macOS и Latte Dock: значок под курсором вырастает, индикаторы окон, прыжки и частицы при запуске, 3D-наклон и 3D-полка с отражениями, разделы и папки, автоскрытие и умное скрытие.",
                "Адаптивная панель, которая прижимается к краю во всю длину, когда окно развёрнуто или касается её, как в Plasma 6, — и панель вместо заголовка окна: заголовок, кнопки окна и глобальное меню для программ на Qt/KDE и GTK.",
                "«Параметры системы» — 18 страниц, которые правят config.toml на месте.",
                "Проводник в духе Windows 11: вкладки в заголовке, две панели, виды «значки / плитка / список / таблица», миниатюры, операции в фоне с паузой и отменой, Ctrl+Z, корзина, поиск и встроенный просмотрщик картинок (поворот по EXIF, HEIC).",
                "Снимок экрана: экран застывает, область выделяется рамкой с ручками и лупой, щелчок берёт окно или монитор; дальше — копировать, сохранить, скопировать путь или открыть.",
                "14 встроенных тем — Nord, Catppuccin, Tokyo Night, Gruvbox, Rosé Pine, Everforest, Dracula, Kanagawa, Solarized и другие — и свои на MSS.",
                "Управление через IPC: syndesktop msg windows, action \"workspace 2\", restart-shell и другое.",
            ],
        },
        "install": {
            "code": "cargo build --profile fast-release\ntarget/fast-release/syndesktop --nested   # try it in a window\nmakepkg -si                              # full session: then pick syndesktop at login",
            "note": {
                "en": "Build from source. The PKGBUILD in the repository installs a real session that you select in your login manager; --nested runs the compositor as a window inside your current session.",
                "ru": "Сборка из исходников. PKGBUILD из репозитория ставит полноценный сеанс, который выбирается в менеджере входа; с --nested композитор запускается окном внутри текущего сеанса.",
            },
        },
        "requirements": {
            "en": [
                "Linux with Wayland; X11 applications run through Xwayland.",
                "No prebuilt packages or AUR entry: you build it from source with Cargo (the PKGBUILD targets Arch Linux).",
                "An early, single-developer project — expect rough edges; logs go to ~/.local/state/syndesktop/.",
            ],
            "ru": [
                "Linux с Wayland; программы для X11 работают через Xwayland.",
                "Готовых пакетов и пакета в AUR нет: собирается из исходников через Cargo (PKGBUILD рассчитан на Arch Linux).",
                "Ранний проект одного разработчика — шероховатости будут; логи пишутся в ~/.local/state/syndesktop/.",
            ],
        },
        "built": {
            "en": "The model writes the code; I decide what to build, describe each task and check the result on my own machine. The whole interface — shell, dock, settings, file manager — is drawn with syngui, the same framework as synthos.",
            "ru": "Код пишет модель; я решаю, что делать, описываю каждую задачу и проверяю результат на своей машине. Весь интерфейс — оболочка, док, параметры, проводник — нарисован на syngui, том же фреймворке, что и synthos.",
        },
        # Screenshots: every image in syndesktop/docs/screenshots/ if the folder exists,
        # otherwise docs/themes.jpg. Re-read on every build.
        "hero": img("syndesktop/docs/themes.jpg",
                    "syndesktop themes: the same desktop in several built-in colour schemes",
                    "Темы syndesktop: один и тот же рабочий стол в нескольких встроенных оформлениях"),
        "gallery": [],
        "gallery_glob": "syndesktop/docs/screenshots/*",
        "glob_alt": {"en": "syndesktop screenshot", "ru": "Скриншот syndesktop"},
    },
    # ------------------------------------------------------------------ linux-legion
    # Source: linux_legion/README.md
    {
        "slug": "linux-legion",
        "name": "linux-legion",
        "repo": "https://github.com/VitaminDB/linux-legion",
        "readme": "https://github.com/VitaminDB/linux-legion#readme",
        "aur": ["linux-legion"],
        "licence": "MIT",
        "platform": {"en": "Linux · Lenovo Legion laptops", "ru": "Linux · ноутбуки Lenovo Legion"},
        "stack": ["Rust", "syngui", "hidraw"],
        "category": "UtilitiesApplication",
        "status": {"en": "Tested on Legion Pro 7 16IAX10H", "ru": "Проверено на Legion Pro 7 16IAX10H"},
        "title": {
            "en": "linux-legion — Lenovo Vantage alternative for Linux",
            "ru": "linux-legion — аналог Lenovo Vantage для Linux",
        },
        "description": {
            "en": "Control Lenovo Legion laptops on Linux: power modes, CPU power limits, fans, "
                  "per-key Spectrum RGB, battery charging modes. No root, no kernel module. AUR.",
            "ru": "Управление Lenovo Legion в Linux: режимы питания, лимиты мощности CPU, "
                  "вентиляторы, RGB-подсветка Spectrum, режимы зарядки. Без root и модулей ядра.",
        },
        "tagline": {
            "en": "A Linux control centre for Lenovo Legion laptops — what Lenovo Vantage and Legion Space do on Windows: power modes, CPU power limits, fans, per-key Spectrum RGB, battery modes and hardware switches.",
            "ru": "Центр управления ноутбуками Lenovo Legion для Linux — то, что в Windows делают Lenovo Vantage и Legion Space: режимы питания, лимиты мощности CPU, вентиляторы, RGB-подсветка Spectrum по клавишам, режимы батареи и аппаратные переключатели.",
        },
        "card": {
            "en": "Lenovo Vantage for Linux: power modes, CPU limits, fans, per-key Spectrum RGB, battery modes. No root, no kernel module.",
            "ru": "Lenovo Vantage для Linux: режимы питания, лимиты CPU, вентиляторы, RGB-подсветка Spectrum, режимы батареи. Без root и модулей ядра.",
        },
        "stats": [
            {"value": "12", "label": {"en": "lighting effects in the layer editor", "ru": "эффектов подсветки в редакторе слоёв"}},
            {"value": "6", "label": {"en": "hardware lighting profiles", "ru": "аппаратных профилей подсветки"}},
            {"value": "~10", "unit": "/s", "label": {"en": "key colours read back from the controller", "ru": "раз в секунду читаются цвета клавиш"}},
            {"value": "0", "label": {"en": "out-of-tree kernel modules, daemons, root", "ru": "сторонних модулей ядра, демонов и root"}},
        ],
        "what": {
            "en": [
                "linux-legion is written in Rust on syngui. It uses the upstream kernel drivers (lenovo-wmi-gamezone, lenovo-wmi-other, ideapad-laptop) and talks to the RGB controller directly through hidraw — no out-of-tree kernel module, no daemon and no root at runtime.",
                "A udev rule gives the logged-in user access to the RGB controller and makes the sysfs knobs writable for the wheel group. The README also documents the Spectrum protocol, including the Gen 10 quirks found on real hardware, for anyone porting it elsewhere.",
            ],
            "ru": [
                "linux-legion написан на Rust и syngui. Он пользуется штатными драйверами ядра (lenovo-wmi-gamezone, lenovo-wmi-other, ideapad-laptop) и общается с RGB-контроллером напрямую через hidraw — без стороннего модуля ядра, без демона и без root при работе.",
                "Правило udev даёт вошедшему пользователю доступ к RGB-контроллеру и открывает настройки в sysfs на запись группе wheel. В README описан и протокол Spectrum, включая особенности 10-го поколения, найденные на живом железе, — для тех, кто захочет перенести его куда-то ещё.",
            ],
        },
        "features": {
            "en": [
                "Home: power mode in one click, live CPU / GPU / memory / battery gauges and fan speeds; the NVIDIA GPU is polled only while it is already awake, so the dashboard never wakes the dGPU.",
                "Performance: Quiet, Balanced, Performance, Extreme and Custom (the same as Fn+Q); in Custom — CPU PL1 / PL2, every other limit the firmware exposes, and manual fan targets.",
                "Auto-apply: the firmware forgets custom limits after a reboot, so an optional user service restores them at login, when Custom mode is switched on and after resume.",
                "Spectrum lighting: six hardware profiles, brightness, the LEGION lid logo and a layer editor on a live key map with 12 effects; profiles are stored in the keyboard itself.",
                "Battery: Standard, Rapid charge or Conservation (≈80 %), plus charge level and health.",
                "Device: Fn Lock, camera kill switch, always-on USB charging and system information.",
                "--simulate shows the whole interface without the hardware; LEGION_TRACE=1 prints every RGB packet.",
            ],
            "ru": [
                "Главная: режим питания в один клик, живые шкалы CPU / GPU / памяти / батареи и обороты вентиляторов; видеокарта NVIDIA опрашивается, только если уже проснулась, так что панель не будит дискретную карту.",
                "Производительность: Quiet, Balanced, Performance, Extreme и Custom (то же, что Fn+Q); в Custom — PL1 / PL2 процессора, все остальные лимиты, которые отдаёт прошивка, и ручные обороты вентиляторов.",
                "Автоприменение: прошивка забывает свои лимиты после перезагрузки, поэтому необязательный пользовательский сервис возвращает их при входе, при включении Custom и после сна.",
                "Подсветка Spectrum: шесть аппаратных профилей, яркость, логотип LEGION на крышке и редактор слоёв на живой карте клавиш с 12 эффектами; профили хранятся в самой клавиатуре.",
                "Батарея: Standard, Rapid charge или Conservation (≈80 %), уровень заряда и износ.",
                "Устройство: Fn Lock, аппаратное отключение камеры, зарядка по USB в выключенном состоянии и сведения о системе.",
                "--simulate показывает весь интерфейс без железа; LEGION_TRACE=1 печатает каждый RGB-пакет.",
            ],
        },
        "install": {
            "code": "yay -S linux-legion        # or: paru -S linux-legion",
            "note": {
                "en": "The package installs the binary, a menu entry, icons and the udev rule. From source: cargo build --release, then install packaging/70-linux-legion.rules into /etc/udev/rules.d/ and reload udev.",
                "ru": "Пакет ставит бинарник, пункт меню, иконки и правило udev. Из исходников: cargo build --release, затем положить packaging/70-linux-legion.rules в /etc/udev/rules.d/ и перезагрузить правила udev.",
            },
        },
        "requirements": {
            "en": [
                "Developed and tested on one laptop: Legion Pro 7 16IAX10H (83F5, Core Ultra 9 275HX, RTX 5090 Laptop, Spectrum controller 048d:c197), Arch Linux, kernel 7.0.",
                "Other Legion models with the same kernel interfaces and a Spectrum controller (048d:c1xx / c9xx) should work — every page adapts to what the firmware reports — but are untested.",
                "The interface is in Russian for now.",
                "Unofficial and not affiliated with Lenovo. Power limits and fan targets go through the vendor's own firmware interfaces, but you use it at your own risk.",
            ],
            "ru": [
                "Разработан и проверен на одном ноутбуке: Legion Pro 7 16IAX10H (83F5, Core Ultra 9 275HX, RTX 5090 Laptop, контроллер Spectrum 048d:c197), Arch Linux, ядро 7.0.",
                "Другие модели Legion с теми же интерфейсами ядра и контроллером Spectrum (048d:c1xx / c9xx) должны работать — каждая страница подстраивается под то, что сообщает прошивка, — но не проверялись.",
                "Интерфейс пока только на русском.",
                "Неофициальный проект, с Lenovo не связан. Лимиты и обороты задаются через штатные интерфейсы прошивки, но вся ответственность — на вас.",
            ],
        },
        "built": {
            "en": "The model writes the code, the tests and most of the documentation. Every packet format was captured from and tested on my own Legion laptop — the live tests write layers to an inactive keyboard profile, read them back and restore the original byte for byte.",
            "ru": "Модель пишет код, тесты и большую часть документации. Каждый формат пакета снят с моего собственного Legion и проверен на нём — живые тесты пишут слои в неактивный профиль клавиатуры, читают обратно и восстанавливают исходный байт в байт.",
        },
        "hero": img("linux_legion/screenshots/home.png",
                    "linux-legion home page: power mode, CPU / GPU / memory / battery gauges and fan speeds",
                    "Главная страница linux-legion: режим питания, шкалы CPU / GPU / памяти / батареи и вентиляторы"),
        "gallery": [
            img("linux_legion/screenshots/lighting.png", "Spectrum lighting — live key map", "Подсветка Spectrum — живая карта клавиш"),
            img("linux_legion/screenshots/lighting-layers.png", "Lighting effect layers", "Слои эффектов подсветки"),
            img("linux_legion/screenshots/performance.png", "Performance modes, power limits and fans", "Режимы производительности, лимиты мощности и вентиляторы"),
            img("linux_legion/screenshots/battery.png", "Battery charging modes", "Режимы зарядки батареи"),
            img("linux_legion/screenshots/device.png", "Device switches and system information", "Переключатели устройства и сведения о системе"),
        ],
    },
    # ------------------------------------------------------------------ ardor-mouse
    # Source: ardor_mouse/README.md
    {
        "slug": "ardor-mouse",
        "name": "ardor-mouse",
        "repo": "https://github.com/VitaminDB/ardor-mouse",
        "readme": "https://github.com/VitaminDB/ardor-mouse#readme",
        "aur": ["ardor-mouse"],
        "licence": "MIT",
        "platform": {"en": "Linux · ARDOR GAMING Edge Air Ultra", "ru": "Linux · ARDOR GAMING Edge Air Ultra"},
        "stack": ["Rust", "syngui", "hidraw"],
        "category": "UtilitiesApplication",
        "status": {"en": "Tested on Edge Air Ultra", "ru": "Проверено на Edge Air Ultra"},
        "title": {
            "en": "ardor-mouse — ARDOR Edge Air Ultra mouse software for Linux",
            "ru": "ardor-mouse — настройка мыши ARDOR Edge Air Ultra в Linux",
        },
        "description": {
            "en": "Linux configurator for the ARDOR GAMING Edge Air Ultra mouse: DPI stages, RGB, "
                  "button remapping, polling rate. Reverse-engineered protocol, no root. On the AUR.",
            "ru": "Программа для мыши ARDOR GAMING Edge Air Ultra в Linux: DPI, RGB-подсветка, "
                  "кнопки, частота опроса. Протокол восстановлен реверс-инжинирингом, без root.",
        },
        "tagline": {
            "en": "A native Linux configuration tool for the ARDOR GAMING Edge Air Ultra wireless mouse — a replacement for the vendor's Windows-only OemDrv.exe.",
            "ru": "Нативная программа для настройки беспроводной мыши ARDOR GAMING Edge Air Ultra в Linux — замена фирменной OemDrv.exe, которая есть только под Windows.",
        },
        "card": {
            "en": "Linux configurator for the ARDOR GAMING Edge Air Ultra mouse — DPI, RGB, button remapping. Reverse-engineered protocol.",
            "ru": "Настройка мыши ARDOR GAMING Edge Air Ultra в Linux — DPI, подсветка, переназначение кнопок. Протокол восстановлен реверсом.",
        },
        "stats": [
            {"value": "8", "label": {"en": "DPI stages, each with its own colour", "ru": "ступеней DPI, у каждой свой цвет"}},
            {"value": "50–19 000", "label": {"en": "DPI range", "ru": "диапазон DPI"}},
            {"value": "7", "label": {"en": "lighting effects with live preview", "ru": "эффектов подсветки с живым превью"}},
            {"value": "30", "label": {"en": "tests on packets from a real mouse", "ru": "тестов на пакетах с настоящей мыши"}},
        ],
        "what": {
            "en": [
                "The vendor ships no Linux software and publishes no protocol. Everything here was reverse-engineered: the Windows utility was disassembled, its USB traffic compared against a live mouse, and every EEPROM field verified on real dumps.",
                "Written in Rust on syngui, it talks to the mouse directly through hidraw — no kernel module, no daemon, no root. Settings are read from the mouse's own memory and only the changed regions are written back, so the tool never overwrites what it does not understand.",
            ],
            "ru": [
                "Производитель не выпускает софта под Linux и не публикует протокол. Всё восстановлено реверс-инжинирингом: утилита для Windows дизассемблирована, её USB-трафик сверен с живой мышью, каждое поле EEPROM проверено на настоящих дампах.",
                "Программа написана на Rust и syngui и общается с мышью напрямую через hidraw — без модуля ядра, без демона и без root. Настройки читаются из памяти самой мыши, а обратно записываются только изменённые участки, так что программа не затирает то, чего не понимает.",
            ],
        },
        "features": {
            "en": [
                "DPI: up to 8 stages from 50 to 19 000 DPI, each with its own indicator colour; choose the active stage.",
                "RGB lighting: static, breathing, flow, neon, marquee, colour breathing or off — with colour, speed, brightness and a live preview.",
                "Buttons: remap all 6 — clicks, back / forward, DPI cycle / up / down, or disable.",
                "Sensor: polling rate 125 / 250 / 500 / 1000 Hz, lift-off distance 1 / 2 mm, debounce, angle snapping, ripple control, sleep timeout.",
                "Battery level and charging state.",
                "--simulate runs the app with a simulated mouse; ARDOR_TRACE=1 prints every packet exchanged with the mouse.",
                "The protocol and the EEPROM map are documented for anyone porting it to another tool or another mouse on the same controller.",
            ],
            "ru": [
                "DPI: до 8 ступеней от 50 до 19 000 DPI, у каждой свой цвет индикатора; выбор активной ступени.",
                "RGB-подсветка: статичная, дыхание, поток, неон, бегущая строка, дыхание цветом или выключена — цвет, скорость, яркость и живое превью.",
                "Кнопки: переназначение всех шести — клики, назад / вперёд, переключение DPI по кругу / вверх / вниз или отключение.",
                "Сенсор: частота опроса 125 / 250 / 500 / 1000 Гц, высота отрыва 1 / 2 мм, антидребезг, выравнивание линий, подавление дрожания, тайм-аут сна.",
                "Уровень заряда батареи и состояние зарядки.",
                "--simulate запускает программу с виртуальной мышью; ARDOR_TRACE=1 печатает каждый пакет обмена с мышью.",
                "Протокол и карта EEPROM описаны — для тех, кто захочет перенести их в другую программу или на другую мышь с тем же контроллером.",
            ],
        },
        "install": {
            "code": "yay -S ardor-mouse        # or: paru -S ardor-mouse",
            "note": {
                "en": "The package installs the binary, a menu entry, icons and a udev rule that gives the logged-in user access to the mouse; replug the receiver once if it was already plugged in. From source: cargo build --release plus the udev rule from packaging/.",
                "ru": "Пакет ставит бинарник, пункт меню, иконки и правило udev, которое даёт вошедшему пользователю доступ к мыши; если приёмник уже был вставлен, переподключите его один раз. Из исходников: cargo build --release и правило udev из packaging/.",
            },
        },
        "requirements": {
            "en": [
                "Tested only with the Edge Air Ultra: 2.4 GHz receiver 25a7:fa7c and USB cable 25a7:fa7b (PixArt PMW3370 sensor, JM03 controller). Other mice on the same controller may speak the same protocol.",
                "If the mouse is asleep the receiver answers but its memory is unreachable — move the mouse and the settings load by themselves.",
                "The interface is in Russian for now.",
                "Unofficial and not affiliated with ARDOR GAMING. EEPROM writes are done the way the vendor utility does them, but at your own risk.",
            ],
            "ru": [
                "Проверено только с Edge Air Ultra: приёмник 2,4 ГГц 25a7:fa7c и кабель USB 25a7:fa7b (сенсор PixArt PMW3370, контроллер JM03). Другие мыши на том же контроллере могут говорить на том же протоколе.",
                "Если мышь спит, приёмник отвечает, но её память недоступна — пошевелите мышью, и настройки загрузятся сами.",
                "Интерфейс пока только на русском.",
                "Неофициальный проект, с ARDOR GAMING не связан. Запись в EEPROM делается так же, как в фирменной утилите, но вся ответственность — на вас.",
            ],
        },
        "built": {
            "en": "The model writes the code, the tests and most of the documentation. The protocol was reverse-engineered from and tested on my own mouse; the tests decode packets and EEPROM dumps captured from it.",
            "ru": "Модель пишет код, тесты и большую часть документации. Протокол восстановлен и проверен на моей собственной мыши; тесты разбирают пакеты и дампы EEPROM, снятые с неё.",
        },
        "hero": img("ardor_mouse/screenshots/dpi.png",
                    "ardor-mouse: DPI stages with indicator colours",
                    "ardor-mouse: ступени DPI с цветами индикатора"),
        "gallery": [
            img("ardor_mouse/screenshots/lighting.png", "RGB lighting effects with a live preview", "Эффекты RGB-подсветки с живым превью"),
            img("ardor_mouse/screenshots/buttons.png", "Remapping the six buttons", "Переназначение шести кнопок"),
            img("ardor_mouse/screenshots/sensor.png", "Sensor: polling rate, lift-off distance, debounce", "Сенсор: частота опроса, высота отрыва, антидребезг"),
        ],
    },
]
