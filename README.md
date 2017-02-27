# App Engine Workshop



## Prerequisites

### Software
For this workshop, you will need the [Google Cloud SDK](https://cloud.google.com/sdk/), [git](https://git-scm.com/), and [Python 2.7](https://www.python.org/) with [pip](https://pip.pypa.io/en/stable/) installed.
*(All steps in the workshop are tested using Google Cloud SDK 143.0.1 and Python 2.7.13).*

It should work by using the [Cloud Shell](https://cloud.google.com/shell/docs/) in the [Console](https://console.cloud.google.com), but it has not been tested.

### Initialize
Go to the [console](https://console.cloud.google.com) and create a new project on your account.
(It is possible to [create projects with the SDK](https://cloud.google.com/sdk/gcloud/reference/alpha/projects/create), but this feature is in alpha and may change without notice.
It might also be a bit tricky to get a unique project id).

Setup the Cloud SDK on your machine and connect it to your user and newly created project
```
gcloud init
```

Clone this repository
```
git clone git@github.com:ChristofferKarlsson/app-engine-workshop.git
cd app-engine-workshop
```



## Using the Cloud SDK

### Basics
Show info about the `gcloud` command
```
gcloud -h
```
This give a short list of available commands.

For a more filled out description, you can instead append the `--help` flag, which will give you a `man` like description
```
gcloud --help
```

You can apply `-h` and `--help` to any command/group in the SDK
```
gcloud config -h
```

Also, in the Cloud Shell (and if you have set it up properly on your local machine), you can use the tab autocomplete to autocomplete a command, or to get a list of available commands
```
gcloud config <tab><tab>
```

To enable autocomplete on your own machine, you have to source the file:
```
source /path/to/google-cloud-sdk/completion.bash.inc
or
source /path/to/google-cloud-sdk/completion.zsh.inc
```

If you have not written a complete command, or have some typo in your command, the SDK tool will often help you by printing some informative text along with the same info as in `-h`
```
gcloud config
gcloud config get-valu
```



## Explore the app
In the cloned repo you will see two folders, in the first part and most of this workshop, you will work in the the `main` folder.
Unless anything other is stated, all commands are to be executed in this folder.

In here, you have the following files:

| File | Description |
| ---- | ----------- |
| app.yaml | Your App Engine config for this app (the default service) |
| appengine_config.py | This file makes sure your third party libraries are loaded (in this case, [flask](http://flask.pocoo.org/)) |
| main.py | The Python application, which is built using the micro web framework [flask](http://flask.pocoo.org/) |
| requirements.txt | A typical way of defining a Python application libraries |

The application, `main.py` in this case, contains a couple of endpoints that the workshop is built upon.
Most of what happens in the application is pretty self explaining and you do not need to know exactly what is happening.
The focus on the workshop will be on App Engine and not coding.


### app.yaml
The most interesting file is the app.yaml, which currently contains a very basic config (please note that app.yaml is not used in all App Engine runtimes. In Java, the corresponding config will be in xml files).
```
runtime: python27
api_version: 1
threadsafe: true

handlers:
- url: .*
  script: main.app
```

The `runtime` defines the runtime this app is intended to run in (for all runtimes other than Java, you specify it here).
There is currently only one API for the Python runtime, so the `api_version` is set to 1.
The `threadsafe` option defines whether your application can use concurrent requests or not.

The `handlers` part is where you define the entrances to your application.
Here you can define one or more URL regex patterns and how to handle them.
In this example, there is a catch-all `.*` regex that sends all requests to `main.app`, which is the `main.py` application.

There are A LOT more options that can be configured in the app.yaml, some which will be explored throughout this workshop.
If you want to check out all the available options, you will find it in the [official documentation](https://cloud.google.com/appengine/docs/standard/python/config/appref).


### Installing the requirements
To install the app's libraries, run the following command
```
pip install -t lib -r requirements.txt
```
The `-t lib` flag makes pip install the libraries to a folder in the current directory called lib, and the `-r requirements.txt` flag says to install all libraries defined in the text file.

It is not possible to install libraries in the App Engine Python runtime, which is why you have to download them to a directory.
By doing it this way, the lib directory will be uploaded when you deploy the app, and your app can use the libraries.

**A note on using virtualenv:** Since you are installing all libraries to a local folder, there is no need to use virtualenv.
However, if you for some reason want to use it anyway, you might run into some trouble launching the development server (at least I did).
If you get some import errors when running the development server, check out the Troubleshooting part at the end of this readme.



## Running the app locally
The Cloud SDK comes with a [development server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server) that can be run locally and allows you to run an application in an App Engine simulated environment.

To start the development server and run your application, execute
```
dev_appserver.py .
```
You can execute the command above either pointing at a directory where app.yaml can be found, or specify the app.yaml itself, which is needed when using multiple services.

If you want to specify the port for your app, you can do it by using the `--port` flag
```
dev_appserver.py --port=5000 .
```

Upon execution, you should get output that looks something like this:
```
$ dev_appserver.py
...
INFO     2017-02-24 16:58:22,672 dispatcher.py:199] Starting module "default" running at: http://localhost:8080
INFO     2017-02-24 16:58:22,673 admin_server.py:116] Starting admin server at: http://localhost:8000
```
What you see here, is the app, defined as the `default` module that is running at `http://localhost:8080`, and an admin server running at `http://localhost:8000`.

Now, go check out the first two endpoints that are defined in the app:

* http://localhost:8080/
* http://localhost:8080/hello-world/

Both endpoints are just returning a simple text string.
Now, while the server is running, go change something in the response text for one of the endpoints in the `main.py` file and then reload your browser.

As you can see, the development server listens to file changes and will automatically reload when you make changes. Sweet! :)

You can also go and check out the admin server: http://localhost:8000. Here you will find some information about your development environment.
It is rather empty now, and the only exciting thing you can see there is the default service and some stats of it.



## Deploy the app
Before you can deploy the app, you need to create an App Engine app in your project.
When creating an app, you define where you want it to reside, and since we live in europe, the european region is probably your best choice ;)

To create the app using the SDK
```
gcloud app create
```

And now, you are ready to deploy the actual app!
Deploying an app is just as simple as running (and answering yes on the "Do you want to continue" question):
```
gcloud app deploy
```
And that is it!
Now you have your super-awesome app deployed to App Engine, where it can handle any traffic and is automatically scaled from zero to infinity (well, almost)!

You can now check out the app by going to `http://<project-id>.appspot.com`, or open it by executing
```
gcloud app browse
```

When deploying the app, you will get some information about what you are deploying:
```
$ gcloud app deploy
You are about to deploy the following services:
 - ws-feb/default/20170225t131847 (from [/path/to/project/app.yaml])
     Deploying to URL: [https://ws-feb.appspot.com]
...
You may also view the gcloud log file, found at
[/home/user/.config/gcloud/logs/2017.02.25/13.18.44.615344.log].
...
To view your application in the web browser run:
  $ gcloud app browse
```
The information here tells you that you are about to deploy an app to the project `ws-feb`, using the `default` service.
It also tells you that the version will be numbered `20170225t131847`, and the path to your `app.yaml`.

The project used is the one that was specified earlier in your setup of the Cloud SDK.
Since no service was specified for the app, it is assigned the `default` service.
Neither was any version specified, so you get a default version that corresponds to the current date and time in the format `YYYYMMDDtHHmmSS`.

If you want to see very verbose information, such as which files that were uploaded and not, you can check the log file that is mentioned in the output: `$HOME/.config/gcloud/logs/...`.



## Update the app and re-deploy

### With automatic traffic migration
Now, go make some changes to the text that is outputted from one of the two endpoints in the `main.py` file.
Then deploy the app again, using the same command as earlier
```
gcloud app deploy
```

When the deploy is done, go visit the deployed app again (`http://<project-id>.appspot.com`) and verify that it has been updated.

What happened here, is that a new version of your app was uploaded to App Engine, on the same service and project as before.
Then App Engine, as done by default, migrated all traffic sent to your service, to be sent to this newly uploaded version.

If you examine the versions on your app now, you should see two versions, and that the traffic split is configured to send all traffic to the newest version
```
gcloud app versions list
```

The old version is still available to visit, and can be accessed by specifying the version in the URL.
Try visiting your old version, by construction the URL as `http://<version>.<project-id>.appspot.com`.

Using the `versions` command, you can also get extended information about a deployed version, containing things like who deployed it, which files it uses and where they are stored, etc.
```
gcloud app versions describe <version> --service=default
```

### Without traffic migration
As in the last step, do some more changes and deploy a new version once again. But this time, add the `--no-promote` flag to the [deploy command](https://cloud.google.com/sdk/gcloud/reference/app/deploy)
```
gcloud app deploy --no-promote
```

If you issue the `gcloud app versions list` command once again, you should see your new version, but that the version before it still has 100 % of the traffic.

Now go to `http://<project-id>.appspot.com` and verify that the app is still serving your second version. To visit your new version, again use the URL pattern `http://<version>.<project-id>.appspot.com`.

#### Promoting the new version
When switching a service to serve a new version, the traffic is switched immediately, even before the instance has been started.
Due to this, the users might notice a bit of a delay as the instance has to spin up (especially if you are having a Java application, which probably have longer startup time).

This can be avoided by using something called a [warmup request]((https://cloud.google.com/appengine/docs/python/warmup-requests/configuring)).
When enabling this, a request will be sent to the new version before sending any real user traffic there, thus letting it have some time to startup.
Enabling warmup requests is rather easy, you simply define it in your `app.yaml` file before deploying the version, using
```
inbound_services:
- warmup
```
But since Python is used here, and Python is fast, we do not care about that today ;)

Now, to the actual migration. To change all traffic to target your new version, use the following command
```
gcloud app services set-traffic default --splits <your-new-version>=1
```
This says that your *default* service should "split" the traffic 100 % to *<your-new-version>*.
If you have warmup requests activated, you can also add the `--migrate` flag to gradually migrate the traffic.

If you want to just split traffic between multiple versions (for example, to try it out on a smaller part of the requests, or to do some A/B testing) the command looks like this
```
gcloud app services set-traffic default --splits <your-old-version>=0.7,<your-new-version>=0.3
```
This will give *your-old-version* 70 % of the traffic and *your-new-version* 30 % of the traffic.

We will not go into any more details about this here today, but if you want to know more about it and how it handles connections between versions, you can checkout the official documentation on [traffic splitting](https://cloud.google.com/appengine/docs/standard/python/splitting-traffic).

A great advantage of always getting a new version when deploying your app, is that you can always roll it back easily, by setting 100 % traffic to an old version.

**A note on version naming:**
Google advices against reusing the same version name as before.
If you reuse an old version, the files of the old version will be overwritten, and while that happens, it might disrupt the traffic.
As will be described later, it is also important that your version names does not collide with your service names.


## Static files
When serving static files, you can either let your application take care of it, or you can let App Engine do it by defining them in your config.
The preferred way is to let App Engine take care of them.
By doing that, they will not consume any instance hours (what you pay for in App Engine).

To set it up, you add a handler that matches your static URL and uses the `static_dir` option to specify in which folder they are.
Add this to your `app.yaml`
```
- url: /static
  static_dir: static_files
```

You can also specify the expiration for the static files, which will set the Cache-Control and Expires HTTP headers.
It can either be done by setting the global `default_expiration` property, or by setting the `expiration` property on a specific handler.

Check the `app.yaml` reference in the [official documentation](https://cloud.google.com/appengine/docs/standard/python/config/appref#handlers_expiration) for the format and change it in your config.

There is an image added to your `static_files` directory, and an endpoint setup at `/test-static/`.
After you have setup the static dir and expiration, deploy the app again.
Then, go to the `/test-static/` endpoint and inspect the network traffic in your browser to verify that the headers are set correctly.
In Chrome, it is done by opening the developer tools, going to the network tab, reloading the page, click the image.png and then check the Headers tab.

Please note that once a static resource has been sent with a given cache, modifying the expiration and deploying the app again will not modify the already existing cache.
[You can read more about it here.](https://cloud.google.com/appengine/docs/standard/python/config/appref#handlers_expiration).



## Logging
App Engine is integrated with [Stackdriver Logging](https://cloud.google.com/logging/docs/).
All requests are logged, and you can check the logs by either opening the [Logging application](https://console.cloud.google.com/logs) in Console, or read them in your command line
```
gcloud app logs read
```

Everything that is written to the standard output will be captured in the logs.
In the Python runtime, everything that is written to standard output will be assigned an error log level.
By using the default logging library, you can define the log level yourself.
```
import logging

logging.debug('')
logging.info('')
logging.warning('')
logging.error('')
logging.critical('')
logging.exception('')
```

There is an endpoint setup at `/test-logging/`, that will fire on all levels.
Go to that URL and then go and examine your logs again.
Remember to expand the logs in the Console to see the actual messages.

I have not found a way to expand the logs and see the actual logged messages when using the SDK.
If you find out, please let me know :)



## Security and authentication

### HTTP/S
App Engine will by default let you access your app through both HTTP and HTTPS.
This option can be changed, such that your app is only accessible over HTTP, why anyone ever would want that?!
Or the better alternative, to only be accessible over HTTPS, where it also redirects (302) all HTTP requests to HTTPS.

To change the level, you add the secure flag your handle.
It has three options: `optional` (default), `never`, and `always`, which are pretty self describing.

Now add `secure: always` to your handle, deploy your app and try to access it at the regular HTTP address.

```
- url: .*
  script: main.app
  secure: always
```

The certificate that App Engine gives you is only for `*.appspot.com` and is not valid for multiple levels of subdomains, such as `https://<version>.<project-id>.appspot.com`.
If you want to access a specific version or module with a valid certificate, you can replace the dot with `-dot-`, thus getting the URL:

* `https://<version>-dot-<project-id>.appspot.com`

If you want to use your custom domain and your own certificate, it is also possible.
It will not be discussed here, but if you are interested in it, you can find more information in [the documentation](https://cloud.google.com/appengine/docs/python/console/using-custom-domains-and-ssl).



### Authentication

#### Users API
Google provides a [Users API](https://cloud.google.com/appengine/docs/standard/python/users/) that can be used to authenticate users, using their Google accounts.
Though somewhat limited (as you need a Google account), you can use it to easily add authentication to an App Engine application.

There is an endpoint at `/user/` that makes use of this API in the Python code.
If you are not logged in, it will show you a login link.
If you are logged in, it will show you some user details and a logout link.
Go check that one out and also inspect the code, to see that everything is provided through a library for this API.
(There is also a [similar library](https://cloud.google.com/appengine/docs/standard/java/users/) for Java projects).

There are also other services you can use to authenticate users, but that is out of the scope for this workshop.
If you want to know more or try it out, check the [official documentation](https://cloud.google.com/appengine/docs/standard/python/oauth/).

##### Admin vs. User
If you choose to login with the Google account that you are also using for the App Engine project, you should appear as admin.
But if you login with another account, that is not tied to the App Engine project, it should just be seen as a regular user.
If you have another Google account, you can try it out, or else ask someone else in the room to go to the URL to see it.

Granting Admin permissions to other users in your project can be done in the [IAM & Admin service](https://console.cloud.google.com/iam-admin) in the console.
If you have another user, add it here and assign it the App Engine -> App Engine Admin role, then go to the endpoint again to verify that you are now shown as admin (it might take some time to be updated).

*Besides having the role App Engine Admin, a user that has Viewer, Editor, or Owner access to your project will also an App Engine admin.*

##### Enforcing security
In your app.yaml, you can enforce security at specific URLs and require that the user is either logged in with a Google account, or has admin access to your project.
This is done by setting the `login` [option](https://cloud.google.com/appengine/docs/go/config/appref#handlers_login) on your handler, to either `optional` (default), `required`, or `admin`.
There are two endpoints setup that you can try this on, by adding the following handlers and redeploying your app
```
  # Must be be logged in with a Google account
- url: /user-area/*
  script: main.app
  login: required

  # Must be logged in with a Google account with admin privileges
- url: /secure-area/*
  script: main.app
  login: admin
```

Be sure to add them *before* your catch-all handler, `- url: .*`, as the handlers are read top-down.

Then try visit the URL's with a non-admin Google account and an admin Google account.
To logout of an account, go to the `/user/` endpoint and click the logout link.



## Live debugging
A powerful feature you can use with App Engine is the [Stackdriver Debug](asd), which let you set breakpoints in the code and examine the state of the app when the breakpoint is hit.
The app will not stop at the breakpoint, so the user requesting a page that hits a breakpoint will not notice anything.

Go to the Stackdriver Debug service in the [Console](https://console.cloud.google.com/) and set a breakpoint on some endpoint in your app.
For example, on the following line in the `/user/` endpoint
```
    if current_user is not None:
```

The go visit the `/user/` endpoint and then go back to Stackdriver Debug, where it now should have hit the breakpoint and you can examine the `current_user` data.



## Multiple services (modules)
*Services were previously called modules, that is why they still might be referred to as modules in the libraries.*

If you want to split your app up into microservices, or just host two different apps in the same project, it can be done by using multiple services.
Services can be deployed independently and have their own versions.
They can also be run with different runtimes, i.e., a default service is Python, and some other service is Java.

In this project, there are two services: the `default` one that you have used all the time in the `main` folder, and another one named `movie`.
Go to the directory of the movie service and install the libraries for it, as done earlier for the service in the main folder
```
pip install -t lib -r requirements.txt
```

To start the development server with both services active, you have to specify both yaml files.
When standing in the the project root directory, start the development server
```
dev_appserver.py main/app.yaml movie/app.yaml
```

If you go to `http://localhost:8000/` now, you will see that there is another service there named movie.
If you go to the movie service, it has an endpoint at `/movies/` that returns a list of movies.

Deploy the two services (I recommend you to *not* deploy both at the same time - I will explain why in the next section)
```
gcloud app deploy main/app.yaml
gcloud app deploy movie/app.yaml
```

You can now check that you have two services, both in the [Console](https://console.cloud.google.com), under the App Engine service and the *Services* tab, and in the CLI
```
gcloud app services list
```

You can now visit the two services at

* `http://<project-id>.appspot.com/`
* `http://movie.<project-id>.appspot.com`

And if you want to access a specific version of the movie service, the URL is: `http://<version>.movie.<project-id>.appspot.com`.
Also remember that *all* dots before *.appspot.com must be replaced by `-dot-` if you are using HTTPS.


### Communicating between services
If you want to communicate to any server outside your app, or between your services, you can use the [URL Fetch](https://cloud.google.com/appengine/docs/standard/python/issue-requests) library.
To make communication easier between services, there is a [Modules API](https://cloud.google.com/appengine/docs/standard/python/refdocs/google.appengine.api.modules.modules) that can be used to get the hostname of other services.

There is a `/get-movies/` endpoint setup on your `default` service that you can access to see the communication between services in action.
The endpoint will look up the hostname of the `movie` service, then make a request to the endpoint `/movies/` to retrieve a JSON list of movies, and finally format and print the result.
Go to the endpoint to see the output, and then examine the code that is run in the `main/main.py`.

#### A note on deploying multiple services separately
If a service retrieves the hostname of another service using `modules.get_hostname(module='movie')`, and both services are having a version with the same name, the hostname that is returned will *always* point to that version.
In practice, this means that if you deploy a new version of your movie service, the default service will still point to that old version.
That is why I advice you to deploy them both separately.

## Other interesting things
There are too many things in App Engine to be covered in a workshop that only spans a couple of hours.
But if you are done early, or just want to explore more of App Engine, here are a few tips:

* Set up a [cron job](https://cloud.google.com/appengine/docs/python/config/cron).
* Play around with the config file `app.yaml`. There are many options that have not been shown here. [See the documentation](https://cloud.google.com/appengine/docs/standard/python/config/appref).
* Change scaling from automatic to manual or basic for some service - [more info about the scaling types](https://cloud.google.com/appengine/docs/standard/python/an-overview-of-app-engine#scaling_types_and_instance_classes) and [how to change](https://cloud.google.com/appengine/docs/standard/python/config/appref#scaling_elements).
* Set up a project using Java. There is a quick start that get you started in the [documentation](https://cloud.google.com/appengine/docs/standard/java/quickstart).
* Set up [Task Queues](https://cloud.google.com/appengine/docs/standard/python/taskqueue/) for longer running tasks.
* [Storing persistent data](https://cloud.google.com/appengine/docs/standard/python/storage).
* [Use memcache for caching](https://cloud.google.com/appengine/docs/standard/python/memcache/).
* Set up services behind custom routes in your default service, using [dispatch.yaml](https://cloud.google.com/appengine/docs/standard/python/config/dispatchref).
* Look at the [flexible environment](https://cloud.google.com/appengine/docs/flexible/) (currently only available in beta).



## Troubleshooting

### Problem with development server and virtualenv
You do not have to use virtualenv as all libraries are downloaded to a directory, but if you for some reason have to anyways, you might get an error like the following
```
user@host $ dev_appserver.py .
Traceback (most recent call last):
  File "/opt/google-cloud-sdk/platform/google_appengine/dev_appserver.py", line 89, in <module>
    _run_file(__file__, globals())
  File "/opt/google-cloud-sdk/platform/google_appengine/dev_appserver.py", line 85, in _run_file
    execfile(_PATHS.script_file(script_name), globals_)
  File "/opt/google-cloud-sdk/platform/google_appengine/google/appengine/tools/devappserver2/devappserver2.py", line 21, in <module>
    import argparse
  File "/opt/google-cloud-sdk/lib/third_party/argparse/__init__.py", line 85, in <module>
    import copy as _copy
ImportError: No module named copy
```

A workaround to this, is to start the `dev_appserver.py` directly from the platform tools
```
python /<path>/<to>/google-cloud-sdk/platform/google_appengine/dev_appserver.py
```

Please note that this is *not* the same as the one in the `bin` directory (which is the one that is pointed to on your path)
```
/<path>/<to>/google-cloud-sdk/bin/dev_appserver.py
```
