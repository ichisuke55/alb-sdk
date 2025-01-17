# Copyright 2021 VMware, Inc.
# SPDX-License-Identifier: Apache License 2.0

""" Almost all the constants we used are available here """

# Constant Objects
DEFAULT_TIMEOUT = 16
DEFAULT_INTERVAL = 5
DEFAULT_TIME_UNTIL_UP = 1
DEFAULT_FAILED_CHECKS = 1
DEFAULT_PORT = 80
SOURCE_ADDR_TIMEOUT = 180
MIN_SESSION_TIMEOUT = 60
MAX_SESSION_TIMEOUT = 1800
APP_PERSISTANCE_TIMEOUT = 100
PLACE_HOLDER_STR = "auto_created"

# skipping objects
POOL_SKIP = ['inband-health']
PERSISTANCE_SKIP = ['RADIUS', 'RTSP', 'Header', 'SIP']
