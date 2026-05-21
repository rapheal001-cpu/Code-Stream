USER_ROLE = [
    ("", "--Select Role--"),
    ("student", "Student"),
    ("instructor", "Instructor"),
]


PAYMENT_TYPE = [
    ("", "--Select Payment--"),
    ("withdraw", "Withdraw"),
    ("income", "Income"),
]


STATUS_TYPE = [
    ("", "--Select Status--"),
    ('success', 'Success'),
    ('failed', 'Failed'),
    ('canceled', 'Canceled'),
]


role_selection = ["student", "instructor"]


# ==========
# Core Urls
# ==========
index_view_url = "index-view"
about_view_url = "about-view"


# ===========
# Course Urls
# ===========
course_view_url = "course-index-view"
create_course_view_url = "create-course-view"
create_course_done_view_url = "create-course-done-view"
update_course_done_view_url = "update-course-done-view"
notification_view_url = "notification-view"


# ===========
# Accounts Urls
# ===========
login_view_url = "account_login"
setting_view_url = "settings-view"
