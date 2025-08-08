function qs(name) { return new URLSearchParams(location.search).get(name); }

async function fetchItem(googleId) {
  const res = await fetch(`/api/library/${encodeURIComponent(googleId)}`);
  if (!res.ok) return null;
  return res.json();
}

async function patchItem(googleId, payload) {
  const res = await fetch(`/api/library/${encodeURIComponent(googleId)}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

function renderStars(name, value) {
  const wrap = document.createElement('div');
  wrap.className = 'stars';
  for (let i = 1; i <= 5; i++) {
    const s = document.createElement('span');
    s.className = 'star' + (value >= i ? ' on' : '');
    s.textContent = '★';
    s.dataset.value = String(i);
    s.dataset.name = name;
    wrap.appendChild(s);
  }
  return wrap;
}

function render(item) {
  const { book, entry } = item;
  const root = document.getElementById('book-details');
  root.innerHTML = '';

  const head = document.createElement('div');
  head.style.display = 'grid';
  head.style.gridTemplateColumns = '120px 1fr';
  head.style.gap = '12px';

  const img = document.createElement('img');
  img.src = book.thumbnail || '/static/placeholder.png';
  img.alt = book.title; img.style.width = '120px'; img.style.borderRadius = '8px';

  const meta = document.createElement('div');
  const h2 = document.createElement('h2'); h2.textContent = book.title;
  const a = document.createElement('div'); a.className = 'muted'; a.textContent = (book.authors || []).join(', ');
  const pd = document.createElement('div'); pd.className = 'muted'; pd.textContent = book.published_date || '';
  meta.appendChild(h2); meta.appendChild(a); meta.appendChild(pd);

  head.appendChild(img); head.appendChild(meta);

  const form = document.createElement('form');
  form.className = 'card';
  form.innerHTML = `
    <label>Status</label>
    <select name="status" class="select">
      <option value="to_read" ${entry.status==='to_read'?'selected':''}>to-read</option>
      <option value="reading" ${entry.status==='reading'?'selected':''}>reading</option>
      <option value="finished" ${entry.status==='finished'?'selected':''}>finished</option>
    </select>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px;">
      <div>
        <label>Started At</label>
        <input type="datetime-local" name="started_at" class="select" value="${entry.started_at?entry.started_at.slice(0,16):''}">
      </div>
      <div>
        <label>Finished At</label>
        <input type="datetime-local" name="finished_at" class="select" value="${entry.finished_at?entry.finished_at.slice(0,16):''}">
      </div>
    </div>
    <label>My Rating</label>
    <div id="rating"></div>
    <label>My Notes</label>
    <textarea name="my_notes" placeholder="Notes...">${entry.my_notes || ''}</textarea>
    <div class="actions" style="margin-top:8px;">
      <button class="btn" type="submit">Save</button>
    </div>
  `;

  const ratingWrap = form.querySelector('#rating');
  const stars = renderStars('my_rating', entry.my_rating || 0);
  ratingWrap.appendChild(stars);
  ratingWrap.addEventListener('click', (e) => {
    const t = e.target;
    if (t.classList.contains('star')) {
      const val = Number(t.dataset.value);
      stars.querySelectorAll('.star').forEach((s, idx) => s.classList.toggle('on', idx < val));
      stars.dataset.value = String(val);
    }
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(form);
    const payload = Object.fromEntries(fd.entries());
    const ratingVal = Number(stars.dataset.value || 0);
    if (ratingVal > 0) payload.my_rating = ratingVal;
    // Convert empty strings to null for dates
    ['started_at','finished_at'].forEach(k => { if (!payload[k]) payload[k] = null; });
    await patchItem(book.google_id, payload);
  });

  root.appendChild(head);
  root.appendChild(document.createElement('div')).style.height = '12px';
  root.appendChild(form);
}

(async function init() {
  const gid = qs('google_id');
  if (!gid) return;
  const item = await fetchItem(gid);
  if (item) render(item);
})();


