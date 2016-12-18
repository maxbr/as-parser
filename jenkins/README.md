Jenkins
=======

## Prepare

### Tools

**Install hyper cli:**

```
cd /sandbox
wget https://hyper-install.s3.amazonaws.com/hyper-linux-x86_64.tar.gz
tar xzf hyper-linux-x86_64.tar.gz
rm hyper-linux-x86_64.tar.gz
chmod +x hyper
mkdir .hyper
echo "{\"auths\":{},\"clouds\":{\"tcp://us-west-1.hyper.sh:443\":{\"accesskey\":\"$HYPER_ACCESS_KEY\",\"secretkey\":\"$HYPER_SECRET_KEY\"}}}" > .hyper/config.json
```

### Plugins
  * [Git Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Git+Plugin)
  * [Workspace Cleanup Plugin](http://wiki.jenkins-ci.org/display/JENKINS/Workspace+Cleanup+Plugin)
  * [Job DSL](https://wiki.jenkins-ci.org/display/JENKINS/Job+DSL+Plugin)
  * [Environment Inject Plugin](https://wiki.jenkins-ci.org/display/JENKINS/EnvInject+Plugin)

### Seed job

**Create job:**
```
curl -X POST "https://${USER}:${PASS}@{URL}/createItem?name=Seed_Job" --data-binary "@seed.xml" -H "Content-Type: text/xml"
```
