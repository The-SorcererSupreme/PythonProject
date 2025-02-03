from app.services.database import Database

class Session:
    def remove_session(self, db: Database, token: str) -> bool:
        """Remove a session by token."""
        query = "DELETE FROM sessions WHERE session_token = %s RETURNING id;"
        db.cursor.execute(query, (token,))
        deleted_row = db.cursor.fetchone()
        db.connection.commit()
        return bool(deleted_row)  # If a row was deleted, return True
