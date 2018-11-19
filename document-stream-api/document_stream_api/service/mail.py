from typing import List, Optional, Union, Dict, Any, Type
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from contextlib import contextmanager

from ..environment import Environment
from ..api.account import Account
from ..service import printer


environment = Environment.get()
database = environment.register.get('database')
account_service = Account(database)


class Attachment:
    _subclasses = set()

    def __init_subclass__(cls):
        cls.add_subclass(cls)

    def __init__(self, type):
        self._type = type

    def read(self):
        raise NotImplementedError

    @property
    def name(self):
        raise NotImplementedError

    @classmethod
    def add_subclass(cls, subcls):
        cls._subclasses.add(cls)

    @classmethod
    def _search_type(cls, name):
        return next((subcls for subcls in cls._subclasses if subcls.type == name), None)

    @classmethod
    def parse(cls, attachments: List[Dict[str, Any]]):
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
              >>> concrete_attachment = ConcreteAttachment(**attachment.get('arguments', {})
        """

        concrete_attachments = []

        for attachment in attachments:
            attachment_cls_name = attachment.get('type', None)
            arguments = attachment.get('arguments', {})

            attachment_cls = cls._search_type(attachment_cls_name)

            if attachment_cls is not None:
                concrete_attachments.append(attachment_cls(**arguments))
            else:
                raise NotImplementedError(f'Unknown attachment type `{attachment_cls_name}`')

        return concrete_attachments


class AttachmentReport(Attachment):
    type = 'report'

    def __init__(self, id, entity, format='pdf'):
        self._id = id
        self._entity = entity
        self._format = format

    @property
    def name(self) -> str:
        return f'{self._entity}.{self._format}'

    def read(self) -> bytes:
        account = account_service.selectone_filled(self._id)

        if self._entity == 'account':
            return printer.account_as_pdf(account)
        elif self._entity == 'act':
            return printer.act_as_pdf(account)
        elif self._entity == 'invoice':
            return printer.invoice_as_pdf(account)
        else:
            raise NotImplementedError(f'Have no implementation for `{self._entity}`')


class Sender:
    def __init__(self, host, port, user, password, ssl):
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

    def send(self, *, from_address: str, to_addresses: List[str],
             subject: str, body: str,
             attachments: Optional[List[Attachment]] = None):

        if not to_addresses:
            raise ValueError('`to_addresses` must be not empty')

        if not from_address:
            raise ValueError('`from_address` must be not empty')

        message = MIMEMultipart()

        message['From'] = from_address
        message['To'] = COMMASPACE.join(to_addresses)
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

    def quit(self):
        self._server.quit()

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.quit()

        if exception_value is not None:
            raise exception_value
