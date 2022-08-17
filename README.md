
# views\_docs

A small service that proxies to various introspection routes to forward
documentation to the user.  The service also checks for optional verbose
documentation, which can also be posted to expand upon what is already provided
by the services.

## Env settings

|Key                                                          |Description                    |Default                      |
|-------------------------------------------------------------|-------------------------------|-----------------------------|
|DB_HOST                                                      |                               |                             |
|DB_PORT                                                      |                               |                             |
|DB_USER                                                      |                               |                             |
|DB_NAME                                                      |                               |                             |
|DB_SSL                                                       |                               |                             |
|BASE_DATA_RETRIEVER_URL                                      |                               |                             |
|TRANSFORMER_URL                                              |                               |                             |

## Depends-on

* [base_data_retriever](https://github.com/prio-data/base_data_retriever)
* [views_data_transformer](https://github.com/prio-data/views_data_transformer)

## Contributing

For information about how to contribute, see [contributing](https://www.github.com/prio-data/contributing).
