"""Git integration service for template version control.

First Iteration - Analysis & Understanding:
-------------------------------------
Day-in-the-Life Analysis:
* Teams need version control
* Changes require tracking
* History needs maintenance
* Collaboration is essential

Objectives:
* Version control
* Change tracking
* History management
* Collaboration support

Gap Analysis:
* Manual versioning
* Poor change tracking
* Limited history
* Difficult collaboration

Second Iteration - Solution & Implementation:
---------------------------------------
Gap Management:
* Git integration
* Change tracking
* History system
* Team workflows

Problem-Solving Approach:
* Repository management
* Branch strategies
* Commit handling
* Conflict resolution

Third Iteration - Enhancement & Optimization:
---------------------------------------
Solution Refinement:
* Performance tuning
* Storage efficiency
* Operation batching
* Cache management

Future Scenarios:
* Large repositories
* Complex workflows
* Custom integrations
* Advanced automation

Integration Touchpoints:
* Template service
* Deployment system
* CI/CD pipeline
* Monitoring tools
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from git import Repo, GitCommandError
from loguru import logger

from ..models.config import ConfigModel
from ..models.document import DocumentMetadataModel

class GitService:
    """Git integration service for version control.
    
    First Iteration - Analysis & Understanding:
    -------------------------------------
    Day-in-the-Life:
    * Teams commit changes
    * Systems track versions
    * History needs review
    * Changes need sync
    
    Objectives:
    * Version control
    * Change tracking
    * History access
    * Team sync
    
    Gaps:
    * Manual versioning
    * Poor tracking
    * Limited history
    * Sync issues
    
    Second Iteration - Solution & Implementation:
    --------------------------------------
    Gap Management:
    * Git integration
    * Change tracking
    * History system
    * Sync mechanism
    
    Problem-Solving:
    * Repository setup
    * Branch strategy
    * Commit handling
    * Conflict resolution
    
    Implementation:
    * Core operations
    * Event handling
    * Error recovery
    * Status tracking
    
    Third Iteration - Enhancement & Optimization:
    --------------------------------------
    Solution Refinement:
    * Performance tuning
    * Storage efficiency
    * Operation batching
    * Cache strategy
    
    Future Scenarios:
    * Large repos
    * Complex flows
    * Custom hooks
    * Advanced automation
    
    Integration Analysis:
    * Template system
    * Deployment service
    * CI/CD pipeline
    * Monitoring tools
    """
    
    def __init__(self, config: ConfigModel):
        """Initialize Git service.
        
        First Iteration:
        * Basic setup
        * Config loading
        * Path initialization
        
        Second Iteration:
        * Repository setup
        * Branch config
        * Event handlers
        
        Third Iteration:
        * Performance setup
        * Cache init
        * Monitor setup
        """
        self.config = config
        self.repo_path = Path(config.paths.template_root)
        self._init_repository()
        
    def _init_repository(self) -> None:
        """Initialize Git repository.
        
        First Iteration:
        * Basic init
        * Config setup
        * Path check
        
        Second Iteration:
        * Branch setup
        * Remote config
        * Hook setup
        
        Third Iteration:
        * Performance
        * Security
        * Monitoring
        """
        try:
            if not (self.repo_path / '.git').exists():
                self.repo = Repo.init(self.repo_path)
                logger.info(f"Initialized Git repository: {self.repo_path}")
            else:
                self.repo = Repo(self.repo_path)
                logger.info(f"Loaded existing repository: {self.repo_path}")
        except GitCommandError as e:
            logger.error(f"Git initialization error: {e}")
            raise
            
    async def commit_changes(
        self,
        files: List[str],
        message: str,
        author: Optional[str] = None
    ) -> str:
        """Commit changes to repository.
        
        First Iteration:
        * Basic commit
        * File tracking
        * Message handling
        
        Second Iteration:
        * Author handling
        * Validation
        * Event handling
        
        Third Iteration:
        * Performance
        * Batching
        * Analytics
        """
        try:
            # Add files
            self.repo.index.add(files)
            
            # Create commit
            commit = self.repo.index.commit(
                message,
                author=author
            )
            
            logger.info(f"Created commit: {commit.hexsha}")
            return commit.hexsha
            
        except GitCommandError as e:
            logger.error(f"Commit error: {e}")
            raise
            
    async def get_history(
        self,
        path: Optional[str] = None,
        max_count: int = 100
    ) -> List[Dict[str, Any]]:
        """Get commit history.
        
        First Iteration:
        * Basic history
        * Commit info
        * Path filtering
        
        Second Iteration:
        * Advanced filtering
        * Detailed info
        * Performance
        
        Third Iteration:
        * Caching
        * Analytics
        * Optimization
        """
        try:
            commits = []
            for commit in self.repo.iter_commits(
                paths=path,
                max_count=max_count
            ):
                commits.append({
                    'hash': commit.hexsha,
                    'message': commit.message,
                    'author': str(commit.author),
                    'date': datetime.fromtimestamp(commit.committed_date),
                    'files': list(commit.stats.files.keys())
                })
                
            return commits
            
        except GitCommandError as e:
            logger.error(f"History error: {e}")
            raise
            
    async def create_branch(
        self,
        branch_name: str,
        start_point: Optional[str] = None
    ) -> None:
        """Create a new branch.
        
        First Iteration:
        * Basic creation
        * Name handling
        * Point setting
        
        Second Iteration:
        * Validation
        * Error handling
        * Event handling
        
        Third Iteration:
        * Performance
        * Security
        * Analytics
        """
        try:
            if start_point:
                self.repo.create_head(branch_name, start_point)
            else:
                self.repo.create_head(branch_name)
                
            logger.info(f"Created branch: {branch_name}")
            
        except GitCommandError as e:
            logger.error(f"Branch creation error: {e}")
            raise
            
    async def switch_branch(self, branch_name: str) -> None:
        """Switch to a branch.
        
        First Iteration:
        * Basic switch
        * Name validation
        * State check
        
        Second Iteration:
        * Clean check
        * Event handling
        * Error recovery
        
        Third Iteration:
        * Performance
        * Security
        * Analytics
        """
        try:
            self.repo.heads[branch_name].checkout()
            logger.info(f"Switched to branch: {branch_name}")
            
        except GitCommandError as e:
            logger.error(f"Branch switch error: {e}")
            raise
            
    async def get_changes(
        self,
        ref: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """Get working directory changes.
        
        First Iteration:
        * Basic changes
        * Status check
        * File listing
        
        Second Iteration:
        * Detailed status
        * Change types
        * Filtering
        
        Third Iteration:
        * Performance
        * Analytics
        * Optimization
        """
        try:
            changes = {
                'modified': [],
                'added': [],
                'deleted': [],
                'untracked': []
            }
            
            # Get status
            for item in self.repo.index.diff(None):
                if item.change_type == 'M':
                    changes['modified'].append(item.a_path)
                elif item.change_type == 'A':
                    changes['added'].append(item.a_path)
                elif item.change_type == 'D':
                    changes['deleted'].append(item.a_path)
                    
            # Get untracked files
            changes['untracked'] = self.repo.untracked_files
            
            return changes
            
        except GitCommandError as e:
            logger.error(f"Status error: {e}")
            raise
            
    async def revert_changes(
        self,
        files: Optional[List[str]] = None
    ) -> None:
        """Revert working directory changes.
        
        First Iteration:
        * Basic revert
        * File handling
        * State check
        
        Second Iteration:
        * Validation
        * Error handling
        * Event handling
        
        Third Iteration:
        * Performance
        * Security
        * Analytics
        """
        try:
            if files:
                self.repo.index.checkout(files)
            else:
                self.repo.index.checkout()
                
            logger.info("Reverted changes")
            
        except GitCommandError as e:
            logger.error(f"Revert error: {e}")
            raise
