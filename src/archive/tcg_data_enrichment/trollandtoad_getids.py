
# Get IDs
url = https://www.trollandtoad.com/category.php?selected-cat=7061&search-words=001%2F185+Vivid+Voltage




# Get prices
import requests
url = "https://www.trollandtoad.com/ajax/productAjax.php?productid=1057698&action=getBuyingOptions"
payload={}
headers = {
  # 'Cookie': 'beta_PxvuRUfLL2ouQMXycaqHvZW3OgByOkAN=6ZB47uIB8jkOf6TGzj1vhYlYcD-Gg9oCBbU0aTImOisyUCpn'
}
response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
