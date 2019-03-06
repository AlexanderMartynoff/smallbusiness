from typing import List, Optional, Union, Dict, Any, Type, Set, Callable, TypeVar
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate  # type: ignore
from contextlib import contextmanager

from ..resource import FRAMEWORK_RESOURCE_DIR
from ..logger import getlogger
from .api import API
from . import printer


logger = getlogger(__name__)


class Attachment:
    subclasses: Set[Type['Attachment']] = set()
    type: Optional[str] = None

    def __init__(self, *args, **kwargs):
        raise Exception('Must be override in subclass')

    def __init_subclass__(cls):
        cls.add_subclass(cls)

    def read(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @classmethod
    def add_subclass(cls, subcls):
        cls.subclasses.add(cls)


class AttachmentReport(Attachment):
    type = 'report'

    def __init__(self, id, entity, api, i18n, format='pdf'):
        self._id = id
        self._entity = entity
        self._format = format
        self._api = api
        self._i18n = i18n

    @property
    def name(self) -> str:
        return f'{self._entity}.{self._format}'

    def read(self) -> bytes:
        account = self._api.account.selectone_filled(self._id)

        if self._entity == 'account':
            return printer.account_as_pdf(account, self._i18n)
        elif self._entity == 'act':
            return printer.act_as_pdf(account, self._i18n)
        elif self._entity == 'invoice':
            return printer.invoice_as_pdf(account, self._i18n)
        else:
            raise NotImplementedError(f'Have no implementation for `{self._entity}`')


class Sender:
    _server: smtplib.SMTP

    def __init__(self, host: str, port: int, user: str, password: str, ssl: bool):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._ssl = ssl

        if self._ssl:
            self._server = smtplib.SMTP_SSL(self._host, port)
        else:
            self._server = smtplib.SMTP(self._host, port)

    def login(self):
        self._server.login(self._user, self._password)

    def send(self, from_address: str,
             to_addresses: List[str],
             subject: Optional[str],
             body: Optional[str],
             attachments: Optional[List[Attachment]] = None):

        if not to_addresses:
            raise ValueError('`to_addresses` must be not empty')

        if not from_address:
            raise ValueError('`from_address` must be not empty')

        to_addresses = _flatten_address_list(to_addresses)
        to_address = COMMASPACE.join(to_addresses)

        message = MIMEMultipart()

        message['From'] = from_address
        message['To'] = to_address
        message['Date'] = formatdate(localtime=True)

        if subject:
            message['Subject'] = subject

        if body:
            message.attach(MIMEText(body))

        for attachment in attachments or []:
            application = MIMEApplication(attachment.read())

            application['Name'] = attachment.name
            application['Content-Disposition'] = f'attachment; filename="{attachment.name}"'

            message.attach(application)

        self._server.sendmail(from_address, to_addresses, message.as_string())

        logger.info('Success send mail from ``%s`` to ``%s``', from_address, to_address)

    def quit(self):
        self._server.quit()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, etype, evalue, etraceback):
        self.quit()

        if evalue is not None:
            raise evalue


def parse_attachment(attachments: List[Dict[str, Any]], api: API, i18n) -> List[Attachment]:
    """ Parse attachments protocol data.

        >>> attachments
        >>> [
        >>>   {
        >>>     type: 'type_name',
        >>>     arguments: {}
        >>>   }
        >>> ]

        Each attachment record (aka dict) have next properties:
        - type (str) - name that was used for defining concrete attachment implementation
        - arguments (dict) - dict that will passed to __init__ method of concrete implementation
          >>> concrete_attachment = Attachment(**attachment.get('arguments', {})
    """

    concrete_attachments = []

    for attachment in attachments:
        attachment_cls_name = attachment.get('type', None)
        arguments = attachment.get('arguments', {})

        arguments.update({
            'i18n': i18n,
            'api': api
        })

        attachment_cls = _search_attachment_type(attachment_cls_name)

        if attachment_cls is not None:
            concrete_attachments.append(attachment_cls(**arguments))
        else:
            raise NotImplementedError(f'Unknown attachment type `{attachment_cls_name}`')

    return concrete_attachments


def _search_attachment_type(type_name: str) -> Optional[Type[Attachment]]:
    return next((subcls for subcls in Attachment.subclasses if subcls.type == type_name), None)


def _flatten_address_list(address_list: List[str]) -> List[str]:
    flatten_address_list: List[str] = []

    for address in address_list:
        if address:
            flatten_address_list += [_.strip() for _ in address.split(',')]

    return flatten_address_list
