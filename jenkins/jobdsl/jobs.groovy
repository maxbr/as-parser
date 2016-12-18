def envVars = binding.variables

def repoUrl = envVars['REPO_URL']

def cloudKarafkaBrokers = envVars['CLOUDKARAFKA_BROKERS']
def cloudKarafkaTopicPrefix = envVars['CLOUDKARAFKA_TOPIC_PREFIX']
def cloudKarafkaCA = envVars['CLOUDKARAFKA_CA']
def cloudKarafkaCert = envVars['CLOUDKARAFKA_CERT']
def cloudKarafkaPrivateKey = envVars['CLOUDKARAFKA_PRIVATE_KEY']

def dbName = envVars['DB_NAME']
def dbUser = envVars['DB_USER']
def dbHost = envVars['DB_HOST']
def dbPassword = envVars['DB_PASSWORD']

def sslPrivateKey = envVars['PRIVATE_KEY']
def sslCertificate = envVars['CERTIFICATE']

def statsUser = envVars['STATS_USER']
def statsPassword = envVars['STATS_PASSWORD']

def dockerComposeProject = 'prod'


// containers
job('Hyper_Show_Containers') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {

        }
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

hyper ps -a
""")
    }
}


// images
job('Hyper_Show_Images') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {}
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

hyper images
""")
    }
}


// producers
['airsoftrusru', 'sharometru', 'voentursnarru'].each { SITE_SCRIPT ->
    job("Hyper_Run_Producer_${SITE_SCRIPT}") {
        logRotator(-1, 100, -1, 5)
        parameters {
            choiceParam('BRANCH', ['master', 'dev'])
            choiceParam('TAG', ['latest', 'dev'])
        }
        scm {
            git {
                remote { url(repoUrl) }
                branch('\$BRANCH')
            }
        }
        wrappers {
            preBuildCleanup { deleteDirectories() }
            environmentVariables {
                env('CLOUDKARAFKA_TOPIC_PREFIX', cloudKarafkaTopicPrefix)
                env('CLOUDKARAFKA_BROKERS', cloudKarafkaBrokers)
                env('ENV_FILE', 'env-file')
                env('DOCKER_REPO', 'maxbr/as-producer')
            }
            maskPasswordsBuildWrapper {
                varPasswordPairs {
                    varPasswordPair {
                        var('CLOUDKARAFKA_CA')
                        password(cloudKarafkaCA)
                    }
                    varPasswordPair {
                        var('CLOUDKARAFKA_CERT')
                        password(cloudKarafkaCert)
                    }
                    varPasswordPair {
                        var('CLOUDKARAFKA_PRIVATE_KEY')
                        password(cloudKarafkaPrivateKey)
                    }
                }
            }
        }
        steps {
            shell("""
source jenkins/scripts/core.sh

echo "CLOUDKARAFKA_CA=\$CLOUDKARAFKA_CA" > \$ENV_FILE
echo "CLOUDKARAFKA_CERT=\$CLOUDKARAFKA_CERT" >> \$ENV_FILE
echo "CLOUDKARAFKA_PRIVATE_KEY=\$CLOUDKARAFKA_PRIVATE_KEY" >> \$ENV_FILE

echo "CLOUDKARAFKA_TOPIC_PREFIX=\$CLOUDKARAFKA_TOPIC_PREFIX" >> \$ENV_FILE
echo "CLOUDKARAFKA_BROKERS=\$CLOUDKARAFKA_BROKERS" >> \$ENV_FILE

hyper run --size=s3 --env-file \$ENV_FILE --rm \$DOCKER_REPO:\$TAG ${SITE_SCRIPT}.py
""")
        }
    }
}


// webui
job('Hyper_Compose_Kill') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {}
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

hyper compose rm -p ${dockerComposeProject}
""")
    }
}

job('Hyper_Compose_Remove') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {}
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

hyper compose rm -p ${dockerComposeProject}
""")
    }
}

job('Hyper_Compose_Up') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {}
        environmentVariables {
            env('CLOUDKARAFKA_TOPIC_PREFIX', cloudKarafkaTopicPrefix)
            env('CLOUDKARAFKA_BROKERS', cloudKarafkaBrokers)
            env('DB_NAME', dbName)
            env('DB_USER', dbUser)
            env('DB_HOST', dbHost)
            env('STATS_USER', statsUser)
        }
        maskPasswordsBuildWrapper {
            varPasswordPairs {
                varPasswordPair {
                    var('CLOUDKARAFKA_CA')
                    password(cloudKarafkaCA)
                }
                varPasswordPair {
                    var('CLOUDKARAFKA_CERT')
                    password(cloudKarafkaCert)
                }
                varPasswordPair {
                    var('CLOUDKARAFKA_PRIVATE_KEY')
                    password(cloudKarafkaPrivateKey)
                }
                varPasswordPair {
                    var('DB_PASSWORD')
                    password(dbPassword)
                }
                varPasswordPair {
                    var('PRIVATE_KEY')
                    password(sslPrivateKey)
                }
                varPasswordPair {
                    var('CERTIFICATE')
                    password(sslCertificate)
                }
                varPasswordPair {
                    var('STATS_PASSWORD')
                    password(statsPassword)
                }
            }
        }
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

PROD_DIR=.prod
DB_ENV=\$PROD_DIR/db.env
KAFKA_ENV=\$PROD_DIR/kafka.env
SSL_ENV=\$PROD_DIR/ssl.env
STATS_ENV=\$PROD_DIR/stats.env

echo "CLOUDKARAFKA_CA=\\"\$CLOUDKARAFKA_CA\\"" > \$KAFKA_ENV
echo "CLOUDKARAFKA_PRIVATE_KEY=\\"\$CLOUDKARAFKA_PRIVATE_KEY\\"" >> \$KAFKA_ENV
echo "CLOUDKARAFKA_CERT=\\"\$CLOUDKARAFKA_CERT\\"" >> \$KAFKA_ENV
echo "CLOUDKARAFKA_TOPIC_PREFIX=\\"\$CLOUDKARAFKA_TOPIC_PREFIX\\"" >> \$KAFKA_ENV
echo "CLOUDKARAFKA_BROKERS=\\"\$CLOUDKARAFKA_BROKERS\\"" >> \$KAFKA_ENV

echo "DB_NAME=\$DB_NAME" > \$DB_ENV
echo "DB_USER=\$DB_USER" >> \$DB_ENV
echo "DB_HOST=\$DB_HOST" >> \$DB_ENV
echo "DB_PASSWORD=\$DB_PASSWORD" >> \$DB_ENV

echo "PRIVATE_KEY=\\"\$PRIVATE_KEY\\"" > \$SSL_ENV
echo "CERTIFICATE=\\"\$CERTIFICATE\\"" >> \$SSL_ENV

echo "STATS_USER=\$STATS_USER" > \$STATS_ENV
echo "STATS_PASSWORD=\$STATS_PASSWORD" >> \$STATS_ENV

hyper compose pull -f docker-compose.yml -f prod.yml
hyper compose up -p ${dockerComposeProject} -f prod.yml -d

rm -rf \$PROD_DIR
""")
    }
}

job('Hyper_Compose_Ps') {
    logRotator(-1, 100, -1, 5)
    parameters {
        choiceParam('BRANCH', ['master', 'dev'])
    }
    scm {
        git {
            remote { url(repoUrl) }
            branch('\$BRANCH')
        }
    }
    wrappers {
        preBuildCleanup { deleteDirectories() }
        environmentVariables {}
        environmentVariables {}
    }
    steps {
        shell("""
source jenkins/scripts/core.sh

hyper compose ps -p ${dockerComposeProject}
""")
    }
}


// views
listView('Producers') {
    jobs {
        regex(/Hyper_Run_Producer_.*/)
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}

listView('Consumers') {
    jobs {
        regex(/Hyper_Run_Consumer.*/)
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}

listView('HyperUtils') {
    jobs {
        name('Hyper_Show_Images')
        name('Hyper_Show_Containers')
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}

listView('WebUI') {
    jobs {
        regex(/Hyper_Compose_.*/)
    }
    columns {
        status()
        weather()
        name()
        lastSuccess()
        lastFailure()
        lastDuration()
        buildButton()
    }
}
