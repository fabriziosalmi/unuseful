document.addEventListener('DOMContentLoaded', () => {
    // Theme toggling
    const toggleTheme = document.getElementById('toggleTheme');
    let isDarkMode = localStorage.getItem('theme') === 'dark';
    
    function setTheme(dark) {
        document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
        localStorage.setItem('theme', dark ? 'dark' : 'light');
        isDarkMode = dark;
    }
    
    setTheme(isDarkMode);
    
    toggleTheme.addEventListener('click', () => {
        setTheme(!isDarkMode);
    });

    // View toggling (grid/list)
    const toggleView = document.getElementById('toggleView');
    const fragmentsContainer = document.getElementById('fragmentsContainer');
    let isGridView = localStorage.getItem('view') !== 'list';
    
    function setView(grid) {
        fragmentsContainer.style.display = grid ? 'grid' : 'block';
        localStorage.setItem('view', grid ? 'grid' : 'list');
        isGridView = grid;
    }
    
    setView(isGridView);
    
    toggleView.addEventListener('click', () => {
        setView(!isGridView);
    });

    // Sort fragments according to selected option
    function sortFragments(fragments, sortBy) {
        const [field, direction] = sortBy.split('-');
        const desc = direction === 'desc' ? -1 : 1;
        
        return fragments.sort((a, b) => {
            let valueA, valueB;
            
            switch (field) {
                case 'date':
                    valueA = new Date(a.timestamp);
                    valueB = new Date(b.timestamp);
                    break;
                case 'size':
                    valueA = a.size;
                    valueB = b.size;
                    break;
                case 'id':
                default:
                    valueA = a.id;
                    valueB = b.id;
                    break;
            }
            
            if (valueA < valueB) return -1 * desc;
            if (valueA > valueB) return 1 * desc;
            return 0;
        });
    }

    // Search and filtering
    const searchInput = document.getElementById('searchInput');
    const typeFilter = document.getElementById('typeFilter');
    const patternFilter = document.getElementById('patternFilter');
    const sortSelect = document.getElementById('sortBy');
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    function applySort() {
        const fragments = Array.from(fragmentsContainer.children);
        const sortBy = sortSelect.value;
        
        sortFragments(fragments, sortBy).forEach(fragment => {
            fragmentsContainer.appendChild(fragment);
        });
    }
    
    const filterFragments = debounce(() => {
        const searchTerm = searchInput.value.toLowerCase();
        const typeValue = typeFilter.value;
        const patternValue = patternFilter.value;
        const activeChipTags = Array.from(document.querySelectorAll('.chip.active')).map(c => c.textContent);
        
        document.querySelectorAll('.fragment-card').forEach(card => {
            const title = card.querySelector('.fragment-title').textContent.toLowerCase();
            const content = card.querySelector('.fragment-content').textContent.toLowerCase();
            const type = card.dataset.type;
            const patterns = (card.dataset.patterns || '').split(',');
            
            const matchesSearch = !searchTerm || 
                                title.includes(searchTerm) || 
                                content.includes(searchTerm);
            
            const matchesType = !typeValue || type === typeValue;
            
            const matchesPattern = (!patternValue || patterns.some(p => p.includes(patternValue))) &&
                                 (activeChipTags.length === 0 || activeChipTags.every(t => patterns.includes(t)));
            
            card.style.display = (matchesSearch && matchesType && matchesPattern) ? '' : 'none';
        });

        // Update fragment count
        const visibleFragments = document.querySelectorAll('.fragment-card[style="display: ;"]').length;
        document.getElementById('fragmentCount').textContent = String(visibleFragments);
    }, 300);
    
    searchInput.addEventListener('input', filterFragments);
    typeFilter.addEventListener('change', filterFragments);
    patternFilter.addEventListener('change', filterFragments);
    sortSelect.addEventListener('change', applySort);

    // Utility: language mapping
    function mapLanguage(fileType) {
        const map = {
            'python': 'python',
            'ipynb': 'json',
            'json': 'json',
            'js': 'javascript',
            'ts': 'typescript',
            'md': 'markdown'
        };
        return map[fileType] || 'markup';
    }

    // Load fragments from embedded data
    async function loadFragments() {
        try {
            // Check for shared fragment ID in URL
            const params = new URLSearchParams(window.location.search);
            const sharedFragmentId = params.get('id');

            let fragments = FRAGMENTS_DATA.fragments;
            
            // If there's a shared fragment ID, move it to the top
            if (sharedFragmentId) {
                const sharedFragment = fragments.find(f => f.id === parseInt(sharedFragmentId));
                if (sharedFragment) {
                    fragments = [
                        sharedFragment,
                        ...fragments.filter(f => f.id !== parseInt(sharedFragmentId))
                    ];
                }
            }
            
            if (!fragments || !fragments.length) {
                fragmentsContainer.innerHTML = '<p>Nessun frammento trovato.</p>';
                return;
            }
            
            // Build tag chips dynamically
            const allTags = new Set();
            fragments.forEach(f => (f.patterns || '').split(',').forEach(p => p && allTags.add(p.trim())));
            const chipsContainer = document.getElementById('tagChips');
            chipsContainer.innerHTML = '';
            allTags.forEach(tag => {
                const chip = document.createElement('button');
                chip.className = 'chip';
                chip.textContent = tag;
                chip.addEventListener('click', () => {
                    chip.classList.toggle('active');
                    filterFragments();
                });
                chipsContainer.appendChild(chip);
            });
            
            // Sort and display fragments
            const sortBy = document.getElementById('sortBy').value;
            fragments = sortFragments(fragments, sortBy);
            document.getElementById('fragmentCount').textContent = String(fragments.length);
            
            fragments.forEach(fragment => {
                const card = document.createElement('div');
                card.className = 'fragment-card';
                card.dataset.type = fragment.file_type;
                card.dataset.patterns = fragment.patterns || '';
                card.dataset.id = fragment.id;
                
                const lang = mapLanguage(fragment.file_type);
                
                card.innerHTML = `
                    <div class="fragment-header">
                        <h3 class="fragment-title">${fragment.title}</h3>
                        <div class="fragment-meta">
                            Frammento #${String(fragment.id).padStart(4, '0')} • ${new Date(fragment.timestamp).toLocaleDateString('it-IT')}
                        </div>
                    </div>
                    <pre class="fragment-content"><code class="language-${lang}">${fragment.content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>
                    <div class="fragment-tags">
                        ${(fragment.patterns || '').split(',').map(p => `<span class="tag">${p}</span>`).join('')}
                    </div>
                `;
                
                // Add action buttons
                const actions = document.createElement('div');
                actions.className = 'fragment-actions';
                
                const shareBtn = document.createElement('button');
                shareBtn.className = 'share-btn';
                shareBtn.textContent = 'Condividi';
                shareBtn.setAttribute('aria-label', 'Condividi frammento');
                
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.textContent = 'Copia';
                copyBtn.setAttribute('aria-label', 'Copia codice');
                
                actions.appendChild(shareBtn);
                actions.appendChild(copyBtn);
                card.appendChild(actions);
                
                fragmentsContainer.appendChild(card);
                Prism.highlightElement(card.querySelector('code'));
                
                // Share functionality
                shareBtn.addEventListener('click', () => {
                    const params = new URLSearchParams();
                    params.set('id', fragment.id);
                    const shareUrl = `${window.location.origin}${window.location.pathname}?${params.toString()}`;
                    
                    const overlay = document.createElement('div');
                    overlay.className = 'overlay';
                    
                    const dialog = document.createElement('div');
                    dialog.className = 'share-dialog';
                    dialog.innerHTML = `
                        <h3>Condividi frammento</h3>
                        <p>Copia questo link per condividere il frammento:</p>
                        <input type="text" class="share-link" value="${shareUrl}" readonly>
                        <div class="buttons">
                            <button class="copy-link">Copia link</button>
                            <button class="close-dialog">Chiudi</button>
                        </div>
                    `;
                    
                    document.body.appendChild(overlay);
                    document.body.appendChild(dialog);
                    
                    const closeDialog = () => {
                        overlay.remove();
                        dialog.remove();
                    };
                    
                    dialog.querySelector('.copy-link').addEventListener('click', async () => {
                        const input = dialog.querySelector('.share-link');
                        input.select();
                        await navigator.clipboard.writeText(input.value);
                        dialog.querySelector('.copy-link').textContent = 'Copiato!';
                        setTimeout(() => {
                            dialog.querySelector('.copy-link').textContent = 'Copia link';
                        }, 1500);
                    });
                    
                    dialog.querySelector('.close-dialog').addEventListener('click', closeDialog);
                    overlay.addEventListener('click', closeDialog);
                });
                
                // Copy to clipboard
                copyBtn.addEventListener('click', async () => {
                    try {
                        const code = card.querySelector('code').textContent;
                        await navigator.clipboard.writeText(code);
                        copyBtn.textContent = 'Copiato!';
                        setTimeout(() => (copyBtn.textContent = 'Copia'), 1500);
                    } catch (e) {
                        console.error('Copy failed', e);
                    }
                });
            });
            
            // Highlight shared fragment if any
            if (sharedFragmentId) {
                const sharedCard = fragmentsContainer.querySelector(`[data-id="${sharedFragmentId}"]`);
                if (sharedCard) {
                    sharedCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    sharedCard.style.animation = 'highlight 2s';
                }
            }
            
        } catch (error) {
            console.error('Error loading fragments:', error);
            fragmentsContainer.innerHTML = '<p>Errore nel caricamento dei frammenti.</p>';
        }
    }

    // Initialize visualizations
    function initializeVisualizations(fragments) {
        const patternChart = new Chart(document.getElementById('patternChart'), {
            type: 'doughnut',
            data: {
                labels: ['Struttura', 'Funzione', 'Tensore', 'Modello', 'Apprendimento'],
                datasets: [{
                    data: [
                        fragments.filter(f => f.patterns?.includes('struttura')).length,
                        fragments.filter(f => f.patterns?.includes('funzione')).length,
                        fragments.filter(f => f.patterns?.includes('tensore')).length,
                        fragments.filter(f => f.patterns?.includes('modello')).length,
                        fragments.filter(f => f.patterns?.includes('apprendimento')).length
                    ],
                    backgroundColor: [
                        '#00b894',
                        '#00cec9',
                        '#0984e3',
                        '#6c5ce7',
                        '#fd79a8'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    // Add highlight animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes highlight {
            0% { background-color: var(--accent-color); }
            100% { background-color: var(--card-background); }
        }
    `;
    document.head.appendChild(style);

    // Start loading fragments
    loadFragments();
});

document.addEventListener('DOMContentLoaded', () => {
    // Theme toggling
    const toggleTheme = document.getElementById('toggleTheme');
    let isDarkMode = localStorage.getItem('theme') === 'dark';
    
    function setTheme(dark) {
        document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
        localStorage.setItem('theme', dark ? 'dark' : 'light');
        isDarkMode = dark;
    }
    
    setTheme(isDarkMode);
    
    toggleTheme.addEventListener('click', () => {
        setTheme(!isDarkMode);
    });

    // View toggling (grid/list)
    const toggleView = document.getElementById('toggleView');
    const fragmentsContainer = document.getElementById('fragmentsContainer');
    let isGridView = localStorage.getItem('view') !== 'list';
    
    function setView(grid) {
        fragmentsContainer.style.display = grid ? 'grid' : 'block';
        localStorage.setItem('view', grid ? 'grid' : 'list');
        isGridView = grid;
    }
    
    setView(isGridView);
    
    toggleView.addEventListener('click', () => {
        setView(!isGridView);
    });

    // Search and filtering
    const searchInput = document.getElementById('searchInput');
    const typeFilter = document.getElementById('typeFilter');
    const patternFilter = document.getElementById('patternFilter');
    
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    const filterFragments = debounce(() => {
        const searchTerm = searchInput.value.toLowerCase();
        const typeValue = typeFilter.value;
            const patternValue = patternFilter.value;

            const activeChipTags = Array.from(document.querySelectorAll('.chip.active')).map(c => c.textContent);
            
            document.querySelectorAll('.fragment-card').forEach(card => {
            const title = card.querySelector('.fragment-title').textContent.toLowerCase();
            const content = card.querySelector('.fragment-content').textContent.toLowerCase();
            const type = card.dataset.type;
            const patterns = card.dataset.patterns.split(',');
            
            const matchesSearch = !searchTerm || 
                                title.includes(searchTerm) || 
                                content.includes(searchTerm);
            
            const matchesType = !typeValue || type === typeValue;
            
            const matchesPattern = (!patternValue || patterns.some(p => p.includes(patternValue))) &&
                                   (activeChipTags.length === 0 || activeChipTags.every(t => patterns.includes(t)));
            
            card.style.display = (matchesSearch && matchesType && matchesPattern) ? '' : 'none';
        });
    }, 300);
    
    searchInput.addEventListener('input', filterFragments);
    typeFilter.addEventListener('change', filterFragments);
    patternFilter.addEventListener('change', filterFragments);

    // Utility: language mapping
    function mapLanguage(fileType) {
        const map = {
            python: 'python',
            ipynb: 'json',
            json: 'json',
            js: 'javascript',
            ts: 'typescript',
            md: 'markdown'
        };
        return map[fileType] || 'markup';
    }

    // Load fragments (embedded first, fallback to metadata JSON)
    async function loadFragments() {
        try {
            let fragments = [];
            if (typeof FRAGMENTS_DATA !== 'undefined' && FRAGMENTS_DATA.fragments) {
                fragments = FRAGMENTS_DATA.fragments;
            } else {
                const response = await fetch('/memorie/_metadata/index.json');
                const data = await response.json();
                fragments = data.fragments || [];
            }
            
            if (!fragments || !fragments.length) {
                fragmentsContainer.innerHTML = '<p>Nessun frammento trovato.</p>';
                return;
            }
            
            // Build tag chips dynamically
            const allTags = new Set();
            fragments.forEach(f => (f.patterns || '').split(',').forEach(p => p && allTags.add(p.trim())));
            const chipsContainer = document.getElementById('tagChips');
            chipsContainer.innerHTML = '';
            allTags.forEach(tag => {
                const chip = document.createElement('button');
                chip.className = 'chip';
                chip.textContent = tag;
                chip.addEventListener('click', () => {
                    chip.classList.toggle('active');
                    filterFragments();
                });
                chipsContainer.appendChild(chip);
            });

            // Sort fragments by ID (newest first)
            fragments.sort((a, b) => b.id - a.id);
            document.getElementById('fragmentCount').textContent = String(fragments.length);
            
            fragments.forEach(fragment => {
                const card = document.createElement('div');
                card.className = 'fragment-card';
                card.dataset.type = fragment.file_type;
                card.dataset.patterns = fragment.patterns || '';
                
                const lang = mapLanguage(fragment.file_type);
                
                card.innerHTML = `
                    <div class="fragment-header">
                        <h3 class="fragment-title">${fragment.title}</h3>
                        <div class="fragment-meta">
                            Frammento #${String(fragment.id).padStart(4, '0')} • ${new Date(fragment.timestamp).toLocaleDateString('it-IT')}
                        </div>
                    <button class="copy-btn" aria-label="Copia codice">Copia</button>
                    </div>
                    <pre class="fragment-content"><code class="language-${lang}">${fragment.content.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>
                    <div class="fragment-tags">
                        ${(fragment.patterns || '').split(',').map(p => `<span class="tag">${p}</span>`).join('')}
                    </div>
                `;
                
                fragmentsContainer.appendChild(card);
                Prism.highlightElement(card.querySelector('code'));
                
                // Copy to clipboard
                const copyBtn = card.querySelector('.copy-btn');
                copyBtn.addEventListener('click', async () => {
                    try {
                        const code = card.querySelector('code').textContent;
                        await navigator.clipboard.writeText(code);
                        copyBtn.textContent = 'Copiato!';
                        setTimeout(() => (copyBtn.textContent = 'Copia'), 1500);
                    } catch (e) {
                        console.error('Copy failed', e);
                    }
                });
            });
            
            // Initialize visualizations
            initializeVisualizations(fragments);
            
        } catch (error) {
            console.error('Error loading fragments:', error);
            fragmentsContainer.innerHTML = '<p>Errore nel caricamento dei frammenti.</p>';
        }
    }

    // Initialize visualizations
    function initializeVisualizations(fragments) {
        const patternChart = new Chart(document.getElementById('patternChart'), {
            type: 'doughnut',
            data: {
                labels: ['Struttura', 'Funzione', 'Tensore', 'Modello', 'Apprendimento'],
                datasets: [{
                    data: [
                        fragments.filter(f => f.patterns?.includes('struttura')).length,
                        fragments.filter(f => f.patterns?.includes('funzione')).length,
                        fragments.filter(f => f.patterns?.includes('tensore')).length,
                        fragments.filter(f => f.patterns?.includes('modello')).length,
                        fragments.filter(f => f.patterns?.includes('apprendimento')).length
                    ],
                    backgroundColor: [
                        '#00b894',
                        '#00cec9',
                        '#0984e3',
                        '#6c5ce7',
                        '#fd79a8'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Timeline visualization
        const timeline = document.getElementById('timeline');
        const dates = fragments.map(f => new Date(f.timestamp));
        const minDate = new Date(Math.min(...dates));
        const maxDate = new Date(Math.max(...dates));
        
        const timelineWidth = timeline.offsetWidth;
        const timeScale = timelineWidth / (maxDate - minDate);
        
        fragments.forEach(fragment => {
            const dot = document.createElement('div');
            dot.className = 'timeline-dot';
            dot.style.left = `${(new Date(fragment.timestamp) - minDate) * timeScale}px`;
            dot.title = `Frammento #${fragment.id}: ${fragment.title}`;
            timeline.appendChild(dot);
        });
    }

    // Start loading fragments
    loadFragments();
});
