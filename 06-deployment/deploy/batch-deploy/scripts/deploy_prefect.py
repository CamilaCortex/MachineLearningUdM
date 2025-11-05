"""Prefect deployment script for NYC Taxi batch prediction system"""

import asyncio
from prefect import serve

from src.prefect_flows import taxi_batch_prediction_flow, taxi_batch_cleanup_flow
from config.settings import settings


async def create_deployments():
    """Create and serve Prefect deployments using modern Prefect 3.x API"""
    
    print("🚀 Creating Prefect deployments for NYC Taxi Batch Prediction")
    
    # Create deployments using flow.to_deployment()
    batch_deployment = taxi_batch_prediction_flow.to_deployment(
        name="taxi-batch-prediction-scheduled",
        description="Scheduled NYC Taxi batch prediction processing",
        tags=["taxi", "batch", "ml", "prediction"],
        cron=settings.BATCH_SCHEDULE_CRON,
        parameters={
            "use_parallel": True,
            "skip_data_generation": False
        }
    )
    
    cleanup_deployment = taxi_batch_cleanup_flow.to_deployment(
        name="taxi-batch-cleanup-scheduled", 
        description="Scheduled cleanup of old batch files",
        tags=["taxi", "cleanup", "maintenance"],
        cron=settings.CLEANUP_SCHEDULE_CRON
    )
    
    manual_deployment = taxi_batch_prediction_flow.to_deployment(
        name="taxi-batch-prediction-manual",
        description="Manual NYC Taxi batch prediction processing",
        tags=["taxi", "batch", "ml", "prediction", "manual"],
        parameters={
            "use_parallel": True,
            "skip_data_generation": False
        }
    )
    
    print("✅ Deployments created successfully!")
    print("\n📋 Deployment Summary:")
    print(f"  🔄 Batch Processing: Every 2 hours ({settings.BATCH_SCHEDULE_CRON})")
    print(f"  🧹 Cleanup: Daily at 2 AM ({settings.CLEANUP_SCHEDULE_CRON})")
    print("  🎯 Manual: On-demand execution")
    
    return [batch_deployment, cleanup_deployment, manual_deployment]


async def serve_flows():
    """Serve flows for local development and production"""
    print("🏃 Starting Prefect flow server...")
    
    # Create deployments
    deployments = await create_deployments()
    
    print("\n🚀 Starting server with all deployments...")
    
    # Serve all deployments
    await serve(
        *deployments,
        limit=10,
        pause_on_shutdown=True
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        # Local development mode
        asyncio.run(serve_flows())
    else:
        # Create deployments
        asyncio.run(create_deployments())
