<?php
/**
 * 番茄小说 API 配置
 */

namespace FanQie;

class Config
{
    public static $cookie = 'Hm_lvt_2667d29c8e792e6fa9182c20a3013175=1716438629; '
        . 'csrf_session_id=cb69e6cf3b1af43a88a56157e7795f2e; '
        . 'novel_web_id=7372047678422058532; '
        . 's_v_web_id=verify_lwir8sbl_HcMwpu3M_DoJp_4RKG_BcMo_izZ4lEmNBlEQ; '
        . 'Hm_lpvt_2667d29c8e792e6fa9182c20a3013175=1716454389; '
        . 'ttwid=1%7CRpx4a-wFaDG9-ogRfl7wXC7k61DQkWYwkb_Q2THEqb4%7C1716454388%7Cb80bb1f8f2ccd546e6a1ccd1b1abb9151e31bbf5d48e3224451a90b7ca5d534c; '
        . 'msToken=-9U5-TOe5X2axgeeY4G28F-tp-R7o8gDaOF5p2fPPvcNdZYLXWU9JiPv_tOU81HeXCDT52o4UtGOLCZmuDMN2I8yulNK-8hIUpNSHiEVK3ke5aEeGJ4wDhk_cQgJ3g==';

    public static $baseUrl = 'https://fanqienovel.com';

    public static function getHeaders()
    {
        return [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept: application/json, text/plain, */*',
            'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding: identity',
            'Referer: https://fanqienovel.com/',
            'Connection: keep-alive',
        ];
    }

    public static function getHtmlHeaders()
    {
        return [
            'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding: identity',
            'Referer: https://fanqienovel.com/',
        ];
    }
}
