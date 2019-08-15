from tinydb import TinyDB, Query


class Cacher:
    def __init__(self):
        self.db = TinyDB('cache.json')

    def insert_image(self, path, revision):
        self.db.insert({'path': path, 'revision': revision})

    def update_image(self, path, revision):
        image = Query()
        self.db.update({"revision": revision}, image.path == path)

    def search_image(self, path):
        image = Query()
        result = self.db.search(image.path == path)
        return result

    def update_or_insert_image(self, path, revision):
        result = self.search_image(path)
        if len(result):
            self.update_image(path, revision)
        else:
            self.insert_image(path, revision)

    def get_user_id_for_name(self, user_name):
        user = Query()
        result = self.db.search(user.name == user_name)
        if len(result):
            return result[0]['user_id']
        return False

    def insert_user(self, name, user_id):
        self.db.insert({"name": name, "user_id": user_id})

    def get_project_id_for_name(self, project_name):
        project = Query()
        result = self.db.search(project.name == project_name)
        if len(result):
            return result[0]['project_id']
        return False

    def insert_project(self, project_name, project_id):
        self.db.insert({"name": project_name, "project_id": project_id})

    def get_repository_id_for_project(self, project_id):
        project = Query()
        result = self.db.search(project.project_id == int(project_id))
        if len(result):
            if result[0].get('repository_id'):
                return result[0]['repository_id']
        return False

    def get_project_and_repository_id(self, project_name):
        project = Query()
        result = self.db.search(project.name == project_name)
        if len(result):
            if result[0].get('repository_id'):
                return result[0]['project_id'], result[0]['repository_id']
        return False

    def insert_repository(self, project_id, repository_id):
        project = Query()
        self.db.update({"repository_id": repository_id}, project.project_id == int(project_id))


if __name__ == '__main__':
    cacher = Cacher()
    if len(cacher.get_user_id_for_name('roytouwa')):
        print('a')
