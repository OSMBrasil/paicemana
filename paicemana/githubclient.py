from github3 import GitHub

repo_user = 'OSMBrasil'
repo_name = 'semanario'

github = GitHub()

repo = github.repository(repo_user, repo_name)
s = ''
for milestone in repo.milestones():
    s += 'The milestone "%s" has number=%s\n'\
        % (milestone.title, milestone.number)
s = s[:-1]

print(s)
