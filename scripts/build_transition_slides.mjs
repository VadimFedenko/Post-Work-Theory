import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
process.on('uncaughtException',error=>{console.error(error.name+': '+error.message);console.error((error.stack??'').split('\n').filter(x=>x.includes('build_transition_slides')).join('\n'));process.exit(1);});

const ROOT=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SKILL='C:/Users/Vadim/.codex/plugins/cache/openai-primary-runtime/presentations/26.1020.11127/skills/presentations';
const RUNTIME_MODULES='C:/Users/Vadim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=RUNTIME_MODULES;
const RUNTIME_PYTHON='C:/Users/Vadim/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const {Presentation,PresentationFile,FileBlob}=await import(pathToFileURL(path.join(RUNTIME_MODULES,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const OUT=path.join(ROOT,'research/exploratory-analysis/presentation');
const BUILD=path.join(ROOT,'research/exploratory-analysis/.transition-slides-build');
await fs.mkdir(OUT,{recursive:true});await fs.mkdir(BUILD,{recursive:true});
const DATA=JSON.parse(await fs.readFile(path.join(ROOT,'research/exploratory-analysis/transition-analysis.json'),'utf8'));
const RAW=JSON.parse(await fs.readFile(path.join(ROOT,'data/societies.json'),'utf8')).societies;
const ST=DATA.stage_order;
const FONT='Arial';
const INK='#223A40',MUTED='#60747A',BG='#FFFFFF';
const STCOLOR=['#7B8896','#D69C46','#277F75'];
const REGCOLOR=['#D69C46','#AD654D','#277F75','#5C9D85','#6874B5','#9C5D91'];
const REGLABEL=['1  Элиты с гарантиями','2  Элиты без гарантий','3  Распределённая власть с гарантиями','4  Распределённые активы без гарантий','5  Автономная система с гарантиями','6  Автономная система без гарантий'];
const SHORT=['Трудовые','Частичный переход','Посттрудовые'];
const CAT=['Трудовые, n = 345','Частичный переход, n = 75','Посттрудовые, n = 470'];
const pct=(x,d=1)=>(100*x).toFixed(d).replace('.',',')+'%';
const num=(x,d=2)=>(x>0?'+':'')+x.toFixed(d).replace('.',',');
const src='Источник: data/societies.json, 890 обществ. Редакторские оценки на 22.10.2026.';
const prs=Presentation.create({slideSize:{width:1600,height:900}});

function text(s,t,x,y,w,h,size=26,color=INK,bold=false,alignment='left'){
  const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});
  sh.text=t;sh.text.style={typeface:FONT,fontSize:size,bold,color,alignment,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:0};return sh;
}
function slide(title,subtitle,notes=''){
  const s=prs.slides.add();s.background.fill=BG;
  text(s,title,65,43,1470,70,44,INK,true);
  if(subtitle)text(s,subtitle,65,122,1470,72,25,MUTED);
  text(s,src,65,851,1400,30,17,MUTED);
  text(s,String(prs.slides.items.length),1485,850,50,30,18,MUTED,false,'right');
  s.speakerNotes.text=src+'\nDerived data: research/exploratory-analysis/transition-analysis.json\n'+notes;
  return s;
}
function chart(s,type,opts){
  // Excel's embedded workbooks retain up to 15 significant digits. Ten decimal
  // places preserve these chart proportions far beyond their display precision.
  if(opts.series)opts={...opts,series:opts.series.map(v=>({...v,values:v.values?.map(x=>typeof x==='number'?Math.round(x*1e10)/1e10:x),
    ...(v.dataLabels?{dataLabels:{...v.dataLabels,textStyle:{...(v.dataLabels.textStyle??{}),typeface:FONT}}}:{}),
    ...(v.dataLabelOverrides?{dataLabelOverrides:v.dataLabelOverrides.map(o=>({...o,textStyle:{...(opts.dataLabels?.textStyle??{}),...(v.dataLabels?.textStyle??{}),...(o.textStyle??{}),typeface:FONT}}))}:{})}))};
  const c=s.charts.add(type,{chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',chartLine:{style:'solid',fill:'none',width:0},plotAreaLine:{style:'solid',fill:'none',width:0},titlePlacement:'none',...opts});
  applyPresentationChartFont(c,{fontFamily:FONT});return c;
}
function axes(min=0,max=1,format='0%'){
  return {xAxis:{tickLabelPosition:'low',textStyle:{fontSize:23,fill:INK},line:{style:'solid',fill:'none',width:0}},
    yAxis:{min,max,majorUnit:max-min<=2?.2:20,numberFormatCode:format,textStyle:{fontSize:21,fill:MUTED},majorGridlines:{style:'solid',fill:'#DEE6E7',width:1},line:{style:'solid',fill:'none',width:0}}};
}
function bar(s,{x=65,y=225,w=1470,h=480,categories,series,max=1,min=0,format='0%',grouping='clustered',legend=true,labels=true}){
  return chart(s,'bar',{position:{left:x,top:y,width:w,height:h},categories,series,
    barOptions:{direction:'bar',grouping,gapWidth:70,overlap:grouping==='clustered'?0:100},
    hasLegend:legend,legend:{position:'bottom',overlay:false,textStyle:{fontSize:22,fill:INK}},
    ...axes(min,max,format),dataLabels:{showValue:labels,numberFormatCode:format,position:grouping==='clustered'?'outEnd':'center',textStyle:{fontSize:22,fill:grouping==='clustered'?INK:'#FFFFFF',bold:true}}});
}
function metric(s,value,label,x,y,w,color=INK,size=70){text(s,value,x,y,w,95,size,color,true);text(s,label,x,y+97,w,115,27,INK);}

// 1. The requested three pies, preserving the user's earlier projection of regime 0.
{
  const s=slide('Уклады на трёх стадиях перехода','Стадия описывает роль труда в распределении благ. Цвет показывает устройство общества.',
    'Stage counts: zero_variant=345, transition=75, post_work=470. For the 345 original zero regimes only, use guarantees<0 and control boundaries +/-1/3. Other records retain their editorial regime. Shares are within each stage; the three stages are separate cross-sectional samples, not a measured trajectory.');
  for(let j=0;j<3;j++){
    const st=ST[j],rows=DATA.regimes.filter(r=>r.stage===st);
    text(s,SHORT[j],65+j*510,200,460,43,30,STCOLOR[j],true,'center');
    text(s,DATA.stages[st].n+' обществ, '+pct(DATA.stages[st].n/890)+' базы',65+j*510,246,460,35,24,MUTED,false,'center');
    const values=rows.map(r=>r.n),total=values.reduce((a,b)=>a+b,0);
    chart(s,'pie',{position:{left:65+j*510,top:294,width:460,height:360},categories:REGLABEL,
      series:[{name:SHORT[j],values,points:REGCOLOR.map((fill,idx)=>({idx,fill,line:{style:'solid',fill:'#FFFFFF',width:1.5}})),dataLabelOverrides:values.map((v,idx)=>({idx,showPercent:v/total>=.045,showValue:false,showCategoryName:false,textStyle:{fontSize:24,fill:idx===0||idx===3?INK:'#FFFFFF',bold:true}}))}],
      pieOptions:{firstSliceAngle:270},hasLegend:false,
      dataLabels:{showPercent:true,showValue:false,showCategoryName:false,position:'center',numberFormatCode:'0.0%',textStyle:{fontSize:24,fill:'#FFFFFF',bold:true}}});
  }
  for(let k=0;k<6;k++)text(s,REGLABEL[k],80+(k%2)*760,697+Math.floor(k/2)*40,735,36,23,REGCOLOR[k],true);
  text(s,'У трудовых обществ уклад задан координатами. Границы: гарантии 0, контроль −⅓ и +⅓.',65,815,1470,28,18,MUTED);
}
// 2. Averages conceal both tails.
{
  const s=slide('Среднее скрывает разные доли крайних исходов','Частичный и полный переход имеют среднюю U около −0,12, но разные распределения.',
    'Strong dystopia U<=-0.5, strong utopia U>=0.5, central band -0.5<U<0.5. Post-work vs partial differences remain after medium controls and equal recognition-group weighting: strong utopia +13.2 percentage points (q<0.001), strong dystopia +12.4 points (q<0.05). Thresholds are descriptive editorial choices.');
  bar(s,{x:65,y:230,w:1130,h:480,categories:CAT,grouping:'stacked',series:[
    {name:'Сильная дистопия',values:ST.map(st=>DATA.stages[st].strong_dystopia_share),fill:'#AD654D'},
    {name:'Промежуточные оценки',values:ST.map(st=>DATA.stages[st].central_share),fill:'#D7E0DF',dataLabels:{showValue:true,numberFormatCode:'0%',position:'center',textStyle:{fontSize:22,fill:INK,bold:true}}},
    {name:'Сильная утопия',values:ST.map(st=>DATA.stages[st].strong_utopia_share),fill:'#277F75',dataLabels:{showValue:true,numberFormatCode:'0%',position:'center',textStyle:{fontSize:22,fill:'#FFFFFF',bold:true}},dataLabelOverrides:[{idx:0,showValue:false},{idx:1,showValue:false}]},
  ]});
  metric(s,'19%','сильных утопий при полном переходе',1220,240,320,'#277F75',78);
  metric(s,'4%','сильных утопий при частичном переходе',1220,505,320,'#D69C46',78);
  text(s,'Сильная дистопия: U ≤ −0,5. Сильная утопия: U ≥ +0,5. Центральная зона включает смешанные и неясные случаи.',65,764,1470,62,22,MUTED);
}
// 3. Security differs between stages; within each stage it also distinguishes U.
{
  const s=slide('Гарантии различают исходы при любой стадии перехода','При полном переходе гарантии встречаются чаще, а их отсутствие связано с самой низкой средней U.',
    'Guarantees here use the same sign rule for all stages: axis.guarantees<0. Cells: zero no 316 U=-.506, yes 29 U=.055; partial no49 U=-.242, yes26 U=.112; full no155 U=-.642, yes315 U=.145. This is observational composition, not a causal transition effect.');
  text(s,'Доля обществ с гарантиями',65,218,665,44,28,INK,true);
  bar(s,{x:65,y:272,w:665,h:410,categories:SHORT,series:[{name:'Гарантии',values:ST.map(st=>DATA.stages[st].secure_share),fill:'#277F75'}],legend:false});
  text(s,'Средняя утопичность',835,218,700,44,28,INK,true);
  bar(s,{x:835,y:272,w:700,h:410,categories:SHORT,min:-.8,max:.3,format:'0.00',series:[
    {name:'Без гарантий',values:ST.map(st=>DATA.security.find(r=>r.stage===st&&!r.has_guarantees).mean_utopia),fill:'#AD654D'},
    {name:'С гарантиями',values:ST.map(st=>DATA.security.find(r=>r.stage===st&&r.has_guarantees).mean_utopia),fill:'#277F75'}]});
  text(s,'Полный переход без гарантий: U = −0,64. Трудовая зависимость без гарантий: U = −0,51.',65,734,1470,45,29,INK,true);
  text(s,'Гарантии на этом слайде означают axis.guarantees < 0. Все ячейки имеют не менее 26 записей.',65,792,1470,32,21,MUTED);
}
// 4. Post-wage is not zero participation.
{
  const s=slide('Посттрудовые общества сохраняют массовую работу','В разметке работа включает добровольное творчество, заботу, исследования и обязательные задания.',
    'Mean working share equals 1-axis.nonworking. Of 470 full-transition records, 341 have nonworking<=.5, so at least half the scoped population works. 11 have nonworking>=.95. Participation values are low-confidence editorial scenarios, not labour-market surveys.');
  bar(s,{x:65,y:230,w:1000,h:470,categories:CAT,series:[{name:'Средняя доля работающих',values:ST.map(st=>1-DATA.stages[st].mean_nonworking),fill:'#6874B5'}],legend:false});
  metric(s,pct(DATA.stages.post_work.share_majority_working,0),'посттрудовых обществ: работает хотя бы половина населения',1160,240,370,'#277F75',86);
  metric(s,'11 из 470','имеют оценку неработающих 95% и выше',1160,535,370,INK,52);
  text(s,'Переход означает, что труд перестал быть главным каналом получения благ. Участие в деятельности оценивается отдельно.',65,754,1470,76,26,INK);
}
// 5. Three stages across media.
{
  const ms=['book','anime','manga','game','tv','movie','comic','web_fiction'];
  const ml={book:'Книги',anime:'Аниме',manga:'Манга',game:'Игры',tv:'Телевидение',movie:'Кино',comic:'Комиксы',web_fiction:'Веб-проза'};
  const s=slide('Доля состоявшегося перехода различается между медиа','Теги медиа пересекаются. Размер выборки указан рядом с каждой строкой.',
    'Source transition-media-counts.csv. Web fiction has 29 rows but only 6 recognition groups; 23 of 29 belong to Orion’s Arm. This is a selected catalogue, not all fiction. Manga has only 18 rows.');
  bar(s,{x:65,y:217,w:1470,h:530,categories:ms.map(m=>ml[m]+', n = '+DATA.media.find(r=>r.medium===m).media_n),grouping:'stacked',series:ST.map((st,i)=>({name:SHORT[i],fill:STCOLOR[i],values:ms.map(m=>DATA.media.find(r=>r.medium===m&&r.stage===st).share_in_medium),dataLabelOverrides:ms.map((m,idx)=>({idx,showValue:DATA.media.find(r=>r.medium===m&&r.stage===st).share_in_medium>=.035}))}))});
  text(s,'Веб-проза: 27 из 29 обществ прошли переход, но 23 записи принадлежат Orion’s Arm. У манги всего 18 записей.',65,788,1470,44,22,MUTED);
}
// 6. Within-group comparison.
{
  const a=DATA.paired_groups.post_work_minus_zero_variant;
  const s=slide('Сравнение обществ внутри одной группы','В 60 из 84 групп посттрудовые общества имеют более высокую среднюю U, чем трудовые.',
    'Recognition groups approximate works/franchises, not a universal universe ontology. Positive group differences:60, negative23, tie1. Average equally weighted paired difference .358987, group bootstrap 5000 draws 95% [.2303,.4845]. Distinct societies can differ in population and chronology; these pairs are not randomized policy transitions.');
  bar(s,{x:65,y:230,w:950,h:440,categories:['Посттрудовые выше','Трудовые выше','Одинаковая средняя U'],max:84,format:'0',legend:false,series:[{name:'Групп',values:[a.positive_groups,a.negative_groups,a.ties],points:[{idx:0,fill:'#277F75'},{idx:1,fill:'#AD654D'},{idx:2,fill:'#7B8896'}]}]});
  metric(s,num(a.mean_difference),'средняя разница U между посттрудовыми и трудовыми',1120,235,420,'#277F75',82);
  text(s,'95%-ный интервал\n['+num(a.low)+'; '+num(a.high)+']',1120,480,420,112,30,MUTED);
  text(s,'Одна франшиза может показывать противоположные модели. Сравнение внутри группы ослабляет влияние известности и медиа.',65,748,1470,80,27,INK);
}
// 7. An editable evidence table with the change in comparisons after controls.
{
  const s=slide('Связь стадии с утопичностью зависит от состава сравнения','Разница U с трудовыми обществами. Веса групп одинаковы, ошибки учитывают зависимость внутри группы.',
    'WLS results from transition-analysis.json, models utopia_raw, utopia_media_adjusted, utopia_structural_adjusted. CIs are unadjusted 95% CR1 cluster intervals. Structural controls: security, control, control squared, nonworking, popularity, multi-label media. These include potential mediators and shared rating criteria, so coefficients are not causal transition effects. Within-group structural full transition coefficient -.091, CI[-.182,.001]. Saved axis intervals are wide and can alter these conditional coefficients.');
  const names=['utopia_raw','utopia_media_adjusted','utopia_structural_adjusted'];
  const labels=['Только стадия','Медиа и узнаваемость','Также гарантии, контроль, участие'];
  const cell=(m,t)=>{const c=DATA.models[m].coefficients.find(v=>v.term===t);return num(c.beta)+'\n['+num(c.low)+'; '+num(c.high)+']';};
  const vals=[['Условия сравнения','Частичный переход','Полный переход'],...names.map((m,i)=>[labels[i],cell(m,'partial_transition'),cell(m,'full_transition')])];
  const table=s.tables.add({rows:4,columns:3,left:65,top:230,width:1470,height:365,columnWidths:[650,410,410],values:vals});
  table.borders.assign({fill:'#DAE3E4',width:1,style:'solid'});
  for(let r=0;r<4;r++){
    table.rows[r].height=r===0?65:100;
    for(let c=0;c<3;c++){
      const cell=table.getCell(r,c);cell.fill=r===0?'#E9F1EF':'#FFFFFF';
      cell.text.style={typeface:FONT,fontSize:r===0?27:28,bold:r===0,color:INK,verticalAlignment:'middle',alignment:c===0?'left':'center',insets:15,autoFit:'none'};
    }
  }
  text(s,'После учёта условий преимущество полного перехода исчезает. Это условная связь, чувствительная к разметке координат.',65,650,1470,95,31,INK,true);
  text(s,'Гарантии и контроль входят и в описание общества, и в оценку благополучия. Таблица не измеряет последствия самого перехода.',65,773,1470,60,23,MUTED);
}
// 8. Popularity is a different dimension.
{
  const s=slide('Узнаваемость почти не различает три стадии','Показаны средние редакторские оценки популярности с равным весом групп внутри стадии.',
    'Group-balanced popularity: .47838, .50385, .46735. Group scores repeat across their societies; the values are not audience percentages. WLS with medium controls: partial-zero .004[-.049,.057], full-zero .014[-.017,.044]; q>.45. Overall group significance does not establish historical popularity changes.');
  bar(s,{x:65,y:230,w:1000,h:450,categories:CAT,format:'0.00',legend:false,series:[{name:'Узнаваемость',values:ST.map(st=>DATA.stages[st].group_balanced_popularity),fill:'#6874B5'}]});
  metric(s,'≈0,5','средняя узнаваемость у каждой стадии',1160,265,365,'#6874B5',82);
  text(s,'Одинаковый балл наследуют все общества одной группы.',1160,535,365,120,26,MUTED);
  text(s,'После поправки на медиа различия неубедительны. Для исторической популярности нужен временной ряд аудитории.',65,740,1470,90,28,INK);
}
// 9. Explicit records show why stage alone does not define utopia.
{
  const ids=['starwars-narkina5-cheap-labor-zero','aria-aqua-terraformed-work-zero','colossus-initial-machine-rule-zero','transformers-one-restored-energon','matrix-pod-humanity','culture-main'];
  const names=['Трудовые: Narkina 5','Трудовые: Aria / Аква','Частичный: Colossus','Частичный: Iacon после восстановления','Посттрудовые: люди в Матрице','Посттрудовые: Культура'];
  const rr=ids.map(id=>RAW.find(r=>r.id===id));
  const s=slide('Каждая стадия допускает противоположные исходы','Сопоставимые статусы могут сочетаться с принуждением, свободным выбором или исключением части населения.',
    rr.map(r=>'ID '+r.id+'; status='+r.post_work_assessment.status+'; U='+r.utopia_score+'; scope='+JSON.stringify(r.scope)+'; rationale='+r.utopia_assessment.basis).join('\n'));
  bar(s,{x:65,y:222,w:1470,h:495,categories:names,min:-1,max:1,format:'0.00',legend:false,series:[{name:'Утопичность',values:rr.map(r=>r.utopia_score),points:rr.map((r,idx)=>({idx,fill:r.utopia_score<0?'#AD654D':'#277F75'})),dataLabelOverrides:rr.map((r,idx)=>({idx,showValue:true,position:r.utopia_score<0?'inEnd':'outEnd',textStyle:{fontSize:22,fill:r.utopia_score<0?'#FFFFFF':INK,bold:true}}))}]});
  text(s,'Для нового исследования полезно отдельно разметить свободу выхода, принуждение и охват гарантий, независимо от U.',65,765,1470,65,27,INK);
}

const candidate=path.join(BUILD,'candidate.pptx');
await (await PresentationFile.exportPptx(prs)).save(candidate);
for(let i=0;i<prs.slides.items.length;i++){
  const b=await prs.export({slide:prs.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(BUILD,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));
}
await fs.writeFile(path.join(BUILD,'layout.ndjson'),(await prs.inspect({kind:'slide,textbox,table,chart',maxChars:500000})).ndjson);
console.log(JSON.stringify({draft:candidate,slides:prs.slides.items.length,previewDir:BUILD}));
if(process.argv.includes('--finalize')){
  const finalName=process.argv.find(v=>v.startsWith('--output='))?.slice(9)??'post-work-stages-v2.pptx';
  const finalPath=path.join(OUT,finalName);
  const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,pythonExecutable:RUNTIME_PYTHON,
    integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--validate-bullet-geometry','--require-native-table-slide','7'],
    requiredNativeTableOwnerSlides:[7],requiredNativeChartOwnerSlides:[1,2,3,4,5,6,8,9],materializeLiteralChartWorkbooks:true,
    fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
    receiptPath:path.join(BUILD,finalName+'.validation.json')});
  const final=await PresentationFile.importPptx(await FileBlob.load(finalPath));
  for(let i=0;i<final.slides.items.length;i++){
    const b=await final.export({slide:final.slides.items[i],format:'png',scale:1});
    await fs.writeFile(path.join(OUT,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await b.arrayBuffer()));
  }
  const html=`<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Три стадии перехода: 9 слайдов</title><style>body{margin:0;background:#182f34;color:white;font:18px/1.5 Arial,sans-serif}header{padding:22px 4vw}a{color:#b5e3d5}main{max-width:1600px;margin:auto}figure{margin:0 0 22px}img{width:100%;height:auto;display:block}figcaption{padding:8px 3vw;color:#b9c9ce;font-size:14px}</style><header><b>Три стадии перехода</b><br><a href="${finalName}">Скачать редактируемую презентацию PowerPoint</a> · <a href="../report.html#transitions">Открыть подробный анализ</a></header><main>${Array.from({length:9},(_,i)=>`<figure id="slide-${i+1}"><img src="slide-${String(i+1).padStart(2,'0')}.png" alt="Слайд ${i+1}"><figcaption>${i+1} / 9</figcaption></figure>`).join('')}</main></html>`;
  await fs.writeFile(path.join(OUT,'index.html'),html,'utf8');
  console.log(JSON.stringify({finalPath,slides:final.slides.items.length,validationReceipt:result.receiptPath}));
}
