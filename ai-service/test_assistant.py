"""
Automated Test Suite for Surya M's Portfolio AI Assistant Service.
Tests endpoints, grounding, guardrails, validation, and rate-limiting.
"""

import sys
from fastapi.testclient import TestClient

from main import app, ip_request_history

client = TestClient(app)


def test_health():
    """Verify health endpoint returns healthy status and service info."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "provider" in data
    print("PASS: test_health")


def test_suggested_questions():
    """Verify suggested questions endpoint returns expected starter prompts."""
    response = client.get("/api/suggested-questions")
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) >= 4
    assert any("MES" in q["label"] for q in questions)
    print("PASS: test_suggested_questions")


def test_teamtrack_grounding():
    """Verify assistant correctly returns TeamTrack details, stack, and case study action."""
    response = client.post("/api/chat", json={"message": "Tell me about the TeamTrack project"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "TeamTrack" in reply
    assert "HMAC" in reply or "hmacAuth" in reply
    assert "Socket.IO" in reply
    assert "MySQL" in reply
    assert data.get("suggested_actions") is not None
    assert any(a["target"] == "modal-teamtrack" for a in data["suggested_actions"] if a["type"] == "case_study")
    print("PASS: test_teamtrack_grounding")


def test_visionguard_grounding():
    """Verify assistant correctly returns VisionGuard AI details, YOLO, and repo action."""
    response = client.post("/api/chat", json={"message": "What is VisionGuard AI and how does it detect spoofing?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "VisionGuard AI" in reply
    assert "YOLO" in reply
    assert "OpenCV" in reply
    assert data.get("suggested_actions") is not None
    assert any("github.com/surya-murugasen" in a["url"] for a in data["suggested_actions"] if a["type"] == "repo")
    print("PASS: test_visionguard_grounding")


def test_mes_traceability_grounding():
    """Verify assistant accurately handles MES Traceability and sanitized company context."""
    response = client.post("/api/chat", json={"message": "What is Surya's work on Manufacturing Execution Systems (MES)?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "Manufacturing Execution System" in reply
    assert "KnowledgeQ" in reply
    assert "Node.js" in reply or "TypeScript" in reply
    print("PASS: test_mes_traceability_grounding")


def test_rag_document_intelligence_grounding():
    """Verify assistant accurately handles RAG Document Intelligence, FAISS, PyMuPDF, and case study action."""
    response = client.post("/api/chat", json={"message": "Explain Surya's RAG Document Intelligence project and how vector search works"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "RAG Document Intelligence" in reply
    assert "FAISS" in reply
    assert "PyMuPDF" in reply
    assert "88" in reply
    assert data.get("suggested_actions") is not None
    assert any(a["target"] == "modal-rag" for a in data["suggested_actions"] if a["type"] == "case_study")
    print("PASS: test_rag_document_intelligence_grounding")


def test_qa_query_1_architecture():
    """Test Query 1: 'Explain my RAG Document Intelligence architecture.'"""
    response = client.post("/api/chat", json={"message": "Explain my RAG Document Intelligence architecture."})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "RAG Document Intelligence" in reply
    assert "Architecture" in reply or "architecture" in reply
    assert "PyMuPDF" in reply
    assert "FAISS" in reply
    assert "88" in reply
    assert any(a["target"] == "modal-rag" for a in data.get("suggested_actions", []))
    print("PASS: test_qa_query_1_architecture")


def test_qa_query_2_faiss_vector_search():
    """Test Query 2: 'How does FAISS vector search work in my project?'"""
    response = client.post("/api/chat", json={"message": "How does FAISS vector search work in my project?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "FAISS" in reply
    assert "IndexFlatIP" in reply
    assert "Cosine Similarity" in reply
    assert "page" in reply.lower()
    assert any(a["target"] == "modal-rag" for a in data.get("suggested_actions", []))
    print("PASS: test_qa_query_2_faiss_vector_search")


def test_qa_query_3_user_isolation():
    """Test Query 3: 'How do you prevent one user from accessing another user's documents?'"""
    response = client.post("/api/chat", json={"message": "How do you prevent one user from accessing another user's documents?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "Authorization" in reply or "Session" in reply or "session" in reply
    assert "cookie" in reply.lower() or "session" in reply.lower()
    assert "filter" in reply.lower() or "user_id" in reply
    assert any(a["target"] == "modal-rag" for a in data.get("suggested_actions", []))
    print("PASS: test_qa_query_3_user_isolation")


def test_qa_query_4_ocr_refusal():
    """Test Query 4: 'Does my RAG system support OCR?' (Must refuse / state no OCR support)"""
    response = client.post("/api/chat", json={"message": "Does my RAG system support OCR?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    # Must clearly deny OCR support and explain PyMuPDF direct text layer extraction
    assert "not" in reply.lower() or "no" in reply.lower()
    assert "PyMuPDF" in reply
    assert "is_scanned_image_only" in reply or "scanned" in reply.lower()
    assert any(a["target"] == "modal-rag" for a in data.get("suggested_actions", []))
    print("PASS: test_qa_query_4_ocr_refusal")


def test_qa_query_5_enterprise_scale():
    """Test Query 5: 'Is this deployed at enterprise scale?' (Must clarify local/Docker, not public enterprise)"""
    response = client.post("/api/chat", json={"message": "Is this deployed at enterprise scale?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    assert "Docker Compose" in reply or "local" in reply.lower()
    assert "not" in reply.lower()
    assert "88" in reply or "KnowledgeQ" in reply
    assert any(a["target"] == "modal-rag" for a in data.get("suggested_actions", []))
    print("PASS: test_qa_query_5_enterprise_scale")


def test_missing_information_refusal():
    """Verify assistant does NOT hallucinate on topics Surya has no verified experience with."""
    response = client.post("/api/chat", json={"message": "Can Surya build an enterprise blockchain smart contract in Solidity?"})
    assert response.status_code == 200
    data = response.json()
    reply = data["reply"]
    # Must declare absence of verified records and provide contact link
    assert "don't have verified records" in reply or "I do not have verified records" in reply
    assert "suryamurugasen135@gmail.com" in reply
    print("PASS: test_missing_information_refusal")


def test_validation_empty_message():
    """Verify empty string request is rejected with HTTP 422 or 400."""
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code in [400, 422]
    print("PASS: test_validation_empty_message")


def test_validation_oversized_message():
    """Verify query over 500 characters is rejected by Pydantic validator with HTTP 422."""
    long_msg = "A" * 501
    response = client.post("/api/chat", json={"message": long_msg})
    assert response.status_code == 422
    print("PASS: test_validation_oversized_message")


def test_rate_limiting():
    """Verify rate limiter triggers HTTP 429 when threshold is reached."""
    # Reset history
    ip_request_history.clear()
    
    # Send 20 requests (allowed)
    for _ in range(20):
        res = client.post("/api/chat", json={"message": "Hello"})
        assert res.status_code == 200

    # 21st request should trigger rate limit (429)
    res_limited = client.post("/api/chat", json={"message": "One more question"})
    assert res_limited.status_code == 429
    assert "Rate limit exceeded" in res_limited.json()["detail"]
    
    # Clean up history for future tests
    ip_request_history.clear()
    print("PASS: test_rate_limiting")


if __name__ == "__main__":
    print("Running Portfolio AI Assistant Test Suite...")
    test_health()
    test_suggested_questions()
    test_teamtrack_grounding()
    test_visionguard_grounding()
    test_mes_traceability_grounding()
    test_rag_document_intelligence_grounding()
    test_missing_information_refusal()
    test_validation_empty_message()
    test_validation_oversized_message()
    test_rate_limiting()
    print("\nALL 10 TESTS PASSED SUCCESSFULLY!")
