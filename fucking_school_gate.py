from mitmproxy import http
from bs4 import BeautifulSoup as bs


def response(flow: http.HTTPFlow):
    if "http://serv.tju.edu.cn/verifyqr/access" in flow.request.url:
        text = flow.response.get_text()
        soup = bs(text, 'lxml')
        verify_page = soup.select_one(
            "body > div.page-wrapper > div.page-container > div.page-content-wrapper > div > div.qr-content.row > div > div > div > div > div > div.r")
        # 验证结果里的图片
        verify_result = verify_page.select_one("div:nth-child(1) > span.c")
        print(verify_page.select_one("div:nth-child(6)").text)
        if "出校" in verify_page.select_one("div:nth-child(6)").text:
            new_verify_result = bs("""
                <span class="c"><img src="http://serv.tju.edu.cn/upload/1.png" class="qr-status-slim">您已离开北洋园校区北门，再见！</span>
            """, 'lxml')
        else:
            new_verify_result = bs("""
                <span class="c"><img src="http://serv.tju.edu.cn/upload/1.png" class="qr-status-slim">欢迎进入北洋园</span>
            """, 'lxml')

        verify_result.decompose()
        verify_page.select_one(
            "div:nth-child(1)").append(new_verify_result.span)

        limit_num = bs("""<div class="b">
                                <span class="a">限定人数规模</span>
                                <span class="c">无限制</span>
                            </div>""", 'lxml')
        cur_num = bs("""<div class="b">
                                <span class="a">当前人数规模</span>
                                <span class="c">3342</span>
                            </div>""", 'lxml')
        verify_page.insert(2, limit_num.div)
        verify_page.insert(3, cur_num.div)

        verify_page.select_one("div:nth-child(8)").decompose()
        verify_page.select_one(
            "div.text-center.r2 > img")['src'] = "http://serv.tju.edu.cn/upload/1.png"
        flow.response.set_text(soup.prettify())
