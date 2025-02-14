#-*- coding: utf-8 -*-

__version__ = "0.38"

'''  
Requirements
python3, kops, ssh-keygen, awscli, packaging, appdirs, gcloud, azure-cli, helm, kubectl, kubernetes.tar.gz

# References:   https://github.com/kubernetes-incubator/client-python/blob/master/kubernetes/README.md
#   https://github.com/kubernetes/kops/blob/master/docs/aws.md
'''

import warnings
import requests
import fire
import tarfile
import os
import sys
import kubernetes.client as kubeclient
from kubernetes.client.rest import ApiException
import kubernetes.config as kubeconfig
import pick
import yaml
import json
import dill as pickle
from git import Repo
from pprint import pprint
import subprocess

class PioCli(object):
    _kube_deploy_registry = {'jupyter': (['jupyterhub.ml/jupyterhub-deploy.yaml'], []),
                            'spark': (['apachespark.ml/master-deploy.yaml'], ['spark-worker', 'metastore']),
                            'spark-worker': (['apachespark.ml/worker-deploy.yaml'], []),
                            'metastore': (['metastore.ml/metastore-deploy.yaml'], ['mysql']),
                            'hdfs': (['hdfs.ml/namenode-deploy.yaml'], []),
                            'redis': (['keyvalue.ml/redis-master-deploy.yaml'], []),
                            'presto': (['presto.ml/master-deploy.yaml',
                                        'presto.ml/worker-deploy.yaml'], ['metastore']),
                            'presto-ui': (['presto.ml/ui-deploy.yaml'], ['presto']),
                            'airflow': (['scheduler.ml/airflow-deploy.yaml'], ['mysql', 'redis']),
                            'mysql': (['sql.ml/mysql-master-deploy.yaml'], []),
                            'www': (['web.ml/home-deploy.yaml'], []),
                            'zeppelin': (['zeppelin.ml/zeppelin-deploy.yaml'], []),
                            'zookeeper': (['zookeeper.ml/zookeeper-deploy.yaml'], []),
                            'elasticsearch': (['elasticsearch.ml/elasticsearch-2-3-0-deploy.yaml'], []),
                            'kibana': (['kibana.ml/kibana-4-5-0-deploy.yaml'], ['elasticsearch'], []), 
                            'kafka': (['stream.ml/kafka-0.10-deploy.yaml'], ['zookeeper']),
                            'cassandra': (['cassandra.ml/cassandra-deploy.yaml'], []),
                            'prediction-jvm': (['prediction.ml/jvm-deploy.yaml'], []),
                            'prediction-python3': (['prediction.ml/python3-deploy.yaml'], []),
                            'prediction-tensorflow': (['prediction.ml/tensorflow-deploy.yaml'], []),
                            'turbine': (['dashboard.ml/turbine-deploy.yaml'], []),
                            'hystrix': (['dashboard.ml/hystrix-deploy.yaml'], []),
                            'weave-scope-app': (['dashboard.ml/weavescope/scope-1.3.0.yaml'], []),
                            'kubernetes-dashboard': (['dashboard.ml/kubernetes-dashboard/v1.6.0.yaml'], []),
                            'heapster': (['metrics.ml/monitoring-standalone/v1.3.0.yaml'], []),
                            'route53-mapper': (['dashboard.ml/route53-mapper/v1.3.0.yml'], []), 
                            'kubernetes-logging': (['dashboard.ml/logging-elasticsearch/v1.5.0.yaml'], []),
                           }

    _kube_svc_registry = {'jupyter': (['jupyterhub.ml/jupyterhub-svc.yaml'], []),
                         'spark': (['apachespark.ml/master-svc.yaml'], ['spark-worker', 'metastore']), 
                         'spark-worker': (['apachespark.ml/worker-svc.yaml'], []),
                         'metastore': (['metastore.ml/metastore-svc.yaml'], ['mysql']),
                         'hdfs': (['hdfs.ml/namenode-svc.yaml'], []),
                         'redis': (['keyvalue.ml/redis-master-svc.yaml'], []),
                         'presto': (['presto.ml/presto-master-svc.yaml',
                                     'presto.ml/presto-worker-svc.yaml'], ['metastore']),
                         'presto-ui': (['presto.ml/presto-ui-svc.yaml'], ['presto']),
                         'airflow': (['scheduler.ml/airflow-svc.yaml'], ['mysql', 'redis']),
                         'mysql': (['sql.ml/mysql-master-svc.yaml'], []),
                         'www': (['web.ml/home-svc.yaml'], []),
                         'zeppelin': (['zeppelin.ml/zeppelin-svc.yaml'], []),
                         'zookeeper': (['zookeeper.ml/zookeeper-svc.yaml'], []),
                         'kafka': (['stream.ml/kafka-0.10-svc.yaml'], ['zookeeper']),
                         'cassandra': (['cassandra.ml/cassandra-svc.yaml'], []),
                         'prediction-jvm': (['prediction.ml/jvm-svc.yaml'], []),
                         'prediction-python3': (['prediction.ml/python3-svc.yaml'], []),
                         'prediction-tensorflow': (['prediction.ml/tensorflow-svc.yaml'], []),
                         'turbine': (['dashboard.ml/turbine-svc.yaml'], []),
                         'hystrix': (['dashboard.ml/hystrix-svc.yaml'], []),
                        }

<<<<<<< HEAD
class PioCli(object):
    kube_deploy_registry = {'jupyter': (['jupyterhub.ml/jupyterhub-deploy.yaml'], []),
                            'spark': (['apachespark.ml/master-deploy.yaml'], ['spark-worker', 'metastore']),
                            'spark-worker': (['apachespark.ml/worker-deploy.yaml'], []),
                            'metastore': (['metastore.ml/metastore-deploy.yaml'], ['mysql']),
                            'hdfs': (['hdfs.ml/namenode-deploy.yaml'], []),
                            'redis': (['keyvalue.ml/redis-master-deploy.yaml'], []),
                            'presto': (['presto.ml/presto-master-deploy.yaml',
                                        'presto.ml/presto-worker-deploy.yaml'], ['metastore']),
                            'presto-ui': (['presto.ml/presto-ui-deploy.yaml'], ['presto']),
                            'airflow': (['scheduler.ml/airflow-deploy.yaml'], ['mysql', 'redis']),
                            'mysql': (['sql.ml/mysql-master-deploy.yaml'], []),
                            'www': (['web.ml/home-deploy.yaml'], []),
                            'zeppelin': (['zeppelin.ml/zeppelin-deploy.yaml'], []),
                            'zookeeper': (['zookeeper.ml/zookeeper-deploy.yaml'], []),
                            'kafka': (['stream.ml/kafka-0.10-rc.yaml'], ['zookeeper']),
                            'cassandra': (['cassandra.ml/cassandra-rc.yaml'], []),
                            'prediction-jvm': (['prediction.ml/jvm-deploy.yaml'], []),
                            'prediction-python3': (['prediction.ml/python3-deploy.yaml'], []),
                            'prediction-tensorflow': (['prediction.ml/tensorflow-deploy.yaml'], []),
                            'turbine': (['dashboard.ml/turbine-deploy.yaml'], []),
                            'hystrix': (['dashboard.ml/hystrix-deploy.yaml'], []),
                            'weavescope': (['dashboard.ml/weavescope.yaml'], []),
                            #'dashboard': (['dashboard.ml/kubernetes/kubernetes-dashboard.yaml'], []),
                            #'heapster': (['https://raw.githubusercontent.com/kubernetes/kops/master/addons/monitoring-standalone/v1.3.0.yaml']), []),
                            #'route53': (['https://raw.githubusercontent.com/kubernetes/kops/master/addons/route53-mapper/v1.3.0.yml']), []),
                           }

    kube_svc_registry = {'jupyter': (['jupyterhub.ml/jupyterhub-svc.yaml'], []),
                         'spark': (['apachespark.ml/master-svc.yaml'], ['spark-worker', 'metastore']), 
                         'spark-worker': (['apachespark.ml/worker-svc.yaml'], []),
                         'metastore': (['metastore.ml/metastore-svc.yaml'], ['mysql']),
                         'hdfs': (['hdfs.ml/namenode-svc.yaml'], []),
                         'redis': (['keyvalue.ml/redis-master-svc.yaml'], []),
                         'presto': (['presto.ml/presto-master-svc.yaml',
                                     'presto.ml/presto-worker-svc.yaml'], ['metastore']),
                         'presto-ui': (['presto.ml/presto-ui-svc.yaml'], ['presto']),
                         'airflow': (['scheduler.ml/airflow-svc.yaml'], ['mysql', 'redis']),
                         'mysql': (['sql.ml/mysql-master-svc.yaml'], []),
                         'www': (['web.ml/home-svc.yaml'], []),
                         'zeppelin': (['zeppelin.ml/zeppelin-svc.yaml'], []),
                         'zookeeper': (['zookeeper.ml/zookeeper-svc.yaml'], []),
                         'kafka': (['stream.ml/kafka-0.10-svc.yaml'], ['zookeeper']),
                         'cassandra': (['cassandra.ml/cassandra-svc.yaml'], []),
                         'prediction-jvm': (['prediction.ml/jvm-svc.yaml'], []),
                         'prediction-python3': (['prediction.ml/python3-svc.yaml'], []),
                         'prediction-tensorflow': (['prediction.ml/tensorflow-svc.yaml'], []),
                        }
=======
>>>>>>> fluxcapacitor/master

    def _get_default_pio_api_version(self):
        return 'v1'

<<<<<<< HEAD

    def config_get(self,
                   config_key):
        print(self.config_get_all()[config_key])
        print("\n")
        return self.config_get_all()[config_key]


    def config_set(self,
                   config_key,
                   config_value):
        self.config_merge_dict({config_key: config_value})


    def config_merge_dict(self, 
=======

    def _get_default_pio_git_home(self):
        return 'https://github.com/fluxcapacitor/pipeline/'


    def _get_default_pio_git_version(self):
        return 'v1.2.0'


    def get_config_value(self,
                         config_key):
        print("")
        pprint(self._get_full_config())
        print("")
        return self._get_full_config()[config_key]


    def set_config_value(self,
                         config_key,
                         config_value):
        print("config_key: '%s'" % config_key)
        self._merge_config_dict({config_key: config_value})
        print("config_value: '%s'" % self._get_full_config()[config_key])
        self._merge_config_dict({config_key: config_value})
        print("")
        pprint(self._get_full_config())
        print("")        


    def _merge_config_dict(self, 
>>>>>>> fluxcapacitor/master
                          config_dict):

        pio_api_version = self._get_full_config()['pio_api_version']

        config_file_base_path = os.path.expanduser("~/.pio/")
        expanded_config_file_base_path = os.path.expandvars(config_file_base_path)
        expanded_config_file_base_path = os.path.expanduser(expanded_config_file_base_path)
        expanded_config_file_base_path = os.path.abspath(expanded_config_file_base_path)
        expanded_config_file_path = os.path.join(expanded_config_file_base_path, 'config')
<<<<<<< HEAD

        pprint("Merging dict '%s' with existing config '%s'..." % (config_dict, expanded_config_file_path))

        existing_config_dict = self.config_get_all()
=======
        print("")
        pprint("Merging dict '%s' with existing config '%s'." % (config_dict, expanded_config_file_path))

        existing_config_dict = self._get_full_config()
>>>>>>> fluxcapacitor/master

        # >= Python3.5 
        # {**existing_config_dict, **config_dict}
        existing_config_dict.update(config_dict)

        new_config_yaml = yaml.dump(existing_config_dict, default_flow_style=False, explicit_start=True)

        with open(expanded_config_file_path, 'w') as fh:
            fh.write(new_config_yaml)
        print(new_config_yaml)
<<<<<<< HEAD
        print("...Done!")
        print("\n")
=======
        print("")
>>>>>>> fluxcapacitor/master


    def _get_full_config(self):
        config_file_base_path = os.path.expanduser("~/.pio/")
<<<<<<< HEAD
        expanded_config_file_base_path = os.path.expandvars(config_file_base_path)
        expanded_config_file_base_path = os.path.expanduser(expanded_config_file_base_path)
        expanded_config_file_base_path = os.path.abspath(expanded_config_file_base_path)
        expanded_config_file_path = os.path.join(expanded_config_file_base_path, 'config')

        # >= Python3.5
        # os.makedirs(expanded_config_file_base_path, exist_ok=True)
        if not os.path.exists(expanded_config_file_path):
            if not os.path.exists(expanded_config_file_base_path):
                os.makedirs(expanded_config_file_base_path)
            pio_api_version = self.pio_api_version() 
            initial_config_dict = {'pio_api_version': pio_api_version}
            initial_config_yaml =  yaml.dump(initial_config_dict, default_flow_style=False, explicit_start=True)
            print("Creating config '%s'..." % expanded_config_file_path)
            with open(expanded_config_file_path, 'w') as fh:
=======
        config_file_base_path = os.path.expandvars(config_file_base_path)
        config_file_base_path = os.path.expanduser(config_file_base_path)
        config_file_base_path = os.path.abspath(config_file_base_path)
        config_file_filename = os.path.join(config_file_base_path, 'config')

        if not os.path.exists(config_file_filename):
            if not os.path.exists(config_file_base_path):
                os.makedirs(config_file_base_path)
            initial_config_dict = {'pio_api_version': self._get_default_pio_api_version(),
                                   'pio_git_home': self._get_default_pio_git_home(),
                                   'pio_git_version': self._get_default_pio_git_version()}
            initial_config_yaml =  yaml.dump(initial_config_dict, default_flow_style=False, explicit_start=True)
            print("")
            print("Default config created at '%s'.  Override with 'pio init-pio'" % config_file_filename)
            print("")
            with open(config_file_filename, 'w') as fh:
>>>>>>> fluxcapacitor/master
                fh.write(initial_config_yaml)
                pprint(initial_config_dict)

        # Update the YAML 
<<<<<<< HEAD
        with open(expanded_config_file_path, 'r') as fh:
=======
        with open(config_file_filename, 'r') as fh:
>>>>>>> fluxcapacitor/master
            existing_config_dict = yaml.load(fh)
            return existing_config_dict
        print("\n")


<<<<<<< HEAD
    def config_view(self):
        pprint(self.config_get_all())
        print("\n")


    def cluster_top(self):
        subprocess.call("kubectl top node", shell=True)
        print("\n")
        print("Note:  Heapster must be deployed for this command ^^ to work.\n")
        print("\n")


    def app_top(self,
                app_name):
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if (app_name in pod.metadata.name):
                    subprocess.call("kubectl top %s" % app_name, shell=True)
        print("\n")
        print("Note:  Heapster must be deployed for this command ^^ to work.\n")
        print("\n")


    def cluster_init(self,
                     pio_home,
                     pio_runtime_version,
                     kube_cluster_context,
                     kube_namespace='default'):
=======
    def config(self):
        pprint(self._get_full_config())
        print("")


    def proxy(self,
              app_name,
              local_port=None,
              app_port=None):

        self.tunnel(app_name, local_port, app_port)


    def tunnel(self,
               app_name,
               local_port=None,
               app_port=None):

        pio_api_version = self._get_full_config()['pio_api_version']
        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        pod = self._get_pod_by_app_name(app_name)
        if not pod:
            print("")
            print("App '%s' is not running." % app_name)
            print("")
            return
        if not app_port:
            svc = self._get_svc_by_app_name(app_name)
            if not svc:
                print("")
                print("App '%s' proxy port cannot be found." % app_name)
                print("")
                return
            app_port = svc.spec.ports[0].target_port

        if not local_port:
            print("")
            print("Proxying local port '<randomly-chosen>' to app '%s' port '%s' using pod '%s'." % (app_port, app_name, pod.metadata.name))
            print("")
            print("Use 'http://127.0.0.1:<randomly-chosen>' to access app '%s' on port '%s'." % (app_name, app_port))
            print("")
            print("If you break out of this terminal, your proxy session will end.")
            print("")
            subprocess.call('kubectl port-forward %s :%s' % (pod.metadata.name, app_port), shell=True)
            print("")
        else:
            print("")
            print("Proxying local port '%s' to app '%s' port '%s' using pod '%s'." % (local_port, app_port, app_name, pod.metadata.name))
            print("")
            print("Use 'http://127.0.0.1:%s' to access app '%s' on port '%s'." % (local_port, app_name, app_port))
            print("")
            print("If you break out of this terminal, your proxy session will end.")
            print("")
            subprocess.call('kubectl port-forward %s %s:%s' % (pod.metadata.name, local_port, app_port), shell=True)
            print("")


    # TODO:  Start an airflow job
    def flow(self,
             flow_name):
        print("")
        print("Submit airflow coming soon!")


    # TODO:  Submit a spark job
    def submit(self,
               replicas):
        print("Submit spark job coming soon!")


    def top(self,
            app_name=None):

        self.system(app_name)


    def system(self,
               app_name=None):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured 'pio init-cluster'.")
            print("")
            return

        if (app_name):
            print("")
            print("Retrieving system resources used by app '%s'." % app_name)
            print("")
            self._get_app_resources(app_name)
            print("")
            print("Retrieving system resources for cluster.")
            print("")
            self._get_cluster_resources()
        else:
            print("")
            print("Retrieving only system resources for cluster.  Use '--app-name' for app-level, as well.")
            print("")
            self._get_cluster_resources()
        print("")


    def _get_cluster_resources(self):
        subprocess.call("kubectl top node", shell=True)
        print("")
        print("If you see an error above, you need to start Heapster with 'pio start heapster'.")
        print("")
>>>>>>> fluxcapacitor/master


<<<<<<< HEAD
        if 'http:' in pio_home or 'https:' in pio_home:
            pio_home = os.path.expandvars(pio_home)
            pio_home = os.path.expanduser(pio_home)
            pio_home = os.path.abspath(pio_home)

        config_dict = {'pio_home': pio_home, 
                       'pio_runtime_version': pio_runtime_version, 
                       'kube_cluster_context': kube_cluster_context, 
                       'kube_namespace': kube_namespace}
        self.config_merge_dict(config_dict)
        print("\n")
        pprint(self.config_get_all())
        print("\n")
=======
    def _get_app_resources(self,
                           app_name):

        pio_api_version = self._get_full_config()['pio_api_version']
>>>>>>> fluxcapacitor/master

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured 'pio init-cluster'.")
            print("")
            return

<<<<<<< HEAD
    def  model_init(self,
=======
        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()
        
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if (app_name in pod.metadata.name):
                    subprocess.call("kubectl top pod %s" % pod.metadata.name, shell=True)
        print("")


    def join(self,
             federation):
        print("")
        print("Federation joining coming soon!")
        print("")


    def up(self,
           provider='aws',
           ssh_public_key='~/.ssh/id_rsa.pub',
           initial_worker_count='1',
#           min_worker_count='1',
#           max_worker_count='1',
           worker_zones='us-west-2a,us-west-2b',
           worker_type='r2.2xlarge',
           master_zones='us-west-2c',
           master_type='t2.medium',
#           dns_zone='',
#           vpc='',
           kubernetes_version='1.6.2',
           kubernetes_image='kope.io/k8s-1.5-debian-jessie-amd64-hvm-ebs-2017-01-09'):
        try:
            kops_cluster_name = self._get_full_config()['kops_cluster_name']
            kops_state_store = self._get_full_config()['kops_state_store']

            if not kops_ssh_public_key:
                subprocess.call("ssh-keygen -t rsa", shell=True)
                ssh_public_key = '~/.ssh/id_rsa.pub'

            subprocess.call("aws configure", shell=True)
            subprocess.call("aws s3 mb %s" % kops_state_store, shell=True)

            subprocess.call("kops create cluster --ssh-public-key %s --node-count %s --zones %s --master-zones %s --node-size %s --master-size %s --kubernetes-version %s --image %s --state %s --name %s" % (ssh_public_key, initial_worker_count, worker_zones, master_zones, worker_type, master_type, kubernetes_version, kubernetes_image, kops_state_store, kops_cluster_name), shell=True)
            subprocess.call("kops update --state %s cluster %s --yes" % (kops_state_store, kops_cluster_name), shell=True)
            subprocess.call("kubectl config set-cluster %s --insecure-skip-tls-verify=true" % kops_cluster_name)
            print("")
            print("Cluster is being created.  This may take a few mins.")
            print("")
            print("Once the cluster is up, run 'kubectl cluster-info' for the Kubernetes-dashboard url.")
            print("Username is 'admin'.")
            print("Password can be retrieved with 'kops get secrets kube --type secret -oplaintext --state %s'" % kops_state_store)
        except:
            print("")
            print("Kops needs to be configured with 'pio init-kops'.")
            print("")
            return
           

    def init_kops(self,
                  kops_cluster_name,
                  kops_state_store):
        config_dict = {'kops_cluster_name': kops_cluster_name,
                       'kops_state_store': kops_state_store}
        self._merge_config_dict(config_dict)
        print("")
        pprint(self._get_full_config())
        print("")

       
    def instancegroups(self):
        try:
            kops_cluster_name = self._get_full_config()['kops_cluster_name']
            kops_state_store = self._get_full_config()['kops_state_store']
            
            subprocess.call("kops --state %s --name %s get instancegroups" % (kops_state_store, kops_cluster_name), shell=True)
            print("")
        except:
            print("")
            print("Kops needs to be configured with 'pio init-kops'.")
            print("")
            return


    def clusters(self):
        try:
            kops_cluster_name = self._get_full_config()['kops_cluster_name']
            kops_state_store = self._get_full_config()['kops_state_store']

            subprocess.call("kops --state %s --name %s get clusters" % (kops_state_store, kops_cluster_name), shell=True)
            print("")
        except:
            print("")
            print("Kops needs to be configured with 'pio init-kops'.")
            print("")
            return
 

    def federations(self):
        try:
            kops_cluster_name = self._get_full_config()['kops_cluster_name']
            kops_state_store = self._get_full_config()['kops_state_store']

            subprocess.call("kops --state %s --name %s get federations" % (kops_state_store, kops_cluster_name), shell=True)
            print("")
        except:
            print("")
            print("Kops needs to be configured with 'pio init-kops'.")
            print("")
            return


    def secrets(self):
        try:
            kops_cluster_name = self._get_full_config()['kops_cluster_name']
            kops_state_store = self._get_full_config()['kops_state_store']

            subprocess.call("kops --state %s --name %s get secrets" % (kops_state_store, kops_cluster_name), shell=True)
            print("")
        except:
            print("")
            print("Kops needs to be configured with 'pio init-kops'.")
            print("")
            return


    def init_pio(self,
                 pio_api_version,
                 pio_git_home,
                 pio_git_version):
        config_dict = {'pio_api_version': pio_api_version,
                       'pio_git_home': pio_git_home,
                       'pio_git_version': pio_git_version}
        self._merge_config_dict(config_dict)
        print("")
        pprint(self._get_full_config())
        print("")


    def init_cluster(self,
                     kube_cluster_context,
                     kube_namespace):
        pio_api_version = self._get_full_config()['pio_api_version']
        config_dict = {'kube_cluster_context': kube_cluster_context, 
                       'kube_namespace': kube_namespace}
        self._merge_config_dict(config_dict)
        print("")
        pprint(self._get_full_config())
        print("")


    def init_model(self,
>>>>>>> fluxcapacitor/master
                   model_server_url,
                   model_type,
                   model_namespace,
                   model_name,
                   model_input_mime_type='application/json',
                   model_output_mime_type='application/json'):

        pio_api_version = self._get_full_config()['pio_api_version']

        config_dict = {"model_server_url": model_server_url, 
                       "model_type": model_type,
                       "model_namespace": model_namespace,
                       "model_name": model_name,
                       "model_input_mime_type": model_input_mime_type,
                       "model_output_mime_type": model_output_mime_type,
        }

<<<<<<< HEAD
        self.config_merge_dict(config_dict)
        print("\n")
        pprint(self.config_get_all())
        print("\n")


    def model_deploy(self,
                     model_version, 
                     model_path,
                     request_timeout=600):
=======
        self._merge_config_dict(config_dict)
        print("")
        pprint(self._get_full_config())
        print("")


    # TODO:  from_git=True/False (include git_commit_hash, use python git API? Perform immutable deployment??)
    #        from_docker=True/False (include image name, version)
    #        canary=True/False
    def deploy(self,
               model_version, 
               model_path,
               request_timeout=600):
>>>>>>> fluxcapacitor/master

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
<<<<<<< HEAD
            model_server_url = self.config_get_all()['model_server_url']
            model_type = self.config_get_all()['model_type']
            model_namespace = self.config_get_all()['model_namespace']
            model_name = self.config_get_all()['model_name']
=======
            model_server_url = self._get_full_config()['model_server_url']
            model_type = self._get_full_config()['model_type']
            model_namespace = self._get_full_config()['model_namespace']
            model_name = self._get_full_config()['model_name']
>>>>>>> fluxcapacitor/master
        except:
            print("")
            print("Model needs to be configured with 'pio init-model'.")
            print("")
            return

<<<<<<< HEAD
#        pprint(self.config_get_all())

=======
>>>>>>> fluxcapacitor/master
        model_path = os.path.expandvars(model_path)
        model_path = os.path.expanduser(model_path)
        model_path = os.path.abspath(model_path)

        print('model_version: %s' % model_version)
        print('model_path: %s' % model_path)
        print('request_timeout: %s' % request_timeout)

        if (os.path.isdir(model_path)):
            compressed_model_bundle_filename = 'bundle-%s-%s-%s-%s.tar.gz' % (model_type, model_namespace, model_name, model_version)

<<<<<<< HEAD
            print("Compressing '%s' into '%s'..." % (model_path, compressed_model_bundle_filename))  
            print("")
            with tarfile.open(compressed_model_bundle_filename, 'w:gz') as tar:
                tar.add(model_path, arcname='.')
            print("...Done!")
            model_file = compressed_model_bundle_filename
            upload_key = 'bundle'
=======
            print("")
            print("Compressing model bundle '%s' to '%s'." % (model_path, compressed_model_bundle_filename))  
            print("")
            with tarfile.open(compressed_model_bundle_filename, 'w:gz') as tar:
                tar.add(model_path, arcname='.')
            model_file = compressed_model_bundle_filename
            upload_key = 'file'
>>>>>>> fluxcapacitor/master
            upload_value = compressed_model_bundle_filename
        else:
            model_file = model_path
            upload_key = 'file'
            upload_value = os.path.split(model_path)

<<<<<<< HEAD
        with open(model_file, 'rb') as fh:
            files = [(upload_key, (upload_value, fh))]

            full_model_server_url = "%s/%s/model/deploy/%s/%s/%s/%s" % (model_server_url, pio_api_version, model_type, model_namespace, model_name, model_version)
            print("Deploying model bundle '%s' to '%s'..." % (model_file, full_model_server_url))
            print("")
            headers = {'Accept': 'application/json'}
            response = requests.post(url=full_model_server_url, 
                                     headers=headers, 
                                     files=files, 
                                     timeout=request_timeout)
            pprint(response.text)
            print("...Done!")

        if (os.path.isdir(model_path)):
            print("Removing model bundle '%s'..." % model_file)
            os.remove(model_file)
            print("...Done!")

        print("\n")


    def model_predict(self, 
                      model_version, 
                      model_input_file_path,
                      request_timeout=30):
=======
        full_model_url = "%s/%s/model/deploy/%s/%s/%s/%s" % (model_server_url, pio_api_version, model_type, model_namespace, model_name, model_version)

        with open(model_file, 'rb') as fh:
            files = [(upload_key, (upload_value, fh))]
            print("")
            print("Deploying model '%s' to '%s'." % (model_file, full_model_url))
            print("")
            headers = {'Accept': 'application/json'}
            try:
                response = requests.post(url=full_model_url, 
                                         headers=headers, 
                                         files=files, 
                                         timeout=request_timeout)
                if response.text:
                    pprint(response.text)
                else:
                    print("")
                    print("Success!")
                    print("")
                    print("Predict with 'pio predict' or POST to '%s'" % full_model_url.replace('/deploy/','/predict/'))
                    print("")
            except IOError as e:
                print("Error while deploying model.  Timeout errors are usually OK.\nError: '%s'" % str(e))
                print("")
                print("Wait a bit, then try to predict with 'pio predict' or POST to '%s'" % full_model_url)
                print("")   
 
        if (os.path.isdir(model_path)):
            print("")
            print("Cleaning up compressed model bundle '%s'..." % model_file)
            print("")
            os.remove(model_file)


    def predict(self, 
                model_version, 
                model_input_filename,
                request_timeout=30):
>>>>>>> fluxcapacitor/master

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
<<<<<<< HEAD
            model_server_url = self.config_get_all()['model_server_url']
            model_type = self.config_get_all()['model_type']
            model_namespace = self.config_get_all()['model_namespace']
            model_name = self.config_get_all()['model_name']
            model_input_mime_type = self.config_get_all()['model_input_mime_type']
            model_output_mime_type = self.config_get_all()['model_output_mime_type']
=======
            model_server_url = self._get_full_config()['model_server_url']
            model_type = self._get_full_config()['model_type']
            model_namespace = self._get_full_config()['model_namespace']
            model_name = self._get_full_config()['model_name']
            model_input_mime_type = self._get_full_config()['model_input_mime_type']
            model_output_mime_type = self._get_full_config()['model_output_mime_type']
>>>>>>> fluxcapacitor/master
        except:
            print("")
            print("Model needs to be configured with 'pio model-init'.")
            print("")
            return

<<<<<<< HEAD
#        pprint(self.config_get_all())

=======
>>>>>>> fluxcapacitor/master
        print('model_version: %s' % model_version)
        print('model_input_filename: %s' % model_input_filename)
        print('request_timeout: %s' % request_timeout)

<<<<<<< HEAD
        full_model_server_url = "%s/%s/model/predict/%s/%s/%s/%s" % (model_server_url, pio_api_version, model_type, model_namespace, model_name, model_version)

        print("Predicting file '%s' with model '%s/%s/%s' at '%s'..." % (model_input_file_path, model_type, model_namespace, model_name, full_model_server_url))
=======
        full_model_url = "%s/%s/model/predict/%s/%s/%s/%s" % (model_server_url, pio_api_version, model_type, model_namespace, model_name, model_version)
        print("")
        print("Predicting file '%s' with model '%s/%s/%s/%s' at '%s'..." % (model_input_filename, model_type, model_namespace, model_name, model_version, full_model_url))
>>>>>>> fluxcapacitor/master
        print("")
        with open(model_input_filename, 'rb') as fh:
            model_input_binary = fh.read()

        headers = {'Content-type': model_input_mime_type, 'Accept': model_output_mime_type} 
        response = requests.post(url=full_model_url, 
                                 headers=headers, 
                                 data=model_input_binary, 
                                 timeout=request_timeout)
        pprint(response.text)
<<<<<<< HEAD
        print("...Done!")
        print("\n")


    def cluster_view(self):
        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_cluster_context = self.config_get_all()['kube_cluster_context']
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

        print("\n")
        print("Config")
        print("******")
        pprint(self.config_get_all())

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()
        print("\n")
        print("Apps")
        print("****")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace, 
                                                                      watch=False, 
                                                                      pretty=True)
            for deploy in response.items:
                print("%s (%s of %s replicas available)" % (deploy.metadata.name, deploy.status.ready_replicas, deploy.status.replicas))

        print("\n")
        print("Internal DNS (Public DNS)")
        print("*************************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_service(namespace=kube_namespace, watch=False, pretty=True)
            for svc in response.items:
                ingress = 'Not public' 
                if svc.status.load_balancer.ingress and len(svc.status.load_balancer.ingress) > 0:
                    if (svc.status.load_balancer.ingress[0].hostname):
                        ingress = svc.status.load_balancer.ingress[0].hostname
                    if (svc.status.load_balancer.ingress[0].ip):
                        ingress = svc.status.load_balancer.ingress[0].ip               
                print("%s (%s)" % (svc.metadata.name, ingress))

        print("\n")
        print("Pods")
        print("****")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                print("%s (%s)" % (pod.metadata.name, pod.status.phase))
        print("\n")


    def apps_available(self):
        pio_api_version = self.config_get_all()['pio_api_version']
=======
        print("")


    def cluster(self):
        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        self.apps()

        print("DNS Internal (Public)")
        print("**************************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_service(namespace=kube_namespace, watch=False, pretty=True)
            for svc in response.items:
                ingress = 'Not public' 
                if svc.status.load_balancer.ingress and len(svc.status.load_balancer.ingress) > 0:
                    if (svc.status.load_balancer.ingress[0].hostname):
                        ingress = svc.status.load_balancer.ingress[0].hostname
                    if (svc.status.load_balancer.ingress[0].ip):
                        ingress = svc.status.load_balancer.ingress[0].ip               
                print("%s (%s)" % (svc.metadata.name, ingress))

        print("")
        print("Running Pods")
        print("************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                print("%s (%s)" % (pod.metadata.name, pod.status.phase))

        print("")
        print("Nodes")
        print("*****")
        self._get_all_nodes()
        
        print("")
        print("Config")
        print("******")
        pprint(self._get_full_config())
        print("")


    def _get_pod_by_app_name(self,
                             app_name):

        pio_api_version = self._get_full_config()['pio_api_version']
        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        found = False 
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if app_name in pod.metadata.name:
                    found = True
                    break
        if found:
            return pod
        else:
            return None


    def _get_svc_by_app_name(self,
                             app_name):

        pio_api_version = self._get_full_config()['pio_api_version']
        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        found = False
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_service(namespace=kube_namespace, watch=False, pretty=True)
            for svc in response.items:
                if app_name in svc.metadata.name:
                    found = True
                    break
        if found:
            return svc 
        else:
            return None


    def _get_all_available_apps(self):
        pio_api_version = self._get_full_config()['pio_api_version']

        available_apps = PioCli._kube_deploy_registry.keys()
        for app in available_apps:
            print(app)


    def nodes(self):
        pio_api_version = self._get_full_config()['pio_api_version']
>>>>>>> fluxcapacitor/master

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

<<<<<<< HEAD
#        pprint(self.config_get_all())
=======
        print("")
        print("Nodes")
        print("*****")
        self._get_all_nodes()
        print("")


    def _get_all_nodes(self):
        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return
>>>>>>> fluxcapacitor/master

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
<<<<<<< HEAD
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace,
                                                                  watch=False,
                                                                  pretty=True)
            for deploy in response.items:
                print("%s (%s of %s replicas available)" % (deploy.metadata.name, deploy.status.ready_replicas, deploy.status.replicas))
        print("\n")

    def apps_deployed(self):
        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_cluster_context = self.config_get_all()['kube_cluster_context']
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

#        pprint(self.config_get_all())

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()
        print("\nApps")
        print("****")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace,
                                                                      watch=False,
                                                                      pretty=True)
            for deploy in response.items:
                print("%s (%s of %s replicas available)" % (deploy.metadata.name, deploy.status.ready_replicas, deploy.status.replicas))
        print("\n")
   
 
    def app_shell(self,
                  app_name):

        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_cluster_context = self.config_get_all()['kube_cluster_context']
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

        pprint(self.config_get_all())
=======
            response = kubeclient_v1.list_node(watch=False, pretty=True)
            for node in response.items:
                print("%s (%s)" % (node.metadata.labels['kubernetes.io/hostname'], node.metadata.labels['kubernetes.io/role']))


    def apps(self):
        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        print("")
        print("All Available Apps")
        print("******************")
        self._get_all_available_apps()

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        print("")
        print("Started Apps")
        print("************")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace,
                                                                      watch=False,
                                                                      pretty=True)
            for deploy in response.items:
                print("%s (%s of %s replicas are running)" % (deploy.metadata.name, deploy.status.ready_replicas, deploy.status.replicas))
        print("")
   

    def shell(self,
              app_name):

        self.connect(app_name)

 
    def connect(self,
                app_name):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return
>>>>>>> fluxcapacitor/master

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
<<<<<<< HEAD
=======
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if app_name in pod.metadata.name:
                    break
            print("")
            print("Connecting to '%s'" % pod.metadata.name)      
            print("")
            subprocess.call("kubectl exec -it %s bash" % pod.metadata.name, shell=True)
        print("")
>>>>>>> fluxcapacitor/master

            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if app_name in pod.metadata.name:
                    break
            print("Shelling into '%s' (%s)" % (pod.metadata.name, pod.status.phase))      
            subprocess.call("kubectl exec -it %s bash" % pod.metadata.name, shell=True)
        print("\n")

<<<<<<< HEAD

    def app_logs(self,
                 app_name):

        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_cluster_context = self.config_get_all()['kube_cluster_context']
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

#        pprint(self.config_get_all())

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            for pod in response.items:
                if app_name in pod.metadata.name:
                    break
            print("Tailing logs on '%s' (%s)" % (pod.metadata.name, pod.status.phase))
            subprocess.call("kubectl logs -f %s" % pod.metadata.name, shell=True)

        print("\n")


    def app_scale(self,
                  app_name,
                  replicas):

        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

#        pprint(self.config_get_all())

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace, watch=False, pretty=True)
            for deploy in response.items:
                if app_name in deploy.metadata.name:
                    break
            print("Scaling '%s' to %s replicas..." % (deploy.metadata.name, replicas))
            subprocess.call("kubectl scale deploy %s --replicas=%s" % (deploy.metadata.name, replicas), shell=True)

        print("\n") 

    def get_config_yamls(self, 
                         app_name):
        return [] 


    def get_secret_yamls(self, 
                         app_name):
        return []


    def get_deploy_yamls(self, 
                         app_name):
        (deploy_yamls, dependencies) = PioCli.kube_deploy_registry[app_name]
        if len(dependencies) > 0:
            for dependency in dependencies:
                deploy_yamls = deploy_yamls + self.get_deploy_yamls(dependency)
        return deploy_yamls 


    def get_svc_yamls(self, 
                      app_name):
        (svc_yamls, dependencies) = PioCli.kube_svc_registry[app_name]
        if len(dependencies) > 0:
            for dependency in dependencies:
                svc_yamls = svc_yamls + self.get_svc_yamls(dependency)
        return svc_yamls 


    def app_deploy(self,
                   app_name):
=======
    def logs(self,
             app_name):
>>>>>>> fluxcapacitor/master

        pio_api_version = self._get_full_config()['pio_api_version']

<<<<<<< HEAD
        try: 
            kube_namespace = self.config_get_all()['kube_namespace']

            pio_home = self.config_get_all()['pio_home']

            if 'http:' in pio_home or 'https:' in pio_home:
                pio_home = os.path.expandvars(pio_home)
                pio_home = os.path.expanduser(pio_home)
                pio_home = os.path.abspath(pio_home)
=======
        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
>>>>>>> fluxcapacitor/master
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

<<<<<<< HEAD
#        pprint(self.config_get_all())
        print("Deploying app... '%s'" % app_name)

        kubeconfig.load_kube_config()

        config_yaml_filenames = [] 
        secret_yaml_filenames = [] 
        deploy_yaml_filenames = []
        svc_yaml_filenames = [] 
       
        config_yaml_filenames = config_yaml_filenames + self.get_config_yamls(app_name)
        secret_yaml_filenames = secret_yaml_filenames + self.get_secret_yamls(app_name)
        deploy_yaml_filenames = deploy_yaml_filenames + self.get_deploy_yamls(app_name)
        svc_yaml_filenames = svc_yaml_filenames + self.get_svc_yamls(app_name)

        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        #for config_yaml_filename in config_yaml_filenames:
            # TODO
        #    return 

        #for secret_yaml_filename in secret_yaml_filenames:
            # TODO 
        #    return

        print(deploy_yaml_filenames)
        print(svc_yaml_filenames)

        for deploy_yaml_filename in deploy_yaml_filenames:
            try:
                # TODO: handle http: or https:
                if 'http:' in pio_home or 'https:' in pio_home:
                    # TODO: handle http: or https:
                    pass
                else:
                    with open(os.path.join(pio_home, deploy_yaml_filename)) as fh:
                        deploy_yaml = yaml.load(fh)
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            response = kubeclient_v1_beta1.create_namespaced_deployment(body=deploy_yaml, 
                                                                                        namespace=kube_namespace, 
                                                                                        pretty=True)
                            pprint(response) 
            except ApiException as e: 
                    print("Deployment not created for '%s':\n%s\n" % (deploy_yaml_filename, str(e)))

        for svc_yaml_filename in svc_yaml_filenames:
            try:
                # TODO: handle http: or https:
                if 'http:' in pio_home or 'https:' in pio_home:
                    # TODO: handle http: or https: 
                    pass
                else:
                    with open(os.path.join(pio_home, svc_yaml_filename)) as fh:
                        svc_yaml = yaml.load(fh)
                        response = kubeclient_v1.create_namespaced_service(body=svc_yaml, 
                                                                           namespace=kube_namespace, 
                                                                           pretty=True)
                        pprint(response)
            except ApiException as e: 
                print("Service not created for '%s':\n%s\n" % (svc_yaml_filename, str(e)))
=======
        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_namespaced_pod(namespace=kube_namespace, watch=False, pretty=True)
            found = False
            for pod in response.items:
                if app_name in pod.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Tailing logs on '%s'." % pod.metadata.name)
                print("")
                subprocess.call("kubectl logs -f %s" % pod.metadata.name, shell=True)
                print("")
            else:
                print("")
                print("App '%s' is not running." % app_name)
                print("")


    def scale(self,
              app_name,
              replicas):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace, watch=False, pretty=True)
            found = False
            for deploy in response.items:
                if app_name in deploy.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Scaling app '%s' to '%s' replicas." % (deploy.metadata.name, replicas))
                print("")
                subprocess.call("kubectl scale deploy %s --replicas=%s" % (deploy.metadata.name, replicas), shell=True)
                print("")
                print("Check status with 'pio cluster'.")
                print("")
            else:
                print("")
                print("App '%s' is not running." % app_name)
                print("") 


    def volumes(self):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        print("")
        print("Volumes")
        print("*******")
        self._get_all_volumes()

        print("")
        print("Volume Claims")
        print("*************")
        self._get_all_volume_claims()
        print("")


    def _get_all_volumes(self):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_persistent_volume(watch=False,
                                                            pretty=True)
            for claim in response.items:
                print("%s" % (claim.metadata.name))
        print("")


    def _get_all_volume_claims(self):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1.list_persistent_volume_claim_for_all_namespaces(watch=False,
                                                                                     pretty=True)
            for claim in response.items:
                print("%s" % (claim.metadata.name))
        print("")
>>>>>>> fluxcapacitor/master

        self.cluster_view()

<<<<<<< HEAD
        print("\n")


    def app_undeploy(self,
                     app_name):

        pio_api_version = self.config_get_all()['pio_api_version']

        try:
            kube_namespace = self.config_get_all()['kube_namespace']
        except:
            print("Cluster needs to be initialized.")
            return

#        pprint(self.config_get_all())

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace, watch=False, pretty=True)
            for deploy in response.items:
                if app_name in deploy.metadata.name:
                    break
            print("Deleting '%s'" % deploy.metadata.name)
            subprocess.call("kubectl delete deploy %s" % deploy.metadata.name, shell=True)

        self.cluster_view()

        print("\n")
        print("Note:  There may be a delay in status change above ^^.")

        print("\n")

#    def git_init(self,
#                 git_repo_base_path,
#                 git_revision='HEAD'):

#        expanded_git_repo_base_path = os.path.expandvars(git_repo_base_path)
#        expanded_git_repo_base_path = os.path.expanduser(expanded_git_repo_base_path)
#        expanded_git_repo_base_path = os.path.abspath(expanded_git_repo_base_path)

#        pio_api_version = self.config_get_all()['pio_api_version']

#        print("git_repo_base_path: '%s'" % git_repo_base_path)
#        print("expanded_git_repo_base_path: '%s'" % expanded_git_repo_base_path)
#        print("git_revision: '%s'" % git_revision)

#        git_repo = Repo(expanded_git_repo_base_path, search_parent_directories=True)
 
#        config_dict = {'git_repo_base_path': git_repo.working_tree_dir , 'git_revision': git_revision}

#        self.config_merge_dict(config_dict)
#        pprint(self.config_get_all())
#        print("\n")

#    def git_view(self):
#        pio_api_version = self.config_get_all()['pio_api_version']
#        try: 
#            git_repo_base_path = self.config_get_all()['git_repo_base_path']

#            expanded_git_repo_base_path = os.path.expandvars(git_repo_base_path)
#            expanded_git_repo_base_path = os.path.expanduser(expanded_git_repo_base_path)
#            expanded_git_repo_base_path = os.path.abspath(expanded_git_repo_base_path)

#            git_revision = self.config_get_all()['git_revision']
#        except:
#            print("Git needs to be initialized.")
#            return

#        pprint(self.config_get_all())

=======
    def _get_config_yamls(self, 
                         app_name):
        return [] 


    def _get_secret_yamls(self, 
                         app_name):
        return []


    def _get_deploy_yamls(self, 
                         app_name):
        try:
            (deploy_yamls, dependencies) = PioCli._kube_deploy_registry[app_name]
        except:
            dependencies = []
            deploy_yamls = []

        if len(dependencies) > 0:
            for dependency in dependencies:
                deploy_yamls = deploy_yamls + self._get_deploy_yamls(dependency)
        return deploy_yamls 


    def _get_svc_yamls(self, 
                      app_name):
        try:
            (svc_yamls, dependencies) = PioCli._kube_svc_registry[app_name]
        except:
            dependencies = []
            svc_yamls = []
       
        if len(dependencies) > 0:
            for dependency in dependencies:
                svc_yamls = svc_yamls + self._get_svc_yamls(dependency)
        return svc_yamls


    def start(self,
              app_name):

        pio_api_version = self._get_full_config()['pio_api_version']

        try: 
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
            pio_git_home = self._get_full_config()['pio_git_home']

            if 'http:' in pio_git_home or 'https:' in pio_git_home:
                pass
            else:
                pio_git_home = os.path.expandvars(pio_git_home)
                pio_git_home = os.path.expanduser(pio_git_home)
                pio_git_home = os.path.abspath(pio_git_home)

            pio_git_version = self._get_full_config()['pio_git_version']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        config_yaml_filenames = [] 
        secret_yaml_filenames = [] 
        deploy_yaml_filenames = []
        svc_yaml_filenames = [] 
       
        config_yaml_filenames = config_yaml_filenames + self._get_config_yamls(app_name)
        secret_yaml_filenames = secret_yaml_filenames + self._get_secret_yamls(app_name)
        deploy_yaml_filenames = deploy_yaml_filenames + self._get_deploy_yamls(app_name)
        svc_yaml_filenames = svc_yaml_filenames + self._get_svc_yamls(app_name)

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        #for config_yaml_filename in config_yaml_filenames:
            # TODO
        #    return 

        #for secret_yaml_filename in secret_yaml_filenames:
            # TODO 
        #    return
        print("")
        print("Starting app '%s'." % app_name)
        print("")
        print("Ignore any 'Already Exists' errors.  These are OK.")
        print("")
        for deploy_yaml_filename in deploy_yaml_filenames:
            try:
                if 'http:' in deploy_yaml_filename or 'https:' in deploy_yaml_filename:
                    deploy_yaml_filename = deploy_yaml_filename.replace('github.com', 'raw.githubusercontent.com')
                    subprocess.call("kubectl create -f %s" % deploy_yaml_filename, shell=True)
                else:
                    if 'http:' in pio_git_home or 'https:' in pio_git_home:
                        pio_git_home = pio_git_home.replace('github.com', 'raw.githubusercontent.com')
                        subprocess.call("kubectl create -f %s/%s/%s" % (pio_git_home.rstrip('/'), pio_git_version, deploy_yaml_filename), shell=True)
                    else:
                        with open(os.path.join(pio_git_home, deploy_yaml_filename)) as fh:
                            deploy_yaml = yaml.load(fh)
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                response = kubeclient_v1_beta1.create_namespaced_deployment(body=deploy_yaml, 
                                                                                            namespace=kube_namespace, 
                                                                                            pretty=True)
                                pprint(response) 
            except ApiException as e: 
                print("")
                print("App '%s' did not start properly.\n%s" % (deploy_yaml_filename, str(e)))
                print("")

        for svc_yaml_filename in svc_yaml_filenames:
            try:
                if 'http:' in svc_yaml_filename or 'https:' in svc_yaml_filename:
                    svc_yaml_filename = svc_yaml_filename.replace('github.com', 'raw.githubusercontent.com')
                    subprocess.call("kubectl create -f %s" % svc_yaml_filename, shell=True)
                else:
                    if 'http:' in pio_git_home or 'https:' in pio_git_home:
                        pio_git_home = pio_git_home.replace('github.com', 'raw.githubusercontent.com')
                        subprocess.call("kubectl create -f %s/%s/%s" % (pio_git_home.rstrip('/'), pio_git_version, svc_yaml_filename), shell=True)
                    else:
                        with open(os.path.join(pio_git_home, svc_yaml_filename)) as fh:
                            svc_yaml = yaml.load(fh)
                            with warnings.catch_warnings():
                                warnings.simplefilter("ignore")
                                response = kubeclient_v1.create_namespaced_service(body=svc_yaml, 
                                                                                   namespace=kube_namespace, 
                                                                                   pretty=True)
                                pprint(response)
            except ApiException as e: 
                print("")
                print("App '%s' did not start properly.\n%s" % (svc_yaml_filename, str(e)))
                print("")

        print("")
        print("Check status with 'pio cluster'.")
        print("")


    def stop(self,
             app_name):

        pio_api_version = self._get_full_config()['pio_api_version']

        try:
            kube_cluster_context = self._get_full_config()['kube_cluster_context']
            kube_namespace = self._get_full_config()['kube_namespace']
        except:
            print("")
            print("Cluster needs to be configured with 'pio init-cluster'.")
            print("")
            return

        kubeconfig.load_kube_config()
        kubeclient_v1 = kubeclient.CoreV1Api()
        kubeclient_v1_beta1 = kubeclient.ExtensionsV1beta1Api()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=kube_namespace, watch=False, pretty=True)
            found = False
            for deploy in response.items:
                if app_name in deploy.metadata.name:
                    found = True
                    break
            if found:
                print("")
                print("Stopping app '%s'." % deploy.metadata.name)
                subprocess.call("kubectl delete deploy %s" % deploy.metadata.name, shell=True)
                print("")
                print("Check status with 'pio cluster'.")
                print("")
            else:
                print("")
                print("App '%s' is not running." % app_name)
                print("")


#    def git_init(self,
#                      git_repo_base_path,
#                      git_revision='HEAD'):

#        expanded_git_repo_base_path = os.path.expandvars(git_repo_base_path)
#        expanded_git_repo_base_path = os.path.expanduser(expanded_git_repo_base_path)
#        expanded_git_repo_base_path = os.path.abspath(expanded_git_repo_base_path)

#        pio_api_version = self._get_full_config()['pio_api_version']

#        print("git_repo_base_path: '%s'" % git_repo_base_path)
#        print("expanded_git_repo_base_path: '%s'" % expanded_git_repo_base_path)
#        print("git_revision: '%s'" % git_revision)

#        git_repo = Repo(expanded_git_repo_base_path, search_parent_directories=True)
 
#        config_dict = {'git_repo_base_path': git_repo.working_tree_dir , 'git_revision': git_revision}

#        self._merge_config_dict(config_dict)
#        pprint(self._get_full_config())
#        print("")

#    def git(self):
#        pio_api_version = self._get_full_config()['pio_api_version']
#        try: 
#            git_repo_base_path = self._get_full_config()['git_repo_base_path']

#            expanded_git_repo_base_path = os.path.expandvars(git_repo_base_path)
#            expanded_git_repo_base_path = os.path.expanduser(expanded_git_repo_base_path)
#            expanded_git_repo_base_path = os.path.abspath(expanded_git_repo_base_path)

#            git_revision = self._get_full_config()['git_revision']
#        except:
#            print("Git needs to be configured with 'pio git-init'.")
#            return

#        pprint(self._get_full_config())

>>>>>>> fluxcapacitor/master
#        git_repo = Repo(expanded_git_repo_base_path, search_parent_directories=False)
#        ch = git_repo.commit(git_revision)

#        print("Git repo base path: '%s'" % git_repo_base_path)
#        print("Git revision: '%s'" % git_revision)
#        print("Git commit message: '%s'" % ch.message)
#        print("Git commit hash: '%s'" % ch.hexsha)
<<<<<<< HEAD
#        print("\n")
=======
#        print("")
>>>>>>> fluxcapacitor/master


def main():
    fire.Fire(PioCli)


if __name__ == '__main__':
    main()
