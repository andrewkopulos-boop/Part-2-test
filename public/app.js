/* ============================================================
   Legal Judge Bot — Frontend Application
   ============================================================ */

const API = '/api';
let lastJudgment = null;
let enumData = {};

// ------------------------------------------------------------------
// Init
// ------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  initFormatToggle();
  await loadEnums();
  addParty('plaintiff');
  addParty('defendant');
  addFact();
  addIssue();
  await loadKnowledge();
});

// ------------------------------------------------------------------
// Tab navigation
// ------------------------------------------------------------------
function initTabs() {
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
      if (btn.dataset.tab === 'history') loadHistory();
    });
  });
}

// ------------------------------------------------------------------
// Format toggle (visual / text / json)
// ------------------------------------------------------------------
function initFormatToggle() {
  document.querySelectorAll('.fmt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.fmt-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const fmt = btn.dataset.fmt;
      document.getElementById('view-visual').style.display = fmt === 'visual' ? '' : 'none';
      document.getElementById('view-text').style.display = fmt === 'text' ? '' : 'none';
      document.getElementById('view-json').style.display = fmt === 'json' ? '' : 'none';
    });
  });
}

// ------------------------------------------------------------------
// Load enums for dynamic selects
// ------------------------------------------------------------------
async function loadEnums() {
  try {
    const resp = await fetch(API + '/enums');
    enumData = await resp.json();
  } catch {
    enumData = {
      case_types: ['civil','criminal','contract','tort','constitutional','administrative','family','property','employment','intellectual_property','corporate','environmental'],
      party_roles: ['plaintiff','defendant','appellant','appellee','petitioner','respondent','prosecutor','intervenor'],
      evidence_types: ['documentary','testimonial','physical','digital','expert_opinion','circumstantial','statistical'],
    };
  }
  const sel = document.getElementById('case-type');
  sel.innerHTML = '';
  (enumData.case_types || []).forEach(t => {
    const opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t.replace(/_/g, ' ');
    sel.appendChild(opt);
  });
}

// ------------------------------------------------------------------
// Dynamic list helpers
// ------------------------------------------------------------------
let listCounters = { party: 0, fact: 0, issue: 0, argument: 0, evidence: 0, statute: 0 };

function removeItem(btn) { btn.closest('.list-item').remove(); }

function addParty(defaultRole) {
  const id = ++listCounters.party;
  const container = document.getElementById('parties-list');
  const roles = enumData.party_roles || ['plaintiff','defendant'];
  const roleOptions = roles.map(r =>
    `<option value="${r}" ${r === defaultRole ? 'selected' : ''}>${r}</option>`
  ).join('');
  container.insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="party-${id}">
      <div class="fields">
        <div class="row">
          <input type="text" placeholder="Party name" class="party-name">
          <select class="party-role">${roleOptions}</select>
        </div>
        <input type="text" placeholder="Description (optional)" class="party-desc">
        <input type="text" placeholder="Counsel (optional)" class="party-counsel">
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

function addFact(value) {
  const id = ++listCounters.fact;
  document.getElementById('facts-list').insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="fact-${id}">
      <div class="fields">
        <input type="text" placeholder="Enter a fact..." class="fact-text" value="${value || ''}">
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

function addIssue(value) {
  const id = ++listCounters.issue;
  document.getElementById('issues-list').insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="issue-${id}">
      <div class="fields">
        <input type="text" placeholder="Enter a legal issue..." class="issue-text" value="${value || ''}">
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

function addArgument(data) {
  const id = ++listCounters.argument;
  document.getElementById('arguments-list').insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="arg-${id}">
      <div class="fields">
        <div class="row">
          <input type="text" placeholder="Party name" class="arg-party" value="${data?.party_name || ''}">
        </div>
        <textarea placeholder="Claim / argument..." class="arg-claim" rows="2">${data?.claim || ''}</textarea>
        <input type="text" placeholder="Supporting facts (comma-separated)" class="arg-facts" value="${(data?.supporting_facts || []).join(', ')}">
        <input type="text" placeholder="Legal basis (comma-separated)" class="arg-basis" value="${(data?.legal_basis || []).join(', ')}">
        <input type="text" placeholder="Cited precedents (comma-separated)" class="arg-prec" value="${(data?.cited_precedents || []).join(', ')}">
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

function addEvidence(data) {
  const id = ++listCounters.evidence;
  const types = enumData.evidence_types || ['documentary','testimonial','physical','digital','expert_opinion'];
  const typeOptions = types.map(t =>
    `<option value="${t}" ${t === (data?.evidence_type || '') ? 'selected' : ''}>${t.replace(/_/g, ' ')}</option>`
  ).join('');
  document.getElementById('evidence-list').insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="ev-${id}">
      <div class="fields">
        <div class="row">
          <input type="text" placeholder="Title" class="ev-title" value="${data?.title || ''}">
          <select class="ev-type">${typeOptions}</select>
        </div>
        <textarea placeholder="Description..." class="ev-desc" rows="2">${data?.description || ''}</textarea>
        <div class="row">
          <input type="text" placeholder="Submitted by" class="ev-by" value="${data?.submitted_by || ''}">
          <input type="number" step="0.05" min="0" max="1" placeholder="Credibility (0-1)" class="ev-cred" value="${data?.credibility_weight ?? 0.5}">
        </div>
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

function addStatute(value) {
  const id = ++listCounters.statute;
  document.getElementById('statutes-list').insertAdjacentHTML('beforeend', `
    <div class="list-item slide-in" data-id="stat-${id}">
      <div class="fields">
        <input type="text" placeholder="e.g. UCC Article 2" class="statute-text" value="${value || ''}">
      </div>
      <button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>
    </div>
  `);
}

// ------------------------------------------------------------------
// Collect form data
// ------------------------------------------------------------------
function collectCase() {
  const parties = [];
  document.querySelectorAll('#parties-list .list-item').forEach(el => {
    const name = el.querySelector('.party-name').value.trim();
    if (!name) return;
    parties.push({
      name,
      role: el.querySelector('.party-role').value,
      description: el.querySelector('.party-desc').value.trim(),
      counsel: el.querySelector('.party-counsel').value.trim(),
    });
  });

  const facts = [];
  document.querySelectorAll('#facts-list .list-item').forEach(el => {
    const v = el.querySelector('.fact-text').value.trim();
    if (v) facts.push(v);
  });

  const issues = [];
  document.querySelectorAll('#issues-list .list-item').forEach(el => {
    const v = el.querySelector('.issue-text').value.trim();
    if (v) issues.push(v);
  });

  const args = [];
  document.querySelectorAll('#arguments-list .list-item').forEach(el => {
    const party = el.querySelector('.arg-party').value.trim();
    const claim = el.querySelector('.arg-claim').value.trim();
    if (!claim) return;
    args.push({
      party_name: party,
      claim,
      supporting_facts: splitCSV(el.querySelector('.arg-facts').value),
      legal_basis: splitCSV(el.querySelector('.arg-basis').value),
      cited_precedents: splitCSV(el.querySelector('.arg-prec').value),
    });
  });

  const evidence = [];
  document.querySelectorAll('#evidence-list .list-item').forEach(el => {
    const title = el.querySelector('.ev-title').value.trim();
    if (!title) return;
    evidence.push({
      title,
      evidence_type: el.querySelector('.ev-type').value,
      description: el.querySelector('.ev-desc').value.trim(),
      submitted_by: el.querySelector('.ev-by').value.trim(),
      credibility_weight: parseFloat(el.querySelector('.ev-cred').value) || 0.5,
    });
  });

  const statutes = [];
  document.querySelectorAll('#statutes-list .list-item').forEach(el => {
    const v = el.querySelector('.statute-text').value.trim();
    if (v) statutes.push(v);
  });

  return {
    case_id: document.getElementById('case-id').value.trim() || 'WEB-' + Date.now(),
    title: document.getElementById('case-title').value.trim(),
    case_type: document.getElementById('case-type').value,
    jurisdiction: document.getElementById('case-jurisdiction').value.trim() || 'General',
    summary: document.getElementById('case-summary').value.trim(),
    parties,
    facts,
    issues,
    arguments: args,
    evidence,
    applicable_statutes: statutes,
  };
}

function splitCSV(s) {
  return s.split(',').map(x => x.trim()).filter(Boolean);
}

// ------------------------------------------------------------------
// Submit case for judgment
// ------------------------------------------------------------------
async function submitCase() {
  const caseData = collectCase();
  if (!caseData.title) {
    alert('Please enter a case title.');
    return;
  }

  // Show loading
  document.getElementById('judgment-empty').style.display = 'none';
  document.getElementById('judgment-result').style.display = 'none';
  document.getElementById('judgment-loading').style.display = '';

  try {
    const resp = await fetch(API + '/judge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!resp.ok) throw new Error(await resp.text());
    const judgment = await resp.json();
    lastJudgment = judgment;
    renderJudgment(judgment);
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    alert('Error: ' + err.message);
  }
}

// ------------------------------------------------------------------
// Render judgment
// ------------------------------------------------------------------
function renderJudgment(j) {
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('judgment-result').style.display = '';
  document.getElementById('format-toggle').style.display = '';

  // Verdict banner
  const banner = document.getElementById('verdict-banner');
  banner.className = 'verdict-banner slide-in ' + dispositionClass(j.disposition);
  document.getElementById('verdict-disposition').textContent = j.disposition.replace(/_/g, ' ');
  document.getElementById('verdict-disposition').style.color = dispositionColor(j.disposition);
  document.getElementById('verdict-meta').innerHTML =
    `<strong>${j.case_title}</strong> &mdash; ${j.date_decided}<br>` +
    `Prevailing party: <strong>${j.prevailing_party}</strong>` +
    (j.remedy !== 'none' ? ` &bull; Remedy: ${j.remedy.replace(/_/g, ' ')}` : '');

  // Score cards
  const cards = document.getElementById('score-cards');
  cards.innerHTML = '';
  const metrics = [
    { label: 'Confidence', value: (j.confidence * 100).toFixed(0) + '%', pct: j.confidence, color: confidenceColor(j.confidence) },
    { label: 'Evidence Strength', value: (j.strength_of_evidence * 100).toFixed(0) + '%', pct: j.strength_of_evidence, color: confidenceColor(j.strength_of_evidence) },
    { label: 'Issues Analyzed', value: j.issues_addressed.length, pct: Math.min(j.issues_addressed.length / 5, 1), color: 'var(--blue)' },
    { label: 'Rules Applied', value: j.rules_applied.length, pct: Math.min(j.rules_applied.length / 8, 1), color: 'var(--gold)' },
  ];
  metrics.forEach(m => {
    cards.innerHTML += `
      <div class="score-card slide-in">
        <div class="score-label">${m.label}</div>
        <div class="score-value" style="color:${m.color}">${m.value}</div>
        <div class="score-bar">
          <div class="score-bar-fill" style="width:${m.pct * 100}%;background:${m.color}"></div>
        </div>
      </div>
    `;
  });

  // Sections
  const sectionsEl = document.getElementById('opinion-sections');
  sectionsEl.innerHTML = '';
  j.sections.forEach((sec, i) => {
    const isAnalysis = sec.heading.includes('Analysis');
    sectionsEl.innerHTML += `
      <div class="opinion-section slide-in">
        <div class="section-header${i < 3 ? ' open' : ''}" onclick="toggleSection(this)">
          <h3>${sec.heading}</h3>
          <span class="section-chevron">${i < 3 ? '&#9650;' : '&#9660;'}</span>
        </div>
        <div class="section-content${i < 3 ? ' open' : ''}">${escapeHtml(sec.content)}</div>
      </div>
    `;
  });

  // Dissent
  const dissentEl = document.getElementById('dissent-section');
  if (j.dissent) {
    dissentEl.style.display = '';
    dissentEl.innerHTML = `
      <div class="dissent-header" onclick="toggleDissent()">
        Dissenting Opinion
        <span class="section-chevron" id="dissent-chevron">&#9660;</span>
      </div>
      <div class="dissent-content" id="dissent-body">${escapeHtml(j.dissent)}</div>
    `;
  } else {
    dissentEl.style.display = 'none';
  }

  // Text view
  document.getElementById('opinion-text-content').textContent = j.opinion_text;

  // JSON view
  document.getElementById('opinion-json-content').textContent = JSON.stringify(j, null, 2);
}

function toggleSection(header) {
  header.classList.toggle('open');
  header.nextElementSibling.classList.toggle('open');
  const chev = header.querySelector('.section-chevron');
  chev.innerHTML = header.classList.contains('open') ? '&#9650;' : '&#9660;';
}

function toggleDissent() {
  const body = document.getElementById('dissent-body');
  body.classList.toggle('open');
  const chev = document.getElementById('dissent-chevron');
  chev.innerHTML = body.classList.contains('open') ? '&#9650;' : '&#9660;';
}

function dispositionClass(d) {
  if (d === 'granted') return 'granted';
  if (d === 'denied') return 'denied';
  if (d === 'granted_in_part') return 'partial';
  if (d === 'dismissed') return 'dismissed';
  if (d === 'guilty') return 'guilty';
  if (d === 'not_guilty') return 'not-guilty';
  return '';
}

function dispositionColor(d) {
  if (d === 'granted' || d === 'not_guilty') return 'var(--green)';
  if (d === 'denied' || d === 'guilty') return 'var(--red)';
  if (d === 'granted_in_part') return 'var(--amber)';
  return 'var(--text-muted)';
}

function confidenceColor(v) {
  if (v >= 0.7) return 'var(--green)';
  if (v >= 0.5) return 'var(--amber)';
  return 'var(--red)';
}

function escapeHtml(s) {
  const div = document.createElement('div');
  div.textContent = s;
  return div.innerHTML;
}

// ------------------------------------------------------------------
// Load demo cases
// ------------------------------------------------------------------
async function loadDemo(name) {
  try {
    const resp = await fetch(API + '/demo/' + name);
    const data = await resp.json();
    populateForm(data);
  } catch (err) {
    alert('Failed to load demo: ' + err.message);
  }
}

function populateForm(c) {
  clearForm();
  document.getElementById('case-id').value = c.case_id || '';
  document.getElementById('case-title').value = c.title || '';
  document.getElementById('case-type').value = c.case_type || 'civil';
  document.getElementById('case-jurisdiction').value = c.jurisdiction || 'General';
  document.getElementById('case-summary').value = c.summary || '';

  (c.parties || []).forEach(p => {
    addParty(p.role);
    const items = document.querySelectorAll('#parties-list .list-item');
    const last = items[items.length - 1];
    last.querySelector('.party-name').value = p.name || '';
    last.querySelector('.party-role').value = p.role || 'plaintiff';
    last.querySelector('.party-desc').value = p.description || '';
    last.querySelector('.party-counsel').value = p.counsel || '';
  });

  (c.facts || []).forEach(f => addFact(f));
  (c.issues || []).forEach(i => addIssue(i));
  (c.arguments || []).forEach(a => addArgument(a));
  (c.evidence || []).forEach(e => addEvidence(e));
  (c.applicable_statutes || []).forEach(s => addStatute(s));
}

function clearForm() {
  document.getElementById('case-form').reset();
  ['parties-list','facts-list','issues-list','arguments-list','evidence-list','statutes-list'].forEach(id => {
    document.getElementById(id).innerHTML = '';
  });
  document.getElementById('judgment-empty').style.display = '';
  document.getElementById('judgment-result').style.display = 'none';
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('format-toggle').style.display = 'none';
}

// ------------------------------------------------------------------
// Knowledge Base
// ------------------------------------------------------------------
async function loadKnowledge() {
  try {
    const resp = await fetch(API + '/knowledge');
    const kb = await resp.json();
    renderKnowledge(kb);
  } catch { /* ignore on load failure */ }
}

function renderKnowledge(kb) {
  // Stats
  document.getElementById('kb-stats').innerHTML = `
    <div class="kb-stat-card slide-in"><div class="kb-stat-number">${kb.statutes}</div><div class="kb-stat-label">Statutes</div></div>
    <div class="kb-stat-card slide-in"><div class="kb-stat-number">${kb.precedents}</div><div class="kb-stat-label">Precedents</div></div>
    <div class="kb-stat-card slide-in"><div class="kb-stat-number">${kb.principles}</div><div class="kb-stat-label">Principles</div></div>
    <div class="kb-stat-card slide-in"><div class="kb-stat-number">${kb.domains.length}</div><div class="kb-stat-label">Domains</div></div>
  `;

  // Precedents
  const precEl = document.getElementById('precedents-list-kb');
  precEl.innerHTML = '';
  (kb.precedents_list || []).forEach(p => {
    precEl.innerHTML += `
      <div class="kb-item">
        <div class="kb-item-title">${p.case_name} <span class="kb-item-badge">${p.domain.replace(/_/g, ' ')}</span></div>
        <div class="kb-item-meta">${p.citation} (${p.year}) &bull; Authority: ${(p.authority_weight * 100).toFixed(0)}%</div>
        <div class="kb-item-body">${p.holding}</div>
      </div>
    `;
  });

  // Statutes
  const statEl = document.getElementById('statutes-list-kb');
  statEl.innerHTML = '';
  (kb.statutes_list || []).forEach(s => {
    statEl.innerHTML += `
      <div class="kb-item">
        <div class="kb-item-title">${s.name} <span class="kb-item-badge">${s.domain.replace(/_/g, ' ')}</span></div>
        <div class="kb-item-meta">${s.code}</div>
        <div class="kb-item-body">${s.summary}</div>
      </div>
    `;
  });

  // Principles
  const prinEl = document.getElementById('principles-list-kb');
  prinEl.innerHTML = '';
  (kb.principles_list || []).forEach(p => {
    prinEl.innerHTML += `
      <div class="kb-item">
        <div class="kb-item-title">${p.name}${p.latin_name ? ' (' + p.latin_name + ')' : ''} <span class="kb-item-badge">${p.domain.replace(/_/g, ' ')}</span></div>
        <div class="kb-item-body">${p.description}</div>
        ${p.elements.length ? '<div class="kb-item-meta">Elements: ' + p.elements.join(', ') + '</div>' : ''}
      </div>
    `;
  });
}

async function searchPrecedents() {
  const query = document.getElementById('prec-search').value.trim();
  if (!query) return;
  try {
    const resp = await fetch(API + '/precedents/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    const data = await resp.json();
    const el = document.getElementById('precedents-results');
    if (!data.results.length) {
      el.innerHTML = '<p style="color:var(--text-muted);padding:0.5rem;">No matching precedents found.</p>';
      return;
    }
    el.innerHTML = '<p style="color:var(--gold);font-size:0.8rem;margin-bottom:0.5rem;">Search results:</p>';
    data.results.forEach(r => {
      el.innerHTML += `
        <div class="kb-item slide-in">
          <div class="kb-item-title">${r.case_name} <span class="kb-item-badge">${r.domain.replace(/_/g, ' ')}</span></div>
          <div class="kb-item-meta">${r.citation} (${r.year}) &bull; Authority: ${(r.authority_weight * 100).toFixed(0)}% &bull; Matched: ${r.matched_terms.join(', ')}</div>
          <div class="kb-item-body">${r.holding}</div>
        </div>
      `;
    });
  } catch { /* ignore */ }
}

// ------------------------------------------------------------------
// History
// ------------------------------------------------------------------
async function loadHistory() {
  try {
    const resp = await fetch(API + '/history');
    const data = await resp.json();
    const el = document.getElementById('history-list');
    if (!data.cases.length) {
      el.innerHTML = '<p style="color:var(--text-muted);">No cases judged yet. Submit a case to see it here.</p>';
      return;
    }
    el.innerHTML = '';
    data.cases.forEach(c => {
      el.innerHTML += `
        <div class="history-card slide-in">
          <div class="history-card-left">
            <h3>${c.title}</h3>
            <p>${c.case_id} &bull; Prevailing: ${c.prevailing_party}</p>
          </div>
          <div class="history-card-right">
            <span class="disp-badge ${dispositionClass(c.disposition)}">${c.disposition.replace(/_/g, ' ')}</span>
            <p style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">Confidence: ${(c.confidence * 100).toFixed(0)}%</p>
          </div>
        </div>
      `;
    });
  } catch { /* ignore */ }
}

// ------------------------------------------------------------------
// View management helpers
// ------------------------------------------------------------------
function showView(viewId) {
  ['view-visual','view-text','view-json','view-panel','view-risk','view-settlement'].forEach(id => {
    document.getElementById(id).style.display = 'none';
  });
  document.getElementById(viewId).style.display = '';
  document.getElementById('judgment-empty').style.display = 'none';
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('judgment-result').style.display = '';
  document.getElementById('format-toggle').style.display = 'none';
}

function showLoading(msg) {
  document.getElementById('judgment-empty').style.display = 'none';
  document.getElementById('judgment-result').style.display = 'none';
  document.getElementById('judgment-loading').style.display = '';
  document.querySelector('.loading-text').textContent = msg || 'Analyzing case...';
}

// ------------------------------------------------------------------
// 3-Judge Panel
// ------------------------------------------------------------------
async function submitPanel() {
  const caseData = collectCase();
  if (!caseData.title) { alert('Please enter a case title.'); return; }
  showLoading('Convening 3-judge panel...');

  try {
    const resp = await fetch(API + '/panel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!resp.ok) throw new Error(await resp.text());
    const result = await resp.json();
    renderPanel(result);
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    alert('Panel error: ' + err.message);
  }
}

function renderPanel(result) {
  showView('view-panel');
  const el = document.getElementById('panel-result');

  const unanimous = result.is_unanimous;
  const bannerClass = unanimous ? 'unanimous' : 'split';

  let html = `
    <div class="panel-vote-banner ${bannerClass}">
      <div class="panel-vote-label">${unanimous ? 'UNANIMOUS' : 'SPLIT'} DECISION</div>
      <div class="panel-vote-disp">${result.majority_disposition.replace(/_/g, ' ').toUpperCase()}</div>
      <div class="panel-vote-count">${result.majority_vote} of ${result.panel_size} judges</div>
      <div style="font-size:0.85rem;margin-top:0.5rem;color:var(--text-muted);">
        Confidence: ${(result.majority_confidence * 100).toFixed(0)}%
      </div>
    </div>
    <div style="padding:1rem 0;">
      <h3 style="color:var(--gold);margin-bottom:0.5rem;">Majority Opinion</h3>
      <p style="color:var(--text-secondary);line-height:1.6;">${escapeHtml(result.majority_opinion)}</p>
    </div>
    <div class="judge-cards">
  `;

  (result.opinions || []).forEach(op => {
    const isMajority = op.in_majority;
    const cardClass = isMajority ? 'majority' : 'dissent';
    html += `
      <div class="judge-card ${cardClass}">
        <div class="judge-name">${escapeHtml(op.judge_name)}</div>
        <div class="judge-philosophy">${escapeHtml(op.philosophy)}</div>
        <div class="judge-disposition" style="color:${dispositionColor(op.disposition)}">${op.disposition.replace(/_/g, ' ')}</div>
        <div class="judge-conf">Confidence: ${(op.confidence * 100).toFixed(0)}%</div>
        <div class="judge-role">${isMajority ? 'MAJORITY' : 'DISSENT'}</div>
        <div class="judge-reasoning">${escapeHtml(op.reasoning)}</div>
      </div>
    `;
  });

  html += '</div>';

  if (result.judgment) {
    lastJudgment = result.judgment;
    html += `
      <div style="text-align:center;margin-top:1.5rem;">
        <button class="btn btn-sm btn-outline" onclick="renderJudgment(lastJudgment);document.getElementById('format-toggle').style.display='';showView('view-visual');">
          View Full Majority Opinion
        </button>
      </div>
    `;
  }

  el.innerHTML = html;
}

// ------------------------------------------------------------------
// Risk Assessment
// ------------------------------------------------------------------
async function runRiskAssessment() {
  const caseData = collectCase();
  if (!caseData.title) { alert('Please enter a case title.'); return; }
  showLoading('Assessing litigation risk...');

  try {
    const resp = await fetch(API + '/risk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: caseData }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    const result = await resp.json();
    renderRisk(result);
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    alert('Risk error: ' + err.message);
  }
}

function renderRisk(result) {
  showView('view-risk');
  const el = document.getElementById('risk-result');

  const riskColor = {
    low: 'var(--green)', moderate: 'var(--amber)', high: 'var(--red)', very_low: 'var(--green)', extreme: 'var(--red)',
  }[result.litigation_risk_level] || 'var(--text-muted)';

  let html = `
    <div class="risk-header">
      <div>
        <div class="risk-level" style="color:${riskColor}">${result.litigation_risk_level.replace(/_/g, ' ').toUpperCase()} RISK</div>
        <div class="risk-title">${escapeHtml(result.case_title)}</div>
      </div>
    </div>
    <div style="padding:0.75rem 0;color:var(--text-secondary);line-height:1.6;font-size:0.9rem;">
      ${escapeHtml(result.recommendation)}
    </div>
    <div class="party-risk-cards">
  `;

  (result.parties || []).forEach(p => {
    const probPct = (p.win_probability * 100).toFixed(0);
    const gradeColorMap = { A: '#22c55e', B: '#84cc16', C: '#eab308', D: '#f97316', F: '#ef4444' };
    const gc = gradeColorMap[p.overall_grade] || '#888';

    html += `
      <div class="party-risk-card slide-in">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">
          <div>
            <div class="party-risk-name">${escapeHtml(p.party_name)}</div>
            <div class="party-risk-role">${p.role}</div>
          </div>
          <div class="grade-badge" style="background:${gc}">${p.overall_grade}</div>
        </div>
        <div style="margin-bottom:0.5rem;">
          <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.25rem;">
            <span>Win Probability</span><span style="color:var(--gold)">${probPct}%</span>
          </div>
          <div class="prob-bar"><div class="prob-bar-fill" style="width:${probPct}%"></div></div>
        </div>
        <div style="display:flex;gap:0.5rem;margin-bottom:0.5rem;">
          <div style="flex:1;">
            <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.25rem;">Evidence</div>
            <div class="prob-bar"><div class="prob-bar-fill" style="width:${(p.evidence_score * 100).toFixed(0)}%;background:var(--blue)"></div></div>
          </div>
          <div style="flex:1;">
            <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.25rem;">Arguments</div>
            <div class="prob-bar"><div class="prob-bar-fill" style="width:${(p.argument_score * 100).toFixed(0)}%;background:var(--purple, #a855f7)"></div></div>
          </div>
        </div>
    `;

    if (p.strengths.length) {
      html += '<div class="sw-list strengths"><div class="sw-label">Strengths</div>';
      p.strengths.forEach(s => { html += `<div class="sw-item">+ ${escapeHtml(s)}</div>`; });
      html += '</div>';
    }
    if (p.weaknesses.length) {
      html += '<div class="sw-list weaknesses"><div class="sw-label">Weaknesses</div>';
      p.weaknesses.forEach(w => { html += `<div class="sw-item">- ${escapeHtml(w)}</div>`; });
      html += '</div>';
    }
    if (p.risk_factors.length) {
      html += '<div class="sw-list risks"><div class="sw-label">Risk Factors</div>';
      p.risk_factors.forEach(r => { html += `<div class="sw-item">! ${escapeHtml(r)}</div>`; });
      html += '</div>';
    }

    html += '</div>';
  });

  html += '</div>';
  el.innerHTML = html;
}

// ------------------------------------------------------------------
// Settlement Calculator
// ------------------------------------------------------------------
async function runSettlement() {
  const caseData = collectCase();
  if (!caseData.title) { alert('Please enter a case title.'); return; }

  const claimedStr = prompt('Enter claimed damages amount (USD). Leave blank for auto-estimate:', '');
  const claimed = parseFloat(claimedStr) || 0;

  showLoading('Calculating settlement...');

  try {
    const resp = await fetch(API + '/settlement', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: caseData, claimed_damages: claimed }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    const result = await resp.json();
    renderSettlement(result);
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    alert('Settlement error: ' + err.message);
  }
}

function fmtMoney(n) {
  if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
  if (n >= 1e3) return '$' + (n / 1e3).toFixed(1) + 'K';
  return '$' + n.toFixed(0);
}

function renderSettlement(result) {
  showView('view-settlement');
  const el = document.getElementById('settlement-result');

  const s = result.settlement_range;
  const d = result.damages_estimate;
  const shouldSettle = result.should_settle;

  let html = `
    <div class="settlement-header" style="text-align:center;padding:1.5rem 0;">
      <div style="font-size:0.85rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;">Settlement Recommendation</div>
      <div style="font-size:1.8rem;font-weight:700;color:${shouldSettle ? 'var(--green)' : 'var(--red)'};margin:0.5rem 0;">
        ${shouldSettle ? 'SETTLE' : 'LITIGATE'}
      </div>
      <div style="color:var(--text-secondary);font-size:0.9rem;max-width:600px;margin:0 auto;">${escapeHtml(result.settlement_recommendation)}</div>
    </div>

    <div class="settlement-grid">
      <div class="settlement-card">
        <div class="settlement-card-label">Estimated Total Damages</div>
        <div class="money-big">${fmtMoney(d.total)}</div>
        <div class="money-row"><span>Compensatory</span><span>${fmtMoney(d.compensatory)}</span></div>
        <div class="money-row"><span>Consequential</span><span>${fmtMoney(d.consequential)}</span></div>
        <div class="money-row"><span>Punitive</span><span>${fmtMoney(d.punitive)}</span></div>
        <div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted);">
          Confidence: ${(d.confidence * 100).toFixed(0)}% &bull; ${escapeHtml(d.basis)}
        </div>
      </div>

      <div class="settlement-card">
        <div class="settlement-card-label">Settlement Range</div>
        <div class="money-big" style="color:var(--green)">${fmtMoney(s.recommended)}</div>
        <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.75rem;">Recommended</div>
        <div class="settlement-range-bar">
          <div class="range-fill" style="left:0%;width:100%"></div>
          ${s.high > 0 ? `<div class="range-marker" style="left:${((s.recommended - s.low) / (s.high - s.low) * 100).toFixed(1)}%"></div>` : ''}
        </div>
        <div class="money-row"><span>Low</span><span>${fmtMoney(s.low)}</span></div>
        <div class="money-row"><span>Midpoint</span><span>${fmtMoney(s.midpoint)}</span></div>
        <div class="money-row"><span>High</span><span>${fmtMoney(s.high)}</span></div>
        <div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted);">${escapeHtml(s.rationale)}</div>
      </div>

      <div class="settlement-card">
        <div class="settlement-card-label">Litigation Cost Estimate</div>
        <div class="money-big" style="color:var(--red)">${fmtMoney(result.cost_of_litigation_estimate)}</div>
        <div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.75rem;">Estimated total cost to litigate</div>
        <div class="settlement-card-label" style="margin-top:1rem;">Risk Summary</div>
        ${(result.risk_summary.parties || []).map(p => `
          <div class="money-row">
            <span>${escapeHtml(p.party_name)} (${p.overall_grade})</span>
            <span>${(p.win_probability * 100).toFixed(0)}%</span>
          </div>
        `).join('')}
      </div>
    </div>
  `;

  el.innerHTML = html;
}
