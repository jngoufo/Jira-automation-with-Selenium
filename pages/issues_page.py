from colorama import Fore, Back, Style, init
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.locators import IssuePageLocators


class Issuepage(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def viewissue(self, issue):
        customerservicequeue_url = "https://justingoufo.atlassian.net/jira/servicedesk/projects/CS/queues/custom/1"
        self.driver.get(customerservicequeue_url)
        customerservice_queue_name = self.driver.find_element(By.CSS_SELECTOR, IssuePageLocators.customerservice_queue_name)
        self.wait_for_presence_of_all_elements(".issuekey")
        print(Style.BRIGHT + f"Chargement de la page: '{self.driver.title}'...")
        print(Style.BRIGHT + f"la page '{self.driver.title}' est chargée")
        issuekey_list = self.driver.find_elements(By.CSS_SELECTOR, IssuePageLocators.customerservice_issue_keys)
        print(Style.BRIGHT + f"Vérification de l'affichage des billets du projet '{customerservice_queue_name}'")
        try:
            if not issuekey_list:
                print(Fore.YELLOW + "Aucun billet listé.")
                print(Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"{len(issuekey_list)} billet(s) listé(s).")
                cs_1 = issue
                billets = []
                for b in issuekey_list:
                    print (b.text)
                    billets.append(b.text)
                assert cs_1 in billets, Fore.RED + f"Element '{cs_1}' was not found in the list {billets}"
                print(Fore.GREEN + f"Test passed: Element '{cs_1}' is in the list {billets}.")
                print(Style.RESET_ALL)
        except TimeoutException:
            print(Fore.CYAN + f"Timeout : Les éléments avec le sélecteur '{selecteur_customerserviceissues}' n'ont pas été trouvés dans le temps imparti.")
            print(Style.RESET_ALL)
        except NoSuchElementException:
            print(Fore.CYAN + f"Aucun élément trouvé avec ce sélecteur CSS : '{selecteur_customerserviceissues}' 🤷")
            print(Style.RESET_ALL)
        except Exception as e:
            print(Fore.CYAN + f"Une erreur est survenue: {e}")
            print(Style.RESET_ALL)
