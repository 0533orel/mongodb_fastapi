import os
from urllib.parse import quote_plus


def mongo_uri():
    uri = os.getenv("MONGO_URI", "").strip()
    if uri:
        return uri
    user = os.getenv("MONGO_USER", "")
    password = os.getenv("MONGO_PASS", "")
    if not user.strip() or not password.strip():
        raise ValueError("Set MONGO_URI or both MONGO_USER and MONGO_PASS")
    host = os.getenv("MONGO_HOST", "mongodb")
    port = int(os.getenv("MONGO_PORT", "27017"))
    database = os.getenv("MONGO_DB", "appdb")
    auth_source = os.getenv("MONGO_AUTH_SOURCE", database)
    return (f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/"
            f"{quote_plus(database)}?authSource={quote_plus(auth_source)}")
