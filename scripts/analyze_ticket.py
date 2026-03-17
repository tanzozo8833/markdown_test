import os
import google.generativeai as genai
from jira import JIRA

# 1. Cấu hình kết nối
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
jira = JIRA(
    server=os.getenv('JIRA_SERVER'), 
    basic_auth=(os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
)

def call_gemini(content):
    # Sử dụng bản preview như bạn yêu cầu
    model = genai.GenerativeModel('gemini-1.5-pro') # Hoặc 'gemini-2.0-flash-exp'
    
    prompt = f"""
    Bạn là một siêu trí tuệ nhân tạo chuyên về phân tích hệ thống.
    Nội dung từ Jira: "{content}"
    
    Nhiệm vụ:
    1. PHÂN LOẠI: Phản hồi từ 'Khách hàng' hay 'Dev'.
    2. CHIẾT XUẤT BUG: Danh sách bug, nguyên nhân, file liên quan.
    3. TRÌNH BÀY: Định dạng Markdown cao cấp, có Table và Checklist.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    ticket_id = os.getenv('TICKET_ID')
    if not ticket_id:
        print("Không nhận được TICKET_ID từ Jira.")
        return

    print(f"Đang xử lý ticket: {ticket_id}")

    # 2. Lấy dữ liệu từ Jira
    issue = jira.issue(ticket_id)
    summary = issue.fields.summary
    description = issue.fields.description or ""
    comments = jira.comments(issue)
    last_comment = comments[-1].body if comments else ""

    data_input = f"Title: {summary}\nDesc: {description}\nLast Comment: {last_comment}"

    # 3. Gọi Gemini phân tích
    try:
        result = call_gemini(data_input)
        
        # 4. Ghi kết quả ngược lại Jira để User xem được luôn
        jira.add_comment(ticket_id, f"--- 🤖 GEMINI ANALYSIS ---\n\n{result}")
        print("Đã đẩy kết quả lên Jira thành công.")
        
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()
