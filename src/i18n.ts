import type { Lang, SocietyStatus } from './types';
export const copy = {
  ru: {
    brand: 'Посттрудовые общества', societies: 'Общества', article: 'Статья', table: 'Таблица',
    title: 'Посттрудовые общества', subtitle: 'Автоматизация, гарантии обеспечения и контроль над ИИ.',
    all: 'Все', books: 'Книги', movies: 'Фильмы', tv: 'Сериалы', anime: 'Аниме', games: 'Игры', comics: 'Комиксы', other: 'Другое',
    postWorkSociety: 'Посттрудовое общество', allSocieties: 'Все общества', societyType: 'Тип общества',
    economyDetails: 'Об устройстве экономики', wageAccess: 'Зависимость от заработка', allocation: 'Как распределяются блага',
    noReplacement: 'Без устойчивого обеспечения: трудовой доход вытеснен, надёжная замена не установилась.',
    statusKey: 'Круг — посттрудовое общество; пятиугольник — переходное или трудовое.',
    shapePostWork: 'Посттрудовые', shapeOther: 'Трудовые / переходные',
    workingPopulation: 'Доля работающих', workingPopulationHint: 'Доля выбранного населения, участвующего в работе, включая неоплачиваемую деятельность.',
    relatedSocieties: 'Связанные общества', insecureProvision: 'Без устойчивого обеспечения',
    noMatches: 'Нет обществ с выбранными фильтрами. Измените тип общества, формат или поиск.',
    search: 'Найти общество или произведение', searchShort: 'Поиск…', shown: 'на карте', names: 'Названия',
    shared: 'Общество', elite: 'Элиты', ai: 'Автономный ИИ', guarantees: 'Широкие гарантии', noGuarantees: 'Гарантии отсутствуют',
    dystopia: 'Дистопия', utopia: 'Утопия', works: 'Работают', nonworking: 'Не работают', size: 'Размер — популярность произведения',
    hint: 'Наведите на общество, чтобы открыть карточку. Нажмите, чтобы закрепить её.',
    mapTools: 'Управление картой', screenshot: 'Сохранить координаты (PNG)', exportError: 'Не удалось сохранить PNG. Повторите попытку.',
    reset: 'Сбросить масштаб', zoomIn: 'Приблизить', zoomOut: 'Отдалить', full: 'Режим чтения', read: 'Статья',
    articleTitle: 'Посттрудовые общества', articleDesc: 'Когда труд перестаёт быть основным способом распределения благ.',
    contents: 'Содержание', intro: 'Посттрудовое и постзарплатное общество', conclusion: 'Будущее левых и правых',
    tableTitle: 'Таблица обществ', tableSub: 'Показаны те же общества, что и на карте. Поиск и фильтры общие.',
    work: 'Произведение / общество', media: 'Формат', guaranteeAxis: 'Гарантии', controlAxis: 'Контроль ИИ', regime: 'Уклад', welfare: 'Утопичность', popularity: 'Популярность',
    empty: 'Форматы не выбраны', emptySub: 'Выберите формат или нажмите «Все».', noResults: 'Ничего не найдено', clear: 'Сбросить поиск',
    estimates: 'Показатели — редакторские оценки по описаниям обществ, а не каноническая статистика.', legacy: 'Нулевой вариант обозначает общество без подтверждённого постзарплатного перехода. Доля работающих — отдельный показатель.',
    enData: 'Описания обществ в базе — на английском.', details: 'Все данные записи', sources: 'Источники', scope: 'Контекст и границы', uncertainty: 'Оговорки',
    societyLabel: 'Общество', workSeries: 'Произведение / серия', societiesInSeries: 'Общества этого произведения / серии', currentSociety: 'Открыто сейчас', hiddenByFilters: 'Скрыто фильтрами', singleSociety: 'В базе описано одно общество этого произведения.', relatedOnMap: 'обществ на карте',
    relatedMapHint: 'Выберите общество, чтобы открыть его на карте. Если оно скрыто, фильтры будут сброшены.', relatedTableHint: 'Выберите общество, чтобы открыть его карточку. В списке также есть общества, скрытые текущими фильтрами.',
    score: 'Благополучие', editorial: 'Редакторская оценка', nearby: 'обществ рядом', close: 'Закрыть', loading: 'Загрузка данных…', retry: 'Повторить', error: 'Не удалось загрузить данные.',
    download: 'Скачать CSV', prev: 'Назад', next: 'Далее', of: 'из', methodology: 'Обозначения и шкалы',
    methodologyText: 'По горизонтали — гарантии доступа к благам: широкие слева, отсутствуют справа. По вертикали — кто контролирует ИИ: общество сверху, элиты в центре, автономный ИИ снизу. Размер иконки зависит от популярности произведения, цвет — от утопичности общества; предельный цвет достигается при ±0,7. Круг — посттрудовое общество, пятиугольник — переходное или трудовое. Каждое общество показано отдельно. Иконки раздвинуты для читаемости без изменения исходных данных.',
    scales: 'Шкалы 0–100: гарантии — от отсутствующих до широких; контроль — автономный ИИ (0), элиты (50), общество (100); утопичность — от дистопии до утопии. Это условные баллы, не проценты.',
    light: 'Светлая тема', dark: 'Тёмная тема', back: 'К карте', translation: 'Английская версия статьи пока не добавлена.', translationSub: 'Карта, таблица и описания обществ доступны на английском. Для чтения статьи переключите язык на русский.',
  },
  en: {
    brand: 'Post-work societies', societies: 'Societies', article: 'Article', table: 'Table',
    title: 'Post-work societies', subtitle: 'Automation, material guarantees and control over AI.',
    all: 'All', books: 'Books', movies: 'Films', tv: 'TV', anime: 'Anime', games: 'Games', comics: 'Comics', other: 'Other',
    postWorkSociety: 'Post-work society', allSocieties: 'All societies', societyType: 'Society type',
    economyDetails: 'How the economy works', wageAccess: 'Dependence on earnings', allocation: 'How goods are allocated',
    noReplacement: 'No secure provision: earnings have been displaced without an established reliable replacement.',
    statusKey: 'Circle: post-work society. Pentagon: transitional or work-based society.',
    shapePostWork: 'Post-work', shapeOther: 'Work-based / transitional',
    workingPopulation: 'Population working', workingPopulationHint: 'Share of the selected population participating in work, including unpaid activity.',
    relatedSocieties: 'Related societies', insecureProvision: 'No secure provision',
    noMatches: 'No societies match these filters. Change the society type, medium or search.',
    search: 'Find a society or work', searchShort: 'Search…', shown: 'on the map', names: 'Labels',
    shared: 'Society', elite: 'Elites', ai: 'Autonomous AI', guarantees: 'Broad guarantees', noGuarantees: 'No guarantees',
    dystopia: 'Dystopia', utopia: 'Utopia', works: 'Working', nonworking: 'Not working', size: 'Size — popularity of the work',
    hint: 'Hover a society to open its card. Click to pin it.',
    mapTools: 'Map controls', screenshot: 'Save map (PNG)', exportError: 'Could not save the PNG. Please try again.',
    reset: 'Reset view', zoomIn: 'Zoom in', zoomOut: 'Zoom out', full: 'Reading mode', read: 'Article',
    articleTitle: 'Post-work societies', articleDesc: 'When work stops being the main way to distribute material goods.',
    contents: 'Contents', intro: 'Post-work and post-wage societies', conclusion: 'The future of left and right',
    tableTitle: 'Society table', tableSub: 'The same societies as on the map. Search and filters are shared.',
    work: 'Work / society', media: 'Medium', guaranteeAxis: 'Guarantees', controlAxis: 'AI control', regime: 'Regime', welfare: 'Utopian character', popularity: 'Popularity',
    empty: 'No media selected', emptySub: 'Select a medium or choose All.', noResults: 'No results found', clear: 'Clear search',
    estimates: 'Values are editorial estimates from descriptions of the societies, not canonical statistics.', legacy: 'Zero variants have no confirmed post-wage transition. Participation in work is a separate measure.',
    enData: 'Society descriptions are in the original English.', details: 'Full record', sources: 'Sources', scope: 'Scope and boundaries', uncertainty: 'Uncertainties',
    societyLabel: 'Society', workSeries: 'Work / series', societiesInSeries: 'Societies in this work / series', currentSociety: 'Currently open', hiddenByFilters: 'Hidden by filters', singleSociety: 'One society from this work is described in the database.', relatedOnMap: 'societies on the map',
    relatedMapHint: 'Choose a society to open it on the map. If it is hidden, the filters will be reset.', relatedTableHint: 'Choose a society to open its card. The list also includes societies hidden by the current filters.',
    score: 'Well-being', editorial: 'Editorial estimate', nearby: 'societies nearby', close: 'Close', loading: 'Loading data…', retry: 'Retry', error: 'Could not load the data.',
    download: 'Download CSV', prev: 'Previous', next: 'Next', of: 'of', methodology: 'Key and scales',
    methodologyText: 'Horizontal: guarantees of material provision, broad on the left and absent on the right. Vertical: who controls AI, society at the top, elites in the centre, autonomous AI at the bottom. Icon size reflects the popularity of the work; colour reflects the society’s utopian character, reaching full saturation at ±0.7. Circles indicate post-work societies; pentagons indicate transitional or work-based societies. Every society is separate. Icons are displaced for readability without changing the underlying data.',
    scales: '0–100 scales: guarantees range from absent to broad; control runs from autonomous AI (0), through elites (50), to society (100); utopian character runs from dystopia to utopia. Scores are not percentages.',
    light: 'Light theme', dark: 'Dark theme', back: 'Back to map', translation: 'The English article has not been added yet.', translationSub: 'The map, table and society descriptions are available in English. Switch to Russian to read the article.',
  },
};
export const societyTypes: Record<Lang, Record<SocietyStatus, string>> = {
  ru: { post_work: 'Посттрудовое общество', transition: 'Переходное общество', zero_variant: 'Трудовое общество' },
  en: { post_work: 'Post-work society', transition: 'Transitional society', zero_variant: 'Work-based society' },
};
export const societyFilterOptions: Record<Lang, Record<SocietyStatus, string>> = {
  ru: { post_work: 'Посттрудовые', transition: 'Переходные', zero_variant: 'Трудовые' },
  en: { post_work: 'Post-work', transition: 'Transitional', zero_variant: 'Work-based' },
};
export const societyTypeDescriptions: Record<Lang, Record<SocietyStatus, string>> = {
  ru: {
    post_work: 'Из-за автоматизации труд перестал быть основным способом распределения благ. Это само по себе не означает надёжного обеспечения.',
    transition: 'Автоматизация делает незарплатный доступ значимым, но сохраняются существенные трудовые и рыночные зависимости.',
    zero_variant: 'В этой классификации посттрудовой переход не установлен: сохраняется зависимость от заработка, необходимого труда или недостаточно автоматизации. Наличие зарплат не обязательно.',
  },
  en: {
    post_work: 'Automation has displaced work as the main way to distribute goods. Secure provision does not necessarily follow.',
    transition: 'Automation makes non-wage access significant, while important work and market dependencies remain.',
    zero_variant: 'This classification does not establish a post-work transition: dependence on earnings or essential labour remains, or automation is insufficient. Wages need not exist.',
  },
};
export const wageLabels: Record<Lang, Record<string, string>> = {
  ru: { secondary: 'Заработок второстепенен', primary: 'Заработок — основной способ доступа', mixed_transition: 'Смешанная, переходная экономика', structurally_displaced_without_replacement: 'Трудовой доход вытеснен без надёжной замены', work_conditioned: 'Доступ обусловлен работой', not_replaced_by_automation: 'Необходимый труд не заменён автоматизацией', retained_or_not_replaced: 'Трудовая зависимость сохраняется', uncertain_primary_best_guess: 'Предположительно зависит от заработка; данных недостаточно' },
  en: { secondary: 'Earnings are secondary', primary: 'Earnings are the main route to provision', mixed_transition: 'Mixed, transitional economy', structurally_displaced_without_replacement: 'Earnings displaced without a secure replacement', work_conditioned: 'Access is conditional on work', not_replaced_by_automation: 'Essential labour has not been replaced by automation', retained_or_not_replaced: 'Dependence on work remains', uncertain_primary_best_guess: 'Probably earnings-based; evidence is limited' },
};
export const allocationLabels: Record<Lang, Record<string, string>> = {
  ru: { commons: 'Общее распределение или свободный доступ', status_or_institutional_allocation: 'Через статус, членство или институты', productive_assets_or_capital: 'Через собственные производящие активы или капитал', autonomous_system_allocation: 'Решением автономной системы', exclusion_or_informal_survival: 'Исключение из распределения или неформальное выживание', mixed_nonwage_transition: 'Сочетание трудового и незарплатного доступа', wages_and_commercial_access: 'Заработок и коммерческие покупки', work_conditioned_earning_or_maintenance: 'Доход или содержание в обмен на работу', restraint_or_restricted_automation: 'Ограниченная или сдерживаемая автоматизация', essential_person_labor: 'Необходимый труд разумных личностей', uncertain_earnings_based_access: 'Предположительно заработок; данных недостаточно' },
  en: { commons: 'Shared distribution or free access', status_or_institutional_allocation: 'Status, membership or institutions', productive_assets_or_capital: 'Productive assets or capital', autonomous_system_allocation: 'Allocation by an autonomous system', exclusion_or_informal_survival: 'Exclusion or informal survival', mixed_nonwage_transition: 'Mixed work-based and non-wage access', wages_and_commercial_access: 'Earnings and commercial purchases', work_conditioned_earning_or_maintenance: 'Earnings or maintenance in exchange for work', restraint_or_restricted_automation: 'Limited or restrained automation', essential_person_labor: 'Essential labour by sentient persons', uncertain_earnings_based_access: 'Probably earnings-based; evidence is limited' },
};
export const regimes: Record<Lang, string[]> = {
  ru: ['Нулевой вариант', 'Монополия элит на ИИ + гарантии', 'Монополия элит на ИИ без гарантий', 'Обобществлённый ИИ + гарантии', 'Распределённый ИИ без гарантий', 'Автономный ИИ + гарантии', 'Автономный ИИ без гарантий'],
  en: ['Zero variant', 'Elite monopoly on AI + guarantees', 'Elite monopoly on AI, no guarantees', 'Socialised AI + guarantees', 'Distributed AI, no guarantees', 'Autonomous AI + guarantees', 'Autonomous AI, no guarantees'],
};
export const levels: Record<Lang, { guarantees: string[]; control: string[]; welfare: string[] }> = {
  ru: { guarantees: ['Отсутствуют', 'Слабые', 'Частичные', 'Умеренные', 'Широкие'], control: ['Автономный ИИ', 'ИИ и элиты', 'Элиты', 'Элиты и общество', 'Общество'], welfare: ['Крайне дистопичное', 'Дистопичное', 'Скорее дистопичное', 'Смешанное', 'Скорее утопичное', 'Утопичное', 'Крайне утопичное'] },
  en: { guarantees: ['Absent', 'Weak', 'Partial', 'Moderate', 'Broad'], control: ['Autonomous AI', 'AI and elites', 'Elites', 'Elites and society', 'Society'], welfare: ['Extremely dystopian', 'Dystopian', 'Mostly dystopian', 'Mixed', 'Mostly utopian', 'Utopian', 'Extremely utopian'] },
};
export const medium: Record<Lang, Record<string, string>> = {
  ru: { book: 'Книга', short_story: 'Рассказ', web_fiction: 'Веб-проза', movie: 'Фильм', tv: 'Сериал', anime: 'Аниме', game: 'Игра', tabletop: 'Настольная игра', comic: 'Комикс', manga: 'Манга', webcomic: 'Веб-комикс', cartoon: 'Анимация', play: 'Пьеса', audio: 'Аудио' },
  en: { book: 'Book', short_story: 'Short story', web_fiction: 'Web fiction', movie: 'Film', tv: 'TV', anime: 'Anime', game: 'Game', tabletop: 'Tabletop', comic: 'Comic', manga: 'Manga', webcomic: 'Webcomic', cartoon: 'Animation', play: 'Play', audio: 'Audio' },
};
