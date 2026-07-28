import os
import sys

from wxcloudrun import app


if __name__ == '__main__':
    host = sys.argv[1] if len(sys.argv) > 1 else '0.0.0.0'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else int(os.environ.get('PORT', 80))
    app.run(host=host, port=port)
