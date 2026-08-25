import pandas as pd


def calculate_risk_summary(df):
    """
    Creates an overall summary of customer risk.
    """

    summary = {
        "total_customers": len(df),

        "default_customers": int(
            (df["TARGET"] == 1).sum()
        ),

        "non_default_customers": int(
            (df["TARGET"] == 0).sum()
        ),

        "default_rate": (
            df["TARGET"].mean() * 100
        ),

        "high_risk_customers": int(
            (df["RISK_LEVEL"].isin(
                ["High Risk", "Very High Risk"]
            )).sum()
        )
    }

    return summary


def get_risk_factors(customer):
    """
    Explains why a customer received a higher risk score.
    """

    factors = []

    if customer["CREDIT_INCOME_RATIO"] > 6:
        factors.append(
            "Very high credit compared with income"
        )

    elif customer["CREDIT_INCOME_RATIO"] > 4:
        factors.append(
            "High credit compared with income"
        )

    if customer["ANNUITY_INCOME_RATIO"] > 0.30:
        factors.append(
            "High repayment burden compared with income"
        )

    if customer["AVERAGE_EXTERNAL_SCORE"] < 0.30:
        factors.append(
            "Low external credit score"
        )

    if customer["AGE"] < 25:
        factors.append(
            "Young applicant"
        )

    if len(factors) == 0:
        factors.append(
            "No major risk indicators detected"
        )

    return factors


def get_risk_label(risk_score):
    """
    Converts numerical risk score into a readable label.
    """

    if risk_score <= 1:
        return "Low Risk"

    elif risk_score == 2:
        return "Moderate Risk"

    elif risk_score == 3:
        return "High Risk"

    else:
        return "Very High Risk"