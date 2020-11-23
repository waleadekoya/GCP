from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

spanner_client = spanner.Client()


def create_instance(instance_id):
    """Creates an instance."""

    config_name = "{}/instanceConfigs/regional-us-central1".format(
        spanner_client.project_name
    )

    instance = spanner_client.instance(
        instance_id,
        configuration_name=config_name,
        display_name="This is a display name.",
        node_count=1,
    )

    operation = instance.create()

    print("Waiting for operation to complete...")
    operation.result(120)

    print("Created instance {}".format(instance_id))


# create_instance("test-spanner")


def create_database(instance_id, database_id):
    """Creates a database and tables for sample data."""
    instance = spanner_client.instance(instance_id)

    database = instance.database(
        database_id,
        ddl_statements=[
            """CREATE TABLE Singers (
            SingerId     INT64 NOT NULL,
            FirstName    STRING(1024),
            LastName     STRING(1024),
            SingerInfo   BYTES(MAX)
        ) PRIMARY KEY (SingerId)""",
            """CREATE TABLE Albums (
            SingerId     INT64 NOT NULL,
            AlbumId      INT64 NOT NULL,
            AlbumTitle   STRING(MAX)
        ) PRIMARY KEY (SingerId, AlbumId),
        INTERLEAVE IN PARENT Singers ON DELETE CASCADE""",
        ],
    )

    operation = database.create()

    print("Waiting for operation to complete...")
    operation.result(120)

    print("Created database {} on instance {}".format(database_id, instance_id))


# create_database("test-spanner", "names")


def insert_data(instance_id, database_id):
    """Inserts sample data into the given database.

    The database and table must already exist and can be created using
    `create_database`.
    """
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.batch() as batch:
        batch.insert(
            table="Singers",
            columns=("SingerId", "FirstName", "LastName"),
            values=[
                (1, u"Marc", u"Richards"),
                (2, u"Catalina", u"Smith"),
                (3, u"Alice", u"Trentor"),
                (4, u"Lea", u"Martin"),
                (5, u"David", u"Lomond"),
            ],
        )

        batch.insert(
            table="Albums",
            columns=("SingerId", "AlbumId", "AlbumTitle"),
            values=[
                (1, 1, u"Total Junk"),
                (1, 2, u"Go, Go, Go"),
                (2, 1, u"Green"),
                (2, 2, u"Forever Hold Your Peace"),
                (2, 3, u"Terrified"),
            ],
        )

    print("Inserted data.")


# insert_data("test-spanner", "names")


def query_data(instance_id, database_id):
    """Queries sample data from the database using SQL."""
    instance = spanner_client.instance(instance_id)
    database = instance.database(database_id)

    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId, AlbumId, AlbumTitle FROM Albums"
        )

        for row in results:
            print(u"SingerId: {}, AlbumId: {}, AlbumTitle: {}".format(*row))
        print(results.metadata, type(results.metadata))


query_data("test-spanner", "names")
