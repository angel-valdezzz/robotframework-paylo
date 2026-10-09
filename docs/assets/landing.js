/* Paylo's real generated payloads; remount safely on Material instant navigation. */
(() => {
  'use strict';
  let dispose=()=>{};
  function mount() {
    dispose();
    const cleanups=[];
    let active=true;
    function listen(el,event,callback){if(el){el.addEventListener(event,callback);cleanups.push(()=>el.removeEventListener(event,callback));}}
    const search=document.querySelector('.pl-search-trigger');
    listen(search,'keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();search.click();}});
    function syncGradient(){const header=document.querySelector('.md-header'),tabs=document.querySelector('.md-tabs');const a=header?.getAnimations().find(x=>x.animationName==='pl-header-flow'),b=tabs?.getAnimations().find(x=>x.animationName==='pl-header-flow');if(a&&b)b.currentTime=a.currentTime;}
    let syncRaf=requestAnimationFrame(syncGradient);
    listen(window,'resize',syncGradient);
    const hero=document.querySelector('[data-pl-hero]');
    dispose=()=>{active=false;cancelAnimationFrame(syncRaf);cleanups.forEach(fn=>fn());};
    if(!hero)return;
    const $=selector=>hero.querySelector(selector);
    const $$=selector=>[...hero.querySelectorAll(selector)];
    const language=hero.dataset.lang==='es'?'es':'en';
    const messages={
      es:{pause:'Pausar',resume:'Continuar',ready:'Una estructura. Datos que cambian.',completed:'Payload listo',substituting:'Sustituyendo',static:'Tipos conservados',captions:['Texto, sin perder su contexto.','Un número. No una cadena.','Un booleano. No texto.'],finished:'El mismo JSON. Los tipos originales.'},
      en:{pause:'Pause',resume:'Resume',ready:'One structure. Changing data.',completed:'Payload ready',substituting:'Substituting',static:'Types preserved',captions:['A string, with its context intact.','A number. Not a string.','A boolean. Not text.'],finished:'The same JSON. The original types.'}
    };
    const pause=$('#pl-pause'),assembly=$('.pl-assembly');
    const reduced=matchMedia('(prefers-reduced-motion: reduce)');
    let paused=false,onscreen=true,elapsed=0,previous=null,stateKey='',data,geometry,raf;
    const sources=$$('[data-pl-source]'),values=$$('[data-pl-value]'),inputs=$$('[data-pl-input]');
    const rows=$$('[data-pl-row]'),types=$$('[data-pl-type]'),traveler=$('#pl-traveler');
    const names=['name','quantity','active'];
    listen(pause,'click',()=>{paused=!paused;hero.toggleAttribute('data-pl-paused',paused);pause.setAttribute('aria-pressed',String(paused));pause.firstElementChild.textContent=paused?'▷':'Ⅱ';pause.lastElementChild.textContent=messages[language][paused?'resume':'pause'];previous=null;});
    listen($('.pl-scroll'),'click',event=>{event.preventDefault();const content=document.querySelector('#overview');content.focus({preventScroll:true});content.scrollIntoView({behavior:reduced.matches?'instant':'smooth'});history.replaceState(null,'','#overview');});
  function measure(index) {
    const origin = assembly.getBoundingClientRect();
    const source = sources[index].getBoundingClientRect();
    const destination = values[index].getBoundingClientRect();
    const style = getComputedStyle(values[index]);
    const startFont = parseFloat(getComputedStyle(sources[index]).fontSize);
    const endFont = parseFloat(style.fontSize);
    geometry = {x:source.left-origin.left+parseFloat(getComputedStyle(sources[index]).paddingLeft),
      y:source.top-origin.top+(source.height-startFont*1.4)/2,
      tx:destination.left-origin.left,ty:destination.top-origin.top,
      startFont,endFont};
  }
  function render() {
    // Reconcile every frame as well as on the media event: the preference can
    // change while Material retains the page or while motion is paused.
    pause.disabled = reduced.matches;
    if (!data) return;
    const cycle = 10900;
    const scenarioIndex = reduced.matches ? 0 : Math.floor(elapsed/cycle)%data.scenarios.length;
    const part = reduced.matches ? 8500 : elapsed%cycle;
    const scenario = data.scenarios[scenarioIndex];
    const phase = part < 600 ? 'ready' : part < 8100 ? 'field' : part < 10300 ? 'complete' : 'reset';
    const index = phase === 'field' ? Math.min(2,Math.floor((part-600)/2500)) : -1;
    const progress = index < 0 ? 0 : (part-600-index*2500)/1000;
    const arrived = phase === 'complete' || (phase === 'field' && progress >= 1);
    const completed = phase === 'complete' || phase === 'reset' ? 3 : index < 0 ? 0 : index + (arrived ? 1 : 0);
    const key = [scenarioIndex,phase,index,arrived,language].join(':');
    if (key !== stateKey) {
      stateKey = key;
      assembly.dataset.phase = phase;
      assembly.dataset.scenario = scenarioIndex;
      assembly.classList.toggle('pl-complete',phase === 'complete');
      $('#pl-scenario-number').textContent = String(scenarioIndex+1).padStart(2,'0');
      $('#pl-scenario-name').textContent = scenario.variables.customer.name;
      sources.forEach((el,i) => {el.textContent = JSON.stringify(scenario.payload[names[i]]);});
      values.forEach((el,i) => {
        const done = i < completed;
        el.textContent = done ? JSON.stringify(scenario.payload[names[i]]) : JSON.stringify(data.template[names[i]]);
        el.classList.toggle('pl-placeholder',!done);
        el.classList.toggle('pl-received',done && i === index);
        rows[i].classList.toggle('pl-active',i===index);
        rows[i].classList.toggle('pl-done',done);
        inputs[i].classList.toggle('pl-active',i===index);
        types[i].classList.toggle('pl-active',i===index);
        types[i].classList.toggle('pl-done',done);
      });
      $('#pl-step-caption').textContent = phase === 'complete' ? messages[language].finished : index >= 0 ? messages[language].captions[index] : messages[language].ready;
      $('#pl-state-label').textContent = reduced.matches ? messages[language].static : phase === 'complete' ? messages[language].completed : messages[language].substituting;
      traveler.hidden = index < 0 || arrived;
      if (!traveler.hidden) {
        traveler.textContent = JSON.stringify(scenario.payload[names[index]]);
        measure(index);
      }
    }
    if (index >= 0 && !arrived && geometry) {
      const t = Math.min(1,Math.max(0,progress));
      const ease = t*t*(3-2*t);
      const g = geometry;
      // Follow the clear gap above the row so a traveling value never covers a key.
      const lift = Math.sin(Math.PI*t)*(innerWidth<=760 ? 24 : 29);
      traveler.style.transform = `translate(${g.x+(g.tx-g.x)*ease}px,${g.y+(g.ty-g.y)*ease-lift}px)`;
      traveler.style.fontSize = `${g.startFont+(g.endFont-g.startFont)*ease}px`;
      traveler.style.opacity = String(Math.min(1,t*10,(1-t)*10));
      values[index].style.opacity = String(t>.7 ? 1-(t-.7)/.3 : 1);
    }
    values.forEach((el,i) => {if (i!==index || arrived) el.style.opacity = '';});
    const fade=phase==='reset' ? 1-(part-10300)/600 : phase==='ready' && elapsed>=10900 ? part/600 : 1;
    sources.forEach(el=>{el.style.opacity=String(fade);});
    values.forEach(el=>{if(fade!==1)el.style.opacity=String(fade);});
    assembly.dataset.field=String(index);
    assembly.dataset.arrived=String(arrived);
  }
  function tick(now) {
    if (active && previous !== null && !paused && !document.hidden && onscreen && !reduced.matches) elapsed += Math.min(64,now-previous);
    previous = now;
    render();
    if (active) raf=requestAnimationFrame(tick);
  }

    const resize=new ResizeObserver(()=>{stateKey='';geometry=null;render();});
    resize.observe(assembly);
    const intersection=new IntersectionObserver(entries=>{onscreen=entries[0].isIntersecting;previous=null;},{threshold:.05});
    intersection.observe(hero);
    listen(document,'visibilitychange',()=>{previous=null;});
    listen(reduced,'change',()=>{pause.disabled=reduced.matches;previous=null;stateKey='';render();});
    const controller=new AbortController();
    fetch(hero.dataset.scenariosUrl,{signal:controller.signal}).then(response=>{if(!response.ok)throw new Error('Scenario data unavailable');return response.json();}).then(result=>{
      if(!active)return;
      data=result;pause.hidden=false;pause.disabled=reduced.matches;render();
      document.fonts.ready.then(()=>{if(active){stateKey='';render();}});
      raf=requestAnimationFrame(tick);
    }).catch(error=>{if(active&&error.name!=='AbortError')$('#pl-state-label').textContent=language==='es'?'Plantilla JSON':'JSON template';});
    const previousDispose=dispose;
    dispose=()=>{previousDispose();cancelAnimationFrame(raf);resize.disconnect();intersection.disconnect();controller.abort();};
  }
  if(typeof document$!=='undefined')document$.subscribe(mount);
  else if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount,{once:true});
  else mount();
})();
