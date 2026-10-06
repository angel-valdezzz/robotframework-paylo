"""Validate embedded demos and capture independent use cases with the real APIs."""

import json
import shutil
import threading
from contextlib import contextmanager
from functools import partial
from html import escape
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import JsonLexer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.name
CAPTURES = ROOT / "build/demo-captures"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


@contextmanager
def serve():
    handler = partial(QuietHandler, directory=str(CAPTURES))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def case_page(language):
    """Create the case fixture; screenshots are independent of demo controls."""
    spanish = language == "es"
    style = (ROOT / "docs/assets/demo/demo.css").read_text()
    style += "main{max-width:960px} .case-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}"
    style += ".output{grid-column:1/-1} pre{margin:0;font-size:15px} .profile{padding:30px 60px}"
    style += ".profile input{max-width:500px} .profile button{display:block;margin-top:28px} .eyebrow{font-weight:700;color:var(--demo-accent)}"
    if PROJECT.endswith("paylo"):
        from paylo import render_template

        template = {"name": "{{customer.name}}", "active": "{{active}}", "count": "{{count}}"}
        values = {"customer": {"name": "Ana"}, "active": True, "count": 3}
        result = render_template(template, values)
        assert result == {"name": "Ana", "active": True, "count": 3}
        labels = (
            ["Plantilla", "Datos de la iteración", "Cuerpo preparado para la API"]
            if spanish
            else ["Template", "Iteration data", "API request body"]
        )
        blocks = []
        focus_lines = ([2, 3, 4], [3, 5, 6], [2, 3, 4])
        for index, (label, data) in enumerate(zip(labels, [template, values, result])):
            formatter = HtmlFormatter(nowrap=True, hl_lines=focus_lines[index])
            code = highlight(json.dumps(data, indent=2), JsonLexer(), formatter)
            blocks.append(
                f'<section class="panel {"output" if index == 2 else ""}"><h2>{label}</h2><pre><code>{code}</code></pre></section>'
            )
        style += ".nt{color:var(--demo-accent)} .s2{color:#226c60} .kc,.mi{color:#6554C0;font-weight:700} .hll{background:#d8efe7}"
        title = "Preparar el alta de un cliente" if spanish else "Prepare a customer request"
        subtitle = (
            "Los valores anidados se resuelven; booleanos y números conservan su tipo."
            if spanish
            else "Nested values resolve; booleans and numbers keep their types."
        )
        content = f'<p>{subtitle}</p><div class="case-grid">{"".join(blocks)}</div>'
    else:
        title = "Actualizar el perfil de un cliente" if spanish else "Update a customer profile"
        name, email, save = (
            ("Nombre", "Correo", "Guardar cambios")
            if spanish
            else ("Name", "Email", "Save changes")
        )
        saved = "Cambios guardados" if spanish else "Changes saved"
        content = f"""<section class="panel profile"><h2>{"Datos de contacto" if spanish else "Contact details"}</h2>
        <form onsubmit="event.preventDefault();document.getElementById('notice').textContent='{saved}'">
        <label for="name">{name}</label><input id="name" value="Ana Martínez">
        <label for="email">{email}</label><input id="email" type="email" value="ana.old@example.com">
        <button id="save" type="submit">{save}</button><p id="notice" role="status"></p></form></section>"""
    return f'<!doctype html><html lang="{language}"><meta charset="utf-8"><style>{style}</style><main><p class="eyebrow">{escape(PROJECT.removeprefix("robotframework-").title())} · {"Caso de uso" if spanish else "Use case"}</p><h1>{title}</h1>{content}</main></html>'


def validate_demo(browser, language):
    # Exercise the same iframe and palette as the documentation, including live theme changes.
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
    assert not browser.find_elements(By.ID, "language")
    assert browser.find_element(By.TAG_NAME, "html").get_attribute("lang") == language
    if PROJECT.endswith("marka"):
        browser.execute_script("document.getElementById('color').value='#2673D9'")
        width = browser.find_element(By.ID, "width")
        width.clear()
        width.send_keys("5")
        for identifier in ("highlight", "dots", "note", "save"):
            browser.find_element(By.ID, identifier).click()
        WebDriverWait(browser, 10).until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "[data-marka-id]")) == 4
        )
        assert browser.find_element(By.ID, "notice").text == (
            "Guardado" if language == "es" else "Saved"
        )
        style = browser.find_element(By.CSS_SELECTOR, "[data-marka-id]").value_of_css_property
        assert style("border-top-width") == "5px"
        assert Color.from_string(style("border-top-color")).hex == "#2673d9"
        assert Color.from_string(style("background-color")).hex == "#2673d9"
        gap = browser.execute_script(
            "const target=document.getElementById('email').getBoundingClientRect();const dot=[...document.querySelectorAll('[data-marka-id]')].find(n=>n.textContent==='1').getBoundingClientRect();return target.left-dot.right;"
        )
        assert abs(gap - 10) < 1
        browser.find_element(By.ID, "clear").click()
        assert not browser.find_elements(By.CSS_SELECTOR, "[data-marka-id]")
    else:
        from paylo import render_template

        template = json.loads(browser.find_element(By.ID, "template").get_attribute("value"))
        variables = json.loads(browser.find_element(By.ID, "variables").get_attribute("value"))
        assert json.loads(browser.find_element(By.ID, "result").text) == render_template(
            template, variables
        )
    for scheme in ("slate", "default"):
        browser.switch_to.default_content()
        browser.execute_script("document.body.dataset.mdColorScheme=arguments[0]", scheme)
        browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
        expected = "dark" if scheme == "slate" else "light"
        WebDriverWait(browser, 10).until(
            lambda driver: (
                driver.find_element(By.TAG_NAME, "html").get_attribute("data-theme") == expected
            )
        )
        bg = Color.from_string(
            browser.find_element(By.TAG_NAME, "body").value_of_css_property("background-color")
        ).hex
        assert bg == (
            "#101827"
            if scheme == "slate"
            else "#fff7f2"
            if PROJECT.endswith("marka")
            else "#f5f3fc"
        )
        panel = browser.find_element(By.CLASS_NAME, "panel").value_of_css_property(
            "background-color"
        )
        assert panel not in ("rgb(255, 255, 255)", "rgba(255, 255, 255, 1)")
    browser.switch_to.default_content()
    browser.set_window_size(390, 900)
    browser.switch_to.frame(browser.find_element(By.TAG_NAME, "iframe"))
    assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
    browser.switch_to.default_content()
    browser.set_window_size(1100, 780)


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
CAPTURES.mkdir(parents=True, exist_ok=True)
with serve() as base, webdriver.Chrome(options=options) as browser:
    browser.set_window_size(1100, 780)
    for language in ("en", "es"):
        directory = CAPTURES / language
        shutil.copytree(ROOT / "docs/assets", directory / "assets", dirs_exist_ok=True)
        harness = '<!doctype html><link rel="stylesheet" href="assets/stylesheets/visual.css"><body data-md-color-scheme="default" style="margin:0"><iframe src="assets/demo/index.html" style="width:100%;height:1200px;border:0"></iframe></body>'
        (directory / "index.html").write_text(harness)
        browser.get(f"{base}/{language}/index.html")
        validate_demo(browser, language)
        (directory / "case.html").write_text(case_page(language))
        browser.get(f"{base}/{language}/case.html")
        # Fit the complete use case inside one viewport; never stitch or crop.
        geometry = browser.execute_script(
            "return {height:Math.ceil(document.querySelector('main').getBoundingClientRect().bottom"
            "+parseFloat(getComputedStyle(document.body).paddingBottom)),"
            "chrome:outerHeight-innerHeight};"
        )
        browser.set_window_size(1100, geometry["height"] + geometry["chrome"])
        assert browser.execute_script(
            "return document.querySelector('main').getBoundingClientRect().bottom <= innerHeight"
        )
        if PROJECT.endswith("marka"):
            from marka import Annotator

            email = browser.find_element(By.ID, "email")
            email.clear()
            email.send_keys("ana@example.com")
            save = browser.find_element(By.ID, "save")
            marks = Annotator(browser)
            marks.add(email, color="#2673D9", background="rgba(38,115,217,0.12)", width=5)
            marks.add(
                email, kind="dot", text="1", color="#2673D9", position="left", text_color="white"
            )
            marks.add(
                save, kind="dot", text="2", color="#2673D9", position="left", text_color="white"
            )
            marks.add(
                save,
                kind="note",
                text="Guardar los cambios" if language == "es" else "Save the changes",
                color="#567344",
                position="right",
                text_color="white",
            )
            # The second step must not overlap the email field.
            assert browser.execute_script(
                "const email=document.getElementById('email').getBoundingClientRect();"
                "const dot=[...document.querySelectorAll('[data-marka-id]')]"
                ".find(n=>n.textContent==='2').getBoundingClientRect();return dot.top>email.bottom;"
            )
            save.click()
            assert browser.find_element(By.ID, "notice").text == (
                "Cambios guardados" if language == "es" else "Changes saved"
            )
            output = ROOT / f"docs/assets/demo/annotated-profile-{language}.png"
            marks.capture(output)
            assert not browser.find_elements(By.CSS_SELECTOR, "[data-marka-id]")
        else:
            output = ROOT / f"docs/assets/demo/payload-result-{language}.png"
            assert browser.save_screenshot(str(output))
        assert output.stat().st_size > 1000
        print(
            f"{PROJECT} {language}: embedded demo, live themes, mobile width and real use-case capture passed"
        )
