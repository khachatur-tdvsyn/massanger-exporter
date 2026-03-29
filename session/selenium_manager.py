# selenium_manager.py
import threading
import logging
from typing import Dict

from service.base import BaseMessangerFirefoxSession as BaseSession
from service.whatsapp import WhatsappSession
from django.conf import settings

logger = logging.getLogger(__name__)

class ThreadSafeSeleniumManager:
    """Thread-safe manager for BaseSession instances"""
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._sessions: Dict[str, BaseSession] = {}
        return cls._instance
    
    @classmethod
    def _get_instance(cls):
        return cls()
    
    @classmethod
    def _create_new_session(cls, messanger_type, user_id):
        session_types = {
            'wapp': WhatsappSession
        }
        return session_types.get(messanger_type)(user_id, settings.PROFILES_PATH)

    @classmethod
    def create_session(cls, session_id: str, messanger_type: str, user_id: str, **options) -> BaseSession:
        """Create a new BaseSession and open browser"""
        instance = cls._get_instance()
        with cls._lock:
            logger.info(f"Creating session: {session_id}")
            
            if session_id in instance._sessions:
                raise ValueError(f"Session {session_id} already exists")
            
            # Create BaseSession instance
            session = cls._create_new_session(messanger_type, user_id)
            
            # Store in manager
            instance._sessions[session_id] = session
            
            logger.info(f"Session created. Active sessions: {list(instance._sessions.keys())}")
            return session
    
    @classmethod
    def get_session(cls, session_id: str) -> BaseSession:
        """Get an existing session"""
        instance = cls._get_instance()
        with cls._lock:
            if session_id not in instance._sessions:
                logger.error(f"Session {session_id} not found. Available: {list(instance._sessions.keys())}")
                raise ValueError(f"Session {session_id} not found")
            
            session = instance._sessions[session_id]
            
            if not session.is_open:
                logger.error(f"Session {session_id} is not open")
                raise ValueError(f"Session {session_id} is not open")
            
            return session
    
    @classmethod
    def close_session(cls, session_id: str) -> None:
        """Close and remove a session"""
        instance = cls._get_instance()
        with cls._lock:
            logger.info(f"Closing session: {session_id}")
            logger.info(f"Sessions before close: {list(instance._sessions.keys())}")
            
            if session_id in instance._sessions:
                try:
                    instance._sessions[session_id].quit()
                except Exception as e:
                    logger.warning(f"Error closing session: {e}")
                
                del instance._sessions[session_id]
                logger.info(f"Session {session_id} closed. Remaining sessions: {list(instance._sessions.keys())}")
            else:
                logger.error(f"Session {session_id} not found for closing")