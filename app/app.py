
import os, traceback
from flask import Flask, session, render_template
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from langchain.schema import HumanMessage, AIMessage
from app.chain import qa_chain

# Flask setup
app = Flask(__name__, template_folder="templates")
app.config["SECRET_KEY"] = "change-me"
socketio = SocketIO(app, cors_allowed_origins="*")

# SQLite analytics

engine = create_engine("sqlite:///analytics/bot.db", echo=False)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    role = Column(String(10))
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    rating = Column(Integer)  # 1 = 👍, 0 = 👎
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def categorize_question(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ("price", "cost", "bill", "plan")):
        return "pricing"
    if any(k in t for k in ("slack", "integrat", "api", "webhook")):
        return "integration"
    if any(k in t for k in ("security", "gdpr", "encrypt")):
        return "security"
    if any(k in t for k in ("analytics", "report", "dashboard")):
        return "analytics"
    return "other"

@app.route("/")
def index():
    session.setdefault("history", [])
    return render_template("chat.html")

@socketio.on("user_message")
def handle_message(data):
    msg = data.get("message", "")
    db = DBSession()
    try:
        # Log user message with type
        qtype = categorize_question(msg)
        db.add(Log(role="user", content=f"{msg} [type={qtype}]"))
        db.commit()

        # Update history
        session["history"].append(HumanMessage(content=msg))

        # Run QA chain
        res = qa_chain({"query": msg, "chat_history": session["history"]})
        ans = res["result"] if isinstance(res, dict) else res

        # Fallback
        if not ans or len(ans) < 10:
            ans = (
                "I’m sorry, I don’t have that information. "
                "Please rephrase your question or contact support."
            )

        # Log bot response
        db.add(Log(role="bot", content=ans))
        db.commit()

        # Append to history & emit
        session["history"].append(AIMessage(content=ans))
        emit("bot_response", {"message": ans})

    except Exception:
        print(traceback.format_exc())
        emit("bot_response", {"message": "Error occurred, please try again."})

    finally:
        db.close()

@socketio.on("user_rating")
def handle_rating(data):
    question = data.get("question", "")
    rating = int(data.get("rating", 0))
    db = DBSession()
    db.add(Rating(question=question, rating=rating))
    db.commit()
    db.close()

@app.route("/analytics")
def analytics():
    db = DBSession()
    total = db.query(Log).filter(Log.role == "user").count()
    ups = db.query(Rating).filter(Rating.rating == 1).count()
    downs = db.query(Rating).filter(Rating.rating == 0).count()
    by_type = db.query(Log.content, func.count()).group_by(Log.content).all()
    db.close()
    return {
        "total_questions": total,
        "satisfaction": {"up": ups, "down": downs},
        "by_type": {k: v for k, v in by_type}
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
