# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os

chromeDriverSrc = "C:\\Users\\rhyme\\Downloads\\selenium\\chromedriver.exe"
options = webdriver.ChromeOptions()

driver = webdriver.Chrome(executable_path=chromeDriverSrc, options=options)
employmentInformationUrlList = []
nameOfCompanyPosted = []
duplicationCheck = [] # by company name

# Login logic
loginUrl = "https://www.rocketpunch.com/login?next_url=/jobs"
driver.get(loginUrl)
driver.find_elements_by_xpath('//*[@id="form-login-social"]/div[1]/div[2]/a')[0].click()

# insert email account
driver.implicitly_wait(2)
email = driver.find_elements_by_xpath('//*[@id="identifierId"]')[0]
email.send_keys("rhyme884")
driver.find_elements_by_xpath('//*[@id="identifierNext"]')[0].click()

# insert password
time.sleep(6)
pwd = driver.find_elements_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')[0]
pwd.send_keys("moon**4035")
driver.find_elements_by_xpath('//*[@id="passwordNext"]')[0].click()

time.sleep(8)
if len(driver.find_elements_by_xpath('//*[@id="submit_approve_access"]')) > 0:
    driver.find_elements_by_xpath('//*[@id="submit_approve_access"]')[0].click()

# After logged in successfully,
for i in range(1, 40):
    baseDomain = "https://www.rocketpunch.com/jobs?job=sw-developer" \
                 "&location=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C" \
                 "&location=%EA%B2%BD%EA%B8%B0%EB%8F%84&page={index}".format(index=i)
    formattedDomain = "window.open('{url}')".format(url=baseDomain)
    driver.execute_script(formattedDomain)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(4)
    tagWithHref = driver.find_elements_by_xpath('//a[@href]')
    for tag in tagWithHref:
        employmentUrlHeader = "https://www.rocketpunch.com/companies/"
        if tag.get_attribute("href")[:len(employmentUrlHeader)] == employmentUrlHeader \
                and "/job" in tag.get_attribute("href") and "/applicants" not in tag.get_attribute("href"):
            employmentInformationUrlList.append(tag.get_attribute("href"))

    driver.close();
    driver.switch_to.window(driver.window_handles[0])

# directory = os.getcwd()
csv = open('crawled.csv', mode='w', encoding='utf-8')
# excel headers
csv.write("기업명,이메일,연락처,산업 분야,기업 프로필,채용 공고 수,채용 공고 제목,회사 도메인(웹사이트),구성원 수,투자유치,설립일,년차,사무실 주소,지역 범위\n")
csv.flush()
i = 0
while i < len(employmentInformationUrlList):
    formattedDomain = "window.open('{url}')".format(url=employmentInformationUrlList[i])
    driver.execute_script(formattedDomain)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)

    companyName = driver.find_elements_by_xpath('//*[@id="company-name"]/h1')[0].text
    jobs = driver.find_elements_by_xpath('(//*[@id="company-jobs"]/div)')
    info = driver.find_elements_by_xpath('//*[@id="company-info"]/div')[0].text.split('\n')
    offices = len(driver.find_elements_by_class_name('address'))
    infoMap = dict({})

    print(companyName)
    if companyName not in duplicationCheck:
        if '설립일' in info:
            split = info[info.index('설립일')+1].split(" / ")
            infoMap['설립일'] = split[0]
            infoMap['년차'] = split[1]
        else: infoMap['설립일'] = ""
        if '이메일' in info:
            infoMap['이메일'] = info[info.index('이메일')+1].replace(",", "")
        else: infoMap['이메일'] = ""
        if '산업 분야' in info:
            infoMap['산업 분야'] = info[info.index('산업 분야')+1].replace(",", '/')
        else: infoMap['산업 분야'] = ""
        if '홈페이지' in info:
            infoMap['홈페이지'] = info[info.index('홈페이지')+1].replace(",", "")
        else: infoMap['홈페이지'] = ""
        if '구성원' in info:
            infoMap['구성원'] = info[info.index('구성원')+1].replace("상세보기", "")
        else: infoMap['구성원'] = ""
        if '투자유치' in info:
            withoutDelimiter = info[info.index('투자유치')+1].replace(",", "")
            infoMap['투자유치'] = withoutDelimiter.replace("상세보기", "")
        else: infoMap['투자유치'] = ""
        if '사무실' in info:
            fullOfficeLoc = ""
            for k in range(1, offices + 1):
                fullOfficeLoc += info[info.index('사무실')+k].replace(",", "") + " / "
            infoMap['사무실'] = fullOfficeLoc.replace("\n", " ")
        else: infoMap['사무실'] = ""
        if '전화번호' in info:
            infoMap['전화번호'] = info[info.index('전화번호')+1].replace(",", "")
        else: infoMap['전화번호'] = ""

        jobsTitle = ""
        j = 0
        for j in range(len(jobs)):
            jobsTitle += jobs[j].text.split("\n")[3] + " / "
        introductionOfCompany = driver.find_elements_by_xpath('//*[@id="company-overview"]/div')[0].text.replace(",", "")
        introductionOfCompany = introductionOfCompany.replace("\n", " ")
        introductionOfCompany = introductionOfCompany.replace("더 보기", "")

        csv.write(companyName + "," + str(infoMap.get('이메일')) + "," + str(infoMap.get('전화번호')) + "," + str(infoMap.get('산업 분야')) + ","
                  + str(introductionOfCompany) + "," + str(len(jobs)) + "," + str(jobsTitle) + ", " + str(infoMap.get("홈페이지")) + ","
                  + str(infoMap.get("구성원")) + "," + str(infoMap.get("투자유치")) + "," + str(infoMap.get("설립일")) + "," + str(infoMap.get("년차")) + ","
                  + str(infoMap.get("사무실") + ","))
        if "경기" in infoMap.get("사무실"):
            csv.write("경기지역\n")
        else:
            csv.write("서울특별시\n")

        duplicationCheck.append(companyName)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    i += 2

csv.flush()
csv.close()
time.sleep(5)
driver.quit()

# 채용 회사명 //*[@id="company-name"]/h1
# 대표자명
# 기업 프로필 driver.find_elements_by_xpath('//*[@id="company-overview"]/div')[0].text
# 채용 공고 수 len(//*[@id="company-jobs"]/div)
# 채용 공고 제목 //*[@id="company-jobs"]/div[i]/div/div[1]/div[i]/a
# 채용 정보 url (employmentInformationUrlList[i])
# driver.find_elements_by_xpath('//*[@id="company-info"]/div')[0].text

# info = driver.find_elements_by_xpath('//*[@id="company-info"]/div')
# 설립일 / 년차 : driver.find_elements_by_xpath('//*[@id="company-info"]/div/div/div[1]/div[2]')[0].text.split(' / ')
# 전화번호(회사, 개인 휴대폰)
# 구성원 수 driver.find_elements_by_xpath('//*[@id="company-info"]/div/div/div[2]/div[2]')[0].text
# 투자유치 //*[@id="company-info"]/div/div/div[3]/div[2]
# 회사 도메인 //*[@id="company-info"]/div/div/div[4]/div[2]/a
# 이메일 //*[@id="company-email"]/a
# 사무실 주소 //*[@id="company-info"]/div/div/div[7]/div[2]/div/span[2]
# 산업 분야 //a[matches(@href, "/companies?tag-[\S]*")]
# //*[@id="company-info"]/div/div/div[9]/div[2]/div/span[2]
# 지역 범위 사무실 주소.find("경기") => 경기 else "서울"
