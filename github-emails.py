import requests
import sys

GITHUB_TOKEN = 'GITHUB-TOKEN'
GITHUB_API_URL = 'https://api.github.com'

def get_repos(username):
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_commits(repo_full_name):
    url = f'{GITHUB_API_URL}/repos/{repo_full_name}/commits'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_emails_from_commits(commits):
    emails = set()
    for commit in commits:
        commit_author = commit.get('commit', {}).get('author', {})
        email = commit_author.get('email')
        if email:
            emails.add(email)
    return emails

def main(username):
    repos = get_repos(username)
    all_emails = set()

    for repo in repos:
        repo_full_name = repo['full_name']
        commits = get_commits(repo_full_name)
        emails = extract_emails_from_commits(commits)
        all_emails.update(emails)

    for email in all_emails:
        print(email)

if __name__ == '__main__':
    try:
      github_username = sys.argv[1]
      main(github_username)
    except:
        print("Usage : python3 github-emails.py username")
