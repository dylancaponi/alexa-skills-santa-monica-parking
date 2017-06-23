#!/bin/bash
echo 'main.py to site-packages';
cp main.py venv/lib/python2.7/site-packages/main.py;
cd venv/lib/python2.7/site-packages/;
echo 'zip contents of site-packages';
zip -qr Archive.zip ./*;
echo 'update lambda in aws';
aws lambda update-function-code --function-name arn:aws:lambda:us-east-1:369588988403:function:alexa-skills-santa-monica-parking --zip-file fileb://Archive.zip --region us-east-1; 
# --profile aws-noo-1;
