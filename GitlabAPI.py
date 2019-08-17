import requests
from Exceptions import ProjectNotFoundException, RepositoryNotFoundException, UserNotFoundException
from caching import Cacher

base_url = "https://gitlab.com/api/v4"
params = {'private_token': '8TQ5FAb5hEa_hxUpeVq-'}
cacher = Cacher()


#  Fetch json from api supplying header using base url.
def json_fetch(url, header):
    def func(path):
        try:
            return requests.get(url + path, header).json()
        except Exception as error:
            raise error
    return func


fetch = json_fetch(base_url, params)


# Try searching user_id in cache, if not found fetch from Gitlab API.
def get_user_id(user):
    try:
        cached_user_id = cacher.get_user_id_for_name(user)
        if cached_user_id:
            return cached_user_id
        else:
            user_data = fetch(f'/users?username={user}')
            if not len(user_data):
                raise UserNotFoundException('Username not found in Gitlab API!')
            cacher.insert_user(user_data[0]['username'], user_data[0]['id'])
            return user_data[0]['id']
    except Exception:
        raise UserNotFoundException


# Try searching project_id in cache, if not found fetch from Gitlab API.
def get_project_id(user_id, project_name):
    try:
        cached_project_id = cacher.get_project_id_for_name(project_name)
        if cached_project_id:
            return cached_project_id
        else:
            projects = fetch(f'/users/{user_id}/projects')
            if not len(projects):
                raise ProjectNotFoundException(f'No projects for user {user_id} found in Gitlab API!')
            project = next(filter(lambda x: x['name'] == project_name, projects))
            cacher.insert_project(project['name'], project['id'])
            return project['id']
    except Exception:
        raise ProjectNotFoundException


# TODO maybe rewrite using clean code, single return...
# Fetch repository_id of repository belonging to project.
# First looks in cache, if not exists fetch from Gitlab API.
# Assuming single repository for project.
def get_repository_id(project_id):
    try:
        cached_repository = cacher.get_repository_id_for_project(project_id)
        if cached_repository:
            return cached_repository
        else:
            repository = fetch(f'/projects/{project_id}/registry/repositories')[0]
            if not repository.get('id'):
                raise RepositoryNotFoundException(f'No repository for project {project_id} found!')
            cacher.insert_repository(project_id, repository['id'])
            return repository['id']
    except Exception:
        raise RepositoryNotFoundException


def get_image_info(user, project, tag):
    try:
        cached_project = cacher.get_project_and_repository_id(project)
        if cached_project:
            return fetch(f'/projects/{cached_project[0]}/registry/repositories/{cached_project[1]}/tags/{tag}')
        user_id = get_user_id(user)
        project_id = get_project_id(user_id, project)
        repository_id = get_repository_id(project_id)
        image_info = fetch(f'/projects/{project_id}/registry/repositories/{repository_id}/tags/{tag}')
        return image_info
    except Exception as error:
        raise error


if __name__ == "__main__":
    # TODO manner to pass API key to get_image_info into json_fetch closure
    # get_user_id('roytouw')
    # get_project_id('4390202', 'shopr-client')
    # print(get_repository_id('13776728'))
    print(get_image_info('roytouw', 'shopr-client', 'staging'))
