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
        const navItems = document.querySelectorAll('.nav-item[data-filter]');

        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                // Skip sub-items that are handled separately
                if (e.target.classList.contains('sub-item')) {
                    return;
                }

                // Update active state
                document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
                e.target.classList.add('active');

                // If clicking on a parent with children, don't close the menu
                const filter = e.target.dataset.filter;
                this.currentFilter = filter;

                // Update filter display
                const filterDisplay = document.getElementById('current-filter');
                if (filterDisplay) {
                    filterDisplay.textContent = this.getFilterDisplayName(filter);
                }

                // Re-render articles
                Renderer.renderArticles(this.articles, this.currentFilter);
            });
        });
    },

    /**
     * Get display name for filter
     */
    getFilterDisplayName(filter) {
        const names = {
            'all': '全部',
            '本科教育': '本科教育',
            '职业教育': '职业教育',
            '本科教育-国家': '本科教育 - 国家政策',
            '本科教育-省级': '本科教育 - 省级政策',
            '职业教育-国家': '职业教育 - 国家政策',
            '职业教育-省级': '职业教育 - 省级政策',
            '友商': '友商资讯',
            '行业': '行业动态'
        };
        return names[filter] || filter;
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
            filteredArticles = this.applyFilter(articles, this.currentFilter);
        }

        // Render results
        Renderer.renderArticles(filteredArticles, this.currentFilter);
    },

    /**
     * Apply filter to articles
     */
    applyFilter(articles, filter) {
        return articles.filter(article => {
            const sourceType = article.source_type || '';
            const educationLevel = article.education_level || '';
            const policyLevel = article.policy_level || '';

            switch (filter) {
                case 'all':
                    return true;
                case '本科教育':
                    return educationLevel === '本科教育';
                case '职业教育':
                    return educationLevel === '职业教育';
                case '本科教育-国家':
                    return educationLevel === '本科教育' && policyLevel === '国家';
                case '本科教育-省级':
                    return educationLevel === '本科教育' && policyLevel === '省级';
                case '职业教育-国家':
                    return educationLevel === '职业教育' && policyLevel === '国家';
                case '职业教育-省级':
                    return educationLevel === '职业教育' && policyLevel === '省级';
                case '友商':
                    return sourceType === 'vendor';
                case '行业':
                    return sourceType === 'industry' || (sourceType === 'news' && !article.is_policy);
                default:
                    return true;
            }
        });
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
