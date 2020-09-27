class DroneParse(object):
    """
            data = {
            'build': {'id': 36, 'repo_id': 2, 'trigger': 'ismewen', 'number': 36, 'status': 'pending', 'event': 'push',
                      'action': '', 'link': 'https://github.com/ismewen/edrone/compare/4c6512ca4ebb...ba52a49c188f',
                      'timestamp': 0, 'message': 'sha tag', 'before': '4c6512ca4ebbd9f9e897b15024c15561cd9b5152',
                      'after': 'ba52a49c188f208885119ca6791fddfef802e49e', 'ref': 'refs/heads/master',
                      'source_repo': '',
                      'source': 'master', 'target': 'master', 'author_login': '', 'author_name': 'ismewen',
                      'author_email': 'ismewen@MacBook-Air.local',
                      'author_avatar': 'https://avatars0.githubusercontent.com/u/30500262?v=4', 'sender': 'ismewen',
                      'started': 0, 'finished': 0, 'created': 1601197804, 'updated': 1601197804, 'version': 1},
            'repo': {'id': 2, 'uid': '293063525', 'user_id': 1, 'namespace': 'ismewen', 'name': 'edrone',
                     'slug': 'ismewen/edrone', 'scm': '', 'git_http_url': 'https://github.com/ismewen/edrone.git',
                     'git_ssh_url': 'git@github.com:ismewen/edrone.git', 'link': 'https://github.com/ismewen/edrone',
                     'default_branch': 'master', 'private': False, 'visibility': 'public', 'active': True,
                     'config_path': '.drone.yml', 'trusted': True, 'protected': False, 'ignore_forks': False,
                     'ignore_pull_requests': False, 'timeout': 60, 'counter': 0, 'synced': 0, 'created': 0,
                     'updated': 0,
                     'version': 0}}
    """

    def __init__(self, drone_push_params):
        self.drone_push_params = drone_push_params

    def repo_name(self):
