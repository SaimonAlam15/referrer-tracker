MODEL_1_TRAINING_DATA_QUERY = """
    with registered_referrers as (
        select
            ref.ID,
            ref.JOB_ID,
            can.EMAIL as CANDIDATE_EMAIL
        from IREFERRALS ref
        join CANDIDATES can 
            on ref.CANDIDATE_ID = can.ID
        where CANDIDATE_EMAIL is null
        ),

        guest_referrers as (
        select
            ID,
            JOB_ID,
            CANDIDATE_EMAIL
        from IREFERRALS
        where CANDIDATE_EMAIL is not null
        ),

        referrers as (
        select * from guest_referrers
        UNION
        select * from registered_referrers
        )
        
    select  
            c.ID,
            c.EMAIL,
            c.FIRST_NAME,
            c.LAST_NAME,
            c.SOURCE,
            c.CAREER_LEVEL,
            c.TITLE_OF_LAST_POSITION,
            c.FIELD_OF_EXPERTISE,
            c.COUNTRY as candidate_country,
            c.STATE as candidate_state,
            c.CITY as candidate_city,
            j.ID as JOBID,
            j.industry,
            j.country as job_country,
            j.city as job_city,
            j.state as job_state,
            j.remote_job,
            j.location,
            j.required_skills,
            (
                case when DATEDIFF(day, c.last_activity_time, current_date()) <= 60 then 1.0::float
                else 0.0::float
                end
            )
            as RECENTLY_ACTIVE,
            (
                case when r.CANDIDATE_EMAIL is null then 0.0::float
                else 1.0::float
                end
            ) as TARGET
        from referrers r
        right join CANDIDATES c
            on r.CANDIDATE_EMAIL = c.EMAIL
        left join JOB_OPENINGS j
            on r.JOB_ID = j.ID
        order by 1
    """


MODEL_2_TRAINING_DATA_QUERY = """
    with registered_referrers as (
    select
        ref.ID,
        can.EMAIL as CANDIDATE_EMAIL
    from IREFERRALS ref
    join CANDIDATES can 
        on ref.CANDIDATE_ID = can.ID
    where CANDIDATE_EMAIL is null
    ),
    guest_referrers as (
    select
        ID,
        CANDIDATE_EMAIL
    from IREFERRALS
    where CANDIDATE_EMAIL is not null
    ),
    referrers as (
    select distinct CANDIDATE_EMAIL from guest_referrers
    UNION
    select distinct CANDIDATE_EMAIL from registered_referrers
    )
    
    select
        c.ID,
        c.FIRST_NAME,
        c.LAST_NAME,
        c.EMAIL,
        c.SOURCE,
        c.CAREER_LEVEL,
        c.TITLE_OF_LAST_POSITION,
        c.FIELD_OF_EXPERTISE,
        (
            case when DATEDIFF(day, c.last_activity_time, current_date()) <= 60 then 1.0::float
            else 0.0::float
            end
        )
        as RECENTLY_ACTIVE,
        (
            case when r.CANDIDATE_EMAIL is null then 0.0::float
            else 1.0::float
            end
        ) as TARGET
    from referrers r
    right join Candidates c
        on r.CANDIDATE_EMAIL = c.EMAIL
"""


TEST_DATA_QUERY = """
        select
        ID::string as ID,
        EMAIL,
        FIRST_NAME,
        LAST_NAME,
        CITY,
        STATE,
        SOURCE,
        CAREER_LEVEL,
        NAME_OF_LAST_COMPANY,
        TITLE_OF_LAST_POSITION,
        FIELD_OF_EXPERTISE,
        (
            case when DATEDIFF(day, last_activity_time, current_date()) <= 60 then 1.0::float
            else 0.0::float
            end
        )
        as RECENTLY_ACTIVE,
        (
            case when ID in (select CANDIDATEID from IREFERRALS)
            or EMAIL in (select CANDIDATE_EMAIL from IREFERRALS)
            then 1.0::float
            else 0.0::float
            end
        ) as TARGET
    from Candidates
    """


DATA_ANALYSIS_QUERY = """
    with registered_referrers as (
        select
            ref.ID,
            ref.JOB_ID,
            can.EMAIL as CANDIDATE_EMAIL
        from IREFERRALS ref
        join CANDIDATES can
            on ref.CANDIDATE_ID = can.ID
        where CANDIDATE_EMAIL is null
        ),

        guest_referrers as (
        select
            ID,
            JOB_ID,
            CANDIDATE_EMAIL
        from IREFERRALS
        where CANDIDATE_EMAIL is not null
        ),

        referrers as (
        select * from guest_referrers
        UNION
        select * from registered_referrers
        )

    select
            c.ID,
            c.EMAIL,
            c.FIRST_NAME,
            c.LAST_NAME,
            c.SOURCE,
            c.CAREER_LEVEL,
            c.name_of_last_company,
            c.TITLE_OF_LAST_POSITION,
            c.FIELD_OF_EXPERTISE,
            c.COUNTRY as candidate_country,
            c.STATE as candidate_state,
            c.CITY as candidate_city,
            j.ID as JOBID,
            j.industry,
            j.country as job_country,
            j.city as job_city,
            j.state as job_state,
            j.remote_job,
            j.location,
            (
                case when DATEDIFF(day, c.last_activity_time, current_date()) <= 60 then 'Yes'
                else 'No'
                end
            )
            as RECENTLY_ACTIVE
        from referrers r
        inner join CANDIDATES c
            on r.CANDIDATE_EMAIL = c.EMAIL
        inner join JOB_OPENINGS j
            on r.JOB_ID = j.ID
        order by 1
    """