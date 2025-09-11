#!/bin/bash
daphne -b 0.0.0.0 -p 8001 svango.asgi:application