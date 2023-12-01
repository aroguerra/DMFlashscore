import time
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.flashscore.com/standings/jDTEm9zs/I3O5jpB2/#/I3O5jpB2/table/overall'  # Replace this with the target website URL

driver = webdriver.Chrome()
driver.get(url)


modified_html = driver.page_source
time.sleep(10)
print(modified_html)
team_elements = driver.find_elements(By.CLASS_NAME, 'ui-table__row')

for team_element in team_elements:
    team_name = team_element.text
    print("Team Name:", team_name)







# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     # print(soup.prettify())
#     # title_elements = soup.select('.titleColumn a')
#     main_element = soup.find("main", class_="container__liveTableWrapper tournament_page", id="mc")
#     inner_divs = main_element.find_all('div', class_='container__fsbody', id="fsbody")
#     inner_divs_2 = main_element.find_all('div', class_='sport-soccer', id="tournament-table")
#     inner_divs_3 = main_element.find_all('div', class_='ui-table__body')
#     # mydivs = soup.find_all("div", {"class":"container__liveTableWrapper tournament_page"})
#     for title_element in inner_divs_3:
#         print(title_element)
#
#     # print(response.text)  # Print the content of the response
# else:
#     print(f'Request failed with status code: {response.status_code}')
