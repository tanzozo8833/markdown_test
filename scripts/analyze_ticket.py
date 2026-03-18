import os
import sys
import google.generativeai as genai
from jira import JIRA

def main():
    # 1. Lấy biến môi trường từ GitHub Action
    jira_url = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    ticket_id = os.getenv('TICKET_ID')
    gemini_key = os.getenv('GEMINI_API_KEY')

    if not all([jira_url, jira_email, jira_token, ticket_id, gemini_key]):
        print("❌ LỖI: Thiếu cấu hình Secrets trên GitHub.")
        sys.exit(1)

    try:
        # 2. Kết nối Jira Cloud
        jira = JIRA(server=jira_url, basic_auth=(jira_email, jira_token))
        issue = jira.issue(ticket_id)
        
        summary = issue.fields.summary
        description = issue.fields.description or "Không có mô tả chi tiết."
        
        # Lấy lịch sử comment để AI hiểu ngữ cảnh trao đổi
        comments = jira.comments(issue)
        comment_history = "\n".join([f"- {c.author.displayName}: {c.body}" for c in comments[-3:]])

        # 3. Cấu hình Gemini với Model 3.1 Pro Preview
        genai.configure(api_key=gemini_key)
        
        # SỬ DỤNG MODEL CHÍNH XÁC TỪ DANH SÁCH BẠN QUÉT ĐƯỢC
        model = genai.GenerativeModel('gemini-2.5-flash')

        prompt = f"""
        Bạn là một Chuyên gia phân tích hệ thống cao cấp (Senior Business Analyst & Developer).
        Hãy thực hiện phân tích sâu ticket Jira sau:

        [THÔNG TIN TICKET]
        - Mã ticket: {ticket_id}
        - Tiêu đề: {summary}
        - Mô tả: {description}
        - Thảo luận gần đây: 
        {comment_history}

        [NHIỆM VỤ]
        1. PHÂN LOẠI CHI TIẾT: (Ví dụ: Lỗi logic, Yêu cầu UI/UX, Cải thiện hiệu suất...).
        2. ĐÁNH GIÁ MỨC ĐỘ ƯU TIÊN: Dựa trên nội dung, hãy đề xuất độ ưu tiên (Low/Medium/High/Urgent).
        3. PHÂN TÍCH KỸ THUẬT:
           - Tóm tắt vấn đề cốt lõi.
           - Dự đoán các thành phần/file code có thể liên quan.
           - Đề xuất hướng giải quyết (Step-by-step).
        4. TRÌNH BÀY: Định dạng Markdown chuyên nghiệp, sử dụng Table cho danh sách task và Bold cho các lưu ý quan trọng.

        Ngôn ngữ phản hồi: Tiếng Việt.
        """

        print(f"🧠 Đang sử dụng Gemini 3.1 Pro phân tích {ticket_id}...")
        
        # 4. Gọi AI
        response = model.generate_content(prompt)
        ai_response = response.text

        # 5. Đăng kết quả lên Jira
        header = f"## 🤖 PHÂN TÍCH HỆ THỐNG (AI GEMINI 3.1 PRO)\n\n"
        footer = f"\n\n---\n*Phân tích được thực hiện tự động bởi model: {model.model_name}*"
        
        jira.add_comment(ticket_id, header + ai_response + footer)
        
        print(f"✅ Đã đăng phân tích lên ticket {ticket_id} thành công!")

    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
