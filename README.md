# Approval-Based Profile Link Email Bot

这个版本实现：

1. 从 Gmail 读取未读客户邮件。
2. 用客户邮箱去 Google Sheet 匹配客户资料。
3. 从 Sheet 读取客户个人资料链接，例如 `profile_link`。
4. 不直接发给客户；先发审批邮件给员工。
5. 员工回复 `APPROVE <Approval ID>` 后，系统才把资料链接邮件发给客户。
6. 员工回复 `REJECT <Approval ID>` 后，不发送客户邮件。
7. 所有已发送记录写入 `sent_log.json`，待审批记录写入 `pending_approvals.json`。

## Google Sheet 表头

至少建议：

```text
email,name,plan,paid_status,expiry_date,profile_link
```

默认 range 已改为：

```text
users!A:F
```

## .env 示例

```env
EMAIL_ADDRESS=your_bot_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password

IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465

GOOGLE_SHEET_ID=你的sheet id
GOOGLE_SHEET_RANGE=users!A:F
GOOGLE_CREDENTIALS_JSON=credentials.json

EMPLOYEE_APPROVAL_EMAIL=employee@example.com

DRY_RUN=true
AUTO_SEND_ONLY_KNOWN_USERS=true
MAX_EMAILS_PER_RUN=5
DAILY_SEND_LIMIT=20
MARK_AS_READ_AFTER_PROCESS=false
```

## 安装

```bash
pip install -r requirements.txt
```

## 第一次授权 Google Sheet

项目根目录放入 `credentials.json`，然后运行：

```bash
python main.py
```

第一次会弹出 Google OAuth 授权，授权成功后会生成 `token.json`。

## 安全测试流程

先保持：

```env
DRY_RUN=true
```

然后：

1. 用测试客户邮箱给 bot 发一封邮件。
2. 运行 `python main.py`。
3. 检查终端是否打印了审批邮件内容，但没有真正发送。
4. 确认无误后改成 `DRY_RUN=false`。
5. 再运行一次，让系统真正给员工发审批邮件。
6. 员工回复 `APPROVE ABCD1234`。
7. 再运行 `python main.py`，系统会读取员工同意回复，再发给客户。

注意：这个脚本不是后台服务。要自动化，需要用 cron、GitHub Actions、服务器定时任务或云函数定时运行。
