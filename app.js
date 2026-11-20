(function(){
 const list=document.getElementById('product-list'); if(!list)return;
 window.PRODUCTS.forEach((p,i)=>{
   const row=document.createElement('article'); row.className='product-row';
   const label=document.createElement('span'); label.className='product-number'; label.textContent=String(i+1).padStart(2,'0');
   const info=document.createElement('div'); info.innerHTML='<b>Submitted link '+String(i+1)+'</b><small>Intended ID: '+p.intendedAsin+' · destination unverified</small>';
   const link=document.createElement('a'); link.href=p.submitted; link.target='_blank'; link.rel='sponsored nofollow noopener'; link.textContent='Check listing ↗'; link.setAttribute('aria-label','Open submitted Amazon link '+(i+1)+'; destination is unverified');
   row.append(label,info,link);list.appendChild(row);
 });
})();
