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
