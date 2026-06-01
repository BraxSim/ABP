PHOTO_HERO_IMAGE_URL = "https://YOUR_PHOTO_HERO_IMAGE_URL.png"
TRACK_HERO_IMAGE_URL = "https://YOUR_TRACK_HERO_IMAGE_URL.png"

LOGO_URL = "https://i.ibb.co/qYP382xc/Mask-group.png"


def render_photo_confirmation_email(order: dict) -> tuple[str, str, str]:
    name = order.get("Cust_First") or "there"
    photo_link = order.get("Photo_link") or ""

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

    html_body = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0; padding:0; background-color:#ffffff;">
    <tr>
      <td align="center" style="padding:0; margin:0;">

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px; margin:0 auto; background-color:#f4f8fa; border-collapse:collapse;">

          <tr>
            <td align="center" style="padding:32px 24px 18px 24px; background-color:#f4f8fa;">
              <img src="{LOGO_URL}" alt="PRISM" width="120" style="display:block; width:120px; max-width:120px; height:auto; margin:0 auto 24px auto; border:0;">

              <h1 style="margin:0; font-family:Arial, Helvetica, sans-serif; font-size:34px; line-height:40px; font-weight:700; color:#000000; text-align:center;">
                <span style="color:#1f8f55;">Photos Inside</span><br>
                Prepared with Precision
              </h1>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:0; margin:0;">
              <img src="{PHOTO_HERO_IMAGE_URL}" alt="Package photo" width="600" style="display:block; width:100%; max-width:600px; height:auto; border:0; margin:0;">
            </td>
          </tr>

          <tr>
            <td style="padding:40px 48px 36px 48px; font-family:Arial, Helvetica, sans-serif; color:#000000; text-align:left; background-color:#f4f8fa;">

              <h2 style="margin:0 0 26px 0; font-size:32px; line-height:38px; font-weight:700; color:#000000;">
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

              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 32px 0;">
                <tr>
                  <td bgcolor="#176b43" style="border-radius:4px;">
                    <a href="{photo_link}" target="_blank"
                       style="display:inline-block; padding:16px 34px; font-size:15px; line-height:18px; font-weight:700; font-family:Arial, Helvetica, sans-serif; color:#ffffff; text-decoration:none;">
                      VIEW PACKAGE PHOTO
                    </a>
                  </td>
                </tr>
              </table>

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 30px 0;">&nbsp;</div>

              <p style="margin:0 0 28px 0; font-size:16px; line-height:22px;">
                If the button does not work, use this link to view photo:<br>
                <a href="{photo_link}" target="_blank" style="color:#000000; text-decoration:none; word-break:break-all;">
                  {photo_link}
                </a>
              </p>

              <p style="margin:0 0 30px 0; font-size:16px; line-height:22px;">
                Questions? Just reply to this email.<br>
                We’re always happy to help.
              </p>

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 22px 0;">&nbsp;</div>

              <p style="margin:0; text-align:center; font-size:12px; line-height:18px; color:#777777;">
                Prism Research<br>
                Proudly Prepared in Australia.
              </p>

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
    name = order.get("Cust_First") or "there"
    track_link = order.get("Track_link") or ""

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

    html_body = f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background-color:#ffffff;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0; padding:0; background-color:#ffffff;">
    <tr>
      <td align="center" style="padding:0; margin:0;">

        <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px; margin:0 auto; background-color:#f4f8fa; border-collapse:collapse;">

          <tr>
            <td align="center" style="padding:32px 24px 18px 24px; background-color:#f4f8fa;">
              <img src="{LOGO_URL}" alt="PRISM" width="120" style="display:block; width:120px; max-width:120px; height:auto; margin:0 auto 24px auto; border:0;">

              <h1 style="margin:0; font-family:Arial, Helvetica, sans-serif; font-size:34px; line-height:40px; font-weight:700; color:#000000; text-align:center;">
                <span style="color:#41699e;">Order Shipped</span><br>
                Tracking Number Inside
              </h1>
            </td>
          </tr>

          <tr>
            <td align="center" style="padding:0; margin:0;">
              <img src="{TRACK_HERO_IMAGE_URL}" alt="Tracking information" width="600" style="display:block; width:100%; max-width:600px; height:auto; border:0; margin:0;">
            </td>
          </tr>

          <tr>
            <td style="padding:40px 48px 36px 48px; font-family:Arial, Helvetica, sans-serif; color:#000000; text-align:left; background-color:#f4f8fa;">

              <h2 style="margin:0 0 26px 0; font-size:32px; line-height:38px; font-weight:700; color:#000000;">
                Tracking Number (3/3)
              </h2>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Hi {name},
              </p>

              <p style="margin:0 0 22px 0; font-size:16px; line-height:24px;">
                Your tracking information is now available
              </p>

              <p style="margin:0 0 28px 0; font-size:16px; line-height:24px;">
                Please click the button below to track your order.
              </p>

              <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 32px 0;">
                <tr>
                  <td bgcolor="#46699b" style="border-radius:4px;">
                    <a href="{track_link}" target="_blank"
                       style="display:inline-block; padding:16px 34px; font-size:15px; line-height:18px; font-weight:700; font-family:Arial, Helvetica, sans-serif; color:#ffffff; text-decoration:none;">
                      TRACK YOUR ORDER
                    </a>
                  </td>
                </tr>
              </table>

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 30px 0;">&nbsp;</div>

              <p style="margin:0 0 28px 0; font-size:16px; line-height:22px;">
                If the button does not work, use this link to track order:<br>
                <a href="{track_link}" target="_blank" style="color:#000000; text-decoration:none; word-break:break-all;">
                  {track_link}
                </a>
              </p>

              <p style="margin:0 0 30px 0; font-size:16px; line-height:22px;">
                Questions? Just reply to this email.<br>
                We’re always happy to help.
              </p>

              <div style="height:1px; background-color:#cfcfcf; line-height:1px; font-size:1px; margin:0 0 22px 0;">&nbsp;</div>

              <p style="margin:0; text-align:center; font-size:12px; line-height:18px; color:#777777;">
                Prism Research<br>
                Proudly Prepared in Australia.
              </p>

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