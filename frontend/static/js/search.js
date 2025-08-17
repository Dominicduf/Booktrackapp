async function searchBooks(query) {
  const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
  if (!res.ok) return [];
  return await res.json();
}

async function addToLibrary(item) {
  const resp = await fetch('/api/library', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
  });
  return await resp.json();
}

function renderResults(items) {
  const container = document.getElementById('results');
  container.innerHTML = '';
  for (const it of items) {
    const card = document.createElement('div');
    card.className = 'book';
    const img = document.createElement('img');
    img.className = 'thumb';
    img.src = it.thumbnail || '/static/placeholder.png';
    img.alt = it.title;

    const content = document.createElement('div');
    content.className = 'content';
    const h3 = document.createElement('h3');
    h3.textContent = it.title;
    const authors = document.createElement('div');
    authors.className = 'muted';
    authors.textContent = (it.authors || []).join(', ');
    const desc = document.createElement('div');
    desc.className = 'muted';
    desc.textContent = it.description ? it.description.slice(0, 160) + '…' : '';
    const actions = document.createElement('div');
    actions.className = 'actions';
    
    const statusSelect = document.createElement('select');
    statusSelect.className = 'select';
    statusSelect.innerHTML = `
      <option value="to_read">To Read</option>
      <option value="reading">Currently Reading</option>
      <option value="completed">Finished</option>
    `;
    
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = 'Add to library';
    btn.onclick = async () => {
      btn.disabled = true;
      try {
        const selectedStatus = statusSelect.value;
        await addToLibrary({...it, status: selectedStatus});
        btn.textContent = 'Added';
      } catch (e) {
        btn.textContent = 'Error';
      } finally {
        setTimeout(() => { btn.disabled = false; btn.textContent = 'Add to library'; }, 1200);
      }
    };
    
    actions.appendChild(statusSelect);
    actions.appendChild(btn);

    content.appendChild(h3);
    content.appendChild(authors);
    content.appendChild(desc);
    content.appendChild(actions);

    card.appendChild(img);
    card.appendChild(content);
    container.appendChild(card);
  }
}

let searchTimeout;

async function performSearch() {
  const q = document.getElementById('q').value.trim();
  if (!q) {
    document.getElementById('results').innerHTML = '';
    return;
  }
  const items = await searchBooks(q);
  renderResults(items);
}

document.getElementById('q').addEventListener('input', () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(performSearch, 300);
});

document.getElementById('search-btn').addEventListener('click', performSearch);

document.getElementById('q').addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    clearTimeout(searchTimeout);
    performSearch();
  }
});


