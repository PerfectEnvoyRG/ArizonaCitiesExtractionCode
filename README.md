# ArizonaCitiesZipcode

## What was the primary goal or objective of the project?
Extract the Incentive programs data from every city of Arizona State
    
## Can you briefly explain the main components of the project?
Scraping Codes and Target Data

## What technology stack did you use for your project? 
Selenium, BeautifulSoup, Python, ChatGPT prompt

## Where is the codebase stored? Do we use a version control system like Git?
Stored in Github, but I did not use any version control, I modify the code on my own desktop.

## Were there any specific challenges you encountered during the development? How did you address them?
When you use Selenium to extract data from multiple zip codes, the efficiency is very low because Selenium by default only opens one browser.
Therefore, I modified my code to make it capable of opening multiple browsers at the same time, which means I can scrape data from multiple zip codes.

## Is there any documentation or README that can help me understand the project better?
No further documentation is needed for my code because I have already written comments in it.

## Were there any third-party tools or APIs you integrated into the project?
No, i think.

## Is there any specific part of the project you believe needs improvement or refactoring?
I believe there are numerous columns that hold no significance, so I am in the process of cleaning them up.
