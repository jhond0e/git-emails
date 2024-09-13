import requests
import sys

GITHUB_TOKEN = 'GITHUB-TOKEN'
GITHUB_API_URL = 'https://api.github.com'

def check_github_token():
    if GITHUB_TOKEN == 'GITHUB-TOKEN':
        print("Error: You must replace 'GITHUB-TOKEN' with your actual GitHub token.")
        sys.exit(1)

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
                'sha': commit_sha,
            })
    
    if verbose:
        for email, details in email_details.items():
            print(f'Email: {email}')
            for detail in details:
                print(f'  Repo: {detail["repo"]}')
                print(f'  Commit SHA: {detail["sha"]}')
            print()
    
    return email_details

def write_output_to_file(filename, all_emails, verbose=False):
    with open(filename, 'w') as f:
        for email, details in all_emails.items():
            if verbose:
                f.write(f'Email: {email}\n')
                for detail in details:
                    f.write(f'  Repo: {detail["repo"]}\n')
                    f.write(f'  Commit SHA: {detail["sha"]}\n')
                f.write('\n')
            else:
                f.write(f'{email}\n')

def show_help():
    print("""
Usage: python3 github-emails.py username [options]

Positional arguments:
  username          GitHub username to retrieve emails from commits

Optional arguments:
  -h                Show this help message and exit
  --no-forks        Exclude forked repositories from the search
  -v                Enable verbose mode (show repository and commit SHA for each email)
  -o output_file    Output the results to the specified file

Examples:
  python3 github-emails.py username               # Basic usage, output emails to the console
  python3 github-emails.py username --no-forks    # Exclude forks from search
  python3 github-emails.py username -v            # Verbose output with commit details (repo and commit SHA)
  python3 github-emails.py username -o output.txt # Save emails to output.txt
  python3 github-emails.py username -v -o output.txt # Verbose output saved to file
""")

def main(username, include_forks=True, verbose=False, output_file=None):
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

    if output_file:
        write_output_to_file(output_file, all_emails, verbose)

    if not verbose and not output_file:
        for email in all_emails:
            print(email)

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        show_help()
    else:
        check_github_token()

        try:
            github_username = sys.argv[1]
            include_forks = '--no-forks' not in sys.argv[2:]
            verbose = '-v' in sys.argv[2:]
            output_file = None

            if '-o' in sys.argv:
                output_index = sys.argv.index('-o') + 1
                output_file = sys.argv[output_index] if output_index < len(sys.argv) else None

            if output_file is None and '-o' in sys.argv:
                raise IndexError("You must provide a filename after the -o option.")

            main(github_username, include_forks, verbose, output_file)
        except IndexError:
            show_help()
        except Exception as e:
            print(f"Error: {e}")
            show_help()
