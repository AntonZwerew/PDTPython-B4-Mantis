# -*- coding: utf-8 -*-

from sys import maxsize


class Contact():
    def __init__(self, first_name=None, middle_name=None, last_name=None, nickname=None, photo=None, title=None,
                 company=None, address1=None, phone_home=None, phone_mobile=None, phone_work=None, phone_fax=None,
                 email1=None, email2=None, email3=None, homepage=None, bday_day=None, bday_month=None, bday_year=None,
                 aday_day=None, aday_month=None, aday_year=None, group=None, address2=None, phone2=None, notes=None,
                 contact_id=None, all_phones_from_homepage=None, all_emails_from_homepage=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.nickname = nickname
        self.photo = photo
        self.title = title
        self.company = company
        self.address1 = address1
        self.phone_home = phone_home
        self.phone_mobile = phone_mobile
        self.phone_work = phone_work
        self.phone_fax = phone_fax
        self.email1 = email1
        self.email2 = email2
        self.email3 = email3
        self.homepage = homepage
        self.bday_day = bday_day
        self.bday_month = bday_month
        self.bday_year = bday_year
        self.aday_day = aday_day
        self.aday_month = aday_month
        self.aday_year = aday_year
        self.group = group
        self.address2 = address2
        self.phone2 = phone2
        self.notes = notes
        self.id = contact_id
        self.all_phones_from_homepage = all_phones_from_homepage
        self.all_emails_from_homepage = all_emails_from_homepage

    def __repr__(self):
        return "%s:%s:%s:%s" % (self.id, self.first_name, self.last_name, self.address1)

    def __eq__(self, other):
        eq = (self.id == other.id or self.id is None or other.id is None) and (
              self.first_name == other.first_name) and (
              self.last_name == other.last_name)
        return eq

    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
