"""Blog: sections (one per project) and posts. Texts EN + RU.

Images and media are paths relative to REPOS_ROOT (content.py). A post body is a list of blocks:
    ("p", {"en": ..., "ru": ...})                     paragraph
    ("h", {"en": ..., "ru": ...})                     subheading (h2)
    ("shots", [(path, {"en": caption, "ru": caption}), ...])   phone screenshots in a row
    ("wide", path_or_{"en","ru"}, {"en","ru"})        one wide image with caption
    ("gif", path, {"en","ru"})                        animation (GIF)
    ("video", path, {"en","ru"})                      MP4 with controls
    ("list", {"en": [...], "ru": [...]})              bullet list
"""

D = "alexeyev.dev/blog/2026-10-synmobile-12t-pro"
RAW = D + "/raw/"
VID = D + "/video/"

# Link to the 4pda thread; empty until the post is published there.
FOURPDA_URL = ""

UI = {
    "en": {
        "nav": "Blog",
        "title": "Blog — Vitaliy Alexeyev",
        "h1": "Blog",
        "lead": "Screenshots, videos and notes from my projects, one section per project.",
        "description": "Notes, screenshots and videos from my projects: Arch Linux on a phone, a Wayland desktop in Rust, GUI and ML engines.",
        "posts": "posts",
        "read": "Read",
        "back": "All posts",
        "section": "Section",
        "discuss": "Discussion on 4pda",
        "more_in": "More in this section",
        "video_file": "MP4 file",
        "open_full": "open full size",
    },
    "ru": {
        "nav": "Блог",
        "title": "Блог — Виталий Алексеев",
        "h1": "Блог",
        "lead": "Скриншоты, ролики и заметки о моих проектах — по разделу на проект.",
        "description": "Заметки, скриншоты и видео моих проектов: Arch Linux на телефоне, Wayland-окружение на Rust, GUI- и ML-движки.",
        "posts": "записей",
        "read": "Читать",
        "back": "Все записи",
        "section": "Раздел",
        "discuss": "Обсуждение на 4pda",
        "more_in": "Ещё в этом разделе",
        "video_file": "Файл MP4",
        "open_full": "открыть в полном размере",
    },
}

SECTIONS = [
    {
        "slug": "synshell",
        "name": "synshell",
        "about": {
            "en": "My Wayland desktop environment for computers and phones: releases and applications.",
            "ru": "Моё окружение рабочего стола Wayland для компьютеров и телефонов: выпуски и программы.",
        },
        "project": "synshell",
    },
    {
        "slug": "synmobile",
        "name": "synmobile",
        "about": {
            "en": "Arch Linux ARM on Android phones with my own shell, synshell. First device: Xiaomi 12T Pro (Redmi K50 Ultra, diting).",
            "ru": "Arch Linux ARM на Android-телефонах с моей оболочкой synshell. Первый телефон — Xiaomi 12T Pro (Redmi K50 Ultra, diting).",
        },
        "project": None,
    },
]

POSTS = [
    {
        "slug": "synshell-0-2-0",
        "section": "synshell",
        "tags": ["release", "desktop", "phone"],
        "date": "2026-11-07",
        "cover": "synshell/docs/screenshots/desktop.png",
        "title": {"en": "synshell 0.2.0: the first public release", "ru": "synshell 0.2.0: первый публичный выпуск"},
        "summary": {
            "en": "Wayland desktop in Rust for computers and phones: compositor, desktop, phone and game shells, System Settings and 31 apps. Packages in the AUR.",
            "ru": "Рабочий стол Wayland на Rust для ПК и телефонов: композитор, оболочки для ПК, телефона и игр, «Параметры системы» и 31 приложение. Пакеты в AUR.",
        },
        "body": [
            ("p", {"en": "synshell is the desktop I use every day on my laptop and on my phone. Version 0.2.0 is the first one published: prebuilt packages for x86_64 and aarch64 are in the AUR, archives are attached to the GitHub release.",
                   "ru": "synshell — рабочий стол, которым я пользуюсь каждый день на ноутбуке и на телефоне. Версия 0.2.0 — первая опубликованная: готовые пакеты для x86_64 и aarch64 лежат в AUR, архивы приложены к выпуску на GitHub."}),
            ("wide", {"en": "synshell/docs/screenshots/desktop.png", "ru": "synshell/docs/screenshots/desktop-ru.png"}, {"en": "The Nord theme: a floating top panel, the dock, the file manager, Resource Monitor and the terminal", "ru": "Тема Nord: плавающая верхняя панель, док, Проводник, Монитор ресурсов и Терминал"}),
            ("h", {"en": "How it is built", "ru": "Как устроено"}),
            ("p", {"en": "It is split the way KDE Plasma is: the synwm compositor on smithay, a separate shell process for panels, dock, launcher and notifications, and System Settings. If the shell crashes, the compositor restarts it and the windows stay. Almost everything is configured in one file, ~/.config/synshell/config.toml, and applied live; System Settings edits it in place and keeps comments. Every window and panel is drawn with syngui, my GUI framework.",
                   "ru": "Устроено как KDE Plasma: композитор synwm на smithay, отдельный процесс оболочки с панелями, доком, меню запуска и уведомлениями и «Параметры системы». Если оболочка упадёт, композитор перезапустит её, а окна останутся. Почти всё настраивается в одном файле, ~/.config/synshell/config.toml, и применяется на лету; «Параметры системы» правят его на месте и сохраняют комментарии. Все окна и панели нарисованы на syngui — моём GUI-фреймворке."}),
            ("h", {"en": "Desktop", "ru": "Рабочий стол"}),
            ("list", {"en": ["Three panel layouts out of the box — top panel with a dock, classic taskbar (the default) and a vertical panel — and any of your own, edited with the mouse.",
                             "Floating, tile, columns, grid and monocle layouts, window overview, Alt+Tab, window rules, Xwayland.",
                             "The panel becomes the title bar of a maximized window, with a global menu for Qt/KDE and GTK 3.",
                             "14 themes, Nord by default; the palette is passed to GTK, Qt/KDE and GIMP.",
                             "Own lock screen, screen-sharing and screenshot portal over PipeWire, interface in 14 languages."],
                      "ru": ["Три раскладки панелей из коробки — верхняя панель с доком, классическая панель задач (по умолчанию) и вертикальная — и любые свои, мышью.",
                             "Раскладки окон «плавающая», «мозаика», «колонки», «сетка» и «монокль», обзор окон, Alt+Tab, правила окон, Xwayland.",
                             "Панель становится заголовком развёрнутого окна с глобальным меню для Qt/KDE и GTK 3.",
                             "14 тем, по умолчанию Nord; палитра передаётся в GTK, Qt/KDE и GIMP.",
                             "Свой экран блокировки, портал показа экрана и снимков через PipeWire, интерфейс на 14 языках."]}),
            ("wide", {"en": "synshell/docs/screenshots/classic.png", "ru": "synshell/docs/screenshots/classic-ru.png"}, {"en": "Classic taskbar — the default layout", "ru": "Классическая панель задач — раскладка по умолчанию"}),
            ("h", {"en": "Phone and game mode", "ru": "Телефон и игровой режим"}),
            ("p", {"en": "The same compositor runs a phone shell with an on-screen keyboard and phone apps: Phone, Messages, Camera, NFC, Compass, Sports and health, IR remote. Game mode (Super+G) is a fullscreen launcher with the Steam library, covers and gamepad navigation; Android apps run in a LineageOS container, each in its own window.",
                   "ru": "Тот же композитор запускает оболочку телефона с экранной клавиатурой и телефонными приложениями: Телефон, Сообщения, Камера, NFC, Компас, Спорт и здоровье, ИК-пульт. Игровой режим (Super+G) — полноэкранное меню с библиотекой Steam, обложками и управлением с геймпада; Android-приложения работают в контейнере LineageOS, каждое в своём окне."}),
            ("shots", [("synshell/docs/screenshots/phone.png", {"en": "Phone: home screen", "ru": "Телефон: домашний экран"}),
                       ("synshell/docs/screenshots/phone-shade.png", {"en": "Phone: quick settings", "ru": "Телефон: быстрые настройки"})]),
            ("h", {"en": "Applications", "ru": "Приложения"}),
            ("p", {"en": "31 applications, each with its own page on this site: System Settings, file manager, terminal, software center for Arch and AUR, Resource Monitor, theme editor, Notes, passwords, virtual machines, video and music players, voice recorder, Maps, an assistant on local neural networks, cycle tracker, QuitSmoke and Syn Blocks.",
                   "ru": "31 приложение, у каждого своя страница на этом сайте: «Параметры системы», Проводник, Терминал, «Программы» для Arch и AUR, Монитор ресурсов, Редактор тем, Заметки, Пароли, Виртуальные машины, Видео и Музыка, Диктофон, Карты, Ассистент на локальных нейросетях, «Цикл», «Бросить курить» и Syn Blocks."}),
            ("h", {"en": "Install", "ru": "Установка"}),
            ("list", {"en": ["yay -S synshell-bin — the desktop and all applications; synshell-core-bin — the minimum; any application on its own by its package name.",
                             "Then pick “synshell” in your display manager, or enable the bundled login screen: systemctl enable synlogin.service."],
                      "ru": ["yay -S synshell-bin — рабочий стол и все приложения; synshell-core-bin — минимум; любое приложение отдельно — по имени пакета.",
                             "Затем выберите «synshell» в менеджере входа или включите встроенный экран входа: systemctl enable synlogin.service."]}),
            ("h", {"en": "What to keep in mind", "ru": "Что учесть"}),
            ("list", {"en": ["Early: one developer, the first commit is from September 2026.",
                             "Tested on one laptop (Intel iGPU + NVIDIA RTX 5090 Laptop GPU) and one phone (Xiaomi 12T Pro). Other hardware is handled in the code but untested."],
                      "ru": ["Ранняя стадия: один разработчик, первый коммит — сентябрь 2026.",
                             "Проверено на одном ноутбуке (Intel iGPU + NVIDIA RTX 5090 Laptop GPU) и одном телефоне (Xiaomi 12T Pro). Другое железо учтено в коде, но не проверялось."]}),
        ],
    },
    {
        "slug": "synmobile-boot-and-login",
        "section": "synmobile",
        "date": "2026-10-23",
        "cover": RAW + "09-login.png",
        "title": {"en": "Arch Linux on Xiaomi 12T Pro: boot and login", "ru": "Arch Linux на Xiaomi 12T Pro: загрузка и вход"},
        "summary": {
            "en": "Dual boot with Android, a boot splash drawn straight to KMS, the login and lock screens.",
            "ru": "Двойная загрузка с Android, заставка прямо на KMS, экран входа и блокировки.",
        },
        "body": [
            ("p", {
                "en": "My Xiaomi 12T Pro boots real Arch Linux ARM next to Android. Not a chroot and not Termux: the stock GKI 5.10 kernel with the phone's own vendor modules, systemd, and my Wayland shell synshell on top. Android stays where it was, and Arch lives in an image file on /data.",
                "ru": "Мой Xiaomi 12T Pro загружает настоящий Arch Linux ARM рядом с Android. Не chroot и не Termux: штатное ядро GKI 5.10 с vendor-модулями самого телефона, systemd и сверху моя Wayland-оболочка synshell. Android остаётся на месте, Arch живёт образом в /data.",
            }),
            ("wide", {"en": RAW.replace("raw/", "framed/") + "00-dualboot-en.jpg", "ru": RAW.replace("raw/", "framed/") + "00-dualboot.jpg"}, {
                "en": "The boot menu has no screen: the phone vibrates, Vol+ starts Arch, Vol− starts Android, no key repeats the last choice.",
                "ru": "У меню нет экрана: телефон вибрирует, Vol+ — Arch, Vol− — Android, ничего не нажали — прошлый выбор.",
            }),
            ("p", {
                "en": "You can try it without flashing anything: fastboot boot loads the image once. For everyday use the boot partition gets a small menu; the stock image is backed up first.",
                "ru": "Попробовать можно, ничего не прошивая: fastboot boot загружает образ один раз. Для постоянной работы в boot ставится маленькое меню, стоковый образ перед этим сохраняется.",
            }),
            ("shots", [
                (RAW + "00-boot-splash.png", {"en": "Boot splash: synsplash draws to DRM/KMS from the initramfs", "ru": "Заставка: synsplash рисует прямо в DRM/KMS ещё из initramfs"}),
                (RAW + "09-login.png", {"en": "Login screen (synlogin) with its own on-screen keyboard", "ru": "Экран входа synlogin со своей экранной клавиатурой"}),
                (RAW + "07-lock-cover.png", {"en": "Lock screen", "ru": "Экран блокировки"}),
                (RAW + "08-lock-pin.png", {"en": "PIN pad, or a full keyboard via «ABC»", "ru": "Ввод PIN или полная клавиатура «ABC»"}),
            ]),
            ("gif", VID + "boot-splash.gif", {"en": "The spinner turns once every 0.96 s, as on the device.", "ru": "Кольцо делает оборот за 0,96 с — как на телефоне."}),
        ],
    },
    {
        "slug": "synmobile-shell",
        "section": "synmobile",
        "date": "2026-10-23",
        "cover": RAW + "02-desk-1.png",
        "title": {"en": "synshell on a phone: desktops, widgets, shades", "ru": "synshell на телефоне: столы, виджеты, шторки"},
        "summary": {
            "en": "Home pages with live hardware widgets, two pull-down shades, the launcher, recents and a charging animation.",
            "ru": "Страницы стола с живыми виджетами железа, две шторки, «Пуск», «Недавние» и анимация зарядки.",
        },
        "body": [
            ("p", {
                "en": "The phone runs the same desktop environment as my laptop: the synwm compositor, built on smithay, and a phone shell, synmobile-shell. Composition runs on the Adreno 730 GPU through zink on top of the turnip Vulkan driver. Everything below is written in Rust on my GUI framework syngui.",
                "ru": "На телефоне то же окружение, что на ноутбуке: композитор synwm на smithay и телефонная оболочка synmobile-shell. Композитинг идёт на GPU Adreno 730 через zink поверх Vulkan-драйвера turnip. Всё ниже написано на Rust на моём GUI-фреймворке syngui.",
            }),
            ("video", VID + "ui-tour-720p.mp4", {"en": "40 seconds around the shell, recorded with synlink from a laptop.", "ru": "40 секунд по оболочке; записано с ноутбука через synlink."}),
            ("h", {"en": "Home pages", "ru": "Рабочие столы"}),
            ("shots", [
                (RAW + "02-desk-1.png", {"en": "CPU, memory, GPU, battery and network widgets", "ru": "Виджеты процессора, памяти, графики, питания и сети"}),
                (RAW + "02-desk-2.png", {"en": "App icons and running apps", "ru": "Значки приложений и запущенные программы"}),
                (RAW + "02-desk-3.png", {"en": "Temperatures, cores, storage, VRAM, charging power", "ru": "Температуры, ядра, хранилище, видеопамять, мощность зарядки"}),
            ]),
            ("gif", VID + "desks.gif", {"en": "Pages follow the finger; the panorama wallpaper moves with them.", "ru": "Страницы идут за пальцем, панорамные обои едут вместе с ними."}),
            ("h", {"en": "Shades, launcher, recents", "ru": "Шторки, «Пуск», «Недавние»"}),
            ("shots", [
                (RAW + "03-quick-settings.png", {"en": "Quick settings: the linked laptop, Wi-Fi, Bluetooth, window mode, game mode", "ru": "Быстрые настройки: связанный ноутбук, Wi-Fi, Bluetooth, режим окон, игровой режим"}),
                (RAW + "04-notifications.png", {"en": "Notifications", "ru": "Уведомления"}),
                (RAW + "05-launcher.png", {"en": "Launcher with Linux and Android apps", "ru": "«Пуск»: Linux- и Android-приложения"}),
                (RAW + "06-recents.png", {"en": "Recents with live window thumbnails", "ru": "«Недавние» с живыми миниатюрами окон"}),
            ]),
            ("h", {"en": "Charging", "ru": "Зарядка"}),
            ("shots", [
                (RAW + "01-charging-a.png", {"en": "Plug in the cable — the charge level and an energy stream", "ru": "Подключили кабель — уровень заряда и поток частиц"}),
            ]),
            ("gif", VID + "charging.gif", {"en": "The charging animation.", "ru": "Анимация зарядки."}),
        ],
    },
    {
        "slug": "synmobile-apps",
        "section": "synmobile",
        "date": "2026-10-23",
        "cover": RAW + "12-terminal.png",
        "title": {"en": "synmobile: apps and the link to a PC", "ru": "synmobile: приложения и связь с ПК"},
        "summary": {
            "en": "Settings, file manager, terminal with an on-screen keyboard, resource monitor, maps and the phone's screen on a laptop.",
            "ru": "Параметры, проводник, терминал с экранной клавиатурой, монитор ресурсов, карты и экран телефона на ноутбуке.",
        },
        "body": [
            ("p", {
                "en": "Every app here is a crate of synshell on syngui; the same binaries run on the laptop and adapt to a narrow portrait screen.",
                "ru": "Каждое приложение здесь — крейт synshell на syngui; те же программы работают на ноутбуке и подстраиваются под узкий вертикальный экран.",
            }),
            ("shots", [
                (RAW + "10-settings.png", {"en": "System Settings: one config.toml, comments survive", "ru": "Параметры: один config.toml, комментарии сохраняются"}),
                (RAW + "11-files.png", {"en": "File manager", "ru": "Проводник"}),
                (RAW + "12-terminal.png", {"en": "Terminal and the on-screen keyboard with Esc, Tab, Ctrl and arrows", "ru": "Терминал и экранная клавиатура с Esc, Tab, Ctrl и стрелками"}),
            ]),
            ("shots", [
                (RAW + "13-sysinfo.png", {"en": "Resource monitor: CPU, Adreno 730, Hexagon NPU, sensors", "ru": "Монитор ресурсов: CPU, Adreno 730, NPU Hexagon, датчики"}),
                (RAW + "14-maps.png", {"en": "Maps: OpenStreetMap, GPS through GeoClue, routes", "ru": "Карты: OpenStreetMap, GPS через GeoClue, маршруты"}),
                (RAW + "50-link-window.png", {"en": "synlink: the phone's screen in a window on the laptop", "ru": "synlink: экран телефона в окне на ноутбуке"}),
            ]),
            ("p", {
                "en": "synlink links the phone and the PC over USB or Wi-Fi (QUIC with pinned keys): screen and remote input, files, notifications, a shared clipboard and ssh without knowing addresses. All screenshots and videos in this blog were taken through it.",
                "ru": "synlink связывает телефон и ПК по USB или Wi-Fi (QUIC с закреплёнными ключами): экран и управление, файлы, уведомления, общий буфер обмена и ssh без адресов. Все скриншоты и ролики этого блога сняты через него.",
            }),
        ],
    },
    {
        "slug": "synmobile-games-and-android",
        "section": "synmobile",
        "date": "2026-10-23",
        "cover": RAW + "30-cuphead-a.png",
        "title": {"en": "synmobile: Windows games and Android apps", "ru": "synmobile: Windows-игры и Android-приложения"},
        "summary": {
            "en": "A console-style game mode, Steam, Cuphead through Wine with an on-screen gamepad, and Android apps in a container.",
            "ru": "Игровой режим как у консоли, Steam, Cuphead через Wine с экранным геймпадом и Android-приложения в контейнере.",
        },
        "body": [
            ("p", {
                "en": "Game mode turns the shell into a console-style launcher: Steam library, Windows games under Wine, Linux games and Android apps in one place, gamepad navigation, every app fullscreen without frames.",
                "ru": "Игровой режим превращает оболочку в лаунчер как у консоли: библиотека Steam, Windows-игры под Wine, Linux-игры и Android-приложения в одном месте, управление геймпадом, каждое приложение во весь экран без рамок.",
            }),
            ("wide", RAW + "21-gameshell-land.png", {"en": "Game mode: recent games and apps", "ru": "Игровой режим: недавние игры и приложения"}),
            ("wide", RAW + "22-gameshell-games.png", {"en": "Games: Wine, Linux, Minecraft through Prism Launcher", "ru": "Игры: Wine, Linux, Minecraft через Prism Launcher"}),
            ("h", {"en": "Windows games through Wine", "ru": "Windows-игры через Wine"}),
            ("p", {
                "en": "Windows games run through wine-arm64ec with DXVK on the turnip Vulkan driver, through Xwayland. Touches become a mouse, and the on-screen controller emulates an Xbox 360 pad.",
                "ru": "Windows-игры идут через wine-arm64ec и DXVK на Vulkan-драйвере turnip, через Xwayland. Касания превращаются в мышь, экранный контроллер изображает геймпад Xbox 360.",
            }),
            ("wide", RAW + "30-cuphead-a.png", {"en": "Cuphead (GOG) through Wine on Snapdragon 8+ Gen 1", "ru": "Cuphead (GOG) через Wine на Snapdragon 8+ Gen 1"}),
            ("video", VID + "cuphead-720p.mp4", {"en": "Cuphead with sound, controlled with the on-screen gamepad.", "ru": "Cuphead со звуком, управление экранным геймпадом."}),
            ("h", {"en": "Android apps", "ru": "Android-приложения"}),
            ("p", {
                "en": "Android runs in a container (LineageOS 20 with Google apps) and its apps open as ordinary windows of the Linux shell.",
                "ru": "Android работает в контейнере (LineageOS 20 с приложениями Google), а его приложения открываются обычными окнами Linux-оболочки.",
            }),
            ("wide", RAW + "24-gameshell-android.png", {"en": "Android apps in game mode", "ru": "Android-приложения в игровом режиме"}),
            ("shots", [
                (RAW + "41-android-settings.png", {"en": "Android Settings as a window", "ru": "Настройки Android окном"}),
            ]),
        ],
    },
]
