import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

import api.models.v1.emails as emails


def create_email_template(subject: str, body: str) -> str:
    """Create a styled HTML email template using the app's design system"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap" rel="stylesheet">
    <style>
        :root {{
            /* theme is modern blue and purple */
            --primary: #4a90e2;
            --secondary: #8e44ad;
            --primary-light: #74a9f7;
            --secondary-light: #b47ece;
            --primary-accent: #a8cbf0;
            --secondary-accent: #d1a3e8;
            --primary-dark: #2c5aa0;
            --secondary-dark: #6a1b9a;
            --primary-bg: #e3f2fd;
            --secondary-bg: #f3e5f5;

            /* danger colors */
            --danger-red: #ff6b6b;
            --danger-dark: #e74c3c;
            --danger-light: #ffebeb;
            --danger-accent: #ffd8d8;

            /* grey colors */
            --grey-100: #f5f5f5;
            --grey-200: #e5e5e5;
            --grey-300: #d4d4d4;
            --grey-600: #525252;
            --grey-800: #262626;

            /* subtle variants */
            --subtle-primary: rgba(74, 144, 226, 0.1);
            --subtle-secondary: rgba(142, 68, 173, 0.1);
            --subtle-danger: rgba(255, 107, 107, 0.1);
            --subtle-primary-hover: rgba(74, 144, 226, 0.15);
            --subtle-secondary-hover: rgba(142, 68, 173, 0.15);
            --subtle-danger-hover: rgba(255, 107, 107, 0.15);

            /* border radius */
            --border-radius-standard: 6px;
            --border-radius-full: 9999px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Space Grotesk', Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
            line-height: 1.5;
            font-weight: 400;
            background-color: var(--grey-100);
            padding: 20px;
        }}

        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border-radius: var(--border-radius-standard);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .email-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 32px 24px;
            text-align: center;
        }}

        .email-logo {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 8px;
        }}
        
        .email-logo img {{
            height: 32px;
            width: 32px;
        }}
        
        .email-logo-text {{
            font-size: 28px;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        .email-tagline {{
            font-size: 16px;
            opacity: 0.9;
            font-weight: 300;
        }}

        .email-content {{
            padding: 32px 24px;
        }}

        .email-subject {{
            font-size: 24px;
            font-weight: 600;
            color: var(--grey-800);
            margin-bottom: 16px;
            line-height: 1.3;
        }}

        .email-body {{
            font-size: 16px;
            color: var(--grey-600);
            line-height: 1.6;
            margin-bottom: 32px;
        }}

        .email-body p {{
            margin-bottom: 16px;
        }}

        .email-body p:last-child {{
            margin-bottom: 0;
        }}

        .email-footer {{
            background-color: var(--grey-100);
            padding: 24px;
            border-top: 1px solid var(--grey-200);
            text-align: center;
        }}

        .unsubscribe-button {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 24px;
            font-size: 14px;
            color: var(--grey-600);
            background-color: white;
            border: 1px solid var(--grey-300);
            border-radius: var(--border-radius-standard);
            text-decoration: none;
            font-family: inherit;
            font-weight: 400;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            margin-bottom: 16px;
        }}

        .unsubscribe-button:hover {{
            background-color: var(--grey-100);
            border-color: var(--grey-400);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }}

        .email-disclaimer {{
            font-size: 12px;
            color: var(--grey-600);
            line-height: 1.4;
        }}

        .company-info {{
            margin-top: 12px;
            font-size: 11px;
            color: var(--grey-600);
        }}

        /* Responsive design */
        @media screen and (max-width: 640px) {{
            body {{
                padding: 10px;
            }}
            
            .email-header {{
                padding: 24px 16px;
            }}
            
            .email-content {{
                padding: 24px 16px;
            }}
            
            .email-footer {{
                padding: 16px;
            }}
            
            .email-subject {{
                font-size: 20px;
            }}
            
            .email-logo {{
                flex-direction: column;
                gap: 8px;
            }}
            
            .email-logo-text {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <header class="email-header">
            <div class="email-logo">
                <div class="email-logo-text">AM/A</div>
            </div>
            <div class="email-tagline">Your scheduling companion</div>
        </header>
        
        <main class="email-content">
            <h1 class="email-subject">{subject}</h1>
            <div class="email-body">
                {body}
            </div>
            - AM/A
        </main>
        
        <footer class="email-footer">
            <a href="#" class="unsubscribe-button">
                Unsubscribe from emails
            </a>
            <div class="email-disclaimer">
                You're receiving this email because you have an account with AMIA.
                If you no longer wish to receive these emails, you can unsubscribe using the button above.
            </div>
            <div class="company-info">
                AM/A - Making scheduling effortless<br>
                © 2025 AMIA. All rights reserved.
            </div>
        </footer>
    </div>
</body>
</html>"""


class EmailsService:
    def __init__(self) -> None:
        self.ses_client = boto3.client("ses", region_name="us-east-2")
        self.source_email = "amia@amiavailable.com"
        self.source_name = "AM/A"

    async def send_email(
        self, *, to: list[str], subject: str, body: str
    ) -> emails.SendEmailResponse:
        """Send an email using AWS SES with styled HTML template"""
        try:
            # Create styled HTML email
            html_body = create_email_template(subject, body)

            response = self.ses_client.send_email(
                Source=f"{self.source_name} <{self.source_email}>",
                Destination={"ToAddresses": to},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {
                        "Html": {"Data": html_body},
                        "Text": {"Data": body},  # Keep plain text as fallback
                    },
                },
            )

            message_id = response.get("MessageId")
            return emails.SendEmailResponse(
                message="Email sent successfully", message_id=message_id
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]

            if error_code == "MessageRejected":
                raise HTTPException(
                    status_code=400, detail=f"Email rejected: {error_message}"
                )
            elif error_code == "MailFromDomainNotVerified":
                raise HTTPException(status_code=500, detail="Email domain not verified")
            elif error_code == "ConfigurationSetDoesNotExist":
                raise HTTPException(status_code=500, detail="Email configuration error")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Failed to send email: {error_message}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Unexpected error sending email: {str(e)}"
            )
