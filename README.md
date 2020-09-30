---
title: ci/cd之drone
date: 2020-09-29 19:29:38
tags: 
  - ci/cd 
  - drone
---

公司去年底的时候运维组通过drone搭建了ci/cd的平台。公司的项目也陆陆续续通过drone来进行部署了。在使用的过程中，我觉得有两点不怎么方便。
- 使用的过程中不过公司的项目过于多，drone的yaml文件分散在每一个项目之中，管理麻烦, 有时候修改一个基础的step需要到每一个项目中去修改。
- 服务管理不灵活。很多时候一个项目对应到一个服务，关于这个服务的测试，部署, 检测不够灵活,若是能手动触发，会更方便管理。

之前看到drone的文档的时候，对这两个问题的解决办法有了一点思路。 这些天抽空把这两个问题的解决办法写成了一个demo。
ps:本文是流程性的一个总结，略过了大量细节.
### 添加github application

打开 `https://github.com/settings/developers` 新建一个 authapp，并记录client_id,和 client_secret
回调地址填写 `http://edrone.ismewen.com/login`。
### helm安装drone

#### 添加helm仓库
```bash
helm repo add stable  http://mirror.azure.cn/kubernetes/charts/
```
#### 安装helm 

```
kubectl create ns edrone
helm install edrone stable/drone -n edrone -f values.yaml
```
values.yaml
```
ingress:
  enabled: true
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-staging
  hosts:
    - edrone.ismewen.com
sourceControl:
  provider: github
  github:
    clientID: YOUR_CLIENT_ID 
    clientSecretKey: clientSecret
    clientSecretValue: YOUR_CLIENT_SECRET_VALUE 
    server: https://github.com

server:
  adminUser: ismewen # githubname
  kubernetes:
    enabled: true
  host: edrone.ismewen.com
  protocol: http

persistence:
  enabled: true
  existingClaim: dronepvc # 预先创建一个pvc
```

#### 验证安装结果
- drone server pod running
```
root@CCS-TEST-M001:~/ethan/edrone# kubectl get pods -n edrone
NAME                                   READY   STATUS    RESTARTS   AGE
edrone-drone-server-6b49c69997-qzpg6   1/1     Running   0          11h
```
- edrone.ismewen.com 能够正常访问

### drone部署helm应用 

#### 准备部署的应用

新建一个django应用并为其编写Dockerfile 和 helm charts包. 具体位置在 `https://github.com/ismewen/edrone`.

#### drone上面激活

 激活drone并设置为trust

#### 获取k8s信息
获取k8s相关信息. 并在drone中添加secret信息.
- 获取token
```
kubectl get secret -n kube-system | grep admin-user | awk '{print $1}' | xargs -I  {} kubectl get secret {} -o jsonpath={.data.token} -n kube-system | base64 -d
```
- 获取 ca
```
kubectl get secret -n kube-system | grep admin-user | awk '{print $1}' | xargs -I  {} kubectl get secret {} -o jsonpath={.data.ca\\.crt} -n kube-system 
```
- 添加 k8s_token, k8s_ca, k8s_api_server等secret

#### 编写 .drone.yaml 
```
kind: pipeline
name: default

steps:
  - name: docker
    image: plugins/docker
    settings:
      repo: fscripy/edrone
      tag: ${DRONE_COMMIT_SHA}
      username:
        from_secret: fscripyu_username
      password:
        from_secret: fscripyu_password
    volumes:
      - name: dockercache
        path: /var/lib/docker
  - name: default-deploy
    image: bitsbeats/drone-helm3
    settings:
      kube_api_server:
        from_secret: k8s_api_server
      kube_token:
        from_secret: k8s_token
      kube_certificate:
        from_secret: k8s_ca
      chart: ./edrone
      release: edrone
      helm_command: upgrade
      wait: true
      force: false
      namespace: default
      values: image.tag=${DRONE_COMMIT_SHA}
volumes:
- name: dockercache
  host:
    path: /tmp/docker/${DRONE_REPO}/${DRONE_BRANCH}
```
至此一个完整的部署流程就走完了。

### DRONE_YAML_ENDPOINT 自定义yaml返回

#### 修改drone server
- 修改drone server的部署方式。环境变量新增 `DRONE_YAML_ENDPOINT``
```
server:
  adminUser: ismewen
  kubernetes:
    enabled: true
  host: edrone.ismewen.com
  protocol: http
  env:
    DRONE_YAML_ENDPOINT: http://edrone-demo.ismewen.com/edrone/
```
- 升级一下drone server. `helm upgrade edrone stable/drone -n edrone -f values.yaml`

#### DRONE_YAML_ENDPOINT的作用

drone每次构建的时候会向 `DRONE_YAML_ENDPOINT` 定义的地址发送一个post请求，并获取构建的yaml.所以我们定义的接口需要返回构建所需的yaml。

dronepost的提交的相关数据如下

- headers(这里有个坑， headers中的accept为 `application/vnd.drone.config.v1+json`。解决办法可以参考`EdronAPIView`)

```
{
	'Content-Length': '1193',
	'Content-Type': 'application/json',
	'Host': 'edrone-demo.ismewen.com',
	'X-Request-Id': 'f0b7add0ee3094ea3fd634629bda0725',
	'X-Real-Ip': '10.244.3.1',
	'X-Forwarded-For': '10.244.3.1',
	'X-Forwarded-Host': 'edrone-demo.ismewen.com',
	'X-Forwarded-Port': '80',
	'X-Forwarded-Proto': 'http',
	'X-Original-Uri': '/edrone/',
	'X-Scheme': 'http',
	'User-Agent': 'Go-http-client/1.1',
	'Accept': 'application/vnd.drone.config.v1+json',
	'Accept-Encoding': 'identity',
	'Date': 'Wed,
	30Sep202009: 08: 58GMT',
	'Digest': 'SHA-256=Dtn2RSEVorWlBinp4/XzpMseS/UvYK/sQjbMfJPYhfs=',
	'Signature': 'keyId="hmac-key",
	algorithm="hmac-sha256",
	signature="VBrMY7bohxd5rxAHeclFA9WM8Wshcy1YBx5StGCNSvQ=",
	headers="accept accept-encoding content-type date digest"'
}
```
- body
```json
{
    "build": {
        "id": 0,
        "repo_id": 11,
        "trigger": "@hook",
        "number": 0,
        "status": "pending",
        "event": "push",
        "action": "",
        "link": "https://github.com/ismewen/edrone/compare/5c008182b0d1...0d469dd79c03",
        "timestamp": 0,
        "message": "delete pydroneio",
        "before": "5c008182b0d10307a77fc28d2b19c5ddab308e2f",
        "after": "0d469dd79c03e8d0e99e5331c606c27b660e4498",
        "ref": "refs/heads/develop",
        "source_repo": "",
        "source": "develop",
        "target": "develop",
        "author_login": "ismewen",
        "author_name": "ismewen",
        "author_email": "ismewen@outlook.com",
        "author_avatar": "https://avatars0.githubusercontent.com/u/30500262?v=4",
        "sender": "ismewen",
        "started": 0,
        "finished": 0,
        "created": 1601437767,
        "updated": 1601437767,
        "version": 0
    },
    "repo": {
        "id": 11,
        "uid": "293063525",
        "user_id": 1,
        "namespace": "ismewen",
        "name": "edrone",
        "slug": "ismewen/edrone",
        "scm": "",
        "git_http_url": "https://github.com/ismewen/edrone.git",
        "git_ssh_url": "git@github.com:ismewen/edrone.git",
        "link": "https://github.com/ismewen/edrone",
        "default_branch": "master",
        "private": false,
        "visibility": "public",
        "active": true,
        "config_path": ".drone.yml",
        "trusted": true,
        "protected": false,
        "ignore_forks": false,
        "ignore_pull_requests": false,
        "timeout": 60,
        "counter": 0,
        "synced": 0,
        "created": 0,
        "updated": 0,
        "version": 0
    }
}
```

#### 查找所需要的drone文件
根据项目的名字和分支的名字找到对应的yaml返回给drone server。
返回的数据格式如下。
```
{
    "Data": .... # yaml字符串
}
```

```
projects
├── __init__.py
├── default.yaml
└── edrone
    ├── __init__.py
    ├── default.yaml
    ├── develop.yaml
    └── master.yaml
```

这样便能将所有的项目的yaml文件集中管理起来。解决了前面提的问题1.


### 手动触发构建

参考dron的官方的api `https://docs.drone.io/api/builds/build_create/` 便可实现手动触发一次构建。

#### 设置drone server的数据库

```
server:
  adminUser: ismewen
  kubernetes:
    enabled: true
  host: edrone.ismewen.com
  protocol: http
  env:
    DRONE_YAML_ENDPOINT: http://edrone-demo.ismewen.com/edrone/
  database:
    driver: postgres
    dataSource: postgres://xxx:xxx@postgresql-13293-0.cloudclusters.net:13314/edrone
```
再helm upgrade一下.

#### 建立django模型
 
- 执行 inspect 命令.生成django的model
```
python manage.py inspectdb
``` 

#### 结合api编写接口

详细代码请参考 `BuildAPIViewSet`类的实现

```
class BuildAPIViewSet(APIViewSet):
    custom_name = "build"
    path = "builds"

    model = Builds
    serializer_class = serializers.BuildSerializer

    serializer_mapping = {
        "create": serializers.BuildCreateSerializer
    }
```

通过django的model和drone的api相结合便能比较好的实现drone自带的界面。方便集成到其他的系统。至此便解决了问题2.