<?php
/**
 * 番茄小说 API 入口 (PHP 7.4/8.0 兼容)
 */

namespace FanQie;

require_once __DIR__ . '/FanQieAPI.php';

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

$api = new FanQieAPI();
$path = $_SERVER['REQUEST_URI'] ?? '/';
$path = parse_url($path, PHP_URL_PATH);
$path = rtrim($path, '/');

function getParam(string $key, $default = null)
{
    return isset($_GET[$key]) ? $_GET[$key] : $default;
}

function jsonResponse(array $data, int $code = 200)
{
    http_response_code($code);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

$bookId = null;
$chapterId = null;

if (preg_match('/^\/api\/book\/(.+)$/', $path, $m)) {
    $bookId = $m[1];
} elseif (preg_match('/^\/api\/chapter\/(.+)$/', $path, $m)) {
    $chapterId = $m[1];
}

switch (true) {
    case $path === '' || $path === '/':
        jsonResponse([
            'name' => '番茄小说 API (FanQie Novel API)',
            'version' => '1.0.0',
            'description' => 'Unofficial API wrapper for FanQie Novel (PHP 7.4/8.0)',
            'endpoints' => [
                'GET /api/books/top' => 'Get top/popular books',
                'GET /api/books/recommend' => 'Get recommended books',
                'GET /api/books/rank' => 'Get category ranking list',
                'GET /api/books/recent' => 'Get recently updated books',
                'GET /api/books/banner' => 'Get banner list',
                'GET /api/authors/top' => 'Get top authors',
                'GET /api/book/{book_id}' => 'Get book detail and chapter list',
                'GET /api/chapter/{chapter_id}' => 'Get chapter content',
                'GET /api/search' => 'Search books (keyword query)',
            ],
            'source' => 'https://fanqienovel.com',
            'disclaimer' => 'Unofficial API for educational purposes. Please respect copyright.',
        ]);

    case $path === '/api/books/top':
        jsonResponse($api->getTopBooks(
            (int) getParam('limit', 20),
            (int) getParam('offset', 0)
        ));

    case $path === '/api/books/recommend':
        jsonResponse($api->getRecommendList(
            (int) getParam('type', 2),
            (int) getParam('limit', 10),
            (int) getParam('offset', 0)
        ));

    case $path === '/api/books/rank':
        jsonResponse($api->getRankCategory(
            (int) getParam('category_id', 1),
            (int) getParam('gender', 1),
            (int) getParam('rank_mold', 2),
            3,
            (int) getParam('limit', 20),
            (int) getParam('offset', 0)
        ));

    case $path === '/api/books/recent':
        jsonResponse($api->getRecentUpdates(
            (int) getParam('limit', 20),
            (int) getParam('offset', 0)
        ));

    case $path === '/api/books/banner':
        jsonResponse($api->getBannerList(
            (int) getParam('location', 1)
        ));

    case $path === '/api/authors/top':
        jsonResponse($api->getTopAuthors(
            (int) getParam('limit', 20),
            (int) getParam('offset', 0)
        ));

    case $bookId !== null:
        jsonResponse($api->getBookDetail($bookId));

    case $chapterId !== null:
        jsonResponse($api->getChapterContent($chapterId));

    case $path === '/api/search':
        $q = getParam('q', '');
        if (empty($q)) {
            jsonResponse(['error' => 'Missing search keyword. Use ?q=keyword'], 400);
        }
        jsonResponse($api->search($q, (int) getParam('page', 1)));

    default:
        jsonResponse([
            'error' => 'Not found',
            'message' => 'The requested resource was not found',
        ], 404);
}
