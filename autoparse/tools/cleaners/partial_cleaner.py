from bs4 import BeautifulSoup, Comment
from bs4.element import Tag


def extract_partial_clean_html(html: str) -> str:
    """
    Лёгкая, но надёжная очистка HTML:
      - Убирает абсолютно всё «служебное» (script, style, head и т.д.).
      - Убирает комментарии.
      - Оставляет все семантические контейнеры (section, article и т.п.) и их class/id.
      - Удаляет только полностью пустые теги без текста и без вложенных информативных тегов.
      - Стирает все атрибуты, кроме href/src/alt/title/class/id.
      - Возвращает содержимое <body> (или весь документ, если <body> нет).
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 1) Удаляем абсолютно всё служебное
    for tag in soup.find_all(['script', 'style', 'noscript', 'iframe',
                              'embed', 'object', 'head', 'meta', 'link', 'svg']):
        tag.decompose()

    # 2) Удаляем комментарии
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        comment.extract()

    # 3) Удаляем пустые теги, но только если у них нет текста и нет вложенных тегов
    def remove_empty(tag: Tag):
        for child in list(tag.contents):
            if isinstance(child, Tag):
                remove_empty(child)
        # если нет текста и нет тегов внутри — удаляем,
        # но не трогаем семантические контейнеры и теги с class/id
        if (not tag.get_text(strip=True)
            and not tag.find()
            and not (tag.has_attr('class') or tag.has_attr('id'))
            and tag.name not in ('section','article','nav','header','footer','aside')):
            tag.decompose()

    root = soup.body or soup
    remove_empty(root)

    # 4) Оставляем у всех тегов только безопасные атрибуты
    allowed_attrs = {'href', 'src', 'alt', 'title', 'class', 'id'}
    for tag in root.find_all():
        if not isinstance(tag, Tag):
            continue
        new_attrs = {
            k: v for k, v in tag.attrs.items()
            if k in allowed_attrs
        }
        tag.attrs = new_attrs

    # 5) Собираем финальный HTML из тела
    parts = []
    for child in root.children:
        # сохраняем и теги, и чистый текст
        if isinstance(child, Tag):
            parts.append(str(child))
        else:
            txt = child.strip()
            if txt:
                parts.append(txt)

    return ''.join(parts)
