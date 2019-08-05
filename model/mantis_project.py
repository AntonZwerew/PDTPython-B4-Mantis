from sys import maxsize


class MantisProject:

    valid_project_statuses = {10: "development",
                              30: "release",
                              50: "stable",
                              70: "obsolete"}
    valid_project_views = {10: "public",
                           50: "private"}

    def __init__(self, name, status, view_status, description, global_categories=None, project_id=None):

        self.id = project_id
        self.name = name

        if status in self.valid_project_statuses.values():
            self.status = status
        else:
            raise AttributeError("Incorrect project status")

        if type(global_categories) == bool or global_categories is None:
            self.global_categories = global_categories
        else:
            raise AttributeError("Incorrect Inherit Global Categories flag")

        if view_status in self.valid_project_views.values():
            self.view_status = view_status
        else:
            raise AttributeError("Incorrect project view")

        self.description = description

    def __repr__(self):
        return "%s %s %s %s" % (self.name, self.status, self.view_status, self.description)

    def __eq__(self, other):
        eq = (self.name == other.name and
              self.status == other.status and
              # Через SOAP нельзя получить данный флаг
              # self.global_categories == other.global_categories and
              self.view_status == other.view_status and
              self.description == other.description)
        return eq


def id_or_max(project):
    if project.id:
        return project.id
    else:
        return maxsize
