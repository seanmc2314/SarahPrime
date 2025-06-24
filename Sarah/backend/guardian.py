import os
import ast
import logging
import uuid
from datetime import datetime

class Guardian:
    def __init__(self):
        logging.basicConfig(filename="logs/guardian.log", level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def log_proposed_change(self, description, code, filename):
        change_id = str(uuid.uuid4())
        with open(f"changes/pending/{change_id}.py", "w") as f:
            f.write(code)
        self.logger.info(f"{datetime.now()} - Proposed change {change_id}: {description}, File: {filename}")
        return change_id

    def validate_change(self, change_id):
        try:
            with open(f"changes/pending/{change_id}.py", "r") as f:
                code = f.read()
            # Basic syntax check
            ast.parse(code)
            # Add more validation (e.g., security checks, dependency analysis)
            return True
        except Exception as e:
            self.logger.error(f"{datetime.now()} - Validation failed for {change_id}: {str(e)}")
            return False

    def log_applied_change(self, change_id):
        os.rename(f"changes/pending/{change_id}.py", f"changes/applied/{change_id}.py")
        self.logger.info(f"{datetime.now()} - Applied change {change_id}")
