ami-03a7c686223124056
https://aws.amazon.com/marketplace/pp/prodview-lb5bojtkc3wv2?sr=0-6&ref_=beagle&applicationId=AWSMPContessa#pdp-usage

Usage Instructions:

    Make sure the instance security groups allow inbound traffic to TCP port 8443.
    Make sure the instance has the role to access the license file: https://docs.aws.amazon.com/dcv/latest/adminguide/setting-up-license.html
    Connect to your remote machine with ssh -i <your-pem-key> ec2-user@<public-dns>
    Set the password for the ec2-user with sudo passwd ec2-user. This is the password you will use to log in DCV.
    Create a DCV virtual session using command dcv create-session &lt;name-of-your-session&gt;, see
    https://docs.aws.amazon.com/dcv/latest/adminguide/managing-sessions.html
    Connect to your remote machine with the NICE DCV native client or web client using https://<public_dns>:8443.

https://docs.aws.amazon.com/dcv/latest/adminguide/managing-sessions-lifecycle-view.html

