from typing import Dict, Any

from backend.database import get_recommendations, initialize_database, save_recommendation
from backend.ml_model import predict_cloud


def recommend(
    user_name: str,
    budget: float,
    storage: str,
    compute_requirement: str,
    security_requirement: str,
    aiml_requirement: str,
    business_type: str,
    db_path: str = "backend/multicloud.db",
) -> Dict[str, Any]:
    """Generate a cloud recommendation, store it, and return the recommendation result."""
    initialize_database(db_path)

    prediction = predict_cloud(
        budget=budget,
        storage=storage,
        compute_requirement=compute_requirement,
        security_requirement=security_requirement,
        aiml_requirement=aiml_requirement,
        business_type=business_type,
    )

    save_recommendation(
        user_name=user_name,
        budget=budget,
        storage=storage,
        compute_requirement=compute_requirement,
        security_requirement=security_requirement,
        aiml_requirement=aiml_requirement,
        business_type=business_type,
        aws_score=float(prediction.get("aws_score", 0.0)),
        gcp_score=float(prediction.get("gcp_score", 0.0)),
        esds_score=float(prediction.get("esds_score", 0.0)),
        recommended_platform=prediction.get("predicted_platform", "Unknown"),
        db_path=db_path,
    )

    return {
        "user_name": user_name,
        "budget": budget,
        "storage": storage,
        "compute_requirement": compute_requirement,
        "security_requirement": security_requirement,
        "aiml_requirement": aiml_requirement,
        "business_type": business_type,
        **prediction,
        "explanation": (
            f"The decision tree model selected {prediction.get('predicted_platform', 'Unknown')} "
            f"based on your workload and business requirements."
        ),
    }


def get_recommendation_history(db_path: str = "backend/multicloud.db") -> Dict[str, Any]:
    return {"history": get_recommendations(db_path)}


if __name__ == "__main__":
    result = recommend(
        user_name="Test User",
        budget=2800,
        storage="SSD",
        compute_requirement="Heavy",
        security_requirement="Critical",
        aiml_requirement="Advanced",
        business_type="Analytics",
    )
    print(result)
