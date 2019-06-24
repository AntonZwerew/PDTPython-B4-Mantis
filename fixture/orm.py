from pony.orm import *
# from datetime import datetime
from model.group import Group
from model.contact import Contact
from pymysql.converters import decoders


class ORMFixture:
    db = Database()

    class Group(db.Entity):
        _table_ = "group_list"
        id = PrimaryKey(int, column="group_id")
        name = Optional(str, column="group_name")
        header = Optional(str, column="group_header")
        footer = Optional(str, column="group_footer")
        contacts = Set(lambda: ORMFixture.Contact, table="address_in_groups", column="id", reverse="groups", lazy=True)

    class Contact(db.Entity):
        _table_ = "addressbook"
        id = PrimaryKey(int, column="id")
        firstname = Optional(str, column="firstname")
        lastname = Optional(str, column="lastname")
        # deprecated = Optional(datetime, column="deprecated")
        deprecated = Optional(str, column="deprecated")
        # Оставил deprecated строкой, т.к. почему-то python не может перевести строку в datetime, в том числе описанным
        # в уроке способом. Как я понял из Инфтернета - может быть своязано с локалью (у меня по умолчанию датавремя
        # Пт июн 21 19:42:06 MSK 2019. Вручную приветсти строку deprecated в время так же не сумел.
        groups = Set(lambda: ORMFixture.Group, table="address_in_groups", column="group_id", reverse="contacts", lazy=True)

    def __init__(self, host, name, user, password):
        self.db.bind("mysql", host=host, database=name, user=user, password=password# , conv=decoders)
                     )
        self.db.generate_mapping()
        # sql_debug(True)

    def destroy(self):
        pass

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(group_id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(contact_id=str(contact.id), first_name=contact.firstname, last_name=contact.lastname)
        return list(map(convert, contacts))

    @db_session
    def get_group_list(self):
        return self.convert_groups_to_model(select(g for g in ORMFixture.Group))

    @db_session
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.Contact
                                                     if c.deprecated == "0000-00-00 00:00:00"))
                                                     # if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.Group if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)

    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.Group if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.Contact if c.deprecated is None and orm_group not in c.groups)
        )

    def get_contacts_id_in_group(self, group):
        def get_id(contact):
            return int(contact.id)
        contacts = self.get_contacts_in_group(group)
        ids = []
        for contact in contacts:
            ids.append(get_id(contact))
        return ids



