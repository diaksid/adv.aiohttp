import re

from ..config import debug, minify as config


async def minify_middleware(app, handler):
    async def middleware(request):
        def re_code(m):
            s = m.group(1) \
                .lstrip(u'\n\r') \
                .rstrip()
            if len(s):
                s = s \
                    .replace(u'\n\r', '<br>') \
                    .replace(u'\n', '<br>') \
                    .replace(u'\r', '<br>')
                s = s \
                    .replace(u'\t', '&nbsp;' * 4) \
                    .replace(u' ', '&nbsp;')
            return m.group(0).replace(m.group(1), s)

        def re_style(m):
            s = m.group(1).strip()
            if len(s):
                s = re \
                    .compile(r'\s*([\{\}\*\>\+\,\;])\s*') \
                    .sub(r'\1', s)
                s = re \
                    .compile(r'([\[\:]) ') \
                    .sub(r'\1', s)
                s = s \
                    .replace(u' ]', ']') \
                    .replace(u';}', '}')
            return m.group(0).replace(m.group(1), s)

        def re_script(m):
            s = m.group(1).strip()
            if len(s):
                s = s.rstrip(u';')
                s = re \
                    .compile(
                    r'\s*([\(\)\[\]\{\}\?\|\&\/\*\-\+\:\.\,\;\>\<\=])\s*') \
                    .sub(r'\1', s)
            return m.group(0).replace(m.group(1), s)

        def re_quote(m):
            s = m.group(2) \
                .replace(u'\'', '"')
            s = re \
                .compile(r'=" ([^"]+)"') \
                .sub(r'="\1"', s)
            s = re \
                .compile(r'="([^"]+) "') \
                .sub(r'="\1"', s)
            s = re \
                .compile(r'="\s*"') \
                .sub(r'', s)
            s = re \
                .compile(r'="([^=\s]+?)"') \
                .sub(r'=\1', s)
            return m.group(0).replace(m.group(2), s)

        def minify(value, config):
            value = value.decode('utf-8')
            if config.get('code', None):
                value = re \
                    .compile(r'<pre.*?>(.+?)</pre>', re.DOTALL) \
                    .sub(re_code, value)
            value = re \
                .compile(r'\s+') \
                .sub(' ', value)
            value = re \
                .compile(r'<(\w+)(.*?) \/?>') \
                .sub(r'<\1\2>', value)
            value = re \
                .compile(r'> <([!\/]?)([\w+\[\]-])') \
                .sub(r'><\1\2', value)
            value = re \
                .compile(r'<style>(.*?)</style>') \
                .sub(re_style, value)
            value = re \
                .compile(r'<script.*?>(.*?)</script>') \
                .sub(re_script, value)
            if config.get('strict', None):
                value = re \
                    .compile(r'<([^\/\s]+)(.+?)>') \
                    .sub(re_quote, value)
                value = re \
                    .compile(r'</(html|body|p|li)>') \
                    .sub('', value)
            return value.encode('utf-8')

        try:
            response = await handler(request)
        except Exception as e:
            raise e
        else:
            if response.content_type == 'text/html' and not debug:
                if config and config.get('plain', None):
                    response.body = minify(response.body, config)
            return response

    return middleware
