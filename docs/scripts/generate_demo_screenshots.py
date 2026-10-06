"""Generate bilingual documentation screenshots and validate the interactive demo."""

import json
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import WebDriverWait

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT.name
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
with webdriver.Chrome(options=options) as browser:
    browser.set_window_size(1200, 1200)
    for language in ("en", "es"):
        directory = ROOT / "build" / "demo-captures" / language / "assets"
        shutil.copytree(ROOT / "docs/assets", directory, dirs_exist_ok=True)
        browser.get((directory / "demo/index.html").as_uri())
        assert not browser.find_elements(By.ID, "language")
        assert browser.find_element(By.TAG_NAME, "html").get_attribute("lang") == language
        if PROJECT.endswith("marka"):
            # Exercise the demo's controls, which call the shipped overlay engine.
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
                "const target=document.getElementById('email').getBoundingClientRect();"
                "const dot=[...document.querySelectorAll('[data-marka-id]')]"
                ".find(n=>n.textContent==='1').getBoundingClientRect();return target.left-dot.right;"
            )
            assert abs(gap - 10) < 1
            output = ROOT / f"docs/assets/demo/annotated-profile-{language}.png"
            from marka import Annotator

            # Capture the annotated viewport through the real Python capture API.
            Annotator(browser).capture(output, clear=False)
            browser.find_element(By.ID, "clear").click()
            assert not browser.find_elements(By.CSS_SELECTOR, "[data-marka-id]")
        else:
            from paylo import render_template

            template = json.loads(browser.find_element(By.ID, "template").get_attribute("value"))
            variables = json.loads(browser.find_element(By.ID, "variables").get_attribute("value"))
            expected = render_template(template, variables)
            assert json.loads(browser.find_element(By.ID, "result").text) == expected
            assert expected["quantity"] == 3
            output = ROOT / f"docs/assets/demo/payload-result-{language}.png"
            assert browser.save_screenshot(str(output))
        assert output.stat().st_size > 1000
        # Check the same controls in a narrow viewport as well.
        browser.set_window_size(390, 900)
        assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
        browser.set_window_size(1200, 1200)
        print(f"{PROJECT} {language}: demo, screenshot and mobile width passed")
