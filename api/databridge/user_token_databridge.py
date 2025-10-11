from ..settings.database import get_supabase_admin_client
from supabase import Client
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)


class DBUserTokenResponse(BaseModel):
    google_access_token: str
    google_refresh_token: str


class UserTokenDatabridge:
    def __init__(self, supabase: Client) -> None:
        self.supabase = supabase
        self.user_tokens = self.supabase.table("user_tokens")

    async def get_user_tokens(self, *, user_id: str) -> DBUserTokenResponse | None:
        try:
            response = (
                self.user_tokens.select("google_access_token, google_refresh_token")
                .eq("id", user_id)
                .single()
                .execute()
            )
            if not response.data:
                return None

            _data = response.data
            return DBUserTokenResponse(
                google_access_token=_data["google_access_token"],
                google_refresh_token=_data["google_refresh_token"],
            )
        except Exception as e:
            logger.info(f"Error fetching user tokens: {e}")
            return None
