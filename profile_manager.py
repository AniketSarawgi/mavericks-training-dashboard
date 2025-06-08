from db_config import get_connection
import mysql.connector # type: ignore

class ProfileManager:
    def __init__(self):
        try:
            self.conn = get_connection()
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(f"[DB ERROR] Could not connect to DB: {e}")
            raise

    def create_profile(self, fresher_id, name):
        try:
            self.cursor.execute("SELECT * FROM fresher_profiles WHERE fresher_id = %s", (fresher_id,))
            if self.cursor.fetchone():
                print(f"[!] Fresher ID {fresher_id} already exists. Skipping creation.")
                return

            self.cursor.execute("INSERT INTO fresher_profiles (fresher_id, name) VALUES (%s, %s)", (fresher_id, name))
            self.conn.commit()
            print(f"[✓] Profile created for {name} (ID: {fresher_id})")

        except mysql.connector.Error as e:
            print(f"[DB ERROR] Failed to create profile: {e}")

    def update_assessment(self, fresher_id, assessment_type, score):
        try:
            if not self._profile_exists(fresher_id):
                print(f"[x] Fresher ID {fresher_id} not found. Cannot update assessment.")
                return

            self.cursor.execute("""
                INSERT INTO assessments (fresher_id, assessment_type, score) 
                VALUES (%s, %s, %s)
            """, (fresher_id, assessment_type, score))
            self.conn.commit()
            print(f"[✓] Assessment '{assessment_type}' updated for ID {fresher_id}")

        except mysql.connector.Error as e:
            print(f"[DB ERROR] Failed to update assessment: {e}")

    def update_certification(self, fresher_id, certification_name):
        try:
            if not self._profile_exists(fresher_id):
                print(f"[x] Fresher ID {fresher_id} not found. Cannot update certification.")
                return

            self.cursor.execute("""
                INSERT INTO certifications (fresher_id, certification_name)
                VALUES (%s, %s)
            """, (fresher_id, certification_name))
            self.conn.commit()
            print(f"[✓] Certification '{certification_name}' added to ID {fresher_id}")

        except mysql.connector.Error as e:
            print(f"[DB ERROR] Failed to update certification: {e}")

    def update_learning_progress(self, fresher_id, topic, status):
        try:
            if not self._profile_exists(fresher_id):
                print(f"[x] Fresher ID {fresher_id} not found. Cannot update learning progress.")
                return

            self.cursor.execute("""
                INSERT INTO learning_progress (fresher_id, topic, status)
                VALUES (%s, %s, %s)
            """, (fresher_id, topic, status))
            self.conn.commit()
            print(f"[✓] Learning progress for '{topic}' updated to '{status}' for ID {fresher_id}")

        except mysql.connector.Error as e:
            print(f"[DB ERROR] Failed to update learning progress: {e}")

    def view_profile(self, fresher_id):
        try:
            self.cursor.execute("SELECT name FROM fresher_profiles WHERE fresher_id = %s", (fresher_id,))
            result = self.cursor.fetchone()
            if not result:
                print(f"[x] Fresher ID {fresher_id} not found.")
                return

            name = result[0]
            print(f"\n=== Profile for {name} (ID: {fresher_id}) ===")

            self.cursor.execute("SELECT assessment_type, score FROM assessments WHERE fresher_id = %s", (fresher_id,))
            assessments = self.cursor.fetchall()
            print("Assessments:", {row[0]: row[1] for row in assessments} or "None")

            self.cursor.execute("SELECT certification_name FROM certifications WHERE fresher_id = %s", (fresher_id,))
            certs = [row[0] for row in self.cursor.fetchall()]
            print("Certifications:", certs or "None")

            self.cursor.execute("SELECT topic, status FROM learning_progress WHERE fresher_id = %s", (fresher_id,))
            lp = {row[0]: row[1] for row in self.cursor.fetchall()}
            print("Learning Progress:", lp or "None")

            print("=" * 50)

        except mysql.connector.Error as e:
            print(f"[DB ERROR] Failed to fetch profile: {e}")

    def _profile_exists(self, fresher_id):
        self.cursor.execute("SELECT 1 FROM fresher_profiles WHERE fresher_id = %s", (fresher_id,))
        return self.cursor.fetchone() is not None

    def __del__(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
