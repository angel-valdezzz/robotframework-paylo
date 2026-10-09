"""Verify real payloads, meaningful motion and native bilingual documentation."""

import json
from functools import partial
from hashlib import sha256
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[2]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def values(page):
    return page.locator("[data-pl-value]").all_text_contents()


def check_cache(browser, base):
    assets = (
        "assets/stylesheets/landing.css",
        "assets/stylesheets/visual.css",
        "assets/landing.js",
    )
    versions = {p: sha256((ROOT / "docs" / p).read_bytes()).hexdigest()[:16] for p in assets}
    for locale in ("", "es/"):
        page = browser.new_page()
        seen = set()

        def cached(route):
            url = urlsplit(route.request.url)
            path = next((p for p in assets if url.path.endswith("/" + p)), None)
            if path is None:
                route.continue_()
            elif parse_qs(url.query).get("content") == [versions[path]]:
                seen.add(path)
                route.continue_()
            else:
                route.fulfill(
                    content_type="text/css" if path.endswith(".css") else "text/javascript",
                    body="body{background:white}" if path.endswith(".css") else "void 0;",
                )

        page.route("**/assets/**", cached)
        page.goto(base + locale)
        expect(page.locator("#pl-pause")).to_be_visible()
        assert seen == set(assets), seen
        page.close()


def check_navigation(browser, base, output):
    page = browser.new_page(viewport={"width": 1440, "height": 1024})
    page.goto(base)
    page.locator(".pl-search-trigger").focus()
    page.keyboard.press("Enter")
    page.locator('[data-md-component="search-query"]').fill("Render JSON")
    expect(page.locator(".md-search-result__link").first).to_be_visible(timeout=30000)
    page.keyboard.press("Escape")
    page.locator(".pl-primary").click()
    page.wait_for_url("**/guide/")
    expect(page.locator("[data-pl-hero]")).to_have_count(0)
    page.locator('label[for="__palette_1"]').click()
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    page.locator(".md-select button").click()
    page.locator('[data-doc-language="es"]').click()
    page.wait_for_url("**/es/guide/")
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    assert page.evaluate("""() => {
      const h=document.querySelector('.md-header'),t=document.querySelector('.md-tabs');
      const a=getComputedStyle(h),b=getComputedStyle(t);
      return a.animationName==='pl-header-flow' && b.animationName===a.animationName &&
        a.backgroundImage===b.backgroundImage && a.backgroundPosition===b.backgroundPosition &&
        Math.abs(h.getAnimations()[0].currentTime-t.getAnimations()[0].currentTime)<1;
    }""")
    page.screenshot(path=str(output / "docs-es-header.png"))
    assert page.locator(".md-logo img").first.evaluate(
        "el=>getComputedStyle(el).filter==='brightness(0) invert(1)'"
    )
    page.locator(".md-logo").first.click()
    expect(page.locator("#pl-pause")).to_be_visible()
    assert page.locator("[data-pl-hero]").get_attribute("data-lang") == "es"
    page.locator("#pl-pause").click()
    expect(page.locator("#pl-pause")).to_have_attribute("aria-pressed", "true")
    page.locator(".pl-scroll").click()
    expect(page.locator("#overview")).to_be_focused()
    page.wait_for_timeout(900)
    page.screenshot(path=str(output / "es-explanation.png"))
    assert page.request.get(page.locator(".pl-secondary").evaluate("el=>el.href")).ok
    page.goto(base + "es/examples/")
    page.locator(".md-select button").click()
    page.locator('[data-doc-language="en"]').click()
    page.wait_for_url("**/examples/")
    assert "/es/" not in page.url
    expect(page.locator("body")).to_have_attribute("data-md-color-scheme", "slate")
    page.close()


def main():
    server_root = ROOT / "build/docs-server"
    server_root.mkdir(parents=True, exist_ok=True)
    mount = server_root / "robotframework-paylo"
    if not mount.exists():
        mount.symlink_to(ROOT / "site", target_is_directory=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(server_root))
    )
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/robotframework-paylo/"
    output = ROOT / "build/landing-checks"
    output.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=["--no-sandbox"])
            check_cache(browser, base)
            for locale in ("en", "es"):
                for width, height in (
                    (1440, 1024),
                    (1366, 625),
                    (820, 1180),
                    (390, 844),
                    (320, 900),
                ):
                    page = browser.new_page(viewport={"width": width, "height": height})
                    errors = []
                    page.on("pageerror", lambda error, found=errors: found.append(str(error)))
                    page.goto(base + ("es/" if locale == "es" else ""))
                    expect(page.locator("#pl-pause")).to_be_visible()
                    page.evaluate("document.fonts.ready")
                    assert page.locator("h1").count() == 1
                    assert page.locator("#speed,.review-controls,canvas").count() == 0
                    assert page.locator(".pl-notation").inner_text().startswith("customer.name")
                    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth")
                    assert page.locator(".md-header").evaluate(
                        "el=>getComputedStyle(el).backgroundColor==='rgba(0, 0, 0, 0)'"
                    )
                    assert page.locator(".md-logo img").first.evaluate(
                        "el=>getComputedStyle(el).backgroundColor==='rgba(0, 0, 0, 0)'"
                    )
                    assert page.locator(".md-select button").evaluate(
                        "el=>el.getBoundingClientRect().right<=document.querySelector('.pl-search-trigger').getBoundingClientRect().left"
                    )
                    page.screenshot(path=str(output / f"{locale}-{width}-{height}-initial.png"))
                    if width >= 1100:
                        assert page.locator(".pl-primary,.pl-scroll").evaluate_all(
                            "els=>els.every(el=>{const r=el.getBoundingClientRect();return r.top>=0 && r.bottom<=innerHeight;})"
                        )
                    page.wait_for_function(
                        "document.querySelector('.pl-assembly').dataset.field==='0' && Number(document.querySelector('#pl-traveler').style.opacity)>.8"
                    )
                    page.screenshot(path=str(output / f"{locale}-{width}-{height}-transfer.png"))
                    page.wait_for_function(
                        "document.querySelector('.pl-assembly').dataset.phase==='complete'"
                    )
                    assert values(page) == ['"Ana"', "3", "true"]
                    assert page.locator(".pl-type-list .pl-done").count() == 3
                    if width <= 760:
                        assert all(el.is_visible() for el in page.locator(".pl-type-mobile").all())
                    page.locator("#pl-pause").click()
                    before = values(page)
                    page.wait_for_timeout(200)
                    assert values(page) == before
                    page.locator('[data-pl-input="0"]').hover()
                    assert values(page) == before
                    for scheme in ("default", "slate"):
                        page.evaluate("s=>document.body.dataset.mdColorScheme=s", scheme)
                        assert page.locator("#pl-headline").evaluate(
                            "el=>getComputedStyle(el).color==='rgb(240, 240, 245)'"
                        )
                        assert page.locator(".pl-intro-copy p").evaluate(
                            "el=>getComputedStyle(el).color==='rgb(166, 164, 185)'"
                        )
                        page.screenshot(
                            path=str(output / f"{locale}-{width}-{height}-{scheme}.png")
                        )
                    if width == 1440:
                        page.locator("#pl-pause").click()
                        page.wait_for_function(
                            "document.querySelector('.pl-assembly').dataset.phase==='reset' && Number(document.querySelector('[data-pl-source]').style.opacity)<.7"
                        )
                        assert values(page) == ['"Ana"', "3", "true"]
                        page.wait_for_function(
                            "document.querySelector('.pl-assembly').dataset.scenario==='1' && document.querySelector('.pl-assembly').dataset.phase==='complete'"
                        )
                        assert values(page) == ['"Luis"', "12", "false"]
                    page.emulate_media(reduced_motion="reduce")
                    expect(page.locator("#pl-pause")).to_be_disabled()
                    expect(page.locator("#pl-traveler")).to_be_hidden()
                    assert values(page) == ['"Ana"', "3", "true"]
                    assert not errors, errors
                    page.close()
            check_navigation(browser, base, output)
            context = browser.new_context(java_script_enabled=False)
            page = context.new_page()
            page.goto(base)
            expect(page.locator("#pl-pause")).to_be_hidden()
            expect(page.locator("#pl-traveler")).to_be_hidden()
            expect(page.locator(".pl-primary")).to_be_visible()
            assert values(page) == ['"{{customer.name}}"', '"{{quantity}}"', '"{{active}}"']
            page.locator(".pl-scroll").click()
            assert page.url.endswith("#overview")
            browser.close()
    finally:
        server.shutdown()
    (output / "result.json").write_text(
        json.dumps({"languages": 2, "viewports": 5, "passed": True})
    )
    print("Paylo passed: real typed outputs, motion, cache, five viewports, themes and navigation.")


if __name__ == "__main__":
    main()
