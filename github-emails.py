import requests
import sys

GITHUB_TOKEN = 'GITHUB_TOKEN'
GITHUB_API_URL = 'https://api.github.com'

def get_repos(username, include_forks=True):
    url = f'{GITHUB_API_URL}/users/{username}/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    repos = response.json()
    if not include_forks:
        repos = [repo for repo in repos if not repo['fork']]

    return repos

def get_commits(repo_full_name):
    url = f'{GITHUB_API_URL}/repos/{repo_full_name}/commits'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def extract_emails_from_commits(commits, repo_full_name, verbose=False):
    email_details = {}
    for commit in commits:
        commit_author = commit.get('commit', {}).get('author', {})
        email = commit_author.get('email')
        if email and not email.endswith('@users.noreply.github.com'):
            commit_sha = commit.get('sha')
            if email not in email_details:
                email_details[email] = []
            email_details[email].append({
                'repo': repo_full_name,
                'sha': commit_sha
            })

    if verbose:
        for email, details in email_details.items():
            print(f'Email: {email}')
            for detail in details:
                print(f'  Repo: {detail["repo"]}')
                print(f'  Commit SHA: {detail["sha"]}')
            print()

    return email_details

def main(username, include_forks=True, verbose=False):
    repos = get_repos(username, include_forks)
    all_emails = {}

    for repo in repos:
        repo_full_name = repo['full_name']
        commits = get_commits(repo_full_name)
        email_details = extract_emails_from_commits(commits, repo_full_name, verbose)
        for email, details in email_details.items():
            if email not in all_emails:
                all_emails[email] = []
            all_emails[email].extend(details)

    if not verbose:
        for email in all_emails:
            print(email)

if __name__ == '__main__':
    try:
        github_username = sys.argv[1]
        if GITHUB_TOKEN == 'GITHUB_TOKEN':
               raise ValueError("Change the variable on line 4 with the value of your own github token! Check https://github.com/settings/tokens")
        include_forks = '--no-forks' not in sys.argv[2:]
        verbose = '-v' in sys.argv[2:]
        main(github_username, include_forks, verbose)
    except IndexError:
        print("Usage: python3 github-emails.py username [--no-forks] [-v]")
    except ValueError as message:
        print(message)
