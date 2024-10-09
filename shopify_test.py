from curl_cffi import requests as cffi_requests


cookies = {
    'master_device_id': '75d7e4d3-0a29-4f45-89c2-6ce13cf412eb',
    '_shopify_s': 'ea03bdf5-E0F3-4E13-6AE5-FFBB6141D7DB',
    '_shopify_y': 'ea03bdf5-0C1A-4074-EF32-53AC0311E542',
    'logged_in': 'true',
    'koa.sid': 'WyMUnunlt0wT1lXDWhI2DYXh57oGiGGE',
    'koa.sid.sig': 'nfWz8XsVU6tidKSBXEZtEAJ0TA8',
}


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cookie': 'master_device_id=75d7e4d3-0a29-4f45-89c2-6ce13cf412eb; _shopify_s=ea03bdf5-E0F3-4E13-6AE5-FFBB6141D7DB; _shopify_y=ea03bdf5-0C1A-4074-EF32-53AC0311E542; logged_in=true; koa.sid=WyMUnunlt0wT1lXDWhI2DYXh57oGiGGE; koa.sid.sig=nfWz8XsVU6tidKSBXEZtEAJ0TA8',
    'priority': 'u=0, i',
    'referer': 'https://admin.shopify.com/auth/callback?code=dFZEbXNKUHFudFl5VGxCSzdaaytMZTlGRDFweHAwQjlVemhWeG9PUnk3dDBPSmx3WTNrdzZISnRaSFBWeThLNWM5cktkbERUTEEvN3UrUGxVNDlRYldCUXV6czNIYmRSTkpyZXM2Z28yYWp1SnpUTjNDdGIwb2VtNFcxbWJWRnVmenlYMVo1NFJqajlWY0Z5RzhCem40VUtNSlRCMWdIZnNVWTdXdVpSaUxzL1ZlczBwT2xqSzR2dTBjZzg5QVFscVZJd05yWndSTmR3QjdXaEI3NDhsTGUrbXRTSzRMN3RyV1FtbmMwVnQxVWhsdkdsNUY4Ty93TXFWRGFGbHpqY0ZiTVJiMGY2amQ3a1VQT0RINHI5MUNHOTlaRjJ0amdLMjFtV01zakdKa2E5QmRlZHVreXNaRkFITDVjPS0tNWJXMnhkYlhXL0ZEU1NiNC0tM3pRWXVtdmVjRGEvRkhMNjZJVmNqZz09&state=8c27eecaf4ca5e7f28b2ec1672edec15&fwd=country%3DJP',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
}

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

response = cffi_requests.get('https://admin.shopify.com/store/alanna-mx/orders.json?country=JP', cookies=cookies, headers=headers, proxies=proxies)
print(response.json())