"""
GitHub Repository Analytics Tool
Tracks and analyzes GitHub repository metrics including:
- Commits
- Pull Requests
- Issues
- Contributors
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json

class GitHubAnalytics:
    """Analyze GitHub repository metrics"""
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_repo_stats(self) -> Dict[str, Any]:
        """Get basic repository statistics"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data["name"],
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "watchers": data["watchers_count"],
                "open_issues": data["open_issues_count"],
                "language": data["language"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"]
            }
        return {}
    
    def get_commits(self, days: int = 30) -> List[Dict]:
        """Get commit statistics for the last N days"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/commits"
        params = {"since": since, "per_page": 100}
        
        commits = []
        page = 1
        while page <= 10:  # Limit to 1000 commits
            params["page"] = page
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break
                commits.extend(data)
                page += 1
            else:
                break
        
        return commits
    
    def get_pull_requests(self, state: str = "closed", days: int = 30) -> List[Dict]:
        """Get pull request metrics"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/pulls"
        params = {
            "state": state,
            "since": since,
            "per_page": 100,
            "sort": "updated",
            "direction": "desc"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_issues(self, state: str = "closed", days: int = 30) -> List[Dict]:
        """Get issue metrics"""
        since = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/issues"
        params = {
            "state": state,
            "since": since,
            "per_page": 100,
            "sort": "updated",
            "direction": "desc"
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_contributors(self) -> List[Dict]:
        """Get top contributors"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contributors"
        params = {"per_page": 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []
    
    def generate_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        commits = self.get_commits(days)
        prs = self.get_pull_requests("closed", days)
        issues = self.get_issues("closed", days)
        contributors = self.get_contributors()
        repo_stats = self.get_repo_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "period_days": days,
            "repository": repo_stats,
            "commits": {
                "total": len(commits),
                "commits": commits
            },
            "pull_requests": {
                "closed": len(prs),
                "data": prs
            },
            "issues": {
                "closed": len(issues),
                "data": issues
            },
            "contributors": {
                "total": len(contributors),
                "top": contributors[:10]
            }
        }
    
    def save_report(self, filename: str = "analytics_report.json") -> None:
        """Save analytics report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {filename}")


def main():
    """Example usage"""
    import os
    
    # Get credentials from environment
    token = os.getenv("GITHUB_TOKEN")
    owner = "nadeemmallick"
    repo = "nadeemmallick"
    
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        return
    
    analytics = GitHubAnalytics(token, owner, repo)
    
    print("Generating GitHub Analytics Report...")
    print("-" * 50)
    
    # Get repository stats
    stats = analytics.get_repo_stats()
    print(f"\nRepository: {stats.get('name', 'N/A')}")
    print(f"Stars: {stats.get('stars', 0)}")
    print(f"Forks: {stats.get('forks', 0)}")
    print(f"Open Issues: {stats.get('open_issues', 0)}")
    
    # Get activity metrics
    commits = analytics.get_commits(30)
    prs = analytics.get_pull_requests("closed", 30)
    issues = analytics.get_issues("closed", 30)
    contributors = analytics.get_contributors()
    
    print(f"\n📊 Last 30 Days Activity:")
    print(f"Commits: {len(commits)}")
    print(f"Pull Requests (Closed): {len(prs)}")
    print(f"Issues (Closed): {len(issues)}")
    print(f"Total Contributors: {len(contributors)}")
    
    # Save detailed report
    analytics.save_report("github_analytics_report.json")


if __name__ == "__main__":
    main()
