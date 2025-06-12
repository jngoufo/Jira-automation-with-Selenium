import pytest
from pages.issues_page import Issuepage


@pytest.mark.usefixtures("login")
class TestIssuePage:

    def test_issuesdisplay(self):
        issuepage = Issuepage(self.driver)
        issuepage.viewissue('CS\n-\n1')