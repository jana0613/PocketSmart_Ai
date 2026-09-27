const tokenKey = 'pocketsmart_token';
function token(){ return localStorage.getItem(tokenKey); }
function authHeaders(json=true){ const h={}; if(json) h['Content-Type']='application/json'; if(token()) h.Authorization=`Bearer ${token()}`; return h; }
function requireAuth(){ if(!token()) location.href='/login'; }
function logout(){ localStorage.removeItem(tokenKey); location.href='/login'; }
async function api(path, options={}){
  options.headers={...(options.headers||{}), ...authHeaders(!(options.body instanceof FormData))};
  const r=await fetch(path, options); let d={}; try{d=await r.json()}catch{}
  if(!r.ok) throw new Error(d.detail||'Request failed'); return d;
}
function money(n,c='INR'){ return new Intl.NumberFormat('en-IN',{style:'currency',currency:c,maximumFractionDigits:0}).format(n); }
function escapeHtml(s){ return String(s??'').replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
function safeUrl(u){ try{const x=new URL(u); return ['https:','http:'].includes(x.protocol)?x.href:'#'}catch{return '#'} }
function renderResult(target,data){
  document.querySelector(target).innerHTML=`<div class="summary"><h3>${escapeHtml(data.summary)}</h3><p>Allocated: <b>${money(data.allocated_total,data.currency)}</b> · Remaining: <b>${money(data.remaining_budget,data.currency)}</b> · Source: <b>${escapeHtml(data.source)}</b></p></div><div class="grid">${data.recommendations.map(r=>`<article class="card"><span class="pill">${escapeHtml(r.category)}</span><h4>${escapeHtml(r.name)}</h4><p>${escapeHtml(r.reason)}</p><strong>${money(r.estimated_price,data.currency)}</strong><p class="muted">${escapeHtml(r.platform)}</p><a href="${safeUrl(r.url)}" target="_blank" rel="noopener">Open platform</a></article>`).join('')}</div><div class="tips"><h4>Planning tips</h4><ul>${(data.tips||[]).map(x=>`<li>${escapeHtml(x)}</li>`).join('')}</ul></div>`;
}
