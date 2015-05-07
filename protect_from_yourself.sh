#!/bin/bash

chmod +x ./pre-push
cp ./pre-push .git/hooks/pre-push

echo "You've been protected from your own instict of destroying important branches"
