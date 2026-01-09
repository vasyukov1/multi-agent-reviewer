from app.core.orchestrator import ReviewOrchestrator
from app.models.schemas import AdInput, AgentIssue

def test_review_flow_with_mocked_agents(monkeypatch):
    orchestrator = ReviewOrchestrator()

    # Mock Auditor
    def mock_auditor_analyze(ad):
        return 0.6, [
            AgentIssue(
                agent="auditor",
                code="MOCK_RISK",
                message="Mocked risk",
            )
        ]
    
    # Mock Quality
    def mock_quality_analyze(ad):
        return 0.8, []
    
    monkeypatch.setattr(orchestrator.auditor, "analyze", mock_auditor_analyze)
    monkeypatch.setattr(orchestrator.quality, "analyze", mock_quality_analyze)

    ad = AdInput(
        title="Test title",
        description="Test description long enough",
        category="test",
    )

    result = orchestrator.run_review(ad)

    assert result.risk_score == 0.6
    assert result.quality_score == 0.8
    assert result.verdict == "revise"  # 0.5 * (1 - 0.6) + 0.5 * 0.8 = 0.6
    assert len(result.issues) == 1
    assert result.issues[0].code == "MOCK_RISK"
