# Git-Emails
This tool is simply searching for "leaked" email addresses in every commit of every repository of a given github user.

## Install
```bash
git clone https://github.com/jhond0e/git-emails
cd git-emails
pip3 install -r requirements.txt
```
Generate a github token at https://github.com/settings/tokens and write it on the 4th line of github-emails.py
```python
- GITHUB_TOKEN = 'GITHUB-TOKEN'
+ GITHUB_TOKEN = 'github_pat_*********'
```

## Usage
```
Usage: python3 github-emails.py username [options]

Positional arguments:
  username          GitHub username to retrieve emails from commits

Optional arguments:
  -h                Show this help message and exit
  --no-forks        Exclude forked repositories from the search
  -v                Enable verbose mode (show repository and commit SHA for each email)
  -o output_file    Output the results to the specified file
```

## Examples
```
python3 github-emails.py username                  # Basic usage, output emails to the console
python3 github-emails.py username --no-forks       # Exclude forks from search
python3 github-emails.py username -v               # Verbose output with commit details (repo and commit SHA)
python3 github-emails.py username -o output.txt    # Save emails to output.txt
python3 github-emails.py username -v -o output.txt # Verbose output saved to file
```

### Tip :
You can view the email associated with a commit in the raw data by appending '.patch' to the end of the GitHub commit URL in your browser.
![image](https://github.com/user-attachments/assets/477d9e8d-454a-40cb-bf8b-e259e9c1c2fb)
