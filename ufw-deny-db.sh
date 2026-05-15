#!/bin/bash
ufw delete allow 33306/tcp
ufw reload
ufw status
