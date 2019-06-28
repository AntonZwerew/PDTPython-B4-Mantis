from pony.orm import *
from model.mantis_project import MantisProject
import random


class ORMHelper:
    db = Database()

    class MantisProject(db.Entity):
        _table_ = "mantis_project_table"
        id = PrimaryKey(int, column="id")
        name = Optional(str, column="name")
        status = Optional(str, column="status")
        view_state = Optional(str, column="view_state")
        access_min = Optional(str, column="access_min")
        file_path = Optional(str, column="file_path")
        description = Optional(str, column="description")
        category_id = Optional(str, column="category_id")
        inherit_global = Optional(str, column="inherit_global")  # str не преобразует, из таблицы получается int

    def __init__(self, host, name, user, password):
        self.db.bind("mysql", host=host, database=name, user=user, password=password
                     )
        self.db.generate_mapping()
        # sql_debug(True)

    @db_session
    def get_all_projects(self):
        return self.convert_projects_to_model(select(p for p in ORMHelper.MantisProject))

    def get_random_project(self):
        return random.choice(self.get_all_projects())

    def convert_projects_to_model(self, projects):
        def convert(project):
            return MantisProject(project_id=project.id,
                                 name=project.name,
                                 status=MantisProject.valid_project_statuses.get(project.status),
                                 global_categories=(lambda x: x == 1)(project.inherit_global),
                                 view_status=MantisProject.valid_project_views.get(project.view_state),

                                 description=project.description)
        return list(map(convert, projects))

    def destroy(self):
        pass


