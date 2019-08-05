from model.mantis_project import MantisProject
from suds.client import Client
from suds import WebFault


class SoapHelper:
    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_all_projects(self, username, password):
        # На самом деле возвращает не все проекты.
        # В выдачу не попадут проекты, у которых в базе данных enabled = 0, но они не удалены
        # Каких - либо методов, позволяющих получать проекты по айди или как-либо еще не обнаружил
        projects = []
        try:
            client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
            soap_projects = client.service.mc_projects_get_user_accessible(username, password)
        except WebFault:
            return None
        for project in soap_projects:
            converted_project = MantisProject(project_id=int(project.id),
                                              name=str(project.name),
                                              status=str(project.status.name),
                                              view_status=str(project.view_state.name),
                                              description=str(project.description))
            projects.append(converted_project)
        return projects
