import os # Import the os module to access environment variables
import pytest
import time
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# Initialize Colorama
init(autoreset=True)

@pytest.fixture(scope="class")
def login(request):

    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)
    accounturl = "https://justingoufo.atlassian.net/jira/your-work"
    driver.get(accounturl)
    request.cls.driver = driver
    request.cls.wait = wait
    print(Style.BRIGHT + f"Ouverture du site Jira...")

    # Retrieve credentials from environment variables
    username_jira = os.getenv("JIRA_USERNAME")
    password_jira = os.getenv("JIRA_PASSWORD")

    if not username_jira or not password_jira:
        print(Fore.RED + "Erreur: Les variables d'environnement JIRA_USERNAME et JIRA_PASSWORD ne sont pas définies.")
        print(Style.RESET_ALL)
        pytest.fail("Les identifiants Jira ne sont pas configurés.")
    try:
        username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#username")))
        print(Style.BRIGHT + f"La page '{driver.title}' est chargée. Connexion en cours...")
        username_field.clear()
        username_field.send_keys(username_jira)  # Use the retrieved username

        continue_button = driver.find_element(By.CSS_SELECTOR, "button#login-submit")
        continue_button.click()

        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#password")))
        print(Style.BRIGHT + "Nom d'utilisateur vérifié.")
        password_field.clear()
        password_field.send_keys(password_jira)  # Use the retrieved password

        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-submit")))
        login_button.click()
        time.sleep(5)  # Give some time for the page to load after login

        expected_substring_en = "Log in with Atlassian account"
        expected_substring_fr = "Se connecter avec le compte Atlassian"
        actual_title = driver.title

        if expected_substring_fr in actual_title or expected_substring_en in actual_title:
            print(Back.BLUE + "Des vérifications sont nécessaires avant de se connecter (MFA ou autre).")
            print(Style.RESET_ALL)

            # If verification = MFA promotion, dismiss it
            if driver.find_elements(By.CSS_SELECTOR, "button#mfa-promote-dismiss"):
                driver.find_element(By.CSS_SELECTOR, "button#mfa-promote-dismiss").click()
            else:
                print(Style.BRIGHT + f"La page actuelle contient '{expected_substring_en}' ou '{expected_substring_fr}'.")
                print(Style.RESET_ALL)
                # In case Atlassian does not remember you, and requires a code sent to your email...
                code = input("Veuillez entrer le code de vérification envoyé à votre e-mail: ")
                verification_code_field = driver.find_element(By.CSS_SELECTOR, ".css-1ndkufm .css-1pgxbvo")
                verification_code_field.send_keys(code)
                wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#WhiteboxContainer")))
                time.sleep(5)
            assert driver.title == "Your work - Jira", f"Échec de la connexion: Titre de page inattendu: '{driver.title}'"
            print(Fore.GREEN + "Connexion réussie: Titre de page attendu 'Your work - Jira'.")

        else:
            print(
                Fore.GREEN + f"Connexion réussie: '{actual_title}'")
            print(Style.RESET_ALL)
            assert driver.title == "Your work - Jira", f"Échec de la connexion: Titre de la page inattendu: '{driver.title}'"

    except TimeoutException:
        print(Fore.RED + "Erreur de délai d'attente: Un élément crucial n'a pas été trouvé à temps.")
        print(Style.RESET_ALL)
        pytest.fail("Test de connexion échoué en raison d'un délai d'attente.")
    except NoSuchElementException:
        print(Fore.RED + "Erreur d'élément non trouvé: Un élément requis pour la connexion n'a pas été localisé.")
        print(Style.RESET_ALL)
        pytest.fail("Test de connexion échoué en raison d'un élément manquant.")
    except Exception as e:
        print(Fore.CYAN + f"Votre test de connexion a échoué: {e}")
        print(Style.RESET_ALL)
        pytest.fail(f"Test de connexion échoué en raison d'une erreur inattendue: {e}")

    yield  # This yields control back to the test class
    driver.quit()


# def login(request): # "request" is a pytest fixture that provides access to this object. We use it to store the driver that the test class will need
#     driver = webdriver.Edge()
#     wait = WebDriverWait(driver, 10)
#     driver.get("https://justingoufo.atlassian.net/jira/your-work")
#     request.cls.driver = driver # "cls" is a pytest fixture that stands for "class". It provides access to the driver object for the test class
#     request.cls.wait = wait
#     try:
#         username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#username")))
#         username.clear()
#         username.send_keys("marketing.jobhunter@gmx.com")
#         continue_button = driver.find_element(By.CSS_SELECTOR, "button#login-submit")
#         continue_button.click()
#
#         password = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input#password")))
#         password.clear()
#         password.send_keys("Atlassian{120}")
#
#         login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#login-submit")))
#         login_button.click()
#         time.sleep(5)
#         # Verify if the expected substring is present in the actual title
#         # The string you want to check for in the title
#         expected_substring = "Log in"
#         # Get the actual page title
#         actual_title = driver.title
#         # Verify if the expected substring is present in the actual title
#         if expected_substring in actual_title:
#             print(f"Page title '{actual_title}' contains '{expected_substring}'")
#             code = input("Enter verification code: ")
#             verification_code_field = driver.find_element(By.CSS_SELECTOR, ".css-1ndkufm .css-1pgxbvo")
#             verification_code_field.send_keys(code)
#             wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div#WhiteboxContainer")))
#             time.sleep(5)
#             assert driver.title == "Your work - Jira"
#         else:
#             print(f"Test passed: Page title '{actual_title}' does not contain '{expected_substring}'")
#             assert driver.title == "Your work - Jira"
#     except Exception as e:
#         print(f"Your Login Test failed: {e}")
#         assert False
#
#     yield ## the followings run after each test class execution
#     driver.quit()