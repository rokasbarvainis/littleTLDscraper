import os
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def writeToColumn(filename, list):
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        for e in list:
            wr.writerow([e])


def writeToRow(filename, list):
    with open(filename, 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(list)


# Scape from www.iwantmyname.com
def iWantMyName():
    extensionList = []
    driver = webdriver.Firefox(executable_path=str(os.getcwd())+'/geckodriver')
    driver.get("https://iwantmyname.com/domains")

    for x in range(1, 511):
        extension = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[2]/div[2]/ul/li[' + str(x) + ']/span[1]')
        extensionText = 'www.domain.' + extension.text[1:].lower()
        extensionList.append(extensionText)

    driver.close()

    writeToColumn('extensions1.csv', extensionList)
    return extensionList


# Scrape from www.domain.com
def domain():
    extensionList = []
    driver = webdriver.Firefox(executable_path=str(os.getcwd()) + '/geckodriver')
    driver.get("https://www.domain.com/domains/new-domain-extensions")
    time.sleep(5)  # some time to click the pop-up accept manually

    # for every letter
    for abc in range(1, 27):
        elem = driver.find_element_by_xpath('/html/body/section/section[2]/div/div[1]/a[' + str(abc) + ']')
        elem.click()  # open new letter
        letter = elem.text.lower()  # current letter
        table_id = driver.find_element(By.ID, letter) # find table by id
        tbody = table_id.find_element(By.CSS_SELECTOR, 'tbody')  # find table body
        rows = tbody.find_elements(By.CLASS_NAME, "tld-row")  # get all of the rows in the table
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[0]  # find first column of the row which is the TLD
            extensionList.append('www.domain' + col.text.lower())

    driver.close()

    writeToColumn('extensions2.csv', extensionList)
    return extensionList


# Get list of top level domains from IANA (Updates every once in a while)
def getIANAlist():
    driver = webdriver.Firefox(executable_path=str(os.getcwd()) + '/geckodriver')
    driver.get("http://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    text = driver.find_element_by_xpath('/html/body/pre').text.lower()
    driver.close()

    extensionList = text.split()[11:]
    newlist = []
    for e in range(0, len(extensionList)):
        newlist.append('www.domain.'+extensionList[e])

    writeToColumn('extensionsIANA.csv', newlist)
    return newlist


eList1 = iWantMyName()  # iwantmyname.com
eList2 = domain()  # domain.com
eListIANA = getIANAlist()  # https://www.icann.org/resources/pages/tlds-2012-02-25-en
filteredList = set(eList2).union(eList1).union(eListIANA)  # a joined list from all sets without duplicates
print('-List Sizes-')
print('eList1: ' + str(len(eList1)))
print('eList2: ' + str(len(eList2)))
print('eListIANA: ' + str(len(eListIANA)))
print('Filtered: ' + str(len(filteredList)))

writeToColumn('filtered.csv', filteredList)
