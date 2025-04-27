import re
from bs4 import BeautifulSoup
from autoparse.tools.fetchers.static_fetcher import fetch_static_html


def is_dynamic_site(url: str, timeout: int = 10) -> bool:
    """
    Эвристика: если «сырый» HTML слишком пустой или там много признаков SPA/гидрации —
    считаем, что нужен JS-рендеринг.
    """
    try:
        html = fetch_static_html(url, timeout=timeout)
    except Exception:
        # не смогли сходить — пусть попробует рендерить через JS
        return True

    soup = BeautifulSoup(html, "html.parser")

    # 1) слишком мало текста в body?
    body = soup.body.get_text(" ", strip=True) if soup.body else ""
    if len(body) < 300:
        return True

    # 2) слишком много скриптов подряд — часто SPA
    scripts = soup.find_all("script")
    if len(scripts) > 10:
        return True

    # 3) script type=module или application/json (часто подгружают bundle или initial data)
    for tag in scripts:
        typ = tag.get("type", "").lower()
        if typ in ("module", "application/json"):
            return True

    # 4) внешние SPA-bundles по src
    spa_libs = ("react", "angular", "vue", "ember", "svelte", "next", "nuxt")
    for tag in scripts:
        src = tag.get("src", "")
        if any(lib in src.lower() for lib in spa_libs):
            return True

    # 5) inline-скрипты с признаками гидрации или initial state
    for tag in scripts:
        content = tag.string or ""
        if "window.__" in content or "hydrate(" in content:
            return True

    # 6) наличие атрибутов гидрации на корневом элементе
    hydration_attrs = {"data-reactroot", "data-reactid", "data-vue", "data-server-rendered"}
    for attr in hydration_attrs:
        if soup.find(attrs={attr: True}):
            return True

    # 7) корневые контейнеры SPA
    if soup.find(id=re.compile(r"^(app|root|main|container|__next|__nuxt)$")):
        return True

    return False
