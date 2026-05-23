# Toreja Medical Clinic PMS — Playwright Python Automation

Playwright version of the Selenium automation project.
URL: http://torejamedicalclinic.wuaze.com

---

## Setup

```bash
# 1. Install Python packages
pip install -r requirements.txt

# 2. Install Playwright browsers (no ChromeDriver needed!)
playwright install chromium

# 3. Run all tests
pytest

# 4. Run by suite
pytest -m smoke
pytest -m functional
pytest -m regression
pytest -m e2e
```

---

## Key differences from the Selenium version

| Feature | Selenium | Playwright |
|---|---|---|
| Browser setup | webdriver-manager + ChromeDriver | `playwright install` — no driver |
| Waiting | `WebDriverWait(driver, 10).until(EC....)` | Auto-wait built into every action |
| Select2 click | JS click hack required | `locator().click()` works directly |
| Locators | `By.ID`, `By.CSS_SELECTOR`, `By.XPATH` | CSS strings, `:has-text()`, `:nth-child()` |
| Screenshots | `driver.save_screenshot(path)` | `page.screenshot(path=path, full_page=True)` |
| Page load | `options.page_load_strategy = "eager"` | `wait_until="domcontentloaded"` |
| Fixtures | Manual `driver` fixture | Built-in `page`, `browser`, `context` |
| Date input | `execute_script("el.value = ...")` | `page.evaluate("el.value = ...")` |

---

## Project structure

```
toreja_pms_playwright/
├── conftest.py              ← Playwright fixtures (auth_page, e2e_page, page objects)
├── pytest.ini               ← pytest config
├── requirements.txt
├── .env                     ← URL, credentials, browser, timeout
│
├── locators/
│   └── locators.py          ← All CSS selectors as string constants
│
├── pages/
│   ├── base_page.py         ← Parent class — navigation, select2_option(), set_date()
│   ├── login_page.py
│   ├── dashboard_page.py
│   ├── patients_page.py
│   ├── new_prescription_page.py
│   ├── patient_history_page.py
│   ├── medicines_page.py
│   ├── medicine_details_page.py
│   ├── reports_page.py
│   └── users_page.py
│
├── tests/
│   └── test_e2e_prescription.py
│
├── test_data/
│   └── test_data.py
│
└── utils/
    ├── config.py
    ├── logger.py
    └── test_step.py
```
