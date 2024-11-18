from faker import Faker
from sqlalchemy import text
from random import randint, choice
from database.connect import Session
from database.models import Student, Group, Teacher, Subject, Grade

fake = Faker()


def clear_database(session):
    session.query(Grade).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Student).delete()
    session.query(Group).delete()
    session.commit()

    tables = ["students", "teachers", "groups", "subjects", "grades"]
    for table in tables:
        session.execute(text(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1"))
    session.commit()


def seed_data():
    with Session() as session:
        clear_database(session)

        # Group
        groups = [Group(name=f"{i}") for i in ["A", "B", "C"]]
        session.bulk_save_objects(groups)
        session.commit()

        # Teacher
        teachers = [
            Teacher(first_name=fake.first_name(), last_name=fake.last_name())
            for _ in range(randint(3, 5))
        ]
        session.bulk_save_objects(teachers)
        session.commit()

        # Subject
        teacher_ids = [teacher.id for teacher in session.query(Teacher).all()]
        subjects = [
            Subject(name=fake.job(), teacher_id=choice(teacher_ids))
            for _ in range(randint(5, 8))
        ]
        session.bulk_save_objects(subjects)
        session.commit()

        # Student
        students = [
            Student(first_name=fake.first_name(), last_name=fake.last_name())
            for _ in range(50)
        ]
        session.bulk_save_objects(students)
        session.commit()

        # Group - Student
        group_ids = [group.id for group in session.query(Group).all()]
        for student in session.query(Student).all():
            assigned_groups = fake.random_elements(elements=group_ids, length=1)
            student.groups.extend(
                session.query(Group).filter(Group.id.in_(assigned_groups)).all()
            )
        session.commit()

        # Subject
        subject_ids = [subject.id for subject in session.query(Subject).all()]
        for student in session.query(Student).all():
            grades = [
                Grade(
                    student_id=student.id,
                    subject_id=choice(subject_ids),
                    grade=randint(1, 20),
                    date_received=fake.date_this_year(),
                )
                for _ in range(randint(10, 20))
            ]
            session.bulk_save_objects(grades)
        session.commit()


if __name__ == "__main__":
    seed_data()
