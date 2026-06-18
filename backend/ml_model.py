from typing import Dict, List, Tuple

from sklearn.tree import DecisionTreeClassifier

LABEL_ENCODER = {"AWS": 0, "Google Cloud": 1, "ESDS": 2}
LABEL_DECODER = {value: key for key, value in LABEL_ENCODER.items()}

BUDGET_MAP = {"low": 0, "medium": 1, "high": 2}
STORAGE_MAP = {"hdd": 0, "ssd": 1, "nvme": 2}
COMPUTE_MAP = {"light": 0, "standard": 1, "heavy": 2}
SECURITY_MAP = {"standard": 0, "high": 1, "critical": 2}
AIML_MAP = {"none": 0, "basic": 1, "advanced": 2}
BUSINESS_MAP = {
    "small": 0,
    "startup": 1,
    "enterprise": 2,
    "analytics": 1,
    "saas": 1,
    "government": 2,
}


def _encode_value(value: str, mapping: Dict[str, int], default: int = 0) -> int:
    if not isinstance(value, str):
        return default
    return mapping.get(value.strip().lower(), default)


def _prepare_sample(
    budget: float,
    storage: str,
    compute_requirement: str,
    security_requirement: str,
    aiml_requirement: str,
    business_type: str,
) -> List[float]:
    budget_level = "low" if budget < 1500 else "medium" if budget < 5000 else "high"

    return [
        _encode_value(budget_level, BUDGET_MAP),
        _encode_value(storage, STORAGE_MAP),
        _encode_value(compute_requirement, COMPUTE_MAP),
        _encode_value(security_requirement, SECURITY_MAP),
        _encode_value(aiml_requirement, AIML_MAP),
        _encode_value(business_type, BUSINESS_MAP),
    ]


def _generate_training_data() -> Tuple[List[List[float]], List[int]]:
    training_examples = [
        (1200, "ssd", "standard", "high", "basic", "enterprise", "AWS"),
        (8000, "nvme", "heavy", "critical", "advanced", "enterprise", "AWS"),
        (2500, "ssd", "heavy", "high", "advanced", "saas", "AWS"),
        (3200, "ssd", "heavy", "standard", "advanced", "analytics", "Google Cloud"),
        (1800, "ssd", "standard", "high", "basic", "startup", "Google Cloud"),
        (4200, "nvme", "heavy", "critical", "advanced", "analytics", "Google Cloud"),
        (700, "hdd", "light", "standard", "none", "small", "ESDS"),
        (1500, "hdd", "standard", "standard", "basic", "small", "ESDS"),
        (900, "hdd", "light", "high", "basic", "small", "ESDS"),
        (5000, "nvme", "heavy", "critical", "advanced", "government", "AWS"),
        (2000, "ssd", "standard", "high", "advanced", "enterprise", "Google Cloud"),
        (1300, "ssd", "light", "standard", "basic", "startup", "ESDS"),
        (2700, "ssd", "standard", "high", "basic", "analytics", "Google Cloud"),
        (1900, "hdd", "standard", "high", "basic", "small", "ESDS"),
        (6000, "nvme", "heavy", "critical", "advanced", "enterprise", "AWS"),
    ]

    X: List[List[float]] = []
    y: List[int] = []
    for budget, storage, compute, security, aiml, business, label in training_examples:
        X.append(_prepare_sample(budget, storage, compute, security, aiml, business))
        y.append(LABEL_ENCODER[label])

    return X, y


def train_model() -> DecisionTreeClassifier:
    model = DecisionTreeClassifier(random_state=42)
    X, y = _generate_training_data()
    model.fit(X, y)
    return model


def predict_cloud(
    budget: float,
    storage: str,
    compute_requirement: str,
    security_requirement: str,
    aiml_requirement: str,
    business_type: str,
) -> Dict[str, object]:
    model = train_model()
    sample = _prepare_sample(
        budget,
        storage,
        compute_requirement,
        security_requirement,
        aiml_requirement,
        business_type,
    )
    prediction = model.predict([sample])[0]
    probabilities = model.predict_proba([sample])[0]

    predicted_platform = LABEL_DECODER.get(prediction, "Unknown")
    return {
        "predicted_platform": predicted_platform,
        "confidence_score": round(float(max(probabilities)), 2),
        "aws_score": round(float(probabilities[LABEL_ENCODER["AWS"]]), 2),
        "gcp_score": round(float(probabilities[LABEL_ENCODER["Google Cloud"]]), 2),
        "esds_score": round(float(probabilities[LABEL_ENCODER["ESDS"]]), 2),
    }


if __name__ == "__main__":
    print(predict_cloud(
        budget=2800,
        storage="SSD",
        compute_requirement="heavy",
        security_requirement="critical",
        aiml_requirement="advanced",
        business_type="analytics",
    ))
