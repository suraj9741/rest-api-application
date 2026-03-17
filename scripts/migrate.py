import sys
import os
import logging
from alembic.config import Config
from alembic import command

# Add project root to path (IMPORTANT)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings

# -------------------------
# Logging
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------
# Alembic Config Loader
# -------------------------
def get_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(base_dir, "alembic.ini")

    config = Config(alembic_ini)

    # Inject DB URL dynamically
    config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

    return config

# -------------------------
# Commands
# -------------------------
def upgrade():
    logger.info("🚀 Running migrations (upgrade → head)")
    command.upgrade(get_config(), "head")
    logger.info("✅ Migration successful")


def downgrade(step="-1"):
    logger.warning(f"⚠️ Rolling back {step}")
    command.downgrade(get_config(), step)
    logger.info("↩️ Rollback complete")


def current():
    command.current(get_config())


def history():
    command.history(get_config())


# -------------------------
# CLI Entry
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/migrate.py [upgrade|downgrade|current|history]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "upgrade":
        upgrade()
    elif cmd == "downgrade":
        step = sys.argv[2] if len(sys.argv) > 2 else "-1"
        downgrade(step)
    elif cmd == "current":
        current()
    elif cmd == "history":
        history()
    else:
        print(f"Unknown command: {cmd}")