/* ============================================================
   Legal Judge Bot — Frontend Application (Complete)
   ============================================================ */

const API = '/api';
let lastJudgment = null;
let lastPanel = null;
let lastRisk = null;
let lastSettlement = null;
let enumData = {};
let knowledgeData = null;
let activeKBDomain = 'all';
let llmAvailable = false;
let llmProvider = '';
let lastCaseData = null;

// ============================================================
// 1. INITIALIZATION
// ============================================================
// Loading phase messages
var loadingPhases = [
  'Parsing case materials...',
  'Applying IRAC framework...',
  'Matching relevant precedents...',
  'Weighing evidence...',
  'Consulting legal principles...',
  'Drafting opinion...',
  'Finalizing judgment...'
];
var loadingPhaseInterval = null;

document.addEventListener('DOMContentLoaded', async () => {
  initTabs();
  initFormatToggle();
  initResultTabs();
  initKeyboardShortcuts();
  initParticles();
  initTabIndicator();
  await loadEnums();
  addParty('plaintiff');
  addParty('defendant');
  addFact();
  addIssue();
  updateFieldsetCounts();
  await loadKnowledge();
  await checkLLMStatus();
});

// ============================================================
// 2. TOAST NOTIFICATION SYSTEM
// ============================================================
function showToast(message, type, duration) {
  type = type || 'info';
  duration = duration || 4000;
  var container = document.getElementById('toast-container');
  var toast = document.createElement('div');
  toast.className = 'toast toast-' + type;
  toast.innerHTML =
    '<span class="toast-msg">' + escapeHtml(message) + '</span>' +
    '<button class="toast-close" onclick="this.parentElement.remove()">&times;</button>';
  container.appendChild(toast);
  // Trigger slide-in
  requestAnimationFrame(function() {
    toast.classList.add('toast-visible');
  });
  setTimeout(function() {
    toast.classList.remove('toast-visible');
    toast.classList.add('toast-exit');
    setTimeout(function() { toast.remove(); }, 400);
  }, duration);
}

// ============================================================
// 3. MODAL SYSTEM
// ============================================================
function openModal(title, bodyHTML, footerHTML) {
  document.getElementById('modal-title').textContent = title;
  document.getElementById('modal-body').innerHTML = bodyHTML;
  var footer = document.getElementById('modal-footer');
  if (footerHTML) {
    footer.innerHTML = footerHTML;
    footer.style.display = '';
  } else {
    footer.innerHTML = '';
    footer.style.display = 'none';
  }
  document.getElementById('modal-overlay').classList.add('modal-open');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('modal-open');
}

function handleModalOverlayClick(event) {
  if (event.target === document.getElementById('modal-overlay')) {
    closeModal();
  }
}

// ============================================================
// 4. ESCAPE HTML & FORMAT HELPERS
// ============================================================
function escapeHtml(s) {
  if (!s) return '';
  var div = document.createElement('div');
  div.textContent = String(s);
  return div.innerHTML;
}

function fmtMoney(n) {
  if (n == null || isNaN(n)) return '$0';
  if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
  if (n >= 1e3) return '$' + (n / 1e3).toFixed(1) + 'K';
  return '$' + n.toFixed(0);
}

function splitCSV(s) {
  return s.split(',').map(function(x) { return x.trim(); }).filter(Boolean);
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

// ============================================================
// 5. ANIMATED CONFIDENCE RING (SVG)
// ============================================================
function renderConfidenceRing(pct, color, size) {
  size = size || 54;
  var r = (size - 6) / 2;
  var circ = 2 * Math.PI * r;
  var offset = circ * (1 - pct);
  return '<svg class="conf-ring" width="' + size + '" height="' + size + '" viewBox="0 0 ' + size + ' ' + size + '">' +
    '<circle cx="' + (size / 2) + '" cy="' + (size / 2) + '" r="' + r + '" fill="none" stroke="var(--border)" stroke-width="4"/>' +
    '<circle class="conf-ring-fill" cx="' + (size / 2) + '" cy="' + (size / 2) + '" r="' + r + '" fill="none" stroke="' + color + '" stroke-width="4" ' +
    'stroke-dasharray="' + circ + '" stroke-dashoffset="' + circ + '" data-target="' + offset + '" ' +
    'stroke-linecap="round" transform="rotate(-90 ' + (size / 2) + ' ' + (size / 2) + ')"/>' +
    '</svg>';
}

function animateConfidenceRings() {
  setTimeout(function() {
    document.querySelectorAll('.conf-ring-fill').forEach(function(el) {
      el.style.transition = 'stroke-dashoffset 0.8s ease-out';
      el.style.strokeDashoffset = el.getAttribute('data-target');
    });
  }, 50);
}

// ============================================================
// 6. TAB NAVIGATION
// ============================================================
function initTabs() {
  document.querySelectorAll('.nav-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
      document.querySelectorAll('.tab-panel').forEach(function(p) { p.classList.remove('active'); });
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
      updateTabIndicator();
      if (btn.dataset.tab === 'history') loadHistory();
    });
  });
  window.addEventListener('resize', updateTabIndicator);
}

// ============================================================
// 7. FORMAT TOGGLE (Visual / Text / JSON)
// ============================================================
function initFormatToggle() {
  document.querySelectorAll('.fmt-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.fmt-btn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var fmt = btn.dataset.fmt;
      document.getElementById('view-judgment').style.display = fmt === 'visual' ? '' : 'none';
      document.getElementById('view-text').style.display = fmt === 'text' ? '' : 'none';
      document.getElementById('view-json').style.display = fmt === 'json' ? '' : 'none';
    });
  });
}

// ============================================================
// 8. RESULT TABS (Judgment / Panel / Risk / Settlement)
// ============================================================
function initResultTabs() {
  // Result tabs are handled via onclick in HTML, calling switchResultTab
}

function switchResultTab(btn) {
  var view = btn.dataset.view;
  // Highlight active tab
  document.querySelectorAll('.result-tab').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  // Hide all result views
  var views = ['view-judgment', 'view-text', 'view-json', 'view-panel', 'view-risk', 'view-settlement'];
  views.forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  // Show the selected view
  var formatToggle = document.getElementById('format-toggle');
  if (view === 'judgment') {
    // Show format toggle for judgment view
    formatToggle.style.display = '';
    // Show whichever format sub-view is active
    var activeFmt = document.querySelector('.fmt-btn.active');
    var fmt = activeFmt ? activeFmt.dataset.fmt : 'visual';
    if (fmt === 'visual') document.getElementById('view-judgment').style.display = '';
    else if (fmt === 'text') document.getElementById('view-text').style.display = '';
    else if (fmt === 'json') document.getElementById('view-json').style.display = '';
  } else {
    formatToggle.style.display = 'none';
    document.getElementById('view-' + view).style.display = '';
  }
}

function showResultTabs() {
  var tabsEl = document.getElementById('result-tabs');
  tabsEl.style.display = '';
  // Highlight tabs that have data
  tabsEl.querySelectorAll('.result-tab').forEach(function(btn) {
    var view = btn.dataset.view;
    var hasData = false;
    if (view === 'judgment') hasData = !!lastJudgment;
    if (view === 'panel') hasData = !!lastPanel;
    if (view === 'risk') hasData = !!lastRisk;
    if (view === 'settlement') hasData = !!lastSettlement;
    btn.classList.toggle('has-data', hasData);
  });
}

// ============================================================
// 9. COLLAPSIBLE FIELDSETS
// ============================================================
function toggleFieldset(legendEl) {
  var fieldset = legendEl.closest('.fieldset');
  var body = fieldset.querySelector('.fieldset-body');
  var chevron = legendEl.querySelector('.fieldset-chevron');
  var isOpen = fieldset.classList.contains('open');
  if (isOpen) {
    fieldset.classList.remove('open');
    body.style.display = 'none';
    chevron.innerHTML = '&#9654;'; // right arrow
  } else {
    fieldset.classList.add('open');
    body.style.display = '';
    chevron.innerHTML = '&#9660;'; // down arrow
  }
}

function updateFieldsetCounts() {
  var argCount = document.querySelectorAll('#arguments-list .list-item').length;
  var evCount = document.querySelectorAll('#evidence-list .list-item').length;
  var statCount = document.querySelectorAll('#statutes-list .list-item').length;
  document.getElementById('arg-count').textContent = argCount;
  document.getElementById('ev-count').textContent = evCount;
  document.getElementById('stat-count').textContent = statCount;
}

// ============================================================
// 10. KEYBOARD SHORTCUTS
// ============================================================
function initKeyboardShortcuts() {
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      submitCase();
    }
    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

// ============================================================
// 11. LOAD ENUMS
// ============================================================
async function loadEnums() {
  try {
    var resp = await fetch(API + '/enums');
    enumData = await resp.json();
  } catch (err) {
    enumData = {
      case_types: ['civil','criminal','contract','tort','constitutional','administrative','family','property','employment','intellectual_property','corporate','environmental'],
      party_roles: ['plaintiff','defendant','appellant','appellee','petitioner','respondent','prosecutor','intervenor'],
      evidence_types: ['documentary','testimonial','physical','digital','expert_opinion','circumstantial','statistical'],
    };
  }
  var sel = document.getElementById('case-type');
  sel.innerHTML = '';
  (enumData.case_types || []).forEach(function(t) {
    var opt = document.createElement('option');
    opt.value = t;
    opt.textContent = t.replace(/_/g, ' ');
    sel.appendChild(opt);
  });
}

// ============================================================
// 12. DYNAMIC LIST HELPERS
// ============================================================
var listCounters = { party: 0, fact: 0, issue: 0, argument: 0, evidence: 0, statute: 0 };

function removeItem(btn) {
  btn.closest('.list-item').remove();
  updateFieldsetCounts();
}

function addParty(defaultRole) {
  var id = ++listCounters.party;
  var container = document.getElementById('parties-list');
  var roles = enumData.party_roles || ['plaintiff','defendant'];
  var roleOptions = roles.map(function(r) {
    return '<option value="' + r + '"' + (r === defaultRole ? ' selected' : '') + '>' + r + '</option>';
  }).join('');
  container.insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="party-' + id + '">' +
      '<div class="fields">' +
        '<div class="row">' +
          '<input type="text" placeholder="Party name" class="party-name">' +
          '<select class="party-role">' + roleOptions + '</select>' +
        '</div>' +
        '<input type="text" placeholder="Description (optional)" class="party-desc">' +
        '<input type="text" placeholder="Counsel (optional)" class="party-counsel">' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
}

function addFact(value) {
  var id = ++listCounters.fact;
  document.getElementById('facts-list').insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="fact-' + id + '">' +
      '<div class="fields">' +
        '<input type="text" placeholder="Enter a fact..." class="fact-text" value="' + escapeHtml(value || '') + '">' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
}

function addIssue(value) {
  var id = ++listCounters.issue;
  document.getElementById('issues-list').insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="issue-' + id + '">' +
      '<div class="fields">' +
        '<input type="text" placeholder="Enter a legal issue..." class="issue-text" value="' + escapeHtml(value || '') + '">' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
}

function addArgument(data) {
  var id = ++listCounters.argument;
  var partyName = (data && data.party_name) ? escapeHtml(data.party_name) : '';
  var claim = (data && data.claim) ? escapeHtml(data.claim) : '';
  var facts = (data && data.supporting_facts) ? data.supporting_facts.join(', ') : '';
  var basis = (data && data.legal_basis) ? data.legal_basis.join(', ') : '';
  var prec = (data && data.cited_precedents) ? data.cited_precedents.join(', ') : '';
  document.getElementById('arguments-list').insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="arg-' + id + '">' +
      '<div class="fields">' +
        '<div class="row">' +
          '<input type="text" placeholder="Party name" class="arg-party" value="' + partyName + '">' +
        '</div>' +
        '<textarea placeholder="Claim / argument..." class="arg-claim" rows="2">' + claim + '</textarea>' +
        '<input type="text" placeholder="Supporting facts (comma-separated)" class="arg-facts" value="' + escapeHtml(facts) + '">' +
        '<input type="text" placeholder="Legal basis (comma-separated)" class="arg-basis" value="' + escapeHtml(basis) + '">' +
        '<input type="text" placeholder="Cited precedents (comma-separated)" class="arg-prec" value="' + escapeHtml(prec) + '">' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
  updateFieldsetCounts();
}

function addEvidence(data) {
  var id = ++listCounters.evidence;
  var types = enumData.evidence_types || ['documentary','testimonial','physical','digital','expert_opinion'];
  var selType = (data && data.evidence_type) ? data.evidence_type : '';
  var typeOptions = types.map(function(t) {
    return '<option value="' + t + '"' + (t === selType ? ' selected' : '') + '>' + t.replace(/_/g, ' ') + '</option>';
  }).join('');
  var title = (data && data.title) ? escapeHtml(data.title) : '';
  var desc = (data && data.description) ? escapeHtml(data.description) : '';
  var by = (data && data.submitted_by) ? escapeHtml(data.submitted_by) : '';
  var cred = (data && data.credibility_weight != null) ? data.credibility_weight : 0.5;
  document.getElementById('evidence-list').insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="ev-' + id + '">' +
      '<div class="fields">' +
        '<div class="row">' +
          '<input type="text" placeholder="Title" class="ev-title" value="' + title + '">' +
          '<select class="ev-type">' + typeOptions + '</select>' +
        '</div>' +
        '<textarea placeholder="Description..." class="ev-desc" rows="2">' + desc + '</textarea>' +
        '<div class="row">' +
          '<input type="text" placeholder="Submitted by" class="ev-by" value="' + by + '">' +
          '<input type="number" step="0.05" min="0" max="1" placeholder="Credibility (0-1)" class="ev-cred" value="' + cred + '">' +
        '</div>' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
  updateFieldsetCounts();
}

function addStatute(value) {
  var id = ++listCounters.statute;
  document.getElementById('statutes-list').insertAdjacentHTML('beforeend',
    '<div class="list-item slide-in" data-id="stat-' + id + '">' +
      '<div class="fields">' +
        '<input type="text" placeholder="e.g. UCC Article 2" class="statute-text" value="' + escapeHtml(value || '') + '">' +
      '</div>' +
      '<button class="remove-btn" onclick="removeItem(this)" title="Remove">&times;</button>' +
    '</div>'
  );
  updateFieldsetCounts();
}

// ============================================================
// 13. COLLECT FORM DATA
// ============================================================
function collectCase() {
  var parties = [];
  document.querySelectorAll('#parties-list .list-item').forEach(function(el) {
    var name = el.querySelector('.party-name').value.trim();
    if (!name) return;
    parties.push({
      name: name,
      role: el.querySelector('.party-role').value,
      description: el.querySelector('.party-desc').value.trim(),
      counsel: el.querySelector('.party-counsel').value.trim(),
    });
  });

  var facts = [];
  document.querySelectorAll('#facts-list .list-item').forEach(function(el) {
    var v = el.querySelector('.fact-text').value.trim();
    if (v) facts.push(v);
  });

  var issues = [];
  document.querySelectorAll('#issues-list .list-item').forEach(function(el) {
    var v = el.querySelector('.issue-text').value.trim();
    if (v) issues.push(v);
  });

  var args = [];
  document.querySelectorAll('#arguments-list .list-item').forEach(function(el) {
    var party = el.querySelector('.arg-party').value.trim();
    var claim = el.querySelector('.arg-claim').value.trim();
    if (!claim) return;
    args.push({
      party_name: party,
      claim: claim,
      supporting_facts: splitCSV(el.querySelector('.arg-facts').value),
      legal_basis: splitCSV(el.querySelector('.arg-basis').value),
      cited_precedents: splitCSV(el.querySelector('.arg-prec').value),
    });
  });

  var evidence = [];
  document.querySelectorAll('#evidence-list .list-item').forEach(function(el) {
    var title = el.querySelector('.ev-title').value.trim();
    if (!title) return;
    evidence.push({
      title: title,
      evidence_type: el.querySelector('.ev-type').value,
      description: el.querySelector('.ev-desc').value.trim(),
      submitted_by: el.querySelector('.ev-by').value.trim(),
      credibility_weight: parseFloat(el.querySelector('.ev-cred').value) || 0.5,
    });
  });

  var statutes = [];
  document.querySelectorAll('#statutes-list .list-item').forEach(function(el) {
    var v = el.querySelector('.statute-text').value.trim();
    if (v) statutes.push(v);
  });

  return {
    case_id: document.getElementById('case-id').value.trim() || 'WEB-' + Date.now(),
    title: document.getElementById('case-title').value.trim(),
    case_type: document.getElementById('case-type').value,
    jurisdiction: document.getElementById('case-jurisdiction').value.trim() || 'General',
    summary: document.getElementById('case-summary').value.trim(),
    parties: parties,
    facts: facts,
    issues: issues,
    arguments: args,
    evidence: evidence,
    applicable_statutes: statutes,
  };
}

// ============================================================
// 14. VIEW MANAGEMENT HELPERS
// ============================================================
function showLoading(msg) {
  document.getElementById('judgment-empty').style.display = 'none';
  document.getElementById('judgment-result').style.display = 'none';
  document.getElementById('judgment-loading').style.display = '';
  document.querySelector('.loading-text').textContent = msg || 'Analyzing case...';
  startLoadingPhases();
}

function startLoadingPhases() {
  if (loadingPhaseInterval) clearInterval(loadingPhaseInterval);
  var phaseIdx = 0;
  var phaseEl = document.querySelector('.phase-text');
  var dotsEl = document.querySelector('.loading-phase-dots');
  if (!phaseEl) return;
  phaseEl.textContent = loadingPhases[0];
  if (dotsEl) {
    var dots = dotsEl.querySelectorAll('.phase-dot');
    dots.forEach(function(d,i) { d.className = 'phase-dot' + (i === 0 ? ' active' : ''); });
  }
  loadingPhaseInterval = setInterval(function() {
    phaseIdx = (phaseIdx + 1) % loadingPhases.length;
    phaseEl.style.opacity = '0';
    setTimeout(function() {
      phaseEl.textContent = loadingPhases[phaseIdx];
      phaseEl.style.opacity = '1';
    }, 200);
    if (dotsEl) {
      var dots = dotsEl.querySelectorAll('.phase-dot');
      dots.forEach(function(d,i) {
        if (i < phaseIdx) d.className = 'phase-dot completed';
        else if (i === phaseIdx) d.className = 'phase-dot active';
        else d.className = 'phase-dot';
      });
    }
  }, 1500);
}

function stopLoadingPhases() {
  if (loadingPhaseInterval) {
    clearInterval(loadingPhaseInterval);
    loadingPhaseInterval = null;
  }
}

function showView(viewId) {
  var views = ['view-judgment', 'view-text', 'view-json', 'view-panel', 'view-risk', 'view-settlement'];
  views.forEach(function(id) {
    var el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  document.getElementById(viewId).style.display = '';
  document.getElementById('judgment-empty').style.display = 'none';
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('judgment-result').style.display = '';
  document.getElementById('format-toggle').style.display = 'none';
}

function activateResultTab(viewName) {
  document.querySelectorAll('.result-tab').forEach(function(b) { b.classList.remove('active'); });
  var tab = document.querySelector('.result-tab[data-view="' + viewName + '"]');
  if (tab) {
    tab.classList.add('active');
    switchResultTab(tab);
  }
}

// ============================================================
// 15. SUBMIT CASE (Single Judgment)
// ============================================================
async function submitCase() {
  var caseData = collectCase();
  if (!caseData.title) {
    showToast('Please enter a case title.', 'error');
    return;
  }
  showLoading('Analyzing case...');
  showResultTabs();

  try {
    lastCaseData = caseData;
    var resp = await fetch(API + '/judge', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var judgment = await resp.json();
    lastJudgment = judgment;
    renderJudgment(judgment);
    showResultTabs();
    activateResultTab('judgment');
    showToast('Judgment rendered successfully.', 'success');
  } catch (err) {
    stopLoadingPhases();
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    showToast('Error: ' + err.message, 'error');
  }
}

// ============================================================
// 16. RENDER JUDGMENT
// ============================================================
function renderJudgment(j) {
  stopLoadingPhases();
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('judgment-result').style.display = '';
  document.getElementById('format-toggle').style.display = '';

  // Verdict banner with stamp animation
  var banner = document.getElementById('verdict-banner');
  banner.className = 'verdict-banner ' + dispositionClass(j.disposition);
  var dispEl = document.getElementById('verdict-disposition');
  var stamp = document.getElementById('verdict-stamp');
  if (stamp) stamp.style.animation = 'none';
  dispEl.textContent = '';
  dispEl.style.color = dispositionColor(j.disposition);
  // Trigger stamp animation
  setTimeout(function() {
    if (stamp) { stamp.offsetHeight; stamp.style.animation = ''; }
    typewriterEffect(dispEl, j.disposition.replace(/_/g, ' ').toUpperCase(), 60);
  }, 100);
  // Fire confetti
  setTimeout(function() { fireConfetti(); }, 400);
  document.getElementById('verdict-meta').innerHTML =
    '<strong>' + escapeHtml(j.case_title) + '</strong> &mdash; ' + escapeHtml(j.date_decided) + '<br>' +
    'Prevailing party: <strong>' + escapeHtml(j.prevailing_party) + '</strong>' +
    (j.remedy !== 'none' ? ' &bull; Remedy: ' + j.remedy.replace(/_/g, ' ') : '') +
    '<br><button class="btn-why-result" onclick="openWhyThisResult()">Why this result?</button>' +
    (llmAvailable ? ' <button class="btn-why-result btn-ai-enhance" id="btn-enhance-judgment" onclick="enhanceJudgment()"><span class="btn-icon-sm">&#9733;</span> AI Enhance</button>' : '');

  // Score cards with confidence rings
  var cards = document.getElementById('score-cards');
  cards.innerHTML = '';
  var metrics = [
    { label: 'Confidence', value: (j.confidence * 100).toFixed(0) + '%', pct: j.confidence, color: confidenceColor(j.confidence), detail: 'issues' },
    { label: 'Evidence Strength', value: (j.strength_of_evidence * 100).toFixed(0) + '%', pct: j.strength_of_evidence, color: confidenceColor(j.strength_of_evidence), detail: 'evidence' },
    { label: 'Issues Analyzed', value: j.issues_addressed.length, pct: Math.min(j.issues_addressed.length / 5, 1), color: 'var(--blue)', detail: 'issues_list' },
    { label: 'Rules Applied', value: j.rules_applied.length, pct: Math.min(j.rules_applied.length / 8, 1), color: 'var(--gold)', detail: 'rules_list' },
  ];
  metrics.forEach(function(m, idx) {
    cards.innerHTML +=
      '<div class="score-card card-3d" onclick="openScoreDetail(' + idx + ')" style="cursor:pointer;" title="Click for details">' +
        '<div class="score-ring">' + renderConfidenceRing(m.pct, m.color) + '</div>' +
        '<div class="score-label">' + m.label + '</div>' +
        '<div class="score-value animated-counter" data-target="' + m.value + '" style="color:' + m.color + '">0</div>' +
        '<div class="score-bar">' +
          '<div class="score-bar-fill" style="width:' + (m.pct * 100) + '%;background:' + m.color + '"></div>' +
        '</div>' +
      '</div>';
  });
  animateConfidenceRings();
  animateCounters();
  initCardTilt();

  // Inline AI Insights (from ai_enhancement if present)
  var insightsEl = document.getElementById('inline-ai-insights');
  if (j.ai_enhancement && j.ai_enhancement.plain_english_summary) {
    insightsEl.style.display = '';
    var insightsHTML = '<h4>&#10024; AI Insights</h4>';
    insightsHTML += '<p style="color:var(--text-secondary);line-height:1.7;margin-bottom:0.75rem;">' +
      escapeHtml(j.ai_enhancement.plain_english_summary) + '</p>';
    if (j.ai_enhancement.key_insights && j.ai_enhancement.key_insights.length) {
      insightsHTML += '<div style="display:flex;flex-wrap:wrap;gap:0.25rem;">';
      j.ai_enhancement.key_insights.forEach(function(insight) {
        insightsHTML += '<span class="insight-chip">&#9733; ' + escapeHtml(insight) + '</span>';
      });
      insightsHTML += '</div>';
    }
    insightsEl.innerHTML = insightsHTML;
  } else {
    insightsEl.style.display = 'none';
  }

  // Sections
  var sectionsEl = document.getElementById('opinion-sections');
  sectionsEl.innerHTML = '';
  (j.sections || []).forEach(function(sec, i) {
    var openClass = i < 3 ? ' open' : '';
    var chevHtml = i < 3 ? '&#9650;' : '&#9660;';
    sectionsEl.innerHTML +=
      '<div class="opinion-section slide-in">' +
        '<div class="section-header' + openClass + '" onclick="toggleSection(this)">' +
          '<h3>' + escapeHtml(sec.heading) + '</h3>' +
          '<span class="section-chevron">' + chevHtml + '</span>' +
        '</div>' +
        '<div class="section-content' + openClass + '">' + escapeHtml(sec.content) + '</div>' +
      '</div>';
  });

  // Dissent
  var dissentEl = document.getElementById('dissent-section');
  if (j.dissent) {
    dissentEl.style.display = '';
    dissentEl.innerHTML =
      '<div class="dissent-header" onclick="toggleDissent()">' +
        'Dissenting Opinion ' +
        '<span class="section-chevron" id="dissent-chevron">&#9660;</span>' +
      '</div>' +
      '<div class="dissent-content" id="dissent-body">' + escapeHtml(j.dissent) + '</div>';
  } else {
    dissentEl.style.display = 'none';
  }

  // Text view
  document.getElementById('opinion-text-content').textContent = j.opinion_text || '';

  // JSON view
  document.getElementById('opinion-json-content').textContent = JSON.stringify(j, null, 2);

  // Make sure judgment view is visible
  document.getElementById('view-judgment').style.display = '';
}

// ============================================================
// 17. SCORE CARD DETAIL MODAL
// ============================================================
function openScoreDetail(idx) {
  if (!lastJudgment) return;
  var j = lastJudgment;
  var title = '';
  var body = '';

  if (idx === 0) {
    title = 'Confidence Analysis';
    body = '<p style="margin-bottom:1rem;">Overall confidence: <strong style="color:' + confidenceColor(j.confidence) + '">' +
      (j.confidence * 100).toFixed(1) + '%</strong></p>' +
      '<p style="color:var(--text-secondary);">This confidence score reflects the strength and consistency of the legal reasoning, ' +
      'the weight of applicable precedent, and the quality of evidence presented.</p>' +
      '<h4 style="margin:1rem 0 0.5rem;color:var(--gold);">Issues Addressed</h4>' +
      '<ul style="color:var(--text-secondary);padding-left:1.25rem;">' +
      j.issues_addressed.map(function(i) { return '<li>' + escapeHtml(i) + '</li>'; }).join('') +
      '</ul>';
  } else if (idx === 1) {
    title = 'Evidence Strength';
    body = '<p style="margin-bottom:1rem;">Evidence strength: <strong style="color:' + confidenceColor(j.strength_of_evidence) + '">' +
      (j.strength_of_evidence * 100).toFixed(1) + '%</strong></p>' +
      '<p style="color:var(--text-secondary);">This score evaluates the credibility, relevance, and persuasiveness of all evidence submitted.</p>' +
      '<h4 style="margin:1rem 0 0.5rem;color:var(--gold);">Facts Found</h4>' +
      '<ul style="color:var(--text-secondary);padding-left:1.25rem;">' +
      (j.facts_found || []).map(function(f) { return '<li>' + escapeHtml(f) + '</li>'; }).join('') +
      '</ul>';
  } else if (idx === 2) {
    title = 'Issues Analyzed';
    body = '<p style="margin-bottom:1rem;">' + j.issues_addressed.length + ' issues were analyzed in this judgment.</p>' +
      '<ul style="color:var(--text-secondary);padding-left:1.25rem;">' +
      j.issues_addressed.map(function(i) { return '<li>' + escapeHtml(i) + '</li>'; }).join('') +
      '</ul>';
  } else if (idx === 3) {
    title = 'Rules Applied';
    body = '<p style="margin-bottom:1rem;">' + j.rules_applied.length + ' legal rules were applied.</p>' +
      '<ul style="color:var(--text-secondary);padding-left:1.25rem;">' +
      j.rules_applied.map(function(r) { return '<li>' + escapeHtml(r) + '</li>'; }).join('') +
      '</ul>';
  }

  openModal(title, body);
}

// ============================================================
// 17b. "WHY THIS RESULT?" REASONING EXPLAINER
// ============================================================
function openWhyThisResult() {
  if (!lastJudgment) return;
  var j = lastJudgment;

  var body = '<div class="why-result-container">';

  // Step 1: Overview
  body += '<div class="why-step">' +
    '<div class="why-step-number">1</div>' +
    '<div class="why-step-content">' +
      '<h4>Disposition: ' + j.disposition.replace(/_/g, ' ').toUpperCase() + '</h4>' +
      '<p>' + escapeHtml(j.summary) + '</p>' +
    '</div></div>';

  // Step 2: Issues analyzed
  body += '<div class="why-step">' +
    '<div class="why-step-number">2</div>' +
    '<div class="why-step-content">' +
      '<h4>Legal Issues Analyzed (' + j.issues_addressed.length + ')</h4>' +
      '<p>The court identified and analyzed the following legal issues using the IRAC framework (Issue, Rule, Application, Conclusion):</p>' +
      '<ul>' + j.issues_addressed.map(function(i) { return '<li>' + escapeHtml(i) + '</li>'; }).join('') + '</ul>' +
    '</div></div>';

  // Step 3: Rules applied
  body += '<div class="why-step">' +
    '<div class="why-step-number">3</div>' +
    '<div class="why-step-content">' +
      '<h4>Rules &amp; Precedents Applied (' + j.rules_applied.length + ')</h4>' +
      '<p>The following legal rules, statutes, and precedents guided the analysis:</p>' +
      '<div class="why-rules-list">' +
      j.rules_applied.map(function(r) {
        return '<div class="why-rule-item clickable-rule" onclick="lookupRule(\'' + escapeHtml(r).replace(/'/g, "\\'") + '\')">' +
          '<span class="why-rule-icon">&#9878;</span> ' + escapeHtml(r) +
          '<span class="why-lookup-hint">click to look up</span>' +
        '</div>';
      }).join('') +
      '</div>' +
    '</div></div>';

  // Step 4: Evidence evaluation
  body += '<div class="why-step">' +
    '<div class="why-step-number">4</div>' +
    '<div class="why-step-content">' +
      '<h4>Evidence Evaluation</h4>' +
      '<p>The court weighed the evidence and found the following facts:</p>' +
      '<div class="why-evidence-bar">' +
        '<div class="why-evidence-label">Evidence Strength</div>' +
        '<div class="why-bar-track"><div class="why-bar-fill" style="width:' + (j.strength_of_evidence * 100) + '%;background:' + confidenceColor(j.strength_of_evidence) + '"></div></div>' +
        '<div class="why-evidence-pct" style="color:' + confidenceColor(j.strength_of_evidence) + '">' + (j.strength_of_evidence * 100).toFixed(0) + '%</div>' +
      '</div>' +
      (j.facts_found && j.facts_found.length ?
        '<ul>' + j.facts_found.map(function(f) { return '<li>' + escapeHtml(f) + '</li>'; }).join('') + '</ul>' :
        '<p style="color:var(--text-muted);">No specific facts enumerated.</p>') +
    '</div></div>';

  // Step 5: Reasoning chain
  body += '<div class="why-step">' +
    '<div class="why-step-number">5</div>' +
    '<div class="why-step-content">' +
      '<h4>Reasoning Chain</h4>' +
      '<p>' + escapeHtml(j.reasoning || j.analysis || 'The court applied the identified rules to the facts and evidence to reach its conclusion.') + '</p>' +
    '</div></div>';

  // Step 6: Holding
  body += '<div class="why-step">' +
    '<div class="why-step-number">6</div>' +
    '<div class="why-step-content">' +
      '<h4>Holding</h4>' +
      '<p><strong style="color:var(--gold);">' + escapeHtml(j.holding || 'The court rendered judgment as stated above.') + '</strong></p>' +
    '</div></div>';

  // Step 7: Confidence assessment
  body += '<div class="why-step">' +
    '<div class="why-step-number">7</div>' +
    '<div class="why-step-content">' +
      '<h4>Confidence Assessment: ' + (j.confidence * 100).toFixed(0) + '%</h4>' +
      '<p>This confidence level reflects:</p>' +
      '<ul>' +
        '<li>Strength of applicable precedent (' + j.rules_applied.length + ' rules applied)</li>' +
        '<li>Quality of evidence presented (' + (j.strength_of_evidence * 100).toFixed(0) + '% strength)</li>' +
        '<li>Clarity of legal issues (' + j.issues_addressed.length + ' issues identified)</li>' +
        (j.dissent ? '<li style="color:var(--red);">Note: A dissenting opinion was filed, indicating some judicial disagreement</li>' : '') +
      '</ul>' +
    '</div></div>';

  if (j.dissent) {
    body += '<div class="why-step why-step-dissent">' +
      '<div class="why-step-number" style="background:var(--red);">!</div>' +
      '<div class="why-step-content">' +
        '<h4 style="color:var(--red);">Dissenting View</h4>' +
        '<p>' + escapeHtml(j.dissent) + '</p>' +
      '</div></div>';
  }

  body += '</div>';

  openModal('Why This Result? — Step-by-Step Reasoning', body);
}

// ============================================================
// 17c. RULE / PRECEDENT LOOKUP FROM REASONING
// ============================================================
function lookupRule(ruleName) {
  if (!knowledgeData) {
    showToast('Knowledge base not loaded yet.', 'error');
    return;
  }
  var ruleNameLower = ruleName.toLowerCase();

  // Search precedents
  var matchedPrec = (knowledgeData.precedents_list || []).find(function(p) {
    return ruleNameLower.indexOf(p.case_name.toLowerCase()) !== -1 ||
      p.case_name.toLowerCase().indexOf(ruleNameLower) !== -1;
  });

  // Search statutes
  var matchedStat = (knowledgeData.statutes_list || []).find(function(s) {
    return ruleNameLower.indexOf(s.name.toLowerCase()) !== -1 ||
      s.name.toLowerCase().indexOf(ruleNameLower) !== -1 ||
      ruleNameLower.indexOf(s.code.toLowerCase()) !== -1;
  });

  // Search principles
  var matchedPrin = (knowledgeData.principles_list || []).find(function(p) {
    return ruleNameLower.indexOf(p.name.toLowerCase()) !== -1 ||
      p.name.toLowerCase().indexOf(ruleNameLower) !== -1;
  });

  var body = '';

  if (matchedPrec) {
    body += '<div class="lookup-section">' +
      '<div class="lookup-type-badge">Precedent</div>' +
      '<h4>' + escapeHtml(matchedPrec.case_name) + '</h4>' +
      '<div class="lookup-meta">' + escapeHtml(matchedPrec.citation) + ' (' + matchedPrec.year + ') &bull; Authority: ' +
        (matchedPrec.authority_weight * 100).toFixed(0) + '%</div>' +
      '<div class="lookup-field"><strong>Holding:</strong> ' + escapeHtml(matchedPrec.holding) + '</div>' +
      '<div class="lookup-field"><strong>Domain:</strong> ' + matchedPrec.domain.replace(/_/g, ' ') + '</div>' +
    '</div>';
  }

  if (matchedStat) {
    body += '<div class="lookup-section">' +
      '<div class="lookup-type-badge" style="background:var(--blue);">Statute</div>' +
      '<h4>' + escapeHtml(matchedStat.name) + '</h4>' +
      '<div class="lookup-meta">' + escapeHtml(matchedStat.code) + '</div>' +
      '<div class="lookup-field">' + escapeHtml(matchedStat.summary) + '</div>' +
      '<div class="lookup-field"><strong>Domain:</strong> ' + matchedStat.domain.replace(/_/g, ' ') + '</div>' +
    '</div>';
  }

  if (matchedPrin) {
    body += '<div class="lookup-section">' +
      '<div class="lookup-type-badge" style="background:var(--purple);">Principle</div>' +
      '<h4>' + escapeHtml(matchedPrin.name) + (matchedPrin.latin_name ? ' (' + escapeHtml(matchedPrin.latin_name) + ')' : '') + '</h4>' +
      '<div class="lookup-field">' + escapeHtml(matchedPrin.description) + '</div>' +
      (matchedPrin.elements && matchedPrin.elements.length ?
        '<div class="lookup-field"><strong>Elements:</strong><ul>' +
        matchedPrin.elements.map(function(e) { return '<li>' + escapeHtml(e) + '</li>'; }).join('') +
        '</ul></div>' : '') +
    '</div>';
  }

  if (!body) {
    body = '<p style="color:var(--text-muted);padding:1rem;">No matching entry found in the knowledge base for "' + escapeHtml(ruleName) + '".</p>' +
      '<p style="color:var(--text-secondary);padding:0 1rem;">This rule was applied through general legal reasoning rather than a specific knowledge base entry.</p>';
  }

  openModal('Legal Reference: ' + ruleName, body);
}

// ============================================================
// 18. SECTION TOGGLES
// ============================================================
function toggleSection(header) {
  header.classList.toggle('open');
  header.nextElementSibling.classList.toggle('open');
  var chev = header.querySelector('.section-chevron');
  chev.innerHTML = header.classList.contains('open') ? '&#9650;' : '&#9660;';
}

function toggleDissent() {
  var body = document.getElementById('dissent-body');
  body.classList.toggle('open');
  var chev = document.getElementById('dissent-chevron');
  chev.innerHTML = body.classList.contains('open') ? '&#9650;' : '&#9660;';
}

// ============================================================
// 19. LOAD DEMO CASES
// ============================================================
async function loadDemo(name) {
  try {
    var resp = await fetch(API + '/demo/' + name);
    if (!resp.ok) throw new Error(await resp.text());
    var data = await resp.json();
    populateForm(data);
    showToast('Loaded "' + name + '" demo case.', 'success');
  } catch (err) {
    showToast('Failed to load demo: ' + err.message, 'error');
  }
}

function populateForm(c) {
  clearForm();
  document.getElementById('case-id').value = c.case_id || '';
  document.getElementById('case-title').value = c.title || '';
  document.getElementById('case-type').value = c.case_type || 'civil';
  document.getElementById('case-jurisdiction').value = c.jurisdiction || 'General';
  document.getElementById('case-summary').value = c.summary || '';

  (c.parties || []).forEach(function(p) {
    addParty(p.role);
    var items = document.querySelectorAll('#parties-list .list-item');
    var last = items[items.length - 1];
    last.querySelector('.party-name').value = p.name || '';
    last.querySelector('.party-role').value = p.role || 'plaintiff';
    last.querySelector('.party-desc').value = p.description || '';
    last.querySelector('.party-counsel').value = p.counsel || '';
  });

  (c.facts || []).forEach(function(f) { addFact(f); });
  (c.issues || []).forEach(function(i) { addIssue(i); });
  (c.arguments || []).forEach(function(a) { addArgument(a); });
  (c.evidence || []).forEach(function(e) { addEvidence(e); });
  (c.applicable_statutes || []).forEach(function(s) { addStatute(s); });

  updateFieldsetCounts();
}

function clearForm() {
  document.getElementById('case-form').reset();
  ['parties-list','facts-list','issues-list','arguments-list','evidence-list','statutes-list'].forEach(function(id) {
    document.getElementById(id).innerHTML = '';
  });
  document.getElementById('judgment-empty').style.display = '';
  document.getElementById('judgment-result').style.display = 'none';
  document.getElementById('judgment-loading').style.display = 'none';
  document.getElementById('format-toggle').style.display = 'none';
  document.getElementById('result-tabs').style.display = 'none';
  lastJudgment = null;
  lastPanel = null;
  lastRisk = null;
  lastSettlement = null;
  updateFieldsetCounts();
}

// ============================================================
// 20. 3-JUDGE PANEL
// ============================================================
async function submitPanel() {
  var caseData = collectCase();
  if (!caseData.title) { showToast('Please enter a case title.', 'error'); return; }
  lastCaseData = caseData;
  showLoading('Convening 3-judge panel...');
  showResultTabs();

  try {
    var resp = await fetch(API + '/panel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(caseData),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var result = await resp.json();
    lastPanel = result;
    if (result.judgment) lastJudgment = result.judgment;
    renderPanel(result);
    showResultTabs();
    activateResultTab('panel');
    showToast('Panel decision rendered.', 'success');
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    showToast('Panel error: ' + err.message, 'error');
  }
}

function renderPanel(result) {
  stopLoadingPhases();
  showView('view-panel');
  var el = document.getElementById('panel-result');
  var unanimous = result.is_unanimous;
  var bannerClass = unanimous ? 'unanimous' : 'split';

  var html =
    '<div class="panel-vote-banner ' + bannerClass + '">' +
      '<div class="panel-vote-label">' + (unanimous ? 'UNANIMOUS' : 'SPLIT') + ' DECISION</div>' +
      '<div class="panel-vote-disp">' + result.majority_disposition.replace(/_/g, ' ').toUpperCase() + '</div>' +
      '<div class="panel-vote-count">' + result.majority_vote + ' of ' + result.panel_size + ' judges</div>' +
      '<div style="font-size:0.85rem;margin-top:0.5rem;color:var(--text-muted);">' +
        'Confidence: ' + (result.majority_confidence * 100).toFixed(0) + '%' +
      '</div>' +
      '<button class="btn-why-result" onclick="openWhyPanelResult()" style="margin-top:0.75rem;">Why did the panel decide this way?</button>' +
      (llmAvailable ? ' <button class="btn-why-result btn-ai-enhance" id="btn-enhance-panel" onclick="enhancePanel()" style="margin-top:0.75rem;"><span class="btn-icon-sm">&#9733;</span> AI Enhance</button>' : '') +
    '</div>' +
    '<div style="padding:1rem 0;">' +
      '<h3 style="color:var(--gold);margin-bottom:0.5rem;">Majority Opinion</h3>' +
      '<p style="color:var(--text-secondary);line-height:1.6;">' + escapeHtml(result.majority_opinion) + '</p>' +
    '</div>' +
    '<h3 style="color:var(--text-primary);margin-bottom:0.75rem;">Individual Opinions <span style="color:var(--text-muted);font-size:0.8rem;">(click to expand reasoning)</span></h3>' +
    '<div class="judge-cards">';

  (result.opinions || []).forEach(function(op, idx) {
    var isMajority = op.agrees_with_majority;
    var cardClass = isMajority ? 'majority' : 'dissent';
    html +=
      '<div class="judge-card ' + cardClass + '">' +
        '<div class="judge-card-header" onclick="toggleJudgeCard(this)" style="cursor:pointer;">' +
          '<div class="judge-name">' + escapeHtml(op.judge_name) + '</div>' +
          '<div class="judge-philosophy">' + escapeHtml(op.philosophy) + '</div>' +
          '<div class="judge-disposition" style="color:' + dispositionColor(op.disposition) + '">' +
            op.disposition.replace(/_/g, ' ') +
          '</div>' +
          '<div class="judge-conf">Confidence: ' + (op.confidence * 100).toFixed(0) + '%</div>' +
          '<div class="judge-role">' + (isMajority ? 'MAJORITY' : 'DISSENT') + '</div>' +
          '<span class="section-chevron" style="float:right;color:var(--text-muted);">&#9660;</span>' +
        '</div>' +
        '<div class="judge-card-body" style="display:none;">' +
          '<div style="margin-bottom:0.75rem;">' +
            '<div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:0.25rem;">Philosophy</div>' +
            '<div style="color:var(--text-secondary);font-size:0.85rem;">' + escapeHtml(op.philosophy_description) + '</div>' +
          '</div>' +
          '<div style="margin-bottom:0.75rem;">' +
            '<div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:0.25rem;">Reasoning</div>' +
            '<div style="color:var(--text-secondary);font-size:0.85rem;">' + escapeHtml(op.reasoning_summary) + '</div>' +
          '</div>' +
          (op.key_factors && op.key_factors.length ?
            '<div style="margin-bottom:0.75rem;">' +
              '<div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:0.25rem;">Key Factors</div>' +
              '<ul style="color:var(--text-secondary);font-size:0.85rem;padding-left:1.25rem;">' +
                op.key_factors.map(function(f) { return '<li>' + escapeHtml(f) + '</li>'; }).join('') +
              '</ul>' +
            '</div>' : '') +
          (op.cited_precedents && op.cited_precedents.length ?
            '<div style="margin-bottom:0.75rem;">' +
              '<div style="font-size:0.75rem;color:var(--text-muted);text-transform:uppercase;margin-bottom:0.25rem;">Cited Precedents</div>' +
              '<ul style="color:var(--text-secondary);font-size:0.85rem;padding-left:1.25rem;">' +
                op.cited_precedents.map(function(p) { return '<li>' + escapeHtml(p) + '</li>'; }).join('') +
              '</ul>' +
            '</div>' : '') +
        '</div>' +
      '</div>';
  });

  html += '</div>';

  if (result.judgment) {
    lastJudgment = result.judgment;
    html +=
      '<div style="text-align:center;margin-top:1.5rem;">' +
        '<button class="btn btn-sm btn-outline" onclick="renderJudgment(lastJudgment);showResultTabs();activateResultTab(\'judgment\');">' +
          'View Full Majority Opinion' +
        '</button>' +
      '</div>';
  }

  el.innerHTML = html;
}

function toggleJudgeCard(header) {
  var body = header.nextElementSibling;
  var isOpen = body.style.display !== 'none';
  body.style.display = isOpen ? 'none' : '';
  var chev = header.querySelector('.section-chevron');
  if (chev) chev.innerHTML = isOpen ? '&#9660;' : '&#9650;';
}

// ============================================================
// 21. RISK ASSESSMENT
// ============================================================
async function runRiskAssessment() {
  var caseData = collectCase();
  if (!caseData.title) { showToast('Please enter a case title.', 'error'); return; }
  lastCaseData = caseData;
  showLoading('Assessing litigation risk...');
  showResultTabs();

  try {
    var resp = await fetch(API + '/risk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: caseData }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var result = await resp.json();
    lastRisk = result;
    renderRisk(result);
    showResultTabs();
    activateResultTab('risk');
    showToast('Risk assessment complete.', 'success');
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    showToast('Risk error: ' + err.message, 'error');
  }
}

function renderRisk(result) {
  stopLoadingPhases();
  showView('view-risk');
  var el = document.getElementById('risk-result');

  var riskColorMap = {
    low: 'var(--green)', moderate: 'var(--amber)', high: 'var(--red)',
    very_low: 'var(--green)', extreme: 'var(--red)',
  };
  var riskColor = riskColorMap[result.litigation_risk_level] || 'var(--text-muted)';

  var html =
    '<div class="risk-header">' +
      '<div>' +
        '<div class="risk-level" style="color:' + riskColor + '">' +
          result.litigation_risk_level.replace(/_/g, ' ').toUpperCase() + ' RISK</div>' +
        '<div class="risk-title">' + escapeHtml(result.case_title) + '</div>' +
      '</div>' +
      '<button class="btn-why-result" onclick="openWhyRiskResult()" style="margin-top:0.5rem;">Why this risk level?</button>' +
      (llmAvailable ? ' <button class="btn-why-result btn-ai-enhance" id="btn-enhance-risk" onclick="enhanceRisk()" style="margin-top:0.5rem;"><span class="btn-icon-sm">&#9733;</span> AI Enhance</button>' : '') +
    '</div>' +
    '<div style="padding:0.75rem 0;color:var(--text-secondary);line-height:1.6;font-size:0.9rem;">' +
      escapeHtml(result.recommendation) +
    '</div>' +
    '<div class="party-risk-cards">';

  (result.parties || []).forEach(function(p) {
    var probPct = (p.win_probability * 100).toFixed(0);
    var gradeColorMap = { A: '#22c55e', B: '#84cc16', C: '#eab308', D: '#f97316', F: '#ef4444' };
    var gc = gradeColorMap[p.overall_grade] || '#888';

    html +=
      '<div class="party-risk-card slide-in">' +
        '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.75rem;">' +
          '<div>' +
            '<div class="party-risk-name">' + escapeHtml(p.party_name) + '</div>' +
            '<div class="party-risk-role">' + escapeHtml(p.role) + '</div>' +
          '</div>' +
          '<div class="grade-badge" style="background:' + gc + '">' + p.overall_grade + '</div>' +
        '</div>' +
        '<div style="margin-bottom:0.5rem;">' +
          '<div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.25rem;">' +
            '<span>Win Probability</span><span style="color:var(--gold)">' + probPct + '%</span>' +
          '</div>' +
          '<div class="prob-bar"><div class="prob-bar-fill" style="width:' + probPct + '%"></div></div>' +
        '</div>' +
        '<div style="display:flex;gap:0.5rem;margin-bottom:0.5rem;">' +
          '<div style="flex:1;">' +
            '<div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.25rem;">Evidence</div>' +
            '<div class="prob-bar"><div class="prob-bar-fill" style="width:' + (p.evidence_score * 100).toFixed(0) + '%;background:var(--blue)"></div></div>' +
          '</div>' +
          '<div style="flex:1;">' +
            '<div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.25rem;">Arguments</div>' +
            '<div class="prob-bar"><div class="prob-bar-fill" style="width:' + (p.argument_score * 100).toFixed(0) + '%;background:var(--purple, #a855f7)"></div></div>' +
          '</div>' +
        '</div>';

    if (p.strengths && p.strengths.length) {
      html += '<div class="sw-list strengths"><div class="sw-label">Strengths</div>';
      p.strengths.forEach(function(s) { html += '<div class="sw-item">+ ' + escapeHtml(s) + '</div>'; });
      html += '</div>';
    }
    if (p.weaknesses && p.weaknesses.length) {
      html += '<div class="sw-list weaknesses"><div class="sw-label">Weaknesses</div>';
      p.weaknesses.forEach(function(w) { html += '<div class="sw-item">- ' + escapeHtml(w) + '</div>'; });
      html += '</div>';
    }
    if (p.risk_factors && p.risk_factors.length) {
      html += '<div class="sw-list risks"><div class="sw-label">Risk Factors</div>';
      p.risk_factors.forEach(function(r) { html += '<div class="sw-item">! ' + escapeHtml(r) + '</div>'; });
      html += '</div>';
    }

    html += '</div>';
  });

  html += '</div>';
  el.innerHTML = html;
}

// ============================================================
// 22. SETTLEMENT CALCULATOR
// ============================================================
function openSettlementModal() {
  var caseData = collectCase();
  if (!caseData.title) {
    showToast('Please enter a case title first.', 'error');
    return;
  }
  var bodyHTML =
    '<div style="margin-bottom:1rem;">' +
      '<label style="display:block;color:var(--text-secondary);margin-bottom:0.5rem;">Claimed Damages Amount (USD)</label>' +
      '<input type="number" id="settlement-damages-input" placeholder="Leave blank for auto-estimate" ' +
        'style="width:100%;padding:0.6rem 0.75rem;background:var(--bg-input);border:1px solid var(--border);' +
        'border-radius:var(--radius);color:var(--text-primary);font-family:var(--font);font-size:0.9rem;">' +
    '</div>' +
    '<p style="color:var(--text-muted);font-size:0.8rem;">Leave blank to let the AI auto-estimate damages based on the case details.</p>';

  var footerHTML =
    '<button class="btn btn-sm btn-outline" onclick="closeModal()">Cancel</button>' +
    '<button class="btn btn-sm btn-primary" onclick="executeSettlement()">Calculate</button>';

  openModal('Settlement Calculator', bodyHTML, footerHTML);

  setTimeout(function() {
    var inp = document.getElementById('settlement-damages-input');
    if (inp) inp.focus();
  }, 100);
}

async function executeSettlement() {
  var input = document.getElementById('settlement-damages-input');
  var claimed = input ? parseFloat(input.value) || 0 : 0;
  closeModal();

  var caseData = collectCase();
  lastCaseData = caseData;
  showLoading('Calculating settlement...');
  showResultTabs();

  try {
    var resp = await fetch(API + '/settlement', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: caseData, claimed_damages: claimed }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var result = await resp.json();
    lastSettlement = result;
    renderSettlement(result);
    showResultTabs();
    activateResultTab('settlement');
    showToast('Settlement analysis complete.', 'success');
  } catch (err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    showToast('Settlement error: ' + err.message, 'error');
  }
}

function renderSettlement(result) {
  stopLoadingPhases();
  showView('view-settlement');
  var el = document.getElementById('settlement-result');

  var s = result.settlement_range;
  var d = result.damages_estimate;
  var shouldSettle = result.should_settle;

  var rangeMarker = '';
  if (s.high > 0 && s.high > s.low) {
    var markerPos = ((s.recommended - s.low) / (s.high - s.low) * 100).toFixed(1);
    rangeMarker = '<div class="range-marker" style="left:' + markerPos + '%"></div>';
  }

  var html =
    '<div class="settlement-header" style="text-align:center;padding:1.5rem 0;">' +
      '<div style="font-size:0.85rem;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;">Settlement Recommendation</div>' +
      '<div style="font-size:1.8rem;font-weight:700;color:' + (shouldSettle ? 'var(--green)' : 'var(--red)') + ';margin:0.5rem 0;">' +
        (shouldSettle ? 'SETTLE' : 'LITIGATE') +
      '</div>' +
      '<div style="color:var(--text-secondary);font-size:0.9rem;max-width:600px;margin:0 auto;">' +
        escapeHtml(result.settlement_recommendation) +
      '</div>' +
      '<button class="btn-why-result" onclick="openWhySettlementResult()" style="margin-top:0.75rem;">How was this calculated?</button>' +
      (llmAvailable ? ' <button class="btn-why-result btn-ai-enhance" id="btn-enhance-settlement" onclick="enhanceSettlement()" style="margin-top:0.75rem;"><span class="btn-icon-sm">&#9733;</span> AI Enhance</button>' : '') +
    '</div>' +
    '<div class="settlement-grid">' +
      '<div class="settlement-card">' +
        '<div class="settlement-card-label">Estimated Total Damages</div>' +
        '<div class="money-big">' + fmtMoney(d.total) + '</div>' +
        '<div class="money-row"><span>Compensatory</span><span>' + fmtMoney(d.compensatory) + '</span></div>' +
        '<div class="money-row"><span>Consequential</span><span>' + fmtMoney(d.consequential) + '</span></div>' +
        '<div class="money-row"><span>Punitive</span><span>' + fmtMoney(d.punitive) + '</span></div>' +
        '<div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted);">' +
          'Confidence: ' + (d.confidence * 100).toFixed(0) + '% &bull; ' + escapeHtml(d.basis) +
        '</div>' +
      '</div>' +
      '<div class="settlement-card">' +
        '<div class="settlement-card-label">Settlement Range</div>' +
        '<div class="money-big" style="color:var(--green)">' + fmtMoney(s.recommended) + '</div>' +
        '<div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.75rem;">Recommended</div>' +
        '<div class="settlement-range-bar">' +
          '<div class="range-fill" style="left:0%;width:100%"></div>' +
          rangeMarker +
        '</div>' +
        '<div class="money-row"><span>Low</span><span>' + fmtMoney(s.low) + '</span></div>' +
        '<div class="money-row"><span>Midpoint</span><span>' + fmtMoney(s.midpoint) + '</span></div>' +
        '<div class="money-row"><span>High</span><span>' + fmtMoney(s.high) + '</span></div>' +
        '<div style="margin-top:0.5rem;font-size:0.75rem;color:var(--text-muted);">' + escapeHtml(s.rationale) + '</div>' +
      '</div>' +
      '<div class="settlement-card">' +
        '<div class="settlement-card-label">Litigation Cost Estimate</div>' +
        '<div class="money-big" style="color:var(--red)">' + fmtMoney(result.cost_of_litigation_estimate) + '</div>' +
        '<div style="font-size:0.75rem;color:var(--text-muted);margin-bottom:0.75rem;">Estimated total cost to litigate</div>' +
        '<div class="settlement-card-label" style="margin-top:1rem;">Risk Summary</div>' +
        (result.risk_summary.parties || []).map(function(p) {
          return '<div class="money-row"><span>' + escapeHtml(p.party_name) + ' (' + p.overall_grade + ')</span><span>' +
            (p.win_probability * 100).toFixed(0) + '%</span></div>';
        }).join('') +
      '</div>' +
    '</div>';

  el.innerHTML = html;
}

// ============================================================
// 23. RUN ALL ANALYSES
// ============================================================
async function runAllAnalyses() {
  var caseData = collectCase();
  if (!caseData.title) {
    showToast('Please enter a case title.', 'error');
    return;
  }

  showLoading('Running all analyses...');
  showResultTabs();

  var judgmentPromise = fetch(API + '/judge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(caseData),
  }).then(function(r) { return r.ok ? r.json() : r.text().then(function(t) { throw new Error(t); }); });

  var panelPromise = fetch(API + '/panel', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(caseData),
  }).then(function(r) { return r.ok ? r.json() : r.text().then(function(t) { throw new Error(t); }); });

  var riskPromise = fetch(API + '/risk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ case: caseData }),
  }).then(function(r) { return r.ok ? r.json() : r.text().then(function(t) { throw new Error(t); }); });

  var settlementPromise = fetch(API + '/settlement', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ case: caseData, claimed_damages: 0 }),
  }).then(function(r) { return r.ok ? r.json() : r.text().then(function(t) { throw new Error(t); }); });

  var results = await Promise.allSettled([judgmentPromise, panelPromise, riskPromise, settlementPromise]);
  var successCount = 0;
  var errorMessages = [];

  // Judgment
  if (results[0].status === 'fulfilled') {
    lastJudgment = results[0].value;
    renderJudgment(results[0].value);
    successCount++;
  } else {
    errorMessages.push('Judgment: ' + results[0].reason.message);
  }

  // Panel
  if (results[1].status === 'fulfilled') {
    lastPanel = results[1].value;
    if (results[1].value.judgment) lastJudgment = results[1].value.judgment;
    renderPanel(results[1].value);
    successCount++;
  } else {
    errorMessages.push('Panel: ' + results[1].reason.message);
  }

  // Risk
  if (results[2].status === 'fulfilled') {
    lastRisk = results[2].value;
    renderRisk(results[2].value);
    successCount++;
  } else {
    errorMessages.push('Risk: ' + results[2].reason.message);
  }

  // Settlement
  if (results[3].status === 'fulfilled') {
    lastSettlement = results[3].value;
    renderSettlement(results[3].value);
    successCount++;
  } else {
    errorMessages.push('Settlement: ' + results[3].reason.message);
  }

  document.getElementById('judgment-loading').style.display = 'none';

  if (successCount > 0) {
    document.getElementById('judgment-result').style.display = '';
    showResultTabs();
    // Activate the judgment tab by default if available
    if (lastJudgment) {
      activateResultTab('judgment');
    } else if (lastPanel) {
      activateResultTab('panel');
    } else if (lastRisk) {
      activateResultTab('risk');
    } else {
      activateResultTab('settlement');
    }
    showToast(successCount + ' of 4 analyses completed successfully.', 'success');
  } else {
    document.getElementById('judgment-empty').style.display = '';
    showToast('All analyses failed.', 'error');
  }

  if (errorMessages.length > 0) {
    errorMessages.forEach(function(msg) {
      showToast(msg, 'error', 6000);
    });
  }
}

// ============================================================
// 24. KNOWLEDGE BASE
// ============================================================
async function loadKnowledge() {
  try {
    var resp = await fetch(API + '/knowledge');
    var kb = await resp.json();
    knowledgeData = kb;
    renderKnowledge(kb);
  } catch (err) {
    /* silently ignore on load failure */
  }
}

function renderKnowledge(kb) {
  // Stats
  document.getElementById('kb-stats').innerHTML =
    '<div class="kb-stat-card slide-in"><div class="kb-stat-number">' + kb.statutes + '</div><div class="kb-stat-label">Statutes</div></div>' +
    '<div class="kb-stat-card slide-in"><div class="kb-stat-number">' + kb.precedents + '</div><div class="kb-stat-label">Precedents</div></div>' +
    '<div class="kb-stat-card slide-in"><div class="kb-stat-number">' + kb.principles + '</div><div class="kb-stat-label">Principles</div></div>' +
    '<div class="kb-stat-card slide-in"><div class="kb-stat-number">' + kb.domains.length + '</div><div class="kb-stat-label">Domains</div></div>';

  // Domain filters
  var filtersEl = document.getElementById('kb-domain-filters');
  filtersEl.innerHTML = '<button class="domain-filter active" data-domain="all" onclick="filterKBDomain(this)">All Domains</button>';
  (kb.domains || []).forEach(function(d) {
    filtersEl.innerHTML +=
      '<button class="domain-filter" data-domain="' + d + '" onclick="filterKBDomain(this)">' +
        d.replace(/_/g, ' ') +
      '</button>';
  });

  // Render all items
  renderKBPrecedents(kb.precedents_list || []);
  renderKBStatutes(kb.statutes_list || []);
  renderKBPrinciples(kb.principles_list || []);
}

function renderKBPrecedents(list) {
  var precEl = document.getElementById('precedents-list-kb');
  precEl.innerHTML = '';
  list.forEach(function(p) {
    if (activeKBDomain !== 'all' && p.domain !== activeKBDomain) return;
    precEl.innerHTML +=
      '<div class="kb-item" onclick="toggleKBExpand(this)">' +
        '<div class="kb-item-title">' + escapeHtml(p.case_name) +
          ' <span class="kb-item-badge">' + p.domain.replace(/_/g, ' ') + '</span></div>' +
        '<div class="kb-item-meta">' + escapeHtml(p.citation) + ' (' + p.year + ') &bull; Authority: ' +
          (p.authority_weight * 100).toFixed(0) + '%</div>' +
        '<div class="kb-item-body">' + escapeHtml(p.holding) + '</div>' +
        '<div class="kb-item-expand" style="display:none;">' +
          (p.ratio_decidendi ? '<div style="margin-top:0.5rem;"><strong style="color:var(--gold);">Ratio Decidendi:</strong> ' +
            '<span style="color:var(--text-secondary);">' + escapeHtml(p.ratio_decidendi) + '</span></div>' : '') +
          (p.key_facts ? '<div style="margin-top:0.25rem;"><strong style="color:var(--gold);">Key Facts:</strong> ' +
            '<span style="color:var(--text-secondary);">' + escapeHtml(p.key_facts) + '</span></div>' : '') +
        '</div>' +
      '</div>';
  });
}

function renderKBStatutes(list) {
  var statEl = document.getElementById('statutes-list-kb');
  statEl.innerHTML = '';
  list.forEach(function(s) {
    if (activeKBDomain !== 'all' && s.domain !== activeKBDomain) return;
    statEl.innerHTML +=
      '<div class="kb-item" onclick="toggleKBExpand(this)">' +
        '<div class="kb-item-title">' + escapeHtml(s.name) +
          ' <span class="kb-item-badge">' + s.domain.replace(/_/g, ' ') + '</span></div>' +
        '<div class="kb-item-meta">' + escapeHtml(s.code) + '</div>' +
        '<div class="kb-item-body">' + escapeHtml(s.summary) + '</div>' +
        '<div class="kb-item-expand" style="display:none;">' +
          (s.full_text ? '<div style="margin-top:0.5rem;color:var(--text-secondary);font-size:0.85rem;">' +
            escapeHtml(s.full_text) + '</div>' : '') +
          (s.key_provisions ? '<div style="margin-top:0.25rem;"><strong style="color:var(--gold);">Key Provisions:</strong> ' +
            '<span style="color:var(--text-secondary);">' + escapeHtml(s.key_provisions) + '</span></div>' : '') +
        '</div>' +
      '</div>';
  });
}

function renderKBPrinciples(list) {
  var prinEl = document.getElementById('principles-list-kb');
  prinEl.innerHTML = '';
  list.forEach(function(p) {
    if (activeKBDomain !== 'all' && p.domain !== activeKBDomain) return;
    var elementsHtml = '';
    if (p.elements && p.elements.length) {
      elementsHtml =
        '<div style="margin-top:0.5rem;"><strong style="color:var(--gold);">Elements:</strong>' +
        '<ul style="color:var(--text-secondary);padding-left:1.25rem;margin-top:0.25rem;">' +
        p.elements.map(function(e) { return '<li>' + escapeHtml(e) + '</li>'; }).join('') +
        '</ul></div>';
    }
    prinEl.innerHTML +=
      '<div class="kb-item" onclick="toggleKBExpand(this)">' +
        '<div class="kb-item-title">' + escapeHtml(p.name) +
          (p.latin_name ? ' (' + escapeHtml(p.latin_name) + ')' : '') +
          ' <span class="kb-item-badge">' + p.domain.replace(/_/g, ' ') + '</span></div>' +
        '<div class="kb-item-body">' + escapeHtml(p.description) + '</div>' +
        '<div class="kb-item-expand" style="display:none;">' +
          elementsHtml +
          (p.application ? '<div style="margin-top:0.25rem;"><strong style="color:var(--gold);">Application:</strong> ' +
            '<span style="color:var(--text-secondary);">' + escapeHtml(p.application) + '</span></div>' : '') +
        '</div>' +
      '</div>';
  });
}

function toggleKBExpand(itemEl) {
  var expand = itemEl.querySelector('.kb-item-expand');
  if (!expand) return;
  var isOpen = expand.style.display !== 'none';
  expand.style.display = isOpen ? 'none' : '';
  itemEl.classList.toggle('kb-item-expanded', !isOpen);
}

function filterKBDomain(btn) {
  document.querySelectorAll('.domain-filter').forEach(function(b) { b.classList.remove('active'); });
  btn.classList.add('active');
  activeKBDomain = btn.dataset.domain;
  if (knowledgeData) {
    renderKBPrecedents(knowledgeData.precedents_list || []);
    renderKBStatutes(knowledgeData.statutes_list || []);
    renderKBPrinciples(knowledgeData.principles_list || []);
  }
}

async function searchPrecedents() {
  var query = document.getElementById('prec-search').value.trim();
  if (!query) return;
  try {
    var resp = await fetch(API + '/precedents/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query }),
    });
    var data = await resp.json();
    var el = document.getElementById('precedents-results');
    if (!data.results || !data.results.length) {
      el.innerHTML = '<p style="color:var(--text-muted);padding:0.5rem;">No matching precedents found.</p>';
      return;
    }
    el.innerHTML = '<p style="color:var(--gold);font-size:0.8rem;margin-bottom:0.5rem;">Search results:</p>';
    data.results.forEach(function(r) {
      el.innerHTML +=
        '<div class="kb-item slide-in" onclick="toggleKBExpand(this)">' +
          '<div class="kb-item-title">' + escapeHtml(r.case_name) +
            ' <span class="kb-item-badge">' + r.domain.replace(/_/g, ' ') + '</span></div>' +
          '<div class="kb-item-meta">' + escapeHtml(r.citation) + ' (' + r.year + ') &bull; Authority: ' +
            (r.authority_weight * 100).toFixed(0) + '% &bull; Matched: ' + r.matched_terms.join(', ') + '</div>' +
          '<div class="kb-item-body">' + escapeHtml(r.holding) + '</div>' +
          '<div class="kb-item-expand" style="display:none;">' +
            (r.ratio_decidendi ? '<div style="margin-top:0.5rem;"><strong style="color:var(--gold);">Ratio Decidendi:</strong> ' +
              '<span style="color:var(--text-secondary);">' + escapeHtml(r.ratio_decidendi) + '</span></div>' : '') +
          '</div>' +
        '</div>';
    });
    showToast('Found ' + data.results.length + ' matching precedent(s).', 'info');
  } catch (err) {
    showToast('Search failed: ' + err.message, 'error');
  }
}

// ============================================================
// 25. CASE HISTORY
// ============================================================
async function loadHistory() {
  try {
    var resp = await fetch(API + '/history');
    var data = await resp.json();
    var el = document.getElementById('history-list');
    if (!data.cases || !data.cases.length) {
      el.innerHTML = '<p style="color:var(--text-muted);">No cases judged yet. Submit a case to see it here.</p>';
      return;
    }
    el.innerHTML = '';
    data.cases.forEach(function(c) {
      var card = document.createElement('div');
      card.className = 'history-card slide-in';
      card.style.cursor = 'pointer';
      card.innerHTML =
        '<div class="history-card-left">' +
          '<h3>' + escapeHtml(c.title) + '</h3>' +
          '<p>' + escapeHtml(c.case_id) + ' &bull; Prevailing: ' + escapeHtml(c.prevailing_party) + '</p>' +
        '</div>' +
        '<div class="history-card-right">' +
          '<span class="disp-badge ' + dispositionClass(c.disposition) + '">' + c.disposition.replace(/_/g, ' ') + '</span>' +
          '<p style="font-size:0.75rem;color:var(--text-muted);margin-top:0.25rem;">Confidence: ' +
            (c.confidence * 100).toFixed(0) + '%</p>' +
        '</div>';
      card.addEventListener('click', function() {
        reJudgeFromHistory(c);
      });
      el.appendChild(card);
    });
  } catch (err) {
    /* silently ignore */
  }
}

function reJudgeFromHistory(caseInfo) {
  showToast('Re-judging "' + caseInfo.title + '"...', 'info');
  // Switch to judge tab
  document.querySelectorAll('.nav-btn').forEach(function(b) { b.classList.remove('active'); });
  document.querySelectorAll('.tab-panel').forEach(function(p) { p.classList.remove('active'); });
  var judgeBtn = document.querySelector('.nav-btn[data-tab="judge"]');
  if (judgeBtn) judgeBtn.classList.add('active');
  document.getElementById('tab-judge').classList.add('active');

  showLoading('Re-judging "' + caseInfo.title + '"...');

  // Build a minimal case payload from history info
  var payload = {
    case_id: caseInfo.case_id,
    title: caseInfo.title,
    case_type: 'civil',
    jurisdiction: 'General',
    summary: '',
    parties: [],
    facts: [],
    issues: [],
    arguments: [],
    evidence: [],
    applicable_statutes: [],
  };

  fetch(API + '/judge', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  .then(function(resp) {
    if (!resp.ok) return resp.text().then(function(t) { throw new Error(t); });
    return resp.json();
  })
  .then(function(judgment) {
    lastJudgment = judgment;
    renderJudgment(judgment);
    showResultTabs();
    activateResultTab('judgment');
    showToast('Judgment rendered for "' + caseInfo.title + '".', 'success');
  })
  .catch(function(err) {
    document.getElementById('judgment-loading').style.display = 'none';
    document.getElementById('judgment-empty').style.display = '';
    showToast('Error: ' + err.message, 'error');
  });
}

// ============================================================
// 26. PANEL REASONING EXPLAINER
// ============================================================
function openWhyPanelResult() {
  if (!lastPanel) return;
  var p = lastPanel;

  var body = '<div class="why-result-container">';

  body += '<div class="why-step">' +
    '<div class="why-step-number">1</div>' +
    '<div class="why-step-content">' +
      '<h4>Panel Composition</h4>' +
      '<p>A ' + p.panel_size + '-judge panel was convened, each bringing a different judicial philosophy to the analysis. ' +
      'This ensures multiple perspectives are considered before reaching a decision.</p>' +
      '<div class="panel-compare-grid">';

  (p.opinions || []).forEach(function(op) {
    body += '<div class="panel-compare-card">' +
      '<div class="panel-compare-name">' + escapeHtml(op.judge_name) + '</div>' +
      '<div class="panel-compare-phil">' + escapeHtml(op.philosophy) + '</div>' +
      '<div class="panel-compare-desc">' + escapeHtml(op.philosophy_description || '') + '</div>' +
    '</div>';
  });
  body += '</div></div></div>';

  body += '<div class="why-step">' +
    '<div class="why-step-number">2</div>' +
    '<div class="why-step-content">' +
      '<h4>How Each Judge Weighed the Case</h4>' +
      '<p>Different judicial philosophies lead judges to weigh evidence, precedent, statutory text, and policy considerations differently:</p>' +
      '<table class="why-compare-table"><thead><tr>' +
        '<th>Judge</th><th>Philosophy</th><th>Disposition</th><th>Confidence</th><th>Agrees?</th>' +
      '</tr></thead><tbody>';

  (p.opinions || []).forEach(function(op) {
    body += '<tr>' +
      '<td>' + escapeHtml(op.judge_name) + '</td>' +
      '<td>' + escapeHtml(op.philosophy) + '</td>' +
      '<td style="color:' + dispositionColor(op.disposition) + '">' + op.disposition.replace(/_/g, ' ') + '</td>' +
      '<td>' + (op.confidence * 100).toFixed(0) + '%</td>' +
      '<td>' + (op.agrees_with_majority ?
        '<span style="color:var(--green);">Yes</span>' :
        '<span style="color:var(--red);">No (Dissent)</span>') + '</td>' +
    '</tr>';
  });
  body += '</tbody></table></div></div>';

  // Step 3: Key reasoning differences
  body += '<div class="why-step">' +
    '<div class="why-step-number">3</div>' +
    '<div class="why-step-content">' +
      '<h4>Individual Reasoning</h4>';

  (p.opinions || []).forEach(function(op) {
    var borderColor = op.agrees_with_majority ? 'var(--green)' : 'var(--red)';
    body += '<div class="why-judge-reasoning" style="border-left:3px solid ' + borderColor + ';">' +
      '<div style="display:flex;justify-content:space-between;align-items:center;">' +
        '<strong>' + escapeHtml(op.judge_name) + '</strong>' +
        '<span class="why-judge-tag" style="background:' + (op.agrees_with_majority ? 'var(--green)' : 'var(--red)') + ';">' +
          (op.agrees_with_majority ? 'MAJORITY' : 'DISSENT') + '</span>' +
      '</div>' +
      '<p style="margin:0.5rem 0;">' + escapeHtml(op.reasoning_summary || '') + '</p>' +
      (op.key_factors && op.key_factors.length ?
        '<div style="margin-top:0.5rem;"><strong>Key factors this judge considered:</strong><ul>' +
        op.key_factors.map(function(f) { return '<li>' + escapeHtml(f) + '</li>'; }).join('') +
        '</ul></div>' : '') +
      (op.cited_precedents && op.cited_precedents.length ?
        '<div style="margin-top:0.5rem;"><strong>Cited precedents:</strong> ' +
        op.cited_precedents.map(function(pr) {
          return '<span class="clickable-rule" onclick="lookupRule(\'' + escapeHtml(pr).replace(/'/g, "\\'") + '\')" style="cursor:pointer;">' + escapeHtml(pr) + '</span>';
        }).join(', ') +
        '</div>' : '') +
    '</div>';
  });
  body += '</div></div>';

  body += '<div class="why-step">' +
    '<div class="why-step-number">4</div>' +
    '<div class="why-step-content">' +
      '<h4>Final Vote: ' + p.majority_vote + '-' + (p.panel_size - p.majority_vote) + '</h4>' +
      '<p>' + (p.is_unanimous ?
        'The panel reached a <strong style="color:var(--green);">unanimous</strong> decision, indicating strong consensus across different judicial perspectives.' :
        'The panel was <strong style="color:var(--amber);">divided</strong>, reflecting genuine disagreement about how the law should be applied in this case. The dissenting judge(s) identified valid concerns that the majority addressed but ultimately did not find persuasive.') +
      '</p>' +
    '</div></div>';

  body += '</div>';

  openModal('Panel Decision — Reasoning Explained', body);
}

// ============================================================
// 27. RISK ASSESSMENT REASONING EXPLAINER
// ============================================================
function openWhyRiskResult() {
  if (!lastRisk) return;
  var r = lastRisk;

  var body = '<div class="why-result-container">';

  body += '<div class="why-step">' +
    '<div class="why-step-number">1</div>' +
    '<div class="why-step-content">' +
      '<h4>Risk Level Determination</h4>' +
      '<p>The litigation risk was assessed as <strong style="color:' +
        ({low:'var(--green)',moderate:'var(--amber)',high:'var(--red)',very_low:'var(--green)',extreme:'var(--red)'}[r.litigation_risk_level] || 'var(--text-muted)') + ';">' +
        r.litigation_risk_level.replace(/_/g, ' ').toUpperCase() + '</strong>. This assessment considers:</p>' +
      '<ul>' +
        '<li>The relative strength of each party\'s evidence and arguments</li>' +
        '<li>The clarity and applicability of relevant legal standards</li>' +
        '<li>The likelihood of prevailing at trial for each party</li>' +
        '<li>Identified risk factors that could affect the outcome</li>' +
      '</ul>' +
    '</div></div>';

  (r.parties || []).forEach(function(party, idx) {
    var gradeColorMap = { A: '#22c55e', B: '#84cc16', C: '#eab308', D: '#f97316', F: '#ef4444' };
    var gc = gradeColorMap[party.overall_grade] || '#888';

    body += '<div class="why-step">' +
      '<div class="why-step-number" style="background:' + gc + ';">' + party.overall_grade + '</div>' +
      '<div class="why-step-content">' +
        '<h4>' + escapeHtml(party.party_name) + ' (' + escapeHtml(party.role) + ')</h4>' +
        '<div class="why-risk-scores">' +
          '<div class="why-risk-score-item">' +
            '<span>Win Probability</span>' +
            '<div class="why-bar-track"><div class="why-bar-fill" style="width:' + (party.win_probability * 100) + '%;background:var(--gold);"></div></div>' +
            '<span style="color:var(--gold);">' + (party.win_probability * 100).toFixed(0) + '%</span>' +
          '</div>' +
          '<div class="why-risk-score-item">' +
            '<span>Evidence Score</span>' +
            '<div class="why-bar-track"><div class="why-bar-fill" style="width:' + (party.evidence_score * 100) + '%;background:var(--blue);"></div></div>' +
            '<span style="color:var(--blue);">' + (party.evidence_score * 100).toFixed(0) + '%</span>' +
          '</div>' +
          '<div class="why-risk-score-item">' +
            '<span>Argument Score</span>' +
            '<div class="why-bar-track"><div class="why-bar-fill" style="width:' + (party.argument_score * 100) + '%;background:var(--purple);"></div></div>' +
            '<span style="color:var(--purple);">' + (party.argument_score * 100).toFixed(0) + '%</span>' +
          '</div>' +
        '</div>';

    if (party.strengths && party.strengths.length) {
      body += '<div style="margin-top:0.75rem;"><strong style="color:var(--green);">Strengths:</strong><ul>' +
        party.strengths.map(function(s) { return '<li style="color:var(--text-secondary);">' + escapeHtml(s) + '</li>'; }).join('') + '</ul></div>';
    }
    if (party.weaknesses && party.weaknesses.length) {
      body += '<div style="margin-top:0.5rem;"><strong style="color:var(--red);">Weaknesses:</strong><ul>' +
        party.weaknesses.map(function(w) { return '<li style="color:var(--text-secondary);">' + escapeHtml(w) + '</li>'; }).join('') + '</ul></div>';
    }
    if (party.risk_factors && party.risk_factors.length) {
      body += '<div style="margin-top:0.5rem;"><strong style="color:var(--amber);">Risk Factors:</strong><ul>' +
        party.risk_factors.map(function(rf) { return '<li style="color:var(--text-secondary);">' + escapeHtml(rf) + '</li>'; }).join('') + '</ul></div>';
    }

    body += '</div></div>';
  });

  body += '<div class="why-step">' +
    '<div class="why-step-number">&#10003;</div>' +
    '<div class="why-step-content">' +
      '<h4>Recommendation</h4>' +
      '<p>' + escapeHtml(r.recommendation) + '</p>' +
    '</div></div>';

  body += '</div>';
  openModal('Risk Assessment — Detailed Breakdown', body);
}

// ============================================================
// 28. SETTLEMENT REASONING EXPLAINER
// ============================================================
function openWhySettlementResult() {
  if (!lastSettlement) return;
  var st = lastSettlement;
  var d = st.damages_estimate;
  var s = st.settlement_range;

  var body = '<div class="why-result-container">';

  body += '<div class="why-step">' +
    '<div class="why-step-number">1</div>' +
    '<div class="why-step-content">' +
      '<h4>Damages Calculation</h4>' +
      '<p>The system estimated total damages of <strong style="color:var(--gold);">' + fmtMoney(d.total) + '</strong> based on:</p>' +
      '<table class="why-compare-table"><thead><tr><th>Component</th><th>Amount</th><th>Explanation</th></tr></thead><tbody>' +
        '<tr><td>Compensatory</td><td>' + fmtMoney(d.compensatory) + '</td><td>Direct losses suffered by the injured party</td></tr>' +
        '<tr><td>Consequential</td><td>' + fmtMoney(d.consequential) + '</td><td>Indirect but foreseeable losses flowing from the breach/harm</td></tr>' +
        '<tr><td>Punitive</td><td>' + fmtMoney(d.punitive) + '</td><td>' + (d.punitive > 0 ? 'Punitive damages to deter egregious conduct' : 'Not applicable in this case type') + '</td></tr>' +
        '<tr style="font-weight:700;color:var(--gold);"><td>Total</td><td>' + fmtMoney(d.total) + '</td><td>Confidence: ' + (d.confidence * 100).toFixed(0) + '%</td></tr>' +
      '</tbody></table>' +
      '<p style="margin-top:0.5rem;color:var(--text-muted);font-size:0.85rem;">Basis: ' + escapeHtml(d.basis) + '</p>' +
    '</div></div>';

  body += '<div class="why-step">' +
    '<div class="why-step-number">2</div>' +
    '<div class="why-step-content">' +
      '<h4>Settlement Range Calculation</h4>' +
      '<p>The settlement range was calculated by adjusting the estimated damages based on each party\'s probability of winning:</p>' +
      '<div class="why-settlement-range">' +
        '<div class="why-range-visual">' +
          '<div class="why-range-bar">' +
            '<div class="why-range-low">Low<br>' + fmtMoney(s.low) + '</div>' +
            '<div class="why-range-mid">Recommended<br><strong>' + fmtMoney(s.recommended) + '</strong></div>' +
            '<div class="why-range-high">High<br>' + fmtMoney(s.high) + '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<p style="margin-top:0.75rem;color:var(--text-secondary);">' + escapeHtml(s.rationale) + '</p>' +
    '</div></div>';

  body += '<div class="why-step">' +
    '<div class="why-step-number">3</div>' +
    '<div class="why-step-content">' +
      '<h4>Litigation Cost Analysis</h4>' +
      '<p>Estimated cost to litigate this case through trial: <strong style="color:var(--red);">' + fmtMoney(st.cost_of_litigation_estimate) + '</strong></p>' +
      '<p>This estimate includes attorney fees, court costs, discovery expenses, expert witnesses, and other litigation expenses.</p>' +
      (st.should_settle ?
        '<p style="color:var(--green);margin-top:0.5rem;"><strong>Settlement is recommended</strong> because the potential litigation costs combined with the uncertainty of trial outcome make settling more cost-effective.</p>' :
        '<p style="color:var(--amber);margin-top:0.5rem;"><strong>Litigation may be preferable</strong> because the expected trial outcome justifies the cost of continuing to trial.</p>') +
    '</div></div>';

  if (st.risk_summary && st.risk_summary.parties) {
    body += '<div class="why-step">' +
      '<div class="why-step-number">4</div>' +
      '<div class="why-step-content">' +
        '<h4>Risk Factor Impact</h4>' +
        '<p>The settlement recommendation is influenced by each party\'s litigation risk:</p>' +
        '<div class="why-risk-scores">';
    st.risk_summary.parties.forEach(function(p) {
      body += '<div class="why-risk-score-item">' +
        '<span>' + escapeHtml(p.party_name) + ' (' + p.overall_grade + ')</span>' +
        '<div class="why-bar-track"><div class="why-bar-fill" style="width:' + (p.win_probability * 100) + '%;background:var(--gold);"></div></div>' +
        '<span>' + (p.win_probability * 100).toFixed(0) + '%</span>' +
      '</div>';
    });
    body += '</div></div></div>';
  }

  body += '</div>';
  openModal('Settlement Analysis — How It Was Calculated', body);
}

// ============================================================
// 29. LLM ENHANCEMENT INTEGRATION
// ============================================================
async function checkLLMStatus() {
  try {
    var resp = await fetch(API + '/llm/status');
    var data = await resp.json();
    llmAvailable = data.available;
    llmProvider = data.provider || '';
    updateLLMIndicator();
  } catch (err) {
    llmAvailable = false;
  }
}

function updateLLMIndicator() {
  var hint = document.querySelector('.header-hint');
  if (!hint) return;
  var existing = document.getElementById('llm-indicator');
  if (existing) existing.remove();
  var indicator = document.createElement('div');
  indicator.id = 'llm-indicator';
  indicator.className = 'llm-indicator';
  if (llmAvailable) {
    indicator.innerHTML = '<span class="llm-dot llm-dot-active"></span> AI: ' + escapeHtml(llmProvider);
    indicator.title = 'LLM provider connected: ' + llmProvider;
  } else {
    indicator.innerHTML = '<span class="llm-dot llm-dot-inactive"></span> AI: Not Connected';
    indicator.title = 'No LLM API key configured. Add GROQ_API_KEY, GEMINI_API_KEY, or OPENROUTER_API_KEY to Vercel environment variables.';
  }
  hint.parentNode.insertBefore(indicator, hint);
}

function collectCaseForLLM() {
  return lastCaseData || collectCase();
}

async function enhanceJudgment() {
  if (!lastJudgment) { showToast('No judgment to enhance.', 'error'); return; }
  if (!llmAvailable) {
    showToast('No LLM API configured. Add an API key in Vercel settings.', 'error');
    return;
  }
  var btn = document.getElementById('btn-enhance-judgment');
  if (btn) { btn.disabled = true; btn.textContent = 'Enhancing...'; }

  try {
    var resp = await fetch(API + '/llm/enhance-judgment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: collectCaseForLLM(), judgment: lastJudgment }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var data = await resp.json();
    if (data.error) {
      showToast('LLM error: ' + data.error, 'error');
      return;
    }
    showLLMEnhancement('AI-Enhanced Judgment Analysis', data);
    showToast('AI enhancement complete via ' + data.provider + '.', 'success');
  } catch (err) {
    showToast('Enhancement failed: ' + err.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = '<span class="btn-icon-sm">&#9733;</span> AI Enhance'; }
  }
}

async function enhancePanel() {
  if (!lastPanel) { showToast('No panel decision to enhance.', 'error'); return; }
  if (!llmAvailable) {
    showToast('No LLM API configured. Add an API key in Vercel settings.', 'error');
    return;
  }
  var btn = document.getElementById('btn-enhance-panel');
  if (btn) { btn.disabled = true; btn.textContent = 'Enhancing...'; }

  try {
    var resp = await fetch(API + '/llm/enhance-panel', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: collectCaseForLLM(), panel: lastPanel }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var data = await resp.json();
    if (data.error) {
      showToast('LLM error: ' + data.error, 'error');
      return;
    }
    showLLMEnhancement('AI-Enhanced Panel Analysis', data);
    showToast('AI enhancement complete via ' + data.provider + '.', 'success');
  } catch (err) {
    showToast('Enhancement failed: ' + err.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = '<span class="btn-icon-sm">&#9733;</span> AI Enhance'; }
  }
}

async function enhanceRisk() {
  if (!lastRisk) { showToast('No risk assessment to enhance.', 'error'); return; }
  if (!llmAvailable) {
    showToast('No LLM API configured. Add an API key in Vercel settings.', 'error');
    return;
  }
  var btn = document.getElementById('btn-enhance-risk');
  if (btn) { btn.disabled = true; btn.textContent = 'Enhancing...'; }

  try {
    var resp = await fetch(API + '/llm/enhance-risk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: collectCaseForLLM(), risk: lastRisk }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var data = await resp.json();
    if (data.error) {
      showToast('LLM error: ' + data.error, 'error');
      return;
    }
    showLLMEnhancement('AI-Enhanced Risk Analysis', data);
    showToast('AI enhancement complete via ' + data.provider + '.', 'success');
  } catch (err) {
    showToast('Enhancement failed: ' + err.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = '<span class="btn-icon-sm">&#9733;</span> AI Enhance'; }
  }
}

async function enhanceSettlement() {
  if (!lastSettlement) { showToast('No settlement analysis to enhance.', 'error'); return; }
  if (!llmAvailable) {
    showToast('No LLM API configured. Add an API key in Vercel settings.', 'error');
    return;
  }
  var btn = document.getElementById('btn-enhance-settlement');
  if (btn) { btn.disabled = true; btn.textContent = 'Enhancing...'; }

  try {
    var resp = await fetch(API + '/llm/enhance-settlement', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ case: collectCaseForLLM(), settlement: lastSettlement }),
    });
    if (!resp.ok) throw new Error(await resp.text());
    var data = await resp.json();
    if (data.error) {
      showToast('LLM error: ' + data.error, 'error');
      return;
    }
    showLLMEnhancement('AI-Enhanced Settlement Analysis', data);
    showToast('AI enhancement complete via ' + data.provider + '.', 'success');
  } catch (err) {
    showToast('Enhancement failed: ' + err.message, 'error');
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = '<span class="btn-icon-sm">&#9733;</span> AI Enhance'; }
  }
}

function showLLMEnhancement(title, data) {
  var body = '<div class="llm-enhancement">';
  body += '<div class="llm-provider-badge">Powered by ' + escapeHtml(data.provider) + ' (' + escapeHtml(data.model) + ')</div>';

  if (data.plain_english_summary) {
    body += '<div class="llm-section">' +
      '<h4 class="llm-section-title">Plain English Summary</h4>' +
      '<p class="llm-summary-text">' + escapeHtml(data.plain_english_summary) + '</p>' +
    '</div>';
  }

  if (data.enhanced_opinion) {
    body += '<div class="llm-section">' +
      '<h4 class="llm-section-title">AI-Enhanced Opinion</h4>' +
      '<div class="llm-opinion-text">' + formatLLMText(data.enhanced_opinion) + '</div>' +
    '</div>';
  }

  if (data.enhanced_reasoning) {
    body += '<div class="llm-section">' +
      '<h4 class="llm-section-title">Detailed Reasoning</h4>' +
      '<div class="llm-opinion-text">' + formatLLMText(data.enhanced_reasoning) + '</div>' +
    '</div>';
  }

  if (data.key_insights && data.key_insights.length) {
    body += '<div class="llm-section">' +
      '<h4 class="llm-section-title">Key Insights</h4>' +
      '<ul class="llm-insights-list">' +
      data.key_insights.map(function(insight) {
        return '<li class="llm-insight-item"><span class="llm-insight-icon">&#9733;</span> ' + escapeHtml(insight) + '</li>';
      }).join('') +
      '</ul></div>';
  }

  if (data.enhanced_dissent) {
    body += '<div class="llm-section llm-dissent-section">' +
      '<h4 class="llm-section-title" style="color:var(--red);">Counterargument / Dissent</h4>' +
      '<div class="llm-opinion-text">' + formatLLMText(data.enhanced_dissent) + '</div>' +
    '</div>';
  }

  body += '</div>';
  openModal(title, body);
}

function formatLLMText(text) {
  if (!text) return '';
  // Convert line breaks to <br> and escape HTML
  return escapeHtml(text).replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
}

// ============================================================
// 30. PARTICLE BACKGROUND SYSTEM
// ============================================================
function initParticles() {
  var canvas = document.getElementById('particles-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var particles = [];
  var numParticles = 60;
  var connectionDist = 120;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  for (var i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: -Math.random() * 0.2 - 0.05,
      size: Math.random() * 2 + 0.5,
      opacity: Math.random() * 0.3 + 0.1,
      color: Math.random() > 0.7 ? '167, 139, 250' : '212, 168, 67'
    });
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach(function(p) {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = canvas.width;
      if (p.x > canvas.width) p.x = 0;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) { p.y = canvas.height; p.vy = -Math.random() * 0.2 - 0.05; }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + p.color + ', ' + p.opacity + ')';
      ctx.fill();
    });

    // Draw connections
    for (var i = 0; i < particles.length; i++) {
      for (var j = i + 1; j < particles.length; j++) {
        var dx = particles[i].x - particles[j].x;
        var dy = particles[i].y - particles[j].y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < connectionDist) {
          var alpha = (1 - dist / connectionDist) * 0.08;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = 'rgba(212, 168, 67, ' + alpha + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(animate);
  }
  animate();
}

// ============================================================
// 31. ANIMATED NUMBER COUNTING
// ============================================================
function animateCounters() {
  document.querySelectorAll('.animated-counter').forEach(function(el) {
    var target = el.getAttribute('data-target');
    if (!target) return;
    var isPercent = target.indexOf('%') !== -1;
    var numTarget = parseInt(target);
    if (isNaN(numTarget)) { el.textContent = target; return; }
    var suffix = isPercent ? '%' : '';
    var duration = 1000;
    var start = Date.now();
    var startVal = 0;

    function update() {
      var elapsed = Date.now() - start;
      var progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      var eased = 1 - Math.pow(1 - progress, 3);
      var current = Math.round(startVal + (numTarget - startVal) * eased);
      el.textContent = current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  });
}

// ============================================================
// 32. CONFETTI BURST
// ============================================================
function fireConfetti() {
  var container = document.getElementById('confetti-container');
  if (!container) return;
  var colors = ['#d4a843', '#ecd278', '#34d399', '#60a5fa', '#a78bfa', '#fb7185', '#fbbf24'];
  var numPieces = 100;
  var pieces = [];

  for (var i = 0; i < numPieces; i++) {
    var piece = document.createElement('div');
    piece.className = 'confetti-piece';
    var color = colors[Math.floor(Math.random() * colors.length)];
    var size = Math.random() * 8 + 4;
    var shape = Math.random() > 0.5 ? '50%' : '0';
    piece.style.cssText =
      'width:' + size + 'px;height:' + (size * 0.6) + 'px;' +
      'background:' + color + ';' +
      'border-radius:' + shape + ';' +
      'left:' + (40 + Math.random() * 20) + '%;' +
      'top:30%;' +
      'opacity:1;' +
      'position:absolute;';
    container.appendChild(piece);
    pieces.push({
      el: piece,
      x: (40 + Math.random() * 20) / 100 * window.innerWidth,
      y: window.innerHeight * 0.3,
      vx: (Math.random() - 0.5) * 12,
      vy: -Math.random() * 15 - 5,
      rotation: Math.random() * 360,
      rotationSpeed: (Math.random() - 0.5) * 15,
      gravity: 0.4 + Math.random() * 0.2,
      opacity: 1,
      drag: 0.98
    });
  }

  var startTime = Date.now();
  function animateConfetti() {
    var elapsed = Date.now() - startTime;
    var allDone = true;
    pieces.forEach(function(p) {
      p.vy += p.gravity;
      p.vx *= p.drag;
      p.x += p.vx;
      p.y += p.vy;
      p.rotation += p.rotationSpeed;
      if (elapsed > 1500) p.opacity -= 0.02;
      if (p.opacity > 0) allDone = false;
      p.el.style.transform = 'translate(' + p.x + 'px, ' + p.y + 'px) rotate(' + p.rotation + 'deg)';
      p.el.style.opacity = Math.max(0, p.opacity);
    });
    if (!allDone && elapsed < 4000) {
      requestAnimationFrame(animateConfetti);
    } else {
      container.innerHTML = '';
    }
  }
  requestAnimationFrame(animateConfetti);
}

// ============================================================
// 33. TYPEWRITER EFFECT
// ============================================================
function typewriterEffect(element, text, speed) {
  speed = speed || 50;
  element.textContent = '';
  element.classList.add('typing-cursor');
  var idx = 0;
  function type() {
    if (idx < text.length) {
      element.textContent += text[idx];
      idx++;
      setTimeout(type, speed);
    } else {
      setTimeout(function() {
        element.classList.remove('typing-cursor');
      }, 1500);
    }
  }
  type();
}

// ============================================================
// 34. 3D CARD TILT EFFECT
// ============================================================
function initCardTilt() {
  document.querySelectorAll('.card-3d').forEach(function(card) {
    card.addEventListener('mousemove', function(e) {
      var rect = card.getBoundingClientRect();
      var x = e.clientX - rect.left;
      var y = e.clientY - rect.top;
      var centerX = rect.width / 2;
      var centerY = rect.height / 2;
      var tiltX = (y - centerY) / centerY * -5;
      var tiltY = (x - centerX) / centerX * 5;
      card.style.transform = 'perspective(800px) rotateX(' + tiltX + 'deg) rotateY(' + tiltY + 'deg) translateY(-4px) scale(1.02)';
    });
    card.addEventListener('mouseleave', function() {
      card.style.transform = '';
    });
  });
}

// ============================================================
// 35. TAB INDICATOR (Animated sliding underline)
// ============================================================
function initTabIndicator() {
  updateTabIndicator();
}

function updateTabIndicator() {
  var activeBtn = document.querySelector('.nav-btn.active');
  var indicator = document.getElementById('tab-indicator');
  if (!activeBtn || !indicator) return;
  var nav = activeBtn.parentElement;
  var navRect = nav.getBoundingClientRect();
  var btnRect = activeBtn.getBoundingClientRect();
  indicator.style.left = (btnRect.left - navRect.left) + 'px';
  indicator.style.width = btnRect.width + 'px';
}
