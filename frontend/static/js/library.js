const listEl = document.getElementById('library-list');
const tabs = document.querySelectorAll('.tab');
let currentStatus = 'to_read';

async function fetchLibrary(status) {
  const url = status ? `/api/library?status=${encodeURIComponent(status)}` : '/api/library';
  const res = await fetch(url);
  return res.ok ? res.json() : [];
}

async function patchEntry(googleId, payload) {
  const res = await fetch(`/api/library/${encodeURIComponent(googleId)}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return res.json();
}

async function deleteEntry(googleId) {
  await fetch(`/api/library/${encodeURIComponent(googleId)}`, { method: 'DELETE' });
}

function renderStars(value, onChange) {
  const wrap = document.createElement('div');
  wrap.className = 'stars';
  for (let i = 1; i <= 5; i++) {
    const s = document.createElement('span');
    s.className = 'star' + (value >= i ? ' on' : '');
    s.textContent = '★';
    s.onclick = () => onChange(i);
    wrap.appendChild(s);
  }
  return wrap;
}

function renderList(items) {
  listEl.innerHTML = '';
  for (const { book, entry } of items) {
    const row = document.createElement('div');
    row.className = 'row';

    const img = document.createElement('img');
    img.src = book.thumbnail || '/static/placeholder.png';
    img.alt = book.title;

    const meta = document.createElement('div');
    meta.className = 'meta';
    const title = document.createElement('a');
    title.className = 'link';
    title.href = `/book?google_id=${encodeURIComponent(book.google_id)}`;
    title.textContent = book.title;
    const authors = document.createElement('div');
    authors.className = 'muted';
    authors.textContent = (book.authors || []).join(', ');
    meta.appendChild(title);
    meta.appendChild(authors);

    const controls = document.createElement('div');
    controls.className = 'controls';
    const select = document.createElement('select');
    select.className = 'select';
    ['to_read','reading','finished'].forEach(st => {
      const opt = document.createElement('option');
      opt.value = st; opt.textContent = st.replace('_','-');
      if (entry.status === st) opt.selected = true;
      select.appendChild(opt);
    });
    select.onchange = async () => {
      const newStatus = select.value;
      const previous = entry.status;
      entry.status = newStatus; // optimistic
      try { await patchEntry(book.google_id, { status: newStatus }); }
      catch { entry.status = previous; select.value = previous; }
    };

    const rating = renderStars(entry.my_rating || 0, async (v) => {
      const prev = entry.my_rating;
      entry.my_rating = v; // optimistic
      rating.querySelectorAll('.star').forEach((s, idx) => {
        s.classList.toggle('on', idx < v);
      });
      try { await patchEntry(book.google_id, { my_rating: v }); }
      catch { entry.my_rating = prev; renderList([{ book, entry }]); }
    });

    const remove = document.createElement('button');
    remove.className = 'btn';
    remove.textContent = 'Remove';
    remove.onclick = async () => {
      const saved = listEl.innerHTML;
      row.remove(); // optimistic
      try { await deleteEntry(book.google_id); }
      catch { listEl.innerHTML = saved; }
    };

    controls.appendChild(select);
    controls.appendChild(rating);
    controls.appendChild(remove);

    row.appendChild(img);
    row.appendChild(meta);
    row.appendChild(controls);
    listEl.appendChild(row);
  }
}

async function load(status) {
  currentStatus = status;
  const items = await fetchLibrary(status);
  renderList(items);
}

tabs.forEach(t => t.addEventListener('click', () => {
  tabs.forEach(s => s.classList.remove('active'));
  t.classList.add('active');
  load(t.dataset.status);
}));

load(currentStatus);


