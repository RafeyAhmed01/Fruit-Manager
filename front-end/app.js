const API = 'http://localhost:8000';

(function() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();

function toggleTheme() {
  const html = document.documentElement;
  html.setAttribute('data-theme', html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  localStorage.setItem('theme', html.getAttribute('data-theme'));
}

function onMethodChange() {
  const method = document.getElementById('methodSelect').value;
  const btn = document.getElementById('actionBtn');
  btn.textContent = method === 'GET' ? 'Fetch' : method === 'POST' ? 'Add' : method === 'PUT' ? 'Update' : 'Delete';

  const entity = document.getElementById('entitySelect').value;
  const head = document.querySelector('#tableHead');
  head.innerHTML = (entity === 'categories'
    ? '<tr><th>ID</th><th>Name</th></tr>'
    : '<tr><th>ID</th><th>Name</th><th>Category / Extra</th><th>Price</th><th>Quantity</th></tr>');
  document.querySelector('#dataTable tbody').innerHTML = '';
  const box = document.getElementById('paramFields');
  box.innerHTML = '';

  if (method === 'GET') {
    document.getElementById('searchInput').placeholder = 'Search...';
    document.getElementById('searchInput').style.display = 'inline-block';
  } else if (method === 'DELETE') {
    document.getElementById('searchInput').placeholder = 'ID to delete';
    document.getElementById('searchInput').style.display = 'inline-block';
  } else if (method === 'POST') {
    document.getElementById('searchInput').style.display = 'none';
    if (entity === 'categories') {
      box.appendChild(makeLabel('Name'));
      box.appendChild(makeInput('paramName', 'name', 'e.g. Citrus'));
    } else if (entity === 'fruits') {
      box.appendChild(makeLabel('Name'));
      box.appendChild(makeInput('paramName', 'name', 'e.g. Orange'));
      box.appendChild(makeLabel('Category ID'));
      box.appendChild(makeInput('paramCategoryId', 'category_id', '1', 'number'));
      box.appendChild(makeLabel('Price'));
      box.appendChild(makeInput('paramPrice', 'price', '1.99', 'number'));
      box.appendChild(makeLabel('Quantity'));
      box.appendChild(makeInput('paramQuantity', 'quantity', '10', 'number'));
    }
  } else if (method === 'PUT') {
    document.getElementById('searchInput').style.display = 'inline-block';
    document.getElementById('searchInput').placeholder = 'Record ID (in URL)';
    if (entity === 'categories') {
      box.appendChild(makeLabel('Content'));
      box.appendChild(makeInput('paramName', 'name', 'new name'));
    } else if (entity === 'fruits') {
      box.appendChild(makeLabel('Content'));
      box.appendChild(makeInput('paramName', 'name', 'updated'));
      box.appendChild(makeLabel('Category ID'));
      box.appendChild(makeInput('paramCategoryId', 'category_id', '2', 'number'));
      box.appendChild(makeLabel('Price'));
      box.appendChild(makeInput('paramPrice', 'price', '1.99', 'number'));
      box.appendChild(makeLabel('Quantity'));
      box.appendChild(makeInput('paramQuantity', 'quantity', '10', 'number'));
    }
  }
}

function makeLabel(text) {
  const l = document.createElement('label');
  l.textContent = text;
  return l;
}

function makeInput(id, placeholder, value = '', type = 'text') {
  const i = document.createElement('input');
  i.id = id; i.placeholder = placeholder; i.value = value; i.type = type;
  return i;
}

function buildPayload() {
  const method = document.getElementById('methodSelect').value;
  const entity = document.getElementById('entitySelect').value;
  const payload = {};

  if (method === 'POST' || method === 'PUT') {
    if (entity === 'categories') {
      const val = document.getElementById('paramName')?.value || '';
      if (/^\d+$/.test(val.trim())) { alert('Category name must not be only a number.'); return null; }
      payload.name = val;
    } else if (entity === 'fruits') {
      const val = document.getElementById('paramName')?.value || '';
      if (/^\d+$/.test(val.trim())) { alert('Fruit name must not be only a number.'); return null; }
      payload.name = val;
      payload.category_id = parseInt(document.getElementById('paramCategoryId')?.value || '0', 10) || 0;
      if (method === 'POST') {
        payload.price = parseFloat(document.getElementById('paramPrice')?.value || '0') || 0;
        payload.quantity = parseInt(document.getElementById('paramQuantity')?.value || '0', 10) || 0;
      } else if (method === 'PUT') {
        payload.category_id = parseInt(document.getElementById('paramCategoryId')?.value || '0', 10) || 0;
        payload.price = parseFloat(document.getElementById('paramPrice')?.value || '0') || 0;
        payload.quantity = parseInt(document.getElementById('paramQuantity')?.value || '0', 10) || 0;
      }
    }
  }
  return payload;
}

async function runAction() {
  const method = document.getElementById('methodSelect').value;
  const entity = document.getElementById('entitySelect').value;
  const search = document.getElementById('searchInput').value.trim();
  let url = `${API}/${entity}`;

  if (method === 'GET' || method === 'DELETE') {
    const id = search ? `/${search}` : '';
    url = `${API}/${entity}${id}` + (method === 'GET' && search && isNaN(search) ? `?q=${encodeURIComponent(search)}` : '');
  } else if (method === 'PUT') {
    const id = search ? `/${search}` : '';
    url = `${API}/${entity}${id}`;
  }

  try {
    const payload = (method === 'POST' || method === 'PUT') ? buildPayload() : null;
    if (payload === null && (method === 'POST' || method === 'PUT')) return; // validation blocked
    const opts = { method };
    if (method === 'POST' || method === 'PUT') {
      opts.headers = { 'Content-Type': 'application/json' };
      opts.body = JSON.stringify(payload);
    }
    if (method === 'DELETE') {
      opts.headers = {};
    }
    const res = await fetch(url, opts);
    if (!res.ok && res.status === 404) {
      document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3"><pre style="padding:1rem;color:#b91c1c">Data not found (404)</pre></td></tr>`;
      return;
    }
    const data = await res.json().catch(() => ({}));
    if (method === 'DELETE' && res.ok) {
      document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3"><pre style="padding:0.75rem;color:#2b6cb0;font-weight:600">✓ Deleted successfully</pre></td></tr>`;
      return;
    }
    if (method === 'POST' || method === 'PUT') {
      document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3"><pre style="padding:0.75rem;color:#2b6cb0;font-weight:600">✓ Submitted successfully</pre></td></tr>`;
      return;
    }
    if (Array.isArray(data) || (data && typeof data === 'object' && data.id !== undefined)) renderTable(entity, data);
    else if (data && data.detail) {
      document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3"><pre style="padding:1rem;color:#b91c1c">${data.detail}</pre></td></tr>`;
    } else {
      document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3">No data returned</td></tr>`;
    }
  } catch (e) {
    document.querySelector('#dataTable tbody').innerHTML = `<tr><td colspan="3">Failed (${method})</td></tr>`;
  }
}

function renderTable(entity, data) {
  const tbody = document.querySelector('#dataTable tbody');
  const head = document.querySelector('#tableHead');
  tbody.innerHTML = '';
  if (entity === 'categories') {
    head.innerHTML = '<tr><th>ID</th><th>Name</th></tr>';
  } else {
    head.innerHTML = '<tr><th>ID</th><th>Name</th><th>Category / Extra</th><th>Price</th><th>Quantity</th></tr>';
  }
  const rows = Array.isArray(data) ? data : [data];
  rows.forEach(r => {
    if (!r || !r.id) return;
    const tr = document.createElement('tr');
    const extra = entity === 'categories' ? r.name : (r.category ? (r.category.name || r.category_id) : r.category_id);
    if (entity === 'categories') {
      tr.innerHTML = `<td>${r.id}</td><td>${r.name}</td>`;
    } else {
      const price = r.price !== undefined ? r.price : '—';
      const qty = r.quantity !== undefined ? r.quantity : '—';
      tr.innerHTML = `<td>${r.id}</td><td>${r.name}</td><td>${extra !== undefined ? extra : '—'}</td><td>${price}</td><td>${qty}</td>`;
    }
    tbody.appendChild(tr);
  });
}

onMethodChange();
