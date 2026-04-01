/**
 * Main application module
 */

const App = {
    articles: [],
    fuse: null,
    currentFilter: 'all',

    /**
     * Initialize the application
     */
    async init() {
        console.log('Initializing Education Policy Aggregator...');

        // Load data
        const data = await DataLoader.loadArticles('data/articles.json');
        this.articles = data.articles;

        // Initialize search
        this.initSearch();

        // Render initial state
        Renderer.renderHeader(data.metadata);
        Renderer.renderArticles(this.articles, this.currentFilter);

        // Bind events
        this.bindFilters();
        this.bindSearch();

        console.log(`Loaded ${this.articles.length} articles`);
    },

    /**
     * Initialize Fuse.js search
     */
    initSearch() {
        const options = {
            keys: [
                { name: 'title', weight: 0.7 },
                { name: 'summary', weight: 0.3 }
            ],
            threshold: 0.3,
            ignoreLocation: true,
            includeScore: true
        };

        this.fuse = new Fuse(this.articles, options);
    },

    /**
     * Bind filter tab click events
     */
    bindFilters() {
        const tabs = document.querySelectorAll('.filter-tab');

        tabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                // Update active tab
                tabs.forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');

                // Update filter and re-render
                this.currentFilter = e.target.dataset.filter;
                Renderer.renderArticles(this.articles, this.currentFilter);
            });
        });
    },

    /**
     * Bind search input events
     */
    bindSearch() {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;

        let debounceTimer;

        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.trim();

            // Clear previous timer
            clearTimeout(debounceTimer);

            // Debounce search
            debounceTimer = setTimeout(() => {
                this.performSearch(query);
            }, 200);
        });
    },

    /**
     * Perform search and render results
     * @param {string} query - Search query
     */
    performSearch(query) {
        let results;

        if (!query) {
            // No query - show filtered articles
            Renderer.renderArticles(this.articles, this.currentFilter);
            return;
        }

        // Search with Fuse.js
        results = this.fuse.search(query);

        // Get article objects from results
        const articles = results.map(r => r.item);

        // Apply category filter if active
        let filteredArticles = articles;
        if (this.currentFilter !== 'all') {
            filteredArticles = articles.filter(article => {
                const category = article.primary_category || '';
                return category === this.currentFilter;
            });
        }

        // Render results
        Renderer.renderArticles(filteredArticles, this.currentFilter);
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
