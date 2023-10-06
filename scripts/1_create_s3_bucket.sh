# backend-lambda
echo "Please type your lambda name"
read lambdaname
cat > lambdaname <<EOF
$lambdaname
EOF
echo "Please type your bucket name"
read bucketname
cat > bucketname <<EOF
$bucketname
EOF
bucketname=`cat bucketname`
aws s3api create-bucket --bucket $bucketname --region us-west-2 --create-bucket-configuration LocationConstraint=us-west-2 --profile personaljulian
cd ../terraform
cat > variables.tf <<EOF
variable "app_version" {}

variable "s3_bucket" {
  default = "$bucketname"
}

variable "lambda_name" {
  default = "$lambdaname"
}

variable "retention_in_days"{
  default = 1
}

variable "aws_access_key" {
  description = "Access Key for AWS"
}

variable "aws_secret_key" {
  description = "Secret Key for AWS"
}
EOF

