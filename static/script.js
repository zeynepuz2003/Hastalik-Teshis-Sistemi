/* ── State ──────────────────────────────────────────────────────────────── */
let lastResult = null;

/* ── Symptom selection ──────────────────────────────────────────────────── */
function onSymptomChange() {
  const chips   = document.querySelectorAll('.symptom-chip');
  const counter = document.getElementById('symptom-counter');
  let count = 0;

  chips.forEach(chip => {
    const cb = chip.querySelector('input');
    if (cb.checked) {
      chip.classList.add('selected');
      count++;
    } else {
      chip.classList.remove('selected');
    }
  });

  counter.textContent = `${count} belirti seçildi`;
  counter.style.color = count > 0 ? '#4f8ef7' : '#8892b0';
}

function getSelected() {
  return Array.from(document.querySelectorAll('.symptom-chip input:checked'))
              .map(cb => cb.value);
}

function clearAll() {
  document.querySelectorAll('.symptom-chip input').forEach(cb => cb.checked = false);
  onSymptomChange();
  document.getElementById('placeholder').classList.remove('hidden');
  document.getElementById('results-content').classList.add('hidden');
}

/* ── Diagnose ───────────────────────────────────────────────────────────── */
async function diagnose() {
  const symptoms = getSelected();
  if (symptoms.length === 0) {
    showToast('En az bir belirti seçiniz!');
    return;
  }

  const btn    = document.getElementById('diagnose-btn');
  const btext  = document.getElementById('btn-text');
  const bspin  = document.getElementById('btn-spinner');

  btn.disabled = true;
  btext.textContent = 'Analiz ediliyor...';
  bspin.classList.remove('hidden');

  try {
    const res  = await fetch('/diagnose', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ symptoms }),
    });
    const data = await res.json();

    if (data.error) {
      showToast(data.error);
      return;
    }

    lastResult = data;
    renderResults(data);

  } catch (err) {
    showToast('Sunucu hatası: ' + err.message);
  } finally {
    btn.disabled = false;
    btext.textContent = 'Teşhis Yap';
    bspin.classList.add('hidden');
  }
}

/* ── Render ─────────────────────────────────────────────────────────────── */
function renderResults(data) {
  document.getElementById('placeholder').classList.add('hidden');
  document.getElementById('results-content').classList.remove('hidden');

  // badge
  document.getElementById('rules-badge').textContent =
    `${data.logic.rules_fired_count} kural ateşlendi`;

  renderDiagnoses(data.diagnoses);
  renderLogic(data.logic);
  renderMath(data.math, data.diagnoses);
  renderOptimization(data.optimization);
}

/* ── Diagnoses ──────────────────────────────────────────────────────────── */
function renderDiagnoses(diagnoses) {
  const container = document.getElementById('diagnoses-list');
  container.innerHTML = '';

  diagnoses.forEach((d, i) => {
    const card = document.createElement('div');
    card.className = 'diagnosis-card' + (i === 0 ? ' rank-1' : '');

    const rankColors = ['#4f8ef7','#7c5cfc','#2ecc71','#f1c40f','#e67e22'];
    const rc = rankColors[i] || '#8892b0';

    const matchedHtml = d.matched_symptoms.map(s =>
      `<span class="symp-tag">${s}</span>`
    ).join('');

    const logicBadge = d.logic_rules.length > 0
      ? `<span style="margin-left:8px;font-size:.7rem;background:rgba(124,92,252,.2);
          border:1px solid rgba(124,92,252,.4);border-radius:10px;padding:2px 8px;
          color:#c8b4ff">⚡ ${d.logic_rules.length} kural</span>`
      : '';

    card.innerHTML = `
      <div class="card-top">
        <div class="rank-badge" style="background:${rc}22;color:${rc};border:1.5px solid ${rc}">
          ${d.rank}
        </div>
        <div>
          <div class="disease-name" style="color:${d.color}">${d.name}${logicBadge}</div>
        </div>
      </div>
      <div class="disease-desc">${d.description}</div>

      <div class="confidence-row">
        <span class="conf-label">Genel Güven</span>
        <div class="conf-bar-wrap">
          <div class="conf-bar" style="width:0%;background:${d.color}" data-target="${d.final_score}"></div>
        </div>
        <span class="conf-value" style="color:${d.color}">${d.final_score}%</span>
      </div>

      <div class="confidence-row">
        <span class="conf-label">Bayes Olasılığı</span>
        <div class="conf-bar-wrap">
          <div class="conf-bar" style="width:0%;background:#4f8ef7"
               data-target="${Math.min(d.bayes_score * 20, 100).toFixed(1)}"></div>
        </div>
        <span class="conf-value" style="color:#4f8ef7">${d.bayes_score}%</span>
      </div>

      <div class="confidence-row">
        <span class="conf-label">Kosinüs Benzerliği</span>
        <div class="conf-bar-wrap">
          <div class="conf-bar" style="width:0%;background:#2ecc71"
               data-target="${Math.max(0, Math.min(d.cosine_sim * 100, 100)).toFixed(1)}"></div>
        </div>
        <span class="conf-value" style="color:#2ecc71">${(d.cosine_sim * 100).toFixed(1)}%</span>
      </div>

      <div class="matched-symptoms">${matchedHtml}</div>
    `;

    container.appendChild(card);
  });

  // Animate bars
  requestAnimationFrame(() => {
    setTimeout(() => {
      document.querySelectorAll('.conf-bar[data-target]').forEach(bar => {
        bar.style.width = bar.dataset.target + '%';
      });
    }, 80);
  });
}

/* ── Logic ──────────────────────────────────────────────────────────────── */
function renderLogic(logic) {
  const list = document.getElementById('logic-rules-list');
  list.innerHTML = '';

  if (logic.fired_rules.length === 0) {
    list.innerHTML = `<p style="color:var(--muted);font-size:.82rem">
      Seçili belirtiler için yeterli kural koşulu sağlanamadı.
      (En az 2-3 belirti gerekebilir)</p>`;
  } else {
    logic.fired_rules.forEach(r => {
      const conds = r.conditions.map(c => `<span class="cond-tag">${c}</span>`).join('');
      const card  = document.createElement('div');
      card.className = 'rule-card';
      card.innerHTML = `
        <div class="rule-id">${r.id} — ${r.disease}</div>
        <div class="rule-name">${r.name}</div>
        <div class="rule-fol">${r.fol}</div>
        <div class="rule-conditions">Koşullar: ${conds}</div>
        <div class="rule-conf">Güven Skoru: %${r.confidence}</div>
      `;
      list.appendChild(card);
    });
  }

  const chains = document.getElementById('mp-chains');
  if (logic.modus_ponens_chains.length > 0) {
    chains.textContent = logic.modus_ponens_chains.join('\n\n──────────────────────────────\n\n');
  } else {
    chains.textContent = 'Modus Ponens zinciri oluşturulmadı.';
  }
}

/* ── Math ───────────────────────────────────────────────────────────────── */
function renderMath(math, diagnoses) {
  const grid = document.getElementById('math-grid');
  grid.innerHTML = `
    <div class="math-card">
      <div class="val">${math.matrix_frobenius_norm}</div>
      <div class="lbl">M Frobenius Normu<br>‖M‖_F</div>
    </div>
    <div class="math-card">
      <div class="val">${math.symptom_vector_norm}</div>
      <div class="lbl">Belirti Vektörü Normu<br>‖v‖₂</div>
    </div>
    <div class="math-card">
      <div class="val">${math.n_symptoms_selected}</div>
      <div class="lbl">Seçili Belirti<br>Sayısı</div>
    </div>
    <div class="math-card">
      <div class="val">${math.top_eigenvalues[0]}</div>
      <div class="lbl">λ₁ (1. Özdeğer)<br>MᵀM kovaryans</div>
    </div>
    <div class="math-card">
      <div class="val">${math.explained_variance[0]}%</div>
      <div class="lbl">1. Bileşen Açıklanan<br>Varyans (PCA)</div>
    </div>
    <div class="math-card">
      <div class="val">${math.explained_variance[0] + math.explained_variance[1]}%</div>
      <div class="lbl">İlk 2 Bileşen<br>Kümülatif Varyans</div>
    </div>
  `;

  // Score table
  const tableDiv = document.getElementById('math-scores-table');
  const rows = diagnoses.slice(0, 5).map((d, i) =>
    `<tr>
      <td><span style="color:${d.color};font-weight:700">${i+1}. ${d.short || d.name}</span></td>
      <td style="color:#4f8ef7">${d.bayes_score}%</td>
      <td style="color:#2ecc71">${(d.cosine_sim * 100).toFixed(1)}%</td>
      <td style="color:#f1c40f">${d.logic_score}</td>
      <td style="color:#fff;font-weight:700">${d.final_score}%</td>
    </tr>`
  ).join('');

  tableDiv.innerHTML = `
    <table class="score-table">
      <thead>
        <tr>
          <th>Hastalık</th>
          <th>Bayes P(H|v)</th>
          <th>cos(M_i, v)</th>
          <th>Mantık</th>
          <th>Hibrit Skor</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `;
}

/* ── Optimization ───────────────────────────────────────────────────────── */
function renderOptimization(opt) {
  // Stats
  const statsDiv = document.getElementById('opt-stats');
  const impColor = opt.improvement > 0 ? '#2ecc71' : '#8892b0';
  statsDiv.innerHTML = `
    <div class="stat-card">
      <div class="sv" style="color:#8892b0">${opt.initial_score}%</div>
      <div class="sl">Başlangıç<br>Güveni</div>
    </div>
    <div class="stat-card">
      <div class="sv">${opt.final_score}%</div>
      <div class="sl">Optimize<br>Güven</div>
    </div>
    <div class="stat-card">
      <div class="sv" style="color:${impColor}">+${opt.improvement}%</div>
      <div class="sl">İyileşme<br>(Δ)</div>
    </div>
    <div class="stat-card">
      <div class="sv" style="color:#f1c40f">${opt.iterations_run}</div>
      <div class="sl">İterasyon<br>${opt.converged ? '✓ Yakınsadı' : 'Çalıştı'}</div>
    </div>
  `;

  // Chart
  drawOptChart(opt.history);

  // Weights
  const wDiv = document.getElementById('weights-chart');
  wDiv.innerHTML = '';
  const maxW = Math.max(...Object.values(opt.top_weights), 1.5);
  Object.entries(opt.top_weights).forEach(([label, w]) => {
    const pct = Math.min((w / maxW) * 100, 100).toFixed(1);
    const color = w > 1.2 ? '#4f8ef7' : w < 0.8 ? '#e74c3c' : '#8892b0';
    const row = document.createElement('div');
    row.className = 'weights-row';
    row.innerHTML = `
      <span class="weight-label">${label}</span>
      <div class="weight-bar-wrap">
        <div class="weight-bar" style="width:0%;background:${color}" data-target="${pct}"></div>
      </div>
      <span class="weight-val" style="color:${color}">${w.toFixed(3)}</span>
    `;
    wDiv.appendChild(row);
  });

  setTimeout(() => {
    document.querySelectorAll('.weight-bar[data-target]').forEach(b => {
      b.style.width = b.dataset.target + '%';
    });
  }, 100);
}

function drawOptChart(history) {
  const canvas = document.getElementById('opt-chart');
  const ctx    = canvas.getContext('2d');
  const W = canvas.offsetWidth || 600;
  const H = 180;
  canvas.width  = W * window.devicePixelRatio;
  canvas.height = H * window.devicePixelRatio;
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);

  const pad = { top: 20, right: 20, bottom: 30, left: 50 };
  const cW  = W - pad.left - pad.right;
  const cH  = H - pad.top  - pad.bottom;

  const vals = history.length > 200
    ? history.filter((_, i) => i % Math.ceil(history.length / 200) === 0)
    : history;

  const minV = Math.min(...vals);
  const maxV = Math.max(...vals, minV + 1);

  ctx.clearRect(0, 0, W, H);

  // Grid lines
  ctx.strokeStyle = 'rgba(45,49,84,.6)';
  ctx.lineWidth   = 0.8;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + cH - (i / 4) * cH;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(pad.left + cW, y);
    ctx.stroke();
    ctx.fillStyle = '#8892b0';
    ctx.font = '10px sans-serif';
    ctx.fillText(((minV + (i / 4) * (maxV - minV))).toFixed(1) + '%', 2, y + 4);
  }

  // Gradient fill
  const grad = ctx.createLinearGradient(0, pad.top, 0, pad.top + cH);
  grad.addColorStop(0, 'rgba(79,142,247,.3)');
  grad.addColorStop(1, 'rgba(79,142,247,.02)');

  ctx.beginPath();
  vals.forEach((v, i) => {
    const x = pad.left + (i / (vals.length - 1)) * cW;
    const y = pad.top  + cH - ((v - minV) / (maxV - minV)) * cH;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.lineTo(pad.left + cW, pad.top + cH);
  ctx.lineTo(pad.left,      pad.top + cH);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // Line
  ctx.beginPath();
  ctx.strokeStyle = '#4f8ef7';
  ctx.lineWidth   = 2;
  vals.forEach((v, i) => {
    const x = pad.left + (i / (vals.length - 1)) * cW;
    const y = pad.top  + cH - ((v - minV) / (maxV - minV)) * cH;
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Labels
  ctx.fillStyle = '#8892b0';
  ctx.font      = '11px sans-serif';
  ctx.fillText('0', pad.left, pad.top + cH + 18);
  ctx.fillText(vals.length + ' adım', pad.left + cW - 50, pad.top + cH + 18);
  ctx.fillText('Objektif f(w) (%)', pad.left, pad.top - 6);
}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
function switchTab(name) {
  document.querySelectorAll('.tab').forEach((t, i) => {
    const names = ['logic', 'math', 'opt'];
    t.classList.toggle('active', names[i] === name);
  });

  document.querySelectorAll('.tab-content').forEach(tc => {
    tc.classList.remove('active');
    tc.classList.add('hidden');
  });

  const target = document.getElementById('tab-' + name);
  if (target) {
    target.classList.remove('hidden');
    target.classList.add('active');
    if (name === 'opt' && lastResult) {
      setTimeout(() => drawOptChart(lastResult.optimization.history), 60);
    }
  }
}

/* ── Toast ──────────────────────────────────────────────────────────────── */
function showToast(msg) {
  const t = document.createElement('div');
  t.style.cssText = `
    position:fixed;bottom:24px;left:50%;transform:translateX(-50%);
    background:#e74c3c;color:#fff;padding:10px 20px;border-radius:8px;
    font-size:.85rem;z-index:9999;box-shadow:0 4px 16px rgba(0,0,0,.4);
  `;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

/* ── Enter key support ──────────────────────────────────────────────────── */
document.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.target.matches('input')) diagnose();
});
