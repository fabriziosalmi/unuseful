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
        
        document.querySelectorAll('.fragment-card').forEach(card => {
            const title = card.querySelector('.fragment-title').textContent.toLowerCase();
            const content = card.querySelector('.fragment-content').textContent.toLowerCase();
            const type = card.dataset.type;
            const patterns = card.dataset.patterns.split(',');
            
            const matchesSearch = !searchTerm || 
                                title.includes(searchTerm) || 
                                content.includes(searchTerm);
            
            const matchesType = !typeValue || type === typeValue;
            
            const matchesPattern = !patternValue || 
                                 patterns.some(p => p.includes(patternValue));
            
            card.style.display = (matchesSearch && matchesType && matchesPattern) ? '' : 'none';
        });
    }, 300);
    
    searchInput.addEventListener('input', filterFragments);
    typeFilter.addEventListener('change', filterFragments);
    patternFilter.addEventListener('change', filterFragments);

    // Load fragments from metadata
    async function loadFragments() {
        try {
            const response = await fetch('/memorie/_metadata/index.json');
            const data = await response.json();
            
            if (!data.fragments || !data.fragments.length) {
                fragmentsContainer.innerHTML = '<p>Nessun frammento trovato.</p>';
                return;
            }
            
            // Sort fragments by ID (newest first)
            const fragments = data.fragments.sort((a, b) => b.id - a.id);
            
            fragments.forEach(async fragment => {
                const card = document.createElement('div');
                card.className = 'fragment-card';
                card.dataset.type = fragment.file_type;
                card.dataset.patterns = fragment.patterns || '';
                
                const content = await fetch(fragment.archived_path).then(r => r.text());
                
                card.innerHTML = `
                    <div class="fragment-header">
                        <h3 class="fragment-title">${fragment.title}</h3>
                        <div class="fragment-meta">
                            Frammento #${String(fragment.id).padStart(4, '0')} • ${new Date(fragment.timestamp).toLocaleDateString('it-IT')}
                        </div>
                    </div>
                    <pre class="fragment-content"><code class="language-${fragment.file_type}">${content}</code></pre>
                    <div class="fragment-tags">
                        ${(fragment.patterns || '').split(',').map(p => `<span class="tag">${p}</span>`).join('')}
                    </div>
                `;
                
                fragmentsContainer.appendChild(card);
                Prism.highlightElement(card.querySelector('code'));
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
