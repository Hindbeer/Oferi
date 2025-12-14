from config import settings


class CaptionUtils:
    @staticmethod
    def escape_html(text: str) -> str:
        """
        Escaping special characters in HTML
        """
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )

    @staticmethod
    def build_caption(text: str | None, user_full_name: str) -> str:
        """
        Creating a signature for a message
        """

        safe_caption = CaptionUtils.escape_html(text) if text is not None else ""
        text_link = f'<a href="{settings.BOT_LINK}">👤 {CaptionUtils.escape_html(user_full_name)}</a>'
        caption = f"{safe_caption}\n\n{text_link}"

        return caption
