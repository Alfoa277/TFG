from nordvpn_switcher import initialize_VPN, rotate_VPN

initialize_VPN(save=1, area_input=['europe'])


# set options to be headless
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import numpy as np




PATH = "C:\Program Files\chromedriver.exe"


url="https://www.idealista.com/venta-viviendas/las-palmas-de-gran-canaria-las-palmas/"


def scrapePage(driver, fileName,scrapedSinceLastReset):

    if scrapedSinceLastReset>600:
        rotate_VPN()
        scrapedSinceLastReset = 0

    f = open(fileName, "a", encoding="utf-8")
    # Name of the property
    names = driver.find_elements(By.CSS_SELECTOR, "section.items-container article div.item-info-container a.item-link")
    # Obtengo el "price row" que contiene el precio actual, si tiene garaje o no, y precio anterior si ha sido reducido
    price_row = driver.find_elements(By.CSS_SELECTOR,
                                     "section.items-container article div.item-info-container div.price-row")
    # Details (number of rooms, area...)
    details = driver.find_elements(By.CSS_SELECTOR,
                                   "section.items-container article div.item-info-container div.item-detail-char")

    for name_, price_, detail_ in zip(names, price_row, details):
        scrapedSinceLastReset+=1
        price_elem = price_.text.split('\n')
        # Remove € and . signs
        price = price_elem[0][:-5].replace('.', '')
        s = ''
        # Add name information
        s += name_.text + ';'

        # Add details information
        # s+=detail_.text
        # Parse details (length is variable depending on the information given by the seller)
        details_list = detail_.text.split(' ')
        new_details = []
        # Parse number of rooms and area
        hab = False
        area = False
        elems = []

        for i in range(min(4, len(details_list))):
            elem = details_list.pop(0)
            if i % 2 == 0:
                elems.append(elem)
            if elem[0] == "h":
                hab = True
            if elem[0] == "m":
                area = True

        if hab and area:
            s += elems[0] + ';' + elems[1] + ';'
        elif hab:
            s += elems[0] + ';0;'
        elif area:
            s += '0;' + elems[0] + ';'
        else:
            s += '0;0;'

        if len(details_list) > 0:
            # There are more details besides number of bedrooms and area
            if details_list[0] == "Planta":
                details_list.pop(0)
                s += details_list.pop(0)[:-1] + ';'  # Get rid of the ª/º symbol
            else:
                s += '0;'
            try:
                if details_list[0] == "exterior" or details_list[0] == "interior":
                    s += details_list.pop(0) + ';'
                else:
                    s += "UNK;"
            except:
                s += "UNK;"
            try:
                if details_list[0] == "con":
                    s += "True;"
                else:
                    s += 'False;'
            except:
                s += 'UNK;'
        else:
            s += "UNK;UNK;UNK;"

        # print(detail_.text.split(' '))

        # Add price information
        s += price + ';'
        if len(price_elem) > 1:
            if len(price_elem) == 3:
                if price_elem[1] == 'Garaje incluido':
                    s += 'True;0;'
                elif price_elem[1][:6] == 'Garaje': # Garaje opcional
                    garage_elements = price_elem[1].split(' ')
                    garage_price = garage_elements[2]
                    garage_price = garage_price.replace('.','')
                    s+='True;'+garage_price+';'
                else:
                    s += 'False;-1;'
                # Obtain price without € and . signs and ignore percentage of change
                old_price = price_elem[2]
                old_price = old_price.split(' ')
                old_price = old_price[0].replace('.', '')
                if int(price) < int(old_price):
                    s += old_price + ';Decrease'
                elif int(price) == int(old_price):
                    s += old_price + ';Equal'
                else:
                    s += old_price + ';Increase'
            else:
                if price_elem[1] == 'Garaje incluido':
                    s += 'True;0;' + price + ';Equal'
                elif price_elem[1][:6] == 'Garaje':  # Garaje opcional
                    garage_elements = price_elem[1].split(' ')
                    garage_price = garage_elements[2]
                    garage_price = garage_price.replace('.', '')
                    s += 'True;' + garage_price + ';'+price+';Equal'
                else:
                    old_price = price_elem[1]
                    old_price = old_price.split(' ')
                    old_price = old_price[0].replace('.', '')
                    if int(price) < int(old_price):
                        s += 'False;-1;' + old_price + ';Decrease'
                    elif int(price) == int(old_price):
                        s += 'False;-1;' + old_price + ';Equal'
                    else:
                        s += 'False;-1;' + old_price + ';Increase'

        else:
            # If length is 1, then add False for Garage, -1 price for garage same price for property,
            # and Equal for price change
            s += 'False;-1;' + price + ';Equal'
        f.write(s + '\n')
    f.close()
    return scrapedSinceLastReset


def scrapeArea(initialUrl, provinceName, scrapedSinceLastReset):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled') # Removes aumation control flag
    #options.add_argument(
    #    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(initialUrl)
    # Added ActionChains to click "Siguiente" without getting a "Other element would receive click" error message
    actions = ActionChains(driver)

    hOne = driver.find_element(By.CSS_SELECTOR, "#h1-container")
    findTotalProperties = hOne.text.split(' ')
    findTotalProperties = findTotalProperties[0].replace('.','')
    if int(findTotalProperties)>1800:
        dropDown = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-navigation-current-level")

        # The correct dropdown link is the first
        rightLink = dropDown[0]

        # Clicking the right link is not useful in the beginning because there is an "accept cookies" popup that must be
        # dealt with first.
        next_button = driver.find_element(By.CSS_SELECTOR, "a.icon-arrow-right-after span")
        actions.move_to_element(next_button).click().perform()  # Luckily, clicking the next button

        actions.move_to_element(rightLink).click().perform()

        moreLinks = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-dropdown-subitem-element-list a")
        numbers = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-navigation-sidenote")
        numbers = numbers[1:]
        area_name = initialUrl.split('/')
        for i in moreLinks:
            newLink = i.get_attribute('href')
            time.sleep(np.random.uniform(0.5, 1))
            newProvinceName = provinceName + '_' + area_name[-2]
            scrapedSinceLastReset = scrapeArea(newLink, newProvinceName, scrapedSinceLastReset)
            print(newLink)
            #TODO: 10,20
            #time.sleep(np.random.uniform(1.5, 2.5))
        return scrapedSinceLastReset
    else:
        area_name = initialUrl.split('/')
        """conditionName = False
        fileNameIndex = 4
        area=''
        while not conditionName:
            string = area_name[fileNameIndex]
            if len(string.split('-')) == 1:
                fileNameIndex += 1
                area+=string+'_'
            else:
                conditionName = True
                area += string"""
        fileName = provinceName+'_' + area_name[-2] + '_RENT.csv'
        f = open(fileName, "w", encoding="utf-8")
        f.write("NAME;ROOMS;AREA;FLOOR;LOCATION;ELEVATOR;PRICE;GARAGE;GARAGE_PRICE;OLD_PRICE;CHANGE_IN_PRICE\n")
        f.close()

        # Scrape first page
        scrapedSinceLastReset=scrapePage(driver, fileName,scrapedSinceLastReset)
        # Try to obtain Siguiente link. If there is no "Siguiente" link, then the scraping is done.
        print(driver.current_url)
        try:
            #time.sleep(np.random.uniform(0.5, 1))
            next_button = driver.find_element(By.CSS_SELECTOR, "a.icon-arrow-right-after span")
            # Clicking must be done twice on the first page...
            actions.move_to_element(next_button).click().perform()
            actions.move_to_element(next_button).click().perform()
            while next_button:
                #time.sleep(np.random.uniform(0.5, 1))
                scrapedSinceLastReset=scrapePage(driver, fileName,scrapedSinceLastReset)
                print(driver.current_url)
                next_button = driver.find_element(By.CSS_SELECTOR, "a.icon-arrow-right-after span")
                actions.move_to_element(next_button).click().perform()
            return scrapedSinceLastReset
        except:
            return -1


def scrapeProvince(initialUrl, provinceName, startingPoint):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')  # Removes aumation control flag
    # options.add_argument(
    #    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(initialUrl)
    # Added ActionChains to click "Siguiente" without getting a "Other element would receive click" error message
    actions = ActionChains(driver)

    areas = driver.find_elements(By.CSS_SELECTOR, "#location_list li ul li a")

    #driver.close()

    scrapedSinceLastReset = 0

    scrapedAreas = 0
    areaStart = startingPoint[1]

    try:
        for area in areas[areaStart:]:
            #time.sleep(np.random.uniform(0.5, 1))
            scrapedSinceLastReset = scrapeArea(area.get_attribute('href'), provinceName, scrapedSinceLastReset)
            if scrapedSinceLastReset == (-1):
                raise ValueError("Unfinished scraping")
            scrapedAreas+=1
        return 0
    except:
        indexReturn = scrapedAreas + areaStart
        return indexReturn



def scrapeIdealista(startingPoint):
    url="https://www.idealista.com/alquiler-viviendas/#municipality-search"
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')  # Removes aumation control flag
    # options.add_argument(
    #    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    # Added ActionChains to click "Siguiente" without getting a "Other element would receive click" error message
    actions = ActionChains(driver)

    provinces = driver.find_elements(By.CSS_SELECTOR, "div.locations-list ul li a")
    names_ = driver.find_elements(By.CSS_SELECTOR, ".locations-list ul li a")
    names=[]
    for name in names_:
        names.append(name.text)
    # Remove redundant indices
    indexes = [2,5,6,10,11,15,16,17,19,20,21,26,37,42,44,45,46,51,52,53,55,56,60,65,69,68,72,78,81,84]
    indexes.sort(reverse=True)

    for i in indexes:
        provinces.pop(i)
        names.pop(i)

    #driver.close()

    scrapedProvinces = 0
    provinceStart = startingPoint[0]

    try:
        for province, name in zip(provinces[provinceStart:],names[provinceStart:]):
            if scrapedProvinces != 0:
                rotate_VPN()
            #time.sleep(np.random.uniform(15,30))
            result = scrapeProvince(province.get_attribute("href"), name, startingPoint)
            if result != 0:
                indexProvince = provinceStart + scrapedProvinces
                return [indexProvince,result]
            else:
                startingPoint[1] = 0
                scrapedProvinces+=1
            #time.sleep(np.random.uniform(4, 7))
        return []
    except:
        indexProvince = provinceStart + scrapedProvinces
        return [indexProvince, 0]


def scrapeProvinceLimited(initialUrl, provinceName, startingPoint):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')  # Removes aumation control flag
    # options.add_argument(
    #    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(initialUrl)
    # Added ActionChains to click "Siguiente" without getting a "Other element would receive click" error message
    actions = ActionChains(driver)

    areas = driver.find_elements(By.CSS_SELECTOR, "#location_list li ul li a")

    #driver.close()

    scrapedSinceLastReset = 0
    rotate_VPN()
    for area in areas[startingPoint:]:
        time.sleep(np.random.uniform(1.5, 2.5))
        scrapedSinceLastReset = scrapeArea(area.get_attribute('href'), provinceName, scrapedSinceLastReset)
        #time.sleep(np.random.uniform(2.5, 3.5))

def scrapeAreaTempFake(initialUrl):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled') # Removes aumation control flag
    #options.add_argument(
    #    "user-agent= Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(initialUrl)
    # Added ActionChains to click "Siguiente" without getting a "Other element would receive click" error message
    actions = ActionChains(driver)

    hOne = driver.find_element(By.CSS_SELECTOR, "#h1-container")
    findTotalProperties = hOne.text.split(' ')
    findTotalProperties = findTotalProperties[0].replace('.','')
    if int(findTotalProperties)>1800:
        dropDown = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-navigation-current-level")

        # The correct dropdown link is the first
        rightLink = dropDown[0]

        # Clicking the right link is not useful in the beginning because there is an "accept cookies" popup that must be
        # dealt with first.
        next_button = driver.find_element(By.CSS_SELECTOR, "a.icon-arrow-right-after span")
        actions.move_to_element(next_button).click().perform() #Luckily, clicking the next button

        actions.move_to_element(rightLink).click().perform()

        moreLinks = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-dropdown-subitem-element-list a")
        numbers = driver.find_elements(By.CSS_SELECTOR, ".breadcrumb-navigation-sidenote")
        numbers = numbers[1:]

        for i in moreLinks:
            newLink = i.get_attribute('href')
            #time.sleep(np.random.uniform(7, 10))
            print(newLink)
            #scrapeAreaTempFake(newLink)
            #time.sleep(np.random.uniform(10, 20))
        pass
    else:
        print(initialUrl)

#scrapeArea(url)
#scrapeAreaTemp(url,'Gran Canaria', 0)
#scrapeProvince(url)
#scrapeIdealista()
#scrapeProvinceLimited("https://www.idealista.com/venta-viviendas/malaga-provincia/municipios","Málaga",75)

condition = True
newList = [13,0]

while condition:
    rotate_VPN()
    newList = scrapeIdealista(newList)
    if newList:
        rotate_VPN()
    else:
        condition = False

