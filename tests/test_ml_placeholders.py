def test_ml_packages_are_placeholders() -> None:
    from ml.behaviour import STATUS as behaviour_status
    from ml.fusion import STATUS as fusion_status
    from ml.phishing import STATUS as phishing_status
    from ml.url_risk import STATUS as url_status

    assert phishing_status == "not_implemented"
    assert url_status == "not_implemented"
    assert behaviour_status == "not_implemented"
    assert fusion_status == "not_implemented"
