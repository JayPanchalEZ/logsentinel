from processor_regex import classify_with_regex
from processor_llm import classify_with_llm
from processor_bert import classify_with_bert
import pandas as pd
import re
from openpyxl.styles import Alignment, Font

ip_fail_count = {}

STANDARD_LABELS = [
    "failed_login",
    "brute_force_attempt",
    "possible_attack",
    "suspicious_activity",
    "normal_activity",
    "system_event"
]

LABEL_MAPPING = {
    # Old / inconsistent → new
    "security alert": "suspicious_activity",
    "http status": "system_event",
    "workflow error": "system_event",
    "deprecation warning": "system_event",
    "user action": "normal_activity",
    "system notification": "system_event"
}

def normalize_label(label):
    if not label:
        return "suspicious_activity"

    label = label.strip().lower()

    # If already correct
    if label in STANDARD_LABELS:
        return label

    # Map old labels
    if label in LABEL_MAPPING:
        return LABEL_MAPPING[label]

    # Default fallback
    return "suspicious_activity"


def detect_brute_force(log_message):
    ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', log_message)
    if ip_match:
        ip = ip_match.group()
        if any(keyword in log_message.lower() for keyword in [
            "failed",
            "login failed",
            "authentication failed"
        ]):
            ip_fail_count[ip] = ip_fail_count.get(ip, 0) + 1
            if ip_fail_count[ip] > 3:
                return "brute_force_attempt"
    return None

def classify(logs):
    labels = []
    for source, log_message in logs:
        raw_label = classify_log(source, log_message)

        label = normalize_label(raw_label)

        if label in ["brute_force_attempt", "possible_attack", "suspicious_activity"]:
            print(f"ALERT: {label.upper()} detected -> {log_message}")

        labels.append(label)
    return labels

def classify_log(source, log_message):
    bf_label = detect_brute_force(log_message)
    if bf_label:
        return bf_label

    if source == "LegacyCRM":
        label = classify_with_llm(log_message)
    else:
        label = classify_with_regex(log_message)
        if label is None:
            label = classify_with_bert(log_message)

        if label is None:
            label = "suspicious_activity"
    return label

def classify_csv(input_file):
    global ip_fail_count
    ip_fail_count = {}
    df = pd.read_csv(input_file)
    df['target_label'] = classify(list(zip(df['source'], df['log_message'])))

    print("\n--Log Summary--")
    print(df['target_label'].value_counts())


    threats = df[df['target_label'].isin([
        "brute_force_attempt",
        "possible_attack",
        "suspicious_activity"
    ])]

    print("\nTotal Threats Detected:", len(threats))
    print("\n" + "=" * 50)
    print("--Suspicious Logs--")
    print("=" * 50)
    print(threats[['log_message', 'target_label']])
    output_file = "resources/security_report.xlsx"

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:

        # 📄 Sheet 1: All Logs
        df.to_excel(writer, sheet_name='All Logs', index=False)
        workbook = writer.book
        worksheet = writer.sheets['All Logs']

        # ✅ Auto column width + wrap text
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter

            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
                    cell.alignment = Alignment(wrap_text=True)

            worksheet.column_dimensions[col_letter].width = min(max_length + 2, 50)

        # ✅ Bold header

        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        # 🚨 Sheet 2: Threat Logs
        threats.to_excel(writer, sheet_name='Threat Logs', index=False)
        worksheet2 = writer.sheets['Threat Logs']

        for col in worksheet2.columns:
            max_length = 0
            col_letter = col[0].column_letter

            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
                    cell.alignment = Alignment(wrap_text=True)

            worksheet2.column_dimensions[col_letter].width = min(max_length + 2, 50)

        for cell in worksheet2[1]:
            cell.font = Font(bold=True)

        # 📊 Sheet 3: Summary
        summary = df['target_label'].value_counts().reset_index()
        summary.columns = ['Label', 'Count']
        summary.to_excel(writer, sheet_name='Summary', index=False)

        worksheet3 = writer.sheets['Summary']
        for cell in worksheet3[1]:
            cell.font = Font(bold=True)
        for col in worksheet3.columns:
            max_length = 0
            col_letter = col[0].column_letter

            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
                    cell.alignment = Alignment(wrap_text=True)

            worksheet3.column_dimensions[col_letter].width = min(max_length + 2, 50)

        # Bold header
        for cell in worksheet3[1]:
            cell.font = Font(bold=True)


if __name__ == '__main__':
    classify_csv("resources/test.csv")

    # logs = [
    #     ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    #     ("BillingSystem", "User User12345 logged in."),
    #     ("AnalyticsEngine", "File data_6957.csv uploaded successfully by user User265."),
    #     ("AnalyticsEngine", "Backup completed successfully."),
    #     ("ModernHR", "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400"),
    #     ("ModernHR", "Admin access escalation detected for user 9429"),
    #     ("LegacyCRM", "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."),
    #     ("LegacyCRM", "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."),
    #     ("LegacyCRM", "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality."),
    #     ("LegacyCRM", " The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025")
    # ]
    # labels = classify(logs)
    #
    # for log, label in zip(logs, labels):
    #     print(log[0], "->", label)\
    # classified_logs = classify(logs)
    # print(classified_logs)