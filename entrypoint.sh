#!/usr/bin/env bash
aea fingerprint skill brainbot/channel_manager:0.1.0
aea install && aea build && aea run
