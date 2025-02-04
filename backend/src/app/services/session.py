from app.services.database import Database

class Session:
    def remove_session(self, db: Database, session_id: str) -> bool:
        """Remove a session by session using the Database class."""
        query = "DELETE FROM sessions WHERE id = %s RETURNING id;"
        deleted_row = db.delete_query(query, (session_id,))
        return bool(deleted_row)  # If a row was deleted, return True
