from flask import Flask, jsonify, request

from app.ingestion.ingest import ingest_repository
from app.ingestion.rag.pipeline import RAGPipeline
from app.ingestion.rag.conversation_manager import ConversationManager


app = Flask(__name__)

pipeline = RAGPipeline()


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "RepoMind",
    })


@app.post("/repositories")
def create_repository():
    data = request.get_json(silent=True) or {}
    repo_url = data.get("repo_url")

    if not repo_url:
        return jsonify({
            "error": "repo_url is required"
        }), 400

    try:
        repository_id = ingest_repository(repo_url)

        return jsonify({
            "repository_id": repository_id,
            "status": "ingested",
        }), 201

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500


@app.post("/conversations")
def create_conversation():
    data = request.get_json(silent=True) or {}

    repository_id = data.get("repository_id")
    title = data.get("title", "New Conversation")

    if repository_id is None:
        return jsonify({
            "error": "repository_id is required"
        }), 400

    manager = ConversationManager()

    try:
        conversation = manager.create_conversation(
            repository_id=repository_id,
            title=title,
        )

        return jsonify({
            "conversation_id": conversation.id,
            "repository_id": conversation.repository_id,
            "title": conversation.title,
        }), 201

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500

    finally:
        manager.close()


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}

    question = data.get("question")
    repository_id = data.get("repository_id")
    conversation_id = data.get("conversation_id")

    if not question:
        return jsonify({
            "error": "question is required"
        }), 400

    if repository_id is None:
        return jsonify({
            "error": "repository_id is required"
        }), 400

    try:
        answer = pipeline.answer(
            question=question,
            repository_id=repository_id,
            conversation_id=conversation_id,
        )

        return jsonify({
            "answer": answer,
            "repository_id": repository_id,
            "conversation_id": conversation_id,
        })

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    except Exception as exc:
        return jsonify({
            "error": str(exc)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )
