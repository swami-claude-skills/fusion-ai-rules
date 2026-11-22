/* ---- Fusion AI Rules (site/phase2.js): local-draft marking and "Propose on GitHub" ----
   Edits made on this page stay in the browser. These helpers mark them clearly and turn
   them into a GitHub proposal (an issue on the propose-rule form), the only way a change
   reaches the published rule set. Injected into the page by build/build.py. */
var REPO = '@@REPO@@', PAGES = '@@PAGES@@';
var DFIELDS = [['cat','Category'],['title','Title'],['rule','Rule'],['why','Why'],['good','Good example'],['avoid','Avoid example'],['pri','Priority'],['status','Status']];
function worksStr(r){ return AIS.map(function(a){ var v = (r.works||{})[a[0]]; v = v==null ? 2 : v; return a[2] + ':' + ['no','connected only','yes'][v]; }).join(', '); }
function defRule(id){ return DEF.rules.find(function(x){ return x.id===id; }); }
function ruleDiff(a, b){
  var out = DFIELDS.filter(function(f){ return String(a[f[0]]||'') !== String(b[f[0]]||''); });
  if(worksStr(a) !== worksStr(b)) out.push(['works','Works in']);
  return out;
}
function draftChanges(){
  var res = {added:[], changed:[], deleted:[]};
  if(!edited) return res;
  SET.rules.forEach(function(r){ var d = defRule(r.id); if(!d) res.added.push(r); else if(ruleDiff(d, r).length) res.changed.push([d, r]); });
  DEF.rules.forEach(function(d){ if(!SET.rules.some(function(r){ return r.id===d.id; })) res.deleted.push(d); });
  return res;
}
function draftTag(r){
  if(!edited) return '';
  var d = defRule(r.id);
  if(!d) return '<span class="rc-draft" title="Added in your local draft; not in the published set">local new<\/span>';
  return ruleDiff(d, r).length ? '<span class="rc-draft" title="Changed in your local draft; the published rule differs">local edit<\/span>' : '';
}
function srcLink(r){
  var d = defRule(r.id);
  return d && d.file ? '<a class="rc-src" href="' + REPO + '/blob/main/' + esc(d.file) + '" target="_blank" rel="noopener" title="The published rule file and its history on GitHub">yaml ↗<\/a>' : '';
}
function fieldVal(r, f){ return f==='works' ? worksStr(r) : String(r[f]||'(empty)'); }
function ruleBlock(r){
  return '**' + r.id + ' ' + r.title + '** [' + r.pri + '] (' + r.cat + ', ' + r.status + ')\n' +
    '- Rule: ' + r.rule + '\n' + (r.why ? '- Why: ' + r.why + '\n' : '') + (r.good ? '- Good: ' + r.good + '\n' : '') +
    (r.avoid ? '- Avoid: ' + r.avoid + '\n' : '') + '- Works in: ' + worksStr(r) + '\n';
}
function changeBlock(d, r){
  return '**' + d.id + ' ' + d.title + '**\n' + ruleDiff(d, r).map(function(f){
    return '- ' + f[1] + ':\n  - was: ' + fieldVal(d, f[0]) + '\n  - now: ' + fieldVal(r, f[0]);
  }).join('\n') + '\n';
}
function issueUrl(o){
  var q = new URLSearchParams({template:'propose-rule.yml', title:o.title});
  ['changes','rule','why','good','avoid'].forEach(function(k){ if(o[k]) q.set(k, o[k]); });
  return REPO + '/issues/new?' + q.toString();
}
async function openProposal(o, msgId){
  var url = issueUrl(o), note = '';
  if(url.length > 7500){
    var full = o.rule;
    var ok = await copyText(full);
    o.rule = ok ? 'The full change list is on your clipboard: paste it here, replacing this line.' : 'The change list was too long to pass along. Use Save JSON backup and attach that file here.';
    url = issueUrl(o);
    note = ok ? ' The change list was too long for a link, so it is on your clipboard: paste it into the form.' : '';
  }
  var el = document.getElementById(msgId);
  if(el){ el.innerHTML = 'Your proposal form is ready on GitHub: <a href="' + esc(url) + '" target="_blank" rel="noopener">open the proposal form ↗<\/a>. You need a free GitHub account to submit it.' + esc(note); el.className = 'amr-msg good'; }
  try{ var w = window.open(url, '_blank', 'noopener'); }catch(e){}
}
function proposeAll(msgId){
  var c = draftChanges(), n = c.added.length + c.changed.length + c.deleted.length;
  var el = document.getElementById(msgId);
  if(!n){ if(el){ el.textContent = edited ? 'Your draft matches the published set: nothing to propose.' : 'You have no local edits yet. Edit or add a rule first, or use Propose on GitHub inside a rule\'s editor.'; el.className = 'amr-msg bad'; } return; }
  var s = 'Proposed from the Rule Set page. Based on published v' + DEF.meta.version + '; local draft edited ' + (SET.meta.edited||'') + '.\n\n';
  if(c.changed.length) s += '### Changed (' + c.changed.length + ')\n\n' + c.changed.map(function(p){ return changeBlock(p[0], p[1]); }).join('\n') + '\n';
  if(c.added.length) s += '### New (' + c.added.length + ')\n\n' + c.added.map(ruleBlock).join('\n') + '\n';
  if(c.deleted.length) s += '### Remove (' + c.deleted.length + ')\n\n' + c.deleted.map(function(d){ return '- ' + d.id + ' ' + d.title; }).join('\n') + '\n';
  var ids = c.changed.map(function(p){ return p[0].id; }).concat(c.deleted.map(function(d){ return d.id; }));
  openProposal({title:'Rule proposal: ' + n + ' change' + (n>1?'s':'') + ' from the Rule Set page', changes:ids.join(', '), rule:s,
    why:'See the change list above. (Add a sentence on why, if it is not obvious.)'}, msgId);
}
function proposeFromForm(ov, r, catSel){
  var v = function(s){ return ov.querySelector(s).value.trim(); };
  var nr = {id:r.id, cat: catSel.value==='__new' ? v('#mdCatNew') : catSel.value, title:v('#mdTitle'), rule:v('#mdRule'), why:v('#mdWhy'), good:v('#mdGood'), avoid:v('#mdAvoid'), pri:v('#mdPri'), status:v('#mdSta'), works:{}};
  ov.querySelectorAll('[data-w]').forEach(function(s){ nr.works[s.dataset.w] = +s.value; });
  if(!nr.title || !nr.rule){ ov.querySelector('#mdErr').textContent = 'A title and the rule are needed to propose.'; return; }
  var d = defRule(r.id), diff = d ? ruleDiff(d, nr) : null;
  if(d && !diff.length){ ov.querySelector('#mdErr').textContent = 'This matches the published rule: change something first.'; return; }
  var extra = '\n\nPriority: ' + nr.pri + ' · Category: ' + nr.cat + ' · Works in: ' + worksStr(nr) +
    (d ? '\n\nChanges ' + d.id + ' (published v' + DEF.meta.version + '):\n' + diff.map(function(f){ return '- ' + f[1] + ': was "' + fieldVal(d, f[0]) + '"'; }).join('\n') : '');
  ov.hidden = true; ov.innerHTML = '';
  openProposal({title:'Rule proposal: ' + (d ? 'change ' + d.id + ' ' : '') + nr.title, changes: d ? d.id : '', rule:nr.rule,
    why:(nr.why || '(why it matters)') + extra, good:nr.good, avoid:nr.avoid}, 'amrPropMsg');
  var host = document.getElementById('amrPropMsg'); if(host && window.jumpToEl) setTimeout(function(){ jumpToEl(host); }, 100);
}
(function drawDraftBanner(){
  var el = document.getElementById('amrDraft'); if(!el || !edited) return;
  var c = draftChanges(), n = c.added.length + c.changed.length + c.deleted.length;
  var base = SET.meta.version, cur = DEF.meta.version;
  el.innerHTML = '<p><span class="dr-k">Local draft<\/span><strong>You are viewing your own edited copy of the rules<\/strong>, based on v' + esc(base) +
    (SET.meta.edited ? ' and edited ' + esc(SET.meta.edited) : '') + '. It is saved in this browser only. It is not the published rule set, and nobody else sees it. ' +
    (n ? n + (n>1 ? ' rules differ' : ' rule differs') + ' from the published set (' + [c.changed.length + ' changed', c.added.length + ' new', c.deleted.length + ' removed'].join(', ') + '); they are tagged <span class="rc-draft">local edit<\/span> or <span class="rc-draft">local new<\/span> on the cards.' : 'It matches the published set.') + '<\/p>' +
    (base !== cur ? '<p class="dr-new">The published set is now v' + esc(cur) + '. Propose any changes you want to keep, then discard your draft to see the new rules.<\/p>' : '') +
    '<div class="amr-btns">' + (n ? '<button type="button" class="amr-prim" id="amrDraftPropose">Propose these changes on GitHub<\/button>' : '') +
    '<button type="button" class="amr-danger" id="amrDraftDiscard">Discard my draft<\/button><span class="amr-msg" id="amrDraftMsg"><\/span><\/div>';
  el.hidden = false;
  var p = document.getElementById('amrDraftPropose'); if(p) p.addEventListener('click', function(){ proposeAll('amrDraftMsg'); });
  document.getElementById('amrDraftDiscard').addEventListener('click', function(e){
    var b = e.currentTarget;
    if(!b.dataset.armed){ b.dataset.armed = '1'; b.textContent = 'Click again to discard'; return; }
    ls.del(K_RULES); ls.del(K_SEL); location.reload();
  });
})();
(function(){ var b = document.getElementById('amrPropose'); if(b) b.addEventListener('click', function(){ proposeAll('amrPropMsg'); }); })();
