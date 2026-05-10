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
index_view_url = "core:index-view"
about_view_url = "core:about-view"
course_view_url = "course:course-index"
create_course_view_url = "course:create-course"
notification_view_url = "notification"
find_friend_view_url = "find-friends"
login_view_url = "account_login"
