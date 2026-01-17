// stats.js - 统计功能统一管理
class ComicStats {
    constructor() {
        this.workerUrl = 'https://comic-hot-counter.zhouguangzheng.workers.dev';
    }
    
    // 获取全站统计
    async getSiteStats() {
        try {
            const response = await fetch(`${this.workerUrl}/stat`);
            const data = await response.json();
            return data.success ? data.data : null;
        } catch (error) {
            console.error('获取全站统计失败:', error);
            return null;
        }
    }
    
    // 获取漫画阅读量
    async getComicViews(comicId) {
        try {
            const response = await fetch(`${this.workerUrl}/hit?id=${comicId}`);
            const data = await response.json();
            return data.success ? data.data.views : 0;
        } catch (error) {
            console.error('获取漫画阅读量失败:', error);
            return 0;
        }
    }
    
    // 获取热门排行榜
    async getHotComics(limit = 10) {
        try {
            const response = await fetch(`${this.workerUrl}/top`);
            const data = await response.json();
            if (data.success) {
                return data.data.slice(0, limit);
            }
            return [];
        } catch (error) {
            console.error('获取热门排行失败:', error);
            return [];
        }
    }
    
    // 记录漫画阅读（使用图片方式，避免被拦截）
    recordComicView(comicId) {
        // 使用 Image 对象，不会被广告拦截器拦截
        const img = new Image();
        img.src = `${this.workerUrl}/hit?id=${comicId}`;
        return img;
    }
}

// 全局统计实例
window.ComicStats = new ComicStats();