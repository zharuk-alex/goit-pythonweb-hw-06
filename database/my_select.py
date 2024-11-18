from sqlalchemy import func, desc
from database.connect import Session
from database.models import Student, Group, Grade, Subject, Teacher
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def select_1():
    with Session() as session:
        result = (
            session.query(
                Student.first_name,
                Student.last_name,
                func.avg(Grade.grade).label("avg_grade"),
            )
            .join(Grade)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .limit(5)
            .all()
        )
    return result


def select_2(subject_id):
    with Session() as session:
        result = (
            session.query(
                Student.first_name,
                Student.last_name,
                func.avg(Grade.grade).label("avg_grade"),
            )
            .join(Grade)
            .filter(Grade.subject_id == subject_id)
            .group_by(Student.id)
            .order_by(desc("avg_grade"))
            .first()
        )
    return result


def select_3(subject_id):
    with Session() as session:
        result = (
            session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
            .join(Student.groups)
            .join(Grade)
            .filter(Grade.subject_id == subject_id)
            .group_by(Group.id)
            .all()
        )
    return result


def select_4():
    with Session() as session:
        result = session.query(func.avg(Grade.grade).label("avg_grade")).scalar()
    return result


def select_5(teacher_id):
    with Session() as session:
        result = (
            session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()
        )
    return result


def select_6(group_id):
    with Session() as session:
        result = (
            session.query(Student.first_name, Student.last_name)
            .join(Student.groups)
            .filter(Group.id == group_id)
            .all()
        )
    return result


def select_7(group_id, subject_id):
    with Session() as session:
        result = (
            session.query(Student.first_name, Student.last_name, Grade.grade)
            .join(Student.groups)
            .join(Grade)
            .filter(Group.id == group_id, Grade.subject_id == subject_id)
            .all()
        )
    return result


def select_8(teacher_id):
    with Session() as session:
        result = (
            session.query(func.avg(Grade.grade).label("avg_grade"))
            .join(Subject)
            .filter(Subject.teacher_id == teacher_id)
            .scalar()
        )
    return result


def select_9(student_id):
    with Session() as session:
        result = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id)
            .group_by(Subject.id)
            .all()
        )
    return result


def select_10(student_id, teacher_id):
    with Session() as session:
        result = (
            session.query(Subject.name)
            .join(Grade)
            .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
            .group_by(Subject.id)
            .all()
        )
    return result


if __name__ == "__main__":
    logger.info(f"select_1: {select_1()}")
    logger.info(f"select_2: {select_2(1)}")
    logger.info(f"select_3: {select_3(1)}")
    logger.info(f"select_4: {select_4()}")
    logger.info(f"select_5: {select_5(1)}")
    logger.info(f"select_6: {select_6(1)}")
    logger.info(f"select_7: {select_7(1, 3)}")
    logger.info(f"select_8: {select_8(1)}")
    logger.info(f"select_9: {select_9(1)}")
    logger.info(f"select_10: {select_10(1, 1)}")
