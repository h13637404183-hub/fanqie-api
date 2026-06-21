<?php
/**
 * 番茄小说 API 核心客户端 (PHP 7.4/8.0 兼容)
 */

namespace FanQie;

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/FontDecryptor.php';

class FanQieAPI
{
    private $baseUrl;
    private $cookie;
    private $headers;
    private $htmlHeaders;

    public function __construct()
    {
        $this->baseUrl = Config::$baseUrl;
        $this->cookie = Config::$cookie;
        $this->headers = Config::getHeaders();
        $this->htmlHeaders = Config::getHtmlHeaders();
    }

    private function fetchJson(string $url, array $extraHeaders = []): array
    {
        $ch = curl_init($url);
        $headers = array_merge($this->headers, $extraHeaders);
        
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_SSL_VERIFYHOST => 0,
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            return ['error' => 'cURL error', 'message' => $error];
        }
        
        if ($httpCode !== 200) {
            return ['error' => "HTTP {$httpCode}", 'message' => 'Request failed'];
        }
        
        $data = json_decode($response, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            return ['error' => 'JSON parse error', 'message' => json_last_error_msg()];
        }
        
        return $data;
    }

    private function fetchHtml(string $url, array $extraHeaders = []): ?string
    {
        $ch = curl_init($url);
        $headers = array_merge($this->htmlHeaders, $extraHeaders);
        
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_FOLLOWLOCATION => true,
            CURLOPT_TIMEOUT => 15,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_SSL_VERIFYPEER => false,
            CURLOPT_SSL_VERIFYHOST => 0,
        ]);
        
        $response = curl_exec($ch);
        $error = curl_error($ch);
        curl_close($ch);
        
        if ($error) {
            return null;
        }
        
        return $response;
    }

    public function getTopBooks(int $limit = 20, int $offset = 0): array
    {
        $url = "{$this->baseUrl}/api/author/misc/top_book_list/v1/?limit={$limit}&offset={$offset}";
        return $this->fetchJson($url);
    }

    public function getRecommendList(int $typeId = 2, int $limit = 10, int $offset = 0): array
    {
        $url = "{$this->baseUrl}/api/rank/recommend/list?type={$typeId}&limit={$limit}&offset={$offset}";
        return $this->fetchJson($url);
    }

    public function getRankCategory(
        int $categoryId = 1,
        int $gender = 1,
        int $rankMold = 2,
        int $rankListType = 3,
        int $limit = 20,
        int $offset = 0
    ): array {
        $url = "{$this->baseUrl}/api/rank/category/list?"
            . "app_id=2503&rank_list_type={$rankListType}&offset={$offset}&limit={$limit}"
            . "&category_id={$categoryId}&rank_version=&gender={$gender}&rankMold={$rankMold}";
        return $this->fetchJson($url);
    }

    public function getBannerList(int $location = 1): array
    {
        $url = "{$this->baseUrl}/api/banner/list?location={$location}";
        return $this->fetchJson($url);
    }

    public function getRecentUpdates(int $limit = 20, int $offset = 0): array
    {
        $url = "{$this->baseUrl}/api/rank/recent/update/list?limit={$limit}&offset={$offset}";
        return $this->fetchJson($url);
    }

    public function getTopAuthors(int $limit = 20, int $offset = 0): array
    {
        $url = "{$this->baseUrl}/api/author/misc/top_author_list/v1/?limit={$limit}&offset={$offset}";
        return $this->fetchJson($url);
    }

    public function getBookDetail(string $bookId): array
    {
        $url = "{$this->baseUrl}/page/{$bookId}";
        $html = $this->fetchHtml($url);
        
        if (!$html) {
            return ['error' => 'Failed to fetch book page'];
        }
        
        $result = [
            'book_id' => $bookId,
            'title' => '',
            'author' => '',
            'cover' => '',
            'category' => '',
            'status' => '',
            'abstract' => '',
            'word_count' => '',
            'chapters' => [],
        ];
        
        if (preg_match('/<script type="application\/ld\+json">(.*?)<\/script>/s', $html, $ldMatch)) {
            $ldData = json_decode($ldMatch[1], true);
            if ($ldData) {
                $result['title'] = $ldData['name'] ?? '';
                if (isset($ldData['author'][0]['name'])) {
                    $result['author'] = $ldData['author'][0]['name'];
                }
                if (isset($ldData['image'])) {
                    $result['cover'] = is_array($ldData['image']) ? ($ldData['image'][0] ?? '') : $ldData['image'];
                }
                $result['abstract'] = $ldData['description'] ?? '';
            }
        }
        
        if (empty($result['title']) && preg_match('/<title>(.*?)<\/title>/', $html, $titleMatch)) {
            $titleText = $titleMatch[1];
            $parts = explode('_', $titleText);
            if (count($parts) >= 2) {
                $result['title'] = trim($parts[0]);
            } else {
                $result['title'] = str_replace('_番茄小说官网', '', $titleText);
            }
        }
        
        if (preg_match('/<span[^>]*class="[^"]*info-label[^"]*"[^>]*>(.*?)<\/span>/', $html, $statusMatch)) {
            $result['status'] = trim(strip_tags($statusMatch[1]));
        }
        
        if (preg_match('/(\d+\.?\d*)\s*万字/', $html, $wordMatch)) {
            $result['word_count'] = $wordMatch[1] . '万字';
        }
        
        if (preg_match_all('/<a[^>]*href="\/reader\/(\d+)"[^>]*>(.*?)<\/a>/s', $html, $chapterMatches, PREG_SET_ORDER)) {
            $seen = [];
            foreach ($chapterMatches as $match) {
                $chapterId = $match[1];
                $title = trim(strip_tags($match[2]));
                if ($title && !in_array($chapterId, $seen, true)) {
                    $seen[] = $chapterId;
                    $result['chapters'][] = [
                        'chapter_id' => $chapterId,
                        'title' => $title,
                    ];
                }
            }
        }
        
        return $result;
    }

    public function getChapterContent(string $chapterId): array
    {
        $result = [
            'chapter_id' => $chapterId,
            'title' => '',
            'content' => '',
            'word_count' => 0,
            'encrypted' => false,
        ];
        
        $url = "{$this->baseUrl}/api/reader/full?itemId={$chapterId}";
        $data = $this->fetchJson($url, ["Cookie: {$this->cookie}"]);
        
        if (isset($data['data']['chapterData'])) {
            $chapterData = $data['data']['chapterData'];
            $result['title'] = $chapterData['chapterTitle'] ?? '';
            $rawContent = $chapterData['content'] ?? '';
            
            if ($rawContent && FontDecryptor::isEncrypted($rawContent)) {
                $result['content'] = FontDecryptor::decryptFast($rawContent);
                $result['encrypted'] = true;
            } else {
                $result['content'] = $rawContent;
            }
            
            $result['word_count'] = $chapterData['wordCount'] ?? 0;
            return $result;
        }
        
        $url = "{$this->baseUrl}/reader/{$chapterId}";
        $html = $this->fetchHtml($url, ["Cookie: {$this->cookie}"]);
        
        if ($html) {
            if (preg_match('/<h1[^>]*class="[^"]*muye-reader-title[^"]*"[^>]*>(.*?)<\/h1>/s', $html, $titleMatch)) {
                $result['title'] = trim(strip_tags($titleMatch[1]));
            }
            
            $rawContent = '';
            if (preg_match('/<div[^>]*class="[^"]*muye-reader-content[^"]*"[^>]*>(.*?)<\/div>/s', $html, $contentMatch)) {
                $contentHtml = $contentMatch[1];
                if (preg_match_all('/<p[^>]*>(.*?)<\/p>/s', $contentHtml, $pMatches)) {
                    $paragraphs = [];
                    foreach ($pMatches[1] as $p) {
                        $text = trim(strip_tags($p));
                        if ($text !== '') {
                            $paragraphs[] = $text;
                        }
                    }
                    $rawContent = implode("\n", $paragraphs);
                }
            }
            
            if ($rawContent && FontDecryptor::isEncrypted($rawContent)) {
                $result['content'] = FontDecryptor::decryptFast($rawContent);
                $result['encrypted'] = true;
            } else {
                $result['content'] = $rawContent;
            }
            
            $result['word_count'] = mb_strlen($result['content'], 'UTF-8');
        }
        
        return $result;
    }

    public function search(string $keyword, int $page = 1): array
    {
        return [
            'keyword' => $keyword,
            'page' => $page,
            'note' => 'Search requires mobile API signature. Consider using known book IDs.',
            'results' => [],
        ];
    }
}
