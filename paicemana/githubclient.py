from github3 import GitHub  # TODO in setup.py (package github3.py)


class RepositoryClient(object):
    """Class to read and write on GitHub repository"""

    def __init__(self, repo_user = 'OSMBrasil', repo_name = 'semanario'):
        """
        @params
        repo_user - name of organization or user
        repo_name - repository name
        """
        github = GitHub()
        self.repo = github.repository(repo_user, repo_name)

    def milestones_info(self):
        """Prints information for identification of milestones"""
        s = ''
        for milestone in self.repo.milestones():
            s += 'The milestone "%s" has number=%s\n'\
                % (milestone.title, milestone.number)
        return s[:-1]


if __name__ == "__main__":
    print(RepositoryClient().milestones_info())

