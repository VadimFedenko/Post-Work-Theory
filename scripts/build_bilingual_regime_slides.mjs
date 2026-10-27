import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import {fileURLToPath, pathToFileURL} from 'node:url';

process.on('uncaughtException', error => {
  console.error(error.name + ': ' + error.message);
  console.error((error.stack ?? '').split('\n').filter(x => x.includes('build_bilingual')).join('\n'));
  process.exit(1);
});
const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SKILL = 'C:/Users/Vadim/.codex/plugins/cache/openai-primary-runtime/presentations/26.1022.11436/skills/presentations';
const MODULES = 'C:/Users/Vadim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const PYTHON = 'C:/Users/Vadim/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
process.env.RUNTIME_NODE_MODULES = MODULES;
const {Presentation, PresentationFile, FileBlob} = await import(pathToFileURL(path.join(MODULES, '@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {applyPresentationChartFont, finalizePresentation} = await import(pathToFileURL(path.join(SKILL, 'container_tools/artifact_tool_utils.mjs')).href);
const BASE = path.join(ROOT, 'research/exploratory-analysis');
const SOURCE = path.join(BASE, 'presentation/post-work-stages-v2.pptx');
const BUILD = path.join(BASE, '.bilingual-slides-build');
const OUT = path.join(BASE, 'presentation/bilingual');
await fs.mkdir(BUILD, {recursive:true});
await fs.mkdir(OUT, {recursive:true});
const sourceHash = crypto.createHash('sha256').update(await fs.readFile(SOURCE)).digest('hex');
const source = await PresentationFile.importPptx(await FileBlob.load(SOURCE));
// Reuse the source composition and its complete literal chart data, with a
// separate editable chart workbook for each language version.
const p = Presentation.create({slideSize:{width:1600,height:900}});

const translations = new Map([
  ['Уклады на трёх стадиях перехода', 'Regimes across three transition stages'],
  ['Стадия описывает роль труда в распределении благ. Цвет показывает устройство общества.', 'Stage describes the role of work in access to goods. Colour shows how society is organised.'],
  ['Источник: data/societies.json, 890 обществ. Редакторские оценки на 22.10.2026.', 'Source: data/societies.json, 890 societies. Editorial assessments as of 22 Oct 2026.'],
  ['Трудовые', 'Work-dependent'],
  ['Частичный переход', 'Partial transition'],
  ['Посттрудовые', 'Post-work'],
  ['345 обществ, 38,8% базы', '345 societies, 38.8% of total'],
  ['75 обществ, 8,4% базы', '75 societies, 8.4% of total'],
  ['470 обществ, 52,8% базы', '470 societies, 52.8% of total'],
  ['1  Элиты с гарантиями', '1  Elite control with guarantees'],
  ['2  Элиты без гарантий', '2  Elite control without guarantees'],
  ['3  Распределённая власть с гарантиями', '3  Distributed control with guarantees'],
  ['4  Распределённые активы без гарантий', '4  Distributed assets without guarantees'],
  ['5  Автономная система с гарантиями', '5  Autonomous system with guarantees'],
  ['6  Автономная система без гарантий', '6  Autonomous system without guarantees'],
  ['У трудовых обществ уклад задан координатами. Границы: гарантии 0, контроль −⅓ и +⅓.', 'Coordinates assign regimes to work-dependent societies. Boundaries: guarantees 0, control −⅓ and +⅓.'],
  ['1', '2'],
]);
const englishCategories = [...translations].filter(([x]) => /^[1-6]  /.test(x)).map(([,y]) => y);
const russianCategories = [...translations.keys()].filter(x => /^[1-6]  /.test(x));
const expected = [[17,226,11,42,1,48],[11,29,12,10,5,8],[115,80,116,11,89,59]];
const stageLabels = ['Трудовые','Частичный переход','Посттрудовые'];
const stageCounts = ['345 обществ, 38,8% базы','75 обществ, 8,4% базы','470 обществ, 52,8% базы'];
const REGCOLOR=['#D69C46','#AD654D','#277F75','#5C9D85','#6874B5','#9C5D91'];
const STCOLOR=['#7B8896','#D69C46','#277F75'];
const INK='#223A40', MUTED='#60747A';
function text(slide, value, x,y,w,h,size,color,bold=false,alignment='left') {
  const shape=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});
  shape.text=value;
  shape.text.style={typeface:'Arial',fontSize:size,bold,color,alignment,verticalAlignment:'top',autoFit:'none',wrap:'square',insets:0};
}
for (let language=0;language<2;language++) {
  const s=p.slides.add(); s.background.fill='#FFFFFF';
  const t=value=>language===0?value:translations.get(value);
  text(s,t('Уклады на трёх стадиях перехода'),65,43,1470,70,44,INK,true);
  text(s,t('Стадия описывает роль труда в распределении благ. Цвет показывает устройство общества.'),65,122,1470,72,25,MUTED);
  text(s,t('Источник: data/societies.json, 890 обществ. Редакторские оценки на 22.10.2026.'),65,851,1400,30,17,MUTED);
  text(s,String(language+1),1485,850,50,30,18,MUTED,false,'right');
  const labels=language===0?russianCategories:englishCategories;
  for (let j=0;j<3;j++) {
    const values=expected[j], total=values.reduce((a,b)=>a+b,0);
    const originalValues=source.slides.items[0].charts.items[j].series.items[0].values;
    if(JSON.stringify(values)!==JSON.stringify(originalValues)) throw new Error('Source chart values differ');
    text(s,t(stageLabels[j]),65+j*510,200,460,43,30,STCOLOR[j],true,'center');
    text(s,t(stageCounts[j]),65+j*510,246,460,35,24,MUTED,false,'center');
    const c=s.charts.add('pie',{
      position:{left:65+j*510,top:294,width:460,height:360},
      chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF',chartLine:{style:'solid',fill:'none',width:0},plotAreaLine:{style:'solid',fill:'none',width:0},titlePlacement:'none',
      categories:labels,
      series:[{name:t(stageLabels[j]),values,points:REGCOLOR.map((fill,idx)=>({idx,fill,line:{style:'solid',fill:'#FFFFFF',width:1.5}})),
        dataLabelOverrides:values.map((v,idx)=>({idx,showPercent:v/total>=.045,showValue:false,showCategoryName:false,textStyle:{fontSize:24,fill:idx===0||idx===3?INK:'#FFFFFF',bold:true,typeface:'Arial'}}))}],
      pieOptions:{firstSliceAngle:270},hasLegend:false,
      dataLabels:{showPercent:true,showValue:false,showCategoryName:false,position:'center',numberFormatCode:'0.0%',textStyle:{fontSize:24,fill:'#FFFFFF',bold:true,typeface:'Arial'}}
    });
    applyPresentationChartFont(c,{fontFamily:'Arial'});
  }
  for(let k=0;k<6;k++)text(s,labels[k],80+(k%2)*760,697+Math.floor(k/2)*40,735,36,23,REGCOLOR[k],true);
  text(s,t('У трудовых обществ уклад задан координатами. Границы: гарантии 0, контроль −⅓ и +⅓.'),65,815,1470,28,18,MUTED);
  s.speakerNotes.text=source.slides.items[0].speakerNotes.text;
}
const en=p.slides.items[1];
en.speakerNotes.text = 'Source: data/societies.json, 890 societies. Editorial assessments as of 22 Oct 2026.\nDerived data: research/exploratory-analysis/transition-analysis.json\nStage counts: work-dependent 345, partial transition 75, post-work 470. The 345 original regime-0 societies receive a chart regime from guarantees < 0 and control boundaries −1/3 and +1/3. Other records retain their editorial regime. Shares are within each stage. The three stages are cross-sectional groups, not a measured trajectory. Post-work means that work has ceased to be the principal channel of access to goods.\nRegime counts, in category order 1 to 6: work-dependent [17,226,11,42,1,48], partial transition [11,29,12,10,5,8], post-work [115,80,116,11,89,59].';
if (p.slides.items.length !== 2) throw new Error('Expected exactly two slides');
for (const slide of p.slides.items) {
  if (slide.charts.items.length !== 3) throw new Error('Expected three charts');
  slide.charts.items.forEach((c, i) => {
    if (JSON.stringify(c.series.items[0].values) !== JSON.stringify(expected[i])) throw new Error('Chart values changed');
  });
}
const candidate = path.join(BUILD, 'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
for (let i=0; i<2; i++) {
  const blob = await p.export({slide:p.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(BUILD, i === 0 ? 'ru.png' : 'en.png'), new Uint8Array(await blob.arrayBuffer()));
}
await fs.writeFile(path.join(BUILD, 'layout.ndjson'), (await p.inspect({select:'$.slides[*]',include:['id','index','elements.id','elements.kind','elements.text','elements.position','elements.style']})).ndjson);
console.log(JSON.stringify({draft:candidate,slides:p.slides.items.length,previews:BUILD}));
if (process.argv.includes('--finalize')) {
  const finalName = process.argv.find(x => x.startsWith('--output='))?.slice(9) ?? 'regimes-ru-en.pptx';
  const finalPath = path.join(OUT, finalName);
  await finalizePresentation({
    workspaceDir:ROOT, candidatePath:candidate, finalPath, pythonExecutable:PYTHON,
    integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
    layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
    layoutArgs:['--expected-slide-size-emu','15240000,8572500','--validate-heading-fit','--validate-bullet-geometry'],
    explicitTotalSlideCount:2, requiredNativeTableOwnerSlides:[], requiredNativeChartOwnerSlides:[1,2],
    // New native chart workbooks snapshot the exact counts from the source slide.
    materializeLiteralChartWorkbooks:true,
    fontPolicy:{basis:'reference',families:['Arial'],referencePath:SOURCE,referenceSha256:sourceHash},
    verifyArtifactToolImport:true, receiptPath:path.join(BUILD,finalName+'.validation.json'),
  });
  const final = await PresentationFile.importPptx(await FileBlob.load(finalPath));
  if(final.slides.items.length !== 2) throw new Error('Final deck slide count changed');
  for(let i=0;i<2;i++){
    const blob=await final.export({slide:final.slides.items[i],format:'png',scale:1});
    await fs.writeFile(path.join(OUT,i===0?'slide-ru.png':'slide-en.png'),new Uint8Array(await blob.arrayBuffer()));
  }
  console.log(JSON.stringify({finalPath,slides:final.slides.items.length,charts:final.slides.items.reduce((n,s)=>n+s.charts.items.length,0)}));
}
