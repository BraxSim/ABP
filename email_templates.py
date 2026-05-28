def render_prism_logistics_email(order: dict) -> tuple[str, str, str]:
    name = order.get("name") or "there"
    order_id = order.get("order_id") or ""
    logistics_link = order.get("logistics_link") or ""

    subject = f"Your Tracking Information - {order_id}"

    text_body = f"""Hi {name},

Your order tracking information is now available.

Order ID: {order_id}
Tracking link: {logistics_link}

Please use this link to check the latest delivery status.

Best,
PRISM Team"""

    html_body = f"""
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:0; padding:0; background-color:#ffffff; font-family:Arial, Helvetica, sans-serif; color:#2c2c2c;">
  <tr>
    <td align="center" style="padding:0; margin:0;">

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px; margin:0 auto; background-color:#f4eddd; border-collapse:collapse;">

        <tr>
          <td align="center" style="padding:30px 28px 28px 28px; background-color:#eee6d3;">

            <img src="https://i.ibb.co/9k8kMy00/Mask-group-1.png"
                 alt="PRISM"
                 width="190"
                 style="display:block; width:190px; max-width:100%; height:auto; margin:0 auto 24px auto; border:0;">

            <h1 style="margin:0 0 18px 0; font-size:30px; line-height:1.15; font-weight:500; color:#303030;">
              Your Order Is<br>
              On The Way
            </h1>

            <p style="margin:0 0 22px 0; font-size:15px; line-height:1.5; color:#303030;">
              Hi {name}, your tracking information is now available.
            </p>

            <p style="margin:0 0 18px 0; font-size:15px; line-height:1.5; color:#303030;">
              <strong>Order ID:</strong> {order_id}
            </p>

            <table cellpadding="0" cellspacing="0" border="0" style="margin-top:18px;">
              <tr>
                <td align="center" bgcolor="#5a168f" style="border-radius:22px;">
                  <a href="{logistics_link}"
                     target="_blank"
                     style="display:inline-block; padding:12px 30px; font-size:13px; font-weight:bold; color:#ffffff; text-decoration:none; border-radius:22px;">
                    TRACK YOUR ORDER
                  </a>
                </td>
              </tr>
            </table>

            <p style="margin:24px 0 0 0; font-size:13px; line-height:1.5; color:#303030;">
              If the button does not work, please copy and paste this link:<br>
              <a href="{logistics_link}" style="color:#5a3c8e;">{logistics_link}</a>
            </p>

          </td>
        </tr>

        <tr>
          <td style="padding:24px 32px; background-color:#eee6d3;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
              <tr>
                <td valign="middle" style="font-size:14px; line-height:1.45; color:#303030;">
                  <h2 style="margin:0 0 6px 0; font-size:22px; line-height:1.2; color:#303030;">
                    Need Help?
                  </h2>
                  If you have any questions about your order or delivery, please contact our support team.
                </td>

                <td align="right" valign="middle" width="130" style="padding-left:16px;">
                  <table cellpadding="0" cellspacing="0" border="0">
                    <tr>
                      <td bgcolor="#0d222b">
                        <a href="mailto:support@prismnootripics.com"
                           style="display:inline-block; padding:13px 22px; font-size:13px; font-weight:bold; color:#ffffff; text-decoration:none;">
                          Contact Us
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:30px 32px; background-color:#0d222b; color:#ffffff;">

            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;">
              <tr>
                <td valign="top" width="50%">
                  <img src="https://i.ibb.co/qYP382xc/Mask-group.png"
                       alt="PRISM"
                       width="190"
                       style="display:block; width:190px; max-width:100%; height:auto; margin:0 0 8px 0; border:0;">

                  <div style="font-size:13px; line-height:1.35; color:#ffffff;">
                    Engineered for Cognitive Performance
                  </div>
                </td>
                <td valign="top" align="right" width="50%" style="font-size:13px; line-height:1.6; color:#ffffff;">
                  support@prismnootripics.com<br><br>
                  Trusted, Local, Responsive Team<br>
                  Based in Australia
                </td>
              </tr>
            </table>

          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>
"""

    return subject, text_body, html_body