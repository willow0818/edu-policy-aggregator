/**
 * Data loader module - fetches articles JSON
 */

const DataLoader = {
    /**
     * Load articles from JSON file
     * @param {string} filepath - Path to articles.json
     * @returns {Promise<Object>} - Article data and metadata
     */
    async loadArticles(filepath = 'data/articles.json') {
        try {
            const response = await fetch(filepath);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return {
                articles: data.articles || [],
                metadata: data.metadata || {}
            };
        } catch (error) {
            console.error('Error loading articles:', error);
            return { articles: [], metadata: {} };
        }
    },

    /**
     * Get the last updated timestamp
     * @param {Object} metadata - Metadata object
     * @returns {string} - Formatted date string
     */
    formatLastUpdated(metadata) {
        if (!metadata.last_updated) {
            return '更新时间未知';
        }

        dayjs.locale('zh-cn');
        const date = dayjs(metadata.last_updated);
        return `最后更新 ${date.format('YYYY.MM.DD HH:mm')}`;
    }
};
