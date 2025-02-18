
# Deploy Wordpress with MySQL

## Add the Wordpress and MySQL Helm charts to the Catalog

## Create secrets

Create the following 2 SealedSecrets:

1. `wordpress-mysql`

- type: `opaque`
- encrypted data:

```yaml
Key=mysql-password
Value=<password>

Key=mysql-root-password
Value=<password>
```

2. `wordpress-credentials`

- type: `opaque`
- encrypted data:

```yaml
Key=mysql-password
Value=<password> # use the same password as in the wordpress-mysql SealedSecret.

Key=wordpress-password
Value=<password>
```

## Create a MySQL database

```yaml
auth:
  database: "wordpress"
  username: "wordpress"
  existingSecret: "wordpress-mysql"
```

## Deploy Wordpress

```yaml
mariadb:
  enabled: false
externalDatabase:
  host: wordpress-mysql.team-labs.svc.cluster.local
  user: wordpress
  database: wordpress
  existingSecret: "wordpress-credentials"
service:
  type: ClusterIP
existingSecret: "wordpress-credentials"
wordpressUsername: "john"
```

## Create a service to expose Wordpress

## Sign in to the Wordpress login page

Click on the URL for wordpress in the list of services

add `wp-login.php` to the url

sign-in with user `john` and password `wordpress-password`