import json
import urllib.request
import urllib.parse
import urllib.error
import random
import re
from html import unescape

# Try to use lxml for HTML parsing, fallback to regex
try:
    from lxml import etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False

class FanQieAPI:
    """番茄小说 API 客户端"""
    
    BASE_URL = "https://fanqienovel.com"
    
    # Common headers mimicking browser
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity',
        'Referer': 'https://fanqienovel.com/',
        'Connection': 'keep-alive',
    }
    
    HTML_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'identity',
        'Referer': 'https://fanqienovel.com/',
    }
    
    def __init__(self):
        self._cookie = None
    
    def _fetch_json(self, url, headers=None, cookie=None):
        """Fetch JSON from URL"""
        h = (headers or self.HEADERS).copy()
        if cookie:
            h['Cookie'] = cookie
        req = urllib.request.Request(url, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read().decode('utf-8')
                return json.loads(data)
        except urllib.error.HTTPError as e:
            return {'error': f'HTTP {e.code}', 'message': str(e.reason)}
        except Exception as e:
            return {'error': 'Request failed', 'message': str(e)}
    
    def _fetch_html(self, url, cookie=None):
        """Fetch HTML page"""
        h = self.HTML_HEADERS.copy()
        if cookie:
            h['Cookie'] = cookie
        req = urllib.request.Request(url, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode('utf-8')
        except Exception as e:
            return None
    
    # ==================== PC端公开 API ====================
    
    def get_top_books(self, limit=20, offset=0):
        """获取热门书籍列表"""
        url = f"{self.BASE_URL}/api/author/misc/top_book_list/v1/?limit={limit}&offset={offset}"
        return self._fetch_json(url)
    
    def get_recommend_list(self, type_id=2, limit=10, offset=0):
        """获取推荐列表
        type_id: 2=男生推荐, 3=女生推荐
        """
        url = f"{self.BASE_URL}/api/rank/recommend/list?type={type_id}&limit={limit}&offset={offset}"
        return self._fetch_json(url)
    
    def get_rank_category(self, category_id=1, gender=1, rank_mold=2, 
                          rank_list_type=3, limit=20, offset=0):
        """获取分类榜单
        category_id: 分类ID
        gender: 1=男, 2=女
        rank_mold: 1=完结榜, 2=阅读榜, 3=新书榜
        rank_list_type: 3=分类榜
        """
        url = (f"{self.BASE_URL}/api/rank/category/list?"
               f"app_id=2503&rank_list_type={rank_list_type}&offset={offset}&limit={limit}"
               f"&category_id={category_id}&rank_version=&gender={gender}&rankMold={rank_mold}")
        return self._fetch_json(url)
    
    def get_banner_list(self, location=1):
        """获取Banner列表"""
        url = f"{self.BASE_URL}/api/banner/list?location={location}"
        return self._fetch_json(url)
    
    def get_recent_updates(self, limit=20, offset=0):
        """获取最近更新列表"""
        url = f"{self.BASE_URL}/api/rank/recent/update/list?limit={limit}&offset={offset}"
        return self._fetch_json(url)
    
    def get_top_authors(self, limit=20, offset=0):
        """获取热门作者列表"""
        url = f"{self.BASE_URL}/api/author/misc/top_author_list/v1/?limit={limit}&offset={offset}"
        return self._fetch_json(url)
    
    # ==================== 网页解析 API ====================
    
    def get_book_detail(self, book_id):
        """获取书籍详情（通过网页解析）"""
        url = f"{self.BASE_URL}/page/{book_id}"
        html = self._fetch_html(url)
        if not html:
            return {'error': 'Failed to fetch book page'}
        
        result = {
            'book_id': str(book_id),
            'title': '',
            'author': '',
            'cover': '',
            'category': '',
            'status': '',
            'abstract': '',
            'word_count': '',
            'chapters': []
        }
        
        try:
            # Try to extract from JSON-LD
            ld_match = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
            if ld_match:
                try:
                    ld_data = json.loads(ld_match.group(1))
                    result['title'] = ld_data.get('name', '')
                    result['author'] = ld_data.get('author', [{}])[0].get('name', '')
                    result['cover'] = ld_data.get('image', [''])[0] if isinstance(ld_data.get('image'), list) else ld_data.get('image', '')
                    result['abstract'] = ld_data.get('description', '')
                except:
                    pass
            
            # Extract from meta tags and HTML
            if not result['title']:
                title_match = re.search(r'<title>(.*?)</title>', html)
                if title_match:
                    title_text = title_match.group(1)
                    # Format: 书名_作者小说_番茄小说官网
                    parts = title_text.split('_')
                    if len(parts) >= 2:
                        result['title'] = parts[0].strip()
                    else:
                        result['title'] = title_text.replace('_番茄小说官网', '').strip()
            
            # Extract status
            status_match = re.search(r'<span[^>]*class="[^"]*info-label[^"]*"[^>]*>(.*?)</span>', html)
            if status_match:
                result['status'] = status_match.group(1).strip()
            
            # Extract category
            cat_match = re.search(r'<a[^>]*href="[^"]*category[^"]*"[^>]*>(.*?)</a>', html)
            if cat_match:
                result['category'] = cat_match.group(1).strip()
            
            # Extract word count
            word_match = re.search(r'(\d+\.?\d*)\s*万字', html)
            if word_match:
                result['word_count'] = word_match.group(1) + '万字'
            
            # Extract chapters
            if HAS_LXML:
                tree = etree.HTML(html)
                chapter_links = tree.xpath('//div[@class="chapter"]//div[@class="chapter-item"]//a')
                for link in chapter_links:
                    href = link.get('href', '')
                    title = link.text or ''
                    if href and title:
                        chapter_id = href.split('/')[-1]
                        result['chapters'].append({
                            'chapter_id': chapter_id,
                            'title': title.strip()
                        })
            else:
                # Fallback regex extraction
                chapter_pattern = re.compile(r'<a[^>]*href="/reader/(\d+)"[^>]*>(.*?)</a>', re.S)
                for match in chapter_pattern.finditer(html):
                    chapter_id = match.group(1)
                    title = re.sub(r'<[^>]+>', '', match.group(2)).strip()
                    if title:
                        result['chapters'].append({
                            'chapter_id': chapter_id,
                            'title': title
                        })
            
            # Remove duplicates while preserving order
            seen = set()
            unique_chapters = []
            for ch in result['chapters']:
                if ch['chapter_id'] not in seen:
                    seen.add(ch['chapter_id'])
                    unique_chapters.append(ch)
            result['chapters'] = unique_chapters
            
        except Exception as e:
            result['parse_error'] = str(e)
        
        return result
    
    def get_chapter_content(self, chapter_id, book_id=None):
        """获取章节内容
        1. 尝试通过API获取
        2. 尝试通过网页解析获取（需要cookie）
        """
        result = {
            'chapter_id': str(chapter_id),
            'title': '',
            'content': '',
            'word_count': 0
        }
        
        # Method 1: Try API endpoint first
        try:
            url = f"{self.BASE_URL}/api/reader/full?itemId={chapter_id}"
            cookie = self._get_cookie()
            data = self._fetch_json(url, cookie=cookie)
            if data and 'data' in data and 'chapterData' in data['data']:
                chapter_data = data['data']['chapterData']
                result['title'] = chapter_data.get('chapterTitle', '')
                result['content'] = chapter_data.get('content', '')
                result['word_count'] = chapter_data.get('wordCount', 0)
                return result
        except:
            pass
        
        # Method 2: Parse from HTML reader page
        try:
            url = f"{self.BASE_URL}/reader/{chapter_id}"
            cookie = self._get_cookie()
            html = self._fetch_html(url, cookie=cookie)
            if html:
                # Extract title
                title_match = re.search(r'<h1[^>]*class="[^"]*muye-reader-title[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
                if title_match:
                    result['title'] = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
                
                # Extract content from muye-reader-content
                if HAS_LXML:
                    tree = etree.HTML(html)
                    paragraphs = tree.xpath('//div[@class="muye-reader-content noselect"]//p/text()')
                    result['content'] = '\n'.join(p.strip() for p in paragraphs if p.strip())
                else:
                    content_match = re.search(r'<div[^>]*class="[^"]*muye-reader-content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
                    if content_match:
                        content_html = content_match.group(1)
                        # Extract text from <p> tags
                        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', content_html, re.DOTALL)
                        result['content'] = '\n'.join(re.sub(r'<[^>]+>', '', p).strip() for p in paragraphs if p.strip())
                
                result['word_count'] = len(result['content'])
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _get_cookie(self):
        """Generate or retrieve a valid cookie for content access"""
        if self._cookie:
            return self._cookie
        
        # Generate a random novel_web_id
        base = 1000000000000000000
        novel_web_id = random.randint(base * 6, base * 9)
        self._cookie = f"novel_web_id={novel_web_id}"
        return self._cookie
    
    def search(self, keyword, page=1):
        """搜索书籍
        Note: This uses the mobile API which may require additional parameters.
        For now, we return a helpful message suggesting alternative approaches.
        """
        # The mobile API requires signature parameters (msToken, a_bogus)
        # which are complex to generate. For now, return a placeholder.
        return {
            'keyword': keyword,
            'page': page,
            'note': 'Search requires mobile API signature. Consider using the web search endpoint or known book IDs.',
            'results': []
        }


# Global API instance
api = FanQieAPI()
