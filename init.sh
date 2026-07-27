set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"
RESET="${1:-}"

echo "======================================================"
echo "  ShopEasy — Database Initialisation"
echo "======================================================"

# ── Require venv ──────────────────────────────────────────────────────────────
if [ ! -d "${VENV_DIR}" ]; then
  echo ""
  echo "  ERROR: Virtual environment not found at ${VENV_DIR}"
  echo "  Run setup.sh first to install dependencies."
  exit 1
fi

source "${VENV_DIR}/bin/activate"
cd "${SCRIPT_DIR}"

# ── Optional reset ────────────────────────────────────────────────────────────
if [ "${RESET}" = "--reset" ]; then
  echo ""
  echo "  --reset flag detected."
  DB_FILE=$(python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
default = os.path.join(os.getcwd(), 'data', 'shopeasy.db')
print(os.path.abspath(os.environ.get('DATABASE_PATH', default)))
")
  if [ -f "${DB_FILE}" ]; then
    echo "  Deleting existing database: ${DB_FILE}"
    rm -f "${DB_FILE}"
  fi
fi

# ── Initialise database ───────────────────────────────────────────────────────
echo ""
echo "▶ Initialising database..."

python3 - <<'PYEOF'
from shopeasy import init_db
init_db()
PYEOF

echo ""
echo "======================================================"
echo "  Initialisation complete."
echo "  Start the app: bash run.sh"
echo "======================================================"
