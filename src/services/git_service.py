from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import logging
import subprocess
from pathlib import Path

class GitService:
    """Git service following the enhanced three-iterations approach"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.logger = logging.getLogger(__name__)
        
    # First Iteration - Analysis & Understanding
    async def analyze_repository(self) -> Dict:
        """Analyzes repository state and history"""
        try:
            analysis = {
                "current_branch": await self._get_current_branch(),
                "uncommitted_changes": await self._get_uncommitted_changes(),
                "recent_commits": await self._get_recent_commits(),
                "contributors": await self._get_contributors()
            }
            return analysis
        except Exception as e:
            self.logger.error(f"Repository analysis failed: {str(e)}")
            raise
            
    async def _get_current_branch(self) -> str:
        """Gets current branch name"""
        result = await self._run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        return result.strip()
        
    async def _get_uncommitted_changes(self) -> List[str]:
        """Gets list of uncommitted changes"""
        result = await self._run_git_command(["status", "--porcelain"])
        return [line.strip() for line in result.split("\n") if line.strip()]
        
    async def _get_recent_commits(self, limit: int = 10) -> List[Dict]:
        """Gets recent commit history"""
        result = await self._run_git_command([
            "log",
            f"-{limit}",
            "--pretty=format:%H|%an|%ae|%at|%s"
        ])
        commits = []
        for line in result.split("\n"):
            if line.strip():
                hash, author, email, timestamp, message = line.split("|")
                commits.append({
                    "hash": hash,
                    "author": author,
                    "email": email,
                    "timestamp": int(timestamp),
                    "message": message
                })
        return commits
        
    async def _get_contributors(self) -> List[Dict]:
        """Gets repository contributors"""
        result = await self._run_git_command([
            "shortlog",
            "-sne",
            "--all"
        ])
        contributors = []
        for line in result.split("\n"):
            if line.strip():
                count, author = line.strip().split("\t")
                contributors.append({
                    "commits": int(count),
                    "author": author
                })
        return contributors
        
    # Second Iteration - Solution & Implementation
    async def create_branch(self, branch_name: str, from_branch: Optional[str] = None) -> bool:
        """Creates a new branch"""
        try:
            if from_branch:
                await self._run_git_command(["checkout", from_branch])
            
            result = await self._run_git_command(["checkout", "-b", branch_name])
            return "Switched to a new branch" in result
        except Exception as e:
            self.logger.error(f"Branch creation failed: {str(e)}")
            return False
            
    async def commit_changes(self, message: str, files: Optional[List[str]] = None) -> bool:
        """Commits changes to repository"""
        try:
            if files:
                await self._run_git_command(["add", *files])
            else:
                await self._run_git_command(["add", "."])
                
            result = await self._run_git_command(["commit", "-m", message])
            return "[" in result and "]" in result
        except Exception as e:
            self.logger.error(f"Commit failed: {str(e)}")
            return False
            
    async def push_changes(self, branch: Optional[str] = None) -> bool:
        """Pushes changes to remote"""
        try:
            push_command = ["push"]
            if branch:
                push_command.extend(["origin", branch])
                
            result = await self._run_git_command(push_command)
            return "Everything up-to-date" in result or "->" in result
        except Exception as e:
            self.logger.error(f"Push failed: {str(e)}")
            return False
            
    # Third Iteration - Enhancement & Optimization
    async def optimize_repository(self) -> Dict:
        """Optimizes repository performance"""
        try:
            optimization_results = {
                "gc": await self._run_git_command(["gc"]),
                "prune": await self._run_git_command(["prune"]),
                "repack": await self._run_git_command(["repack", "-a", "-d"])
            }
            return optimization_results
        except Exception as e:
            self.logger.error(f"Repository optimization failed: {str(e)}")
            raise
            
    async def analyze_performance(self) -> Dict:
        """Analyzes repository performance"""
        try:
            performance_metrics = {
                "size": await self._get_repo_size(),
                "object_count": await self._get_object_count(),
                "largest_files": await self._get_largest_files()
            }
            return performance_metrics
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {str(e)}")
            raise
            
    # Helper methods
    async def _run_git_command(self, args: List[str]) -> str:
        """Runs a git command and returns output"""
        try:
            process = await asyncio.create_subprocess_exec(
                "git",
                *args,
                cwd=str(self.repo_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Git command failed: {stderr.decode()}")
                
            return stdout.decode()
        except Exception as e:
            self.logger.error(f"Git command failed: {str(e)}")
            raise
            
    async def _get_repo_size(self) -> int:
        """Gets repository size in bytes"""
        result = await self._run_git_command(["count-objects", "-v"])
        for line in result.split("\n"):
            if line.startswith("size-pack"):
                return int(line.split()[1]) * 1024
        return 0
        
    async def _get_object_count(self) -> int:
        """Gets total number of git objects"""
        result = await self._run_git_command(["count-objects", "-v"])
        for line in result.split("\n"):
            if line.startswith("count"):
                return int(line.split()[1])
        return 0
        
    async def _get_largest_files(self, limit: int = 5) -> List[Dict]:
        """Gets largest files in repository"""
        result = await self._run_git_command([
            "ls-files",
            "-z",
            "|",
            "xargs",
            "-0",
            "du",
            "-s",
            "|",
            "sort",
            "-rn",
            "|",
            "head",
            f"-{limit}"
        ])
        
        files = []
        for line in result.split("\n"):
            if line.strip():
                size, path = line.strip().split("\t")
                files.append({
                    "path": path,
                    "size": int(size) * 1024  # Convert to bytes
                })
        return files
