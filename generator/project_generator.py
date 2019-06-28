from model.mantis_project import MantisProject
from generator import generator
import random


def random_project():
    project = MantisProject(name=random_proj_name(),
                            status=random_proj_status(),
                            global_categories=random_proj_global_categories(),
                            view_status=random_proj_view_status(),
                            description=random_proj_description())
    return project


def random_proj_name():
    return generator.random_string(prefix="name", maxlen=10)


def random_proj_status():
    return random.choice(list(MantisProject.valid_project_statuses.values()))


def random_proj_global_categories():
    return random.choice([True, False])


def random_proj_view_status():
    return random.choice(list(MantisProject.valid_project_views.values()))


def random_proj_description():
    return generator.random_string(prefix="description", maxlen=10)
