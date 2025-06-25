import os
import requests
import pandas as pd
from datetime import datetime, timedelta

# Get environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO = os.getenv('REPO')

# Check for missing environment variables
if not GITHUB_TOKEN or not REPO:
    raise ValueError("Missing GITHUB_TOKEN or REPO environment variable.")

# Calculate the date one month ago
one_month_ago = datetime.now() - timedelta(days=30)
one_month_ago_str = one_month_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

# GitHub API URL for issues
url = f"https://api.github.com/repos/{REPO}/issues"

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Parameters to fetch issues from the past month
params = {
    'since': one_month_ago_str,
    'state': 'all'
}

# Make the API request
response = requests.get(url, headers=headers, params=params)
response.raise_for_status()
issues = response.json()

# Prepare data for CSV
data = []
for issue in issues:
    data.append({
        'Title': issue['title'],
        'Number': issue['number'],
        'State': issue['state'],
        'Created At': issue['created_at'],
        'Closed At': issue.get('closed_at', 'N/A'),
        'Assignee': issue['assignee']['login'] if issue['assignee'] else 'Unassigned'
    })

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('monthly_issues_report.csv', index=False)

print("Monthly issues report has been generated and saved to 'monthly_issues_report.csv'.")
