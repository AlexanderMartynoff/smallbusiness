import weasyprint
from os.path import join
from .. environment import RESOURCE_DIR


def account_as_pdf(account):
    return weasyprint.HTML(join(RESOURCE_DIR, 'template/account/html/index.html')).write_pdf()
