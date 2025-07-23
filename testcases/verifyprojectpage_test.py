import pytest
from pages.projects_page import Projectpage
from pages.issues_page import Issuepage


@pytest.mark.usefixtures("login")
class TestProjectPage:

    def test_projectdisplay(self):
        projectpage = Projectpage(self.driver)
        projectpage.viewproject("Test Automation Training")


