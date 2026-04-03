import re
def classify_with_regex(log_message):
    regex_patterns = {
        r"failed login|login failed|authentication failed": "failed_login",
        r"multiple login failures": "brute_force_attempt",
        r"unauthorized access|access denied": "possible_attack",
        r"IP .* blocked": "suspicious_activity",
        r"User User\d+ logged (in|out).": "normal_activity",
        r"Backup (started|ended) at .*": "system_event",
        r"Backup completed successfully.": "system_event",
        r"System updated to version .*": "system_event",
        r"File .* uploaded successfully by user .*": "system_event",
        r"Disk cleanup completed successfully.": "system_event",
        r"System reboot initiated by user .*": "system_event",
        r"Account with ID .* created by .*": "normal_activity",
        r"brute force attack": "brute_force_attempt",
        r"suspicious login attempt": "suspicious_activity",
        r"failed authentication": "failed_login",
    }
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message, re.IGNORECASE):
            return label
    return None


# if __name__ == "__main__":
#     print(classify_with_regex("User User123 logged in."))
#     print(classify_with_regex("Backup started at 2023-01-01 00:00:00."))
#     print(classify_with_regex("System updated to version 1.0."))
#     print(classify_with_regex("Disk cleanup completed successfully."))
#     print(classify_with_regex("Account with ID 123 created by user User456."))
#     print(classify_with_regex("Kal aana"))