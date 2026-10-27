"""Generate the saved Russian catalog with a local OPUS model; never upload texts.

Optional authoring tool, not a build dependency. Requires transformers,
sentencepiece and torch. Download Helsinki-NLP/opus-mt-tc-big-en-zle into
tmp/translation-models/opus-mt-tc-big-en-zle before running. Model and sentence cache
stay in ignored tmp/. Existing sentence translations are reused on restart.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import time

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
# SentencePiece on Windows needs ASCII paths; keep these relative to ROOT.
MODEL = Path("tmp/translation-models/opus-mt-tc-big-en-zle")
CACHE = ROOT / "tmp/translation-models/sentence-cache-big.json"

BASIS = {
    "Shared or freely accessible technological provision, rather than current earnings, is the central distribution model.": "Основная модель распределения — совместное или свободно доступное технологическое обеспечение, а не текущий заработок.",
    "Technological support is allocated through membership, status or institutional authority rather than primarily purchased with current wages.": "Доступ к технологическому обеспечению определяется принадлежностью к сообществу, статусом или решениями институтов, а не преимущественно покупается на текущую зарплату.",
    "An independent technical system sustains or allocates the material environment; current wages are not its primary access rule.": "Самостоятельная техническая система поддерживает материальную среду или распределяет блага; текущая зарплата не служит главным условием доступа к ним.",
    "The selected economy still primarily links material access to earnings and commercial purchases despite labor-saving technology.": "В рассматриваемой экономике доступ к материальным благам по-прежнему в основном зависит от заработка и покупок, несмотря на технологии, сокращающие потребность в труде.",
    "Automation has substantially displaced the wage channel for the selected population without establishing a secure replacement; this is a dystopian post-wage interpretation.": "Автоматизация существенно вытеснила зарплату как канал обеспечения рассматриваемого населения, не создав надёжной замены; это антиутопический вариант постзарплатного общества.",
    "Relevant automation is restrained, unavailable or deliberately limited, so the selected population has not made the technology-driven post-wage transition.": "Необходимая автоматизация сдерживается, недоступна или намеренно ограничена, поэтому рассматриваемое население не совершило технологического перехода к постзарплатному обществу.",
    "A partial technological transition plausibly makes nonwage access central for this scoped population, while important work and market dependencies remain.": "Частичный технологический переход, предположительно, делает обеспечение вне зарплаты основным для рассматриваемого населения, хотя существенная зависимость от труда и рынка сохраняется.",
    "Access to productive assets or accumulated capital is the central claim on technological output; this need not provide a universal floor.": "Главное основание для получения результатов технологического производства — доступ к производственным активам или накопленному капиталу; всеобщие базовые гарантии из этого не следуют.",
    "Continued service or productive work remains the main condition of earning access or maintenance; supporting a workforce alone does not establish a post-wage economy.": "Продолжение службы или производительного труда остаётся главным условием доступа к благам или обеспечению; само по себе содержание работников ещё не означает постзарплатную экономику.",
    "Essential labor by actual persons remains central without sufficient technological substitution; communal sharing, biological origin or robot embodiment alone does not establish the transition.": "Необходимый труд реальных личностей остаётся основой экономики без достаточной технологической замены; общинное распределение, биологическое происхождение или роботизированное тело сами по себе не означают такого перехода.",
    "The saved account does not establish a central nonwage material channel; the retained best guess is a continuing earnings-based technical economy, with low confidence.": "Сохранённое описание не подтверждает основного канала материального обеспечения вне зарплаты; рабочая гипотеза с низкой уверенностью — сохранение технологической экономики, основанной на заработке.",
}

REVIEWED_SENTENCES = {
    "Culture citizens do not need a job to obtain the things that keep them alive.": "Жителям Культуры не нужна работа, чтобы получать всё необходимое для жизни.",
    "Automated production supports comfortable lives, while people can explore, make art, study, or take on useful projects.": "Автоматизированное производство обеспечивает комфортную жизнь, а люди могут путешествовать и исследовать мир, заниматься искусством, учиться или участвовать в полезных проектах.",
    "This puts material guarantees very close to the strong end of the map.": "Поэтому на карте это общество расположено очень близко к полюсу сильных материальных гарантий.",
    "Someone choosing a demanding vocation does not lose that underlying security.": "Выбор сложного, требующего больших усилий занятия не лишает человека этой базовой защищённости.",
    "Citizens and independent Minds share political decisions, while Minds operate much of the practical infrastructure.": "Граждане и независимые Разумы совместно принимают политические решения, а значительной частью инфраструктуры управляют Разумы.",
    "The existing positive control point recognizes voting and shared social agency, with a broad alternative toward AI power; it does not mean humans own obedient Minds.": "Положительная координата контроля отражает голосование и совместное участие в управлении; широкий интервал неопределённости допускает и значительно большую власть ИИ. Это не означает, что люди владеют послушными им Разумами.",
    "The best-guess nonworking fraction is substantial because necessities require no job, but useful voluntary research, care, art and service still count as work.": "По рабочей оценке, доля неработающих велика, поскольку для получения необходимого не нужна работа. Однако полезные добровольные исследования, забота о других, искусство и услуги по-прежнему считаются трудом.",
    "The wide interval allows a much more active citizenry than a simple leisure label suggests.": "Широкий интервал допускает гораздо более высокую активность граждан, чем можно предположить, просто назвав это обществом досуга.",
    "This is an editorial scenario for biological humanlike residents, not a census or a count of all machine citizens.": "Это редакторский сценарий для биологических человекоподобных жителей, а не результат переписи и не подсчёт всех машинных граждан.",
    "An underground resident can summon food, clothing, a bed, medical attention, and remote conversation without earning a wage for each service.": "Житель подземного поселения может получить еду, одежду, кровать, медицинскую помощь и дистанционное общение, не зарабатывая на каждую из этих услуг.",
    "The Machine has taken over the material routines of living.": "Машина взяла на себя повседневное материальное обеспечение жизни.",
    "That supports a strong provision score, but the safety net has a brutal condition: dissent can bring expulsion from the system, treated by its residents as a death sentence.": "Это позволяет высоко оценить уровень обеспечения, но у системы есть жестокое условие: за инакомыслие могут изгнать, а жители воспринимают изгнание как смертный приговор.",
    "The score therefore stops well short of an unconditional guarantee.": "Поэтому оценка остаётся значительно ниже уровня безусловных гарантий.",
    "Human committees and attendants remain part of the order, so technical dependence alone does not prove a conscious AI sovereign.": "В этом устройстве общества сохраняются человеческие комитеты и обслуживающий персонал, поэтому сама техническая зависимость не доказывает, что верховная власть принадлежит сознательному ИИ.",
    "The best-guess nonworking fraction is moderately high because provision requires little ordinary production labor, with a broad allowance for useful lectures, care, maintenance and administration.": "Рабочая оценка доли неработающих умеренно высока: обеспечение требует мало обычного производственного труда. При этом широкий интервал учитывает полезные лекции, заботу о других, обслуживание и управление.",
    "Intellectual activity can still be work when it contributes to others.": "Интеллектуальная деятельность тоже может быть трудом, если приносит пользу другим.",
    "The fraction is not inferred from time spent physically motionless in a room.": "Эта доля не выводится из того, сколько времени человек проводит неподвижно в комнате.",
    "These estimates describe living residents before collapse; later deaths and broken machinery cannot supply a population of perfectly leisured people.": "Оценки относятся к живым жителям до краха системы. Последующие смерти и поломки нельзя трактовать как появление населения, полностью свободного от труда.",
    "Coercive exclusion remains a limit on the material floor.": "Угроза принудительного исключения ограничивает базовые материальные гарантии.",
    "Earth Two's settlers receive manufactured goods, medical help and robot teaching without having to earn money.": "Поселенцы Земли-2 получают промышленные товары и медицинскую помощь, а роботы обучают их; зарабатывать деньги для этого не требуется.",
    "This is an explicit interpretation of one active child, with a full zero-to-one interval for the alternative that she has no sustained work role.": "Это явно обозначенная интерпретация для одного деятельного ребёнка; интервал охватывает весь диапазон от нуля до единицы, допуская и вариант, при котором у неё нет постоянной трудовой роли.",
    "Humanity in 17776 has overcome ordinary social deprivation and deploys microtechnology that protects people from injury.": "Человечество в «17776» преодолело обычную социальную нужду и использует микротехнологии, защищающие людей от травм.",
    "The central estimate gives that machine dependency some weight without claiming an independent AI owns the entire economy.": "Центральная оценка учитывает зависимость от машин, но не предполагает, что независимый ИИ владеет всей экономикой.",
    "The later revolt and final original human are separate phases from the opening economy.": "Последующее восстание и этап, на котором остаётся последний исходный человек, рассматриваются отдельно от экономики в начале произведения.",
    "No verified universal food entitlement is inferred from virtual access, and no claim is made that every warehouse task is already automated.": "Доступ к виртуальной среде не считается доказательством всеобщего права на питание; также не утверждается, что все складские операции уже автоматизированы.",
    "Exposure of the experiments changes care possibilities, but it does not establish an already settled universal economy or give later New New York the same coordinates.": "Раскрытие экспериментов меняет возможности оказания помощи, но не доказывает существования уже сложившейся всеобщей системы обеспечения и не позволяет приписать позднейшему Новому Нью-Йорку те же координаты.",
    "Other endings are not averaged into the point, and inactive files or available new bodies do not multiply the active person population.": "Другие концовки не усредняются в этой точке, а неактивные файлы и доступные новые тела не увеличивают число действующих личностей.",
    "Following the article’s second regime, this record now assesses that whole exclusionary institution rather than only its born-human beneficiaries.": "В соответствии со вторым укладом статьи эта запись оценивает весь институт, построенный на исключении части личностей, а не только его получателей благ, родившихся людьми.",
    "Weak access follows the monopoly and punishments rather than an assumption that everyone outside the ruling class receives nothing at all.": "Низкая оценка доступа связана с монополией и наказаниями, а не с предположением, что все, кто не принадлежит к правящему классу, вообще ничего не получают.",
    "The central nonworking scenario is zero for the active service cohort because it is defined by recurring assigned duties; the broad interval allows exceptions without turning idle processing cycles into a leisure count.": "Центральная оценка доли неработающих среди действующего обслуживающего персонала равна нулю, поскольку эта группа определяется регулярным выполнением назначенных обязанностей. Широкий интервал допускает исключения, но не превращает простаивающие вычислительные циклы в показатель досуга.",
    "Workers must pay for the oxygen keeping them alive while a corporate algorithm treats their continued employment as a cost calculation.": "Работники должны платить за кислород, поддерживающий их жизнь, а корпоративный алгоритм решает, продолжать ли их трудоустройство, исходя из расчёта затрат.",
    "A moderate nonworking estimate allows relief from forced extraction while retaining useful rebuilding, engineering, care-like repair and civic organization.": "Умеренная оценка доли неработающих допускает освобождение от принудительной добычи ресурсов, но учитывает полезный труд по восстановлению, инженерной работе, ремонту как форме заботы и гражданской организации.",
    "The Glitch repeat medieval social and agrarian roles after a fault in their simulation-development system.": "Из-за сбоя в системе моделирования развития глитчи воспроизводят средневековые общественные и сельскохозяйственные роли.",
    "The employer’s deliberate attempt to sacrifice its crew makes their material security weak even though ordinary station life provides support.": "Намеренная попытка работодателя пожертвовать экипажем означает слабую материальную защищённость людей, хотя обычная жизнь на станции и предполагает обеспечение их потребностей.",
    "The Australia Project pools resources through a corporation whose members receive equal access to its output.": "Австралийский проект объединяет ресурсы через корпорацию, участники которой получают равный доступ к результатам её производства.",
    "Weekly resource credits come with membership, while robots provide everyday goods and services.": "Участие в проекте даёт право на еженедельные ресурсные кредиты, а повседневные товары и услуги обеспечивают роботы.",
    "A resident does not need to accept a job to secure food or a home.": "Жителю не нужно устраиваться на работу, чтобы обеспечить себя едой и жильём.",
    "Those arrangements place guarantees near the strong end and control toward broad participation, although the promise is for Project members rather than everyone on Earth.": "Такое устройство приближает общество к полюсу сильных гарантий и широкого участия в управлении, хотя эти права распространяются на участников проекта, а не на всех жителей Земли.",
    "Member participation gives the project a strong shared-control interpretation, while access remains bounded to membership and available resources.": "Участие членов проекта позволяет говорить о высокой степени совместного управления, но доступ к благам ограничен членством и имеющимися ресурсами.",
    "The best-guess nonworking fraction is substantial but leaves considerable room for useful self-directed projects, care, research and administration.": "Рабочая оценка доли неработающих велика, но оставляет значительное место полезным самостоятельным проектам, заботе о других, исследованиям и управлению.",
    "Resource credits are not a labor census, and choosing an activity freely does not make its output useless.": "Ресурсные кредиты не дают статистики занятости, а свободный выбор деятельности не делает её результаты бесполезными.",
    "The broad interval is an editorial scenario across members and dependents.": "Широкий интервал — это редакторский сценарий для участников проекта и тех, кто находится на их обеспечении.",
    "It does not give identical protection to nonmembers elsewhere, equate every pleasurable activity with productive employment, or pretend that robots have eliminated every scarce resource.": "Он не предполагает такой же защищённости у людей вне проекта, не приравнивает любое приятное занятие к производительному труду и не утверждает, что роботы устранили дефицит всех ресурсов.",
    "The project’s material entitlement and actual participation remain separate judgments.": "Право на материальное обеспечение в проекте и фактическое участие в труде оцениваются отдельно.",
    "On twenty-fourth-century Earth, the familiar link between earning money and meeting material needs has largely disappeared.": "На Земле XXIV века привычная связь между денежным заработком и удовлетворением материальных потребностей в значительной мере исчезла.",
    "Replicators and supporting infrastructure make everyday goods readily available, and choosing a vocation is presented as a matter of interest and contribution.": "Репликаторы и обслуживающая их инфраструктура делают повседневные блага доступными, а выбор занятия представлен как вопрос личного интереса и желания приносить пользу.",
    "The strong guarantee score describes this ordinary civilian baseline.": "Высокая оценка гарантий относится к этим обычным условиям гражданской жизни.",
    "It is not a claim that every frontier settlement or wartime starship enjoys the same conditions.": "Из неё не следует, что такие же условия есть в каждом пограничном поселении или на каждом звездолёте во время войны.",
    "Shared civilian institutions keep productive control toward the distributed human end, while Starfleet’s chain of command does not describe all of Earth.": "Общие гражданские институты приближают контроль над производством к полюсу распределённого человеческого управления; командная иерархия Звёздного флота не описывает устройство всей Земли.",
    "For participation, the best guess is that about half the scoped population does no ongoing useful work.": "Рабочая оценка участия предполагает, что около половины рассматриваемого населения не выполняет регулярной полезной работы.",
    "The interval is deliberately wide because many residents may choose demanding vocations, research, care or creative contribution even when necessities are free.": "Интервал намеренно широк: даже при бесплатном обеспечении необходимого многие жители могут выбирать сложные занятия, исследования, заботу о других или творчество.",
    "Those activities still count as work.": "Такая деятельность по-прежнему считается трудом.",
    "This is an editorial population scenario, not a quoted Federation unemployment rate, and frontier shortages do not erase the ordinary Earth baseline.": "Это редакторский сценарий для населения, а не взятый из канона уровень безработицы Федерации. Дефицит на периферии не отменяет обычных условий жизни на Земле.",
    "Zion survives through machinery providing air, heat, light and recycled water.": "Зион существует благодаря машинам, обеспечивающим воздух, тепло, свет и переработку воды.",
    "Hamann’s engineering-level discussion makes that dependence concrete, even though the films do not explain every household allocation rule.": "Разговор Хаманна об инженерных системах наглядно показывает эту зависимость, хотя фильмы не объясняют все правила распределения благ между домохозяйствами.",
    "The best-guess reading is a technically supported communal refuge with a modest shared floor.": "Рабочая интерпретация — общинное убежище, которое опирается на технику и обеспечивает скромный общий уровень базовых гарантий.",
    "Material security remains fragile because maintenance, restricted resources and the approaching war can interrupt it.": "Материальная защищённость остаётся хрупкой: необходимость обслуживания, ограниченность ресурсов и приближающаяся война могут нарушить обеспечение.",
    "The city is a partial automation case, with plenty of real human work still necessary.": "Город представляет собой случай частичной автоматизации, при которой по-прежнему необходим большой объём реального человеческого труда.",
    "Human council members and engineers direct the machines, so dependence on technical systems does not mean autonomous AI rule.": "Машинами управляют люди — члены совета и инженеры, поэтому зависимость от технических систем не означает власть автономного ИИ.",
    "Control is estimated toward shared civic authority while allowing a strong council and military hierarchy.": "Оценка контроля смещена к совместному гражданскому управлению, но допускает сильную власть совета и военную иерархию.",
    "The relatively low nonworking estimate includes children and other dependents, but counts defense, repair, care and useful provisioning as work.": "Относительно низкая оценка доли неработающих учитывает детей и других иждивенцев, но относит оборону, ремонт, заботу о других и полезное обеспечение к труду.",
    "Dance and celebrations do not establish universal leisure.": "Танцы и праздники не доказывают всеобщей свободы от труда.",
    "The score is a broad editorial assessment, not an invented Zion employment register.": "Это приблизительная редакторская оценка, а не вымышленный реестр занятости Зиона.",
    "Broad bounds preserve the limited source’s household detail without reading a post-employment constitution into the title or requiring a whole-story reconstruction before saving a clearly qualified estimate.": "Широкие границы отражают скудность сведений источника о повседневной экономике: название произведения не трактуется как доказательство посттрудового устройства, а для сохранения оценки с явными оговорками не требуется реконструировать весь рассказ.",
}


def polish_translation(text):
    # In this population dataset, resident means an inhabitant, not a tax resident.
    inhabitants = {"резидент": "житель", "резидента": "жителя", "резиденту": "жителю", "резидентом": "жителем", "резиденте": "жителе", "резиденты": "жители", "резидентов": "жителей", "резидентам": "жителям", "резидентами": "жителями", "резидентах": "жителях"}
    def replace(match):
        word = match.group()
        result = inhabitants[word.lower()]
        return result.capitalize() if word[0].isupper() else result
    return re.sub(r"\b(?:" + "|".join(inhabitants) + r")\b", replace, text, flags=re.I)


def save_json(file, value):
    file.parent.mkdir(parents=True, exist_ok=True)
    temporary = file.with_suffix(file.suffix + ".pending")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(file)


def source_hash(record):
    source = json.dumps([record["description"], record["post_work_assessment"]["basis"]], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def normalize_source(text):
    # Make the research vocabulary unambiguous for the general-purpose model.
    text = re.sub(r"\b(?:material[- ]|basic )?floor\b", "guarantee of basic necessities", text)
    return (text.replace("control best guess", "estimated control value")
                .replace("control point", "control coordinate")
                .replace("best-guess reading", "estimated interpretation")
                .replace("distributed human end", "end of the axis representing distributed human control")
                .replace("best-guess nonworking fraction", "estimated share of residents who do not work")
                .replace("nonworking fraction", "share of residents who do not work")
                .replace("nonworking scenario", "scenario for the share of residents who do not work")
                .replace("nonworking estimate", "estimate of the share of residents who do not work")
                .replace("nonworking point", "estimated share of residents who do not work")
                .replace("best-guess", "estimated")
                .replace("best guess", "estimate")
                .replace("material-floor", "basic material guarantee")
                .replace("material floor", "basic material guarantee")
                .replace("nonworking", "non-working"))


def main():
    import torch
    from transformers import MarianMTModel, MarianTokenizer

    records = json.loads((ROOT / "data/societies.json").read_text(encoding="utf-8"))["societies"]
    assert all(r["post_work_assessment"]["basis"] in BASIS for r in records), "New economy basis needs a Russian translation"
    tokenizer = MarianTokenizer.from_pretrained(str(MODEL), local_files_only=True)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    translator = MarianMTModel.from_pretrained(str(MODEL), local_files_only=True, dtype=torch.float16 if device == "cuda" else torch.float32).to(device).eval()
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    cache = {key: value for key, value in cache.items() if key.startswith(">>rus<< ")}
    cache_key = lambda text: ">>rus<< " + normalize_source(text)

    def split_paragraph(paragraph):
        sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\u2018])", paragraph.strip())
        # Translate each sentence separately: general NMT models can omit later
        # sentences when handed whole paragraphs, even below their token limit.
        for chunk in sentences:
            assert len(tokenizer.tokenize(normalize_source(chunk))) < 510, "Oversize translation chunk"
        return sentences

    chunks_by_id = {}
    for record in records:
        # Translate the repeated taxonomy conclusion consistently and by hand.
        body = record["description"].split(" Article-aligned classification:")[0]
        chunks_by_id[record["id"]] = [split_paragraph(p) for p in body.split("\n") if p.strip()]
    pending = list(dict.fromkeys(chunk for paragraphs in chunks_by_id.values() for paragraph in paragraphs for chunk in paragraph if chunk not in REVIEWED_SENTENCES and cache_key(chunk) not in cache))
    print(f"{len(records)} records, {len(pending)} uncached chunks; local device: {device}", flush=True)
    started = time.monotonic()
    for offset in range(0, len(pending), 48):
        batch = pending[offset:offset + 48]
        inputs = tokenizer([cache_key(text) for text in batch], return_tensors="pt", padding=True).to(device)
        with torch.inference_mode():
            results = translator.generate(**inputs, num_beams=4, max_new_tokens=510, repetition_penalty=1.05)
        for source, translated in zip(batch, tokenizer.batch_decode(results, skip_special_tokens=True)):
            if not re.search(r"[А-Яа-яЁё]", translated):
                raise RuntimeError(f"No Russian translation: {source[:80]}")
            cache[cache_key(source)] = translated
        save_json(CACHE, cache)
        completed = min(offset + len(batch), len(pending))
        print(f"Translated {completed}/{len(pending)} chunks in {time.monotonic() - started:.0f}s", flush=True)

    translations = {}
    for record in records:
        paragraphs = [" ".join(polish_translation(REVIEWED_SENTENCES.get(chunk) or cache[cache_key(chunk)]) for chunk in paragraph) for paragraph in chunks_by_id[record["id"]]]
        basis = BASIS[record["post_work_assessment"]["basis"]]
        if " Article-aligned classification:" in record["description"]:
            paragraphs[-1] += " Классификация по статье: " + basis + " Полезная деятельность и доля неработающих оцениваются отдельно."
        translations[record["id"]] = {"source_sha256": source_hash(record), "description": "\n\n".join(paragraphs), "economy_basis": basis}
    save_json(ROOT / "data/society-translations.ru.json", {
        "language": "ru", "source": "data/societies.json",
        "method": "Local neural machine translation with Helsinki-NLP/opus-mt-tc-big-en-zle; editorial terminology, taxonomy conclusions and selected descriptions reviewed separately.",
        "model": "https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-zle",
        "model_license": "CC-BY-4.0",
        "attribution": "OPUS-MT, Helsinki-NLP; Tiedemann and Thottingal (2020), https://aclanthology.org/2020.eamt-1.61/",
        "translations": translations,
    })
    print(f"Saved {len(translations)} Russian descriptions", flush=True)


if __name__ == "__main__":
    main()
