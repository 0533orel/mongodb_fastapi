# Credential configuration

No bundled passwords are supported. Copy `.env.example` to `.env` and supply
your own values in the process environment (these Python modules do not load
dotenv files). Missing credentials fail before a database connection is opened.

For OpenShift, copy `infrastructure/k8s/mongodb.secret.env.example` to
`infrastructure/k8s/mongodb.secret.env`, fill both password fields with unique
values in an editor, then create the Secret in your authorized namespace:

```sh
oc create secret generic mongodb-secret --from-env-file=infrastructure/k8s/mongodb.secret.env -n 0533orel-dev
```

The manifests reference this Secret and no longer create one with fixed values.
Do not apply an empty template. Keep the filled file private; Git and Docker
ignore it. Do not put credentials in shell command arguments or commit them.
Existing database volumes need a provider-specific password change; editing a
Secret alone does not rotate database accounts.

Previously committed values remain in Git history. Their validity was not tested.
The service owner must revoke/rotate any reused or active values. No external
database was accessed and no history rewrite was performed.

## Verification

`python -m unittest discover -s tests -v` runs offline with fake DB clients.
Install dependencies from `requirements.txt` first. CI also runs Gitleaks with
full redaction against the current tree (including archives) and newly introduced
commits. Historical values are not claimed to be removed. Real DB/cluster and
container integration remain separate milestones.
