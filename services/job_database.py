import sqlite3
import logging
from typing import List, Optional
from models.job_listing import JobListing
from datetime import datetime

logger = logging.getLogger(__name__)

class JobDatabase:
    def __init__(self, db_path: str = "database.sqlite"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS JobListings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        company TEXT NOT NULL,
                        link TEXT NOT NULL UNIQUE,
                        location TEXT,
                        description TEXT,
                        salary TEXT,
                        time_listed TEXT,
                        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("JobListings table ready")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def save_jobs(self, jobs: List[JobListing]) -> int:
        """Save jobs to database, returns count of new jobs added"""
        if not jobs:
            return 0
            
        new_jobs_count = 0
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for job in jobs:
                    try:
                        cursor.execute("""
                            INSERT OR IGNORE INTO JobListings 
                            (title, company, link, location, description, salary, time_listed)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (
                            job.title,
                            job.company,
                            job.link,
                            job.location,
                            job.description,
                            job.salary,
                            job.time_listed
                        ))
                        
                        if cursor.rowcount > 0:
                            new_jobs_count += 1
                            
                    except Exception as e:
                        logger.error(f"Error saving job {job.title}: {e}")
                        continue
                
                conn.commit()
                logger.info(f"Saved {new_jobs_count} new jobs to database")
                
        except Exception as e:
            logger.error(f"Error saving jobs to database: {e}")
            
        return new_jobs_count
    
    def load_jobs(self, limit: Optional[int] = None) -> List[JobListing]:
        """Load jobs from database, optionally limit results"""
        jobs = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT title, company, link, location, description, salary, time_listed
                    FROM JobListings 
                    ORDER BY scraped_at DESC
                """
                
                if limit:
                    query += f" LIMIT {limit}"
                
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    job = JobListing(
                        title=row[0],
                        company=row[1],
                        link=row[2],
                        location=row[3],
                        description=row[4],
                        salary=row[5],
                        time_listed=row[6]
                    )
                    jobs.append(job)
                    
                logger.info(f"Loaded {len(jobs)} jobs from database")
                
        except Exception as e:
            logger.error(f"Error loading jobs from database: {e}")
            
        return jobs
    
    def get_job_count(self) -> int:
        """Get total number of jobs in database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM JobListings")
                return cursor.fetchone()[0]
        except Exception as e:
            logger.error(f"Error getting job count: {e}")
            return 0
    
    def clear_old_jobs(self, days: int = 30):
        """Remove jobs older than specified days"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Use parameterized modifier for sqlite datetime
                modifier = f"-{days} days"
                cursor.execute(
                    """
                    DELETE FROM JobListings
                    WHERE scraped_at <= datetime('now', ?)
                    """,
                    (modifier,)
                )

                deleted_count = cursor.rowcount
                conn.commit()
                logger.info(f"Deleted {deleted_count} old jobs")
                return deleted_count
                
        except Exception as e:
            logger.error(f"Error clearing old jobs: {e}")
            return 0

    def purge_old_jobs(self, days: int = 1) -> int:
        """Delete jobs older than `days` days. Returns number of rows deleted.

        This is a synchronous function you can call at startup or on-demand.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                modifier = f"-{days} days"
                cursor.execute(
                    """
                    DELETE FROM JobListings
                    WHERE scraped_at <= datetime('now', ?)
                    """,
                    (modifier,)
                )
                deleted = cursor.rowcount
                conn.commit()
                logger.info(f"Purged {deleted} jobs older than {days} days")
                return deleted
        except Exception as e:
            logger.error(f"Error purging old jobs: {e}")
            return 0

    # def schedule_periodic_purge(self, interval_minutes: int = 60, days: int = 1):
    #     """Schedule a periodic purge running in the current event loop.

    #     Call this after the application's asyncio event loop is running. Returns
    #     the created Task so the caller can keep a reference if desired.
    #     """
    #     loop = asyncio.get_event_loop()
    #     return loop.create_task(self._purge_loop(interval_minutes, days))

    # async def _purge_loop(self, interval_minutes: int, days: int):
    #     while True:
    #         try:
    #             deleted = self.purge_old_jobs(days=days)
    #             logger.info(f"Periodic purge removed {deleted} old jobs")
    #         except Exception:
    #             logger.exception("Error during periodic purge")
    #         await asyncio.sleep(interval_minutes * 60)
