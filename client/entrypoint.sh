#!/bin/sh
cat > /etc/asound.conf <<EOF
defaults.pcm.card ${ALSA_CARD}
defaults.pcm.device ${ALSA_DEVICE}
defaults.ctl.card ${ALSA_CARD}
EOF

echo "Wrote /etc/asound.conf: ALSA_CARD=${ALSA_CARD} ALSA_DEVICE=${ALSA_DEVICE}"
cat /etc/asound.conf

exec "$@"