# ==========================================================
# === KHUNG CHAT VỚI GEMINI (bổ sung mới, giữ nguyên các phần khác)
# ==========================================================

st.divider()
st.header("💬 Chat với Gemini AI")

# Tạo session lưu hội thoại
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị hội thoại trước đó
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập câu hỏi chat
user_input = st.chat_input("Nhập câu hỏi của bạn về tài chính, phân tích dữ liệu hoặc bất kỳ nội dung nào...")

if user_input:
    # Hiển thị tin nhắn người dùng
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Gọi API Gemini để phản hồi
    api_key = st.secrets.get("GEMINI_API_KEY")
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            model_name = "gemini-2.5-flash"

            # Gửi nội dung người dùng
            with st.chat_message("assistant"):
                with st.spinner("Gemini đang phản hồi..."):
                    response = client.models.generate_content(
                        model=model_name,
                        contents=f"Người dùng hỏi: {user_input}"
                    )
                    bot_reply = response.text
                    st.markdown(bot_reply)

            # Lưu phản hồi vào lịch sử hội thoại
            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            st.error(f"Lỗi khi kết nối Gemini: {e}")
    else:
        st.error("Không tìm thấy GEMINI_API_KEY trong Secrets. Vui lòng cấu hình trước khi sử dụng.")
