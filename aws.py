from flask import Flask,render_template,request,redirect,url_for
import logging
import boto3
from botocore.exceptions import ClientError
import os
# __name__ is the current file name
app=Flask(__name__ ,template_folder='template') 



@app.route('/')
def root():
    return render_template('index.html')

@app.route('/s3')
def s3():
    return render_template('s3.html')

@app.route('/s3/create/<bucket_name>')
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return render_template('s3_fail.html')
    return render_template('s3_success.html')

@app.route('/s3/delete/<bucket_name>')
def delete_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.delete_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.delete_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return render_template('s3_fail.html')
    return render_template('s3_success.html')

    
@app.route('/s3/upload/<file_name>/<bucket>')
def upload_file(file_name, bucket, object_name=None):

    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return render_template('s3_fail.html')
    return render_template('s3_success.html')


@app.route('/s3/create',methods=['POST','GET'])
def s3_create():
    if request.method=='POST' : 
        user=request.form['bucket_name']
        return redirect(url_for('create_bucket', bucket_name=user))
    else:
        return render_template('s3_create.html')

@app.route('/s3/upload',methods=['POST','GET'])
def s3_upload():
    if request.method=='POST' : 
        fileData=request.files['file'] 
        bucket_name=request.form['bucket_name']
        fileData.save(fileData.filename)
        return redirect(url_for('upload_file', file_name=fileData.filename,bucket=bucket_name))
    else:
        return render_template('s3_upload.html')

@app.route('/s3/delete',methods=['POST','GET'])
def s3_delete():
    if request.method=='POST' : 
        user=request.form['bucket_name']
        return redirect(url_for('delete_bucket', bucket_name=user))
    else:
        return render_template('s3_delete.html')

@app.route('/s3/list')
def s3_list():
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    return render_template('s3_list.html',response=response)


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)


