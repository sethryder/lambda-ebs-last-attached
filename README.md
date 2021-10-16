# lambda-ebs-last-attached
An AWS Lamba function that will add a custom tag with the instance's name and id that a volume is attached to. Useful for if an instance goes away but the volume stays behind and you need to quickly tell what it was connected to.

## How to use

I have a blog post [here](https://www.sethryder.com/tag-ebs-volumes-with-last-attached-instance/) that explains more on how to use this lambda.

## Python Version

This lambda has been tested with both Python2 and Python3. I recommend running Python3 since Python2 is EOL.
