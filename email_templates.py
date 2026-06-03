PHOTO_HERO_IMAGE_URL = "https://YOUR_PHOTO_HERO_IMAGE_URL.png"
TRACK_HERO_IMAGE_URL = "https://YOUR_TRACK_HERO_IMAGE_URL.png"

LOGO_URL = "https://i.ibb.co/qYP382xc/Mask-group.png"


def clean_url(url: str) -> str:
    """
    Make sure email buttons use a valid clickable URL.
    Gmail/Outlook often won't treat links without https:// as clickable.
    """
    url = (url or "").strip()

    if not url:
        return ""

    if url.startswith("http://") or url.startswith("https://"):
        return url

    return "https://" + url


def get_customer_name(order: dict) -> str:
    """
    Supports both old and new sheet columns.
    Priority:
    1. Cust_First
    2. Cust_Full first word
    3. there
    """
    first = (order.get("Cust_First") or "").strip()
    if first:
        return first

    full = (order.get("Cust_Full") or "").strip()
    if full:
        return full.split()[0]

    return "there"


def render_button(url: str, label: str, color: str) -> str:
    """
    Email-safe button.
    Use table + <a>, not <button> or onclick.
    """
    if not url:
        return ""

    return f"""
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 32px 0; border-collapse:collapse;">
  <tr>
    <td align="left" style="padding:0; margin:0;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
        <tr>
          <td bgcolor="{color}" style="border-radius:4px; mso-padding-alt:16px 34px;">
            <a href="{url}" target="_blank" rel="noopener"
               style="display:inline-block; padding:16px 34px; font-size:15px; line-height:18px; font-weight:700; font-family:Arial, Helvetica, sans-serif; color:#ffffff; text-decoration:none; border-radius:4px;">
              {label}
            </a>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""


def render_footer() -> str:
    return """
<div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 22px 0;">&nbsp;</div>

<p style="margin:0; text-align:center; font-family:Arial, Helvetica, sans-serif; font-size:12px; line-height:18px; color:#777777;">
  Prism Research<br>
  Proudly Prepared in Australia.
</p>
"""


def render_photo_confirmation_email(order: dict) -> tuple[str, str, str]:
    name = get_customer_name(order)
    photo_link = clean_url(order.get("Photo_link"))

    subject = "Photos Inside - Prepared with Precision"

    text_body = f"""Hi {name},

Thanks for your patience.

Please click the link below for the photo of your order.

{photo_link}

It has now been sent for dispatch and on the way to you.

Questions? Just reply to this email.
We’re always happy to help.

Prism Research
Proudly Prepared in Australia.
"""

    photo_button = render_button(photo_link, "VIEW PACKAGE PHOTO", "#176b43")

    fallback_link_html = ""
    if photo_link:
        fallback_link_html = f"""
<p style="margin:0 0 28px 0; font-family:Arial, Helvetica, sans-serif; font-size:16px; line-height:22px; color:#000000;">
  If the button does not work, use this link to view photo:<br>
  <a href="{photo_link}" target="_blank" rel="noopener" style="color:#000000; text-decoration:underline; word-break:break-all;">
    {photo_link}
  </a>
</p>
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>

<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0; padding:0; background-color:#ffffff; border-collapse:collapse;">
    <tr>
      <td align="center" style="padding:0; margin:0;">

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px; margin:0 auto; background-color:#f4f8fa; border-collapse:collapse;">

          <tr>
            <td align="center" style="padding:32px 24px 18px 24px; background-color:#f4f8fa;">
              <img src="{LOGO_URL}" alt="PRISM" width="120" style="display:block; width:120px; max-width:120px; height:auto; margin:0 auto 24px auto; border:0; outline:none; text-decoration:none;">

              <h1 style="margin:0; font-family:Arial, Helvetica, sans-serif; font-size:34px; line-height:40px; font-weight:700; color:#000000; text-align:center;">
                <span style="color:#1f8f55;">Photos Inside</span><br>
                Prepared with Precision
              </h1>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:0; margin:0;">
              <img src="{PHOTO_HERO_IMAGE_URL}" alt="Package photo" width="600" style="display:block; width:100%; max-width:600px; height:auto; border:0; outline:none; text-decoration:none; margin:0;">
            </td>
          </tr>

          <tr>
            <td style="padding:40px 28px 36px 28px; font-family:Arial, Helvetica, sans-serif; color:#000000; text-align:left; background-color:#f4f8fa;">

              <h2 style="margin:0 0 26px 0; font-family:Arial, Helvetica, sans-serif; font-size:32px; line-height:38px; font-weight:700; color:#000000;">
                Package Photos (2/3)
              </h2>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Hi {name},
              </p>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Thanks for your patience.
              </p>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Please click the button below for the photo of your order.
              </p>

              <p style="margin:0 0 28px 0; font-size:16px; line-height:24px;">
                It has now been sent for dispatch and on the way to you.
              </p>

              {photo_button}

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 30px 0;">&nbsp;</div>

              {fallback_link_html}

              <p style="margin:0 0 30px 0; font-size:16px; line-height:22px;">
                Questions? Just reply to this email.<br>
                We’re always happy to help.
              </p>

              {render_footer()}

            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>
</body>
</html>
"""

    return subject, text_body, html_body


def render_tracking_number_email(order: dict) -> tuple[str, str, str]:
    name = get_customer_name(order)
    track_link = clean_url(order.get("Track_link"))

    subject = "Order Shipped - Tracking Number Inside"

    text_body = f"""Hi {name},

Your tracking information is now available.

Please click the link below to track your order.

{track_link}

Questions? Just reply to this email.
We’re always happy to help.

Prism Research
Proudly Prepared in Australia.
"""

    track_button = render_button(track_link, "TRACK YOUR ORDER", "#46699b")

    fallback_link_html = ""
    if track_link:
        fallback_link_html = f"""
<p style="margin:0 0 28px 0; font-family:Arial, Helvetica, sans-serif; font-size:16px; line-height:22px; color:#000000;">
  If the button does not work, use this link to track order:<br>
  <a href="{track_link}" target="_blank" rel="noopener" style="color:#000000; text-decoration:underline; word-break:break-all;">
    {track_link}
  </a>
</p>
"""

    html_body = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{subject}</title>
</head>

<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0; padding:0; background-color:#ffffff; border-collapse:collapse;">
    <tr>
      <td align="center" style="padding:0; margin:0;">

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px; margin:0 auto; background-color:#f4f8fa; border-collapse:collapse;">

          <tr>
            <td align="center" style="padding:32px 24px 18px 24px; background-color:#f4f8fa;">
              <img src="{LOGO_URL}" alt="PRISM" width="120" style="display:block; width:120px; max-width:120px; height:auto; margin:0 auto 24px auto; border:0; outline:none; text-decoration:none;">

              <h1 style="margin:0; font-family:Arial, Helvetica, sans-serif; font-size:34px; line-height:40px; font-weight:700; color:#000000; text-align:center;">
                <span style="color:#41699e;">Order Shipped</span><br>
                Tracking Number Inside
              </h1>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:0; margin:0;">
              <img src="{TRACK_HERO_IMAGE_URL}" alt="Tracking information" width="600" style="display:block; width:100%; max-width:600px; height:auto; border:0; outline:none; text-decoration:none; margin:0;">
            </td>
          </tr>

          <tr>
            <td style="padding:40px 28px 36px 28px; font-family:Arial, Helvetica, sans-serif; color:#000000; text-align:left; background-color:#f4f8fa;">

              <h2 style="margin:0 0 26px 0; font-size:32px; line-height:38px; font-weight:700; color:#000000;">
                Tracking Number (3/3)
              </h2>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Hi {name},
              </p>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Your tracking information is now available.
              </p>

              <p style="margin:0 0 28px 0; font-size:16px; line-height:24px;">
                Please click the button below to track your order.
              </p>

              {track_button}

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 30px 0;">&nbsp;</div>

              {fallback_link_html}

              <p style="margin:0 0 30px 0; font-size:16px; line-height:22px;">
                Questions? Just reply to this email.<br>
                We’re always happy to help.
              </p>

              {render_footer()}

            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>
</body>
</html>
"""

    return subject, text_body, html_body