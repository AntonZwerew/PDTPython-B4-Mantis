import mysql.connector
from model.group import Group
from model.contact import Contact


class DbFixture:
    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password,
                                                  autocommit=True, buffered=True)
        # без buffered запрос всех данных контакта выдает Unread Result

    def destroy(self):
        self.connection.close()

    def get_group_list(self):
        group_list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute("select group_id, group_name, group_header, group_footer from group_list")
            for row in cursor:
                (id, name, header, footer) = row
                group_list.append(Group(group_id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return group_list

    def get_contact_list(self):
        contact_list = []
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                '''select id, firstname, middlename, lastname, nickname, company, title, address, home, mobile, work,
                fax, email, email2, email3, homepage, bday, bmonth, byear, aday, amonth, ayear, address2, phone2, notes 
                from addressbook where deprecated = '0000-00-00 00:00:00\'''')
            for row in cursor:
                (contact_id, firstname, middlename, lastname, nickname, company, title, address, home, mobile, work,
                fax, email, email2, email3, homepage, bday, bmonth, byear, aday, amonth, ayear, address2, phone2, notes
                 ) = row
                contact_list.append(Contact(contact_id=str(contact_id), first_name=firstname, middle_name=middlename,
                                            last_name=lastname, nickname=nickname, company=company, title=title,
                                            address1=address, phone_home=home, phone_mobile=mobile, phone_work=work,
                                            phone_fax=fax, email1=email, email2=email2, email3=email3,
                                            homepage=homepage, bday_day=bday, bday_month=bmonth, bday_year=byear,
                                            aday_day=aday, aday_month=amonth, aday_year=ayear, address2=address2,
                                            phone2=phone2,notes=notes
                                            ))
        finally:
            cursor.close()
        return contact_list

    def count_groups(self):
        return len(self.get_group_list())

    def count_contacts(self):
        return len(self.get_contact_list())
