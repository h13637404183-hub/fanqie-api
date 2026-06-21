from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fanqie_api import api

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """API Root - List available endpoints"""
    return jsonify({
        'name': '番茄小说 API (FanQie Novel API)',
        'version': '1.0.0',
        'description': 'Unofficial API wrapper for FanQie Novel (番茄小说)',
        'endpoints': {
            'GET /api/books/top': 'Get top/popular books',
            'GET /api/books/recommend': 'Get recommended books',
            'GET /api/books/rank': 'Get category ranking list',
            'GET /api/books/recent': 'Get recently updated books',
            'GET /api/books/banner': 'Get banner list',
            'GET /api/authors/top': 'Get top authors',
            'GET /api/book/<book_id>': 'Get book detail and chapter list',
            'GET /api/chapter/<chapter_id>': 'Get chapter content',
            'GET /api/search': 'Search books (keyword query)',
        },
        'source': 'https://fanqienovel.com',
        'disclaimer': 'This is an unofficial API for educational purposes. Please respect copyright.'
    })

@app.route('/api/books/top')
def get_top_books():
    """获取热门书籍列表"""
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    data = api.get_top_books(limit=limit, offset=offset)
    return jsonify(data)

@app.route('/api/books/recommend')
def get_recommend_books():
    """获取推荐书籍列表"""
    type_id = request.args.get('type', 2, type=int)
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    data = api.get_recommend_list(type_id=type_id, limit=limit, offset=offset)
    return jsonify(data)

@app.route('/api/books/rank')
def get_rank_books():
    """获取分类榜单
    
    Query Parameters:
        category_id: Category ID (default: 1)
        gender: 1=male, 2=female (default: 1)
        rank_mold: 1=completed, 2=reading, 3=new (default: 2)
        limit: Number of results (default: 20)
        offset: Pagination offset (default: 0)
    """
    category_id = request.args.get('category_id', 1, type=int)
    gender = request.args.get('gender', 1, type=int)
    rank_mold = request.args.get('rank_mold', 2, type=int)
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    data = api.get_rank_category(
        category_id=category_id,
        gender=gender,
        rank_mold=rank_mold,
        limit=limit,
        offset=offset
    )
    return jsonify(data)

@app.route('/api/books/recent')
def get_recent_books():
    """获取最近更新书籍列表"""
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    data = api.get_recent_updates(limit=limit, offset=offset)
    return jsonify(data)

@app.route('/api/books/banner')
def get_banners():
    """获取Banner列表"""
    location = request.args.get('location', 1, type=int)
    data = api.get_banner_list(location=location)
    return jsonify(data)

@app.route('/api/authors/top')
def get_top_authors():
    """获取热门作者列表"""
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)
    data = api.get_top_authors(limit=limit, offset=offset)
    return jsonify(data)

@app.route('/api/book/<book_id>')
def get_book_detail(book_id):
    """获取书籍详情和章节列表
    
    Path Parameters:
        book_id: Book ID (numeric string)
    """
    data = api.get_book_detail(book_id)
    return jsonify(data)

@app.route('/api/chapter/<chapter_id>')
def get_chapter(chapter_id):
    """获取章节内容
    
    Path Parameters:
        chapter_id: Chapter ID (numeric string)
    """
    data = api.get_chapter_content(chapter_id)
    return jsonify(data)

@app.route('/api/search')
def search_books():
    """搜索书籍
    
    Query Parameters:
        q: Search keyword
        page: Page number (default: 1)
    """
    keyword = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    if not keyword:
        return jsonify({'error': 'Missing search keyword. Use ?q=keyword'}), 400
    data = api.search(keyword, page=page)
    return jsonify(data)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
