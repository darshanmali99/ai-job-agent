diff --git a/app.py b/app.py
index 72f19683b43fcb2bfec93aa32a7e4e16643c4d20..b513821607f20489ed489f70df2e1da202e28d5f 100644
--- a/app.py
+++ b/app.py
@@ -1,155 +1,37 @@
-You are a Senior Full-Stack Developer + AI Engineer with 10+ years of experience building scalable, lightweight, and production-ready web systems for industrial businesses.
+import streamlit as st
 
-Your task is to implement a COMPLETE LEAD MANAGEMENT + AI CHATBOT SYSTEM for an industrial website (Mahavir Industries) with focus on PERFORMANCE, SIMPLICITY, and PROFESSIONAL QUALITY.
+from src.agent import get_response
 
-========================
-🎯 CORE OBJECTIVE
-========================
-Build a system where:
-- User submits form or chatbot input
-- Data is stored securely
-- Instant notification is sent (Email + optional WhatsApp)
-- Website remains FAST and LIGHTWEIGHT
 
-Avoid over-engineering. Optimize for performance.
+st.set_page_config(page_title="AI Finance Assistant", page_icon="💹")
+st.title("💹 AI Finance Assistant")
+st.caption("Ask finance questions and get concise answers.")
 
-========================
-⚙️ SYSTEM DESIGN (LIGHTWEIGHT)
-========================
-Frontend:
-- Existing HTML/CSS/JS (no heavy frameworks required)
-- Minimal JS (vanilla or lightweight fetch)
+if "chat_history" not in st.session_state:
+    st.session_state.chat_history = []
 
-Backend:
-- Node.js + Express (simple REST API)
+for item in st.session_state.chat_history:
+    with st.chat_message(item["role"]):
+        st.markdown(item["content"])
 
-Database:
-- MongoDB Atlas (cloud, lightweight usage)
+user_query = st.chat_input("Ask a finance question...")
 
-========================
-📊 DATA FLOW
-========================
-User → Form/Chatbot → API → Database → Notification → Response
+if user_query:
+    st.session_state.chat_history.append({"role": "user", "content": user_query})
+    with st.chat_message("user"):
+        st.markdown(user_query)
 
-========================
-🧠 DATABASE SCHEMA
-========================
-Fields:
-- name (required)
-- phone (required)
-- email (optional)
-- message / requirement
-- source (form / chatbot)
-- createdAt (auto timestamp)
+    with st.chat_message("assistant"):
+        with st.spinner("Thinking..."):
+            try:
+                result = get_response(user_query)
+                answer = result.get("answer", "I could not generate an answer.")
+            except Exception as exc:
+                answer = (
+                    "Sorry, I ran into an error while generating a response. "
+                    f"Details: `{exc}`"
+                )
 
-Keep schema simple and efficient.
+        st.markdown(answer)
 
-========================
-📩 EMAIL NOTIFICATION
-========================
-Use Nodemailer:
-
-Send to:
-- darsham765gmail.com
-
-Format:
-- Clean structured email
-- Clearly readable lead details
-
-========================
-📲 WHATSAPP NOTIFICATION (OPTIONAL BUT INCLUDED)
-========================
-- Use WhatsApp API (Twilio / Meta API)
-- Send short alert:
-  “New Lead: Name, Phone”
-
-Make this optional (toggle-based, not mandatory).
-
-========================
-🤖 AI CHATBOT (LIGHT + SMART)
-========================
-Requirements:
-- Human-like responses (simple, not heavy AI model)
-- Predefined + dynamic replies
-- Fast loading (no large libraries)
-
-Flow:
-1. Greet user
-2. Ask requirement
-3. Collect:
-   - Name
-   - Phone
-   - Email (optional)
-4. Send data to backend
-
-UI:
-- Floating chat widget
-- Clean, minimal design
-- Mobile-friendly
-
-========================
-📊 ADMIN DASHBOARD (BASIC)
-========================
-- Simple protected route (/admin)
-- Display stored leads in table
-- No heavy UI frameworks
-- Basic authentication (simple login)
-
-========================
-🔐 SECURITY (IMPORTANT)
-========================
-- Use .env for credentials
-- Validate inputs
-- Prevent empty/spam submissions
-- Enable CORS properly
-
-========================
-⚡ PERFORMANCE RULES
-========================
-- Keep bundle size small
-- Avoid heavy libraries
-- Optimize API responses
-- Fast loading chatbot
-
-========================
-💻 FRONTEND INTEGRATION
-========================
-- Use fetch API
-- Show:
-   - Loading state
-   - Success message
-- No page reload
-
-========================
-📦 OUTPUT REQUIRED
-========================
-Provide:
-
-1. Clean backend code (server.js)
-2. MongoDB schema
-3. Email setup
-4. API endpoint (/contact)
-5. Chatbot JS (lightweight)
-6. Basic admin panel code
-7. Deployment steps (Render + MongoDB Atlas)
-
-========================
-💎 FINAL EXPECTATION
-========================
-Think like:
-- Senior engineer
-- Performance optimizer
-- Product builder
-
-Build:
-- Fast
-- Clean
-- Scalable
-- Professional
-
-Avoid:
-- Over-complex architecture
-- Heavy frameworks
-- Unnecessary dependencies
-
-Deliver a REAL, WORKING, LIGHTWEIGHT SYSTEM.
\ No newline at end of file
+    st.session_state.chat_history.append({"role": "assistant", "content": answer})
