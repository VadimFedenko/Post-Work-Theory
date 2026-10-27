# Инфографики к article.md: данные и методика

Созданы семь пар изображений: русский и английский PNG, а также SVG для каждой версии. Это редакторская визуализация каталога, а не репрезентативное исследование всей научной фантастики. Единица счёта — общество в указанном населении, периоде и континуитете; не произведение и не число его зрителей.

Источник: [data/societies.json](../../data/societies.json), 890 записей. Контрольная сумма SHA-256: `c61b381bc0206add377d171d368cd8d4e48e65a640a53ac2b91b5a45164ff119`. Основная база не изменялась. Машиночитаемые основания дополнительных оценок: [editorial-assessments.json](editorial-assessments.json). Расчётные показатели: [metrics.json](metrics.json), [stage-matrices.csv](stage-matrices.csv).

Общие правила: дистопичной считается отрицательная редакторская оценка `utopia_score < 0`. Это более широкая категория, чем «выраженная дистопия» с U ≤ −0,5. Почти все оценки имеют низкую уверенность. Проценты округлены для чтения; точные числители и знаменатели сохраняются ниже. Сходство оценок не устанавливает причинность.

<a id="01-infrastructure"></a>
## 01. ИИ не стал прямым снабжением

**12 / 890 = 1.3483%**, на изображении около 1,3%. Это **минимальная редакторская подборка**, а не точная оценка распространённости и не новая исчерпывающая классификация всех 890 записей.

Критерий: в мире показаны или известны мощные технологии автоматизации, однако выбранное население не получает от них прямого автоматического производства и снабжения обычными материальными благами из-за запрета, отказа, ограничения или разделения инфраструктур. Требуется содержательное основание в текущей записи. Одного статуса `zero_variant` недостаточно. Нельзя объявить дополнение до 100% обществами с доказанным прямым снабжением: оно содержит другие и неопределённые случаи.

**Это не буквальное отсутствие любого вклада машин.** В «Дюне» сохраняется обычная неразумная техника, а GAIA в Horizon, Winds в Ventus и системы Heaven’s River поддерживают среду обитания. Такие услуги — реальный косвенный вклад. Поэтому исходная фраза около картинки уточнена до «системы прямого снабжения людей». Знаменатель 890 — вся коллекция, а не отдельно подсчитанные миры с достоверно действующей ИИ-инфраструктурой.

| Запись | Основание включения |
|---|---|


| `dune-post-jihad-imperium` — Dune — The post-Butlerian Imperium | Запрет или подавление доступной технологии. Thinking machines are prohibited; ordinary non-thinking machinery remains. This is not zero mechanization. |
| `threat-robot-labor-veto` — The Threat of the Robot (Ball's restriction on labor automation) | Запрет или подавление доступной технологии. Installed robot production is prevented from starting and displaced workers are recalled. |
| `singularity-sky-new-republic` — Singularity Sky (The New Republic before contact) | Запрет или подавление доступной технологии. The regime suppresses productive technologies available in the surrounding civilization. |
| `fractale-granitz-offgrid` — Fractale — Granitz’s off-grid Lost Millennium community | Локальный сознательный отказ от автоматического снабжения. The local community rejects the automatic provision network; this does not describe connected Fractale residents. |
| `monk-robot-backland-automation-refusal` — Monk & Robot — Panga’s anti-automation community | Локальный сознательный отказ от автоматического снабжения. The selected community explicitly avoids automation, not all of Panga. |
| `trek-baku-chosen-handwork` — Star Trek — The Ba’ku’s chosen handwork | Локальный сознательный отказ от автоматического снабжения. The villagers know advanced machinery but choose handwork in daily life. |
| `emphyrio-halma-handicraft-restriction` — Emphyrio — Halma’s prohibited mass production | Запрет или подавление доступной технологии. Mass manufacturing and mechanical reproduction are prohibited on Halma despite their availability elsewhere. |
| `horizon-tribal-gaia-ecology-zero` — Horizon Zero Dawn — Tribes under GAIA’s ecology | Поддержка среды или ограничение доступа вместо прямого снабжения. GAIA maintains the biosphere; tribes still obtain food and build homes through work. Ecology is an indirect contribution, not literally no contribution. |
| `oa-metasoft-wurm-primitivism` — Orion’s Arm — Metasoft’s Wurm baseline reserve | Поддержка среды или ограничение доступа вместо прямого снабжения. Technological guardians preserve a hunter-gatherer reserve instead of giving residents ordinary automated production. |
| `ventus-winds-technological-ceiling` — Ventus — Human society under the Winds’ ceiling | Поддержка среды или ограничение доступа вместо прямого снабжения. Winds maintain a habitable biosphere but suppress advanced human technology; residents retain subsistence and craft work. |
| `heavens-river-iron-age` — Heaven’s River (Quinlan technology restriction — zero variant) | Поддержка среды или ограничение доступа вместо прямого снабжения. The advanced habitat is maintained while its residents are restricted to an Iron Age economy. |
| `nier-replicant-inherited-tech-zero` — NieR Replicant — The subsistence Replicant communities | Старый технологический проект отделён от повседневного производства. An older preservation project coexists with present farming, fishing and paid errands rather than directly supplying necessities. |


Полные границы населений, собранные свидетельства и идентификаторы источников сохранены в JSON. Нового полного просмотра каждого произведения не заявляется. Пограничные случаи не добавлены автоматически:
- `reignsteel-london-human-zero`: Nonintervention is described, but the saved account does not establish the complete absence of direct technical provision. Excluded from the minimum.
- `her-after-os-withdrawal-zero`: Immediate aftermath is an explicit projection; no settled post-departure economy is depicted. Excluded from the conservative count.
- `erewhon-machine-ban`: A machine ban is explicit but an actually existing AI infrastructure is not established. Excluded.
- `warframe-orokin-selective-automation-ban`: Selective AI suppression coexists with productive technology and minor robots. Excluded from a no-direct-provision comparison.
- `warhammer-imperial-servitor-ai-restrictions`: AI suppression and coerced person labor do not establish a total absence of productive automation. Excluded.
- `idiran-empire-before-defeat`: Rejection of independent machine sovereignty does not establish that automated factories are absent. Excluded.
- `algebraist-mercatoria`: Persecution of AI does not itself measure industrial automation. Excluded.
- `twilightzone-cave-food-advice-zero`: Computer food-safety advice is already a useful contribution to material survival. Excluded.


<a id="02-technology-work"></a>
## 02. Потенциал технологий и участие в работе

Использованы **18 явно выбранных примеров**, а не все 890 обществ и не случайная выборка. Для каждого сделана независимая грубая субъективная оценка возможностей мира: индустриальные системы; роботы и ИИ; планетарные и космические системы; преобразование материи или поддержка цифровых личностей. Эта шкала не объективная универсальная последовательность цивилизаций. При присвоении уровня доля работающих и посттрудовой статус не использованы как критерии.

Оценивается потенциал в самом мире, в том числе инфраструктура вокруг общества. Это существенно для Horizon: жители не владеют всеми возможностями GAIA. Положение «Дюны» также отражает космические возможности, а не разрешённость мыслящих машин.

Каждая точка — один выбранный пример. Ромб — медиана **примеров данного уровня**, а не оценка всей фантастики. Участие взято из базы без переоценки: `100 × (1 − axis.nonworking)`. Это доля лиц с регулярной полезной деятельностью или назначениями, включая неоплачиваемую заботу и добровольные проекты, а не рабочие часы или доля человеческого промышленного выпуска. Изображение показывает, что большая техническая мощность совместима с продолжающейся деятельностью. Оно не измеряет влияние технологического прогресса на занятость.

У 886 из 890 исходных оценок участия низкая уверенность, медианная ширина редакторского диапазона составляет 75 п.п. Подробный [аудит измерения участия](../exploratory-analysis/working-participation.md).

| Пример | Уровень | Работает, центральная оценка | Сохранённый диапазон |
|---|---:|---:|---:|


| `orwell-oceania` — Океания / Oceania | 1 | 85% | 60%–98% |

| `sleeper-graham-trustees` — Спящий пробуждается / The Sleeper Awakes | 1 | 80% | 45%–95% |

| `player-piano-pre-revolt` — Механическое пианино / Player Piano | 1 | 75% | 35%–95% |

| `manna-australia` — Манна: Австралия / Manna: Australia | 2 | 45% | 15%–80% |

| `cyberpunk-night-city` — Найт-Сити / Night City | 2 | 70% | 40%–90% |

| `detroit-before-revolution` — Детройт / Detroit | 2 | 55% | 30%–75% |

| `her-before-departure` — Она / Her | 2 | 70% | 35%–90% |

| `scythe-thunderhead-provision` — Жнец / Scythe | 2 | 45% | 15%–80% |

| `noon-earth` — Мир Полудня / Noon Earth | 3 | 60% | 25%–90% |

| `dune-post-jihad-imperium` — Дюна / Dune | 3 | 80% | 55%–95% |

| `solaria-naked-sun` — Солярия / Solaria | 3 | 55% | 15%–90% |

| `walle-axiom` — Аксиома / Axiom | 3 | 1% | 0%–5% |

| `horizon-tribal-gaia-ecology-zero` — Horizon / Horizon | 3 | 80% | 45%–95% |

| `culture-main` — Культура / The Culture | 4 | 40% | 10%–80% |

| `star-trek-federation-core` — Федерация / The Federation | 4 | 50% | 20%–80% |

| `city-stars-diaspar` — Диаспар / Diaspar | 4 | 30% | 5%–70% |

| `city-stars-lys` — Лис / Lys | 4 | 75% | 40%–95% |

| `diaspora-konishi` — Кониси / Konishi | 4 | 70% | 20%–95% |


<a id="03-six-regimes"></a>
## 03. Координатная матрица

Горизонталь: гарантии слева, отсутствие гарантий справа. Вертикаль: распределённый контроль сверху, элиты посередине, автономные системы снизу. Номера в текущей классификации:

| Контроль | С гарантиями | Без гарантий |
|---|---:|---:|
| Общество | 3 | 4 |
| Элиты | 1 | 2 |
| Автономная система | 5 | 6 |

Это схема двух смысловых вопросов, не новая числовая оценка стран или обществ. У исходных осей диапазон гарантий −1…+1 и контроля −1…+1; в графике числа осей убраны ради чтения.

<a id="04-elite-guarantees-examples"></a>
## 04. Примеры первого уклада

Все **126** записей с `regime_primary == 1`, в том числе частичные переходы. Из них для иллюстрации выбраны четыре знакомых произведения; это не весь список и не утверждение, что произведение целиком содержит только один уклад.

| ID | Выбранное население |
|---|---|


| `brave-new-world-state` | Humans within the World State's caste order |

| `elysium-protected-citizens` | Living admitted Elysium citizens |

| `expanse-earth-basic-assistance` | Registered Earth citizens eligible for Basic, including those without employment |

| `san-junipero-permanent-residents` | Active human-derived permanent residents |


Особенно важно, что у «Элизиума» взяты защищённые граждане станции, а не все люди на Земле; у «Пространства» — Земля с Basic Assistance. Обложки — уже собранные локальные изображения произведений, а не доказательства конкретного периода, населения или финала. Права и происхождение сохраняются в `record.assets`, открытая лицензия не предполагается.

Поздняя «Аксиома» в текущей базе имеет основной уклад 5, поэтому она не вставлена как бесспорный пример уклада 1, даже если соседний авторский текст допускает корпоративную интерпретацию.

<a id="05-work-postwork-matrices"></a>
## 05. Трудовые и посттрудовые общества на матрице

Слева **345** `zero_variant`, справа **470** `post_work`. **75** `transition` в эту пару не входят. Размер матриц одинаков; ячейки показывают проценты внутри соответствующей стадии. Цветовая насыщенность использует общий масштаб, а не отдельный максимум для каждой матрицы. Номера укладов сохранены маленькими в углах.

Только исходным записям уклада 0 для этого изображения задано положение по координатам:

```text
base = control > 1/3 ? 3 : control <= -1/3 ? 5 : 1
display_regime = base + (guarantees < 0 ? 0 : 1)
```

Все остальные записи сохраняют содержательный `regime_primary`. Это производная классификация для графика, а не изменение основной базы.

| Уклад | Трудовые | Посттрудовые |
|---|---:|---:|


| 1 | 17 / 345 (4,9%) | 115 / 470 (24,5%) |

| 2 | 226 / 345 (65,5%) | 80 / 470 (17,0%) |

| 3 | 11 / 345 (3,2%) | 116 / 470 (24,7%) |

| 4 | 42 / 345 (12,2%) | 11 / 470 (2,3%) |

| 5 | 1 / 345 (0,3%) | 89 / 470 (18,9%) |

| 6 | 48 / 345 (13,9%) | 59 / 470 (12,6%) |


Округление до целых процентов упрощает чтение; сектор меньше 1% подписан `<1%`. Это сравнение разных обществ, а не наблюдение одного общества до и после перехода. Соседнее «почти все» исправлено на «около двух третей», поскольку доля ячейки 2 среди трудовых составляет 65,5%.

<a id="06-regime-dystopia"></a>
## 06. Дистопичность шести укладов

Во всех следующих сравнениях дистопия означает **U < 0**, включая умеренно отрицательные оценки, а не только сильную дистопию. Взяты **545** записей с исходными укладами 1–6: посттрудовые и частичные переходы. Трудовые нулевые варианты здесь не перераспределяются и не включаются.

| Уклад | Отрицательных оценок | Всего | Доля |
|---|---:|---:|---:|


| 1 | 66 | 126 | 52,4% |

| 2 | 98 | 109 | 89,9% |

| 3 | 7 | 128 | 5,5% |

| 4 | 7 | 21 | 33,3% |

| 5 | 25 | 94 | 26,6% |

| 6 | 55 | 67 | 82,1% |


На изображении сопоставляются наличие и отсутствие гарантий **внутри каждого семейства контроля**. У уклада 4 только 21 запись; это небольшой поднабор. Состав, редакторские оценки, население и период между ячейками различаются, поэтому причинный эффект гарантий не установлен. Упомянутое в другом месте статьи «вчетверо чаще» относится к иному расчёту: всем 890 обществам и порогу сильной дистопии U ≤ −0,5; смешивать эти знаменатели нельзя.

<a id="07-control-dystopia"></a>
## 07. Контроль и дистопичность

Те же 545 записей и порог U < 0. Семейства объединяют оба варианта гарантий:

| Контроль | Исходные уклады | Отрицательных оценок | Всего | Доля |
|---|---|---:|---:|---:|


| Элиты | [1, 2] | 164 | 235 | 69,8% |

| Автономные системы | [5, 6] | 80 | 161 | 49,7% |

| Общество | [3, 4] | 14 | 149 | 9,4% |


Таким образом, подставлены реальные доли около 70%, 50% и 9% вместо иллюстративных 3%, 2% и 1% из заглушки. Это частоты в выбранном каталоге; они не оценивают вероятность конкретного будущего и не доказывают преимущество передачи власти ИИ. Категория распределённого контроля включает человеческие и явно обозначенные разумные прокси; автономная система не всегда буквально биологически чужой людям интеллект.

## Воспроизведение и проверка

```powershell
& 'C:\Program Files\Python310\python.exe' scripts/build_article_infographics.py
```

Генератор создаёт 14 PNG 1600×1000 и 14 SVG, сохраняет расчёты и заменяет только семь мест изображений в `article.md` с тремя короткими согласованиями окружающего текста. Резервная копия статьи не создаётся. Русская версия видна сразу; английская встроена в раскрытие под ней. Для проверки используется HTML-превью, сгенерированное из самого Markdown, а не отдельная реконструкция содержания.

All English graphics use the same record IDs, counts, denominators, colours and geometry as their Russian counterparts. The first figure is a conservative lower-bound selection, the technology tiers are subjective illustrative ratings, and the other numerical comparisons use the original catalogue fields.

