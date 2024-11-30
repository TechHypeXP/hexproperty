import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.git_service import GitService

@pytest.fixture
def repo_dir(tmp_path):
    """Creates a temporary directory for git tests"""
    return tmp_path / "repo"

@pytest.fixture
def git_service(repo_dir):
    """Creates a git service instance"""
    repo_dir.mkdir(exist_ok=True)
    return GitService(str(repo_dir))

@pytest.mark.asyncio
async def test_analyze_repository(git_service):
    """Tests repository analysis functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        # Mock git command responses
        mock_run.side_effect = [
            "main\n",  # current branch
            "M file1.txt\n",  # uncommitted changes
            "hash1|author1|email1|1234567|message1\n",  # recent commits
            "5\tauthor1 <email1>\n"  # contributors
        ]
        
        analysis = await git_service.analyze_repository()
        
        assert "current_branch" in analysis
        assert "uncommitted_changes" in analysis
        assert "recent_commits" in analysis
        assert "contributors" in analysis
        assert analysis["current_branch"] == "main"
        assert len(analysis["uncommitted_changes"]) == 1
        assert len(analysis["recent_commits"]) == 1
        assert len(analysis["contributors"]) == 1

@pytest.mark.asyncio
async def test_create_branch(git_service):
    """Tests branch creation functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "Switched to a new branch 'feature'\n"
        
        result = await git_service.create_branch("feature")
        assert result is True
        
        # Test branch creation from another branch
        result = await git_service.create_branch("feature2", "main")
        assert result is True
        mock_run.assert_called_with(["checkout", "-b", "feature2"])

@pytest.mark.asyncio
async def test_commit_changes(git_service):
    """Tests commit functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "[main abc123] Test commit\n"
        
        # Test commit all changes
        result = await git_service.commit_changes("Test commit")
        assert result is True
        mock_run.assert_called_with(["commit", "-m", "Test commit"])
        
        # Test commit specific files
        files = ["file1.txt", "file2.txt"]
        result = await git_service.commit_changes("Test commit", files)
        assert result is True
        mock_run.assert_called_with(["commit", "-m", "Test commit"])

@pytest.mark.asyncio
async def test_push_changes(git_service):
    """Tests push functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "Everything up-to-date\n"
        
        # Test push current branch
        result = await git_service.push_changes()
        assert result is True
        mock_run.assert_called_with(["push"])
        
        # Test push specific branch
        result = await git_service.push_changes("feature")
        assert result is True
        mock_run.assert_called_with(["push", "origin", "feature"])

@pytest.mark.asyncio
async def test_optimize_repository(git_service):
    """Tests repository optimization functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "Optimizing repository\n"
        
        optimization_results = await git_service.optimize_repository()
        
        assert "gc" in optimization_results
        assert "prune" in optimization_results
        assert "repack" in optimization_results

@pytest.mark.asyncio
async def test_analyze_performance(git_service):
    """Tests performance analysis functionality"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.side_effect = [
            "size-pack: 1000\n",  # repo size
            "count: 500\n",  # object count
            "1000\tfile1.txt\n500\tfile2.txt\n"  # largest files
        ]
        
        performance_metrics = await git_service.analyze_performance()
        
        assert "size" in performance_metrics
        assert "object_count" in performance_metrics
        assert "largest_files" in performance_metrics
        assert performance_metrics["size"] > 0
        assert performance_metrics["object_count"] > 0
        assert len(performance_metrics["largest_files"]) > 0

@pytest.mark.asyncio
async def test_git_command_error(git_service):
    """Tests error handling in git commands"""
    with patch('asyncio.create_subprocess_exec', new_callable=AsyncMock) as mock_exec:
        process_mock = AsyncMock()
        process_mock.communicate.return_value = (b"", b"error message")
        process_mock.returncode = 1
        mock_exec.return_value = process_mock
        
        with pytest.raises(Exception) as exc_info:
            await git_service._run_git_command(["status"])
        assert "Git command failed" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_repo_size(git_service):
    """Tests repository size calculation"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "size-pack: 1000\n"
        
        size = await git_service._get_repo_size()
        assert size == 1000 * 1024  # Converted to bytes

@pytest.mark.asyncio
async def test_get_object_count(git_service):
    """Tests git object counting"""
    with patch.object(git_service, '_run_git_command', new_callable=AsyncMock) as mock_run:
        mock_run.return_value = "count: 500\n"
        
        count = await git_service._get_object_count()
        assert count == 500
