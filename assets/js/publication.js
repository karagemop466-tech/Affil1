(() => {
 const filters=document.querySelectorAll('[data-filter]');
 filters.forEach(btn=>btn.onclick=()=>{filters.forEach(b=>b.setAttribute('aria-pressed',b===btn)); document.querySelectorAll('[data-group]').forEach(a=>a.hidden=btn.dataset.filter!=='All picks'&&btn.dataset.filter!==a.dataset.group)});
 const open=document.querySelector('.saved-open'), dlg=document.querySelector('#saved-list');
 let saved={}; try{saved=JSON.parse(localStorage.getItem('cc-picks')||'{}')||{}}catch{}
 function update(){document.querySelector('[data-count-saved]').textContent=Object.keys(saved).length;document.querySelectorAll('.save-pick').forEach(b=>{b.setAttribute('aria-pressed',!!saved[b.dataset.id]);b.setAttribute('aria-label',(saved[b.dataset.id]?'Unsave ':'Save ')+b.dataset.name)})}
 function persist(){try{localStorage.setItem('cc-picks',JSON.stringify(saved))}catch{} update()}
 function draw(){const box=document.querySelector('#saved-content');box.replaceChildren();for(const [id,name] of Object.entries(saved)){if(!/^p-0[1-5]$/.test(id))continue;const row=document.createElement('p'),a=document.createElement('a'),remove=document.createElement('button');a.href=open.dataset.root.replace('index.html',id+'.html');a.textContent=name;remove.textContent='Remove';remove.onclick=()=>{delete saved[id];persist();draw()};row.append(a,remove);box.append(row)}if(!box.children.length)box.textContent='Your list is empty. Use the bookmark on a product in the countertop shortlist to save it here.'}
 document.querySelectorAll('.save-pick').forEach(b=>b.onclick=()=>{if(saved[b.dataset.id])delete saved[b.dataset.id];else saved[b.dataset.id]=b.dataset.name;persist()});open.onclick=()=>{draw();dlg.showModal()};dlg.querySelector('.dialog-close').onclick=()=>dlg.close();dlg.onclick=e=>{if(e.target===dlg)dlg.close()};update();
})();
