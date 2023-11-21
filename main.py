from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, select, update, delete, \
    and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased

DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/db'
engine = create_engine(DATABASE_URL)

metadata = MetaData()

users_table = Table('users', metadata,
                    Column('user_id', Integer, primary_key=True),
                    Column('email', String),
                    Column('given_name', String),
                    Column('surname', String),
                    Column('city', String),
                    Column('phone_number', String),
                    Column('profile_description', String),
                    Column('password', String),
                    )

caregiver_table = Table('caregiver', metadata,
                        Column('caregiver_user_id', Integer, primary_key=True),
                        Column('photo', String),
                        Column('gender', String),
                        Column('caregiving_type', String),
                        Column('hourly_rate', Integer),
                        )

member_table = Table('member', metadata,
                     Column('member_user_id', Integer, primary_key=True),
                     Column('house_rules', String),
                     )

address_table = Table('address', metadata,
                      Column('member_user_id', Integer, ForeignKey('MEMBER.member_user_id')),
                      Column('house_number', Integer),
                      Column('street', String),
                      Column('town', String),
                      )

job_table = Table('job', metadata,
                  Column('job_id', Integer, primary_key=True),
                  Column('member_user_id', Integer, ForeignKey('MEMBER.member_user_id')),
                  Column('required_caregiving_type', String),
                  Column('other_requirements', String),
                  Column('date_posted', String),
                  )

job_application_table = Table('job_application', metadata,
                              Column('caregiver_user_id', Integer, ForeignKey('CAREGIVER.caregiver_user_id')),
                              Column('job_id', Integer, ForeignKey('JOB.job_id')),
                              Column('date_applied', String),
                              )

appointment_table = Table('appointment', metadata,
                          Column('appointment_id', Integer, primary_key=True),
                          Column('caregiver_user_id', Integer, ForeignKey('CAREGIVER.caregiver_user_id')),
                          Column('member_user_id', Integer, ForeignKey('MEMBER.member_user_id')),
                          Column('appointment_date', String),
                          Column('appointment_time', String),
                          Column('work_hours', Integer),
                          Column('status', String),
                          )

base_declr = declarative_base()
session_maker = sessionmaker(bind=engine)
session = session_maker()

# 3.1
update_askar_phone_query = update(users_table).where(
    and_(users_table.c.given_name == 'Askar', users_table.c.surname == 'Askarov')).values(
    phone_number='+77771010001')
session.execute(update_askar_phone_query)
session.commit()


# 3.2
update_hourly_rate_query_under_nine = update(caregiver_table).where(caregiver_table.c.hourly_rate < 9).values(
    hourly_rate=(caregiver_table.c.hourly_rate + 0.5))
session.execute(update_hourly_rate_query_under_nine)

update_hourly_rate_percentage_query_by_ten_percent = update(caregiver_table).where(
    caregiver_table.c.hourly_rate >= 9).values(
    hourly_rate=(caregiver_table.c.hourly_rate * 1.1))
session.execute(update_hourly_rate_percentage_query_by_ten_percent)
session.commit()


# 4.1
user_id_bolat = session.query(users_table.c.user_id).filter(
    and_(
        users_table.c.given_name == 'Bolat',
        users_table.c.surname == 'Bolatov'
    )
).scalar()

job_ids_bolat = session.query(job_table.c.job_id).filter(
    job_table.c.member_user_id == user_id_bolat
).all()

job_ids_bolat = [job_id[0] for job_id in job_ids_bolat]

session.query(job_application_table).filter(
    job_application_table.c.job_id.in_(job_ids_bolat)
).delete()

session.query(job_table).filter(job_table.c.member_user_id == user_id_bolat).delete()

session.commit()


# 4.2

turan_member_user_ids = (
    session.query(member_table.c.member_user_id)
    .join(address_table, address_table.c.member_user_id == member_table.c.member_user_id)
    .filter(address_table.c.street == 'Turan')
    .all()
)

turan_member_user_ids = [row[0] for row in turan_member_user_ids]
if turan_member_user_ids:
    session.query(appointment_table).filter(appointment_table.c.member_user_id.in_(turan_member_user_ids)).delete(synchronize_session=False)
    session.query(address_table).filter(address_table.c.member_user_id.in_(turan_member_user_ids)).delete(synchronize_session=False)
    session.query(job_application_table).filter(job_application_table.c.job_id == job_table.c.job_id, job_table.c.member_user_id.in_(turan_member_user_ids)).delete(synchronize_session=False)
    session.query(job_table).filter(job_table.c.member_user_id.in_(turan_member_user_ids)).delete(synchronize_session=False)
    session.query(member_table).filter(member_table.c.member_user_id.in_(turan_member_user_ids)).delete(synchronize_session=False)
    session.commit()
    print("Members living on Turan street deleted.")
else:
    print("No members found in Turan.")

# 5.1
accepted_appointments = text("""
     SELECT
        A.appointment_id,
        CGR.given_name AS caregiver_given_name,
        CGR.surname AS caregiver_surname,
        MEM.given_name AS member_given_name,
        MEM.surname AS member_surname
    FROM
        appointment A
        JOIN users CGR ON A.caregiver_user_id = CGR.user_id
        JOIN users MEM ON A.member_user_id = MEM.user_id
    WHERE
        A.status = 'accepted';
""")

with engine.connect() as connection:
    result = connection.execute(accepted_appointments)
    for row in result:
        print("5.1: ", row['caregiver_name'], row['member_name'])

# 5.2
gentle = text("""
    SELECT job_id
    FROM job
    WHERE LOWER(other_requirements) LIKE '%gentle%';
""")

with engine.connect() as connection:
    result = connection.execute(gentle)
    for row in result:
        print("5.2: ", row[0])

# 5.3
work_hours = text("""
    SELECT
        A.appointment_id,
        A.appointment_date,
        A.appointment_time,
        A.work_hours,
        C.caregiver_user_id,
        C.hourly_rate
    FROM
        appointment A
    JOIN
        caregiver C ON A.caregiver_user_id = C.caregiver_user_id
    WHERE
        C.caregiving_type = 'Baby Sitter';
""")

with engine.connect() as connection:
    result = connection.execute(work_hours)
    for row in result:
        print("5.3: ", row[0], row[1])

# 5.4
no_pets = text("""
    SELECT
        U.given_name,
        U.surname,
        U.city,
        M.house_rules
    FROM
        users U
    JOIN
        member M ON U.user_id = M.member_user_id
    JOIN
        address A ON M.member_user_id = A.member_user_id
    JOIN
        job J ON M.member_user_id = J.member_user_id
    WHERE
        J.required_caregiving_type = 'Elderly Care'
        AND U.city = 'Astana'
        AND M.house_rules = 'No pets';
""")

with engine.connect() as connection:
    result = connection.execute(no_pets)
    for row in result:
        print("5.4: ", row['member_name'])

number_of_applications = text("""
    SELECT
        J.job_id,
        J.member_user_id,
        COUNT(JA.caregiver_user_id) AS num_applicants
    FROM
        JOB J
    JOIN
        JOB_APPLICATION JA ON J.job_id = JA.job_id
    GROUP BY
        J.job_id, J.member_user_id;
""")

with engine.connect() as connection:
    result = connection.execute(number_of_applications)
    print("6.1 Number of applications:", result.rowcount)

# 6_2
total_hours = text("""
    SELECT
        COALESCE(SUM(A.work_hours), 0) AS total_hours_spent
    FROM
        APPOINTMENT A
    JOIN
        CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
    WHERE
        A.status = 'Accepted';
""")

with engine.connect() as connection:
    result = connection.execute(total_hours)
    total_hours_spent = result.scalar()
    print(f"6.2 Total Hours Spent by Caregivers: {total_hours_spent}")

# 6.3
average_pay = text("""
    SELECT
        COALESCE(AVG(C.hourly_rate), 0) AS average_pay
    FROM
        APPOINTMENT A
    JOIN
        CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
    WHERE
        A.status = 'Accepted';
""")

with engine.connect() as connection:
    result = connection.execute(average_pay)
    average_pay = result.scalar()
    print(f"6.3 Average Pay of Caregivers: {average_pay}")

# 6.4
earn_above = text("""
    SELECT
        C.caregiver_user_id,
        C.hourly_rate
    FROM
        CAREGIVER C
    WHERE
        C.hourly_rate > (
            SELECT
                COALESCE(AVG(C1.hourly_rate), 0)
            FROM
                APPOINTMENT A1
            JOIN
                CAREGIVER C1 ON A1.caregiver_user_id = C1.caregiver_user_id
            WHERE
                A1.status = 'Accepted'
        );
""")

with engine.connect() as connection:
    result = connection.execute(earn_above)
    for row in result:
        print(f"6.4 Caregiver ID: {row[0]}, Hourly Rate: {row[1]}")

query_total_cost = text("""
    SELECT
        COALESCE(SUM(A.work_hours * C.hourly_rate), 0) AS total_cost
    FROM
        APPOINTMENT A
    JOIN
        CAREGIVER C ON A.caregiver_user_id = C.caregiver_user_id
    WHERE
        A.status = 'Accepted';
""")

with engine.connect() as connection:
    result = connection.execute(query_total_cost)
    total_cost = result.scalar()
    print(f"7 Total Cost to Pay for Caregivers: {total_cost}")

query_all_job_applications = text("""
    SELECT
        JA.caregiver_user_id,
        JA.job_id,
        JA.date_applied,
        U.given_name AS applicant_given_name,
        U.surname AS applicant_surname,
        J.required_caregiving_type,
        J.other_requirements,
        M.member_user_id,
        M.house_rules
    FROM
        job_application JA
    JOIN
        caregiver C ON JA.caregiver_user_id = C.caregiver_user_id
    JOIN
        users U ON JA.caregiver_user_id = U.user_id
    JOIN
        job J ON JA.job_id = J.job_id
    JOIN
        member M ON J.member_user_id = M.member_user_id;
""")

with engine.connect() as connection:
    result_all_job_applications = connection.execute(query_all_job_applications)
    for row in result_all_job_applications:
        print(f"""
            Caregiver ID: {row[0]},
            Job ID: {row[1]},
            Date Applied: {row[2]},
            Applicant Name: {row[3]} {row[4]},
            Caregiving Type: {row[5]},
            Other Requirements: {row[6]},
            Member ID: {row[7]},
            House Rules: {row[8]}
        """)

session.commit()
session.close()
