from selenium import webdriver
from time import sleep

pages = [
    "404Answernotfound",
    "404NameNotFound",
    "CTRLF",
    "denubs",
    "Derodelantaarn",
    "Devin",
    "DROPTABLETeams",
    "example",
    "failii",
    "FirewallfortifyingFileFiddlers",
    "FlagHunters",
    "flag",
    "GibberendeGitGoobers",
    "KrisCodeCompiletNiet",
    "MaaSMadnessasaSolution",
    "Notworking",
    "OhhnoIgothacked",
    "secret",
    "skrinklydinklesronny",
    "SnackOverflow",
    "steal",
    "teamtest",
    "TheAphotics",
]


options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("http://35.233.74.3/")
driver.add_cookie(
    {"name": "session", "value": "MZAFiB3H9bK5NTMi+HCwHsl5/nCtbAD79VbQVeZuMepz"}
)
for p in pages:
    try:
        driver.get("http://localhost:8080/view/" + p)
    except Exception as e:
        print('page "' + p + '" had an error:', e)
        pass
sleep(2)  # wait for request to finish
driver.close()

#sleep(60 * 5)  # wait 5 minutes
