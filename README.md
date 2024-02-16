# 2dehands.be: Authenticating and Crawling with Scrapy and Playwright
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scrapy](https://img.shields.io/badge/scrapy-50962d?style=for-the-badge&logo=scrapy&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2b3137?style=for-the-badge&logo=playwright&logoColor=orange)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![Scrapy and Playwright](./assets/scrapy-playwright.png)

## 📖 Introduction

Welcome to our GitHub repository, where we blend the strengths of Scrapy with the versatility of Playwright for 
advanced web scraping. My journey began with an interest in combining Selenium and Scrapy to tackle JavaScript-heavy 
websites. As a testcase I will make the program log in to my 2dehands.be account and scrape the saved searches for my user. 
For a more efficient approach I came across Splash an alternative to Scrapy, which uses fewer resources and is easier to 
install and run with a docker. However, Splash lead me to a dead corner as it was unable to handle javascript heavy 
websites. Going back to the research table this led me to discover Playwright. Unlike Splash, Playwright excels in 
handling complex JavaScript, offering easy installation, robust performance, and clear syntax. 

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

## Playwright Splash and Selenium
Github stars don't say everything but they do give an indication of the popularity of a project. Below you can see the
history of the `Scrapy` and `Playwright` projects and some of their siblings: `Selenium` and `Splash`.
In the Github repo of `Splash` I found a lot of open issues about the inability to run `javascript` heavy websites. 
In my limited experience with `playwright` and `Splash` I found that `Playwright` is a better alternative to `Splash`. 
It is easier to install and run, and it is more robust in handling complex `JavaScript`. `Selenium` remains a tough 
competitor, but I have become a fan of the simplicity of `Playwright`.

> When it comes to web crawling, Playwright truly "plays right" into developers' hands with its simplicity and power.

### Github star history
[![Star History Chart](https://api.star-history.com/svg?repos=microsoft/playwright,scrapinghub/splash,SeleniumHQ/selenium,scrapy/scrapy&type=Date)](https://star-history.com/#microsoft/playwright&scrapinghub/splash&SeleniumHQ/selenium&scrapy/scrapy&Date)

## ⏱️ Timeline
In the course of developing this project, I dedicated two full days not just to building but also to immersive research 
and exploration of libraries that could enhance its functionality.

## 📌 Personal Situation
My enthusiasm for initiating a project with Scrapy and Selenium was so intense that it inadvertently bypassed the 
crucial step of preparing good by doing research first. So I dived into this project head first! Because of this I 
worked less efficient and spent more time on libraries that are not suitable anymore for a modern single page applications.

## Disclaimer
The actions performed by the program do not abide by the robots.txt of 2dehands.be, this project is ment for educational 
purpose only. Run at your own risk.

## Possible issues
I had to log in to 2de hands the first time with 2fa. But once it knows my IP the 2fa is not needed anymore and playwright could log in with 1 step.
If you do think you are experiencing issues, make sure to check the screenshots' folder. It will have screenshot before and after the login.

### Connect with me!
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gerrit-geeraerts-143488141)
[![Stack Overflow](https://img.shields.io/badge/-Stackoverflow-FE7A16?style=for-the-badge&logo=stack-overflow&logoColor=white)](https://stackoverflow.com/users/10213635/gerrit-geeraerts)
[![Ask Ubuntu](https://img.shields.io/badge/-Askubuntu-dd4814?style=for-the-badge&logo=ubuntu&logoColor=white)](https://askubuntu.com/users/1097288/gerrit-geeraerts)