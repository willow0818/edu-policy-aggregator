/**
 * Renderer module - handles DOM rendering
 */

const Renderer = {
    /**
     * Render the header with last updated info
     * @param {Object} metadata - Metadata object
     */
    renderHeader(metadata) {
        const lastUpdatedEl = document.getElementById('last-updated');
        if (lastUpdatedEl) {
            lastUpdatedEl.textContent = DataLoader.formatLastUpdated(metadata);
        }
    },

    /**
     * Render article count
     * @param {number} count - Number of articles
     */
    renderArticleCount(count) {
        const countEl = document.getElementById('article-count');
        if (countEl) {
            countEl.textContent = `共 ${count} 条`;
        }
    },

    /**
     * Render articles to the article list
     * @param {Array} articles - List of articles
     * @param {string} filter - Current filter category
     */
    renderArticles(articles, filter = 'all') {
        const container = document.getElementById('article-list');
        if (!container) return;

        // Filter articles
        let filteredArticles = articles;
        if (filter !== 'all') {
            filteredArticles = articles.filter(article => {
                const category = article.primary_category || '';
                return category === filter;
            });
        }

        // Update count
        this.renderArticleCount(filteredArticles.length);

        // Clear container
        container.innerHTML = '';

        if (filteredArticles.length === 0) {
            container.innerHTML = '<div class="empty-state">暂无相关政策资讯</div>';
            return;
        }

        // Render each article
        filteredArticles.forEach(article => {
            const card = this.createArticleCard(article);
            container.appendChild(card);
        });
    },

    /**
     * Create an article card element
     * @param {Object} article - Article data
     * @returns {HTMLElement} - Article card element
     */
    createArticleCard(article) {
        const card = document.createElement('div');
        card.className = 'article-card';

        // Add category class
        const category = article.primary_category || 'policy';
        const categoryClass = this.getCategoryClass(category);
        card.classList.add(categoryClass);

        // Format date
        const date = article.published_date ? this.formatDate(article.published_date) : '未知日期';

        // Get category tag display
        const categoryTag = this.getCategoryTag(category);

        card.innerHTML = `
            <div class="article-header">
                <h3 class="article-title">
                    <a href="${this.escapeHtml(article.url)}" target="_blank" rel="noopener">
                        ${this.escapeHtml(article.title)}
                    </a>
                </h3>
            </div>
            <div class="article-meta">
                <span class="category-tag ${categoryClass}">${categoryTag}</span>
                <span class="source">${this.escapeHtml(article.source)}</span>
                <span class="date">${date}</span>
            </div>
            <p class="article-summary">${this.escapeHtml(article.summary || '')}</p>
        `;

        return card;
    },

    /**
     * Get CSS class for category
     * @param {string} category - Category name
     * @returns {string} - CSS class name
     */
    getCategoryClass(category) {
        const mapping = {
            '职业教育': 'vocational',
            '本科教育': 'undergraduate',
            '资讯': 'news',
            '政策': 'policy'
        };
        return mapping[category] || 'policy';
    },

    /**
     * Get category tag display text
     * @param {string} category - Category name
     * @returns {string} - Tag display text
     */
    getCategoryTag(category) {
        const mapping = {
            '职业教育': '职业教育',
            '本科教育': '本科教育',
            '资讯': '资讯',
            '政策': '政策'
        };
        return mapping[category] || '政策';
    },

    /**
     * Format date string
     * @param {string} dateStr - Date string
     * @returns {string} - Formatted date
     */
    formatDate(dateStr) {
        if (!dateStr) return '';

        dayjs.locale('zh-cn');
        const date = dayjs(dateStr);
        return date.format('YYYY-MM-DD');
    },

    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} - Escaped text
     */
    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};
