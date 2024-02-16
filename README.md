# 2dehands.be: Authenticating and Crawling with Scrapy and Playwright
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scrapy](https://img.shields.io/badge/scrapy-50962d?style=for-the-badge&logo=scrapy&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2b3137?style=for-the-badge&logo=playwright&logoColor=orange)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)


![Scrapy and Playwright](./assets/scrapy-playwright.png)

## 📖 Introduction

Welcome to my GitHub repository, where we blend the strengths of Scrapy with the speed and simplicity of Playwright for 
advanced web scraping. My journey began with an interest in combining Selenium and Scrapy to tackle JavaScript-heavy 
websites. As a testcase I will make the program log in to my [2dehands.be](https://www.2dehands.be/) account and scrape 
the saved searches for my user. (you can have a peak in the screenshot below) 
Before starting the project, I wandered a bit around on github and discovered Playwright. It skyrocketed in popularity 
in the last 4 years. In the [Why Playwrigh? Is Selenium left behind?](#why-playwright-is-selenium-left-behind) section 
I go into more detail about this.

## 📦 Repo structure
```
.
├── data
│   └── data.jsonl           # the result of the spider
├── log
│   └── screenshots
│       └── ...              # screenshots of the crawled pages
├── README.md
├── requirements.txt
├── scrapy.cfg
└── tweedehands
    ├── __init__.py
    ├── items.py             # the data model
    ├── middlewares.py
    ├── pipelines.py         # the pipeline that saves the data
    ├── settings.py          # settings for the spider
    └── spiders
        ├── __init__.py
        └── tweedehands.py   # the spider
```


## 🚀 To start crawling the pages

### install requirements
```bash
pip install -r requirements.txt
```

### Add some saved searches
Go to [2dehands.be](https://www.2dehands.be) log in and save some searches. You can find them in the 
"Mijn Zoekopdracten" section.

### Configure the environment variables

#### For Linux
Add the environment variables to `/etc/environment` and **restart** your computer 
```bash
# /etc/environment
TWEEDHANDS_USERNAME=**your_tweedehands_username**
TWEEDHANDS_PASSWORD=**your_twedehands_password**
```

#### For Windows
This project is not tested on windows, but you can try the following:
Add the environment variables to the system environment variables and **restart** your computer
Search "Edit environment variables" in Start Menu, click it, then add or modify variables.

### Launch the spider
```bash
scrapy crawl tweedehands
```

### Result

You can find the result in `data/data.jsonl` 
## Screenshot
![Screenshot](./assets/my_searches.png)

## Why Playwright? Is Selenium left behind?
Github stars don't say everything but they do give an indication of the popularity of a project. Below you can see the
history of the `Scrapy` and `Playwright` projects and some of their siblings: `Selenium`. In my limited experience with 
`Playwright` I found that `Playwright` is very easy to Install and use. No more wedrivers to manage and or install.
It supports async which and is faster. The code code is more readable and easier and less tedious because there is an 
auto waiting for elements. Below I made 2 sample scripts that log in to reddit. 1 in `Selenium` and 1 in `Playwright`.
### Selenium code example
```python
# selenium example - illustrative dummy code
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver_path = '/path/to/your/webdriver'
driver = webdriver.Chrome(driver_path)
driver.get('https://www.reddit.com/login/')

username_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "loginUsername"))
)
username_field.send_keys('your_username')
password_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "loginPassword"))
)
password_field.send_keys('your_password')
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Log In")]'))
)
login_button.click()
```
### Playwright code example
```python
# playwright example - illustrative dummy code
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto('https://www.reddit.com/login/')
        await page.fill('input#loginUsername', 'your_username')
        await page.fill('input#loginPassword', 'your_password')
        await page.click('button[type="submit"]')
        await browser.close()

asyncio.run(main())
```

### Github star history
[![Star History Chart](https://api.star-history.com/svg?repos=microsoft/playwright,SeleniumHQ/selenium,scrapy/scrapy&type=Date)](https://star-history.com/#microsoft/playwright&SeleniumHQ/selenium&scrapy/scrapy&Date)

### Conclusion
> When it comes to web crawling, Playwright truly "plays right" into developers' hands with its simplicity and power.

Is Selenium left behind than? In a lot of ways yes. But Selenium still has its strength especially for software testing 
as it has a broader support and a solid community and foundation. Also, alot of projects are already build on Selenium, 
and turning a project that is head deep in Selenium will probably not compensate the benefits of Playwright. If you are 
into web scraping So I would highly recommend playing around with Playwright.

## ⏱️ Timeline
In the course of developing this project, I dedicated two full days not just to building but also to research 
and explore libraries.

## 📌 Personal Situation
My enthusiasm for initiating a project with Scrapy and Selenium was so intense that it inadvertently bypassed the 
crucial step of preparing: do your research first!. So I dived into this project head first! Because of this I rotated 
half way the project from Selenium to Playwright.
Note to self: Always do your research first! No matter how excited you are about a project!

## Disclaimer
The actions performed by the program do not abide by the robots.txt of 2dehands.be, this project is ment for educational 
purpose only. Run at your own risk.

## Possible issues
I had to log in to [2dehands.be](https://www.2dehands.be/) the first time with 2fa. But once it knows my IP the 2fa is not needed anymore and playwright could log in with 1 step.
If you do think you are experiencing issues, make sure to check the screenshots' folder. It will have screenshot before and after the login.

## Connect with me!
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gerrit-geeraerts-143488141)
[![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/10213635/gerrit-geeraerts)
[![Ask Ubuntu](https://img.shields.io/badge/-Askubuntu-dd4814?style=for-the-badge&logo=ubuntu&logoColor=white)](https://askubuntu.com/users/1097288/gerrit-geeraerts)

## Links

[The Python Scrapy Playbook | ScrapeOps](https://scrapeops.io/python-scrapy-playbook/): I found lots of great info here.