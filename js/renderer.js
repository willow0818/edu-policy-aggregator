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

        // Apply filter
        let filteredArticles = articles;
        if (filter !== 'all') {
            filteredArticles = this.applyFilter(articles, filter);
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
                    return sourceType === 'industry' || sourceType === 'news';
                default:
                    return true;
            }
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

        // Determine card class based on content type
        const cardClass = this.getCardClass(article);
        card.classList.add(cardClass);

        // Format date
        const date = article.published_date ? this.formatDate(article.published_date) : '未知日期';

        // Get tags
        const tags = this.getArticleTags(article);

        card.innerHTML = `
            <div class="article-header">
                <h3 class="article-title">
                    <a href="${this.escapeHtml(article.url)}" target="_blank" rel="noopener">
                        ${this.escapeHtml(article.title)}
                    </a>
                </h3>
            </div>
            <div class="article-meta">
                ${tags}
                <span class="source">${this.escapeHtml(article.source)}</span>
                <span class="date">${date}</span>
            </div>
            <p class="article-summary">${this.escapeHtml(article.summary || '')}</p>
        `;

        return card;
    },

    /**
     * Get CSS class for card based on article content
     */
    getCardClass(article) {
        const educationLevel = article.education_level || '';
        const policyLevel = article.policy_level || '';
        const sourceType = article.source_type || '';

        if (sourceType === 'vendor') return 'vendor';
        if (sourceType === 'industry') return 'industry';
        if (policyLevel === '国家') return 'national';
        if (policyLevel === '省级') return 'provincial';
        if (educationLevel === '本科教育') return 'undergraduate';
        if (educationLevel === '职业教育') return 'vocational';

        return 'national';
    },

    /**
     * Get article tags HTML
     */
    getArticleTags(article) {
        const tags = [];
        const educationLevel = article.education_level || '';
        const policyLevel = article.policy_level || '';
        const sourceType = article.source_type || '';

        if (educationLevel) {
            tags.push(`<span class="category-tag ${this.getEducationClass(educationLevel)}">${educationLevel}</span>`);
        }

        if (policyLevel) {
            tags.push(`<span class="category-tag ${this.getPolicyClass(policyLevel)}">${policyLevel}</span>`);
        }

        if (sourceType === 'vendor') {
            tags.push(`<span class="category-tag vendor">友商</span>`);
        }

        return tags.join('');
    },

    /**
     * Get CSS class for education level
     */
    getEducationClass(level) {
        const mapping = {
            '职业教育': 'vocational',
            '本科教育': 'undergraduate'
        };
        return mapping[level] || '';
    },

    /**
     * Get CSS class for policy level
     */
    getPolicyClass(level) {
        const mapping = {
            '国家': 'national',
            '省级': 'provincial'
        };
        return mapping[level] || '';
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
