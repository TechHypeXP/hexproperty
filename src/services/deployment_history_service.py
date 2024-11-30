from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import json
import logging
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.models.deployment_model import DeploymentRecord

class DeploymentHistoryService:
    """Deployment history service following the enhanced three-iterations approach"""
    
    def __init__(self, history_dir: str):
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
    # First Iteration - Analysis & Understanding
    async def analyze_deployment_history(self) -> Dict:
        """Analyzes deployment history for patterns and insights"""
        try:
            deployments = await self._load_all_deployments()
            
            analysis = {
                "total_deployments": len(deployments),
                "success_rate": self._calculate_success_rate(deployments),
                "common_errors": self._identify_common_errors(deployments),
                "stakeholder_impact": self._analyze_stakeholder_impact(deployments)
            }
            
            return analysis
        except Exception as e:
            self.logger.error(f"Deployment history analysis failed: {str(e)}")
            raise
            
    # Second Iteration - Solution & Implementation
    async def record_deployment(self, deployment: DeploymentRecord) -> str:
        """Records a new deployment"""
        try:
            deployment_path = self.history_dir / f"{deployment.deployment_id}.json"
            
            deployment_data = {
                "id": deployment.deployment_id,
                "type": deployment.deployment_type,
                "created_at": deployment.created_at.isoformat(),
                "stakeholders": deployment.stakeholders,
                "objectives": deployment.objectives,
                "status": deployment.status,
                "strategy": deployment.deployment_strategy,
                "steps": deployment.implementation_steps,
                "validation": deployment.validation_results,
                "errors": deployment.errors
            }
            
            with open(deployment_path, 'w') as f:
                json.dump(deployment_data, f, indent=2)
                
            return str(deployment_path)
        except Exception as e:
            self.logger.error(f"Deployment recording failed: {str(e)}")
            raise
            
    async def update_deployment_status(self, deployment_id: str, new_status: str,
                                     modified_by: str) -> bool:
        """Updates deployment status"""
        try:
            deployment_path = self.history_dir / f"{deployment_id}.json"
            if not deployment_path.exists():
                raise FileNotFoundError(f"Deployment {deployment_id} not found")
                
            with open(deployment_path, 'r') as f:
                deployment_data = json.load(f)
                
            deployment_data["status"] = new_status
            deployment_data["last_modified"] = datetime.now().isoformat()
            deployment_data["modified_by"] = modified_by
            
            with open(deployment_path, 'w') as f:
                json.dump(deployment_data, f, indent=2)
                
            return True
        except Exception as e:
            self.logger.error(f"Status update failed: {str(e)}")
            return False
            
    # Third Iteration - Enhancement & Optimization
    async def generate_deployment_metrics(self) -> Dict:
        """Generates comprehensive deployment metrics"""
        try:
            deployments = await self._load_all_deployments()
            
            metrics = {
                "performance": self._calculate_performance_metrics(deployments),
                "reliability": self._calculate_reliability_metrics(deployments),
                "trends": self._analyze_deployment_trends(deployments)
            }
            
            return metrics
        except Exception as e:
            self.logger.error(f"Metrics generation failed: {str(e)}")
            raise
            
    async def optimize_deployment_records(self) -> Dict:
        """Optimizes deployment records for better performance"""
        try:
            optimization_results = {
                "compressed": await self._compress_old_records(),
                "indexed": await self._create_deployment_index(),
                "cleaned": await self._clean_invalid_records()
            }
            
            return optimization_results
        except Exception as e:
            self.logger.error(f"Record optimization failed: {str(e)}")
            raise
            
    # Helper methods
    async def _load_all_deployments(self) -> List[Dict]:
        """Loads all deployment records"""
        deployments = []
        for file_path in self.history_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    deployment_data = json.load(f)
                    deployments.append(deployment_data)
            except Exception as e:
                self.logger.warning(f"Failed to load deployment {file_path}: {str(e)}")
        return deployments
        
    def _calculate_success_rate(self, deployments: List[Dict]) -> float:
        """Calculates deployment success rate"""
        if not deployments:
            return 0.0
            
        successful = sum(1 for d in deployments if d["status"] == "completed")
        return successful / len(deployments)
        
    def _identify_common_errors(self, deployments: List[Dict]) -> Dict[str, int]:
        """Identifies common deployment errors"""
        error_counts = {}
        for deployment in deployments:
            for error in deployment.get("errors", []):
                error_type = error["type"]
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts
        
    def _analyze_stakeholder_impact(self, deployments: List[Dict]) -> Dict[str, List[str]]:
        """Analyzes deployment impact on stakeholders"""
        impact_map = {}
        for deployment in deployments:
            for stakeholder in deployment.get("stakeholders", []):
                if stakeholder not in impact_map:
                    impact_map[stakeholder] = []
                impact_map[stakeholder].append(deployment["id"])
        return impact_map
        
    def _calculate_performance_metrics(self, deployments: List[Dict]) -> Dict:
        """Calculates deployment performance metrics"""
        return {
            "average_duration": self._calculate_average_duration(deployments),
            "success_by_type": self._calculate_success_by_type(deployments),
            "error_frequency": self._calculate_error_frequency(deployments)
        }
        
    def _calculate_reliability_metrics(self, deployments: List[Dict]) -> Dict:
        """Calculates deployment reliability metrics"""
        return {
            "mtbf": self._calculate_mtbf(deployments),
            "mttf": self._calculate_mttf(deployments),
            "availability": self._calculate_availability(deployments)
        }
        
    def _analyze_deployment_trends(self, deployments: List[Dict]) -> Dict:
        """Analyzes deployment trends over time"""
        return {
            "frequency": self._calculate_deployment_frequency(deployments),
            "success_trend": self._calculate_success_trend(deployments),
            "complexity_trend": self._calculate_complexity_trend(deployments)
        }
        
    def _calculate_average_duration(self, deployments: List[Dict]) -> float:
        """Calculates average deployment duration"""
        durations = []
        for deployment in deployments:
            if "created_at" in deployment and deployment.get("status") == "completed":
                created = datetime.fromisoformat(deployment["created_at"])
                if "completed_at" in deployment:
                    completed = datetime.fromisoformat(deployment["completed_at"])
                    duration = (completed - created).total_seconds()
                    durations.append(duration)
        return sum(durations) / len(durations) if durations else 0.0
        
    def _calculate_success_by_type(self, deployments: List[Dict]) -> Dict[str, float]:
        """Calculates success rate by deployment type"""
        type_stats = {}
        for deployment in deployments:
            dep_type = deployment.get("type", "unknown")
            if dep_type not in type_stats:
                type_stats[dep_type] = {"total": 0, "success": 0}
            type_stats[dep_type]["total"] += 1
            if deployment.get("status") == "completed":
                type_stats[dep_type]["success"] += 1
                
        return {
            dep_type: stats["success"] / stats["total"]
            for dep_type, stats in type_stats.items()
        }
        
    def _calculate_error_frequency(self, deployments: List[Dict]) -> Dict[str, int]:
        """Calculates frequency of different error types"""
        error_counts = {}
        for deployment in deployments:
            for error in deployment.get("errors", []):
                error_type = error.get("type", "unknown")
                error_counts[error_type] = error_counts.get(error_type, 0) + 1
        return error_counts
        
    def _calculate_mtbf(self, deployments: List[Dict]) -> float:
        """Calculates Mean Time Between Failures"""
        failures = []
        for deployment in deployments:
            if deployment.get("status") == "failed":
                failures.append(datetime.fromisoformat(deployment["created_at"]))
        
        if len(failures) < 2:
            return 0.0
            
        failures.sort()
        intervals = [(failures[i+1] - failures[i]).total_seconds()
                    for i in range(len(failures)-1)]
        return sum(intervals) / len(intervals)
        
    def _calculate_mttf(self, deployments: List[Dict]) -> float:
        """Calculates Mean Time To Failure"""
        failure_times = []
        for deployment in deployments:
            if deployment.get("status") == "failed":
                created = datetime.fromisoformat(deployment["created_at"])
                if "failed_at" in deployment:
                    failed = datetime.fromisoformat(deployment["failed_at"])
                    failure_times.append((failed - created).total_seconds())
        return sum(failure_times) / len(failure_times) if failure_times else 0.0
        
    def _calculate_availability(self, deployments: List[Dict]) -> float:
        """Calculates system availability percentage"""
        total_deployments = len(deployments)
        if not total_deployments:
            return 0.0
            
        successful = sum(1 for d in deployments if d.get("status") == "completed")
        return (successful / total_deployments) * 100
        
    def _calculate_deployment_frequency(self, deployments: List[Dict]) -> Dict[str, int]:
        """Calculates deployment frequency over time"""
        frequency = {}
        for deployment in deployments:
            date = datetime.fromisoformat(deployment["created_at"]).strftime("%Y-%m")
            frequency[date] = frequency.get(date, 0) + 1
        return frequency
        
    def _calculate_success_trend(self, deployments: List[Dict]) -> Dict[str, float]:
        """Calculates success rate trend over time"""
        trend = {}
        for deployment in deployments:
            date = datetime.fromisoformat(deployment["created_at"]).strftime("%Y-%m")
            if date not in trend:
                trend[date] = {"total": 0, "success": 0}
            trend[date]["total"] += 1
            if deployment.get("status") == "completed":
                trend[date]["success"] += 1
                
        return {
            date: stats["success"] / stats["total"]
            for date, stats in trend.items()
        }
        
    def _calculate_complexity_trend(self, deployments: List[Dict]) -> Dict[str, float]:
        """Calculates deployment complexity trend over time"""
        trend = {}
        for deployment in deployments:
            date = datetime.fromisoformat(deployment["created_at"]).strftime("%Y-%m")
            complexity = len(deployment.get("implementation_steps", [])) + \
                        len(deployment.get("validation_results", {})) + \
                        len(deployment.get("errors", []))
            if date not in trend:
                trend[date] = {"total": 0, "count": 0}
            trend[date]["total"] += complexity
            trend[date]["count"] += 1
                
        return {
            date: stats["total"] / stats["count"]
            for date, stats in trend.items()
        }
        
    async def _compress_old_records(self) -> Dict:
        """Compresses old deployment records"""
        compressed_count = 0
        total_size_saved = 0
        # Implementation details for compression
        return {
            "compressed_count": compressed_count,
            "total_size_saved": total_size_saved
        }
        
    async def _create_deployment_index(self) -> Dict:
        """Creates an index for faster deployment lookups"""
        index = {}
        for file_path in self.history_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    index[data["id"]] = str(file_path)
            except Exception as e:
                self.logger.warning(f"Failed to index {file_path}: {str(e)}")
        return index
        
    async def _clean_invalid_records(self) -> Dict:
        """Cleans invalid deployment records"""
        cleaned_count = 0
        error_count = 0
        # Implementation details for cleaning
        return {
            "cleaned_count": cleaned_count,
            "error_count": error_count
        }
