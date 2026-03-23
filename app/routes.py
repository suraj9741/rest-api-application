from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db import SessionLocal
from app.models.student import Student
import logging

student_bp = Blueprint("students", __name__, url_prefix="/api/v1/students")

logger = logging.getLogger(__name__)


# Create student
@student_bp.route("/", methods=["POST"])
def create_student():
    session = SessionLocal()
    data = request.json

    # 🔹 Validate input
    if not data:
        return {"error": "Request body is required"}, 400
    if "first_name" not in data:
        return {"error": "first_name is required"}, 400

    # 🔹 Convert string to date
    dob = None
    if data.get("date_of_birth"):
        try:
            dob = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400

    # 🔹 Create student object
    student = Student(
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        email=data.get("email"),
        gender=data.get("gender"),
        date_of_birth=dob
    )

    # 🔹 DB operation with error handling
    try:
        session.add(student)
        session.commit()
        session.refresh(student)
    except IntegrityError:
        session.rollback()
        return {"error": "Email already exists"}, 400
    except Exception as e:
        session.rollback()
        return {"error": "Something went wrong"}, 500
    finally:
        session.close()

    logger.info(f"Student created: {student.student_id}")

    return jsonify({"id": student.student_id}), 201


# Get all students
@student_bp.route("/", methods=["GET"])
def get_students():
    session = SessionLocal()
    students = session.query(Student).all()
    return jsonify([s.to_dict() for s in students])


# Get student by ID
@student_bp.route("/<int:id>", methods=["GET"])
def get_student(id):
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(student_id=id).first()
        if not student:
            return {"error": "Student not found"}, 404
        return jsonify(student.to_dict())
    except Exception:
        return {"error": "Something went wrong"}, 500
    finally:
        session.close()

# Update student by ID
@student_bp.route("/<int:id>", methods=["PUT"])
def update_student(id):
    session = SessionLocal()
    data = request.json

    # 🔹 Validate input
    if not data:
        return {"error": "Request body is required"}, 400
    try:
        student = session.query(Student).filter_by(student_id=id).first()
        if not student:
            return {"error": "Student not found"}, 404

        # 🔹 Update fields
        student.first_name = data.get("first_name", student.first_name)
        student.last_name = data.get("last_name", student.last_name)
        student.email = data.get("email", student.email)
        student.gender = data.get("gender", student.gender)

        # 🔹 Handle date_of_birth
        if data.get("date_of_birth"):
            try:
                student.date_of_birth = datetime.strptime(
                    data["date_of_birth"], "%Y-%m-%d"
                ).date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}, 400
        session.commit()
        logger.info(f"Student updated: {id}")
        return student.to_dict()

    except IntegrityError:
        session.rollback()
        return {"error": "Email already exists"}, 400

    except Exception:
        session.rollback()
        return {"error": "Something went wrong"}, 500

    finally:
        session.close()

# Delete student by ID
@student_bp.route("/<int:id>", methods=["DELETE"])
def delete_student(id):
    session = SessionLocal()
    try:
        student = session.query(Student).filter_by(student_id=id).first()
        if not student:
            return {"error": "Student not found"}, 404
        session.delete(student)
        session.commit()
        logger.info(f"Student deleted: {id}")
        return {
            "message": "Student deleted successfully",
            "deleted_id": id
        }, 200

    except SQLAlchemyError:
        session.rollback()
        return {"error": "Database error occurred"}, 500
    except Exception:
        session.rollback()
        return {"error": "Something went wrong"}, 500
    finally:
        session.close()


# Healthcheck
@student_bp.route("/healthcheck", methods=["GET"])
def health():
    session = SessionLocal()
    checks = {}
    checks["app"] = "up"
    try:
        session.execute(text("SELECT 1"))
        checks["database"] = "up"
    except Exception:
        checks["database"] = "down"
    finally:
        session.close()
    overall_status = "ok" if all(v == "up" for v in checks.values()) else "error"
    return {
        "status": overall_status,
        "checks": checks
    }, 200 if overall_status == "ok" else 500