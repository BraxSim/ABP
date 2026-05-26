from __future__ import annotations

TEMPLATES = {
    "reference_learning": {
        "subject": "Re: {original_subject}",
        "body": """Hi {name},

Here is the material for reference and learning purposes only. I hope it helps you understand the general structure and coding style.

Please do not copy or reuse any part of it in your own assignment, as that could cause academic integrity issues.

Best,
Zewen"""
    },

    "paid_user_support": {
        "subject": "Re: {original_subject}",
        "body": """Hi {name},

Thanks for reaching out. I can help you with this based on your current {plan} access.

Please send me the specific question or file you would like me to review, and I will focus on giving guidance, structure, and explanation rather than directly completing the work for you.

Best,
Zewen"""
    },

    "not_paid_or_expired": {
        "subject": "Re: {original_subject}",
        "body": """Hi {name},

Thanks for your message. At the moment, I can only provide limited general guidance because your access is currently not marked as active.

If you think this is a mistake, please let me know and I can check it.

Best,
Zewen"""
    },

    "customer_profile_link": {
        "subject": "Re: {original_subject}",
        "body": """Hi {name},

Thanks for your message.

Here is your personal profile link:
{profile_link}

Please only access your own profile. If anything looks incorrect, reply to this email and we will check it manually.

Best,
Zewen"""
    }
}
