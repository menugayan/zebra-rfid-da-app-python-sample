#!/bin/bash
# Test sample-filter.py directly on reader (for development)
READER_IP="${1:-192.168.1.100}"
APP_FILE="sample-filter.py"

echo "Copying $APP_FILE to reader at $READER_IP..."
scp "$APP_FILE" "rfidadm@$READER_IP:/apps/"

echo "To test, SSH into reader and run:"
echo "  ssh rfidadm@$READER_IP"
echo "  cd /apps"
echo "  python3 $APP_FILE"
