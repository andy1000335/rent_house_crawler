# 591 租屋網爬蟲
### python 進階爬蟲
### 使用 selenium 套件模擬瀏覽器行為

- 控制 Chrome 瀏覽器
```python
from selenium import webdriver
driver = webdriver.Chrome()
driver.get(url)    #開啟網頁
```
- 模擬滑鼠點擊
```python
action = ActionChains(driver)
action.click(...).perform() 
```
