from colorama import Fore, Back, Style, init
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.locators import ProjectPageLocators, IssuePageLocators


class Projectpage(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def viewproject(self, project):
        projectpageurl = "https://justingoufo.atlassian.net/jira/projects"
        self.driver.get(projectpageurl)
        print(Style.BRIGHT + f"Chargement de la page: '{self.driver.title}'...")
        self.wait_for_presence_of_all_elements(ProjectPageLocators.testautomation_project)
        print(Style.BRIGHT + f"la page '{self.driver.title}' est chargée")
        print(Style.BRIGHT + f"Vérification de l'affichage des projets...")
        self.wait_for_presence_of_all_elements(ProjectPageLocators.testautomation_project)
        project_names_list = self.driver.find_elements(By.CSS_SELECTOR, ProjectPageLocators.testautomation_project)
        print(Style.RESET_ALL)
        try:
            if not project_names_list:
                print(Fore.YELLOW + "Aucun projet listé.")
                print(Style.RESET_ALL)
            else:
                print(Fore.GREEN + f"{len(project_names_list)} projet(s) listé(s):")
                ta = project
                projects = []
                for p in project_names_list:
                    print(p.text)
                    projects.append(p.text)
                assert ta in projects, Fore.RED + f"Element '{ta}' was not found in the list of projects"
                print(Fore.GREEN + f"Test passed: Element '{ta}' is in the list of projects.")
                print(Style.RESET_ALL)
        except TimeoutException:
            print(
                Fore.CYAN + f"Timeout : Les éléments avec le sélecteur '{ProjectPageLocators.testautomation_project}' n'ont pas été trouvés dans le temps imparti.")
            print(Style.RESET_ALL)
        except NoSuchElementException:
            print(Fore.CYAN + f"Aucun élément trouvé avec ce sélecteur CSS : '{ProjectPageLocators.testautomation_project}' 🤷")
            print(Style.RESET_ALL)
        except Exception as e:
            print(Fore.CYAN + f"Une erreur est survenue: {e}")
            print(Style.RESET_ALL)

    #def searchproject:
    #def filterprojects: