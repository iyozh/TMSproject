import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    files = s3.list_objects(Bucket=event["Records"][0]["s3"]["bucket"]["name"])[
        "Contents"
    ]

    all_avatars = {}

    for path, obj in [[i["Key"].split("/")[0], i] for i in files]:
        all_avatars.setdefault(path, {}).setdefault(
            obj["Key"].split("_")[1], []
        ).append([obj["Key"], obj["LastModified"]])

    keys_to_remove = []

    location = event["Records"][0]["s3"]["object"]["key"].split("/")[0]

    for pk, avatars in all_avatars[location].items():
        files = sorted(avatars, key=lambda avatar: avatar[1])[:-1]
        kk = [f[0] for f in files]
        keys_to_remove.extend(kk)

    for key in keys_to_remove:
        s3.delete_object(Bucket=bucket, Key=key)
