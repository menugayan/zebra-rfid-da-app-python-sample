#!/bin/bash
# Deploy sample-filter to Zebra reader
READER_IP="${1:-192.168.1.100}"
DEB_FILE="sample-filter_1.0.0.deb"

echo "Deploying $DEB_FILE to reader at $READER_IP..."
scp "$DEB_FILE" "rfidadm@$READER_IP:/tmp/"

echo "Installing package..."
ssh "rfidadm@$READER_IP" "sudo dpkg -i /tmp/$DEB_FILE"

echo "Starting application..."
ssh "rfidadm@$READER_IP" "sudo systemctl restart userapps"

echo "Deployment complete!"
