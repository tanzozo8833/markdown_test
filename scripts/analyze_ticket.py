import os
import sys
from jira import JIRA
from google import genai

def main():
    # 1. Đọc biến môi trường (GitHub sẽ truyền vào đây)
    jira_url = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    ticket_id = os.getenv('TICKET_ID')
    gemini_key = os.getenv('GEMINI_API_KEY')

    # Log kiểm tra (Không in Token để bảo mật)
    print(f"Connecting to Jira: {jira_url}")
    print(f"Processing Ticket: {ticket_id}")

    if not jira_url or "atlassian.net" not in jira_url:
        print("LỖI: JIRA_SERVER không hợp lệ hoặc đang bị để là localhost!")
        sys.exit(1)

    try:
        # 2. Khởi tạo Jira
        jira = JIRA(server=jira_url, basic_auth=(jira_email, jira_token))
        
        # 3. Lấy data ticket
        issue = jira.issue(ticket_id)
        summary = issue.fields.summary
        desc = issue.fields.description or "No description"
        
        # 4. Gọi Gemini (Dùng thư viện mới google-genai)
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model='gemini-3.1-pro-preview',
            contents=f"Phân tích ticket sau: {summary}. Nội dung: {desc}"
        )

        # 5. Comment kết quả
        jira.add_comment(ticket_id, f"🤖 **AI Analysis:**\n\n{response.text}")
        print("Thành công!")

    except Exception as e:
        print(f"Lỗi thực thi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
